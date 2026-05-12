#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import json, textwrap, html

ROOT=Path('/home/hermes/respiratory-muscle-mnemonic-site')
PANEL_DIR=ROOT/'assets/gpt-image-2-high-panels'
POSTER=ROOT/'assets/atemmuskulatur_gpt_image_2_high_poster.jpg'

items=[
(1,'Zwerchfell-Kuppelkröte','Diaphragma','N. phrenicus C3–5','Kuppel/Fallschirm zieht Bühnenboden nach unten','Halskrone: Mama–Reh–Löwe = C3–C5','Zentrale Bühne'),
(2,'Zwischenrippen-Leiterakrobaten','Mm. intercostales','Nn. intercostales Th1–11','Akrobaten zwischen Rippen-Leiter öffnen Zwischenräume','Thor + Krawatten-Parade = Th1–Th11','Rippenrang'),
(3,'Hals-Seil-Kapitän','M. sternocleidomastoideus','N. accessorius XI + C2–3','Drei Seile zu Sternum, Clavicula, Mastoid-Mast','Accessoire-XI + Knie/Noah–Mama = C2–C3','Hals-Balkon'),
(4,'Skalenen-Treppengnome','Mm. scaleni','C3–8 variabel','Drei Gnome heben erste/zweite Rippenstufen','Mama–Reh–Löwe–Schuh–Schlüssel–Efeu = C3–C8','Hals-Treppe'),
(5,'Großer Pectoralis-Strongman','M. pectoralis major','Nn. pectorales C5–T1','Kutschersitz-Strongman hebt Rippenvorhänge','Löwe C5 + Thor-Krawatte T1','Kutschersitz-Bühne'),
(6,'Kleiner Pectoralis-Page','M. pectoralis minor','N. pectoralis medialis C8–T1','Kleiner Page zieht Korakoid-Haken / obere Rippen','Efeu C8 + Thor-Krawatte T1','Kutschersitz-Bühne'),
(7,'Oberer Sägezahn-Engel','M. serratus posterior superior','Nn. intercostales Th2–5','Gezackte Flügel heben obere Rippen','Thor + Knie/Noah–Mama–Reh–Löwe = Th2–Th5','Hintere obere Loge'),
(8,'Unterer Sägezahn-Kobold','M. serratus posterior inferior','Nn. intercostales Th9–12','Gezackter Kobold zieht untere Rippen hinab','Thor + Biene–Säge/Krawatte–zwei Krawatten–Krawatte/Noah = Th9–Th12','Hintere untere Loge'),
(9,'Vorderer Sägehai-Boxer','M. serratus anterior','N. thoracicus longus C5–7','Sägehai drückt Scapula flach an Rippen','Langer Thor-Seilnerv: Löwe–Schuh–Schlüssel = C5–C7','Seitliche Wand'),
(10,'Gerader Bauchritter','M. rectus abdominis','Th7–12','Vertikales Schild presst Bauch-Kessel aus','Thor: Schlüssel–Efeu–Biene–Säge/Krawatte–2 Krawatten–Krawatte/Noah','Bauch-Maschinenraum'),
(11,'Querer Korsettmeister','M. transversus abdominis','Th7–12 + L1','Horizontales Korsett zieht Bauch quer zusammen','Thor Th7–12 + Lenden-Holzscheit-Krawatte L1','Bauch-Maschinenraum'),
(12,'Äußerer Schrägschärpen-Krieger','M. obliquus externus abdominis','Th5–12','Äußere Diagonalschärpe presst Bauch schräg','Thor: Löwe bis Krawatte/Noah = Th5–Th12','Bauch-Maschinenraum'),
(13,'Innerer Gegenschärpen-Krieger','M. obliquus internus abdominis','Th7–12 + L1','Innere Gegendiagonale presst Bauch von innen','Thor Th7–12 + Lenden-Holzscheit-Krawatte L1','Bauch-Maschinenraum'),
(14,'Quadratischer Lenden-Holzfäller','M. quadratus lumborum','Th12–L4','Quadratischer Rahmen stabilisiert/zieht 12. Rippe','Thor Th12 + Lenden-Holzscheite Krawatte–Knie–Mama–Reh = L1–L4','Lenden-Fundament'),
(15,'Breiter Rücken-Schwimmer','M. latissimus dorsi','N. thoracodorsalis C6–8','Breiter Schwimmer/Kletterer zieht Seile bei forcierter Exspiration','Thorakodorsal-Seil: Schuh–Schlüssel–Efeu = C6–C8','Hintere Wasserbühne'),
]

