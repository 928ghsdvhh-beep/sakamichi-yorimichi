"""Publish the seat-display guide using the shared live-guide page layout."""
import re
from html import escape

SLUG = 'sakurazaka-seat-display'
TITLE = '櫻坂46ライブの座席はいつわかる？電子チケットの表示日時の調べ方'
DESCRIPTION = '櫻坂46のライブで、電子チケットは受け取れたのに座席番号が表示されないときの確認順。受付案内のどこを見ればよいか、表示前と表示後に分けて図解します。'
LINK = f'<a href="/notes/{SLUG}">{TITLE}</a>'
BODY = '''<div class="wrap edit-article">
<nav class="edit-breadcrumb" aria-label="パンくず"><a href="/">ホーム</a> / <a href="/articles">推し活記事</a> / 櫻坂46</nav>
<article class="prose">
<h1>櫻坂46ライブの座席はいつわかる？電子チケットの表示日時の調べ方</h1>
<p class="lead">チケットがアプリに出ても、座席番号はあとから表示されることがあります。席がわかる日時は、行く公演・日付・申し込んだ受付の案内で「座席表示」を探してください。</p>
<figure class="seat-figure">
<figcaption><strong>いまアプリに何が出ていますか？</strong></figcaption>
<ul class="seat-paths">
<li><a href="#ticket-missing">チケットが見当たらない</a><span>まず受取案内とチケット表示開始を確認</span></li>
<li><a href="#seat-missing">公演名は出ているが、席がない</a><span>券面や購入先の案内で座席表示日を確認</span></li>
<li><a href="#seat-found">座席番号が表示されている</a><span>ゲート・ブロック・列・番号を確認</span></li>
</ul>
</figure>
<h2>電子チケットの受取開始日と座席番号の表示日を確認</h2>
<p>櫻坂46公式の公演特設ページを開き、申込履歴と同じ公演日・受付（FC先行、一般発売など）の案内へ進みます。ページ内検索で「座席表示」「発券」「電子チケット」を探すと、どの日時か見分けやすくなります。</p>
<dl class="seat-terms">
<dt>当落発表</dt><dd>申し込みの結果がわかる日時。</dd>
<dt>発券・チケット表示開始</dt><dd>チケットを受け取る、またはアプリで開けるようになる日時。</dd>
<dt><strong>座席表示開始</strong></dt><dd>ブロック・列・番号などが券面に表示される日時。公演によっては入場時に案内されます。</dd>
</dl>
<p>「発券」の日付しか見当たらない場合は、購入先の公演ページ・受取メール・受け取った券面も確認してください。田村保乃 卒業コンサートのように、公演ごとに公式のチケット案内があります。</p>
<h2 id="ticket-missing">チケット自体が見当たらない</h2>
<p>購入履歴や受取メールで、<strong>指定アプリ</strong>と<strong>チケット表示開始日時</strong>を確認します。ローチケで購入しても、受け取るアプリがチケプラなど別のサービスになる公演があります。指定のアプリを開き、申込時の情報で受け取ってください。</p>
<p>チケプラで受け取る場合は、申込時に登録したPlus member IDと電話番号の端末を確認します。案内メールが見つからなければ、登録メールアドレスの迷惑メールフォルダも確認してください。</p>
<h2 id="seat-missing">チケットはあるのに、座席番号が出ない</h2>
<ul>
<li><strong>チケプラ電子チケット</strong>は、アプリで行く公演の券面を開き、「座席表示日」を確認します。</li>
<li><strong>ローチケ電子チケットアプリ</strong>は、トップの「電子チケット一覧」で該当公演をタップすると、券面に座席番号が表示されます。券面にまだ出ない場合は、購入先の公演案内で座席表示のタイミングを確認します。</li>
</ul>
<p>座席表示の開始前なら、案内された時刻以降に同じ券面を開き直します。開始を過ぎても出ない場合は、公演名・日付・受付名を用意して、受取案内に記載の問い合わせ窓口へ確認してください。</p>
<figure class="seat-figure">
<figcaption><strong>券面で探す項目</strong><span>読み方を示す模式図です。実際の表示名や位置は公演・アプリごとに異なります。</span></figcaption>
<dl class="seat-ticket">
<dt>公演名・公演日</dt><dd>行く回と合っているかを照合</dd>
<dt class="seat-key">座席表示日</dt><dd class="seat-key">席がまだ出ていなければ、ここを確認</dd>
<dt>入口・ゲート</dt><dd>表示されていれば入場口の目印に</dd>
<dt>階・ブロック／列・番号</dt><dd>席が表示されたら、会場でこの順に探す</dd>
</dl>
</figure>
<h2 id="seat-found">座席が見えたら、どこへ向かう？</h2>
<p>入口・ゲートが書かれていれば、会場へ着いたらそこを目印にします。入場後は、階やブロックに進み、列と番号を探します。会場の常設座席表は場所の確認に使えます。</p>
<section class="edit-sources"><h2>公式案内</h2><ul><li><a href="https://sakurazaka46.com/">櫻坂46公式サイト</a></li><li><a href="https://tixplus.jp/feature/sakurazaka46_dticket/">櫻坂46のチケプラ電子チケット受取ガイド</a></li><li><a href="https://qa.tixplus.jp/--6863cabd9f4638ca4d10f124">チケプラヘルプ｜座席番号はいつわかりますか？</a></li><li><a href="https://sakurazaka46.com/s/s46/ticket/detail/hono_graduation?ima=0000">櫻坂46公式｜田村保乃 卒業コンサートのチケット案内</a></li><li><a href="https://l-tike.com/e-tike/navi/guide/display_ticket.html/">ローチケ電子チケットの表示方法</a></li><li><a href="https://faq.l-tike.com/%E4%BA%88%E7%B4%84%E3%81%97%E3%81%9F%E3%83%81%E3%82%B1%E3%83%83%E3%83%88%E3%81%AE%E5%BA%A7%E5%B8%AD%E7%95%AA%E5%8F%B7%E3%82%92%E4%BA%8B%E5%89%8D%E3%81%AB%E7%A2%BA%E8%AA%8D%E3%81%A7%E3%81%8D%E3%81%BE%E3%81%99%E3%81%8B%EF%BC%9F-672b34263649539ff3f0be1e">ローチケFAQ｜座席番号の確認</a></li></ul></section>
<section class="edit-related"><h2>あわせて読みたい</h2><ul><li><a href="/notes/sakurazaka-live-first">櫻坂46ライブ初参戦ガイド</a></li></ul></section>
</article></div>'''


