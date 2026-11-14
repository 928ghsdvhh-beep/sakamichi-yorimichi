# sakamichi-yorimichi 収益化改善報告（2026年11月14日）

作業ブランチ：`improve/monetization-2026-11-14`。mainへのマージ・本番公開は未実施です。
既存サイトの修正です。公開中のデザイン、広告コード、Tracking ID、解析IDを保持。順位・AIO引用・成果発生は検証できていません。

## 優先問題と変更

公開中のファン向けデザインを既存ビルドで再現。生写真スリーブ・双眼鏡記事に寸法確認、型番照合、用途別の比較を補足。2024年・2025年生写真ホルダーの重複タイトルを販売年で区別。非公式表示を維持。

既存mainのdistが古く、公開サイトはmainのsrcをビルドした内容です。今回の生成差分には、既存の14記事・既存CSS・既存アイコンの再生成を含みます。新しいサイトや新しいデザインを作った差分ではありません。既存公開記事と既存生成処理を保持しています。

## 本文を充実した既存記事

文字数はHTMLからscript/styleと空白を除いた概算で、評価指標ではありません。文字数のための水増しはしていません。

| 記事（公開ディレクトリからの相対パス） | 本文概算・改善前 → 改善後 |
| --- | --- |
| `notes/photo-sleeves.html` | 1077 → 1619 |
| `notes/binoculars.html` | 1038 → 1456 |

パンくずを追加した記事は、その表示内容に合うBreadcrumbListを設定。既存のArticleとcanonicalは照合済みです。架空のReview・AggregateRating・Offerは新設していません。購入者レビュー10本文以上を個別確認できた商品は0件で、レビュー要約は追加していません。価格・仕様の古い確認日を一律に新しくしていません。

## 検証結果

- 静的検証：53ページ（404含む）、エラー0。タイトル・description・h1、canonical、サイトマップ、内部リンク・アンカー・参照資産、JSON-LD、重複タイトル・canonical、トップからの到達性を点検。
- サイトマップ：52URL。noindexとの整合を検証。robots.txtは既存のクロール許可と本番Sitemap指定を維持。
- ブラウザ：360・390・1440pxの159ケース。ページ横はみ出し0。外部広告・解析への通信は遮断。画像の実配信や計測通信の成功を意味しません。
- 改善前の横はみ出し：0ケース → 改善後0ケース。
- 広告保全：リンク・広告画像のHTML断片0個をSHA-256照合、一致。`scripts/affiliate-baseline.json`が修正前の基準です。既存Tracking ID：実リンクなし。
- 外部参照先：36URLをHTTP GETで点検。未確認・差し替え前404を含む応答記録は`external-links.json`参照。403/503はリンク切れと断定しません。
- 公開状態：本番の既存ページ・robots・sitemapは200、無効URLは404。ブランチの改善は本番未反映です。
- 表示速度：メダカでは外部画像6リクエストを除去。他サイトを含む本番CWV・Lighthouse・実ユーザーLCP/INP/CLSは未測定。高速化の数値効果は主張しません。

生成サイトはビルド成功、2回目のビルドによる配信ファイル差分0。

既存ツールの動作確認：収納サイズ差の計算、チェック状態の保存・再読込・リセット、グループ絞り込み。すべて成功。

## 未確認事項・公開前の判断

既存コードがASIN未照合のAmazonリンクを非掲載にしており、実際の広告リンクは0件です。4候補のASIN照合を検索しましたが確定できず、リンク新設を保留。仕様解説・内部リンクの改善は済みましたが、Amazon経由の収益化完了とは報告できません。メーカーへの参照リンクは購入成果リンクではありません。

共通：Amazonの商品ページの現在の表示・レビュー本文10件、A8管理画面の提携・成果対象・掲載URL、Search Consoleのクエリ別表示回数・CTR・順位、Cloudflare実測速度、実際の成果計測は未確認。広告をテスト購入・申込する検証は行っていません。既存の商品画像は、A8バナー・イメージ・メーカー参照を区別。新しい未許諾写真を追加していません。

## 全ページの診断台帳

`page-audit.json`にtitle/h1/description/canonical・index可否・サイズ・リンク数・構造化データ・到達性を保存。全ページに一律のタイトル変更はせず、検索意図が重なる販売年違いを区別し、問題のある記事とUIを優先しました。トップから到達できないindex許可ページ・内部リンク切れ・完全なタイトル重複は検証後0件。記事の統合・削除はしていません。

