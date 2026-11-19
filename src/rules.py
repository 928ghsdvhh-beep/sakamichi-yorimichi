"""Apply the verified-product and review publication rules."""
import re
from monetization import KENKO_LINK, FAVLUV_LINK, MINI_LINK

APPROVED_LINKS = {KENKO_LINK, FAVLUV_LINK, MINI_LINK}

def enforce(body):
    body=re.sub(r'<a\b[^>]*href="https://www\.amazon\.co\.jp/[^" ]*"[^>]*>.*?</a>', lambda match: match[0] if match[0] in APPROVED_LINKS else '', body, flags=re.S)
    body=re.sub(r'<section class="member-finder wrap".*?</section>','',body,flags=re.S)
    body=re.sub(r'<p class="callout">Amazonの個別出品・在庫・価格・販売元・真正性は未確認です。下のリンクは商品名による検索結果を開きます。</p>', '', body)
    body=body.replace('<p class="small">広告リンク ／ 商品名にメンバー名を加えると絞り込めます。</p>', '')
    body=body.replace('<p class="section-note">Amazonの出品状況は未確認です。各ページのリンクは検索結果への案内です。</p>', '')
    return body
