import asyncio
import os
import secrets
import tempfile
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch
from datetime import date
import httpx
from fastapi.testclient import TestClient
from backend import main,services as svc
from backend.content import posts
from backend.db import transaction

class PortfolioTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.password=secrets.token_urlsafe()
        self.env=patch.dict(os.environ,{"LOCAL_DB":self.tmp.name+"/db","ADMIN_HASH":svc.password_hash(self.password),"SMTP_HOST":"","APP_ENV":"test","PUBLIC_ORIGIN":"http://testserver"})
        self.env.start()
        self.client=TestClient(main.app);self.client.__enter__()
    def tearDown(self):
        self.client.__exit__(None,None,None);self.env.stop();self.tmp.cleanup()
    def test_public_routes(self):
        for path in ["/","/blog","/status","/resume","/admin","/api/health","/robots.txt","/sitemap.xml","/art/social.png"]+[f"/projects/{p['slug']}" for p in main.P["projects"]]+["/certificates/0","/certificates/1"]:
            with self.subTest(path=path):self.assertEqual(self.client.get(path).status_code,200)
        for path in ["/projects/nonexistent","/blog/linux-permissions","/certificates/-1","/missing","/resume/download"]:self.assertEqual(self.client.get(path).status_code,404)
    def test_privacy_and_owner(self):
        today=str(date.today());url=f"/api/report?start={today}&end={today}"
        self.assertEqual(self.client.get(url).status_code,401)
        self.client.get("/",headers={"DNT":"1"});self.client.get("/",headers={"Sec-GPC":"1"})
        self.client.get("/projects/labquest")
        self.assertEqual(self.client.post("/api/login",json={"password":"wrong"}).status_code,401)
        self.assertEqual(self.client.post("/api/login",json={"password":self.password},headers={"Origin":"https://elsewhere.invalid"}).status_code,403)
        response=self.client.post("/api/login",json={"password":self.password})
        self.assertIn("HttpOnly",response.headers["set-cookie"])
        traffic=dict(self.client.get(url).json()["Traffic"])
        self.assertEqual(traffic["Page views"],1)
        self.assertIn("Visitor analytics",self.client.get("/admin").text)
        self.assertEqual(self.client.post("/api/logout").status_code,200)
        self.assertEqual(self.client.get(url).status_code,401)
    def test_contact(self):
        form={"name":"Reader","subject":"Portfolio","email":"user@example.org","message":"Hello"}
        for field,bad in [("email","x"),("subject","test\nBcc: extra"),("message","   ")]:
            self.assertEqual(self.client.post("/api/contact",json={**form,field:bad}).status_code,422)
        self.assertEqual(self.client.post("/api/contact",json=form).status_code,503)
        with patch.dict(os.environ,{"SMTP_HOST":"test","MAIL_FROM":"owner@example.org","MAIL_TO":"owner@example.org","SMTP_SECURITY":"local"}),patch("smtplib.SMTP") as smtp:
            smtp.return_value.__enter__.return_value.send_message.return_value={}
            self.assertIn("development",self.client.post("/api/contact",json=form).json()["message"])
            smtp.side_effect=OSError()
            self.assertEqual(self.client.post("/api/contact",json=form).status_code,502)
        with transaction() as run:self.assertEqual(run("SELECT COUNT(*) FROM contacts").fetchone()[0],1)
    def test_rate_limit(self):
        data={"password":"incorrect"}
        for _ in range(8):self.assertEqual(self.client.post("/api/login",json=data).status_code,401)
        self.assertEqual(self.client.post("/api/login",json=data).status_code,429)
    def test_blog_publishing(self):
        file=Path(self.tmp.name)/"note.md"
        file.write_text('{"status":"published","title":"A note","slug":"note","category":"Linux","tags":["Shell"],"summary":"Learning","date":"2026-11-01"}\n## Shell\n\n```bash\nls\n```\n<script>alert(1)</script>')
        data=posts(Path(self.tmp.name))
        self.assertEqual(data[0]["toc"],[("section-1","Shell")])
        with patch.object(main,"posts",return_value=data):
            html=self.client.get("/blog/note").text
            self.assertIn('id="section-1"',html);self.assertNotIn("<script>alert",html)
            self.assertIn("A note",self.client.get("/blog").text)
    def test_github_cache_and_errors(self):
        async def check():
            gh=svc.GitHub()
            gh.load=AsyncMock(return_value={"stats":{"Followers":2}})
            self.assertEqual(await gh.read("x"),await gh.read("x"));gh.load.assert_awaited_once()
            gh.until=0;gh.load.side_effect=httpx.ConnectError("offline")
            self.assertIn("cached",(await gh.read("x"))["note"])
            fail=svc.GitHub()
            fail.load=AsyncMock(side_effect=httpx.ConnectError("offline"))
            for _ in range(2):
                with self.assertRaises(svc.HTTPException):await fail.read("x")
            fail.load.assert_awaited_once()
        asyncio.run(check())
    def test_resume_and_certificate_assets(self):
        # Use temporary public fixtures. Keep sample documents outside tracked personal assets.
        with tempfile.TemporaryDirectory(dir=main.PUBLIC) as directory:
            folder=Path(directory)
            pdf=folder/"resume.pdf"
            pdf.write_bytes(b"%PDF-1.4 fixture")
            asset="/assets/"+folder.name+"/resume.pdf"
            cert={**main.P["certificates"][0],"file":asset,"verify":"https://example.org/verify"}
            with patch.dict(main.P,{"resume":asset,"certificates":[cert]}):
                self.assertIn("iframe",self.client.get("/resume").text)
                download=self.client.get("/resume/download")
                self.assertEqual(download.content,pdf.read_bytes())
                self.assertIn("attachment",download.headers["content-disposition"])
                self.assertIn("Verify with issuer",self.client.get("/certificates/0").text)
                cert["file"]="/art/hero.svg"
                self.assertIn('src="/art/hero.svg"',self.client.get("/certificates/0").text)
    def test_assets_and_metadata(self):
        html=self.client.get("/projects/labquest").text
        self.assertIn('rel="canonical"',html);self.assertIn("application/ld+json",html)
        self.assertNotIn("github.com/alishapandit228/LabQuest",html)
        self.assertNotIn("/admin",self.client.get("/sitemap.xml").text)
        self.assertIn("noindex",self.client.get("/admin").text)
    def test_github_public_api_contract(self):
        original=httpx.AsyncClient
        queried=[]
        def upstream(req):
            queried.append(req.url.path)
            if req.url.path=="/graphql":
                self.assertEqual(req.headers.get("authorization"),"Bearer test-only")
                return httpx.Response(200,json={"data":{"user":{"contributionsCollection":{"contributionCalendar":{"totalContributions":2,"weeks":[]}}}}})
            self.assertEqual(req.headers.get("authorization"),"Bearer test-only")
            if req.url.path.endswith("/repos"):data=[{"name":"Public Project","private":False,"language":"Python","stargazers_count":2,"updated_at":"2026-11-01"},{"name":"Private Project","private":True}]
            elif req.url.path.endswith("/public"):data=[{"type":"PushEvent","repo":{"name":"owner/public"}}]
            else:data={"public_repos":1,"followers":3}
            return httpx.Response(200,json=data)
        def client(**kwargs):return original(transport=httpx.MockTransport(upstream),**kwargs)
        with patch.dict(os.environ,{"GITHUB_TOKEN":"test-only"}),patch.object(httpx,"AsyncClient",side_effect=client):
            result=asyncio.run(svc.GitHub().load("owner"))
        self.assertEqual(result["stats"]["Repository stars"],2)
        self.assertEqual(result["calendar"]["totalContributions"],2)
        self.assertEqual(result["languages"],["Python"])
        self.assertEqual(len(queried),4)
