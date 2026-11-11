from pathlib import Path
from html import escape as e
from urllib.parse import urlencode
import json
from refresh import refresh_body, goods_media
from catalog import EXTRA_GOODS, render_gear_pages
from seo import finalize
from editorial import render as render_editorial
from rules import enforce
from photo_layout import product_layout
from expansion import NEW_GUIDES, NEW_GOODS, render as render_expansion

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'dist'
GROUPS={'nogizaka':('乃木坂46','#8058a4'),'sakurazaka':('櫻坂46','#d77891'),'hinatazaka':('日向坂46','#438eb4'),'keyakizaka':('欅坂46','#558c70'),'aobazaka':('青葉坂46','#5c9290')}
TAG='moon12-22'
def amazon(q): return 'https://www.amazon.co.jp/s?'+urlencode({'k':q,'tag':TAG})
def ext(url,label,affiliate=False):
 if affiliate: return ''
 return f'<a class="outlink" href="{e(url)}" target="_blank" rel="{"sponsored " if affiliate else ""}noopener noreferrer">{label} ↗</a>'

items=[
dict(id='nogi-summer24',g='nogizaka',year='2024',kind='タオル',title='個別夏タオル',event='真夏の全国ツアー2024',state='掲載受付終了',note='参照した公式販売ページで受付終了を確認。他の受付枠や再販の有無は公式ショップでも確認してください。',source='https://www.nogizaka46shop.com/product/12346',q='乃木坂46 真夏の全国ツアー2024 個別夏タオル',tip='「夏タオル」と「マフラータオル」は別アイテム。年・メンバー名・絵柄を照合しましょう。'),
dict(id='sakura-acsta24',g='sakurazaka',year='2024',kind='アクスタ',title='アクリルスタンドキーホルダー',event='4th YEAR ANNIVERSARY LIVE 販売分',state='過去の販売情報',note='公式告知で当時の販売を確認。現在の公式在庫・販売終了は未確認です。',source='https://sakurazaka46.com/s/s46/news/detail/G00123',q='櫻坂46 4th ARENA TOUR IN 東京ドーム オープニング衣装 アクリルスタンド',tip='2024年の周年グッズで販売された東京ドームのオープニング衣装版。周年のロゴだけで判断せず、衣装とメンバーを確認。'),
dict(id='sakura-charm24',g='sakurazaka',year='2024',kind='小物',title='メンバーカラーのチャームセット',event='4th YEAR ANNIVERSARY LIVE',state='過去の販売情報',note='公式告知で当時の販売を確認。現在の公式在庫・販売終了は未確認です。',source='https://sakurazaka46.com/s/s46/news/detail/G00123',q='櫻坂46 4th YEAR ANNIVERSARY LIVE チャームセット',tip='セットの一部だけの出品か、セット一式かを確認。名前やカラー、パーツの欠品も見ておきましょう。'),
dict(id='hinata-photo25',g='hinatazaka',year='2025',kind='収納グッズ',title='個別フォトアルバム',event='卒業写真だけが知ってる',state='過去の販売情報',note='2025年の公式販売告知を参照。現在の公式在庫・販売終了は未確認です。',source='https://www.hinatazaka46.com/s/official/news/detail/G00171',q='日向坂46 卒業写真だけが知ってる 個別フォトアルバム',tip='アルバム本体の出品か、生写真のみの出品かを区別。収納サイズや付属リフィルの有無も確認。'),
dict(id='keyaki-pen18',g='keyakizaka',year='2018',kind='ペンライト',title='欅坂46／けやき坂46 公式ペンライト',event='欅共和国2018 販売分',state='過去の販売情報',note='当時の公式告知で発売を確認。現在の公式販売状況は未確認です。',source='https://www.keyakizaka46.com/s/k46o/news/detail/G00060',q='欅坂46 けやき坂46 欅共和国2018 公式ペンライト',tip='発光とボタンの動作、液漏れ、電池ぶた、ストラップを確認。コレクション用とライブで使う目的は分けて選びましょう。')]

items.extend(EXTRA_GOODS + NEW_GOODS)

