import json
import re
from html import escape
from pathlib import Path
from markdown_it import MarkdownIt
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

ROOT=Path(__file__).resolve().parents[1]
P=json.loads((ROOT/"content/portfolio.json").read_text())
# Use the selected portfolio headshot as soon as its public asset is available.
portrait_filename = "1000199425.png"
if not P.get("portrait") and (ROOT / "frontend/public/art" / portrait_filename).is_file():
    P["portrait"] = f"/art/{portrait_filename}"

NAV=[
("home","Home","M3 10l9-7 9 7v10h-6v-6H9v6H3z"),
("about","About","M16 7a4 4 0 1 1-8 0 4 4 0 1 1 8 0M4 21v-2a8 8 0 0 1 16 0v2"),
("skills","Skills","M12 3l10 5-10 5L2 8zM3 13l9 5 9-5M4 18l8 4 8-4"),
("projects","Projects","M3 6h7l2 3h9v11H3z"),("achievements","Wins","M8 4h8v7a4 4 0 0 1-8 0zM8 6H4v3q0 4 5 4m7-7h4v3q0 4-5 4m-3 2v5m-5 1h10"),
("blog","Blog","M3 4q5-1 9 2 4-3 9-2v15q-5-1-9 2-4-3-9-2zM12 6v15"),
("contact","Contact","M2 5h20v14H2zM2 5l10 8L22 5")]
def code(source,lang,*_):
    try:return highlight(source,get_lexer_by_name(lang),HtmlFormatter(nowrap=True))
    except ClassNotFound:return escape(source)
def posts(directory=ROOT/"content/blogs"):
    result=[]
    md=MarkdownIt("commonmark",{"html":False,"highlight":code})
    for file in directory.glob("*.md"):
        meta,body=file.read_text().split("\n",1)
        item=json.loads(meta)
        if item["status"]!="published" or not item.get("date"):continue
        tokens=md.parse(body);toc=[]
        for i,t in enumerate(tokens):
            if t.type=="heading_open":
                title=tokens[i+1].content
                anchor=f"section-{len(toc)+1}"
                t.attrSet("id",anchor);toc.append((anchor,title))
        result.append({**item,"toc":toc,"html":md.renderer.render(tokens,md.options,{}),"minutes":max(1,(len(body.split())+199)//200)})
    return sorted(result,key=lambda a:a["date"],reverse=True)