def apply(out):
    """Use the finalized shared shell and add the guide to navigation and sitemap."""
    parent = out / 'notes/sakurazaka-live-first.html'
    original = parent.read_text()
    head, rest = original.split('<main id="main">', 1)
    foot = rest.split('</main>', 1)[1]
    old_url = re.search(r'<link rel="canonical" href="([^"]+)"', head)[1]
    url = old_url.rsplit('/', 1)[0] + '/' + SLUG
    old_headline = re.search(r'"headline": "([^"]+)"', head)[1]
    old_desc = re.search(r'<meta name="description" content="([^"]+)"', head)[1]
    head = head.replace(old_url, url).replace(old_headline, escape(TITLE)).replace(old_desc, escape(DESCRIPTION))
    diagram = '''<style>
.seat-figure{margin:1.4rem 0;padding:1rem;background:#f5edf8;border-radius:12px;color:#362943}
.seat-figure figcaption span,.seat-paths span{display:block;margin-top:.35rem;font-size:.9rem}
.seat-figure .seat-paths{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.65rem;padding:0;margin:.8rem 0 0;list-style:none}
.seat-figure .seat-paths li{margin:0;padding:.75rem;background:#fff;border:1px solid #cdbbd6;border-radius:8px}
.seat-paths a{display:inline-block;color:#56396b;font-weight:700;text-decoration:underline;text-underline-offset:.18em}
.seat-paths a:focus-visible{outline:2px solid #56396b;outline-offset:3px}
.seat-terms dt,.seat-ticket dt{font-weight:700}.seat-terms dd{margin:0 0 .65rem}
.seat-ticket{display:grid;grid-template-columns:minmax(0,2fr) minmax(0,3fr);margin:.8rem 0 0;background:#fff;border:1px solid #cdbbd6;border-radius:8px;overflow:hidden}
.seat-ticket dt,.seat-ticket dd{margin:0;padding:.65rem;border-bottom:1px solid #dfd1e5;overflow-wrap:anywhere}
.seat-ticket .seat-key{background:#e9dcf0}
@media(max-width:640px){.seat-figure .seat-paths{grid-template-columns:1fr}}
</style>'''
    head = head.replace('</head>', diagram + '</head>')
    (out / f'notes/{SLUG}.html').write_text(head + '<main id="main">' + BODY + '</main>' + foot)
    marker = '<section class="edit-related"><h2>あわせて読みたい</h2><ul>'
    parent.write_text(original.replace(marker, marker + '<li>' + LINK + '</li>', 1))
    sitemap = out / 'sitemap.xml'
    xml = sitemap.read_text()
    old_item = f'<url><loc>{old_url}</loc></url>\n'
    sitemap.write_text(xml.replace(old_item, old_item + f'<url><loc>{url}</loc></url>\n', 1))
