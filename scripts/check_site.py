"""Read-only static checks for canonical routes, sitemap, internal links and metadata.
Run: python scripts/check_site.py [repository root]
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,urljoin,unquote,parse_qs
import json,re,sys,hashlib,xml.etree.ElementTree as ET
class Page(HTMLParser):
    def __init__(self,s):super().__init__();self.tags=[];self.feed(s)
    def handle_starttag(self,t,a):self.tags.append((t,dict(a)))
def check(repo):
    repo=repo.resolve()
    root=repo/'dist' if (repo/'dist').is_dir() else repo
    issues=[];rows=[];titles={};canonicals={};edges={}
    baseline=json.loads((repo/'scripts/affiliate-baseline.json').read_text())
    allowed_ids=set(baseline['tracking_ids'])
    def resolve(url):
        p=root/unquote(urlsplit(url).path.lstrip('/'))
        return next((x for x in (p,p.with_suffix('.html'),p/'index.html') if x.is_file()),None)
    sm=ET.parse(root/'sitemap.xml');smurls=[x.text for x in sm.findall('.//{*}loc')]
    for f in root.rglob('*.html'):
        rel=f.relative_to(root).as_posix();s=f.read_text()
        if re.fullmatch(r'google[0-9a-f]+\.html',rel):continue
        p=Page(s);canonical=[a.get('href') for t,a in p.tags if t=='link' and a.get('rel')=='canonical'];title=re.findall(r'<title>(.*?)</title>',s,re.S);descs=[a.get('content') for t,a in p.tags if t=='meta' and a.get('name')=='description'];noindex=any('noindex' in a.get('content','') for t,a in p.tags if t=='meta' and a.get('name')=='robots');h1=re.findall(r'<h1\b[^>]*>(.*?)</h1>',s,re.S)
        if rel=='404.html':
            if not noindex:issues.append([rel,'404 must be noindex'])
        else:
            for name,vals in [('title',title),('description',descs),('h1',h1),('canonical',canonical)]:
                if len(vals)!=1 or not vals[0]:issues.append([rel,name,'expected one nonempty value'])
            if canonical:
                can=canonical[0];canonicals.setdefault(can,[]).append(rel)
                if resolve(can)!=f:issues.append([rel,'canonical points to a different route',can])
                if not noindex and can not in smurls:issues.append([rel,'indexable canonical missing from sitemap',can])
                if noindex and can in smurls:issues.append([rel,'noindex included in sitemap',can])
            titles.setdefault(str(title),[]).append(rel)
        schemas=[]
        for block in re.findall(r'<script[^>]*type=[\"\']application/ld\+json[\"\'][^>]*>(.*?)</script>',s,re.S):
            try:schemas.append(json.loads(block))
            except Exception as e:issues.append([rel,'invalid JSON-LD',str(e)])
        links=[];aff=[];imgs=[]
        origin=urlsplit(canonical[0]).netloc if canonical else ''
        for t,a in p.tags:
            val=a.get('href') if t in ('a','link') else a.get('src') if t in ('img','script') else None
            if t=='img':imgs.append(a)
            if not val:continue
            u=urlsplit(val)
            if 'tag=' in val or 'a8.net' in u.netloc or u.netloc=='amzn.to':
                aff.append(val)
                if 'tag=' in val and not set(parse_qs(u.query).get('tag',[])).issubset(allowed_ids):issues.append([rel,'unexpected Tracking ID',val])
            if u.scheme and not(u.scheme in ('http','https') and u.netloc==origin):continue
            full=urljoin(canonical[0] if canonical else '/'+rel,val);target=resolve(full)
            if not target:issues.append([rel,'missing local target',val]);continue
            if t=='a':links.append(target.relative_to(root).as_posix())
            frag=urlsplit(full).fragment
            if frag and target.suffix=='.html' and not re.search(r'(?:id|name)=[\"\']'+re.escape(unquote(frag))+r'[\"\']',target.read_text()):issues.append([rel,'missing fragment',val])
        edges[rel]=links
        body=re.sub(r'<(script|style)\b.*?</\1>','',s,flags=re.S);body=re.sub('<[^>]+>',' ',body)
        rows.append(dict(path=rel,title=title[0] if title else None,h1=h1[0] if h1 else None,description=descs[0] if descs else None,canonical=canonical[0] if canonical else None,noindex=noindex,text_characters=len(re.sub(r'\s+','',body)),html_bytes=f.stat().st_size,schema_types=[d.get('@type') for d in schemas],internal_links=len(set(links)),affiliate_links=len(aff),images=len(imgs),review_summary_added=False))
    for name,mapping in [('duplicate title',titles),('duplicate canonical',canonicals)]:
        for k,v in mapping.items():
            if len(v)>1:issues.append([name,v])
    for u in smurls:
        if not resolve(u):issues.append(['sitemap','missing route',u])
    if len(smurls)!=len(set(smurls)):issues.append(['sitemap','duplicate URL'])
    reached={'index.html'};todo=['index.html']
    while todo:
        for target in edges.get(todo.pop(),[]):
            if target not in reached:reached.add(target);todo.append(target)
    for row in rows:
        row['reachable_from_home']=row['path'] in reached
        if not row['noindex'] and not row['reachable_from_home']:issues.append([row['path'],'orphan page'])
    for rel,hashes in baseline['protected_html_sha256'].items():
        file=root/rel
        if not file.exists():
            issues.append([rel,'baseline page removed']);continue
        found=sorted(hashlib.sha256(m[0].encode()).hexdigest() for m in re.finditer(r'<a\b[^>]*>.*?</a>|<img\b[^>]*>',file.read_text(),re.S) if re.search(r'(?:a8\.net/|tag=|amzn\.to/)',m[0]))
        if found!=hashes:issues.append([rel,'affiliate HTML changed'])
    return dict(site=repo.name,pages=len(rows),indexable=sum(not r['noindex'] for r in rows),sitemap_urls=len(smurls),issues=issues,page_audit=rows)
if __name__=='__main__':
    repo=Path(sys.argv[1] if len(sys.argv)>1 else Path(__file__).resolve().parents[1]);r=check(repo)
    print(json.dumps(r,ensure_ascii=False,indent=2));sys.exit(bool(r['issues']))