| ページ | 検索設定 | 本文概算 | 内部リンク先数 | 広告リンク・画像数 | 構造化データ |
| --- | --- | ---: | ---: | ---: | --- |
| `about.html` | index許可 | 841 | 5 | 0 | AboutPage |
| `index.html` | index許可 | 4852 | 49 | 0 | WebSite |
| `tools.html` | index許可 | 1368 | 10 | 0 | WebPage |
| `404.html` | noindex | 328 | 6 | 0 |  |
| `notes.html` | index許可 | 900 | 15 | 0 | WebPage |
| `privacy.html` | index許可 | 1010 | 5 | 0 | WebPage |
| `articles.html` | index許可 | 2434 | 26 | 0 | WebPage |
| `size-check.html` | index許可 | 671 | 7 | 0 | WebPage |
| `checklist.html` | index許可 | 769 | 9 | 0 | WebPage |
| `goods/hinata-towel25.html` | index許可 | 965 | 9 | 0 | WebPage |
| `goods/nogi-photo-holder25.html` | index許可 | 988 | 9 | 0 | WebPage |
| `goods/sakura-acsta24.html` | index許可 | 969 | 9 | 0 | WebPage |
| `goods/sakura-charm24.html` | index許可 | 957 | 9 | 0 | WebPage |
| `goods/nogi-tour-towel24.html` | index許可 | 962 | 9 | 0 | WebPage |
| `goods/nogi-photo-holder24.html` | index許可 | 982 | 9 | 0 | WebPage |
| `goods/nogi-summer24.html` | index許可 | 943 | 9 | 0 | WebPage |
| `goods/hinata-photo25.html` | index許可 | 936 | 9 | 0 | WebPage |
| `goods/sakura-member-pen2.html` | index許可 | 995 | 9 | 0 | WebPage |
| `goods/hinata-suzuka-holder25.html` | index許可 | 998 | 9 | 0 | WebPage |
| `goods/hinata-acsta25.html` | index許可 | 982 | 9 | 0 | WebPage |
| `goods/keyaki-pen18.html` | index許可 | 958 | 9 | 0 | WebPage |
| `goods/hinata-mini-nobori25.html` | index許可 | 956 | 9 | 0 | WebPage |
| `tools/kenko-8x21.html` | index許可 | 828 | 8 | 0 | WebPage |
| `tools/favluv-regular.html` | index許可 | 792 | 8 | 0 | WebPage |
| `tools/favluv-mini.html` | index許可 | 799 | 8 | 0 | WebPage |
| `tools/heiko-l-sleeve.html` | index許可 | 779 | 8 | 0 | WebPage |
| `groups/keyakizaka.html` | index許可 | 1130 | 17 | 0 | WebPage |
| `groups/hinatazaka.html` | index許可 | 1448 | 21 | 0 | WebPage |
| `groups/sakurazaka.html` | index許可 | 1329 | 19 | 0 | WebPage |
| `groups/nogizaka.html` | index許可 | 1468 | 21 | 0 | WebPage |
| `groups/aobazaka.html` | index許可 | 1027 | 15 | 0 | WebPage |
| `notes/events-2026-2027.html` | index許可 | 1736 | 11 | 0 | Article |
| `notes/online-meet-setup.html` | index許可 | 1639 | 8 | 0 | Article |
| `notes/live-items-picks.html` | index許可 | 1618 | 12 | 0 | Article |
| `notes/past-goods.html` | index許可 | 874 | 6 | 0 | Article |
| `notes/keyaki-goods-care.html` | index許可 | 1529 | 10 | 0 | Article |
| `notes/photo-storage.html` | index許可 | 1111 | 7 | 0 | Article |
| `notes/meet-talk-topics.html` | index許可 | 1561 | 8 | 0 | Article |
| `notes/nogizaka-43-meet.html` | index許可 | 1550 | 9 | 0 | Article |
| `notes/storage-picks.html` | index許可 | 1618 | 13 | 0 | Article |
| `notes/meet-greet-first.html` | index許可 | 1621 | 10 | 0 | Article |
| `notes/nogizaka-live-first.html` | index許可 | 1595 | 9 | 0 | Article |
| `notes/buying-check.html` | index許可 | 1372 | 9 | 0 | Article |
| `notes/acsta-carry.html` | index許可 | 1076 | 9 | 0 | Article |
| `notes/sakura-6th-prep.html` | index許可 | 999 | 10 | 0 | Article |
| `notes/photo-sleeves.html` | index許可 | 1619 | 12 | 0 | Article |
| `notes/real-meet-prep.html` | index許可 | 1494 | 8 | 0 | Article |
| `notes/binoculars.html` | index許可 | 1456 | 11 | 0 | Article |
| `notes/sakurazaka-live-first.html` | index許可 | 1521 | 10 | 0 | Article |
| `notes/rain-kit.html` | index許可 | 996 | 9 | 0 | Article |
| `notes/hinatazaka-live-first.html` | index許可 | 1617 | 8 | 0 | Article |
| `notes/news-20261111.html` | index許可 | 1688 | 7 | 0 | Article |
| `notes/live-kit.html` | index許可 | 952 | 7 | 0 | Article |

## 再実行・差分の確認

- `python scripts/check_site.py .`（Python標準ライブラリのみ）
- 全差分：`git diff main...improve/monetization-2026-11-14`
- 本番へのマージ・デプロイは別途承認後。プレビュー環境が自動生成されても本番とは区別。
- 公開後はcanonical・サイトマップの実応答、Search Consoleの除外理由、記事→広告クリック→成果を確認。変更前後で同じ期間・クエリを比較してください。
