from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, textwrap, html

ROOT=Path(__file__).resolve().parent
PANEL_DIR=ROOT/'assets/complete_hook_panels'
POSTER=ROOT/'assets/atemmuskulatur_complete_hooks_poster.jpg'

DATA=[
 dict(id='1', title='Zwerchfell-Kuppelkröte', muscle='Diaphragma', inn='N. phrenicus C3–5', level='C = Halskrone', range='3–5 = Mama → Löwe', nerve='Phrenicus-Fährmann/Phönix', action='Kuppel senkt sich: Inspiration'),
 dict(id='2', title='Zwischenrippen-Leiterakrobaten', muscle='Mm. intercostales', inn='Nn. intercostales Th1–11', level='Th = Thorhammer', range='1–11 = Krawatte → Doppel-Krawatte', nerve='Interkostal-Schienen', action='zwischen den Rippen: Ziehharmonika'),
 dict(id='3', title='Sterno-Kleido-Mastoid-Kapitän', muscle='M. sternocleidomastoideus', inn='N. accessorius XI + C2–3', level='C = Halskrone + XI-Accessoire', range='2–3 = Knie/Noah → Mama', nerve='Accessoire-Bote', action='3 Seile: Sternum, Clavicula, Mastoid'),
 dict(id='4', title='Skalenen-Treppengnome', muscle='Mm. scaleni', inn='C3–8 variabel', level='C = Halskrone', range='3–8 = Mama → Efeu', nerve='Halskronen-Bote', action='Treppen heben 1./2. Rippe'),
 dict(id='5', title='Großer Pectoralis-Strongman', muscle='M. pectoralis major', inn='Nn. pectorales C5–T1', level='C + Th = Krone + Thorhammer', range='C5–T1 = Löwe → Thor-Krawatte', nerve='Pectoralis-Duo-Bote', action='großer Brustzug bei fixierten Armen'),
 dict(id='6', title='Kleiner Pectoralis-Page', muscle='M. pectoralis minor', inn='N. pectoralis medialis C8–T1', level='C + Th = Krone + Thorhammer', range='C8–T1 = Efeu → Thor-Krawatte', nerve='medialer Pectoralis-Bote', action='Coracoid-Haken zieht obere Rippen'),
 dict(id='7', title='Oberer Sägezahn-Engel', muscle='M. serratus posterior superior', inn='Nn. intercostales Th2–5', level='Th = Thorhammer', range='2–5 = Knie/Noah → Löwe', nerve='Interkostal-Bote oben', action='gezackter Engel hebt obere Rippen'),
 dict(id='8', title='Unterer Sägezahn-Kobold', muscle='M. serratus posterior inferior', inn='Nn. intercostales Th9–12', level='Th = Thorhammer', range='9–12 = Biene → Noah', nerve='Interkostal-Bote unten', action='gezackter Kobold zieht untere Rippen'),
 dict(id='9', title='Vorderer Sägehai-Boxer', muscle='M. serratus anterior', inn='N. thoracicus longus C5–7', level='C = Halskrone', range='5–7 = Löwe → Schlüssel', nerve='LANGES Thorax-Seil', action='Sägehai presst Scapula-Tür an'),
 dict(id='10', title='Gerader Bauchritter', muscle='M. rectus abdominis', inn='Th7–12', level='Th = Thorhammer', range='7–12 = Schlüssel → Noah', nerve='Thor-Bauchast', action='gerades Schild presst Bauch'),
 dict(id='11', title='Quer-Korsettmeister', muscle='M. transversus abdominis', inn='Th7–12 + L1', level='Th + L = Thorhammer + Lendenstamm', range='Th7–12 + L1 = Schlüssel→Noah + L-Krawatte', nerve='Thor/Lenden-Bote', action='queres Korsett presst Bauch'),
 dict(id='12', title='Äußerer Schrägschärpen-Krieger', muscle='M. obliquus externus abdominis', inn='Th5–12', level='Th = Thorhammer', range='5–12 = Löwe → Noah', nerve='Thor-Bauchast außen', action='äußere Diagonale abwärts'),
 dict(id='13', title='Innerer Gegenschärpen-Krieger', muscle='M. obliquus internus abdominis', inn='Th7–12 + L1', level='Th + L = Thorhammer + Lendenstamm', range='Th7–12 + L1 = Schlüssel→Noah + L-Krawatte', nerve='Thor/Lenden-Bote innen', action='innere Gegendiagonale'),
 dict(id='14', title='Quadratischer Lenden-Holzfäller', muscle='M. quadratus lumborum', inn='Th12–L4', level='Th + L = Thorhammer + Lendenstamm', range='Th12–L4 = Thor-Noah → Lenden-Reh', nerve='Grenzbote Thor/Lende', action='Quadratrahmen stabilisiert 12. Rippe'),
 dict(id='15', title='Breiter Rücken-Schwimmer', muscle='M. latissimus dorsi', inn='N. thoracodorsalis C6–8', level='C = Halskrone', range='6–8 = Schuh → Efeu', nerve='Thoracodorsal-Seil', action='breiter Rücken zieht Armseile'),
]

