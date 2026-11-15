# 坂道よりみち

既存サイトからのCloudflare Pages移行用ソース。

## Cloudflare Pages

- Production branch: `main`
- Build command: `pip install -r requirements.txt && python src/build.py`
- Output directory: `dist`
- `SITE_URL`: 確定した本番URL（末尾スラッシュなし）を設定。未設定時はCloudflareの`CF_PAGES_URL`を利用。

既存の公開サイトは移行先の動作確認が終わるまで維持する。
AmazonアソシエイツIDは `moon12-22`。秘密キーをソースに保存しない。

2026年11月15日の明示的な設置依頼により、ケンコー双眼鏡の2ページでは、ユーザー提供の広告URLを改変せず `ip17-22` で使用しています。許可した追加広告は `scripts/approved-affiliate-additions.json` に記録し、元の広告保全台帳は保持しています。
