"""Source-checked acquisition articles. Dates are snapshots, not a live feed."""
from html import escape as esc
import re

DAY='2026年11月11日'
S={
 'nogi_live':('乃木坂46公式：乃木坂スター誕生！SIX LIVE 先行案内','https://www.nogizaka46.com/s/n46/news/detail/102395'),
 'nogi_meet':('乃木坂46公式：43rdミーグリ第4次～第6次受付','https://www.nogizaka46.com/s/n46/news/detail/102397'),
 'nogi_disc':('乃木坂46公式：43rdシングル特設ページ','https://www.nogizaka46.com/s/n46/page/43rd_single'),
 'nogi_manner':('乃木坂46公式：コンサート観覧時の応援マナー','https://www.nogizaka46.com/s/n46/news/detail/101561'),
 'sakura_live':('櫻坂46公式：6th YEAR ANNIVERSARY LIVE 特設','https://sakurazaka46.com/s/s46/page/6th_anniversary'),
 'sakura_schedule':('櫻坂46公式：公演スケジュール','https://sakurazaka46.com/s/s46/media/list?dy=20261111&ima=0000'),
 'sakura_meet':('櫻坂46公式：16thミーグリ第10次～第13次受付','https://sakurazaka46.com/s/s46/news/detail/S00229?ima=0000&link=ROBO004'),
 'hina_live':('日向坂46公式：ひなくり2026 特設','https://www.hinatazaka46.com/s/official/page/hinachri2026'),
 'hina_meet':('日向坂46公式：ミート＆グリート一覧','https://www.hinatazaka46.com/s/official/diary/event/list'),
 'fortune_n':('forTUNE music：乃木坂46 43rd対象商品・参加方法','https://www.fortunemusic.jp/nogizaka_202612/'),
 'fortune_h':('forTUNE music：日向坂46 18th対象商品・販売終了告知','https://www.fortunemusic.jp/hinatazaka_202609/'),
 'fortune_rules':('forTUNE music：対象イベント参加注意事項','https://fortunemusic.jp/nogizaka_202612/page/attention/'),
 'keyaki':('欅坂46公式：櫻坂46公式サイト開設のお知らせ','https://www.keyakizaka46.com/s/k46o/news/detail/O00220?ima=0000'),
 'kingjim':('キングジム：ファブラブ製品情報','https://www.kingjim.co.jp/sp/favluv/'),
 'kenko':('ケンコー・トキナー：ウルトラビューH 8×21DH 製品情報','https://www.kenko-tokina.co.jp/optics/binoculars/compactd/uvh/8x21dh_fmc_matbk.html')}

