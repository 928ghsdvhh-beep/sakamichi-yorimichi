from pathlib import Path
import re,json,html
from urllib.parse import quote

def text(s):
 return html.unescape(re.sub('<[^>]+>','',s)).strip()
def apply(root,origin,name,article):
 root=Path(root);origin=origin.rstrip('/');urls=[];count=0
 for p in sorted(root.rglob('*.html')):
  rel=p.relative_to(root).as_posix()
  if rel.startswith('_') or re.fullmatch(r'google[0-9a-f]+\.html',rel):continue
  h=p.read_text()
  if not re.search(r'<head[ >]',h):
   h=re.sub(r'(<html[^>]*>)',r'\1<head>',h,count=1)
   h=re.sub(r'(<body\b|<main\b)',r'</head>\1',h,count=1)
  url=origin+('/' if rel=='index.html' else '/'+quote(rel[:-5]))
  title=text(re.search(r'<title>(.*?)</title>',h,re.S).group(1))
  dm=re.search(r'<meta\b(?=[^>]*name=[\"\']description[\"\'])[^>]*content=[\"\']([^\"\']*)',h)
  desc=html.unescape(dm.group(1)) if dm else (name+'の編集方針・広告掲載・情報の確認方法について。' if rel=='about.html' else name+'における個人情報・広告・アクセス解析の取り扱いについて。')
  if not dm and rel!='404.html':h=h.replace('</head>',f'<meta name="description" content="{html.escape(desc,quote=True)}"></head>')
  h=re.sub(r'<link\b(?=[^>]*rel=[\"\']canonical[\"\'])[^>]*>','',h)
  if rel=='404.html':
   h=re.sub(r'<meta\b(?=[^>]*name=[\"\']robots[\"\'])[^>]*>','',h)
   h=h.replace('</head>','<meta name="robots" content="noindex,follow"></head>');p.write_text(h);continue
  h=h.replace('</head>',f'<link rel="canonical" href="{url}"></head>')
  # Correct internal schema URLs as well as canonical; keep dates, citations and all factual fields.
  def schema(m):
   d=json.loads(m.group(1))
   def walk(x):
    if isinstance(x,dict):
     for k,v in list(x.items()):
      if isinstance(v,str) and v.startswith(origin) and v.endswith('.html'):x[k]=v[:-5]
      else:walk(v)
    elif isinstance(x,list):
     for v in x:walk(v)
   walk(d)
   if d.get('@type') in ('Article','BlogPosting'):
    d['mainEntityOfPage']=url;d['url']=url
   return '<script type="application/ld+json">'+json.dumps(d,ensure_ascii=False).replace('<','\\u003c')+'</script>'
  h=re.sub(r'<script[^>]*type=[\"\']application/ld\+json[\"\'][^>]*>(.*?)</script>',schema,h,flags=re.S)
  isarticle=article(rel);schemas=[json.loads(x) for x in re.findall(r'<script[^>]*type=[\"\']application/ld\+json[\"\'][^>]*>(.*?)</script>',h,re.S)]
  types={d.get('@type') for d in schemas if isinstance(d.get('@type'),str)}
  h1=re.search(r'<h1[^>]*>(.*?)</h1>',h,re.S);headline=text(h1.group(1)) if h1 else title
  if isarticle and not types.intersection({'Article','BlogPosting'}):
   d={'@context':'https://schema.org','@type':'Article','headline':headline,'description':desc,'inLanguage':'ja','mainEntityOfPage':url,'url':url}
  elif rel=='index.html' and 'WebSite' not in types:
   d={'@context':'https://schema.org','@type':'WebSite','name':name,'url':origin+'/','inLanguage':'ja','description':desc}
  elif not isarticle and rel!='index.html' and not types.intersection({'WebPage','AboutPage','CollectionPage'}):
   d={'@context':'https://schema.org','@type':'AboutPage' if rel=='about.html' else 'WebPage','name':headline,'url':url,'inLanguage':'ja','description':desc}
  else:d=None
  if d:h=h.replace('</head>','<script type="application/ld+json">'+json.dumps(d,ensure_ascii=False).replace('<','\\u003c')+'</script></head>')
  # Existing noindex decisions are preserved and omitted from the sitemap.
  if not re.search(r'<meta\b(?=[^>]*name=[\"\']robots[\"\'])(?=[^>]*content=[\"\'][^\"\']*noindex)[^>]*>',h):urls.append(url)
  h=re.sub(r'(<meta\b[^>]*property=[\"\']og:url[\"\'][^>]*content=[\"\'])[^\"\']*',lambda m:m.group(1)+url,h)
  p.write_text(h);count+=1
 (root/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join('<url><loc>'+html.escape(u)+'</loc></url>\n' for u in urls)+'</urlset>\n')
 print(name,count,'pages;',len(urls),'indexable')
