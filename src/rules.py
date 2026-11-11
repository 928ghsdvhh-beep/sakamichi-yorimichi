"""Apply the verified-product and review publication rules."""
import re

def enforce(body):
    body=re.sub(r'<a\b[^>]*href="https://www\.amazon\.co\.jp/[^" ]*"[^>]*>.*?</a>', '', body, flags=re.S)
    body=re.sub(r'<section class="member-finder wrap".*?</section>','',body,flags=re.S)
    body=body.replace('下のリンクは商品名による検索結果を開きます。','Amazonの商品ページを特定できるまで、購入リンクは掲載していません。')
    body=body.replace('広告リンク ／ 商品名にメンバー名を加えると絞り込めます。','商品名・販売年・メンバー名を照合して確認します。')
    body=body.replace('Amazonへの検索リンクは、個別の出品・在庫・真正性を確認した商品へのリンクではありません。','Amazonへの購入リンクは、商品・型番・色・ASINを照合したものに限って掲載します。')
    body=body.replace('Amazonへのリンクは広告を含む検索リンクです。','Amazonの商品・型番・色・ASINを照合できるまで購入リンクは掲載しません。')
    body=body.replace('Amazonの検索結果が開きます。','Amazonの商品情報は確認中です。')
    if 'class="product-page"' in body:
        body=body.replace('<h2>同じグッズを見つけるために</h2>','<div class="verification-note"><strong>Amazonの商品ページは確認中です</strong><p>型番・絵柄・メンバー・ASINを照合できた商品から、商品ページと評価・レビューへのリンクを掲載します。</p></div><h2>同じグッズを見つけるために</h2>')
    return body
