"""Draw original isometric cloud islands and the AP ribbon seal."""
import math
from pathlib import Path
from random import Random

OUT = Path(__file__).resolve().parents[1] / "frontend/public/art"
OUT.mkdir(exist_ok=True, parents=True)
def svg(name, view, body):
    (OUT / (name + ".svg")).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view}">{body}</svg>')

for name, ink in [('seal','#694d68'),('seal-night','#f5d5e0'),('favicon','#694d68')]:
    svg(name,'0 0 100 100',f'<g stroke="{ink}" fill="none"><circle cx="50" cy="47" r="36"/><circle cx="50" cy="47" r="32" stroke-dasharray="1 3"/></g><text x="49" y="60" text-anchor="middle" font-family="Georgia,serif" font-style="italic" font-size="34" fill="{ink}">AP</text><path d="M50 77Q19 55 28 78Q33 85 50 77Q67 58 72 72Q73 86 50 77L62 95L52 89L47 96Z" fill="#e1a9c2" stroke="{ink}" stroke-width="1"/>')

def island(kind):
    rng=Random(4)
    parts=['<defs><linearGradient id="cloud" x2=".28" y2="1"><stop stop-color="#fffefa"/><stop offset=".56" stop-color="#f4e4ef"/><stop offset="1" stop-color="#b6a6c8"/></linearGradient><linearGradient id="sky" x2="1" y2="1"><stop stop-color="#ffe6e8"/><stop offset=".6" stop-color="#dacdf0"/><stop offset="1" stop-color="#b7cde0"/></linearGradient></defs>']
    def ellipse(x,y,rx,ry,c): parts.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{c}"/>')
    def point(x,y,z=0):return (300+(x-y)*.88,238+(x+y)*.39-z)
    def poly(pts,color,stroke='#836e88'):
        coords=' '.join('%.1f,%.1f'%point(*p) for p in pts)
        parts.append(f'<polygon points="{coords}" fill="{color}" stroke="{stroke}" stroke-width="1.25" stroke-linejoin="round"/>')
    def box(x,y,w,d,h,colors,z=0):
        a,b,c,e=(x,y),(x+w,y),(x+w,y+d),(x,y+d)
        poly([(*e,z),(*c,z),(*c,z+h),(*e,z+h)],colors[1])
        poly([(*c,z),(*b,z),(*b,z+h),(*c,z+h)],colors[2])
        poly([(*a,z+h),(*b,z+h),(*c,z+h),(*e,z+h)],colors[0])
    lilac=['#eee4f5','#c3afd6','#a48bb7']; pink=['#ffe5e6','#e5bac9','#c39caf']; blue=['#e1eff4','#bad1dc','#95aebf']
    for y,rx in [(269,192),(257,215),(248,182)]:
        for i in range(17):
            ang=i*math.tau/17
            ellipse(round(300+rx*.85*math.cos(ang)),round(y+37*math.sin(ang)),rng.randint(33,56),rng.randint(20,34),'url(#cloud)')
    box(-104,-80,208,160,9,lilac)
    if kind in ['hero','deployhub','labquest','resume','workspace']:
        if kind in ['hero','labquest','workspace','resume']:
            box(-75,-26,104,58,5,pink,9)
            box(-72,-28,99,5,64,lilac,15)
            poly([(-66,-22,23),(20,-22,23),(20,-22,72),(-66,-22,72)],'#665573')
            for i,w in enumerate([34,48,25,60,41]):
                x=-58+(i%2)*8
                poly([(x,-21,63-i*7),(x+w,-21,63-i*7),(x+w,-21,65-i*7),(x,-21,65-i*7)],['#f6ccdc','#c4dfe8'][i%2])
            for j in range(4):
                for i in range(10):box(-62+i*7,-15+j*6,5,3,1,blue,15)
        if kind in ['hero','deployhub','labquest']:
            for j,(x,y,h) in enumerate([(33,-61,4),(66,-45,3)] if kind!='deployhub' else [(-72,-48,4),(-9,-42,5),(48,-45,3)]):
                for i in range(h):
                    z=10+i*19
                    box(x,y,30,37,16,blue if j else lilac,z)
                    poly([(x+3,y+37,z+5),(x+23,y+37,z+5),(x+23,y+37,z+9),(x+3,y+37,z+9)],'#695c75')
                    px,py=point(x+26,y+37,z+10);ellipse(px,py,1.5,1.5,'#ffe3ae')
        for i in range(3):box(48,25,28,28,3,pink if i%2 else blue,10+i*4)
    elif kind=='booth':
        box(-32,-30,68,58,8,pink,9)
        box(-27,-26,58,49,108,pink,17)
        for i in range(2):
            for j in range(3):
                x=-21+i*24;z=37+j*23
                poly([(x,24,z),(x+18,24,z),(x+18,24,z+17),(x,24,z+17)],'#d8e4ef')
        box(-34,-34,74,66,8,pink,125)
    else:
        for x,y,h in [(-77,-42,65),(-30,-62,91),(12,-40,67),(48,0,40),(-30,21,32)]:
            box(x,y,24,27,h,blue,9)
            for z in range(18,h,13):
                for dx in (4,13):poly([(x+dx,y+27,z),(x+dx+5,y+27,z),(x+dx+5,y+27,z+6),(x+dx,y+27,z+6)],'#ffefcc')
    for x,y,h in [(-90,18,27),(87,26,21),(72,-63,19)]:
        box(x,y,4,4,h,pink,9)
        px,py=point(x,y,h+9);ellipse(px,py-7,11,15,'#bbb9cf');ellipse(px-3,py-12,7,9,'#d5cfdf')
    for x,y,r in [(60,197,5),(510,142,6),(451,101,4),(120,109,4),(215,57,5)]:
        parts.append(f'<path d="M{x-r} {y}q{r} 0 {r} {-r}q0 {r} {r} {r}q{-r} 0 {-r} {r}q0 {-r} {-r} {-r}" fill="#b291a8"/>')
    svg(kind,'0 20 600 320',''.join(parts))
for name in ['hero','labquest','deployhub','resume','saaf-bharath','booth','workspace']:island(name)
