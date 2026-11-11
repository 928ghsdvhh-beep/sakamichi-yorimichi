"""Site metadata from the actual generated routes; no invented product offers."""
from pathlib import Path
from html import escape, unescape
from urllib.parse import quote
import json
import re
import os

ORIGIN=os.environ.get('SITE_URL',os.environ.get('CF_PAGES_URL','https://tsukuru-desk-note.ken47com.chatgpt.site')).rstrip('/')

def finalize(out):
    routes=[]
    for path in sorted(out.rglob('*.html')):
        relative=path.relative_to(out).as_posix()
        if relative.startswith('_qa'): continue
        url=ORIGIN+('/' if relative=='index.html' else '/'+quote(relative))
        html=path.read_text()
        title=unescape(re.search(r'<title>(.*?)</title>',html).group(1))
        desc=unescape(re.search(r'<meta name="description" content="([^"]*)"',html).group(1))
        metadata=(f'<link rel="canonical" href="{url}">'
                  f'<meta property="og:locale" content="ja_JP">'
                  f'<meta property="og:type" content="website">'
                  f'<meta property="og:site_name" content="坂道よりみち">'
                  f'<meta property="og:title" content="{escape(title)}">'
                  f'<meta property="og:description" content="{escape(desc)}">'
                  f'<meta property="og:url" content="{url}">'
                  f'<meta property="og:image" content="{ORIGIN}/assets/share-card.png">'
                  f'<meta property="og:image:width" content="1200">'
                  f'<meta property="og:image:height" content="630">'
                  f'<meta property="og:image:alt" content="坂道よりみち — 坂道グッズと推し活のノート">'
                  f'<meta name="twitter:card" content="summary_large_image">')
        if relative=='404.html': metadata+='<meta name="robots" content="noindex">'
        else: routes.append(url)
        if relative=='index.html':
            schema={'@context':'https://schema.org','@type':'WebSite','name':'坂道よりみち','url':ORIGIN+'/','inLanguage':'ja','description':desc}
            metadata+='<script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False).replace('<','\\u003c')+'</script>'
        html=html.replace('</head>',metadata+'</head>')
        # Disclosure stays visible before links and is repeated in the footer.
        notice='<aside class="affiliate-notice" aria-label="広告について"><span>広告</span> Amazonのアソシエイトとして、坂道よりみちは適格販売により収入を得ています。</aside>'
        html=html.replace('</header>','</header>'+notice)
        html=re.sub(r'<div class="ad-note wrap">.*?</div>','',html,count=1)
        path.write_text(html)
    xml='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    xml+=''.join('<url><loc>'+escape(url)+'</loc></url>\n' for url in routes)+'</urlset>\n'
    (out/'sitemap.xml').write_text(xml)
    (out/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+ORIGIN+'/sitemap.xml\n')
    make_share_card(out/'assets'/'share-card.png')
    print(f'Metadata ready for {len(routes)} indexable routes')

def make_share_card(path):
    from PIL import Image,ImageDraw,ImageFont
    image=Image.new('RGB',(1200,630),'#fffdfb');draw=ImageDraw.Draw(image)
    font_path=str(Path(__file__).resolve().parents[1]/'src'/'fonts'/'ShareCardSubset.otf')
    title=ImageFont.truetype(font_path,85);sub=ImageFont.truetype(font_path,34);small=ImageFont.truetype(font_path,24)
    colors=['#8058a4','#d77891','#438eb4','#558c70','#5c9290']
    for i,color in enumerate(colors):draw.rectangle((i*240,0,(i+1)*240,10),fill=color)
    draw.rounded_rectangle((72,64,1128,566),radius=30,fill='#f2eafa')
    draw.text((125,109),'SAKAMICHI YORIMICHI',font=small,fill='#6f5584')
    draw.text((117,188),'坂道よりみち',font=title,fill='#44374c')
    draw.text((125,327),'あの日のグッズも、これからの推し活も。',font=sub,fill='#77509e')
    draw.text((125,408),'過去グッズを探す  ／  収納・参戦の道具を選ぶ',font=small,fill='#5d5862')
    draw.text((125,474),'乃木坂46・櫻坂46・日向坂46・欅坂46・青葉坂46',font=small,fill='#5d5862')
    image.save(path,optimize=True)
