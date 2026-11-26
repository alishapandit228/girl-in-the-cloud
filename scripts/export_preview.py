"""Export the public portfolio for review without running its backend."""
from pathlib import Path
from urllib.parse import urlsplit
from datetime import date
import re
import shutil

from bs4 import BeautifulSoup
from fastapi.testclient import TestClient
from backend.main import app
from backend.content import P, posts

out = Path("preview-output")
out.mkdir(exist_ok=False)
public = Path("frontend/public")
for folder in ("art", "enhanced", "media"):
    if (public / folder).exists():
        shutil.copytree(public / folder, out / folder)
shutil.copyfile(public / "theme.js", out / "theme.js")
css = (public / "site.css").read_text().replace("url(/art/", "url(art/")
(out / "site.css").write_text(css)
(out / "site.js").write_text((public / "site.js").read_text())

paths = ["/", "/blog", "/resume", "/status"]
paths += ["/projects/" + p["slug"] for p in P["projects"]]
paths += [f"/certificates/{i}" for i in range(len(P["certificates"]))]
paths += ["/blog/" + p["slug"] for p in posts()]
pages = {p: p.strip("/").replace("/", "-") + ".html" for p in paths}
pages["/"] = "index.html"

with TestClient(app) as client:
    for path, filename in pages.items():
        response = client.get(path)
        response.raise_for_status()
        page = BeautifulSoup(response.text, "html.parser")
        for node in page.select("[href], [src]"):
            for attr in ("href", "src"):
                url = node.get(attr, "")
                if not url.startswith("/"):
                    continue
                target = urlsplit(url)
                location = pages.get(target.path, target.path.removeprefix("/assets/").lstrip("/"))
                node[attr] = location + ("#" + target.fragment if target.fragment else "")
        form = page.select_one("#contact-form")
        if form:
            for control in form.select("button,input,textarea"):
                control["disabled"] = ""
            form.select_one("[role=status]").string = "Email delivery is disabled in this preview."
        stats = page.select_one("#github-stats")
        if stats:
            del stats["id"]
            link = page.new_tag("a", href=P["github"])
            link.string = "View current activity on GitHub ↗"
            stats.clear()
            stats.append(link)
        if path == "/status":
            detail = page.select_one(".reading")
            for item in detail.select("p"):
                item.decompose()
            note = page.new_tag("p")
            note.string = "Interactive preview. The production API is offline here."
            detail.append(note)
        robots = page.new_tag("meta", attrs={"name":"robots", "content":"noindex,nofollow"})
        page.head.append(robots)
        (out / filename).write_text(str(page))
