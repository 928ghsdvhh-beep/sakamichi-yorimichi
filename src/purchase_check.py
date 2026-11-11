"""Practical buying checks; no new product specifications or reviews."""
from html import escape as e
import re,json
DATA=('notes/buying-check.html', '注文前に照合する、グッズと出品条件', [('商品の一致', 'グループ・メンバー・販売年・公演名', '似た衣装や同名シリーズでも、希望する販売回の商品か確認'), ('セット内容', '本体・台座・特典・付属品の一覧', '画像に写る物がすべて付くと判断せず、商品説明と照合'), ('状態', '未開封・開封済み・使用済みの区別と傷の説明', '説明が曖昧なら、価格だけで同条件の商品と比較しない'), ('到着・費用', '商品代、送料、到着予定日、返品条件', 'イベントに間に合うかと、支払い総額を注文前に確認')], [('/notes/past-goods', '販売年や公演名から過去グッズを整理'), ('/notes/photo-storage', '生写真の収納方法'), ('/notes/acsta-carry', 'アクスタの持ち歩き方')])
def section(data):
 _,title,rows,links=data
 return '<section id="purchase-comparison" style="margin:32px 0;padding:18px;border:1px solid #dce3de;border-radius:12px"><h2>'+e(title)+'</h2><p>気になる商品が見つかったら、次の項目を手元の寸法や販売ページの説明と照らし合わせてください。確認できない項目は、購入判断を保留するためのメモにできます。</p><div role="region" aria-label="購入前の確認表" tabindex="0" style="overflow-x:auto"><table style="width:100%;min-width:560px;border-collapse:collapse;text-align:left"><caption style="text-align:left;margin:8px 0">確認する対象・調べる項目・判断時の注意</caption><thead><tr>'+''.join('<th scope="col" style="padding:10px;border-bottom:2px solid #b9c7be">'+e(x)+'</th>' for x in ['対象','調べる項目','判断時の注意'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join(('<th scope="row"' if i==0 else '<td')+' style="padding:10px;border-bottom:1px solid #dce3de;vertical-align:top">'+e(c)+('</th>' if i==0 else '</td>') for i,c in enumerate(row))+'</tr>' for row in rows)+'</tbody></table></div><h2>確認したい項目を詳しく読む</h2><ul>'+''.join('<li><a href="'+url+'">'+e(label)+'</a></li>' for url,label in links)+'</ul><p style="font-size:13px">編集更新：2026年11月12日。購入前の確認表と関連記事への案内を追加しました。商品仕様・販売条件の確認日は各記事の記載をご覧ください。</p></section>'
def enrich(path,data):
 h=path.read_text()
 if 'id="purchase-comparison"' in h:raise RuntimeError('already enriched')
 h=h.replace('</main>',section(data)+'</main>')
 # Match only the edit date; do not alter the original publication date or claim a fresh specification check.
 def schema(m):
  d=json.loads(m.group(1))
  if d.get('@type') in ('Article','BlogPosting'):d['dateModified']='2026-11-12'
  return '<script type="application/ld+json">'+json.dumps(d,ensure_ascii=False).replace('<','\\u003c')+'</script>'
 h=re.sub(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',schema,h,flags=re.S)
 path.write_text(h)

def extend(out):
    enrich(out/DATA[0], DATA)
