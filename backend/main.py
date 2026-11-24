import hmac
import json
import os
import secrets
import time
from contextlib import asynccontextmanager
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlparse
from xml.etree.ElementTree import Element, SubElement, tostring

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response, FileResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pydantic import BaseModel, Field
from starlette.exceptions import HTTPException as StarletteError

from . import services as svc
from .content import NAV,P,ROOT,posts
from .db import init, transaction

PUBLIC=ROOT/"frontend/public"
templates=Environment(loader=FileSystemLoader(ROOT/"frontend/templates"),autoescape=select_autoescape())
started=time.monotonic()
def prod():return os.getenv("APP_ENV")=="production"

@asynccontextmanager
async def lifespan(app):
    if prod():
        if (len(os.getenv("APP_SECRET",""))<32 or not os.getenv("ADMIN_HASH") or not os.getenv("DATABASE_URL")
                or not os.getenv("PUBLIC_ORIGIN","").startswith("https://")):
            raise RuntimeError("Production requires HTTPS origin, database, owner hash and a strong app secret.")
    if not (PUBLIC/'art/social.png').exists():
        from scripts.social import generate
        generate()
    init()
    yield

app=FastAPI(lifespan=lifespan,docs_url=None,redoc_url=None,openapi_url=None)
app.mount("/art",StaticFiles(directory=PUBLIC/"art"),name="art")
app.mount("/assets",StaticFiles(directory=PUBLIC),name="assets")
if (PUBLIC/"enhanced").is_dir():app.mount("/enhanced",StaticFiles(directory=PUBLIC/"enhanced"),name="enhanced")

@app.middleware("http")
async def headers(request,call_next):
    response=await call_next(request)
    response.headers.update({
        "Content-Security-Policy":"default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self'; frame-src 'self'; frame-ancestors 'self'; base-uri 'none'; form-action 'self'; object-src 'none'",
        "X-Content-Type-Options":"nosniff","Referrer-Policy":"strict-origin-when-cross-origin",
        "Permissions-Policy":"camera=(), microphone=(), geolocation=()"})
    if request.url.path.startswith(("/admin","/api/")):response.headers["Cache-Control"]="no-store"
    if prod():response.headers["Strict-Transport-Security"]="max-age=31536000"
    return response

def origin(request):
    return os.getenv("PUBLIC_ORIGIN",str(request.base_url).rstrip("/")).rstrip("/")

def render(request,title,*,template="page.html",status=200,**context):
    private=request.url.path.startswith("/admin")
    desc=context.pop("desc",P["tagline"]+" "+P["name"]+" · "+P["title"])
    canonical=origin(request)+request.url.path
    structured={"@context":"https://schema.org","@type":"WebPage","name":title,"url":canonical,"description":desc}
    if request.url.path=="/":structured["about"]={"@type":"Person","name":P["name"],"sameAs":[P["github"]]}
    if context.get("article"):structured.update({"@type":"BlogPosting","headline":title,"datePublished":context["article"]["date"]})
    html=templates.get_template(template).render(title=title,p=P,nav=NAV,desc=desc,canonical=canonical,origin=origin(request),private=private,structured=structured,enhanced=(PUBLIC/"enhanced/scene.js").is_file(),**context)
    if not private and status==200:svc.record(request,"view",request.url.path)
    return HTMLResponse(html,status_code=status)

@app.get("/")
def home(request:Request):return render(request,"Alisha Pandit · Aspiring Cloud Engineer",template="home.html",articles=posts())

@app.get("/projects/{slug}")
def project(request:Request,slug:str):
    item=next((p for p in P["projects"] if p["slug"]==slug),None)
    if not item:raise HTTPException(404)
    return render(request,item["name"],project=item,kicker="PROJECT CASE STUDY",desc=item["summary"])

@app.get("/blog")
def blog(request:Request):
    articles=posts()
    return render(request,"Cloud field notes",mode="blog",kicker="TECHNICAL JOURNAL",articles=articles,categories=sorted({a["category"] for a in articles}))

@app.get("/blog/{slug}")
def article(request:Request,slug:str):
    articles=posts();item=next((a for a in articles if a["slug"]==slug),None)
    if not item:raise HTTPException(404)
    related=[a for a in articles if a!=item and (a["category"]==item["category"] or set(a["tags"])&set(item["tags"]))]
    return render(request,item["title"],article=item,kicker="FIELD NOTE",related=related[:3],desc=item["summary"])

@app.get("/certificates/{idx}")
def certificate(request:Request,idx:int):
    if not 0<=idx<len(P["certificates"]):raise HTTPException(404)
    cert=P["certificates"][idx]
    return render(request,cert["name"],cert=cert,kicker="CERTIFICATION")

@app.get("/resume")
def resume(request:Request):return render(request,"Professional résumé",mode="resume",kicker=P["name"].upper())

@app.get("/resume/download")
def resume_download(request:Request):
    if not P["resume"] or not P["resume"].startswith("/assets/"):raise HTTPException(404)
    path=(PUBLIC/P["resume"].removeprefix("/assets/")).resolve()
    if not path.is_relative_to(PUBLIC) or not path.is_file():raise HTTPException(404)
    svc.record(request,"download","/resume/download")
    return FileResponse(path,filename="Alisha-Pandit-Resume.pdf",media_type="application/pdf")

