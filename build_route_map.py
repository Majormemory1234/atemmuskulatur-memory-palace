#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
import math

ROOT = Path('/home/hermes/respiratory-muscle-mnemonic-site')
PANEL_DIR = ROOT/'assets/gpt-image-2-story-panels'
OUT = ROOT/'assets/atemmuskulatur_route_map.jpg'
items = [
(1,'Zwerchfell','Diaphragma','C3–5'),(2,'Intercostales','Mm. intercostales','Th1–11'),(3,'SCM-Kapitän','M. sternocleidomastoideus','XI+C2–3'),
(4,'Skalenen','Mm. scaleni','C3–8'),(5,'Pectoralis major','M. pectoralis major','C5–T1'),(6,'Pectoralis minor','M. pectoralis minor','C8–T1'),
(7,'Serratus post. sup.','M. serratus posterior superior','Th2–5'),(8,'Serratus post. inf.','M. serratus posterior inferior','Th9–12'),(9,'Serratus anterior','M. serratus anterior','C5–7'),
(10,'Rectus','M. rectus abdominis','Th7–12'),(11,'Transversus','M. transversus abdominis','Th7–12+L1'),(12,'Obliquus externus','M. obliquus externus','Th5–12'),
(13,'Obliquus internus','M. obliquus internus','Th7–12+L1'),(14,'Quadratus lumb.','M. quadratus lumborum','Th12–L4'),(15,'Latissimus','M. latissimus dorsi','C6–8')]

W,H=2600,3900
margin=140
colx=[520,1300,2080]
rowy=[720,1300,1880,2460,3040]
# serpentine reading route to keep all in one image with no overlap
order_positions=[]
for r,y in enumerate(rowy):
    xs=colx if r%2==0 else list(reversed(colx))
    for x in xs: order_positions.append((x,y))
pos={i+1:p for i,p in enumerate(order_positions)}
thumb=(510,340); label_h=105
font_paths=['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf']
bold_paths=['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf','/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf']
def font(size,bold=False):
    for p in (bold_paths if bold else font_paths):
        if Path(p).exists(): return ImageFont.truetype(p,size)
    return ImageFont.load_default()
F_TITLE=font(72,True); F_SUB=font(32); F_NUM=font(44,True); F_NAME=font(24,True); F_SMALL=font(19); F_ZONE=font(29,True)
img=Image.new('RGB',(W,H),(29,20,16)); d=ImageDraw.Draw(img)
# global opera house / rib cage background
for y in range(520,3370,360):
    bbox=[160,y-360,W-160,y+360]
    d.arc(bbox, 200, 340, fill=(86,55,42), width=18)
    d.arc([bbox[0]+20,bbox[1]+20,bbox[2]-20,bbox[3]-20], 200, 340, fill=(220,210,184), width=7)
# central warm glow
for r in range(1300,100,-60):
    alpha=r/1300
    col=(int(38+40*alpha), int(26+25*alpha), int(18+12*alpha))
    d.ellipse([W/2-r, H/2-r*1.25, W/2+r, H/2+r*1.25], fill=col)
# border/title
d.rectangle([30,30,W-30,H-30], outline=(156,70,50), width=9)
d.rectangle([52,52,W-52,H-52], outline=(238,190,104), width=4)
d.text((margin,58),'Atemmuskulatur: Route in einem Bild',font=F_TITLE,fill=(255,239,205))
d.text((margin,145),'Eine einzige sichtbare Memory-Palace-Karte: folge der goldenen Atemperle von 1 bis 15.',font=F_SUB,fill=(250,215,156))
# legend
y=205
for x,c,t in [(margin,(28,164,79),'grün = Muskel/Aktion'),(margin+440,(215,34,180),'magenta = Innervation'),(margin+950,(220,35,51),'rot = Nummer'),(margin+1360,(246,198,67),'gold = Route')]:
    d.ellipse([x,y,x+28,y+28], fill=c)
    d.text((x+40,y-1),t,font=F_SMALL,fill=(255,239,205))
# zone bands
zones=[('Einatmung: Hauptmotor + Rippen',1,2),('Hals-/Brust-Hilfsmuskeln',3,6),('Sägezahn-Logen und Scapula-Wand',7,9),('Bauchpresse',10,13),('Fundament und Finale',14,15)]
for label,a,b in zones:
    x1=min(pos[i][0] for i in range(a,b+1))-thumb[0]/2-25; x2=max(pos[i][0] for i in range(a,b+1))+thumb[0]/2+25
    y1=min(pos[i][1] for i in range(a,b+1))-thumb[1]/2-65
    d.rounded_rectangle([x1,y1,x2,y1+48], radius=20, fill=(255,246,221), outline=(231,183,91), width=3)
    d.text((x1+18,y1+8),label,font=F_ZONE,fill=(67,43,30))
