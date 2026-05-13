#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import json, html, textwrap

ROOT = Path('/home/hermes/respiratory-muscle-mnemonic-site')
PANEL_DIR = ROOT/'assets/gpt-image-2-story-panels'
POSTER = ROOT/'assets/atemmuskulatur_storyline_poster.jpg'

items = [
  dict(id=1, title='Zwerchfell-Kuppelkröte', muscle='Diaphragma', inn='N. phrenicus C3–5', zone='Akt I: Die Einatmung beginnt', scene='Zentrale Kuppelbühne: die Kröte zieht den Bühnenboden nach unten und saugt die goldene Atemperle ein.', green='Kuppel/Fallschirm + grüne Zugseile = Zwerchfell senkt sich.', magenta='Halskrone Mama–Reh–Löwe = C3–C5 / Phrenicus.'),
  dict(id=2, title='Zwischenrippen-Leiterakrobaten', muscle='Mm. intercostales', inn='Nn. intercostales Th1–11', zone='Akt I: Rippen öffnen', scene='Rippen-Leiter-Gang: Akrobaten spreizen die Zwischenräume wie eine Ziehharmonika.', green='Akrobaten wirklich zwischen den Rippen = Intercostales.', magenta='Thor-Geländer mit Krawatten-Parade = Th1–Th11.'),
  dict(id=3, title='Sterno-Kleido-Mastoid-Kapitän', muscle='M. sternocleidomastoideus', inn='N. accessorius XI + C2–3', zone='Akt II: Halshelfer ziehen', scene='Hals-Balkon als Hafenmast: drei grüne Seile laufen zu Sternum, Clavicula und Mastoid.', green='Drei Seile zum Namen + Brustkorb-Zug bei Atemnot.', magenta='XI-Accessoire plus Knie/Noah–Mama = C2–C3.'),
  dict(id=4, title='Skalenen-Treppengnome', muscle='Mm. scaleni', inn='C3–8 variabel', zone='Akt II: Halshelfer ziehen', scene='Schiefe Treppenwerkstatt: drei Gnome heben die ersten Rippenstufen.', green='Skalenen = Treppe; sie heben 1./2. Rippe.', magenta='Mama–Reh–Löwe–Schuh–Schlüssel–Efeu = C3–C8.'),
  dict(id=5, title='Großer Pectoralis-Strongman', muscle='M. pectoralis major', inn='Nn. pectorales C5–T1', zone='Akt III: Kutschersitz', scene='Vorderbühne: Strongman im Kutschersitz zieht Vorhangseile und hebt die Rippenkulisse.', green='Große Brustplatte + fixierte Arme = Atemhilfsmuskel.', magenta='Löwe C5 + Thor-Krawatte T1.'),
  dict(id=6, title='Kleiner Pectoralis-Page', muscle='M. pectoralis minor', inn='N. pectoralis medialis C8–T1', zone='Akt III: Kutschersitz', scene='Kleiner Page unter dem Balkon zieht am Coracoid-Haken und klappt obere Rippen auf.', green='Kleiner Brust-Helfer + Coracoid-Haken.', magenta='Efeu C8 + Thor-Krawatte T1.'),
  dict(id=7, title='Oberer Sägezahn-Engel', muscle='M. serratus posterior superior', inn='Nn. intercostales Th2–5', zone='Akt IV: Hintere Logen', scene='Helle obere Loge: Sägezahn-Engel hebt obere Rippen wie Fensterläden.', green='Oberer gezackter Flügel hebt obere Rippen.', magenta='Thor + Knie/Noah–Mama–Reh–Löwe = Th2–Th5.'),
  dict(id=8, title='Unterer Sägezahn-Kobold', muscle='M. serratus posterior inferior', inn='Nn. intercostales Th9–12', zone='Akt IV: Hintere Logen', scene='Dunkle untere Kellerloge: Sägezahn-Kobold zieht untere Rippen an Ketten hinab.', green='Unterer gezackter Kobold zieht untere Rippen nach unten.', magenta='Thor + Biene–Säge/Krawatte–zwei Krawatten–Krawatte/Noah = Th9–Th12.'),
  dict(id=9, title='Vorderer Sägehai-Boxer', muscle='M. serratus anterior', inn='N. thoracicus longus C5–7', zone='Akt V: Seitliche Wand', scene='Seitliche Boxarena: Sägehai-Boxer presst die Scapula-Tür flach an die Rippenwand.', green='Vorderer Sägezahn fixiert Scapula an den Rippen.', magenta='Langes Thorax-Seil mit Löwe–Schuh–Schlüssel = C5–C7.'),
  dict(id=10, title='Gerader Bauchritter', muscle='M. rectus abdominis', inn='Th7–12', zone='Akt VI: Bauch-Maschinenraum', scene='Dampfmaschinenraum: Ritter mit geradem Sixpack-Schild presst den Bauch-Kessel gerade zusammen.', green='Gerades vertikales Schild = Rectus; Bauchpresse.', magenta='Thor: Schlüssel–Efeu–Biene–Säge/Krawatte–2 Krawatten–Krawatte/Noah = Th7–Th12.'),
  dict(id=11, title='Querer Korsettmeister', muscle='M. transversus abdominis', inn='Th7–12 + L1', zone='Akt VI: Bauch-Maschinenraum', scene='Schneider-Mechaniker schnürt ein horizontales Korsett quer um den Bauch-Kessel.', green='Quer verlaufendes Korsett = Transversus; Luft wird herausgedrückt.', magenta='Thor Th7–Th12 + Lenden-Krawatte L1.'),
  dict(id=12, title='Äußerer Schrägschärpen-Krieger', muscle='M. obliquus externus abdominis', inn='Th5–12', zone='Akt VI: Bauch-Maschinenraum', scene='Außenfassade: Krieger zieht die äußere diagonale Schärpe wie eine Rutsche abwärts.', green='Äußere absteigende Diagonale = Obliquus externus.', magenta='Thor + Löwe bis Krawatte/Noah = Th5–Th12.'),
  dict(id=13, title='Innerer Gegenschärpen-Krieger', muscle='M. obliquus internus abdominis', inn='Th7–12 + L1', zone='Akt VI: Bauch-Maschinenraum', scene='Innenfassade: Gegenkrieger zieht die entgegengesetzte innere Diagonale; zusammen entsteht ein X.', green='Innere Gegendiagonale = Obliquus internus.', magenta='Thor Th7–Th12 + Lenden-Krawatte L1.'),
  dict(id=14, title='Quadratischer Lenden-Holzfäller', muscle='M. quadratus lumborum', inn='Th12–L4', zone='Akt VII: Fundament', scene='Quadratische Holzwerkstatt: würfelförmiger Holzfäller stabilisiert Becken–12.-Rippe mit grünem Rahmen.', green='Quadratischer Rahmen an der Lende = Quadratus lumborum.', magenta='Th12 + L1–L4: Krawatte/Noah + Krawatte–Knie–Mama–Reh.'),
  dict(id=15, title='Breiter Rücken-Schwimmer', muscle='M. latissimus dorsi', inn='N. thoracodorsalis C6–8', zone='Finale: Wasserbühne', scene='Hintere Wasserbühne: breiter Schwimmer zieht Arm-Seile und presst die Atemperle als Fontäne heraus.', green='Breite Rückenflossen + Zug = Latissimus bei forcierter Exspiration.', magenta='Thoracodorsal-Seil mit Schuh–Schlüssel–Efeu = C6–C8.'),
]

