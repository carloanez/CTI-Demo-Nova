"""Generate a self-contained conference-themed browser deck and presenter guide."""
import base64
import html
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
spec = json.loads((root / "slides/slide_content.json").read_text())
esc = lambda s: html.escape(str(s)).replace("\n", "<br>")

def image(file, alt, css=""):
    encoded = base64.b64encode((root / "slides" / file).read_bytes()).decode()
    return f'<img class="{css}" alt="{html.escape(alt, quote=True)}" src="data:image/png;base64,{encoded}">'

sections = []
notes = ["# Presenter guide\n\n60 minutes, including 28 minutes of notebook demonstration.\n\nRead README.md and docs/CLAUDE_DEPLOYMENT.md for setup. Keep instructor/executed_demo.ipynb available as a visibly labeled replay backup. No local model is used.\n\nHI Cyber Con revision: 22 slides with a conference-themed cover, introduction and QR-code closing. The conference website advertises 45-minute sessions. Confirm the assigned slot before presenting; this deck preserves Carlo's requested 60-minute plan.\n"]
for i, s in enumerate(spec, 1):
    kind = s["type"]
    content = '<div class="event">HI CYBER CON 2026</div>'
    content += f'<h1>{esc(s["title"])}</h1>'
    if kind == "cover":
        content = image("assets/hi-cyber-con-cover-art.png", "Original conceptual cyber investigator", "cover-art") + content
        content += f'<h2>{esc(s["subtitle"])}</h2><p class="presenter"><strong>Carlo Anez Mazurco</strong><br>Cause-Finder / IgniteCyber Academy</p>'
    elif kind == "bio":
        content += '<div class="bio-grid">' + image("assets/carlo-defcon-portrait.png", "Carlo DEFCON portrait", "portrait")
        content += f'<div><h2>{esc(s["name"])}</h2><p class="role">{esc(s["lead"])}</p><ul class="bio-list">' + "".join(f'<li>{esc(v)}</li>' for v in s["items"]) + '</ul></div></div>'
        content += f'<p class="languages">{esc(s["languages"])}</p><div class="logo-row">'
        content += image("assets/tcm-security-logo.png", "TCM Security", "logo tcm")
        content += image("assets/ignitecyber-academy-logo.png", "IgniteCyber Academy", "logo ignite")
        content += '<div class="cause-plate">' + image("assets/cause-finder-logo.png", "Cause-Finder", "logo cause") + '</div></div>'
    elif kind == "connect":
        content += f'<p class="lead">{esc(s["lead"])}</p><div class="qr-grid">'
        for link in s["links"]:
            content += f'<div><h2>{esc(link["label"])}</h2><a href="{html.escape(link["url"], quote=True)}">' + image(link["image"], link["url"], "qr") + f'<p>{esc(link["display"])}</p></a></div>'
        content += '</div>'
    else:
        if s.get("lead"):
            lead_class = "quote" if kind == "quote" else "lead"
            content += f'<p class="{lead_class}">{esc(s["lead"])}</p>'
        if s.get("body"):
            content += f'<p>{esc(s["body"])}</p>'
        if s.get("items"):
            content += '<ol>' + ''.join(f'<li>{esc(v)}</li>' for v in s["items"]) + '</ol>'
        if s.get("code"):
            content += f'<pre>{html.escape(s["code"])}</pre>'
        columns, rows = s.get("columns"), s.get("rows")
        if kind == "metrics":
            columns = ["Rule", "TP", "FP", "FN", "Precision", "Recall"]
            rows = [["Infrastructure",5,0,5,"100%","50%"],["PowerShell broad",7,2,0,"77.8%","100%"],["PowerShell tuned",7,0,0,"100%","100%"],["Log-clear",2,0,0,"100%","100%"]]
        if kind == "nova_metrics":
            columns = ["Split", "Stage", "TP", "FP", "FN"]
            rows = [["Development","Raw",30,20,0],["Development","Policy",30,0,0],["Held-out","Raw",0,20,10],["Held-out","Policy",0,0,10]]
        if columns:
            content += '<table><thead><tr>' + ''.join(f'<th>{esc(c)}</th>' for c in columns) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join(f'<td>{esc(v)}</td>' for v in row) + '</tr>' for row in rows) + '</tbody></table>'
        if kind == "metrics":
            content += '<p class="caveat">Authored fixture results. No production efficacy claim.</p>'
        if kind == "nova_metrics":
            content += '<p class="caveat">Quotation policy is separate from raw Nova matches. Held-out attack recall: 0%.</p>'
    content += f'<aside>{esc(s["notes"])}</aside><footer>{i:02d} / {len(spec)}</footer>'
    sections.append(f'<section class="{kind}">{content}</section>')
    notes += [f'\n## Slide {i}: {s["title"].replace(chr(10), " ")}\n\n{s["notes"]}\n', '\nReferences:\n' + '\n'.join(f'- {x}' for x in s["sources"]) if s["sources"] else '']

