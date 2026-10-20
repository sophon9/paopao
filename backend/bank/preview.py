"""Render sample items to an HTML page (and optionally a PNG) to eyeball them.

    python3 -m backend.bank.preview m.geo                 # writes /tmp/bank-preview.html
    python3 -m backend.bank.preview m.geo --png /tmp/geo.png --n 2
    python3 -m backend.bank.preview m.geo.angle --png /tmp/a.png --width 1100

The PNG is made with headless Google Chrome (full-page screenshot), so you
can open it with an image viewer / read_file to check figures visually.
"""

import html
import re
import subprocess
import sys
from pathlib import Path

from backend.bank import SKILLS, TEMPLATES
from backend.bank.core import run_template

ROOT = Path(__file__).resolve().parents[2]


def markup(text):
    t = html.escape(text)
    t = re.sub(r"\[\[(\d+) (\d+)/(\d+)\]\]",
               r'<span class="mixed">\1<span class="frac"><span>\2</span><span>\3</span></span></span>', t)
    t = re.sub(r"\[\[([^\]/]+)/([^\]]+)\]\]", r'<span class="frac"><span>\1</span><span>\2</span></span>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"==(.+?)==", r"<u>\1</u>", t)
    t = re.sub(r"_{3,}", '<span class="blank"></span>', t)
    return t.replace("\n", "<br>")


def table_html(t):
    head = "".join(f"<th>{markup(str(h))}</th>" for h in t.get("head", []))
    rows = "".join("<tr>" + "".join(f"<td>{markup(str(c))}</td>" for c in r) + "</tr>" for r in t["rows"])
    cap = f"<caption>{markup(t['caption'])}</caption>" if t.get("caption") else ""
    return f"<table>{cap}<thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table>"


def render(items):
    css = (ROOT / "figures.css").read_text(encoding="utf-8")
    cards = []
    for it in items:
        ch = "".join(
            f'<li class="{"ok" if i == it["answer_index"] else ""}">{markup(c)}'
            + (f'<small> ← [{it["why"][str(i)]["tag"]}] {html.escape(it["why"][str(i)]["why"])}</small>'
               if str(i) in it["why"] else "")
            + "</li>"
            for i, c in enumerate(it["choices"]))
        steps = "".join(f"<li>{markup(s)}</li>" for s in it["steps"])
        cards.append(f"""<div class="card"><div class="meta">{it['skill']} · {it['difficulty']} · {it['template']}</div>
{f'<div class="passage">{markup(it["passage"])}</div>' if it.get('passage') else ''}
{f'<div class="figure">{it["figure"]}</div>' if it.get('figure') else ''}
{table_html(it['table']) if it.get('table') else ''}
<div class="stem">{markup(it['stem'])}</div><ol>{ch}</ol>
<div class="hint">💡 {markup(it['hint'])}</div><ol class="steps">{steps}</ol></div>""")
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{css}
body{{font-family:"Noto Sans Thai",sans-serif;background:#faf6f8;margin:16px;display:grid;grid-template-columns:repeat(auto-fill,minmax(480px,1fr));gap:12px}}
.card{{background:#fff;border:1px solid #e8dfe4;border-radius:12px;padding:12px;font-size:14px}}
.meta{{color:#888;font-size:11px}} .stem{{font-weight:600;margin:8px 0}} .passage{{background:#fdf2f8;padding:8px;border-radius:8px;white-space:pre-wrap}}
li.ok{{color:#1b7a4e;font-weight:700}} small{{color:#a33;font-weight:400}} .hint{{color:#8d6e00}} .steps{{color:#334}}
.frac{{display:inline-flex;flex-direction:column;vertical-align:middle;text-align:center;font-size:.85em;margin:0 2px}}
.frac>span:first-child{{border-bottom:1.5px solid currentColor}} .mixed{{white-space:nowrap}}
.blank{{display:inline-block;width:60px;border-bottom:2px solid #333}} table{{border-collapse:collapse;margin:6px 0}} td,th{{border:1px solid #ccc;padding:3px 8px}}
.figure{{margin:6px 0}}</style></head><body>{''.join(cards)}</body></html>"""


def main(argv):
    out_html = Path("/tmp/bank-preview.html")
    png = None
    n = 1
    width = 1000
    filters = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--png":
            png = argv[i + 1]; i += 2; continue
        if a == "--n":
            n = int(argv[i + 1]); i += 2; continue
        if a == "--width":
            width = int(argv[i + 1]); i += 2; continue
        if a == "--html":
            out_html = Path(argv[i + 1]); i += 2; continue
        filters.append(a); i += 1

    def ok(t):
        if not filters:
            return True
        keys = (t.skill, SKILLS[t.skill]["topic"], t.name)
        return any(k.startswith(f) for f in filters for k in keys)

    items = []
    for t in TEMPLATES:
        if not ok(t):
            continue
        got = 0
        for _ in range(30):
            if got >= n:
                break
            batch = run_template(t)
            if batch:
                items.extend(batch)
                got += 1
    out_html.write_text(render(items), encoding="utf-8")
    print(f"{len(items)} items → {out_html}")
    if png:
        height = max(800, 420 * ((len(items) + 1) // 2))
        subprocess.run(["google-chrome", "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
                        f"--window-size={width},{min(height, 16000)}", f"--screenshot={png}",
                        out_html.as_uri()], check=False, capture_output=True, timeout=90)
        print(f"png → {png}")


if __name__ == "__main__":
    main(sys.argv[1:])