def p(t): return '<p>'+t+'</p>'
def ul(items): return '<ul>'+''.join('<li>'+i+'</li>' for i in items)+'</ul>'
def table(headers,rows):
 return '<div class="edit-table"><table><thead><tr>'+''.join('<th scope="col">'+x+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+x+'</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table></div>'
def link(slug,label):return f'<a href="/notes/{slug}.html">{label} →</a>'
def a(slug,cat,title,desc,lead,sections,sources,related,group='坂道共通'):
 return dict(slug=slug,cat=cat,title=title,desc=desc,lead=lead,sections=sections,sources=sources,related=related,group=group)

ARTICLES=[
a('events-2026-2027','イベント','坂道イベント情報｜2026年11月以降のライブ・ミーグリ確認ガイド','乃木坂・櫻坂・日向坂の公式発表から、直近の公演と応募情報を整理。開催日と申込締切を分けて確認。','ライブの日にちだけをメモして、申込締切を見落としたことはありませんか。参加までには「応募」「入金」「チケット受取」「当日の受付」があります。ここでは公式発表を確認できたイベントを、準備に使える形で整理します。',[
('確認できたライブ予定',p('以下は2026年11月11日時点の公式発表です。全イベントを網羅した一覧ではありません。開催・出演・販売状況は変更されるため、購入前と出発前に公式の最新案内を確認してください。')+table(['グループ／公演','日程・会場','準備記事'],[
 ('櫻坂46／6th YEAR ANNIVERSARY LIVE','2026年11月14・15日／ZOZOマリンスタジアム',link('sakurazaka-live-first','屋外アニラの準備')),
 ('日向坂46／ひなくり2026','兵庫11月21～23日、東京12月9～11日、愛知12月22～24日',link('hinatazaka-live-first','会場別の準備')),
 ('乃木坂46／乃木坂スター誕生！SIX LIVE','2027年1月16・17日／有明アリーナ',link('nogizaka-live-first','初参戦の準備'))])),
('ミーグリは開催日と応募期間を別にする',p('乃木坂43rdの第4次受付は11月12日14時～13日14時、第5次は19日14時～20日14時、第6次は26日14時～27日14時の予定です。櫻坂16thは11月11日開始の第10次受付について公式告知を確認しました。日向坂18thのforTUNE music販売は終了の案内があるため、「開催がある＝今から応募できる」とは案内しません。')+p(link('nogizaka-43-meet','乃木坂43rdの受付と購入先の違い'))),
('カレンダーに入れるなら、この4項目',ul(['応募終了：受付開始とは別の予定として登録する。','支払い期限：当落を見たら、購入完了まで確認する。','チケット受取・顔写真登録：利用するアプリと必要な手順を確認する。','当日：開演だけでなく、会場到着・入場・帰りの予定も書く。'])+p('時間の余裕は会場までの移動、グッズ受取、本人確認の手続きから逆算します。一律に「開演の何分前で十分」と決めると、初めての会場では予定が崩れやすくなります。')),
('欅坂・青葉坂の扱い',p('欅坂の過去公演・グッズは記録として分けて掲載します。現在の櫻坂の公演に、当時のルールをそのまま当てはめないでください。青葉坂については今回、掲載できる公演日程と参加条件の一次情報を確認できていません。日程を推測してカレンダーへ追加することはしません。'))],['sakura_schedule','hina_live','nogi_live','nogi_meet','sakura_meet','fortune_h','keyaki'],['live-items-picks','meet-greet-first']),

a('news-20261111','最新情報','坂道最新情報メモ｜2026年11月11日確認の公演・リリース・応募情報','乃木坂43rd、櫻坂アニラ、日向坂ひなくり。公式発表をもとに、次に確認することを整理した日付付きニュース。','発表が重なる時期は、見出しを追うだけでも大変です。このページでは、2026年11月11日に確認した発表を「参加準備に何が関係するか」まで整理します。自動更新ニュースではなく、この日付時点の編集メモです。',[
('乃木坂46：43rdと次のライブ',p('43rdシングル「君ロス」の特設ページでは11月11日のMV公開告知を確認。CD発売予定は12月2日です。また「乃木坂スター誕生！SIX LIVE」は2027年1月16・17日に有明アリーナで開催予定。公演準備と、CDの応募特典は別の予定として管理すると整理しやすくなります。')+p('ミーグリを目的にCDを選ぶ場合、通常の商品購入だけで対象の参加権利が付くとは限りません。対象販売窓口、応募回、当落後の手続きを確認してから申し込みます。')),
('櫻坂46：直近のアニラへ向けて',p('6th YEAR ANNIVERSARY LIVEは11月14・15日のZOZOマリンスタジアム公演。公式特設には配信・リピート配信の案内もあります。現地参加と配信視聴では、準備するものと時間が異なります。現地組は入場案内と雨対策、配信組は対応機器と視聴可能時間を確認しましょう。')+p('配信がある場合も、好きな時刻から見返せるとは限りません。リピートと常時視聴可能なアーカイブを同じ意味で扱わず、購入先の説明まで読んで選びます。')),
('日向坂46：ひなくりの会場を取り違えない',p('「ひなくり2026」は兵庫・東京・愛知を巡るアリーナツアー。一般販売は兵庫・東京が11月14日12時から、愛知が11月28日12時からと公式特設で案内されています。これは発売開始予定であり、購入できる在庫の保証ではありません。')+p('同じツアーでも会場・日付・開演時刻が異なります。ホテルや交通を予約する前にチケットの対象公演を照合し、12月公演は帰宅時の防寒も含めて荷物を考えます。')),
('SNSの情報を保存する時のチェック',ul(['投稿日時と対象年をセットで記録する。','画像だけではなく、公式の元ページを保存する。','「受付中」の投稿でも、本文の終了日時を確かめる。','欠席・振替・配送変更は、最初の発表に追加がないか確認する。'])+p('このページの次回更新日は未定です。最新の受付状況は公式で再確認し、変更が確認できた時点で記事本文を更新します。'))],['nogi_disc','nogi_live','sakura_live','hina_live'],['events-2026-2027','nogizaka-43-meet']),

a('storage-picks','収納','坂道グッズ収納のおすすめ｜生写真・アクスタ・タオルを用途で選ぶ','生写真のスリーブ、バインダー、アクスタの持ち運び、タオル整理。サイズと使い方から選ぶ収納用品ガイド。','生写真は増えるのにファイルは閉じない。アクスタを持ち出すたび台座が迷子になる。収納は「何枚入るか」だけでなく、家で眺めるのか、現場へ持っていくのかで向く形が変わります。',[
('保管・持ち運び・展示を分ける',table(['使い方','おすすめの形','確認するところ'],[('自宅の生写真保管','スリーブ＋対応リフィル＋バインダー','袋込みの外寸、リング規格、閉じた時の厚み'),('少量を持ち出す','薄型ホルダー・硬めのケース','写真が動かないか、開口部が閉じるか'),('アクスタを運ぶ','本体・台座を分ける収納','内寸、厚み、パーツの接触'),('タオルを整理','畳んで並べる仕切り・浅型ケース','湿気を残さないこと、出し入れのしやすさ')])+p('これは用途から考えた編集部の選び方です。購入者レビューの人気ランキングや、実使用比較の順位ではありません。')),
('生写真は「スリーブに入れた後」で測る',p('裸の写真がポケットに入っても、袋を足すと入口で引っかかることがあります。まず写真、次にスリーブ、その次にリフィルの収納内寸という順で確認します。厚手・二重スリーブなら、厚みと開口部にも余裕が必要です。')+p('小さいトレカ向けのミニバインダーを、名前だけでL判生写真用として選ばないのがポイント。キングジムのファブラブも、レギュラーとミニでは対象が異なります。リフィルを含めた対応を見て選びましょう。')+p(link('photo-sleeves','写真・袋・リフィルのサイズ確認')+' ／ <a href="/size-check.html">収納サイズ確認ツール →</a>')),
('具体的な比較候補から選ぶ',p('リフィルで分類したい人は、ファブラブのコレクションバインダーを候補にできます。掲載済みのFL5210とFL5200を比較する時は、本体の色より先に、収納対象と対応リフィルを確認してください。Amazonの出品・型番一致は未確認のため、この記事には購入リンクを付けていません。')+p('<a href="/tools/favluv-regular.html">FL5210の確認点 →</a> ／ <a href="/tools/favluv-mini.html">FL5200の確認点 →</a>')),
('アクスタとタオルは別の保管方法にする',p('アクスタは一つの袋へまとめる前に、本体・台座・小物を分けます。長いパーツは横幅だけでなく取り出し口を通るかも確認。展示用の袋と持ち運び用のクッション付きケースは、同じ役目ではありません。')+p('使用後のタオルを、湿ったまま生写真やアクスタのケースへ入れないようにします。持ち帰り用の袋を分けておけば、帰宅後の洗濯・乾燥とグッズ整理を別々に進められます。高価な収納を一式そろえる前に、一種類のグッズでサイズを試す方が買い直しを減らせます。'))],['kingjim'],['acsta-carry','photo-storage','keyaki-goods-care']),

a('live-items-picks','ライブ用品','坂道ライブのおすすめアイテム｜席・天気・荷物から選ぶ持ち物','双眼鏡、雨具、充電、グッズ保護。初参戦で買い足す前に、困る場面と必要条件を整理するライブ用品記事。','ライブ用品は、たくさん持てば安心というものでもありません。入場時に取り出せない荷物や、帰りに増えるグッズまで考えると、選び方が変わります。手持ちで代用できるものと買い足したいものを分けてみましょう。',[
('まずは、席と会場から考える',table(['困りそうな場面','持ち物の候補','選ぶ時の条件'],[('遠い席で表情を追いたい','双眼鏡','倍率、視野、重さ、眼鏡での使いやすさ'),('屋外で雨や風が心配','レインウェア・荷物用の袋','会場ルール、服の上に着られる寸法'),('電子チケットを使う','充電器・対応ケーブル','端子、残量、持込ルール'),('購入グッズが増える','保護袋・折り畳めるバッグ','グッズ外寸、開口部、帰りの持ちやすさ')])+p('全員に必要なセットではありません。屋内公演なら大型の雨具を外すなど、自分の予定に合わせて減らします。')),
('双眼鏡：高倍率だけで決めない',p('見たい範囲を追いやすいことと、長く持てる重さは両方大切です。8倍と10倍では見え方の好みが分かれるため、可能なら店頭で持ち比べ、ピント操作も試しましょう。防振モデルは予算と重さ、電池の扱いまで比べます。')+p('軽さを重視して比較する具体候補として、ケンコーのウルトラビューH 8×21DH FMC-MATBKを掲載しています。メーカーがコンサート用途を案内するモデルですが、席から推しの表情が必ず見えるという保証ではありません。')+p('<a href="/tools/kenko-8x21.html">掲載モデルの仕様確認 →</a> ／ '+link('binoculars','8倍・10倍の選び方'))),
('雨対策：自分とバッグを別に守る',p('上着だけではバッグの開口部までは守れません。荷物用の袋を選ぶ時は、バッグを入れた後に口を閉じられるか確認します。使用後の濡れた雨具を入れる袋も別に用意すると、生写真やタオルと分けて持ち帰れます。傘の使用は会場の指示を優先してください。')),
('買い足す前に、一度バッグへ入れる',p('チケットを使うスマホ、本人確認書類、財布はすぐ出せる位置に。予備電池は手持ちのペンライトに指定された種類を確認します。双眼鏡と飲み物を入れた状態で持ち、重すぎるなら予備を減らす順番を考えます。')+p('この記事のおすすめは用途別の候補です。未確認のAmazon価格・星評価・口コミまとめは掲載していません。<a href="/checklist.html">参戦チェックリスト</a>で持ち物と手続きを一緒に確認できます。'))],['kenko','sakura_live','hina_live'],['rain-kit','nogizaka-live-first','sakurazaka-live-first']),

a('nogizaka-live-first','ライブアドバイス','乃木坂46ライブ初参戦ガイド｜本人確認・応援グッズ・当日の動き方','乃木坂ライブが初めての人へ。公演ごとの入場条件、タオルとペンライト、席での過ごし方を確認。','好きな曲は聴いているけれど、会場へ行くのは初めて。コールを全部覚えていなくても、準備する順番が見えると気持ちに余裕が生まれます。乃木坂の公演は本体ライブ、期別、番組ライブなど対象も違うので、自分のチケットから確認しましょう。',[
('同じ乃木坂でも、対象公演を照合する',p('2027年1月の「乃木坂スター誕生！SIX LIVE」は、有明アリーナで開催予定の6期生を中心とする公演です。全メンバーが出る本体ライブと思い込まず、出演者と公演内容を読みます。公式では来場者全員の身分証確認や手荷物検査が案内されています。必要書類はその公演のリストで確認してください。')),
('タオルとペンライトは持ち方まで準備',p('応援グッズを掲げる高さは、後ろの人の視界に関わります。公式の応援マナー案内では胸の高さまでとされています。新しく買う場合も、大きさや発光のルールを確認してから選び、隣の席へはみ出さない使い方を考えておきます。')+p('推しのサイリウムカラーは、古いまとめ画像や別メンバーの情報を混ぜず、現在の本人発信などから確認します。色替えに自信がなければ開演前に操作を練習。全曲で同じ振りをする必要はなく、分からない時はステージを見ることに集中して構いません。')),
('入場前にすること、着席後にすること',ul(['家を出る前：チケット表示、本人確認書類、スマホ残量を確認。','会場到着後：入場口とグッズ受取の場所を区別して確認。','着席後：周囲をふさがず、荷物とタオルをまとめる。','終演後：規制退場などの案内があれば従い、急な移動を避ける。'])+p('帰りの電車を開演時刻だけから決めると、移動に余裕がなくなることがあります。終演時刻の確約がない場合は、公演の長さを断定した個人投稿に頼りすぎず、帰宅手段に余裕を持たせます。')),
('一人参加の準備もシンプルに',p('待ち合わせがない分、自分で当日の優先順位を決められます。現地での無理な交流やグッズ交換を前提にせず、チケット・飲み物・必要な道具を自分のバッグで完結させておくと動きやすくなります。生写真を買う予定なら、持ち帰りの保護袋だけ先に用意しておく方法もあります。'))],['nogi_live','nogi_manner'],['live-items-picks','storage-picks','meet-greet-first'],group='乃木坂46'),

a('sakurazaka-live-first','ライブアドバイス','櫻坂46ライブ初参戦ガイド｜アニラ・屋外公演の準備と楽しみ方','櫻坂ライブの初参戦に。ZOZOマリンの屋外公演を例に、入場・雨対策・双眼鏡・応援の準備を整理。','映像で見ていたパフォーマンスを会場で見たい。初めての櫻坂ライブでは、応援の仕方より先に、入場と会場環境を押さえておくと当日を楽しみやすくなります。今回は直近の屋外アニラを例に準備を考えます。',[
('6thアニラの対象日を確認',p('2026年の6th YEAR ANNIVERSARY LIVEは、11月14・15日にZOZOマリンスタジアムで開催予定です。開演は14日が17時30分、15日が17時と公式スケジュールで案内されています。日によって時刻が違うため、前日の記憶だけで出発しないようにします。')+p('座席名やゲートが分かったら、チケット表示・本人確認・入場案内を照合します。過去の座席表だけで見え方や入場口を断定しないこと。ステージの形や機材配置で視界が変わる場合があります。')),
('屋外は、待ち時間と帰りの装備も考える',p('当日の気温と天気予報を見て、脱ぎ着できる服を選びます。会場へ向かう時に暖かくても、待機中や帰りは体感が変わります。これは今回の天気予報ではなく、屋外公演に備える一般的な選び方です。雨具と荷物カバーは別に考え、濡れた物を入れる袋を用意しましょう。')),
('振りやコールを覚えきれなくても大丈夫',p('初参戦なら、好きな曲を聴いて気になる場面を楽しみにしておくだけでも準備になります。大声や動きを無理に合わせず、当日のアナウンスと周りの視界への配慮を優先。ペンライトやボードを高く掲げ続けたり、席の外へ動いたりする応援は避けます。')+p('双眼鏡を使うなら、曲の途中で初めて取り出すより、着席後にストラップやピントを確認しておくと扱いやすくなります。場面によって肉眼と切り替え、演出全体を見る時間も作ってみてください。')),
('現地と配信で準備を切り替える',p('現地参加できない場合は公式の配信案内を確認します。ライブ本編とリピート配信は日程が異なり、巻き戻しや後日視聴の条件も購入先ごとに読む必要があります。現地のグッズ購入権利と配信チケットを同じものとして扱わないでください。')+p(link('sakura-6th-prep','既存のアニラ入場準備メモ')))],['sakura_schedule','sakura_live'],['rain-kit','binoculars','live-items-picks'],group='櫻坂46'),

a('hinatazaka-live-first','ライブアドバイス','日向坂46ライブ初参戦ガイド｜ひなくり2026の会場・持ち物・チケット確認','日向坂ひなくり2026を例に、初参戦の準備を解説。会場ごとの日程、本人確認、写真登録と帰りの持ち物。','「ひなくりに行ってみたい」と思ったら、まず公演日と会場をセットにして確認しましょう。同じツアー名でも開催地が複数あると、交通や宿泊の準備を取り違えやすくなります。初参戦向けに、先に決めたいことを整理します。',[
('ひなくり2026は3会場',table(['開催地','会場','日程'],[('兵庫','神戸ワールド記念ホール','2026年11月21～23日'),('東京','国立代々木競技場 第一体育館','2026年12月9～11日'),('愛知','クロコくんホール（日本ガイシホール）','2026年12月22～24日')])+p('公式特設で確認した日程です。一般販売の開始予定は兵庫・東京が11月14日、愛知が11月28日で、いずれも12時から。実際の販売状況は販売ページを確認してください。')),
('電子チケットと本人確認を先に終わらせる',p('今回の公式案内では、顔写真付き電子チケットの顔写真登録や身分証の扱いに注意が必要です。スマホへアプリを入れただけで、入場準備完了とは限りません。自分が選んだ券種と受取方法の説明を読み、表示と登録を前日までに確認しておきます。')+p('同行者がいる場合は、各自の受取や本人確認についてもチェックします。人にチケットを任せきりにせず、自分が会場で何を提示するのか把握しておくと、入場前の行き違いを減らせます。')),
('冬のアリーナは、外で待つ時間もある',p('屋内会場でも、移動・入場待ち・帰りは屋外です。重ね着を選ぶ時は、脱いだ上着をどこへ入れるかまで考えます。大きなバッグを足元へ置けると決めつけず、持込条件やコインロッカーの利用条件を確認しましょう。')+p('タオルとペンライト、必要なら双眼鏡。購入品を入れる保護袋を足したら、一度全部を持って重さを確認。会場別に荷物を増減し、使わない予備で両手がふさがらないようにします。')),
('応援より先に、見たいものを決めてみる',p('初めてなら、好きな曲や気になるメンバーを一つ決めておくだけでも楽しみができます。コールを全部知っていることは参加条件ではありません。公式が案内する応援グッズのルールと当日の指示に従い、後ろの人の視界を妨げない範囲で楽しみましょう。')+p('12月11日には森本茉莉の卒業セレモニー実施が公式特設に記載されています。出演や企画は変更される場合があるため、参加する日付の案内を改めて確認してください。'))],['hina_live'],['live-items-picks','photo-storage','events-2026-2027'],group='日向坂46'),

a('keyaki-goods-care','収納','欅坂46のライブグッズを残す｜タオル・ペンライト・生写真の整理術','欅坂の過去グッズを公演年と一緒に保管。現行イベント情報と混同せず、使う物と残す物を分ける方法。','欅共和国のタオル、昔のペンライト、衣装別の生写真。思い出のグッズは、同じ収納に収めるより「どの公演のものか」を残すと後から見返しやすくなります。今のライブ情報とは分けて、記録として整理してみましょう。',[
('公演名・年・メンバーを一緒に記録',p('同じグッズ名でも、販売年や衣装が違うものがあります。外袋・注文履歴・当時の公式告知を手がかりに、分かる項目だけメモします。記憶が曖昧なものを無理に確定せず、「年未確認」と分けておく方が、後から照合しやすくなります。')+p('例：欅共和国2018／ペンライト／付属品確認済、というように短い記録で十分です。紙のラベルをグッズへ直接貼るのではなく、保管ケースや管理メモ側へ付けると、現物の状態を変えずに済みます。')),
('使うペンライトと保管する物を分ける',p('久しぶりに使う時は、指定の電池・電池室・ボタン・ストラップなどを確認。異常が見える場合に無理に使わず、取扱説明やメーカーの案内に従ってください。動作品としての保管と、記念品として残す目的は別に考えます。')+p('過去グッズだからといって、現在の公演で必ず使用できるとは限りません。櫻坂など現行公演へ持っていく場合は、その公演の使用可能グッズと発光ルールを確認してください。')),
('タオルは出し入れ、生写真はサイズを優先',p('タオルを畳んで立てる時は、見たい名前や公演ロゴを手前へ向けると探しやすくなります。長期保管前には、取扱表示に合わせて手入れし、乾いていることを確認。湿った衣類と生写真を同じ袋へまとめないようにします。')+p('生写真はスリーブ込みで収納内寸を確かめ、公演別・メンバー別のどちらで探すことが多いかで分類します。枚数を詰め込むより、追加する分の余白を残す方が入れ替えやすくなります。')),
('過去の告知と今の活動を分けて読む',p('欅坂公式には、2020年10月14日に櫻坂公式サイトが開設された告知があります。古い公演記事を現在の開催情報として紹介せず、欅坂の販売記録と現行の櫻坂イベントを別の入口にしています。')+p('<a href="/groups/keyakizaka.html">欅坂のグッズ販売記録 →</a> ／ '+link('sakurazaka-live-first','現在の櫻坂ライブ準備')))],['keyaki'],['storage-picks','past-goods','sakurazaka-live-first'],group='欅坂46'),

a('meet-greet-first','ミーグリ','坂道ミーグリ初心者ガイド｜オンライン・リアル・応募方法の違い','乃木坂・櫻坂・日向坂のミーグリが初めての人へ。対象商品、抽選購入、シリアル応募、本人確認の見分け方。','「CDを買えば話せるの？」と迷うところから始めて大丈夫です。ミーグリは、同じグループでも作品や開催方式によって申し込み方が異なります。買う前に、どのイベントの、どの権利が付く商品なのかを確かめましょう。',[
('オンラインとリアルを混同しない',table(['方式','参加する場所','先に確認すること'],[('オンライン','指定アプリを使い、対応する端末で参加','アプリ・端末条件、通信、受付時刻'),('リアル','案内された会場で対面参加','対象会場、受付締切、本人確認・荷物の扱い')])+p('オンラインでも本人確認があり、リアルでもチケットやアプリの準備が必要な場合があります。方式の名前だけで判断せず、対象イベントの詳細を開いてください。')),
('CDの販売先と参加特典を照合する',p('今回確認した乃木坂43rdと日向坂18thの対象商品は、オンライン参加権利が付く販売先としてforTUNE musicが指定されています。一般流通で同じ通常盤を買っても、その参加権利が付くとは扱われません。AmazonでCDを購入する場合も、ミーグリ権利付きと推測しないでください。')+p('別の企画ではシリアルを使う応募方法もあります。初回盤・通常盤という名称だけで決めず、公式告知の対象商品と応募条件を読みます。中古品は特典の使用状況を確かめにくい点にも注意が必要です。')),
('応募・当選・支払いを別の手順として確認',ul(['応募前：自分が参加できる日・部・メンバーを選ぶ。','申込時：すべて当選しても払える総額に収める。','結果発表後：当落だけでなく決済の必要手続きを確認する。','参加前：本人確認の名義と登録情報、対象アプリへの権利反映を確認する。'])+p('当たりやすさ、完売状況、秒数を根拠なく予想しないこと。一回の会話時間やまとめ出しの条件は、対象イベントの説明を優先します。')),
('初参加は一つの流れを確実にする',p('複数メンバー・複数部に一度に申し込むより、自分の予定と予算を把握して無理なく管理できる組み合わせを選びます。何を話すかは、曲やライブの感想を一つ決めるだけでも準備になります。認知や反応を保証するテクニックはありません。')+p(link('meet-talk-topics','会話ネタの作り方')+' ／ '+link('online-meet-setup','端末と部屋の準備')))],['fortune_n','fortune_h','fortune_rules'],['nogizaka-43-meet','real-meet-prep','online-meet-setup']),

a('online-meet-setup','ミーグリ','オンラインミーグリの準備｜スマホの置き方・音・明るさを整える','オンラインミーグリ前日の準備。端末条件、固定方法、音声、照明、受付中の操作を順番に確認。','当日になって、顔が暗い、音が出ない、スマホが倒れる。そんな慌ただしさを減らすため、前日に実際の場所で一度座ってみましょう。高価な配信機材をそろえる前に、手持ちの端末と部屋で確かめられることがあります。',[
('アプリと端末条件を先に確認する',p('対象イベントが指定するアプリ、対応端末・OS、ログイン方法を公式案内から確認します。古い説明記事の画面と今の表示は違う場合があるため、この記事ではOSの最低バージョンやボタン名を固定して案内しません。参加者名義と権利の反映も確認してください。')+p('アップデートや再ログインが必要なら、受付直前にまとめて行わず早めに済ませます。接続に不安がある場合は、公式が案内する事前確認やサポート窓口を確認しておきましょう。')),
('スタンドは顔の高さと充電口で選ぶ',p('スマホを置いた状態で顔全体が無理なく画面に収まるか、机を動かしても倒れないか、充電ケーブルが引っ張られないかを試します。低い机なら高さ調整ができる形、狭い机なら台座が小さい形など、設置条件から候補を絞るのがおすすめです。')+p('手帳型ケースを付けたまま固定する場合は、厚みと重心も変わります。スタンドの耐荷重だけでなく、ケース込みの端末を保持できるか確認。この記事は特定モデルの実使用レビューではありません。')),
('明るさと音は、同じ場所で試す',p('明るい窓を背にするより、顔の前側に光が来る座り方から試します。画面の明るさだけを上げても、カメラに映る顔が明るくなるとは限りません。卓上ライトを追加する時は、まぶしさや眼鏡への映り込みを確認して調整します。')+p('イヤホンを使うなら、端末でマイクが使えるかも確認します。普段の音楽再生ができることと、通話の入力が正しく動くことは別です。実際のイベントを録画してテストするのではなく、端末で使える通常の確認方法や公式の事前案内に従ってください。')),
('受付時刻を一つ前の予定として登録する',p('部の開始と受付終了は、同じ時刻とは限りません。待機に入った後のスリープやアプリ切替にも注意し、対象イベントが求める状態を保ちます。不具合が出た場合は、慌てて操作を繰り返すより、公式の当日サポート案内を確認してください。')+ul(['前日：アプリ・名義・権利・必要書類を確認。','開始前：充電、通信、カメラ位置、音を確認。','受付前：部とメンバー、使用する権利を照合。','待機中：指定された操作を守り、その場で待つ。']))],['fortune_rules'],['meet-talk-topics','meet-greet-first']),

a('real-meet-prep','ミーグリ','リアルミーグリの持ち物と当日の動き方｜初参加の準備メモ','リアルミーグリの受付、本人確認、荷物、名札、会場への移動。オンラインとの違いから持ち物を整理。','対面で推しに会う日は、話すことだけでなく「会場に着いてから受付まで」を考えておくと落ち着いて動けます。持ち物のルールは企画ごとに異なるため、ここでは共通して確認しておきたい順番を整理します。',[
('オンラインの参加権利で行けるとは限らない',p('作品名が同じでも、オンラインとリアルで応募先・権利・日程が分かれることがあります。参加できると思って交通を予約する前に、当選や参加権利の画面でイベント名と会場を確認しましょう。CDの所持だけでは、その対面企画の参加資格を証明できるとは限りません。')),
('書類は「使えるもの」を一式で用意',p('本人確認に使える書類、原本の要否、有効期限、複数点が必要かは、対象の公式案内で確認します。別グループや過去のイベントで通ったものが今回も通るとは限りません。アプリの登録情報と当日の参加者情報も照合しておきます。')+p('バッグへ入れる時は、出し入れしやすい位置にまとめます。画面や書類の写真をSNSへ投稿する際に個人情報が写らないようにするなど、準備の様子を共有する時も確認が必要です。')),
('持ち物は小さく、手順は見やすく',table(['確認項目','準備の例'],[('会場・時間','会場名、部、受付締切を一つのメモにする'),('参加に必要なもの','権利を表示する端末、公式指定の書類'),('移動・待機','充電、飲み物、脱ぎ着しやすい服'),('持込物','名札・ボード・プレゼント等は可否を個別確認')])+p('名札を使いたい場合も、サイズや付け方、持込可否を確認してから準備します。会話のために大きな道具を持てばよいというものではありません。ブースへ持っていける物と、事前に預ける物を当日の指示に従って分けます。')),
('帰りまで含めて無理のない予定にする',p('待ち時間や列の進み方には変動があります。会話の直後に遠い駅の電車を予約するなど、ぎりぎりの移動は避けます。複数部へ参加する人は、その間の休憩や食事も考えておきましょう。終了後に感想を残す時は、自分が覚えている範囲の言葉として書き、メンバーの発言を断定した記録にしない配慮も大切です。'))],['nogi_disc','hina_meet'],['meet-talk-topics','meet-greet-first']),

a('meet-talk-topics','ミーグリ','ミーグリで何を話す？初めてでも伝えやすい会話ネタと準備','ミーグリの話題が決まらない人へ。曲・ライブ・感謝を短く伝える例と、オンライン・リアル共通の準備。','話したいことはあるのに、いざ言葉にしようとするとまとまらない。そんな時は、質問をたくさん用意するより「今日伝えたい一つ」を選んでみましょう。ここにある文は編集部が作った会話例で、実際のメンバーの発言や反応を再現したものではありません。',[
('曲・ライブ・お礼の3つから選ぶ',table(['話題','短くする例'],[('曲の感想','「新曲の○○のところが好きで、何回も聴いています」'),('ライブの感想','「○日のライブで、○○の場面が特に印象に残りました」'),('お礼','「いつも通勤中に曲を聴いて元気をもらっています。ありがとう」'),('一つだけ質問','「最近、気分転換にしていることはありますか？」')])+p('具体的な曲名や場面を自分の体験に置き換えると、短くても何を伝えたいかが見えやすくなります。参加していないライブに行ったふりをしたり、知らない情報を無理に話題にしたりする必要はありません。')),
('時間が短くても伝わる組み立て',p('挨拶、伝えたいこと、一言のお礼。この三つを声に出して一度練習すると、長すぎる部分が分かります。持っている枚数から正確な会話秒数を予測するより、途中で終わっても自分の感想だけは伝わる並びにしておくと安心です。')+p('質問を入れるなら、一度に一つに絞ります。前置きが長いと返事を聞く時間が少なくなるため、「どうして好きになったか」を全部説明するより、今好きな部分を一つ伝える形がおすすめです。')),
('認知や特別な反応を目標にしすぎない',p('名前を覚えてもらえる、必ず喜んでもらえる、といった保証はありません。相手に答えにくい私生活の詮索、他人との比較、否定的な試し行為は避け、作品や本人が公に話している内容を話題の中心にすると会話を組み立てやすくなります。')),
('緊張して言葉が飛んだ時の一言',p('「初めてで緊張しています。今日は会えてうれしいです」だけでも、自分の気持ちを伝えられます。完璧な会話にしようとせず、挨拶とお礼の短い文を予備として覚えておきましょう。')+p('オンラインなら机の近くに自分用の短いメモ、リアルなら待機前に一度読むメモにしておく方法があります。ただし画面やブースで見せる物の可否、録音・録画などのルールは対象イベントの案内を優先してください。終了後は、自分の感想を自分の言葉で残す楽しみ方もあります。'))],['fortune_rules'],['online-meet-setup','real-meet-prep']),

a('nogizaka-43-meet','ミーグリ','乃木坂46「君ロス」ミーグリ｜第4次～第6次受付と参加権利の確認','乃木坂43rdミーグリの2026年11月受付を整理。申込期間、開催日、forTUNE限定特典と一般販売CDの違い。','乃木坂46の43rdシングル「君ロス」でミーグリを検討している人向けに、11月10日の公式告知から第4次～第6次受付を整理します。CDを買う場所と、イベントの参加権利を分けて確認しましょう。',[
('応募受付の予定',table(['受付','開始～終了（日本時間）'],[('第4次','2026年11月12日14:00～11月13日14:00'),('第5次','2026年11月19日14:00～11月20日14:00'),('第6次','2026年11月26日14:00～11月27日14:00')])+p('11月11日時点の確認内容です。第6次は12月6日開催分の最終受付と案内されています。販売状況や参加メンバーの変更は公式告知・販売画面で確認し、受付終了後にこの記事を見た場合は過去の予定として扱ってください。')),
('対象のイベント日程',p('対象日は2026年12月6日、2027年1月9日・31日、2月28日、3月13日・21日と告知されています。日付を選んだ後、メンバーと部の参加状況を確認します。応募できる枠があることと、その枠に当選できることは別です。')),
('参加権利付き商品は販売先まで照合',p('forTUNE musicが案内する対象通常盤はSRCL-13948です。対象のオンライン参加権利が付くのは同販売分と案内されています。一般のCDショップやAmazonで同じ品番を買うことを、参加方法として案内するものではありません。')+p('同作品のスペシャル応募企画とオンライン個別トーク会も、申し込みの仕組みが同じとは限りません。初回仕様や店舗特典と混ぜず、自分が参加したいイベントの公式告知から対象商品を確認してください。')),
('当落後に確認すること',ul(['決済の案内と期限を確認する。','購入内容の日・部・メンバーをメモする。','本人確認の名義と必要書類を確認する。','指定アプリと対応端末を準備する。'])+p('受付回によっておまとめ配送の扱いや配送予定も異なります。送料を含む総額と受取予定を、購入を確定する前に確認しましょう。このページでは未確認の当選率や完売予測は掲載しません。'))],['nogi_meet','fortune_n','nogi_disc'],['meet-greet-first','online-meet-setup','meet-talk-topics'],group='乃木坂46')
]

CATS=['イベント','最新情報','収納','ライブ用品','ライブアドバイス','ミーグリ']
OLD=[('past-goods','過去の公式グッズの探し方'),('photo-storage','生写真とアクスタの収納選び'),('live-kit','参戦グッズの選び方'),('buying-check','中古・マーケットプレイスの確認点'),('sakura-6th-prep','櫻坂6thアニラ｜入場前の準備メモ'),('binoculars','ライブ双眼鏡｜8倍・10倍の選び方'),('rain-kit','屋外ライブ｜荷物の雨対策'),('acsta-carry','アクスタの持ち運びとケース選び'),('photo-sleeves','生写真スリーブとファイルのサイズ選び')]

def cards(items):
 return '<div class="edit-cards">'+''.join(f'<a class="edit-card" href="/notes/{x["slug"]}.html"><span class="edit-thumb" data-cat="{x["cat"]}"><small>{x["group"]}</small><b>{x["cat"]}</b><span>YORIMICHI NOTE</span></span><span class="edit-card-copy"><small>{x["cat"]} ／ {DAY}公開</small><strong>{x["title"]}</strong><span>{x["desc"]}</span></span><b aria-hidden="true">↗</b></a>' for x in items)+'</div>'


def official_screen():
    videos=[('乃木坂46','「君ロス」Music Video','OzhgQxSoljI','nogizaka-live-first','#8b46b1'),('櫻坂46','5th YEAR ANNIVERSARY LIVE / Digest','jteJsHAj6GE','sakurazaka-live-first','#cf547e'),('日向坂46','「イチャイチャ虫」Music Video','mgFUz_c4ToM','hinatazaka-live-first','#2498c8')]
    content='<section class="official-screen"><div class="screen-heading"><p>SAKAMICHI ON SCREEN</p><h2>好きな坂道から、次の楽しみへ。</h2><span>公式映像と、参戦のヒント。</span></div><div class="screen-track">'
    for name,title,vid,slug,color in videos:
        content+=f'<article class="screen-card" style="--screen-color:{color}"><div class="screen-video"><iframe src="https://www.youtube-nocookie.com/embed/{vid}" title="{name}公式 {title}" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" allow="encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe></div><div class="screen-caption"><small>{name} / OFFICIAL YouTube</small><h3>{title}</h3><a href="/notes/{slug}.html">{name}のライブ準備を読む →</a><a class="screen-original" href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noopener noreferrer">YouTubeで見る ↗</a></div></article>'
    return content+'</div><p class="screen-source">各グループの公式YouTube動画を埋め込んでいます。商品写真ではありません。</p></section>'


def render(out,page):
 byslug={x['slug']:x for x in ARTICLES}
 for x in ARTICLES:
  toc='<nav class="edit-toc" aria-label="この記事の目次"><strong>この記事で読むこと</strong><ol>'+''.join(f'<li><a href="#part-{i}">{t}</a></li>' for i,(t,b) in enumerate(x['sections'],1))+'</ol></nav>'
  sources='<section class="edit-sources"><h2>参照した公式情報</h2><p>確認日：'+DAY+'。日程・応募条件はリンク先の変更告知も確認してください。選び方・持ち物・会話例は当サイトの編集による提案で、公式指定と区別しています。</p><ul>'+''.join(f'<li><a href="{esc(S[k][1])}" target="_blank" rel="noopener noreferrer">{esc(S[k][0])} ↗</a></li>' for k in x['sources'])+'</ul></section>'
  related='<section class="edit-related"><h2>あわせて読みたい</h2>'+ul([link(slug,byslug[slug]['title'] if slug in byslug else dict(OLD).get(slug,slug)) for slug in x['related']])+'</section>'
  body='<div class="wrap edit-article"><nav class="edit-breadcrumb" aria-label="パンくず"><a href="/">ホーム</a> / <a href="/articles.html">推し活記事</a> / '+x['cat']+'</nav><article class="prose"><div class="edit-article-heading"><p class="eyebrow">'+x['group']+' ／ '+x['cat']+'</p><h1>'+x['title']+'</h1><p class="edit-date">公開・情報確認：<time datetime="2026-11-11">'+DAY+'</time></p></div><p class="lead">'+x['lead']+'</p>'+toc+''.join(f'<section id="part-{i}"><h2>{t}</h2>{b}</section>' for i,(t,b) in enumerate(x['sections'],1))+sources+related+'<a class="button" href="/articles.html">記事一覧へ戻る →</a></article></div>'
  (out/'notes'/f'{x["slug"]}.html').write_text(page(x['title'],body,x['desc']))
 hub='<div class="wrap edit-hub"><p class="eyebrow">SAKAMICHI FAN JOURNAL</p><h1>次の楽しみを、見つけよう。</h1><p class="lead">イベントの予定から、推しに会う日の準備まで。<br>坂道ファンのための読みものを集めました。</p><nav class="edit-tabs" aria-label="記事カテゴリー">'+''.join(f'<a href="#cat-{i}">{cat}</a>' for i,cat in enumerate(CATS))+'</nav>'
 for i,cat in enumerate(CATS):hub+=f'<section id="cat-{i}" class="edit-category"><h2>{cat}</h2>'+cards([x for x in ARTICLES if x['cat']==cat])+'</section>'
 hub+='<section class="edit-category"><h2>これまでの読みもの</h2>'+ul([link(slug,title) for slug,title in OLD])+'</section></div>'
 hub=hub.replace('<nav class="edit-tabs"',official_screen()+'<nav class="edit-tabs"',1)
 (out/'articles.html').write_text(page('坂道のイベント・収納・ライブ・ミーグリ記事一覧',hub,'坂道ファン向け22記事。乃木坂・櫻坂・日向坂のイベント情報、収納、ライブ用品、初参戦とミーグリ準備をカテゴリー別に。'))
 # Add discoverable entrances without replacing the existing nine articles.
 for path in out.rglob('*.html'):
  if re.fullmatch(r'google[0-9a-f]+\.html',path.name):continue
  text=path.read_text().replace('</head>','<link rel="stylesheet" href="/editorial.css?v=3"></head>')
  text=text.replace('<a href="/#notes">読みもの</a>','<a href="/notes/events-2026-2027.html">イベント</a><a href="/articles.html">記事一覧</a>')
  if path==out/'index.html':
   featured=official_screen()+'<section class="wrap edit-home"><div class="section-heading"><div><p class="eyebrow">NEW / FAN JOURNAL</p><h2>推し活の「知りたい」を、ここから。</h2></div><a href="/articles.html">全22記事を見る →</a></div>'+cards([byslug[s] for s in ['events-2026-2027','news-20261111','storage-picks','live-items-picks','meet-greet-first','nogizaka-43-meet']])+'<nav class="edit-tabs" aria-label="ライブ準備の記事">'+''.join(link(s,t) for s,t in [('nogizaka-live-first','乃木坂ライブ'),('sakurazaka-live-first','櫻坂ライブ'),('hinatazaka-live-first','日向坂ライブ'),('keyaki-goods-care','欅坂グッズ')])+'</nav></section>'
   text=text.replace('<section class="section wrap" id="archive">',featured+'<section class="section wrap" id="archive">',1)
  if path==out/'notes.html':
   text=text.replace('<main id="main">','<main id="main"><aside class="wrap edit-note-banner"><strong>新着13記事を追加しました</strong><a href="/articles.html">イベント・収納・ライブ・ミーグリの記事へ →</a></aside>')
  group=path.stem if path.parent.name=='groups' else None
  names={'nogizaka':'乃木坂46','sakurazaka':'櫻坂46','hinatazaka':'日向坂46','keyakizaka':'欅坂46'}
  if group in names:
   picks=[x for x in ARTICLES if x['group']==names[group]]
   text=text.replace('</main>','<section class="wrap edit-home"><h2>'+names[group]+'の準備・読みもの</h2>'+cards(picks)+'</section></main>')
  if path==out/'privacy.html':
   text=text.replace('</article>','<h2>埋め込み動画について</h2><p>一部ページで各グループの公式YouTube動画をプライバシー強化モードで埋め込んでいます。再生などの操作ではYouTubeの利用条件とプライバシーポリシーが適用されます。</p></article>')
  path.write_text(text)
 (out/'editorial.css').write_text(CSS)

CSS='''
.edit-hub{padding-top:35px;padding-bottom:45px;display:grid;grid-template-columns:1fr 1fr;column-gap:22px}.edit-hub>p,.edit-hub>h1,.edit-hub>nav{grid-column:1/-1}.edit-hub>.edit-category{margin-bottom:18px;padding-top:8px}.edit-hub>.edit-category>.edit-cards{grid-template-columns:1fr}.edit-hub>#cat-4,.edit-hub>#cat-5,.edit-hub>.edit-category:last-child{grid-column:1/-1}.edit-hub>#cat-4>.edit-cards,.edit-hub>#cat-5>.edit-cards{grid-template-columns:1fr 1fr}.edit-hub>h1{font-size:clamp(27px,4vw,40px);line-height:1.6}.edit-tabs{display:flex;flex-wrap:wrap;gap:9px;margin:24px 0}.edit-tabs>a{background:#f2eaf8;border:1px solid #e6d8ef;padding:9px 14px;border-radius:5px;font-size:12px;color:#7c519b}.edit-category{padding-top:22px;margin-bottom:32px;scroll-margin-top:20px}.edit-category>h2{font-size:24px;border-bottom:1px solid #e8deed;padding-bottom:13px}.edit-cards{display:grid;grid-template-columns:1fr 1fr;gap:13px}.edit-card{display:grid;grid-template-columns:88px 1fr 12px;gap:15px;background:#fff;border:1px solid #e7ddec;border-radius:8px;padding:14px;align-items:center}.edit-card:hover{border-color:#b998cf;box-shadow:0 3px 12px #794d9110}.edit-thumb{height:105px;border-radius:5px;background:#eee3f7;color:#8c5aab;display:flex;flex-direction:column;justify-content:center;text-align:center;border-top:4px solid #9b74b8;padding:7px}.edit-thumb[data-cat="ミーグリ"]{background:#fbe8f0;color:#b7688b;border-color:#d88eaf}.edit-thumb[data-cat="イベント"],.edit-thumb[data-cat="最新情報"]{background:#e8f4fb;color:#518eaa;border-color:#80b5cb}.edit-thumb[data-cat="ライブアドバイス"],.edit-thumb[data-cat="ライブ用品"]{background:#edf4ec;color:#5b8a65;border-color:#88b090}.edit-thumb small{font-size:9px}.edit-thumb b{font-size:14px;line-height:1.5;margin:10px 0}.edit-thumb>span{font-size:6px;letter-spacing:.06em}.edit-card-copy{min-width:0}.edit-card-copy>small{font-size:9px;color:#a28aaf}.edit-card-copy>strong{display:block;font-size:16px;line-height:1.65;margin:6px 0;color:#4c375b}.edit-card-copy>span{font-size:11px;color:#8c7e94;line-height:1.8;display:block}.edit-card>b{color:#ae8dc3;font-size:12px}.edit-home{padding-top:25px;padding-bottom:32px}.edit-home .section-heading h2{font-size:26px!important}.edit-home .section-heading>a{font-size:12px;color:#845c9d}.edit-breadcrumb{font-size:11px;color:#9c85a9;padding:22px 0}.edit-article .prose{max-width:800px;padding-top:0}.edit-article-heading{padding:25px 26px;border:1px solid #e7d9ef;border-left:5px solid #a47bbd;background:#f6f0fa;border-radius:8px;margin-bottom:25px}.edit-article-heading h1{font-size:clamp(25px,3vw,35px);line-height:1.6;margin:10px 0 15px}.edit-date{font-size:11px!important;color:#9b81aa}.edit-article .lead{font-size:16px;line-height:2.1}.edit-article section{scroll-margin-top:25px}.edit-article section>h2{font-size:23px;line-height:1.6;margin-top:38px;padding-left:14px;border-left:4px solid #bb9ccf}.edit-article p,.edit-article li{line-height:2;font-size:15px}.edit-toc{display:block!important;background:#faf7fc;border:1px solid #e9dfef;border-radius:7px;padding:20px 23px;margin:26px 0}.edit-toc>strong{font-size:13px}.edit-toc ol{margin:9px 0 0;padding-left:22px}.edit-toc li{font-size:13px;padding:3px 0}.edit-table{overflow-x:auto;margin:22px 0;border:1px solid #e4d8ec;border-radius:7px}.edit-table table{border-collapse:collapse;width:100%;min-width:470px;margin:0;font-size:13px}.edit-table th{background:#eee4f5;color:#735286;text-align:left}.edit-table td,.edit-table th{padding:13px 14px;border-bottom:1px solid #ece4f1;vertical-align:top;line-height:1.8}.edit-table tr:last-child td{border-bottom:0}.edit-table td{background:#fff}.edit-table td:first-child{font-weight:600}.edit-sources{background:#f8f6fa;border:1px solid #e9e1ed;border-radius:7px;padding:18px 22px;margin-top:35px}.edit-sources h2{font-size:18px!important;margin:0 0 10px!important}.edit-sources p,.edit-sources li{font-size:12px!important}.edit-related{padding-bottom:15px}.edit-related li{margin-bottom:9px}.edit-note-banner{background:#f0e8f7;border-radius:8px;padding:18px 24px;margin-top:24px;display:flex;gap:18px;flex-wrap:wrap;font-size:13px}.edit-note-banner a{color:#865b9d}
@media(max-width:700px){.edit-hub{display:block}.edit-hub>#cat-4>.edit-cards,.edit-hub>#cat-5>.edit-cards{grid-template-columns:1fr}.edit-cards{grid-template-columns:1fr}.edit-card{grid-template-columns:74px 1fr 10px;gap:12px;padding:12px}.edit-thumb{height:90px}.edit-thumb b{font-size:12px;margin:8px 0}.edit-card-copy>strong{font-size:15px;line-height:1.65}.edit-card-copy>small{font-size:8px}.edit-card-copy>span{font-size:10px}.edit-home .section-heading{display:block}.edit-home .section-heading h2{font-size:22px!important}.edit-home .section-heading>a{display:inline-block;margin-top:8px}.edit-hub{padding-top:25px}.edit-tabs>a{font-size:11px;padding:8px 10px}.edit-tabs{gap:7px}.edit-article-heading{padding:20px 18px}.edit-article-heading h1{font-size:26px}.edit-article .lead,.edit-article p,.edit-article li{font-size:14px}.edit-article section>h2{font-size:21px}.edit-toc{padding:16px}.edit-toc li{font-size:12px}.edit-breadcrumb{font-size:10px}.edit-sources{padding:16px}.edit-note-banner{font-size:12px}}

/* Consistent list rhythm and touch layout on narrow screens. */
.edit-hub{row-gap:0}
.edit-hub>h1{margin:8px 0 14px}
.edit-hub>.lead{margin:0 0 6px}
.edit-hub>.edit-tabs{justify-content:flex-start;flex:none;margin:18px 0 20px}
.edit-hub>.edit-category{margin:0 0 24px;padding-top:0}
.edit-category>h2{margin:0 0 14px;padding:0 0 10px}
.edit-card{align-items:center;min-height:132px}
.edit-card-copy>strong{font-family:inherit;font-weight:700}
.edit-card-copy>span{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.edit-card-copy>small{display:block;line-height:1.5}
.edit-category:last-child>ul{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:1fr 1fr;gap:8px 20px}
.edit-category:last-child>ul>li{margin:0;border-bottom:1px solid #e9e1ee;padding:10px 0;font-size:13px}
@media(max-width:700px){
header{padding:16px 18px!important}
header .brand{font-size:22px}
header nav[aria-label="メイン"]{display:flex!important;flex-wrap:nowrap!important;justify-content:flex-start!important;gap:20px!important;overflow-x:auto;white-space:nowrap;margin-top:14px!important;padding:0 0 6px!important;scrollbar-width:thin}
header nav[aria-label="メイン"]>a{flex:0 0 auto;font-size:11px;line-height:1.5}
.edit-hub{padding:24px 18px 32px!important}
.edit-hub>.eyebrow{font-size:9px;margin-bottom:10px}
.edit-hub>h1{font-size:26px;letter-spacing:-.025em;line-height:1.5;margin:0 0 14px}
.edit-hub>.lead{font-size:13px;line-height:1.85;margin:0}
.edit-hub>.edit-tabs{display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px;margin:18px 0 26px;justify-content:stretch}
.edit-hub>.edit-tabs>a{font-size:11px;padding:9px 3px;line-height:1.5;text-align:center;border-radius:5px;white-space:nowrap}
.edit-hub>.edit-category{margin:0 0 25px;padding:0}
.edit-category>h2{font-size:19px;line-height:1.5;padding-bottom:9px;margin:0 0 12px}
.edit-cards{gap:9px}
.edit-card{grid-template-columns:64px minmax(0,1fr)!important;gap:12px!important;padding:12px!important;min-height:122px;border-radius:7px}
.edit-card>b{display:none}
.edit-thumb{width:64px;height:76px;min-height:0;padding:5px;border-top-width:3px}
.edit-thumb small{font-size:8px;line-height:1.5}
.edit-thumb b{font-size:10px;line-height:1.5;margin:7px 0}
.edit-thumb>span{font-size:5px;letter-spacing:0;white-space:nowrap}
.edit-card-copy>small{font-size:9px;line-height:1.4;color:#8e789a}
.edit-card-copy>strong{font-size:14px!important;line-height:1.6;margin:5px 0;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;overflow-wrap:anywhere}
.edit-card-copy>span{font-size:11px!important;line-height:1.65}
.edit-category:last-child>ul{display:block}
.edit-category:last-child>ul>li{font-size:12px;line-height:1.7;padding:12px 0}
.edit-breadcrumb{display:block!important;text-align:left;line-height:1.8;padding:16px 0}
footer{padding:25px 18px!important}
footer p{font-size:9px;line-height:1.8}
}


/* Actual official footage, with readable editorial hierarchy. */
.edit-hub>.eyebrow{color:#8d42a8;letter-spacing:.18em}
.edit-hub>h1{font-size:42px;font-weight:850;letter-spacing:-.045em}
.official-screen{grid-column:1/-1;background:#302039;color:#fff;border-radius:12px;padding:25px;margin:20px 0 25px;min-width:0}
.fan-home main>.official-screen{max-width:1116px;margin:25px auto}
.screen-heading{margin-bottom:17px}
.screen-heading>p{font-size:9px;letter-spacing:.2em;color:#e3bceb;margin:0 0 8px;font-weight:700}
.screen-heading h2{font-size:23px;line-height:1.6;margin:0;color:#fff;font-family:inherit;font-weight:750}
.screen-heading>span{font-size:11px;color:#cfbbd7}
.screen-track{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
.screen-card{background:#fff;color:#34203e;border-radius:8px;overflow:hidden;min-width:0;border-bottom:4px solid var(--screen-color)}
.screen-video{position:relative;aspect-ratio:16/9;background:#18141c}
.screen-video iframe{border:0;position:absolute;inset:0;width:100%;height:100%}
.screen-caption{padding:13px}
.screen-caption>small{font-size:9px;font-weight:700;color:var(--screen-color)}
.screen-caption h3{font-size:14px;line-height:1.6;min-height:44px;margin:6px 0 10px}
.screen-caption>a{font-size:11px;font-weight:700;color:var(--screen-color);display:block}
.screen-caption>.screen-original{font-size:9px;font-weight:400;color:#8b7d92;margin-top:7px}
.screen-source{font-size:9px;color:#c4b1cd;margin:15px 0 0}
.edit-hub>.edit-category>h2{border-bottom:2px solid #dbc5e9}
@media(max-width:700px){
.edit-hub>h1{font-size:29px;font-weight:850}
.official-screen{margin:21px -6px 23px;padding:18px 12px 14px;border-radius:9px}
.screen-heading{padding:0 4px;margin-bottom:13px}
.screen-heading h2{font-size:20px;line-height:1.5;letter-spacing:-.025em}
.screen-heading>span{font-size:10px}
.screen-track{display:flex;gap:12px;overflow-x:auto;scroll-snap-type:x mandatory;padding-bottom:8px}
.screen-card{flex:0 0 88%;scroll-snap-align:start}
.screen-caption{padding:12px 14px}
.screen-caption h3{font-size:15px;min-height:0;margin:5px 0 10px}
.screen-caption>a{font-size:12px}
.screen-source{font-size:8px;line-height:1.7;padding:0 4px}
.edit-card{border:0;border-bottom:1px solid #e9dfef;border-radius:0;background:transparent;padding:13px 0!important}
.edit-thumb{border-radius:7px;background:#eadcf3}
}

'''
