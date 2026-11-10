# -*- coding: utf-8 -*-
"""S16 四色人格图鉴 · 预览拼图（6 格，取自 14.57s 样片）"""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont

SRC = r"E:\AI视频工程\MBTI\references\mbti-career-atlas-2026-11-04\replica\replica-intj-14s-v2.mp4"
OUT = r"E:\视频工厂\10-风格库\预览\S16.jpg"
TMP = os.path.join(os.path.dirname(OUT), "_tmp", "s16")
os.makedirs(TMP, exist_ok=True)
FB = r"C:\Windows\Fonts\msyhbd.ttc"
FR = r"C:\Windows\Fonts\msyh.ttc"
ACCENT = (232, 219, 24)

times = [1.2, 3.0, 5.5, 8.5, 12.0, 14.0]
cell_w, cell_h, pad = 300, 169, 6
W = pad + len(times) * (cell_w + pad)
H = 96 + cell_h + 46
canvas = Image.new("RGB", (W, H), (12, 12, 14))
d = ImageDraw.Draw(canvas)
d.text((18, 14), "S16 · 四色人格图鉴 / MBTI 职场图鉴", font=ImageFont.truetype(FB, 34), fill=(240, 238, 232))
d.text((20, 58), "1280x720 · 30fps · 7.07/4.17/3.33s 三镜硬切 · 真生图 low-poly · 无水印", font=ImageFont.truetype(FR, 18), fill=(150, 148, 156))
for i, t in enumerate(times):
    p = os.path.join(TMP, f"f{i}.png")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", SRC, "-frames:v", "1", p], check=True)
    im = Image.open(p).convert("RGB").resize((cell_w, cell_h), Image.LANCZOS)
    x = pad + i * (cell_w + pad); y = 96
    canvas.paste(im, (x, y))
    d.rectangle([x - 1, y - 1, x + cell_w, y + cell_h], outline=(52, 52, 58), width=1)
    d.text((x + 4, y + cell_h + 6), f"{t:.1f}s", font=ImageFont.truetype(FR, 15), fill=(160, 158, 166))
canvas.save(OUT, quality=92)
print("wrote", OUT, canvas.size)