guides=[
('past-goods','01','あの時のグッズを、もう一度。','過去の公式グッズの探し方','販売年・公演・衣装・メンバーから、欲しかった一点に近づく。'),
('photo-storage','02','集めた生写真を、きれいに。','生写真とアクスタの収納選び','スリーブを入れた後のサイズまで確認するのがポイント。'),
('live-kit','03','当日は、ライブに集中したい。','参戦グッズの選び方','遠い席・雨の日・増える荷物。困る場面から持ち物を選ぶ。'),
('buying-check','04','届いてから、がっかりしないために。','中古・マーケットプレイスの確認点','公式グッズという商品と、公式ショップという販売元を区別。')]

guides.extend(NEW_GUIDES)

def header():
 return '<a class="skip" href="#main">本文へ</a><header><a class="brand" href="/"><span class="brand-mark">↗</span><span>坂道よりみち<small>SAKAMICHI YORIMICHI</small></span></a><nav aria-label="メイン"><a href="/#archive">過去グッズ</a><a href="/#official">公式ショップ</a><a href="/#support">収納・参戦</a><a href="/#notes">読みもの</a></nav><span class="header-note">好きの、その先へ。</span></header>'
def footer():
 return '<footer><div class="footer-top"><a class="brand" href="/">坂道よりみち</a><div><a href="/about.html">このサイトについて</a><a href="/privacy.html">プライバシー・広告表示</a></div></div><p>当サイトは非公式のグッズ案内サイトです。各グループ・運営会社とは関係ありません。</p><p>Amazonのアソシエイトとして、坂道よりみちは適格販売により収入を得ています。Amazonへのリンクには広告リンクを含みます。</p><p>価格・在庫・販売元・商品の状態はリンク先でご確認ください。掲載情報の確認日：2026年11月8日</p><small>© 2026 坂道よりみち</small></footer>'
def page(title,body,description='坂道の過去グッズを公演・年・種類から探す。公式ショップへの案内と、収納・ライブ参戦の道具選びも。'):
 body=enforce(product_layout(refresh_body(body)))
 return '<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+e(title)+'｜坂道よりみち</title><meta name="description" content="'+e(description)+'"><meta name="theme-color" content="#faf8f4"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/style.css"><link rel="stylesheet" href="/refresh.css?v=4"><link rel="stylesheet" href="/catalog.css?v=5"><link rel="stylesheet" href="/release.css"><link rel="stylesheet" href="/product-layout.css?v=3"><link rel="stylesheet" href="/expansion.css?v=1"><script defer src="/app.js?v=5"></script><script defer src="/utilities.js?v=1"></script></head><body>'+header()+'<main id="main">'+body+'</main>'+footer()+'</body></html>'
def icon(kind):
 shapes={'タオル':'<rect x="22" y="40" width="156" height="45" rx="3"/><path d="M31 43v39M169 43v39M60 53h80M72 64h56M60 75h80"/>','アクスタ':'<path d="M76 109h48l-3-9H79zM92 35a11 11 0 1 0 16 0M91 53l-12 26 10 4 2-10-3 26h24l-3-26 2 10 10-4-12-26z"/>','ペンライト':'<rect x="87" y="13" width="26" height="69" rx="12"/><rect x="90" y="82" width="20" height="32" rx="4"/><circle cx="100" cy="94" r="3"/>','小物':'<circle cx="94" cy="35" r="16"/><path d="M94 51v10M71 62h46v42H71zM80 72h28M80 83h28M80 94h17"/>','収納グッズ':'<rect x="54" y="17" width="92" height="101" rx="5"/><path d="M66 17v101M77 34h24v29H77zM110 34h24v29h-24zM77 72h24v29H77zM110 72h24v29h-24z"/>','双眼鏡':'<path d="M50 51l11-27h27v57H44zM150 51l-11-27h-27v57h44zM88 40h24v17H88z"/><ellipse cx="66" cy="83" rx="24" ry="15"/><ellipse cx="134" cy="83" rx="24" ry="15"/>'}
 return '<svg aria-hidden="true" viewBox="0 0 200 130" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round">'+shapes.get(kind,shapes['収納グッズ'])+'</svg>'
