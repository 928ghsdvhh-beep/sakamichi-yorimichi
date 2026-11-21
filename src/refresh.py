from html import escape
from catalog import home_gear_section

def goods_media(p, fallback):
    if p['id']=='nogi-tour-towel24':
        return '<img class="goods-photo" src="/assets/nogi-tour-towel24.jpg" alt="真夏の全国ツアー2024 マフラータオルの公式掲載画像" width="800" height="800" loading="lazy"><small class="photo-caption">公式掲載画像</small>'
    if p['id']=='nogi-summer24':
        return '<img class="goods-photo" src="/assets/nogi-summer24.jpg" alt="真夏の全国ツアー2024 個別夏タオルの公式掲載例・筒井あやめバージョン" loading="lazy" width="800" height="800"><small class="photo-caption">公式掲載例：筒井あやめ ver.</small>'
    return fallback+'<small>カテゴリイラスト</small>'

def refresh_body(body):
    if 'class="hero wrap"' in body:
        start=body.index('<div class="hero-art"')
        end=body.index('</section>', start)
        body=body[:start]+'''<div class="hero-art collage" aria-label="公式掲載グッズの写真"><span class="art-label">MY OSHI, MY FAVORITES.</span><span class="collage-sticker">推しがいる毎日に。</span><figure class="collage-photo"><img src="/assets/nogi-summer24.jpg" alt="乃木坂46 真夏の全国ツアー2024 個別夏タオルの公式掲載例" width="800" height="800"><figcaption>2024年の思い出を、もう一度。<a href="https://www.nogizaka46shop.com/product/12346" target="_blank" rel="noopener noreferrer">画像出典：乃木坂46公式ショップ ↗</a></figcaption></figure><figure class="collage-towel"><img src="/assets/sakura-6th-towel.jpg" alt="櫻坂46 6th Anniversary 箱推しマフラータオル" width="700" height="700"><figcaption>6th Anniversary<a href="https://store.plusmember.jp/sakurazaka46/products/detail.php?product_id=114906" target="_blank" rel="noopener noreferrer">画像出典：櫻坂46公式ストア ↗</a></figcaption></figure><span class="collage-star" aria-hidden="true">✳</span><span class="collage-note">あの時も、次の現場も。</span></div>'''+body[end:]
        body=body.replace('A LITTLE DETOUR, A LITTLE MORE LOVE.','坂道グッズと、推し活のよりみち。')
        body=body.replace('<h1>あの日のグッズも、<br>これからの推し活も。</h1>','<h1>あの日の<span class="word-purple">グッズ</span>も、<br>これからの<span class="word-pink">推し活</span>も。</h1>')
        body=body.replace('買い逃したタオル。忘れられない衣装のアクスタ。','買い逃したタオルも、あの衣装のアクスタも。')
        body=body.replace('過去のグッズを探す <span>↗</span>','買い逃したグッズを探す <span>↗</span>')
        body=body.replace('<section class="section wrap" id="notes">',home_gear_section()+'<section class="section wrap" id="notes">')
        marker='<div class="ad-note wrap">'
        finder='''<section class="member-finder wrap" id="member-finder"><div class="finder-title"><span class="eyebrow">FIND YOUR OSHI</span><h2>推しの名前から、探してみる。</h2><p>公演や年を足すと、欲しかったグッズに近づけます。</p></div><form id="member-form" action="https://www.amazon.co.jp/s" method="get" target="_blank" rel="noopener noreferrer"><label>グループ<select id="member-group"><option value="乃木坂46">乃木坂46</option><option value="櫻坂46">櫻坂46</option><option value="日向坂46">日向坂46</option><option value="欅坂46">欅坂46</option><option value="青葉坂46">青葉坂46</option></select></label><label>推しメン名<input id="member-name" type="text" placeholder="例：森田ひかる" maxlength="80"></label><label>グッズ・公演・年（任意）<input id="member-event" type="text" placeholder="例：2024 タオル" maxlength="120"></label><input type="hidden" name="k" id="amazon-keyword"><input type="hidden" name="tag" value="moon12-22"><a id="member-search-link" class="member-search-button" href="https://www.amazon.co.jp/s?k=%E4%B9%83%E6%9C%A8%E5%9D%8246+%E3%82%B0%E3%83%83%E3%82%BA&amp;tag=moon12-22" target="_blank" rel="sponsored noopener noreferrer">Amazonで探す ↗</a></form><p class="finder-note">広告リンク・Amazonの検索結果が開きます。入力内容は検索に使われ、当サイトでは保存しません。</p></section>'''
        body=body.replace(marker,finder+marker)
        body=body.replace('<span class="eyebrow">FIND YOUR GROUP</span>','<span class="eyebrow">あなたの好きな坂道は？</span>')
        body=body.replace('<h2>あの時のグッズを探す。</h2>','<h2>買い逃した、あのグッズ。</h2>')
        body=body.replace('>探す前に確認する <span>↗</span>','>グッズの詳細・探し方 <span>↗</span>')
        body=body.replace('<p class="eyebrow">KEEP IT. TAKE IT. ENJOY IT.</p>','<p class="eyebrow">集める・守る・現場に行く。</p>')
        body=body.replace('増えていく生写真、<br>どうしまう？','生写真を守る。<br>アクスタと出かける。')
        body=body.replace('遠い席も、雨の日も。<br>準備して楽しむ。','次の現場に、<br>これがあると助かる。')
        sample='''<div class="official-pick"><img src="/assets/sakura-6th-towel.jpg" loading="lazy" width="700" height="700" alt="櫻坂46 6th Anniversary 箱推しマフラータオルの公式商品画像"><div><span class="tag">公式ストア掲載グッズ</span><h3>櫻坂46 6th Anniversary<br>箱推しマフラータオル</h3><p>今のグッズをチェックしたい時は、まず公式ストアへ。<br>受付期間・在庫・配送時期は公式ページで確認できます。</p><a class="text-link" href="https://store.plusmember.jp/sakurazaka46/products/detail.php?product_id=114906" target="_blank" rel="noopener noreferrer">公式の商品ページを見る ↗</a><small>画像出典：櫻坂46 OFFICIAL GOODS STORE ／ 在庫はリンク先で確認</small></div></div>'''
        body=body.replace('<div class="shop-grid">',sample+'<div class="shop-grid">')
    if '<article class="prose"><p class="eyebrow">YORIMICHI NOTE 02' in body:
        pic='''<figure class="reference-photo"><img src="/assets/favluv.jpg" width="580" height="450" loading="lazy" alt="キングジム ファブラブ レギュラーサイズのメーカー説明画像"><figcaption><a href="https://www.kingjim.co.jp/sp/favluv/" target="_blank" rel="noopener noreferrer">画像出典：キングジム・ファブラブ公式ページ ↗</a><br>収納例。手持ちの生写真・アクスタとの適合は内寸を確認してください。</figcaption></figure>'''
        body=body.replace('<h2>写真と会報を分けて使える候補</h2>','<h2>写真と会報を分けて使える候補</h2>'+pic)
    if 'YORIMICHI NOTE 02' in body:
        body=body.replace('<hr>','<div class="callout"><h2>収納用品の具体例も比較</h2><p>L判用スリーブと、小型カード用・レギュラーのバインダーを分けて紹介しています。</p><a href="/tools.html">仕様付きの商品比較へ ↗</a></div><hr>')
    if 'YORIMICHI NOTE 03' in body:
        body=body.replace('<hr>','<div class="callout"><h2>軽さから双眼鏡を比べる</h2><p>8倍・190gの具体的な選択候補を、メーカー仕様とともに紹介しています。</p><a href="/tools/kenko-8x21.html">ウルトラビューHの確認ポイントへ ↗</a></div><hr>')
    if 'class="product-art"' in body and '個別夏タオル' in body:
        start=body.index('<div class="product-art">'); end=body.index('</div>',start)+6
        body=body[:start]+'''<figure class="product-art real-product"><img src="/assets/nogi-summer24.jpg" alt="個別夏タオルの公式掲載例・筒井あやめバージョン" width="800" height="800"><figcaption>公式掲載例：筒井あやめ ver.<br><a href="https://www.nogizaka46shop.com/product/12346" target="_blank" rel="noopener noreferrer">画像出典：乃木坂46公式ショップ ↗</a></figcaption></figure>'''+body[end:]
    return body
