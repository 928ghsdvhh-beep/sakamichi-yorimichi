"""Apply reviewed editorial additions without changing advertising code."""
from pathlib import Path
import json,re
from html import escape

# User confirmed the product and requested the site Tracking ID moon12-22.
KENKO_URL = 'https://www.amazon.co.jp/dp/B0HGLYNXFL/ref=cm_sw_r_as_gl_api_gl_i_4830MMZ81CJ0A54WRMM4?linkCode=ml1&tag=moon12-22&linkId=274ae2af9296babbc8b755b1f9d4ffeb'
KENKO_PAGES = ('tools/kenko-8x21.html', 'notes/binoculars.html', 'notes/live-kit.html', 'notes/live-items-picks.html')
KENKO_LINK = '<a class="outlink" href="' + escape(KENKO_URL, quote=True) + '" target="_blank" rel="sponsored nofollow noopener noreferrer">⭐️Amazonのレビューを見る ↗</a>'

FAVLUV_URL = 'https://www.amazon.co.jp/dp/B0C6TDW8MG/ref=cm_sw_r_as_gl_api_gl_i_DGBV37TE9DJA1W1WMCQM?linkCode=ml1&tag=moon12-22&linkId=b5b541f62d892920eee801ee74cfa36d'
FAVLUV_PAGES = ('tools/favluv-regular.html', 'notes/photo-storage.html', 'notes/photo-sleeves.html', 'notes/storage-picks.html')
FAVLUV_LINK = '<a class="outlink" href="' + escape(FAVLUV_URL, quote=True) + '" target="_blank" rel="sponsored nofollow noopener noreferrer">⭐️Amazonのレビューを見る ↗</a>'

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
            if rel in ('notes/live-kit.html', 'notes/live-items-picks.html'):
                # Keep the purchase link beside the existing model discussion.
                pattern = (r'<div class="callout">(?:(?!</div>).)*href="/tools/kenko-8x21\.html"(?:(?!</div>).)*</div>'
                           if rel == 'notes/live-kit.html' else
                           r'<p\b[^>]*>(?:(?!</p>).)*href="/tools/kenko-8x21\.html"(?:(?!</p>).)*</p>')
                anchor=re.search(pattern, text, re.S)
                if not anchor:
                    raise ValueError('Missing Kenko model discussion: '+rel)
                text=text[:anchor.end()]+purchase+text[anchor.end():]
            else:
                text=text.replace('</article>', purchase+'</article>', 1)
        if rel in FAVLUV_PAGES:
            purchase = '<section class="callout"><h2>ファブラブ レギュラー・黄色をAmazonで確認</h2><p>キングジム FL5210-Y（レギュラー・6穴・イエロー）。小型のミニ FL5200とは別仕様です。収納する写真・スリーブとポケット内寸を照合してください。価格・在庫・販売元はリンク先で確認できます。</p>' + FAVLUV_LINK + '</section>'
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
