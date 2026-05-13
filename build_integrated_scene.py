#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter, ImageEnhance
import math

ROOT=Path('/home/hermes/respiratory-muscle-mnemonic-site')
PANEL_DIR=ROOT/'assets/gpt-image-2-story-panels'
OUT=ROOT/'assets/atemmuskulatur_integrated_scene.jpg'
W,H=3200,2400
img=Image.new('RGB',(W,H),(32,22,18))
d=ImageDraw.Draw(img)
# fonts
font_paths=['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf']
bold_paths=['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf','/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf']
def font(size,bold=False):
    for p in (bold_paths if bold else font_paths):
        if Path(p).exists(): return ImageFont.truetype(p,size)
    return ImageFont.load_default()
F_TITLE=font(78,True); F_SUB=font(31); F_NUM=font(42,True); F_SMALL=font(21,True)
# background: giant rib-cage opera house cutaway
for r in range(1500,150,-50):
    a=r/1500
    d.ellipse([W/2-r,350-r*0.45,W/2+r,350+r*1.15], fill=(int(44+35*a),int(29+20*a),int(20+10*a)))
# curtains
for side in [0,1]:
    x0=0 if side==0 else W-260
    for i in range(0,260,32):
        col=(95+i//5,24,35)
        if side==0: d.polygon([(x0+i,0),(x0+i+70,0),(x0+i+35,H)], fill=col)
        else: d.polygon([(W-i,0),(W-i-70,0),(W-i-35,H)], fill=col)
# rib arches / opera balconies
for k,y in enumerate([380,560,740,920,1100,1280,1460]):
    bbox=[310+k*45,y-300,W-310-k*45,y+430]
    d.arc(bbox, 198,342, fill=(224,214,187), width=18)
    d.arc([bbox[0]+25,bbox[1]+25,bbox[2]-25,bbox[3]-25],198,342,fill=(123,75,55),width=8)
# floor, engine, water
for rect,col in [([440,1430,2760,1775],(73,49,38)),([600,1765,2600,2085],(61,42,36)),([680,2070,2520,2310],(20,63,86))]:
    d.rounded_rectangle(rect, radius=70, fill=col, outline=(169,107,70), width=7)
# title small in image
pad=105
d.text((pad,55),'Atemmuskulatur: Das Rippen-Opernhaus',font=F_TITLE,fill=(255,239,204))
d.text((pad,142),'ein einziges Gesamtbild: alle 15 Szenen als Räume einer Story, verbunden durch die goldene Atemperle',font=F_SUB,fill=(250,215,157))
# layout: actual rooms embedded spatially in one cutaway, not card-grid labels
rooms={
 1:(1450,1130,690,450,'oval'),       # diaphragm center
 2:(820,720,500,330,'arch'),         # intercostal rib ladder
 3:(1320,430,430,290,'arch'),        # SCM neck balcony
 4:(1830,455,430,290,'arch'),        # scalenes stair
 5:(570,1065,450,300,'arch'),        # pec major front
 6:(790,1280,360,245,'arch'),        # pec minor small
 7:(2300,690,410,280,'arch'),        # serratus sup
 8:(2360,1180,410,280,'cave'),       # serratus inf
 9:(2670,980,430,300,'arch'),        # serratus ant side wall
 10:(960,1640,420,280,'cave'),       # rectus
 11:(1330,1710,420,280,'cave'),      # transversus
 12:(1710,1625,420,280,'cave'),      # ext oblique
 13:(2100,1710,420,280,'cave'),      # int oblique
 14:(1260,2140,440,300,'cave'),      # QL foundation
 15:(1990,2150,560,360,'oval'),      # lat finale
}
route=[(rooms[i][0],rooms[i][1]) for i in range(1,16)]
# gold path behind rooms, with pearl beads
for width,col in [(42,(92,66,20)),(25,(178,128,34)),(12,(255,211,75))]:
    d.line(route, fill=col, width=width, joint='curve')
for i in range(14):
    x1,y1=route[i]; x2,y2=route[i+1]
    ang=math.atan2(y2-y1,x2-x1)
    ax=x1+(x2-x1)*0.70; ay=y1+(y2-y1)*0.70
    pts=[(ax+math.cos(ang)*18,ay+math.sin(ang)*18),(ax+math.cos(ang+2.55)*38,ay+math.sin(ang+2.55)*38),(ax+math.cos(ang-2.55)*38,ay+math.sin(ang-2.55)*38)]
    d.polygon(pts, fill=(255,222,90))
for x,y in route:
    d.ellipse([x-19,y-19,x+19,y+19], fill=(255,222,83), outline=(255,252,212), width=4)
# functional labels on walls, not individual captions
labels=[('Einatmung',515,465),('Halshelfer',1300,250),('Rippen-/Sägezahn-Logen',2110,390),('Bauchpresse',1280,1450),('Fundament + Finale',1360,2295)]
for text,x,y in labels:
    d.rounded_rectangle([x,y,x+len(text)*17+40,y+42], radius=18, fill=(255,246,221), outline=(232,184,92), width=3)
    d.text((x+18,y+7),text,font=F_SMALL,fill=(67,43,29))
# paste panels as rooms, with arched/oval/cave masks and shared frame, no label cards
for id,(cx,cy,w,h,shape) in rooms.items():
    src=Image.open(PANEL_DIR/f'panel_{id:02d}.png').convert('RGB')
    src=ImageEnhance.Color(src).enhance(1.03)
    src=ImageOps.fit(src,(w,h),Image.Resampling.LANCZOS,centering=(0.5,0.47))
    x=int(cx-w/2); y=int(cy-h/2)
    mask=Image.new('L',(w,h),0); md=ImageDraw.Draw(mask)
    if shape=='oval':
        md.rounded_rectangle([0,0,w,h], radius=min(w,h)//3, fill=255)
    elif shape=='arch':
        md.rounded_rectangle([0,h*0.18,w,h], radius=36, fill=255)
        md.pieslice([0,0,w,h*0.75],180,360,fill=255)
    else:
        md.rounded_rectangle([0,0,w,h], radius=50, fill=255)
    # shadow
    shadow=Image.new('RGBA',(w+54,h+54),(0,0,0,0)); sd=ImageDraw.Draw(shadow)
    sd.rounded_rectangle([25,25,w+25,h+25], radius=60, fill=(0,0,0,150))
    shadow=shadow.filter(ImageFilter.GaussianBlur(9)); img.paste(shadow,(x-27,y-27),shadow)
    img.paste(src,(x,y),mask)
    # architectural frame matching shape
    if shape=='arch':
        d.rounded_rectangle([x,y+h*0.18,x+w,y+h], radius=38, outline=(255,242,215), width=7)
        d.arc([x,y,x+w,y+h*0.75],180,360,fill=(255,242,215),width=8)
    else:
        d.rounded_rectangle([x,y,x+w,y+h], radius=min(w,h)//3 if shape=='oval' else 50, outline=(255,242,215), width=7)
    # red number badge directly on scene
    d.ellipse([x-18,y-18,x+68,y+68], fill=(221,35,51), outline=(255,245,225), width=6)
    s=str(id); bb=d.textbbox((0,0),s,font=F_NUM)
    d.text((x+25-(bb[2]-bb[0])/2,y+21-(bb[3]-bb[1])/2),s,font=F_NUM,fill='white')
    # hook color pins, like Sketchy annotations not a table
    d.ellipse([x+w-70,y+h-40,x+w-44,y+h-14], fill=(28,164,79), outline=(255,255,235), width=3)
    d.ellipse([x+w-38,y+h-40,x+w-12,y+h-14], fill=(215,34,180), outline=(255,255,235), width=3)
# legend embedded in the scene
lx,ly=105,2100
d.rounded_rectangle([lx,ly,lx+520,ly+190], radius=28, fill=(255,246,224), outline=(232,184,92), width=4)
d.text((lx+22,ly+20),'Leseschlüssel',font=font(30,True),fill=(67,43,29))
legend=[((221,35,51),'rot: Reihenfolge'),((255,211,75),'gold: Atemperle/Route'),((28,164,79),'grün: Muskel/Aktion'),((215,34,180),'magenta: Innervation')]
for i,(c,t) in enumerate(legend):
    yy=ly+65+i*29
    d.ellipse([lx+24,yy,lx+46,yy+22], fill=c, outline=(80,50,30), width=2)
    d.text((lx+58,yy-2),t,font=font(21),fill=(67,43,29))
# footer story strip inside image
sx,sy=720,2320
d.rounded_rectangle([sx,sy,W-110,sy+52], radius=22, fill=(255,246,224), outline=(232,184,92), width=3)
d.text((sx+20,sy+12),'1–2 Luft ansaugen → 3–6 Hals/Brust heben → 7–9 Rippen/Scapula lenken → 10–13 Bauchpresse → 14 stabilisiert → 15 Finale herauspressen',font=font(23,True),fill=(67,43,29))
img.save(OUT, quality=93, optimize=True)
print(OUT)
