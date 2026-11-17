"""Add a clearly labelled generated storage image to relevant articles and cards."""
import re

def apply(out):
    figure = '<figure class="storage-editorial"><img src="/storage-editorial.webp" width="960" height="640" alt="スリーブ入りカードと透明ポケット、定規を並べた収納準備のイメージ" loading="lazy" decoding="async"><figcaption>AI生成の収納イメージ。特定の商品や実物のグッズではありません。</figcaption></figure>'
    for slug in ('photo-storage', 'photo-sleeves', 'storage-picks'):
        path = out/'notes'/f'{slug}.html'
        text = path.read_text()
        text, count = re.subn(r'(<p class="lead">.*?</p>)', lambda m: m[0]+figure, text, count=1, flags=re.S)
        if count != 1: raise RuntimeError(f'Expected one article lead: {slug}')
        path.write_text(text)
    for path in out.rglob('*.html'):
        text = path.read_text()
        # Storage only: never use this generic image for unrelated news or live equipment.
        text = re.sub(r'<span class="edit-thumb" data-cat="収納">.*?</span></span>', '<img class="edit-thumb-photo" src="/storage-editorial.webp" width="96" height="114" alt="" loading="lazy" decoding="async">', text, flags=re.S)
        path.write_text(text)
