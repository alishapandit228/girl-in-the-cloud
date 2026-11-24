"""Render a real 1200 × 630 social sharing card during setup."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[1]
def generate():
    im=Image.new("RGB",(1200,630));d=ImageDraw.Draw(im)
    for x in range(1200):
        t=x/1199
        d.line((x,0,x,630),fill=tuple(round(a+(b-a)*t) for a,b in zip((255,249,245),(226,213,239))))
    def font(name,size):
        try:return ImageFont.truetype(name,size)
        except OSError:return ImageFont.load_default(size=size)
    ink="#59465f"
    d.text((90,72),"A L I S H A   P A N D I T",font=font("DejaVuSans.ttf",22),fill=ink)
    d.text((78,156),"Girl in",font=font("DejaVuSerif.ttf",112),fill=ink)
    d.text((78,269),"the Cloud.",font=font("DejaVuSerif-Italic.ttf",112),fill=ink)
    d.text((88,507),"Soft aesthetics. Strong architecture.",font=font("DejaVuSans.ttf",30),fill=ink)
    d.ellipse((800,145,1110,455),outline="#b699ad",width=3)
    d.ellipse((813,158,1097,442),outline="#b699ad",width=1)
    d.text((953,292),"AP",anchor="mm",font=font("DejaVuSerif-Italic.ttf",98),fill=ink)
    im.save(ROOT/"frontend/public/art/social.png",optimize=True)
if __name__=="__main__":generate()