font_paths=['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf']
FONT=ImageFont.truetype(font_paths[0],21)
BOLD=ImageFont.truetype(font_paths[1],24)
BIG=ImageFont.truetype(font_paths[1],48)
SMALL=ImageFont.truetype(font_paths[0],17)

def wrap(draw, text, font, maxw):
    words=text.split(); lines=[]; cur=''
    for w in words:
        test=(cur+' '+w).strip()
        if draw.textbbox((0,0),test,font=font)[2] <= maxw:
            cur=test
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines

def panel(i,d):
    raw=Image.open(PANEL_DIR/f'raw_{i:02d}.png').convert('RGB').resize((560,560), Image.LANCZOS)
    W,H=680,930
    im=Image.new('RGB',(W,H),(255,246,226)); draw=ImageDraw.Draw(im)
    # frame
    draw.rounded_rectangle([8,8,W-8,H-8], radius=22, fill=(255,250,239), outline=(105,64,40), width=4)
    im.paste(raw,(60,82))
    draw.rectangle([60,82,620,642], outline=(123,67,44), width=3)
    # red number
    draw.ellipse([22,22,92,92], fill=(225,29,72), outline=(255,255,255), width=5)
    draw.text((57,57),d['id'],font=BIG,fill='white',anchor='mm')
    # title strip
    draw.rounded_rectangle([105,18,655,74], radius=16, fill=(54,35,24))
    title=f"{d['id']}. {d['title']}"
    yy=24
    for line in wrap(draw,title,BOLD,515)[:2]:
        draw.text((120,yy),line,font=BOLD,fill=(255,228,176)); yy+=24
    # bottom deterministic hooks
    y=660
    draw.rounded_rectangle([28,y,652,y+92], radius=14, fill=(231,255,238), outline=(22,163,74), width=3)
    draw.text((44,y+8),'MUSKEL',font=BOLD,fill=(7,115,54))
    yy=y+8
    for line in wrap(draw, f"{d['muscle']} – {d['action']}", FONT, 485)[:3]:
        draw.text((165,yy),line,font=FONT,fill=(24,78,45)); yy+=24
    y=762
    draw.rounded_rectangle([28,y,652,y+142], radius=14, fill=(255,238,252), outline=(214,41,184), width=3)
    draw.text((44,y+8),'NERV',font=BOLD,fill=(176,24,146))
    parts=[d['inn'], d['level'], d['range'], d['nerve']]
    yy=y+8
    for part in parts:
        for line in wrap(draw, part, SMALL, 485)[:2]:
            if yy < y+122:
                draw.text((165,yy),line,font=SMALL,fill=(115,23,95)); yy+=20
    return im

cards=[panel(i,d) for i,d in enumerate(DATA,1)]
cols,rows=3,5; gap=28; margin=42
W=cols*680+(cols-1)*gap+2*margin
H=rows*930+(rows-1)*gap+2*margin+150
poster=Image.new('RGB',(W,H),(38,25,17)); draw=ImageDraw.Draw(poster)
draw.rounded_rectangle([20,20,W-20,130], radius=26, fill=(255,246,226), outline=(214,185,140), width=4)
draw.text((50,40),'Atemmuskulatur: vollständige Hook-Tafel',font=ImageFont.truetype(font_paths[1],46),fill=(54,35,24))
draw.text((50,92),'Jede Karte: linke Hauptfigur = Muskel/Aktion, rechte magenta Begleitfigur = Innervation. Exakte Hooks zusätzlich direkt auf der Karte.',font=FONT,fill=(79,52,36))
coords={}
for idx,card in enumerate(cards):
    r=idx//cols; c=idx%cols
    x=margin+c*(680+gap); y=150+margin+r*(930+gap)
    poster.paste(card,(x,y)); coords[DATA[idx]['id']]=(100*(x+57)/W,100*(y+57)/H)
poster.save(POSTER,quality=92)

