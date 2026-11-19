"""Apply reviewed editorial additions without changing advertising code."""
from pathlib import Path
import json,re
from html import escape

# User confirmed the product and requested the site Tracking ID moon12-22.
KENKO_URL = 'https://www.amazon.co.jp/dp/B0HGLYNXFL/ref=cm_sw_r_as_gl_api_gl_i_4830MMZ81CJ0A54WRMM4?linkCode=ml1&tag=moon12-22&linkId=274ae2af9296babbc8b755b1f9d4ffeb'
KENKO_PAGES = ('tools/kenko-8x21.html', 'notes/binoculars.html', 'notes/live-kit.html', 'notes/live-items-picks.html', 'notes/nogizaka-live-first.html', 'notes/sakurazaka-live-first.html', 'notes/hinatazaka-live-first.html', 'notes/sakura-6th-prep.html')
KENKO_LINK = '<a class="outlink" href="' + escape(KENKO_URL, quote=True) + '" target="_blank" rel="sponsored nofollow noopener noreferrer">⭐️Amazonのレビューを見る ↗</a>'

FAVLUV_URL = 'https://www.amazon.co.jp/dp/B0C6TDW8MG/ref=cm_sw_r_as_gl_api_gl_i_DGBV37TE9DJA1W1WMCQM?linkCode=ml1&tag=moon12-22&linkId=b5b541f62d892920eee801ee74cfa36d'
FAVLUV_PAGES = ('tools/favluv-regular.html', 'notes/photo-storage.html', 'notes/photo-sleeves.html', 'notes/storage-picks.html', 'notes/keyaki-goods-care.html')
FAVLUV_LINK = '<a class="outlink" href="' + escape(FAVLUV_URL, quote=True) + '" target="_blank" rel="sponsored nofollow noopener noreferrer">⭐️Amazonのレビューを見る ↗</a>'

MINI_URL = 'https://www.amazon.co.jp/dp/B0C6TCY9LW/ref=cm_sw_r_as_gl_api_gl_i_HBAV60C5X5QCBZYQFF43?linkCode=ml1&tag=moon12-22&linkId=08df90a6641e7994b6e93e2fbe666f20'
MINI_PAGES = ('tools/favluv-mini.html', 'notes/photo-storage.html', 'notes/photo-sleeves.html', 'notes/storage-picks.html')
MINI_LINK = '<a class="outlink" href="' + escape(MINI_URL, quote=True) + '" target="_blank" rel="sponsored nofollow noopener noreferrer">⭐️Amazonのレビューを見る ↗</a>'

def insert_purchase(text, purchase):
    marker = '<section class="edit-sources">'
    if marker in text:
        return text.replace(marker, purchase+marker, 1)
    return text.replace('</article>', purchase+'</article>', 1)


 
# Offer related items without suggesting that a historic group good is the item for sale.
DISCOVERY_PRODUCTS = {
    'index.html': ('ライブ・収納の推し活グッズ', (('ケンコーの8倍双眼鏡', KENKO_LINK), ('生写真の収納に使えるバインダー', FAVLUV_LINK), ('トレカ用のミニバインダー', MINI_LINK))),
    'checklist.html': ('席が遠いときに使える双眼鏡', (('ケンコーの8倍双眼鏡', KENKO_LINK),)),
    'size-check.html': ('写真・カードの収納用品', (('写真用のレギュラーバインダー', FAVLUV_LINK), ('トレカ用のミニバインダー', MINI_LINK))),
    'notes/real-meet-prep.html': ('持ち歩き用のカード収納', (('ファブラブ ミニバインダー', MINI_LINK),)),
    'notes/goods-20261116.html': ('生写真・トレカの収納用品', (('写真用のレギュラーバインダー', FAVLUV_LINK), ('トレカ用のミニバインダー', MINI_LINK))),
}

def related_products(rel):
    if rel in DISCOVERY_PRODUCTS:
        return DISCOVERY_PRODUCTS[rel]
    if rel.startswith('groups/') and rel != 'groups/aobazaka.html':
        return 'ライブ・収納の推し活グッズ', (('ケンコーの8倍双眼鏡', KENKO_LINK), ('生写真の収納に使えるバインダー', FAVLUV_LINK))
    if rel.startswith('goods/'):
        if any(word in rel for word in ('photo', 'holder')):
            return '生写真の収納用品', (('ファブラブ レギュラーバインダー', FAVLUV_LINK),)
        if any(word in rel for word in ('tour', 'towel', 'pen', 'summer', 'nobori')):
            return 'ライブの持ち物', (('ケンコーの8倍双眼鏡', KENKO_LINK),)
    return None


