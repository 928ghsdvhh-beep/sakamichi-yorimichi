"""Compact catalogue with an explicit gate for publishable product photos."""
import re

def product_layout(body):
    # Remove the decorative hero collage, keeping the concise introduction.
    if 'class="hero wrap"' in body:
        start=body.index('<div class="hero-art')
        end=body.index('</section>',start)
        body=body[:start]+body[end:]
    # Existing copied images have no recorded permission. Keep the source link.
    body=re.sub(r'<figure\b[^>]*>.*?</figure>', '', body, flags=re.S)
    body=re.sub(r'<img\b[^>]*>', '', body)
    body=re.sub(r'<svg\b.*?</svg>', '', body, flags=re.S)
    body=re.sub(r'<div class="product-art">.*?</div>', '', body, flags=re.S)
    body=re.sub(r'<div class="support-icon">.*?</div>', '', body, flags=re.S)
    body=re.sub(r'<div class="official-pick">(.*?)</div></div>',r'<div class="official-pick text-pick">\1</div></div>',body,flags=re.S)
    body=body.replace('画像出典：櫻坂46 OFFICIAL GOODS STORE ／ 在庫はリンク先で確認','商品写真・在庫は公式ページで確認')
    body=body.replace('画像出典・メーカー公式情報','メーカー公式情報')
    if 'class="hero wrap"' in body:
        start=body.index('<section class="hero wrap">')
        end=body.index('</section>',start)+len('</section>')
        body=body[:start]+'''<section class="hero wrap catalogue-intro"><p class="eyebrow">坂道グッズ・収納用品・ライブ便利グッズの紹介サイト</p><h1>坂道グッズを探すなら、<br>ここから。</h1><p class="hero-desc">買い逃したタオル・アクスタ・ペンライト。<br>生写真の収納から、次のライブの持ち物まで。</p><p class="intro-groups">乃木坂46 ／ 櫻坂46 ／ 日向坂46 ／ 欅坂46 ／ 青葉坂46</p><div class="intent-entries"><a href="#archive"><strong>過去の坂道グッズ</strong><span>タオル・アクスタ・ペンライト</span><b>買い逃したグッズを探す ↗</b></a><a href="/tools.html"><strong>生写真・アクスタの収納</strong><span>スリーブ・ファイル・ケース</span><b>収納用品を比べる ↗</b></a><a href="/notes/live-kit.html"><strong>ライブの便利グッズ</strong><span>双眼鏡・雨対策・持ち物</span><b>参戦の準備をする ↗</b></a></div><p class="intro-note">商品の紹介・探し方をまとめた非公式サイトです。購入はAmazonや公式ショップで。Amazonリンクは広告を含みます。</p></section>'''+body[end:]
    return body