# Build site
hotspots=''.join(f'<button class="hotspot" data-id="{d["id"]}" style="left:{coords[d["id"]][0]:.2f}%;top:{coords[d["id"]][1]:.2f}%">{d["id"]}</button>' for d in DATA)
buttons=''.join(f'<button data-id="{d["id"]}">{d["id"]}</button>' for d in DATA)
rows='\n'.join(f'<tr data-id="{d["id"]}"><td>{d["id"]}</td><td><b>{html.escape(d["title"])}</b><br><em>{html.escape(d["muscle"])}</em></td><td>{html.escape(d["inn"])}</td><td><span class="magenta">{html.escape(d["level"])}<br>{html.escape(d["range"])}<br>{html.escape(d["nerve"])}</span></td><td class="green">{html.escape(d["action"])}</td></tr>' for d in DATA)
jsondata=json.dumps(DATA,ensure_ascii=False)
html_doc=f'''<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Atemmuskulatur komplette Hook-Tafel</title><link rel="stylesheet" href="style.css"></head><body><header><p class="eyebrow">komplett neu · alle Muskeln · Muskel-Figur + Innervations-Figur</p><h1>Atemmuskulatur: vollständige Hook-Tafel</h1><p>Neu aufgebaut, weil die Innervation im Einzelbild nicht zuverlässig sichtbar war: jedes Feld hat jetzt eine Hauptfigur für den Muskel und eine zweite magenta Begleitfigur für die Innervation. Zusätzlich sind die C/Th/L-Höhe und Range-Endpunkte deterministisch direkt auf dem Poster eingeblendet.</p><div class="key"><span class="gdot"></span> grün = Muskel/Aktion <span class="mdot"></span> magenta = Innervation <span class="rdot"></span> rot = klickbare Nummer <span class="ydot"></span> gold = Atem-Story</div></header><main><section class="poster"><h2>Ein zusammengefügtes Poster aus 15 kontrollierten Einzelbildern</h2><p>Die Bildgenerator-Hooks werden nicht mehr blind vertraut: die genaue Innervation steht zusätzlich direkt im Bildfeld. Klick auf rote Nummern im Poster zeigt die gleiche Legende interaktiv.</p><div class="integrated-wrap"><img src="assets/atemmuskulatur_complete_hooks_poster.jpg" alt="Atemmuskulatur vollständige Hook-Tafel">{hotspots}<aside id="sceneLegend" class="scene-legend" aria-live="polite"><b id="sceneLegendTitle"></b><span id="sceneLegendMuscle"></span><span id="sceneLegendInn"></span><span id="sceneLegendCode" class="magenta"></span><span id="sceneLegendAction" class="green"></span><a href="#legend">zur Tabelle</a></aside></div><p><a href="assets/atemmuskulatur_complete_hooks_poster.jpg" target="_blank">Poster groß öffnen</a></p></section><section class="focus"><p class="zone" id="focusZone"></p><h2 id="focusTitle"></h2><p id="focusMuscle"></p><p id="focusInn"></p><p class="magenta" id="focusCode"></p><p class="green" id="focusAction"></p><div class="buttons">{buttons}</div></section><section class="code"><h2>Innervations-Code</h2><div class="codegrid"><div><b>C</b><br>Halskrone</div><div><b>Th</b><br>Thorhammer / Brustschild</div><div><b>L</b><br>Lendenstamm / Holzlog</div><div><b>S</b><br>Sakralschlange</div></div><p>Range-Endpunkte statt Segmentketten: z.B. C5–7 = Halskrone + Löwe → Schlüssel. Th7–12 = Thorhammer + Schlüssel → Noah.</p></section><section><h2>Legende / Wahrheitsebene</h2><table id="legend"><thead><tr><th>#</th><th>Figur / Muskel</th><th>Innervation</th><th>sichtbarer Innervations-Hook</th><th>grüner Muskel-Hook</th></tr></thead><tbody>{rows}</tbody></table></section><section class="note"><h2>Warum diese Version?</h2><p>Bei reiner Ein-Bild-Generierung wurden z.B. langes Thorax-Seil oder C5–7 beim Sägehai nicht zuverlässig sichtbar. Deshalb jetzt: 15 Einzelbilder + deterministische Hook-Badges im Poster. So ist die Mnemonik im Bild vollständig und die Tabelle bleibt exakt.</p></section></main><script>const DATA={jsondata};function setActive(id){{const d=DATA.find(x=>x.id===String(id));if(!d)return;document.querySelectorAll('[data-id]').forEach(e=>e.classList.toggle('active',e.dataset.id===d.id));sceneLegendTitle.textContent=d.id+'. '+d.title;sceneLegendMuscle.textContent=d.muscle;sceneLegendInn.textContent=d.inn;sceneLegendCode.textContent=d.level+' | '+d.range+' | '+d.nerve;sceneLegendAction.textContent=d.action;focusZone.textContent='Muskel '+d.id;focusTitle.textContent=d.title;focusMuscle.textContent=d.muscle;focusInn.textContent=d.inn;focusCode.textContent=d.level+' | '+d.range+' | '+d.nerve;focusAction.textContent=d.action;}}document.querySelectorAll('[data-id]').forEach(e=>{{e.tabIndex=0;e.addEventListener('click',()=>setActive(e.dataset.id));e.addEventListener('mouseenter',()=>setActive(e.dataset.id));e.addEventListener('keydown',ev=>{{if(ev.key==='Enter'||ev.key===' ')setActive(e.dataset.id);}})}});setActive('1');</script></body></html>'''
(ROOT/'index.html').write_text(html_doc)
(ROOT/'README.md').write_text('# Atemmuskulatur vollständige Hook-Tafel\n\n15 kontrolliert generierte Einzelbilder, zu einem Poster zusammengesetzt. Jede Karte hat eine Muskel-Hauptfigur und eine magenta Innervations-Begleitfigur; die exakte Innervation ist zusätzlich deterministisch auf dem Poster eingeblendet.\n')
print(POSTER)
