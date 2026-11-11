# 坂道よりみち

既存サイトからのCloudflare Pages移行用ソース。

## Cloudflare Pages

- Production branch: `main`
- Build command: `pip install -r requirements.txt && python src/build.py`
- Output directory: `dist`
- `SITE_URL`: 確定した本番URL（末尾スラッシュなし）を設定。未設定時はCloudflareの`CF_PAGES_URL`を利用。

既存の公開サイトは移行先の動作確認が終わるまで維持する。
AmazonアソシエイツIDは `moon12-22`。秘密キーをソースに保存しない。
