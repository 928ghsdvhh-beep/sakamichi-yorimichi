"""Small, repeatable metadata and navigation improvements for existing articles."""
from pathlib import Path
from html import escape,unescape
import re,json

def apply(out):
    for path in out.rglob('*.html'):
        if path.name.startswith('google') or path.name=='404.html':continue
        text=path.read_text()
        if not re.search(r'"@type"\s*:\s*"(?:Article|BlogPosting)"',text):continue
        canonical=re.search(r'<link\b(?=[^>]*rel=[\"\']canonical[\"\'])[^>]*href=[\"\']([^\"\']+)',text)
        heading=re.search(r'<h1[^>]*>(.*?)</h1>',text,re.S)
        if not canonical or not heading:continue
        title=unescape(re.sub('<[^>]+>','',heading[1]));url=unescape(canonical[1]);origin=url.split('/',3)[:3];home='/'.join(origin)+'/'
        if not re.search(r'class=[\"\'][^\"\']*(?:breadcrumb|crumb)',text) and '"BreadcrumbList"' not in text:
            crumb='<nav class="audit-breadcrumb" aria-label="パンくず"><a href="/">ホーム</a> <span aria-hidden="true">›</span> <span aria-current="page">'+escape(title)+'</span></nav>'
            text=text[:heading.start()]+crumb+text[heading.start():]
            data={'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'ホーム','item':home},{'@type':'ListItem','position':2,'name':title,'item':url}]}
            text=text.replace('</head>','<script type="application/ld+json">'+json.dumps(data,ensure_ascii=False).replace('<','\\u003c')+'</script></head>')
        if 'class="decision-guide"' in text:
            # A real editorial update; do not imply that all product facts were rechecked.
            def update(m):
                d=json.loads(m[1])
                if d.get('@type') in ('Article','BlogPosting'):d['dateModified']='2026-11-14'
                return '<script type="application/ld+json">'+json.dumps(d,ensure_ascii=False).replace('<','\\u003c')+'</script>'
            text=re.sub(r'<script[^>]*type=[\"\']application/ld\+json[\"\'][^>]*>(.*?)</script>',update,text,flags=re.S)
            note='<p class="editorial-update" style="font-size:12px">編集更新：2026年11月14日。選び方・比較・関連記事を補足しました。商品仕様・料金・制度の確認日は各項目の出典を参照してください。実使用レビューや購入者レビューの要約を追加したものではありません。</p>'
            marker='</article>' if '</article>' in text else '</main>'
            text=text.replace(marker,note+marker,1)
        path.write_text(text)