# Fonts
font_paths=['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf']
bold_paths=['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf','/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf']
def font(size,bold=False):
    for p in (bold_paths if bold else font_paths):
        if Path(p).exists(): return ImageFont.truetype(p,size)
    return ImageFont.load_default()
F_TITLE=font(70,True); F_SUB=font(34); F_ZONE=font(32,True); F_LABEL=font(30,True); F_SMALL=font(23)

# Poster layout 3 x 5
cols, rows = 3, 5
cell_w, cell_h = 760, 650
margin=70; header=260; footer=260; gutter=36
W=margin*2 + cols*cell_w + (cols-1)*gutter
H=header + rows*cell_h + (rows-1)*gutter + footer
poster=Image.new('RGB',(W,H),(244,235,215))
d=ImageDraw.Draw(poster)
# background theater curtains/frame
d.rectangle([0,0,W,H], fill=(242,232,210))
d.rectangle([20,20,W-20,H-20], outline=(100,55,40), width=8)
d.rectangle([38,38,W-38,H-38], outline=(168,42,55), width=5)
# Header
d.text((margin,50),'Atemmuskulatur: Das Rippen-Opernhaus',font=F_TITLE,fill=(65,35,28))
d.text((margin,140),'GPT-image-2-high · deutsche Sketchy/Meditricks-artige Gedächtnisszene · grün = Muskel/Aktion · magenta = Innervation',font=F_SUB,fill=(72,62,55))
d.rounded_rectangle([margin,185,W-margin,235], radius=18, fill=(255,250,235), outline=(160,120,90), width=3)
d.text((margin+26,195),'Route: Bühne → Hals-Balkon → Kutschersitz → Rippenrang/Logen → Bauch-Maschinenraum → Lendenfundament/Wasserbühne',font=F_SMALL,fill=(70,50,42))

def draw_wrapped(draw, xy, text, fnt, fill, width_px, line_gap=4):
    x,y=xy
    words=text.split(); line=''
    for w in words:
        test=(line+' '+w).strip()
        if draw.textlength(test,font=fnt) <= width_px or not line:
            line=test
        else:
            draw.text((x,y),line,font=fnt,fill=fill); y+=fnt.size+line_gap; line=w
    if line:
        draw.text((x,y),line,font=fnt,fill=fill); y+=fnt.size+line_gap
    return y

for idx,it in enumerate(items):
    id,title,muscle,inn,green,magenta,zone=it
    r=idx//cols; c=idx%cols
    x=margin+c*(cell_w+gutter); y=header+r*(cell_h+gutter)
    # panel frame
    d.rounded_rectangle([x,y,x+cell_w,y+cell_h], radius=28, fill=(255,250,238), outline=(108,68,50), width=5)
    img=Image.open(PANEL_DIR/f'panel_{id:02d}.png').convert('RGB')
    img=ImageOps.fit(img,(cell_w-36,430),method=Image.Resampling.LANCZOS,centering=(0.5,0.45))
    poster.paste(img,(x+18,y+18))
    # number badge
    d.ellipse([x+30,y+30,x+104,y+104], fill=(220,40,44), outline=(255,250,230), width=5)
    num=str(id)
    bbox=d.textbbox((0,0),num,font=F_LABEL)
    d.text((x+67-(bbox[2]-bbox[0])/2,y+66-(bbox[3]-bbox[1])/2),num,font=F_LABEL,fill='white')
    # caption strip
    ty=y+462
    d.text((x+24,ty),f'{id}. {title}',font=F_LABEL,fill=(54,35,28)); ty+=39
    d.text((x+24,ty),muscle,font=F_SMALL,fill=(40,40,40)); ty+=29
    d.text((x+24,ty),inn,font=F_SMALL,fill=(165,20,145)); ty+=31
    # green/magenta short hooks
    d.ellipse([x+24,ty+3,x+40,ty+19], fill=(20,150,72));
    ty=draw_wrapped(d,(x+50,ty),green,F_SMALL,(25,110,50),cell_w-78,2)
    d.ellipse([x+24,ty+3,x+40,ty+19], fill=(210,32,180));
    draw_wrapped(d,(x+50,ty),magenta,F_SMALL,(145,25,125),cell_w-78,2)