font_paths=['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf']
bold_paths=['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf','/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf']
def font(size,bold=False):
    for p in (bold_paths if bold else font_paths):
        if Path(p).exists(): return ImageFont.truetype(p,size)
    return ImageFont.load_default()
F_TITLE=font(62,True); F_SUB=font(28); F_CAP=font(23,True); F_SMALL=font(18); F_NUM=font(30,True)

def wrap(draw, xy, text, fnt, fill, width, gap=3):
    x,y=xy; line=''
    for word in text.split():
        t=(line+' '+word).strip()
        if draw.textlength(t,font=fnt)<=width or not line: line=t
        else:
            draw.text((x,y),line,font=fnt,fill=fill); y += fnt.size+gap; line=word
    if line:
        draw.text((x,y),line,font=fnt,fill=fill); y += fnt.size+gap
    return y

# 5x3 story-strip poster; stronger route readability than tall atlas
cols, rows = 5, 3
cell_w, cell_h = 610, 500
gutter=30; margin=58; header=230; footer=210
W=margin*2 + cols*cell_w + (cols-1)*gutter
H=header + rows*cell_h + (rows-1)*gutter + footer
poster=Image.new('RGB',(W,H),(35,23,16)); d=ImageDraw.Draw(poster)
d.rectangle([18,18,W-18,H-18], outline=(169,70,48), width=8)
d.rectangle([36,36,W-36,H-36], outline=(236,181,84), width=4)
d.text((margin,42),'Atemmuskulatur: Die Reise der goldenen Atemperle',font=F_TITLE,fill=(255,238,204))
d.text((margin,124),'Ein zusammenhängendes Rippen-Opernhaus: jeder Raum ist anders, aber die goldene Perle führt dich in Reihenfolge 1–15 durch die Muskel-Liste.',font=F_SUB,fill=(248,215,157))
d.rounded_rectangle([margin,170,W-margin,214], radius=14, fill=(255,246,220), outline=(234,180,82), width=3)
d.text((margin+20,180),'grün = Muskel/Name/Aktion · magenta = Innervation/Wurzelcode · rote Nummern = Reihenfolge · goldene Pfeile = Storypfad',font=F_SMALL,fill=(72,45,28))
positions=[]
for idx,it in enumerate(items):
    r=idx//cols; c=idx%cols
    x=margin+c*(cell_w+gutter); y=header+r*(cell_h+gutter)
    positions.append((x,y))
    d.rounded_rectangle([x,y,x+cell_w,y+cell_h], radius=24, fill=(255,247,229), outline=(218,167,94), width=4)
    img=Image.open(PANEL_DIR/f'panel_{it["id"]:02d}.png').convert('RGB')
    img=ImageOps.fit(img,(cell_w-24,340),Image.Resampling.LANCZOS,centering=(0.5,0.46))
    poster.paste(img,(x+12,y+12))
    d.ellipse([x+24,y+22,x+82,y+80], fill=(220,34,50), outline=(255,244,220), width=4)
    num=str(it['id']); bb=d.textbbox((0,0),num,font=F_NUM)
    d.text((x+53-(bb[2]-bb[0])/2,y+51-(bb[3]-bb[1])/2),num,font=F_NUM,fill='white')
    ty=y+365
    d.text((x+18,ty),f"{it['id']}. {it['title']}",font=F_CAP,fill=(50,32,23)); ty+=29
    d.text((x+18,ty),it['muscle'],font=F_SMALL,fill=(40,40,38)); ty+=23
    d.text((x+18,ty),it['inn'],font=F_SMALL,fill=(172,22,150)); ty+=24
    d.ellipse([x+18,ty+3,x+32,ty+17], fill=(18,151,77)); wrap(d,(x+40,ty),it['green'],F_SMALL,(20,112,54),cell_w-60,1)