def card(p):
 name,color=GROUPS[p['g']]
 return f'<article class="goods-card compact-product" data-group="{p["g"]}" data-kind="{e(p["kind"])}" data-year="{p["year"]}" data-search="{e(name+p["title"]+p["kind"]+p["event"]+p["year"])}" style="--group:{color}"><div class="goods-body"><p class="product-category">{e(p["kind"])} <span>{p["year"]}</span></p><span class="eyebrow group-name">{name}</span><h3><a href="/goods/{p["id"]}.html">{e(p["title"])}</a></h3><p>{e(p["event"])}</p><span class="status">{p["state"]}</span><a class="official-photo-link" href="{e(p["source"])}" target="_blank" rel="noopener noreferrer">公式の商品写真・販売情報 ↗</a><a class="detail-link" href="/goods/{p["id"]}.html">Amazonでの探し方・確認点 ↗</a></div></article>'
def guides_grid():
 return '<div class="guide-grid">'+''.join(f'<a class="guide-card" href="/notes/{slug}.html"><span class="guide-number">{n}</span><div><small>{e(kicker)}</small><h3>{e(title)}</h3><p>{e(desc)}</p></div><span>↗</span></a>' for slug,n,kicker,title,desc in guides)+'</div>'

hero='''<section class="hero wrap"><div class="hero-copy"><p class="eyebrow">A LITTLE DETOUR, A LITTLE MORE LOVE.</p><h1>あの日のグッズも、<br>これからの推し活も。</h1><p class="hero-desc">買い逃したタオル。忘れられない衣装のアクスタ。<br>坂道の「欲しかった」と「あると便利」を、ここから。</p><a class="button" href="#archive">過去のグッズを探す <span>↗</span></a><p class="hero-caption">乃木坂46 / 櫻坂46 / 日向坂46 / 欅坂46 / 青葉坂46</p></div><div class="hero-art" aria-label="推し活の道具を描いたイメージイラスト"><span class="art-label">THE THINGS WE LOVE.</span><div class="art-orbit"></div><div class="art-towel">あの日も、これからも。<span>MY FAVORITE MEMORIES</span></div><div class="art-album"><span>MY<br>COLLECTION</span><i></i><i></i><i></i><i></i></div><div class="art-stick"></div><div class="art-ticket"><span>ONE DAY<br>ONE MEMORY</span><b>↗</b></div><span class="art-spark">✳</span><small>イメージイラスト・実際の商品ではありません</small></div></section>'''
groups='<section class="group-strip wrap" aria-label="グループ別"><span class="eyebrow">FIND YOUR GROUP</span><div>'+''.join(f'<a style="--group:{color}" href="/groups/{slug}.html"><i></i>{name}<span>↗</span></a>' for slug,(name,color) in GROUPS.items())+'</div></section>'
archive='''<section class="section wrap" id="archive"><div class="section-heading"><div><p class="eyebrow">PAST GOODS ARCHIVE</p><h2>あの時のグッズを探す。</h2></div><p>公演名と年をたどって、<br>欲しかった一点に。</p></div><div class="search-panel"><label for="query">グッズ名・公演名で検索</label><div class="search-line"><span aria-hidden="true">⌕</span><input id="query" type="search" placeholder="例：欅共和国 2018、アクスタ" autocomplete="off"><button id="clear" type="button">条件をクリア</button></div><div class="filters"><label>グループ<select id="group"><option value="all">すべてのグループ</option>'''+''.join(f'<option value="{g}">{v[0]}</option>' for g,v in GROUPS.items())+'''</select></label><label>種類<select id="kind"><option value="all">すべての種類</option>'''+''.join(f'<option>{k}</option>' for k in sorted(set(p['kind'] for p in items)))+'''</select></label><label>販売年<select id="year"><option value="all">すべての年</option>'''+''.join(f'<option>{y}</option>' for y in sorted(set(p['year'] for p in items),reverse=True))+'''</select></label><p id="count" role="status" aria-live="polite">'''+str(len(items))+'''件の販売記録</p></div></div><p class="section-note">公式の過去販売記録をもとにした検索ガイドです。Amazonの出品・在庫は未確認。商品ページでの「買える」表示ではありません。</p><div id="goods-grid" class="goods-grid">'''+''.join(card(p) for p in items)+'''</div><div id="empty" class="empty" hidden><h3>この条件の掲載はまだありません。</h3><p>条件を減らすか、グループ別ページから公式情報をご確認ください。</p></div></section>'''
official='''<section class="official-section" id="official"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">OFFICIAL FIRST</p><h2>今のグッズは、まず公式へ。</h2></div><p>現行商品・再販・受注受付を確認。<br>在庫や受付期間は公式ショップで。</p></div><div class="shop-grid">'''+''.join(f'<a target="_blank" rel="noopener noreferrer" href="{url}" class="shop" style="--group:{GROUPS[g][1]}"><span>{GROUPS[g][0]}</span><small>OFFICIAL GOODS STORE</small><b>公式ショップへ ↗</b></a>' for g,url in [('nogizaka','https://www.nogizaka46shop.com/'),('sakurazaka','https://store.plusmember.jp/sakurazaka46/'),('hinatazaka','https://store.plusmember.jp/hinatazaka46/')])+'''</div><div class="aoba-note"><span class="tag">青葉坂46</span><p>新しい坂道の歩みも。商品情報は公式発表で確認できたものから掲載します。</p><a href="https://aobazaka46.com/" target="_blank" rel="noopener noreferrer">公式情報へ ↗</a></div></div></section>'''
support='''<section class="section wrap" id="support"><div class="section-heading"><div><p class="eyebrow">KEEP IT. TAKE IT. ENJOY IT.</p><h2>好きなものを、大切に。<br>ライブの日を、身軽に。</h2></div><p>収納も、持ち物も。<br>困る場面から選んでみる。</p></div><div class="support-grid"><a class="support-card purple" href="/notes/photo-storage.html"><div class="support-icon">'''+icon('収納グッズ')+'''</div><span class="eyebrow">STORAGE</span><h3>増えていく生写真、<br>どうしまう？</h3><p>スリーブ・ファイル・アクスタケース。入れた後のサイズまで。</p><b>収納の選び方 ↗</b></a><a class="support-card blue" href="/notes/live-kit.html"><div class="support-icon">'''+icon('双眼鏡')+'''</div><span class="eyebrow">LIVE ESSENTIALS</span><h3>遠い席も、雨の日も。<br>準備して楽しむ。</h3><p>双眼鏡・荷物カバー・充電。持っていく理由から考える。</p><b>参戦準備を読む ↗</b></a></div></section>'''
notes='<section class="section wrap" id="notes"><div class="section-heading"><div><p class="eyebrow">YORIMICHI NOTES</p><h2>買う前の、よりみちノート。</h2></div></div>'+guides_grid()+'</section>'
OUT.mkdir(exist_ok=True)
(OUT/'index.html').write_text(page('坂道グッズと推し活のノート',hero+groups+'<div class="ad-note wrap">広告を含みます <span>非公式の案内サイト ／ 公式販売記録と出品情報を区別して掲載</span></div>'+archive+official+support+notes))