# route line first
route=[pos[i] for i in range(1,16)]
for width,col in [(42,(85,60,18)),(28,(173,121,31)),(14,(255,207,71))]:
    d.line(route, fill=col, width=width, joint='curve')
for i in range(14):
    x1,y1=route[i]; x2,y2=route[i+1]
    ang=math.atan2(y2-y1,x2-x1)
    ax=x1+(x2-x1)*0.74; ay=y1+(y2-y1)*0.74
    pts=[(ax+math.cos(ang)*18,ay+math.sin(ang)*18),(ax+math.cos(ang+2.55)*42,ay+math.sin(ang+2.55)*42),(ax+math.cos(ang-2.55)*42,ay+math.sin(ang-2.55)*42)]
    d.polygon(pts, fill=(255,222,95))
# add pearl dots between nodes
for i,(x,y) in enumerate(route):
    d.ellipse([x-22,y-22,x+22,y+22], fill=(255,215,68), outline=(255,252,205), width=4)
# draw nodes
for id,name,muscle,inn in items:
    x,y=pos[id]; tw,th=thumb
    src=Image.open(PANEL_DIR/f'panel_{id:02d}.png').convert('RGB')
    src=ImageOps.fit(src,(tw,th),Image.Resampling.LANCZOS,centering=(0.5,0.47))
    sx,sy=int(x-tw/2),int(y-th/2)
    shadow=Image.new('RGBA',(tw+50,th+50),(0,0,0,0)); sd=ImageDraw.Draw(shadow)
    sd.rounded_rectangle([22,22,tw+22,th+22], radius=38, fill=(0,0,0,160)); shadow=shadow.filter(ImageFilter.GaussianBlur(8))
    img.paste(shadow,(sx-25,sy-25),shadow)
    mask=Image.new('L',(tw,th),0); md=ImageDraw.Draw(mask); md.rounded_rectangle([0,0,tw,th], radius=34, fill=255)
    img.paste(src,(sx,sy),mask)
    d.rounded_rectangle([sx,sy,sx+tw,sy+th], radius=34, outline=(255,244,221), width=7)
    # number badge
    d.ellipse([sx-22,sy-22,sx+72,sy+72], fill=(221,35,51), outline=(255,245,226), width=6)
    bb=d.textbbox((0,0),str(id),font=F_NUM)
    d.text((sx+25-(bb[2]-bb[0])/2,sy+22-(bb[3]-bb[1])/2),str(id),font=F_NUM,fill='white')
    # hook dots
    d.ellipse([sx+tw-78,sy+th-42,sx+tw-50,sy+th-14], fill=(28,165,79), outline=(255,255,235), width=3)
    d.ellipse([sx+tw-42,sy+th-42,sx+tw-14,sy+th-14], fill=(215,34,180), outline=(255,255,235), width=3)
    # label underneath within cell area, no overlaps
    ly=sy+th+10
    d.rounded_rectangle([sx,ly,sx+tw,ly+label_h], radius=18, fill=(255,249,234), outline=(158,99,68), width=3)
    d.text((sx+14,ly+8),f'{id}. {name}',font=F_NAME,fill=(48,30,22))
    d.text((sx+14,ly+39),muscle,font=F_SMALL,fill=(45,43,39))
    d.text((sx+14,ly+66),inn,font=F_SMALL,fill=(170,20,150))
# concise story/footer
y=3600
d.rounded_rectangle([margin,y,W-margin,y+190], radius=28, fill=(255,244,220), outline=(232,184,92), width=4)
d.text((margin+26,y+22),'Route:',font=font(34,True),fill=(64,42,28))
footer='1–2 Luft ansaugen → 3–6 Hals/Brust helfen heben → 7–9 Sägezahn-Logen stabilisieren/ziehen Rippen → 10–13 Bauchpresse drückt Luft heraus → 14 Lende stabilisiert → 15 breiter Rücken presst Finale heraus.'
# wrap footer
line=''; yy=y+70
for word in footer.split():
    test=(line+' '+word).strip()
    if d.textlength(test,font=F_SUB)<W-2*margin-60 or not line: line=test
    else:
        d.text((margin+26,yy),line,font=F_SUB,fill=(67,43,30)); yy+=44; line=word
if line: d.text((margin+26,yy),line,font=F_SUB,fill=(67,43,30))
img.save(OUT, quality=93, optimize=True)
print(OUT)