page = """<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>From Threat Intelligence to Detection – HI Cyber Con</title><style>
*{box-sizing:border-box}body{margin:0;background:#f7f4ed;color:#171a1b;font-family:Arial,sans-serif}section{display:none;min-height:100vh;padding:4vh 5.6vw 8vh;position:relative}section.active{display:block}.event{font-size:clamp(13px,1.2vw,18px);font-weight:700;color:#ac551d;letter-spacing:.07em;margin-bottom:2vh}h1{font-size:clamp(32px,3.6vw,54px);line-height:1.15;margin:0 0 2vh;padding-bottom:2vh;border-bottom:1px solid #d8d0c3}h2,.lead{color:#ac551d}h2{font-size:clamp(24px,2.4vw,36px);line-height:1.3}p,li{font-size:clamp(20px,2.2vw,32px);line-height:1.5}li{margin:2.2vh 0;padding-left:1vw}li::marker{color:#ac551d;font-weight:700}.lead{margin:2vh 0 3vh}pre{font-size:clamp(18px,2.1vw,30px);line-height:1.55;white-space:pre-wrap;background:#1c211f;color:#f6f1e8;padding:3vh 2vw;margin-top:3vh}table{border-collapse:collapse;width:100%;font-size:clamp(16px,1.9vw,28px);margin-top:3vh}td,th{border:1px solid #d8d0c3;text-align:left;padding:2vh 1vw}th{color:#ac551d;background:#eae1d3}tbody tr:nth-child(even){background:#f0eae0}.quote .quote{font-size:clamp(28px,3.3vw,47px);color:#ac551d;font-weight:700;margin-top:7vh}.caveat{font-size:18px;color:#626762}footer{position:absolute;bottom:2.5vh;right:4vw;color:#626762;font-size:16px}aside{display:none;font-size:18px;line-height:1.5;background:#eae1d3;padding:20px;margin:20px 0}body.notes aside{display:block}.help{position:fixed;bottom:10px;left:12px;color:#626762;font-size:12px}.cover{overflow:hidden;isolation:isolate}.cover-art{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:-1}.cover h1{border:0;font-size:clamp(45px,5.3vw,80px);width:53%;margin-top:9vh;line-height:1.12}.cover h2{width:47%;font-size:clamp(25px,2.5vw,39px);margin-top:3vh}.cover .presenter{font-size:clamp(18px,1.9vw,28px);line-height:1.6;margin-top:7vh}.cover footer{display:none}.bio-grid{display:grid;grid-template-columns:35% 61%;gap:4%;margin-top:3vh;align-items:start}.portrait{width:100%;height:46vh;object-fit:cover;object-position:50% 36%}.bio-grid h2{color:#171a1b;margin:0;font-size:clamp(25px,2.8vw,40px)}.role{font-size:clamp(18px,1.9vw,27px);margin:1vh 0;color:#ac551d}.bio-list{padding-left:1.7vw;margin-top:2vh}.bio-list li{font-size:clamp(18px,1.9vw,27px);line-height:1.35;margin:1.3vh 0;padding:0}.languages{font-size:20px;color:#626762;margin:1vh 0 2vh}.logo-row{height:11vh;background:#1c211f;display:flex;align-items:center;justify-content:space-around;gap:5%;padding:.8vh 3vw}.logo{object-fit:contain;max-height:9vh}.tcm{width:14%}.ignite{width:23%}.cause-plate{width:24%;height:100%;background:#f7f4ed;text-align:center}.cause{height:100%;width:75%}.qr-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:2vw;margin-top:5vh}.qr-grid h2{color:#171a1b;font-size:clamp(20px,1.8vw,26px)}.qr{width:min(18vw,230px);max-width:100%;height:auto}.qr-grid a{color:#ac551d;text-decoration:none}.qr-grid p{font-size:clamp(16px,1.45vw,21px);line-height:1.4}@media print{section{display:block;page-break-after:always;height:100vh}.help{display:none}aside{display:none!important}}
</style><body>""" + ''.join(sections) + """<div class="help">Arrow keys: navigate · N: notes · F: fullscreen</div><script>
const slides=[...document.querySelectorAll('section')];let current=0;function show(n){current=Math.max(0,Math.min(slides.length-1,n));slides.forEach((s,i)=>s.classList.toggle('active',i===current));location.hash=current+1}show(Number(location.hash.slice(1))-1||0);document.addEventListener('keydown',e=>{if(['ArrowRight','PageDown',' '].includes(e.key)){e.preventDefault();show(current+1)}if(['ArrowLeft','PageUp'].includes(e.key))show(current-1);if(e.key.toLowerCase()==='n')document.body.classList.toggle('notes');if(e.key.toLowerCase()==='f')document.documentElement.requestFullscreen?.()});
</script></body></html>"""
(root / "slides/Threat_Intelligence_to_Detection.html").write_text(page)
(root / "docs").mkdir(exist_ok=True)
(root / "docs/PRESENTER_GUIDE.md").write_text('\n'.join(notes))
print(f'Built {len(spec)}-slide self-contained HTML deck and presenter guide')