for folder in ['goods','groups','notes']: (OUT/folder).mkdir(exist_ok=True)
for p in items:
 name,color=GROUPS[p['g']]
 body=f'<div class="wrap"><p class="breadcrumb"><a href="/">ホーム</a> / <a href="/groups/{p["g"]}.html">{name}</a> / 過去グッズ</p><section class="product-page" style="--group:{color}"><div class="product-art">{icon(p["kind"])}<small>カテゴリイラスト・実際の商品画像ではありません</small></div><div><p class="eyebrow">{name} / {p["year"]}</p><h1>{p["title"]}</h1><p class="lead">{p["event"]}</p><span class="status">{p["state"]}</span><p>{p["note"]}</p><p class="callout">Amazonの個別出品・在庫・価格・販売元・真正性は未確認です。下のリンクは商品名による検索結果を開きます。</p>{ext(amazon(p["q"]),"Amazonでこのグッズを探す",True)}<p class="small">広告リンク ／ 商品名にメンバー名を加えると絞り込めます。</p>{ext(p["source"],"当時の公式販売情報を確認")}</div></section><article class="prose"><h2>同じグッズを見つけるために</h2><p>{p["tip"]}</p><h2>購入前に確認すること</h2><ul><li>公式販売時の名称・写真と、出品の絵柄・年・メンバーが一致するか。</li><li>新品・中古・開封済みの区別。実物写真と状態説明は十分か。</li><li>販売元、発送元、送料を含む合計額、返品条件、届く日。</li><li>公式ショップで再販や別の受付枠がないか。高額な出品を急いで選ばない。</li></ul><p>「公式グッズ」という商品説明だけで、販売元が公式運営であるとは判断できません。当サイトは各出品の真正性を保証していません。</p><a class="text-link" href="/notes/buying-check.html">マーケットプレイスの確認点を詳しく読む ↗</a><p class="small">販売情報確認日：2026年11月8日。参照先の受付終了は、すべての公式販売経路での終了を示すものではありません。</p></article><section class="related"><h2>手に入れた後も、大切に。</h2><p>グッズに合う収納を選んで、次の参戦にも。</p><a href="/notes/photo-storage.html">収納の選び方へ ↗</a></section></div>'
 (OUT/'goods'/f'{p["id"]}.html').write_text(page(name+' '+p['title'],body))

