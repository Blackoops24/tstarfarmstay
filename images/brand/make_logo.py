from PIL import Image, ImageDraw, ImageFont
import numpy as np

src = Image.open("logo-original.jpg").convert("RGB")
cx, cy, R = 657, 358, 281
a = np.array(src).astype(int)
yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]
inside = (xx - cx) ** 2 + (yy - cy) ** 2 <= R ** 2
dark = (a.max(axis=2) < 30) & inside
cream = np.array([253, 248, 233])
a[dark] = cream
img = Image.fromarray(a.astype("uint8"))
d = ImageDraw.Draw(img)

def centered(text, y, size, x=cx, fill=(88, 42, 20), spacing=0):
    f = ImageFont.truetype("C:/Windows/Fonts/georgiab.ttf", size)
    w = sum(f.getlength(c) for c in text) + spacing * (len(text) - 1)
    px = x - w / 2
    for c in text:
        d.text((px, y), c, font=f, fill=fill)
        px += f.getlength(c) + spacing

# replace ESCAPE -> STAY (keep the side flourishes)
d.rectangle([cx - 96, 212, cx + 96, 256], fill=tuple(cream))
centered("STAY", 210, 42, spacing=6)
# replace EST. 2023 -> EST. 2026
d.rectangle([cx - 66, 498, cx + 66, 524], fill=tuple(cream))
centered("EST. 2026", 497, 24, spacing=1)

# crop to the circle with transparent corners
box = (cx - R - 8, cy - R - 8, cx + R + 8, cy + R + 8)
out = img.crop(box).convert("RGBA")
m = Image.new("L", out.size, 0)
ImageDraw.Draw(m).ellipse([0, 0, out.size[0] - 1, out.size[1] - 1], fill=255)
out.putalpha(m)
out.save("logo.png")
print(out.size)


