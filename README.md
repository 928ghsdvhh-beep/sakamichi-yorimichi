# 坂道よりみち

既存サイトからのCloudflare Pages移行用ソース。

## Cloudflare Pages

- Production branch: `main`
- Build command: `pip install -r requirements.txt && python src/build.py`
- Output directory: `dist`
- `SITE_URL`: 確定した本番URL（末尾スラッシュなし）を設定。未設定時はCloudflareの`CF_PAGES_URL`を利用。

既存の公開サイトは移行先の動作確認が終わるまで維持する。
AmazonアソシエイツIDは `moon12-22`。秘密キーをソースに保存しない。

## 再生成の確認

CSS・ブラウザ用JavaScript・Google所有権確認ファイルの編集元は `src/static/`。
ビルド開始時に `dist/` へコピーするため、既存の `dist/` がない状態でも生成できます。
`dist/` の静的ファイルだけを編集せず、対応する `src/static/` を修正してください。

`python scripts/check_build.py` は一時ディレクトリで、空の出力先・連続2回目・既存出力先からの
ビルドを実行し、コミット済み `dist/` の全ファイルとバイト単位で比較します。
ソースを変更した場合は先に `python src/build.py` で `dist/` を更新してから実行します。
最後に既存の静的監査も実行します。作業中の `dist/` は変更しません。

2026年11月15日の明示的な設置依頼により、ケンコー双眼鏡を紹介する4ページでは、ユーザー提供の商品URLを使用し、追加指示に従ってTracking IDを `moon12-22` に統一しています。許可した追加広告は `scripts/approved-affiliate-additions.json` に記録し、元の広告保全台帳は保持しています。
