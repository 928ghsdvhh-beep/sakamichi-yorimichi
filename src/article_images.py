"""Add clearly labelled generated images to the guide notes.

The guide illustrations are embedded as data: URIs (bytes in
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

# Keep illustrations that show how the items fit together.
NOTE_IMAGES = {
    'acsta-carry': ('acsta-carry-editorial.webp',
        '持ち出す数からケースを決める',
        '仕切り付きの透明ケースにアクスタのパーツを収めた、持ち運びのイメージ',
        'AI生成の持ち運びイメージ。特定の商品や実物のグッズではありません。'),
    'photo-sleeves': ('photo-sleeves-editorial.webp',
        '見せる収納と保管用を分ける',
        'バインダーと透明スリーブ、定規を並べた、サイズを確認するイメージ',
        'AI生成のサイズ確認イメージ。特定の商品や実物のグッズではありません。'),
}


def _after_section_intro(path, heading, figure):
    text = path.read_text()
    pattern = rf'<h2>{re.escape(heading)}</h2><p>.*?</p>'
    updated, count = re.subn(pattern, lambda match: match[0] + figure, text, flags=re.S)
    if count != 1:
        raise RuntimeError(f'Expected one section intro for {heading}: {path.name}')
    path.write_text(updated)


def apply(out):
    for slug, (image, heading, alt, caption) in NOTE_IMAGES.items():
        _after_section_intro(out/'notes'/f'{slug}.html', heading, _figure(image, 960, 542, alt, caption))
    for path in out.rglob('*.html'):
        text = path.read_text()
        # Storage only: never use this generic image for unrelated news or live equipment.
        text = re.sub(r'<span class="edit-thumb" data-cat="収納">.*?</span></span>', '<img class="edit-thumb-photo" src="/storage-editorial.webp" width="96" height="114" alt="" loading="lazy" decoding="async">', text, flags=re.S)
        path.write_text(text)
