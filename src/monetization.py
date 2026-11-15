"""Apply reviewed editorial additions without changing advertising code."""
from pathlib import Path
import json,re
from html import escape

# User confirmed the product and requested the site Tracking ID moon12-22.
KENKO_URL = 'https://www.amazon.co.jp/dp/B0HGLYNXFL/ref=cm_sw_r_as_gl_api_gl_i_4830MMZ81CJ0A54WRMM4?linkCode=ml1&tag=moon12-22&linkId=274ae2af9296babbc8b755b1f9d4ffeb'
KENKO_PAGES = ('tools/kenko-8x21.html', 'notes/binoculars.html')
KENKO_LINK = '<a class="outlink" href="' + escape(KENKO_URL, quote=True) + '" target="_blank" rel="sponsored nofollow noopener noreferrer">⭐️Amazonのレビューを見る ↗</a>'

def apply(out):
    source=Path(__file__).parent
    additions=json.loads((source/'monetization-content.json').read_text())
    (out/'decision-guide.css').write_text((source/'decision-guide.css').read_text())
    for path in out.rglob('*.html'):
        if path.name.startswith('google'): continue
        text=path.read_text()
        rel=path.relative_to(out).as_posix()
        if rel in KENKO_PAGES:
            purchase = '<section class="callout"><h2>ケンコー8倍・ブラックをAmazonで確認</h2><p>ウルトラビューH 8×21DH FMC-MATBK（ASIN：B0HGLYNXFL）。2026年11月15日に、提供されたAmazon商品画像と商品URLを照合しました。価格・在庫・販売元・配送条件はリンク先でご確認ください。購入者レビューの要約や実使用レビューは掲載していません。</p>' + KENKO_LINK + '</section>'
            text=text.replace('</article>', purchase+'</article>', 1)
        addition=additions.get(rel)
        if addition:
            # Keep additions inside the existing article column.
            marker='</article>' if '</article>' in text else '</main>'
            text=text.replace(marker,addition+marker,1)
        text=text.replace('</head>','<link rel="stylesheet" href="/decision-guide.css"></head>')
        if rel in ('goods/nogi-photo-holder24.html','goods/nogi-photo-holder25.html'):
            year='2024' if '24.html' in rel else '2025'
            text=text.replace('乃木坂46 個別生写真ホルダー｜','乃木坂46 個別生写真ホルダー '+year+'年販売分｜')
            text=text.replace('<h1>個別生写真ホルダー</h1>','<h1>個別生写真ホルダー '+year+'年販売分</h1>')
        path.write_text(text)
