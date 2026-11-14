"""Apply reviewed editorial additions without changing advertising code."""
from pathlib import Path
import json,re

def apply(out):
    source=Path(__file__).parent
    additions=json.loads((source/'monetization-content.json').read_text())
    (out/'decision-guide.css').write_text((source/'decision-guide.css').read_text())
    for path in out.rglob('*.html'):
        if path.name.startswith('google'): continue
        text=path.read_text()
        rel=path.relative_to(out).as_posix()
        addition=additions.get(rel)
        if addition:
            # Keep additions inside the existing article column.
            marker='</article>' if '</article>' in text else '</main>'
            text=text.replace(marker,addition+marker,1)
        text=text.replace('</head>','<link rel="stylesheet" href="/decision-guide.css"></head>')
        if rel in ('goods/nogi-photo-holder24.html','goods/nogi-photo-holder25.html'):
            year='2024' if '24.html' in rel else '2025'
            text=text.replace('乃木坂46 個別生写真ホルダー｜','乃木坂46 個別生写真ホルダー '+year+'年販売分｜')
            text=text.replace('<h1>個別生写真ホルダー</h1>','<h1>個別生写真ホルダー '+year+'年販売分</h1>')
        path.write_text(text)