# Footer major system key
fy=H-footer+35
d.text((margin,fy),'Deutscher Zahlen-/Wurzel-Code:',font=F_ZONE,fill=(65,35,28)); fy+=46
key='C = Halskrone/-kragen · Th = Thor/Brustpanzer · L = Lenden-Holzscheit · 1 Krawatte · 2 Knie/Noah · 3 Mama · 4 Reh · 5 Löwe · 6 Schuh · 7 Schlüssel/Kuh · 8 Efeu · 9 Biene · 10 Säge+Krawatte · 11 zwei Krawatten · 12 Krawatte+Noah'
draw_wrapped(d,(margin,fy),key,F_SUB,(78,58,48),W-2*margin,6)
POSTER.parent.mkdir(parents=True,exist_ok=True)
poster.save(POSTER,quality=92,optimize=True)
print(POSTER)

# Write manifest
manifest=[]
for it in items:
    manifest.append({'id':it[0],'title':it[1],'muscle':it[2],'innervation':it[3],'green':it[4],'magenta':it[5],'zone':it[6],'image':f'assets/gpt-image-2-high-panels/panel_{it[0]:02d}.png'})
(PANEL_DIR/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))

# HTML/CSS
rows_html='\n'.join([f'''<tr data-id="{i[0]}"><td>{i[0]}</td><td><strong>{html.escape(i[1])}</strong><br><em>{html.escape(i[2])}</em></td><td>{html.escape(i[3])}</td><td class="green">{html.escape(i[4])}</td><td class="magenta">{html.escape(i[5])}</td></tr>''' for i in items])
cards='\n'.join([f'''<article class="card" data-id="{i[0]}"><img src="assets/gpt-image-2-high-panels/panel_{i[0]:02d}.png" alt="{i[0]}. {html.escape(i[1])}"><div><b>{i[0]}. {html.escape(i[1])}</b><br><span>{html.escape(i[2])}</span></div></article>''' for i in items])
buttons='\n'.join([f'<button data-id="{i[0]}">{i[0]}</button>' for i in items])
html_doc=f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Atemmuskulatur Gedächtnispalast</title><link rel="stylesheet" href="style.css"></head><body><header><p class="eyebrow">GPT-image-2-high · deutsche Version</p><h1>Atemmuskulatur: Das Rippen-Opernhaus</h1><p>Ein Sketchy/Meditricks-artiger Gedächtnispalast für inspiratorische und exspiratorische Atemmuskeln. Die Kunst dient als Haken; die Tabelle ist die exakte Faktenebene.</p><div class="key"><span class="gdot"></span> grün = Muskel/Name/Aktion <span class="mdot"></span> magenta = Innervation/Wurzelcode <span class="rdot"></span> rot = aktuell ausgewählt</div></header><main><section class="poster"><h2>Riesenposter / Gesamtbild</h2><p>Alle 15 Einzel-Szenen sind zu einem zusammenhängenden Opernhaus-Poster collagiert.</p><a href="assets/atemmuskulatur_gpt_image_2_high_poster.jpg" target="_blank"><img src="assets/atemmuskulatur_gpt_image_2_high_poster.jpg" alt="Atemmuskulatur Riesenposter: Das Rippen-Opernhaus"></a></section><section class="focus"><div><h2 id="focusTitle">1. Zwerchfell-Kuppelkröte</h2><p id="focusMuscle">Diaphragma — N. phrenicus C3–5</p><p id="focusGreen" class="green">Kuppel/Fallschirm zieht Bühnenboden nach unten</p><p id="focusMagenta" class="magenta">Halskrone: Mama–Reh–Löwe = C3–C5</p><div class="buttons">{buttons}</div></div><img id="focusImg" src="assets/gpt-image-2-high-panels/panel_01.png" alt="Aktives Panel"></section><section><h2>Einzelpanels</h2><div class="grid">{cards}</div></section><section><h2>Legende / Wahrheitsebene</h2><table id="legend"><thead><tr><th>#</th><th>Figur / Muskel</th><th>Innervation</th><th>grüner Haken</th><th>magenta Haken</th></tr></thead><tbody>{rows_html}</tbody></table></section><section class="note"><h2>Reihenfolge lernen</h2><p><b>Route:</b> Zwerchfell-Bühne → Zwischenrippen-Leiter → Halshelfer → Kutschersitz → Sägezahn-Logen → Bauch-Maschinenraum → Lendenfundament → breiter Rücken-Schwimmer.</p><p>Ignoriere eventuell generierte Mikro-Schrift in den Bildern. Verbindlich sind die deutschen Bildhaken und die Tabelle.</p></section></main><script>const items={json.dumps(manifest,ensure_ascii=False)};function setActive(id){{id=Number(id);const it=items.find(x=>x.id===id);if(!it)return;document.querySelectorAll('[data-id]').forEach(e=>e.classList.toggle('active',Number(e.dataset.id)===id));document.getElementById('focusTitle').textContent=it.id+'. '+it.title;document.getElementById('focusMuscle').textContent=it.muscle+' — '+it.innervation;document.getElementById('focusGreen').textContent=it.green;document.getElementById('focusMagenta').textContent=it.magenta;document.getElementById('focusImg').src=it.image;}}document.querySelectorAll('[data-id]').forEach(e=>{{e.addEventListener('click',()=>setActive(e.dataset.id));e.addEventListener('mouseenter',()=>setActive(e.dataset.id));}});setActive(1);</script></body></html>'''
(ROOT/'index.html').write_text(html_doc)
css='''body{margin:0;font-family:Inter,system-ui,-apple-system,Segoe UI,sans-serif;background:#24180f;color:#2d2118}header,main{max-width:1380px;margin:auto}header{padding:38px 22px;color:#fff2dc}h1{font-size:clamp(38px,6vw,80px);margin:.1em 0}h2{margin-top:0}.eyebrow{color:#f6c05c;text-transform:uppercase;letter-spacing:.16em}.key{display:flex;gap:14px;flex-wrap:wrap;align-items:center}.gdot,.mdot,.rdot{display:inline-block;width:18px;height:18px;border-radius:50%}.gdot{background:#16a34a}.mdot{background:#d629b8}.rdot{background:#e11d48}.poster,.focus,section{background:#fff7e8;border:1px solid #d7b98c;border-radius:26px;padding:22px;margin:20px 18px;box-shadow:0 20px 70px #0006}.poster img{width:100%;border-radius:16px;border:4px solid #7b432c}.focus{display:grid;grid-template-columns:minmax(280px,430px) 1fr;gap:22px;align-items:start}.focus img{width:100%;border-radius:18px;border:5px solid #8a4a2d}.green{color:#087336;font-weight:700}.magenta{color:#b01892;font-weight:700}.buttons{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}.buttons button{border:0;border-radius:999px;background:#3a2b20;color:white;padding:10px 14px;font-weight:800;cursor:pointer}.buttons button.active,button:hover{background:#e11d48}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}.card{border:3px solid #e4cda8;background:#fffdf7;border-radius:18px;padding:10px;cursor:pointer}.card.active{border-color:#e11d48;box-shadow:0 0 0 5px #e11d4833}.card img{width:100%;border-radius:12px;display:block}.card b{color:#321f15}table{width:100%;border-collapse:collapse;background:white;border-radius:16px;overflow:hidden}th,td{padding:12px;border-bottom:1px solid #ead9bc;text-align:left;vertical-align:top}th{background:#3a2b20;color:#fff2dc}tr{cursor:pointer}tr.active td{background:#fff0ed;outline:2px solid #e11d48}.note{background:#fff1d6}@media(max-width:850px){.focus{grid-template-columns:1fr}th:nth-child(4),td:nth-child(4),th:nth-child(5),td:nth-child(5){display:none}}'''
(ROOT/'style.css').write_text(css)
(ROOT/'README.md').write_text('# Atemmuskulatur Gedächtnispalast\n\nDeutscher GPT-image-2-high Gedächtnispalast für Atemmuskulatur mit Riesenposter, Einzelpanels und interaktiver Legende.\n')