for g,(name,color) in GROUPS.items():
 selection=[p for p in items if p['g']==g]
 intro='公式の過去販売記録からグッズを探す入口。販売年と公演、衣装をそろえて検索しましょう。'
 special=''
 if g=='aobazaka':
  intro='公式発表をたどりながら、これからの歩みを追うページです。'
  special='<div class="callout"><h2>青葉坂46について</h2><p>公式発表では、オーディションで選ばれたメンバーによる1年間限定の新グループと案内されています。</p><p>このサイトでは、商品情報を確認できていないため購入リンクは掲載していません。</p>'+ext('https://aobazaka46.com/','公式サイトへ')+ext('https://sakurazaka46.com/s/s46/news/detail/O100093','設立についての公式発表')+'</div>'
 body=f'<div class="wrap section"><p class="breadcrumb"><a href="/">ホーム</a> / {name}</p><div class="group-title" style="--group:{color}"><p class="eyebrow">GROUP GUIDE</p><h1>{name}</h1><p>{intro}</p></div>{special}<div class="goods-grid">'+''.join(card(p) for p in selection)+'</div><p class="section-note">Amazonの出品状況は未確認です。各ページのリンクは検索結果への案内です。</p><h2 class="subheading">収納と参戦のノート</h2>'+guides_grid()+'</div>'
 (OUT/'groups'/f'{g}.html').write_text(page(name+'のグッズを探す',body))

