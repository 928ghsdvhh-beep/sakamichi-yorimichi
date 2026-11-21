"""Publish the seat-display guide using the shared live-guide page layout."""
import re
from html import escape

SLUG = 'sakurazaka-seat-display'
TITLE = '櫻坂46ライブの座席はいつわかる？電子チケットの表示日時の調べ方'
DESCRIPTION = '櫻坂46のライブで、電子チケットは受け取れたのに座席が出ないときの確認順。受付案内のどこを見ればよいか、表示前と表示後に分けて図解します。'
LINK = f'<a href="/notes/{SLUG}">{TITLE}</a>'
BODY = '''<div class="wrap edit-article">
<nav class="edit-breadcrumb" aria-label="パンくず"><a href="/">ホーム</a> / <a href="/articles">推し活記事</a> / 櫻坂46</nav>
<article class="prose">
<h1>櫻坂46ライブの座席はいつわかる？電子チケットの表示日時の調べ方</h1>
<p class="lead">座席番号は、自分の公演・受付に案内された「座席表示開始日時」以降に確認できます。チケットがアプリに届く日時と座席の表示日時は、公演によってずれることがあります。</p>
<figure class="seat-flow">
<figcaption><strong>座席がまだ出ていないときの確認順</strong></figcaption>
<ol><li><strong>公演・日付・受付を照合</strong><span>購入履歴と同じ受付の案内を開く</span></li><li><strong>座席表示開始を探す</strong><span>チケプラの券面・購入先の案内を確認</span></li><li><strong>チケット詳細を開く</strong><span>表示開始時刻を過ぎてから座席欄へ</span></li></ol>
</figure>
<h2>公式案内のどこを見ればいい？</h2>
<p>櫻坂46の公式サイトで、自分が行く公演の特設ページまたはチケット案内を開きます。FC先行、一般発売など自分が申し込んだ受付を選び、ページ内検索で「座席表示」「電子チケット」「発券」を探します。「発券」しか見つからない場合は、購入先の公演ページや受取案内も確認します。</p>
<dl><dt><strong>当落発表</strong></dt><dd>申込みの結果を確認する日時。</dd><dt><strong>発券・チケット表示開始</strong></dt><dd>電子チケットを受け取ったり、アプリで開いたりできるようになる日時。</dd><dt><strong>座席表示開始</strong></dt><dd>座席番号を確認できるようになる日時。案内に別記されていれば、こちらを見ます。</dd></dl>
<h2>チケプラとローチケで、どこを確認する？</h2>
<p><strong>チケプラ電子チケットの場合</strong>は、受け取ったチケットの券面にある座席表示日を確認します。櫻坂46では、田村保乃 卒業コンサートの公式電子チケット案内にもチケプラの受取ガイドが掲載されています。</p>
<p><strong>ローチケ電子チケットの場合</strong>は、購入した公演の座席表示開始日時を確認し、アプリのチケット詳細を開きます。ローチケでは一部公演で座席番号が公演直前に表示されます。</p>
<h2>チケットがあるのに座席番号だけ出ない</h2>
<p>表示開始前なら、案内された時刻を待ちます。時刻を過ぎたら、アプリで該当公演のチケット詳細を開き直してください。表示を確認できなければ、公演名・日付・受付名を手元に置いて購入先の窓口に問い合わせます。</p>
<p>チケット自体が見当たらない場合は、購入時の受取案内で指定されたアプリと受取条件を確認します。公演が違うチケットの設定を見て判断しないよう、タイトルと日付を照合してください。</p>
<h2>座席が見えたら控える項目</h2>
<p>公演日、入口・ゲート、階またはブロック、列、番号を控えます。花道や機材の配置は公演ごとに違うので、会場の常設座席表は入口や席の位置を探す用途に使い、ステージの見え方は公演別の公式案内で確認します。</p>
<section class="edit-sources"><h2>公式案内</h2><ul><li><a href="https://sakurazaka46.com/">櫻坂46公式サイト</a></li><li><a href="https://tixplus.jp/feature/sakurazaka46_dticket/">櫻坂46のチケプラ電子チケット受取ガイド</a></li><li><a href="https://qa.tixplus.jp/--6863cabd9f4638ca4d10f124">チケプラヘルプ｜座席番号はいつわかりますか？</a></li><li><a href="https://sakurazaka46.com/s/s46/ticket/detail/hono_graduation?ima=0000">櫻坂46公式｜田村保乃 卒業コンサートのチケット案内</a></li><li><a href="https://cdn-org.l-tike.com/e-tike/navi/guide/display_ticket.html">ローチケ電子チケットの表示方法</a></li></ul></section>
<section class="edit-related"><h2>あわせて読みたい</h2><ul><li><a href="/notes/sakurazaka-live-first">櫻坂46ライブ初参戦ガイド</a></li><li><a href="/notes/binoculars">ライブ双眼鏡の8倍・10倍を比較</a></li></ul></section>
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
    diagram = '<style>.seat-flow{margin:1.4rem 0;padding:1rem;background:#f5edf8;border-radius:12px}.seat-flow ol{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1.7rem;padding:0;margin:.8rem 0 0;list-style:none}.seat-flow li{position:relative;padding:.8rem;background:white;border:1px solid #d7c6df;border-radius:8px}.seat-flow li:not(:last-child)::after{content:"";position:absolute;left:100%;top:50%;width:1.75rem;border-top:2px solid #836893}.seat-flow strong,.seat-flow span{display:block}.seat-flow span{margin-top:.3rem;font-size:.875rem;color:#554760}@media(max-width:640px){.seat-flow ol{grid-template-columns:1fr;gap:1rem}.seat-flow li:not(:last-child)::after{left:50%;top:100%;width:0;height:1.1rem;border-top:0;border-left:2px solid #836893}}</style>'
    head = head.replace('</head>', diagram + '</head>')
    (out / f'notes/{SLUG}.html').write_text(head + '<main id="main">' + BODY + '</main>' + foot)
    marker = '<section class="edit-related"><h2>あわせて読みたい</h2><ul>'
    parent.write_text(original.replace(marker, marker + '<li>' + LINK + '</li>', 1))
    sitemap = out / 'sitemap.xml'
    xml = sitemap.read_text()
    old_item = f'<url><loc>{old_url}</loc></url>\n'
    sitemap.write_text(xml.replace(old_item, old_item + f'<url><loc>{url}</loc></url>\n', 1))
