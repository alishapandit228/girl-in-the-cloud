import asyncio
import hashlib
import hmac
import os
import re
import secrets
import smtplib
import ssl
import time
from datetime import date, timedelta
from email.message import EmailMessage
from urllib.parse import urlparse

import httpx
from fastapi import HTTPException, Request
from pydantic import BaseModel, Field, field_validator

from .db import transaction
from .passwords import password_hash

SECRET = os.getenv("APP_SECRET") or secrets.token_hex(32)
def digest(value):
    return hmac.new(SECRET.encode(),value.encode(),hashlib.sha256).hexdigest()

def authenticated(request):
    token = request.cookies.get("owner", "")
    if not token: return False
    with transaction() as run:
        return bool(run("SELECT 1 FROM sessions WHERE token=:t AND expires>:now", t=digest(token),now=int(time.time())).fetchone())

def owner(request):
    if not authenticated(request): raise HTTPException(401,"Sign in required.")

def address(request):
    return request.client.host if request.client else "local"

def limit(request, purpose, maximum, seconds):
    now = int(time.time())
    bucket = digest(f"{purpose}|{address(request)}|{now//seconds}")
    with transaction() as run:
        run("DELETE FROM limits WHERE expires<=:now",now=now)
        hits = run("""INSERT INTO limits(bucket,hits,expires) VALUES(:b,1,:e)
                    ON CONFLICT(bucket) DO UPDATE SET hits=limits.hits+1 RETURNING hits""",
                   b=bucket,e=(now//seconds+1)*seconds).fetchone()[0]
    if hits>maximum: raise HTTPException(429,"Too many requests. Please try later.")

def validate_origin(request):
    origin = request.headers.get("origin")
    expected = os.getenv("PUBLIC_ORIGIN",str(request.base_url).rstrip("/"))
    if origin and origin != expected: raise HTTPException(403,"Origin rejected.")
    if request.headers.get("sec-fetch-site")=="cross-site": raise HTTPException(403,"Cross-site request rejected.")

class Contact(BaseModel):
    name: str = Field(min_length=1,max_length=90)
    email: str = Field(min_length=3,max_length=254)
    subject: str = Field(min_length=1,max_length=140)
    message: str = Field(min_length=1,max_length=4000)
    website: str = Field(default="",max_length=200)
    @field_validator("name","email","subject","message")
    @classmethod
    def meaningful(cls,v):
        if not v.strip(): raise ValueError("Required")
        return v.strip()
    @field_validator("name","subject","email")
    @classmethod
    def header(cls,v):
        if any(ord(c)<32 or ord(c)==127 for c in v): raise ValueError("Invalid header")
        return v
    @field_validator("email")
    @classmethod
    def email_format(cls,v):
        if not re.fullmatch(r"[^\s@<>;,]+@[^\s@<>;,]+\.[^\s@<>;,]+",v): raise ValueError("Invalid email")
        return v

def send_mail(data):
    host=os.getenv("SMTP_HOST")
    if not host or not os.getenv("MAIL_TO") or not os.getenv("MAIL_FROM"):
        raise HTTPException(503,"Email delivery is not configured yet.")
    msg=EmailMessage()
    msg["From"]=os.environ["MAIL_FROM"]; msg["To"]=os.environ["MAIL_TO"]
    msg["Reply-To"]=data.email; msg["Subject"]="Portfolio · "+data.subject
    msg.set_content(f"From {data.name}\n\n{data.message}")
    tls=os.getenv("SMTP_SECURITY","starttls")
    if tls not in ("starttls","ssl","local") or (tls=="local" and os.getenv("APP_ENV")=="production"):
        raise HTTPException(503,"Mail transport is unavailable.")
    smtp=smtplib.SMTP_SSL if tls=="ssl" else smtplib.SMTP
    try:
        with smtp(host,int(os.getenv("SMTP_PORT","587")),timeout=8) as client:
            if tls=="starttls": client.starttls(context=ssl.create_default_context())
            if os.getenv("SMTP_USER"): client.login(os.environ["SMTP_USER"],os.environ["SMTP_PASSWORD"])
            if client.send_message(msg): raise smtplib.SMTPException()
    except (OSError,smtplib.SMTPException,KeyError):
        raise HTTPException(502,"The mail server did not confirm acceptance. Please try later.") from None
    return "Message accepted by the development mailbox." if tls=="local" else "Message accepted by the email service."

def record(request,kind,path):
    if request.headers.get("dnt")=="1" or request.headers.get("sec-gpc")=="1":return
    today=date.today()
    agent=request.headers.get("user-agent","").lower()
    device="Tablet" if "tablet" in agent or "ipad" in agent else ("Mobile" if "mobile" in agent else "Desktop")
    try: ref=urlparse(request.headers.get("referer","")).hostname or "Direct"
    except ValueError: ref="Direct"
    with transaction() as run:
        run("DELETE FROM events WHERE day<:cutoff",cutoff=str(today-timedelta(days=89)))
        run("INSERT INTO events VALUES(:d,:v,:k,:p,:device,:ref)",d=str(today),v=digest(str(today)+address(request)),k=kind,p=path,device=device,ref=ref[:200])

class GitHub:
    def __init__(self):
        self.cache=None
        self.until=0
        self.lock=asyncio.Lock()
    async def read(self,username):
        async with self.lock:
            if time.monotonic()<self.until:
                if self.cache:return self.cache
                raise HTTPException(503,"GitHub activity is temporarily unavailable.")
            try: data=await asyncio.wait_for(self.load(username),timeout=12)
            except (httpx.HTTPError,TimeoutError,ValueError,KeyError):
                if self.cache:
                    self.until=time.monotonic()+60
                    self.cache={**self.cache,"note":"GitHub is unavailable. Showing the last cached snapshot."}
                    return self.cache
                self.until=time.monotonic()+60
                raise HTTPException(503,"GitHub activity is temporarily unavailable.") from None
            self.cache=data;self.until=time.monotonic()+600
            return data
    async def load(self,username):
        token=os.getenv("GITHUB_TOKEN")
        headers={"Accept":"application/vnd.github+json"}
        async with httpx.AsyncClient(base_url="https://api.github.com",headers=headers,timeout=4) as client:
            # Public REST data stays public even when a token has private repository access.
            async def get(path):
                r=await client.get(path);r.raise_for_status();return r.json()
            profile=await get("/users/"+username)
            result={"stats":{"Public repositories":profile["public_repos"],"Followers":profile["followers"]},"calendar":None}
            notes=[]
            try:
                repositories=[];page=1
                while True:
                    batch=await get(f"/users/{username}/repos?per_page=100&page={page}")
                    repositories.extend(batch)
                    if len(batch)<100:break
                    page+=1
                result["stats"]["Repository stars"]=sum(r["stargazers_count"] for r in repositories)
                result["languages"]=sorted({r["language"] for r in repositories if r["language"]})
                result["featured"]=[r["name"] for r in sorted(repositories,key=lambda r:(r["stargazers_count"],r["updated_at"]),reverse=True)[:4]]
            except httpx.HTTPError:notes.append("Repository statistics are temporarily unavailable.")
            try: result["activity"]=[e["type"].removesuffix("Event")+" · "+e["repo"]["name"] for e in (await get("/users/"+username+"/events/public"))[:3]]
            except httpx.HTTPError: notes.append("Recent activity is unavailable.")
            if token:
                query="query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount contributionLevel}}}}}}"
                try:
                    r=await client.post("/graphql",headers={"Authorization":"Bearer "+token},json={"query":query,"variables":{"login":username}})
                    r.raise_for_status();result["calendar"]=r.json()["data"]["user"]["contributionsCollection"]["contributionCalendar"]
                except (httpx.HTTPError,KeyError,TypeError):notes.append("Contribution calendar unavailable.")
            else:notes.append("Contribution calendar awaits GitHub configuration.")
            result["note"]=" ".join(notes)
            return result
github=GitHub()