articles={
'past-goods':'''<p class="lead">「あの衣装のアクスタが欲しい」。そんな時は、グループ名だけでなく、販売年と公演名をセットにして探してみましょう。</p><h2>まず、当時の正式な名前を探す</h2><p>周年ライブの販売商品でも、別の公演の衣装が使われていることがあります。イベント名、販売年、衣装名、メンバー名を整理すると、似たグッズとの取り違えを減らせます。</p><div class="callout">検索の組み立て：グループ名 ＋ 公演名・販売年 ＋ 商品名 ＋ メンバー名</div><h2>公式で今買えるかを先に確認</h2><p>古い商品ページが受付終了でも、別枠の受注や再販がある場合があります。公式ショップと公式のお知らせの両方を確認しましょう。「古い商品だから公式では絶対に買えない」とは限りません。</p><h2>Amazonでは状態と販売元もセットで見る</h2><p>過去の商品は新品・未開封・中古など、状態が異なる出品があります。同じ名前でも単品とセット、付属品の有無が違うので、実物写真と説明を照合してください。</p><h2>見つからない時は、表記を変える</h2><p>「アクスタ」と「アクリルスタンド」、「個別タオル」と「推しメンマフラータオル」など、呼び方を変えて探す方法もあります。衣装名や年は残したまま検索すると、目的の商品に近づきやすくなります。</p><p><a href="/#archive">過去グッズの販売記録から探す ↗</a></p>''',
'photo-storage':'''<p class="lead">収納用品は、色だけで選ぶと「スリーブごと入らない」「台座が収まらない」ことも。守りたいグッズを先に測ってから選びます。</p><h2>生写真は、スリーブに入れた外寸で考える</h2><p>写真そのものの寸法と、スリーブに入れた後の寸法は違います。ファイルの外寸ではなく、ポケットの有効内寸を確認しましょう。写真用・トレカ用・チェキ用を同じサイズだと思って買わないことが大切です。</p><div class="table-wrap"><table><thead><tr><th>したいこと</th><th>選ぶ候補</th><th>購入前に見る点</th></tr></thead><tbody><tr><td>たくさん保管</td><td>アルバム・リフィル</td><td>ポケット内寸、リング穴数、増設可否</td></tr><tr><td>少量を持ち歩く</td><td>硬質ケース＋ポーチ</td><td>スリーブ込みの寸法、曲がりにくさ</td></tr><tr><td>アクスタを運ぶ</td><td>仕切り付きケース</td><td>本体と台座が別々に入るか、厚み</td></tr></tbody></table></div><h2>写真と会報を分けて使える候補</h2><p>キングジムのファブラブはミニとレギュラーのバインダーがあるシリーズ。サイズごとに付属リフィルが異なるので、保管するものの寸法と照合して選びます。すべての坂道グッズへの適合を確認した商品ではありません。</p>'''+ext('https://www.kingjim.co.jp/sp/favluv/','メーカーのサイズ・リフィルを確認')+ext(amazon('キングジム ファブラブ コレクションバインダー FL5210'),'Amazonでファブラブを探す',True)+'''<h2>シンプルなアルバムも比較する</h2><p>無印良品には写真用アルバムやフォト・ハガキホルダーがあります。名称が似ていても収納対象やポケット数が違うので、品番と寸法を見比べてください。</p>'''+ext('https://www.muji.com/jp/ja/store/search/cmdty/フォトアルバム','無印良品の写真収納を見る')+ext(amazon('無印良品 フォトアルバム L判'),'Amazonで写真用アルバムを探す',True)+'''<h2>飾る収納と、持ち運ぶ収納を使い分ける</h2><p>大きなアクスタは本体だけでなく台座も測ります。収納量を増やしすぎるとケースやファイルが閉じなくなるため、厚みまで含めて確認。専用品でも、手持ちのグッズと寸法が合うとは限りません。</p><p class="small">紹介品は実使用レビューではなく、メーカー情報に基づく選択候補です。Amazonでの個別出品・在庫は未確認です。</p>''',
'live-kit':'''<p class="lead">持ち物は多いほど安心、とは限りません。席・会場・天気・帰宅までの時間から、自分が困りそうな場面を考えて準備します。</p><h2>遠い席：倍率だけで双眼鏡を決めない</h2><p>高倍率にすると視野や手ブレの影響も変わります。見える範囲、本体の重さ、眼鏡での使いやすさ、防振の有無を比較しましょう。可能なら店頭で持ち比べると、自分に合う重さを確認できます。</p>'''+ext('https://www.vixen.co.jp/howtouse/binocular/','ビクセンの双眼鏡選びを読む')+ext(amazon('ライブ 双眼鏡 8倍 10倍'),'Amazonでライブ用双眼鏡を探す',True)+'''<h2>雨の日：グッズと荷物も濡らさない</h2><p>レインウェアに加え、バッグを覆える袋や防水ポーチを候補に。バッグの寸法と袋の開口部を確認して選びます。傘を使える場所や雨具の扱いは、公演ごとの公式案内に従ってください。</p>'''+ext(amazon('バッグ レインカバー 大型 袋'),'Amazonで荷物の雨対策を探す',True)+'''<h2>長い一日：充電と取り出しやすさ</h2><p>スマートフォン用の充電器は、端子・対応ケーブル・重さを確認。使う端末に合ったものを選び、入場時に必要なものは取り出しやすい場所へ。ペンライトの予備電池も、手持ちの機種の指定に合わせます。</p><h2>買う前に持ち物をチェック</h2><div class="checklist"><label><input type="checkbox"> チケット・本人確認に必要なもの</label><label><input type="checkbox"> 公式ルールに合うペンライト</label><label><input type="checkbox"> 必要なら双眼鏡・眼鏡</label><label><input type="checkbox"> 対応する充電器・ケーブル</label><label><input type="checkbox"> 天気に合う雨具・防寒着</label><label><input type="checkbox"> グッズを持ち帰る袋と保護ケース</label></div><p class="small">チェック状態はこのページを開いている間だけのメモです。公演ごとの持込ルールを確認してください。</p>''',
'buying-check':'''<p class="lead">Amazonにある商品でも、販売しているのがAmazonやグループの公式運営とは限りません。商品と出品者を分けて確認します。</p><h2>「公式品」と「公式販売元」は別の確認事項</h2><p>過去に公式で販売されたグッズが、第三者から出品されている場合があります。「公式」というタイトルやブランド表記だけで真正性を判断せず、公式の販売記録と出品画像、説明、販売元情報を照合しましょう。</p><h2>状態を具体的に確認する</h2><ul><li>タオル：使用・洗濯の有無、汚れ、色落ち、ほつれ。</li><li>アクスタ：本体と台座、保護フィルム、傷、印刷の状態。</li><li>ペンライト：全色の発光、ボタン動作、液漏れ、ふた・ストラップ。</li><li>生写真：傷、折れ、反り、汚れ。画像と届く写真が同じものか。</li></ul><h2>合計額と、届く日を確認する</h2><p>商品代に送料を足して比較します。公式販売時より高い出品もあるため、公式での再販も確認してください。ライブで使うなら到着予定日も大切です。急いで高額な出品を選ぶ必要はありません。</p><h2>セットの中身を確認する</h2><p>チャームやアクスタの台座、生写真付き商品などは、写真に写るものすべてが含まれるとは限りません。「本体のみ」「特典なし」などの説明と返品条件を、注文前に読みます。</p><div class="callout">当サイトの「当時の公式販売を確認」は、その商品の販売記録を確認した意味です。Amazonの個々の出品を鑑定・保証した意味ではありません。</div>'''
}
for slug,n,kicker,title,desc in guides:
 if slug not in articles: continue
 body='<div class="wrap"><p class="breadcrumb"><a href="/">ホーム</a> / よりみちノート</p><article class="prose"><p class="eyebrow">YORIMICHI NOTE '+n+'</p><h1>'+title+'</h1><p class="article-meta">2026.11.08 ／ 広告を含みます</p>'+articles[slug]+'<hr><a href="/#notes">ノート一覧へ戻る ↗</a></article></div>'
 (OUT/'notes'/f'{slug}.html').write_text(page(title,body,desc))

