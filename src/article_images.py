"""Add clearly labelled generated images to the guide notes and the top page.

The 10 new illustrations are embedded as data: URIs (bytes in
article_image_data.py) instead of /<name>.webp file references, because the
GitHub connector accepts UTF-8 text only and cannot push binary files, and
the user stopped the browser-upload route. storage-editorial.webp stays a
real file: it was already tracked in the repo before this change.
"""
import re

from article_image_data import data_uri


def _figure(image, width, height, alt, caption):
    src = data_uri(image)
    return (f'<figure class="storage-editorial"><img src="{src}" width="{width}" height="{height}" '
            f'alt="{alt}" loading="lazy" decoding="async"><figcaption>{caption}</figcaption></figure>')

# slug -> (image, alt, caption). All images are AI-generated illustrations,
# never photos of real products or goods.
NOTE_IMAGES = {
    'past-goods': ('past-goods-editorial.webp',
        '畳んだタオルとチケット、アクスタ、ペンライトを並べた、過去のグッズを探すイメージ',
        'AI生成のイメージ。特定の商品や実物のグッズではありません。'),
    'photo-storage': ('photo-storage-editorial.webp',
        'パステル色のカードを入れたリングバインダーとアクスタ、ペンライトを並べた収納のイメージ',
        'AI生成の収納イメージ。特定の商品や実物のグッズではありません。'),
    'live-kit': ('live-kit-editorial.webp',
        '双眼鏡やタオル、ポーチ、予備電池など、ライブ参戦の持ち物を並べたイメージ',
        'AI生成の参戦準備イメージ。特定の商品や実物のグッズではありません。'),
    'buying-check': ('buying-check-editorial.webp',
        '虫眼鏡とスマートフォン、手帳を並べた、出品を確認するイメージ',
        'AI生成のイメージ。特定の商品や実物のグッズではありません。'),
    'sakura-6th-prep': ('stadium-prep-editorial.webp',
        'カードホルダーと巾着ポーチ、ペンライトを並べた、スタジアム参戦準備のイメージ',
        'AI生成の参戦準備イメージ。特定の商品や実物のグッズではありません。'),
    'binoculars': ('binoculars-editorial.webp',
        'ケースとクロスを添えた双眼鏡と、ステージの光を描いたイメージ',
        'AI生成のイメージ。特定の商品や実物ではありません。'),
    'rain-kit': ('rain-kit-editorial.webp',
        '折りたたんだレインポンチョと折りたたみ傘、ポーチを並べた雨対策のイメージ',
        'AI生成の雨対策イメージ。特定の商品や実物のグッズではありません。'),
    'acsta-carry': ('acsta-carry-editorial.webp',
        '仕切り付きの透明ケースにアクスタのパーツを収めた、持ち運びのイメージ',
        'AI生成の持ち運びイメージ。特定の商品や実物のグッズではありません。'),
    'photo-sleeves': ('photo-sleeves-editorial.webp',
        'バインダーと透明スリーブ、定規を並べた、サイズを確認するイメージ',
        'AI生成のサイズ確認イメージ。特定の商品や実物のグッズではありません。'),
}

# storage-picks keeps the generic storage image it has always used.
STORAGE_FIGURE = '<figure class="storage-editorial"><img src="/storage-editorial.webp" width="960" height="640" alt="スリーブ入りカードと透明ポケット、定規を並べた収納準備のイメージ" loading="lazy" decoding="async"><figcaption>AI生成の収納イメージ。特定の商品や実物のグッズではありません。</figcaption></figure>'

TOP_FIGURE = _figure('oshikatsu-editorial.webp', 960, 540,
    'カードを入れたバインダーとアクスタ、ペンライトを並べた推し活のイメージ',
    'AI生成の推し活イメージ。特定の商品や実物のグッズではありません。')

def _after_lead(path, figure):
    text = path.read_text()
    text, count = re.subn(r'(<p class="lead">.*?</p>)', lambda m: m[0]+figure, text, count=1, flags=re.S)
    if count != 1: raise RuntimeError(f'Expected one article lead: {path.name}')
    path.write_text(text)

def _after_hero(path, figure):
    text = path.read_text()
    start = text.find('<section class="fan-hero wrap"')
    if start < 0: raise RuntimeError('Expected fan-hero section: index')
    depth = 0
    for m in re.finditer(r'<section\b|</section>', text[start:]):
        if m[0].startswith('</'):
            depth -= 1
            if depth == 0:
                end = start + m.end()
                path.write_text(text[:end]+figure+text[end:])
                return
        else:
            depth += 1
    raise RuntimeError('Unbalanced fan-hero section: index')

def apply(out):
    for slug, (image, alt, caption) in NOTE_IMAGES.items():
        _after_lead(out/'notes'/f'{slug}.html', _figure(image, 960, 542, alt, caption))
    _after_lead(out/'notes'/'storage-picks.html', STORAGE_FIGURE)
    _after_hero(out/'index.html', TOP_FIGURE)
    for path in out.rglob('*.html'):
        text = path.read_text()
        # Storage only: never use this generic image for unrelated news or live equipment.
        text = re.sub(r'<span class="edit-thumb" data-cat="収納">.*?</span></span>', '<img class="edit-thumb-photo" src="/storage-editorial.webp" width="96" height="114" alt="" loading="lazy" decoding="async">', text, flags=re.S)
        path.write_text(text)