def apply(out):
    source=Path(__file__).parent
    additions=json.loads((source/'monetization-content.json').read_text())
    (out/'decision-guide.css').write_text((source/'decision-guide.css').read_text())
    for path in out.rglob('*.html'):
        if path.name.startswith('google'): continue
        text=path.read_text()
        rel=path.relative_to(out).as_posix()
        if rel in KENKO_PAGES:
            purchase = '<section class="callout"><h2>ケンコー8倍・ブラックをAmazonで確認</h2><p>ウルトラビューH 8×21DH FMC-MATBK。価格・在庫はAmazonでご確認ください。</p>' + KENKO_LINK + '</section>'
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
                text=insert_purchase(text, purchase) if rel in ('notes/nogizaka-live-first.html', 'notes/sakurazaka-live-first.html', 'notes/hinatazaka-live-first.html', 'notes/sakura-6th-prep.html', 'notes/keyaki-goods-care.html') else text.replace('</article>', purchase+'</article>', 1)
        if rel in FAVLUV_PAGES:
            purchase = '<section class="callout"><h2>ファブラブ レギュラー・黄色をAmazonで確認</h2><p>キングジム FL5210-Y（レギュラー・6穴・イエロー）。小型のミニ FL5200とは別仕様です。収納する写真・スリーブとポケット内寸を照合してください。価格・在庫・販売元はリンク先で確認できます。</p>' + FAVLUV_LINK + '</section>'
            text=insert_purchase(text, purchase) if rel in ('notes/nogizaka-live-first.html', 'notes/sakurazaka-live-first.html', 'notes/hinatazaka-live-first.html', 'notes/sakura-6th-prep.html', 'notes/keyaki-goods-care.html') else text.replace('</article>', purchase+'</article>', 1)
        if rel in MINI_PAGES:
            purchase = '<section class="callout"><h2>ファブラブ ミニ・オレンジをAmazonで確認</h2><p>キングジム FL5200-OR（ミニ・3穴・オレンジ）。小型カード向けで、L判写真用ではありません。スリーブ込みのカード寸法とポケット内寸を照合してください。レギュラー FL5210とはサイズ・穴数が異なります。価格・在庫・販売元はリンク先でご確認ください。</p>' + MINI_LINK + '</section>'
            text=insert_purchase(text, purchase) if rel in ('notes/nogizaka-live-first.html', 'notes/sakurazaka-live-first.html', 'notes/hinatazaka-live-first.html', 'notes/sakura-6th-prep.html', 'notes/keyaki-goods-care.html') else text.replace('</article>', purchase+'</article>', 1)
        if rel == 'tools.html':
            purchase = '<section class="prose"><h2>商品を選んでAmazonで確認</h2><p>型番・色を確認した3商品です。用途と寸法を比べ、必要なものを選んでください。</p>'
            purchase += '<section class="callout"><h3>ライブ用の双眼鏡：ケンコー8倍・ブラック</h3><p>ウルトラビューH 8×21DH FMC-MATBK。倍率だけでなく、視野・重さ・眼鏡での使いやすさも確認。席からの見え方を保証するものではありません。</p>'+KENKO_LINK+'</section>'
            purchase += '<section class="callout"><h3>写真・カードの整理：ファブラブ レギュラー・黄色</h3><p>FL5210-Y、6穴。収納する写真・スリーブとポケット内寸を照合してください。</p>'+FAVLUV_LINK+'</section>'
            purchase += '<section class="callout"><h3>小型カードの整理：ファブラブ ミニ・オレンジ</h3><p>FL5200-OR、3穴。L判写真用ではありません。カードをスリーブに入れた外寸と照合してください。</p>'+MINI_LINK+'</section>'
            purchase += '<p>価格・在庫・販売元・配送条件はAmazonで確認してください。実使用レビューや購入者レビューの要約は掲載していません。</p></section>'
            text=text.replace('</main>',purchase+'</main>',1)
        recommendation = related_products(rel)
        if recommendation:
            heading, products = recommendation
            entries = ''.join('<p><strong>'+name+'</strong><br>'+link+'</p>' for name, link in products)
            purchase = '<section class="prose wrap"><h2>'+heading+'</h2><p>広告</p>'+entries+'</section>'
            text = text.replace('</main>', purchase+'</main>', 1)
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