about='''<div class="wrap"><article class="prose"><p class="eyebrow">ABOUT</p><h1>好きの、その先へ。</h1><p class="lead">坂道よりみちは、坂道グループのグッズを探すきっかけと、手に入れた後の推し活をつなぐ非公式の案内サイトです。</p><h2>このサイトで紹介するもの</h2><p>過去の公式グッズの販売記録、現在の公式ショップへの案内、収納とライブ参戦用品の選び方を掲載します。乃木坂46・櫻坂46・日向坂46・欅坂46・青葉坂46を扱います。</p><h2>掲載の考え方</h2><p>商品の存在や名称は公式告知を優先して確認します。現時点の公式在庫、受付終了、Amazonの出品確認は区別します。過去の告知が残っているだけで「今も販売中」とは表示しません。</p><p>Amazonへの検索リンクは、個別の出品・在庫・真正性を確認した商品へのリンクではありません。未確認の価格、レビュー点数、実使用体験を掲載しません。</p><h2>SNSでの調査について</h2><p>Xなどの投稿は、ファンが何に困っているかを調べる手がかりにします。一つの投稿だけで「定番」「人気」と判断せず、商品仕様や適合サイズは公式情報と区別して確認します。現時点では、十分に裏付けた個別投稿のおすすめ商品として掲載しているものはありません。</p><h2>編集・運営</h2><p>坂道よりみち。当サイトは各グループおよびその運営会社から独立した非公式サイトです。商品販売・決済・発送は行いません。</p><a href="/privacy.html">プライバシー・広告表示へ ↗</a></article></div>'''
(OUT/'about.html').write_text(page('このサイトについて',about))
privacy='''<div class="wrap"><article class="prose"><p class="eyebrow">POLICY</p><h1>プライバシー・広告表示</h1><h2>広告について</h2><p>Amazonのアソシエイトとして、坂道よりみちは適格販売により収入を得ています。Amazonへの紹介リンクは広告リンクです。紹介料の発生は商品の真正性や品質を保証するものではありません。</p><h2>情報と販売について</h2><p>当サイトは商品を販売しません。注文、決済、配送、返品のお問い合わせは利用した販売店・サービスへお願いします。価格・在庫・出品者・配送予定はリンク先でご確認ください。</p><h2>アクセス情報</h2><p>本サイト独自のアクセス解析、広告配信スクリプト、会員登録、お問い合わせフォームは設置していません。ホスティングサービスが運用上のアクセス情報や認証に関する情報を処理する場合があります。</p><h2>外部リンク</h2><p>Amazon、公式ショップ、Xなどの外部サービスへ移動した後は、各サービスのプライバシーポリシーが適用されます。外部サービス側でCookieなどが利用される場合があります。</p><h2>掲載内容</h2><p>掲載時点の情報を案内しています。公式の販売状況とAmazonの出品状況を混同せず、分からない情報は未確認として表示します。</p><p>制定日：2026年11月8日</p></article></div>'''
(OUT/'privacy.html').write_text(page('プライバシー・広告表示',privacy))
(OUT/'404.html').write_text(page('ページが見つかりません','<div class="wrap section"><h1>ページが見つかりません。</h1><a class="button" href="/">ホームへ戻る ↗</a></div>'))
(OUT/'favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="15" fill="#766187"/><path d="M17 47L46 18M22 18h24v24" stroke="#faf8f4" fill="none" stroke-width="5"/></svg>')
(OUT/'robots.txt').write_text('User-agent: *\nAllow: /\n')
render_gear_pages(OUT,page,ext,amazon)
render_expansion(OUT,page,ext,amazon)
(OUT/'notes.html').write_text(page('よりみちノート一覧','<div class="wrap section"><p class="eyebrow">YORIMICHI NOTES</p><h1>グッズ選びと、次の現場。</h1><p class="lead">探す・守る・持ち歩く。困った場面から読める9つのノート。</p>'+guides_grid()+'</div>'))
for path in OUT.rglob('*.html'):
 text=path.read_text()
 text=text.replace('<h2>買う前の、よりみちノート。</h2>','<h2>買う前の、よりみちノート。</h2><p><a href="/notes.html">9つのノートを一覧で見る ↗</a></p>')
 text=text.replace('<p>本サイト独自のアクセス解析、','<p>参戦チェックリストはチェック状態のみを利用中のブラウザのローカルストレージに保存します。当サイトへの送信・端末間同期は行いません。チェックリストのリセットで削除できます。収納サイズ確認の入力値は保存・送信しません。</p><p>本サイト独自のアクセス解析、')
 if path.name=='index.html':
  text=text.replace('<section class="section wrap" id="support">','<section class="utility-links wrap"><a href="/checklist.html"><small>LIVE CHECKLIST</small><strong>次の現場、準備できた？</strong><span>12項目をチェックして保存 ↗</span></a><a href="/size-check.html"><small>SIZE CHECK</small><strong>そのケース、サイズは合う？</strong><span>グッズと収納の寸法を比較 ↗</span></a></section><section class="section wrap" id="support">')
 path.write_text(text)
render_editorial(OUT,page)
from purchase_check import extend as extend_purchase_check
extend_purchase_check(OUT)
finalize(OUT)
print(f'Built {len(list(OUT.rglob("*.html")))} HTML pages')