@app.get("/status")
def status(request:Request):
    return render(request,"Service status",mode="status",version=os.getenv("APP_VERSION","development"),build=os.getenv("BUILD_ID"),deployed=os.getenv("DEPLOYED_AT"))

@app.get("/api/health")
def health():
    with transaction() as run:run("SELECT 1").fetchone()
    return {"status":"ok","version":os.getenv("APP_VERSION","development")}

@app.get("/api/github")
async def github():return await svc.github.read(P["username"])

@app.post("/api/contact")
def contact(request:Request,data:svc.Contact):
    svc.validate_origin(request);svc.limit(request,"contact",5,600)
    if data.website:raise HTTPException(400,"Unable to accept this submission.")
    message=svc.send_mail(data)
    with transaction() as run:
        run("DELETE FROM contacts WHERE created<:cutoff",cutoff=int(time.time())-90*86400)
        run("INSERT INTO contacts VALUES(:id,:now,'accepted')",id=secrets.token_hex(12),now=int(time.time()))
    return {"message":message}

class Login(BaseModel):
    password:str=Field(min_length=1,max_length=512)

@app.post("/api/login")
def login(request:Request,data:Login,response:Response):
    svc.validate_origin(request);svc.limit(request,"login",8,900)
    stored=os.getenv("ADMIN_HASH")
    if not stored:raise HTTPException(503,"Owner access is not configured.")
    if not hmac.compare_digest(svc.password_hash(data.password,stored.split(".")[0]),stored):raise HTTPException(401,"Sign-in unsuccessful.")
    token=secrets.token_urlsafe(32);now=int(time.time())
    with transaction() as run:
        run("DELETE FROM sessions WHERE expires<=:now",now=now)
        run("INSERT INTO sessions VALUES(:t,:e)",t=svc.digest(token),e=now+7200)
    response.set_cookie("owner",token,httponly=True,secure=prod(),samesite="strict",max_age=7200,path="/")
    return {"ok":True}

@app.post("/api/logout")
def logout(request:Request,response:Response):
    svc.validate_origin(request);svc.owner(request)
    with transaction() as run:run("DELETE FROM sessions WHERE token=:t",t=svc.digest(request.cookies["owner"]))
    response.delete_cookie("owner",path="/",secure=prod(),httponly=True,samesite="strict")
    return {"ok":True}

@app.get("/admin")
def admin(request:Request):
    if not svc.authenticated(request):return render(request,"Owner sign-in",mode="login")
    return render(request,"Visitor analytics",mode="dashboard",start=date.today()-timedelta(days=29),end=date.today())

@app.get("/api/report")
def report(request:Request,start:date,end:date):
    svc.owner(request)
    if end<start or (end-start).days>366:raise HTTPException(422,"Choose a range of up to one year.")
    params={"a":str(start),"b":str(end)}
    scope=" FROM events WHERE day BETWEEN :a AND :b"
    with transaction() as run:
        counts=run("SELECT COUNT(*),COUNT(DISTINCT visitor)"+scope+" AND kind='view'",**params).fetchone()
        downloads=run("SELECT COUNT(*)"+scope+" AND kind='download'",**params).fetchone()[0]
        def epoch(d):return int(datetime.combine(d,datetime.min.time(),tzinfo=timezone.utc).timestamp())
        contacts=run("SELECT COUNT(*) FROM contacts WHERE created>=:a AND created<:b",a=epoch(start),b=epoch(end+timedelta(days=1))).fetchone()[0]
        result={"Traffic":[["Page views",counts[0]],["Estimated visitor-days",counts[1]],["Résumé downloads",downloads],["Accepted contact submissions",contacts]]}
        for label,column,extra in [("Daily traffic","day",""),("Monthly traffic","substr(day,1,7)",""),("Top pages","path",""),("Project views","path"," AND path LIKE '/projects/%'"),("Devices","device",""),("Referrers","referrer","")]:
            order="1" if "traffic" in label else "2 DESC,1"
            rows=run(f"SELECT {column},COUNT(*)"+scope+f" AND kind='view'{extra} GROUP BY 1 ORDER BY {order} LIMIT 366",**params)
            result[label]=[list(r) for r in rows]
        result["Application metrics"]=[["Process age (seconds)",int(time.monotonic()-started)]]
    return result

@app.get("/robots.txt")
def robots(request:Request):return Response(f"User-agent: *\nDisallow: /admin\nDisallow: /api/\nSitemap: {origin(request)}/sitemap.xml\n",media_type="text/plain")

@app.get("/sitemap.xml")
def sitemap(request:Request):
    root=Element("urlset",xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    paths=["/","/blog","/resume","/status"]+["/projects/"+p["slug"] for p in P["projects"]]+["/blog/"+a["slug"] for a in posts()]+[f"/certificates/{i}" for i in range(len(P["certificates"]))]
    for path in paths:SubElement(SubElement(root,"url"),"loc").text=origin(request)+path
    return Response(tostring(root,encoding="utf-8"),media_type="application/xml")

@app.exception_handler(StarletteError)
async def error(request,exc):
    from fastapi.responses import JSONResponse
    if exc.status_code==404 and not request.url.path.startswith("/api/"):return render(request,"Page not found",status=404)
    return JSONResponse({"detail":exc.detail},status_code=exc.status_code)
