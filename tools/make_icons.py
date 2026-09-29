# -*- coding: utf-8 -*-
"""生成 PWA 图标：512/192（圆角 any）+ maskable 512（全出血）+ apple-touch 180。
用法：D:\\Python314\\python.exe -X utf8 tools\\make_icons.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "icons")
os.makedirs(OUT, exist_ok=True)

C1 = (200, 68, 44)    # 朱砂
C2 = (42, 157, 143)   # 孔雀绿
FONT_CANDIDATES = [r"C:\Windows\Fonts\msyhbd.ttc", r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\simhei.ttf"]


def font(size):
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def gradient(size):
    """对角线渐变底图（RGB）。"""
    w, h = size
    img = Image.new("RGB", size)
    px = img.load()
    for y in range(h):
        for x in range(w):
            t = (x / max(1, w - 1) + y / max(1, h - 1)) / 2
            px[x, y] = tuple(int(C1[i] + (C2[i] - C1[i]) * t) for i in range(3))
    return img


def draw_glyph(img, ratio=0.62, sub=None):
    """居中画白色"旅"，sub 为可选的小字副标。"""
    d = ImageDraw.Draw(img)
    w, h = img.size
    f = font(int(h * ratio))
    text = "旅"
    bbox = d.textbbox((0, 0), text, font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text(((w - tw) / 2 - bbox[0], (h - th) / 2 - bbox[1] - h * (0.03 if sub else 0)), text, font=f, fill=(255, 255, 255))
    if sub:
        fs = font(int(h * 0.11))
        b2 = d.textbbox((0, 0), sub, font=fs)
        d.text(((w - (b2[2] - b2[0])) / 2 - b2[0], h * 0.80), sub, font=fs, fill=(255, 255, 255, 220))


def rounded(img, radius_ratio=0.18):
    """圆角化（四角透明）。"""
    img = img.convert("RGBA")
    w, h = img.size
    mask = Image.new("L", (w * 2, h * 2), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w * 2 - 1, h * 2 - 1], radius=int(w * 2 * radius_ratio), fill=255)
    mask = mask.resize((w, h), Image.LANCZOS)
    img.putalpha(mask)
    return img


def make(size, out_name, rounded_corners, sub=None):
    S = 2
    big = gradient((size * S, size * S))
    draw_glyph(big, sub=sub)
    img = big.resize((size, size), Image.LANCZOS)
    if rounded_corners:
        img = rounded(img)
    path = os.path.join(OUT, out_name)
    img.save(path, "PNG")
    print("OK", out_name, img.size)


if __name__ == "__main__":
    # any 用途：圆角（favicon/manifest）
    make(512, "icon-512.png", True, sub="2026")
    make(192, "icon-192.png", True, sub="2026")
    # maskable：全出血，图形居中 80% 安全区内
    make(512, "icon-maskable-512.png", False, sub="2026")
    # iOS 主屏图标：全出血无透明
    make(180, "apple-touch-icon.png", False, sub=None)
    make(32, "favicon-32.png", True, sub=None)