# Draw golden story arrows between cells
for i in range(14):
    x1,y1=positions[i]; x2,y2=positions[i+1]
    start=(x1+cell_w-8,y1+170); end=(x2+8,y2+170)
    if (i+1)%cols==0: # wrap down to next row
        start=(x1+cell_w/2,y1+cell_h-5); end=(x2+cell_w/2,y2+5)
    d.line([start,end], fill=(246,196,71), width=8)
    # arrowhead
    ex,ey=end; sx,sy=start
    if abs(ex-sx)>abs(ey-sy):
        sign=1 if ex>sx else -1
        pts=[(ex,ey),(ex-24*sign,ey-14),(ex-24*sign,ey+14)]
    else:
        sign=1 if ey>sy else -1
        pts=[(ex,ey),(ex-14,ey-24*sign),(ex+14,ey-24*sign)]
    d.polygon(pts, fill=(246,196,71))
fy=H-footer+28
d.text((margin,fy),'Story in einem Satz:',font=font(30,True),fill=(255,238,204)); fy+=42
wrap(d,(margin,fy),'Die goldene Atemperle wird zuerst durch Zwerchfell und Rippenhelfer eingesogen, dann von Hals-/Brusthelfern unterstützt, durch Sägezahn-Logen und Bauchmaschine gepresst, am Lendenfundament stabilisiert und vom breiten Rücken-Schwimmer im Finale herausgedrückt.',font(24), (255,230,190), W-2*margin, 5)
POSTER.parent.mkdir(parents=True,exist_ok=True)
poster.save(POSTER,quality=92,optimize=True)
print(POSTER)

manifest=[]
for it in items:
    row=it.copy(); row['image']=f'assets/gpt-image-2-story-panels/panel_{it["id"]:02d}.png'; manifest.append(row)
(PANEL_DIR/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))

def esc(s): return html.escape(str(s))
rows_html='\n'.join([f'''<tr data-id="{i['id']}"><td>{i['id']}</td><td><strong>{esc(i['title'])}</strong><br><em>{esc(i['muscle'])}</em><br><span>{esc(i['zone'])}</span></td><td>{esc(i['scene'])}</td><td>{esc(i['inn'])}</td><td class="green">{esc(i['green'])}</td><td class="magenta">{esc(i['magenta'])}</td></tr>''' for i in items])
cards='\n'.join([f'''<article class="card" data-id="{i['id']}"><img src="assets/gpt-image-2-story-panels/panel_{i['id']:02d}.png" alt="{i['id']}. {esc(i['title'])}"><div><b>{i['id']}. {esc(i['title'])}</b><br><span>{esc(i['scene'])}</span></div></article>''' for i in items])
buttons='\n'.join([f'<button data-id="{i["id"]}">{i["id"]}</button>' for i in items])
js_items=json.dumps(manifest,ensure_ascii=False)
html_doc=f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Atemmuskulatur Story-Palast</title><link rel="stylesheet" href="style.css"></head><body><header><p class="eyebrow">GPT-image-2-high · komplett deutsche Story-Version</p><h1>Atemmuskulatur: Die Reise der goldenen Atemperle</h1><p>Neu gebaut als echte Lern-Story statt Figurensammlung: 15 verschiedene Räume im Rippen-Opernhaus, verbunden durch eine goldene Atemperle. Die Tabelle bleibt die exakte Faktenebene.</p><div class="key"><span class="gdot"></span> grün = Muskel/Name/Aktion <span class="mdot"></span> magenta = Innervation/Wurzelcode <span class="rdot"></span> rot = aktuell <span class="ydot"></span> gold = Storypfad</div></header><main><section class="poster"><h2>Riesenposter: ein folgbarer Storypfad</h2><p>Folge den roten Nummern und goldenen Pfeilen: Einatmung startet oben links, forcierte Ausatmung endet im Wasser-Finale unten rechts.</p><a href="assets/atemmuskulatur_storyline_poster.jpg" target="_blank"><img src="assets/atemmuskulatur_storyline_poster.jpg" alt="Atemmuskulatur Storyline Poster"></a></section><section class="focus"><div><p class="zone" id="focusZone">Akt I: Die Einatmung beginnt</p><h2 id="focusTitle">1. Zwerchfell-Kuppelkröte</h2><p id="focusMuscle">Diaphragma — N. phrenicus C3–5</p><p id="focusScene">Zentrale Kuppelbühne: die Kröte zieht den Bühnenboden nach unten und saugt die goldene Atemperle ein.</p><p id="focusGreen" class="green">Kuppel/Fallschirm + grüne Zugseile = Zwerchfell senkt sich.</p><p id="focusMagenta" class="magenta">Halskrone Mama–Reh–Löwe = C3–C5 / Phrenicus.</p><div class="buttons">{buttons}</div></div><img id="focusImg" src="assets/gpt-image-2-story-panels/panel_01.png" alt="Aktives Story-Panel"></section><section class="walk"><h2>Story-Reihenfolge</h2><ol>{''.join([f'<li data-id="{i['id']}"><b>{i['id']}. {esc(i['title'])}</b> — {esc(i['scene'])}</li>' for i in items])}</ol></section><section><h2>Einzelbilder</h2><div class="grid">{cards}</div></section><section><h2>Legende / Wahrheitsebene</h2><table id="legend"><thead><tr><th>#</th><th>Figur / Muskel</th><th>Storyraum</th><th>Innervation</th><th>grüner Haken</th><th>magenta Haken</th></tr></thead><tbody>{rows_html}</tbody></table></section><section class="note"><h2>Wie lernen?</h2><p><b>1.</b> Nur den Film ablaufen lassen: Kuppelkröte → Leiterakrobaten → Kapitän → Treppengnome → Strongman/Page → Engel/Kobold/Sägehai → Bauchmaschine → Holzfäller → Schwimmer. <b>2.</b> Dann pro Bild grün = Muskelaktion abrufen. <b>3.</b> Danach magenta = Innervation abrufen.</p><p>KI-Mikrotext in Bildern ignorieren; die korrekten Namen und Innervationen stehen hier in der HTML-Legende.</p></section></main><script>const ITEMS={js_items};function setActive(id){{id=Number(id);const it=ITEMS.find(x=>x.id===id);if(!it)return;document.querySelectorAll('[data-id]').forEach(e=>e.classList.toggle('active',Number(e.dataset.id)===id));document.querySelectorAll('.buttons button').forEach(b=>b.classList.toggle('active',Number(b.dataset.id)===id));focusTitle.textContent=it.id+'. '+it.title;focusZone.textContent=it.zone;focusMuscle.textContent=it.muscle+' — '+it.inn;focusScene.textContent=it.scene;focusGreen.textContent=it.green;focusMagenta.textContent=it.magenta;focusImg.src=it.image;focusImg.alt=it.id+'. '+it.title;}}document.querySelectorAll('[data-id]').forEach(e=>{{e.tabIndex=0;e.addEventListener('click',()=>setActive(e.dataset.id));e.addEventListener('mouseenter',()=>setActive(e.dataset.id));e.addEventListener('keydown',ev=>{{if(ev.key==='Enter'||ev.key===' ')setActive(e.dataset.id);}})}});setActive(1);</script></body></html>'''
(ROOT/'index.html').write_text(html_doc)
css='''body{margin:0;font-family:Inter,system-ui,-apple-system,Segoe UI,sans-serif;background:#1d140f;color:#2e2118}header,main{max-width:1500px;margin:auto}header{padding:38px 22px;color:#fff2dc}h1{font-size:clamp(36px,6vw,78px);margin:.1em 0}.eyebrow{color:#f5c15e;text-transform:uppercase;letter-spacing:.16em}.key{display:flex;gap:14px;flex-wrap:wrap;align-items:center}.gdot,.mdot,.rdot,.ydot{display:inline-block;width:18px;height:18px;border-radius:50%}.gdot{background:#16a34a}.mdot{background:#d629b8}.rdot{background:#e11d48}.ydot{background:#f2c94c}.poster,.focus,section{background:#fff7e8;border:1px solid #d7b98c;border-radius:26px;padding:22px;margin:20px 18px;box-shadow:0 20px 70px #0007}.poster img{width:100%;border-radius:16px;border:4px solid #7b432c}.focus{display:grid;grid-template-columns:minmax(290px,470px) 1fr;gap:22px;align-items:start}.focus img{width:100%;border-radius:18px;border:5px solid #8a4a2d}.zone{display:inline-block;background:#3b2a20;color:#ffd88b;border-radius:999px;padding:8px 12px;font-weight:800}.green{color:#087336;font-weight:800}.magenta{color:#b01892;font-weight:800}.buttons{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}.buttons button{border:0;border-radius:999px;background:#3a2b20;color:white;padding:10px 14px;font-weight:900;cursor:pointer}.buttons button.active,button:hover{background:#e11d48}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(275px,1fr));gap:16px}.card{border:3px solid #e4cda8;background:#fffdf7;border-radius:18px;padding:10px;cursor:pointer}.card.active{border-color:#e11d48;box-shadow:0 0 0 5px #e11d4833}.card img{width:100%;border-radius:12px;display:block}.card b{color:#321f15}.walk ol{columns:2;column-gap:34px}.walk li{break-inside:avoid;margin:0 0 12px;padding:10px;border-left:5px solid #f0c15a;background:#fffdf7;border-radius:10px;cursor:pointer}.walk li.active{border-color:#e11d48;background:#fff0ed}table{width:100%;border-collapse:collapse;background:white;border-radius:16px;overflow:hidden}th,td{padding:12px;border-bottom:1px solid #ead9bc;text-align:left;vertical-align:top}th{background:#3a2b20;color:#fff2dc}tr{cursor:pointer}tr.active td{background:#fff0ed;outline:2px solid #e11d48}.note{background:#fff1d6}@media(max-width:900px){.focus{grid-template-columns:1fr}.walk ol{columns:1}th:nth-child(5),td:nth-child(5),th:nth-child(6),td:nth-child(6){display:none}}'''
(ROOT/'style.css').write_text(css)
(ROOT/'README.md').write_text('# Atemmuskulatur Story-Palast\n\nDeutsche GPT-image-2-high Story-Version: 15 stärker variierte Einzelbilder, verbunden durch die Reise der goldenen Atemperle im Rippen-Opernhaus.\n')
print('wrote storyline site with', len(items), 'items')
