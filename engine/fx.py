"""Extra scene devices on top of the illustrations: handwritten notepad, chalkboard chapter titles,
phone and TV screens with moving content, red day badge with a ticking clock.

Assets (ChatGPT, generated once, reused by every episode): engine/assets/a1_desk_notepad.png,
a2_chalkboard.png, a3_phone_hand.png, a4_tv_blank.png. Screen and paper rectangles are found
automatically and cached in engine/assets/rects.json.
"""
import os, json, math
import numpy as np, skia
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
AS = os.path.join(HERE, "assets")
FT = {k: skia.Typeface.MakeFromFile(os.path.join(HERE, "fonts", f)) for k, f in
      dict(hand="Caveat.ttf", marker="PermanentMarker.ttf", mono="ShareTechMono.ttf").items()}
W, H = 1920, 1080
INK = skia.Color(28, 48, 120)
CHALK = skia.Color(244, 244, 236)


def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3


def hfont(k, size):
    f = skia.Font(FT[k], size)
    if k == "hand": f.setEmbolden(True)
    return f


_img = {}


def asset(name):
    if name not in _img:
        im = Image.open(os.path.join(AS, name + ".png")).convert("RGBA")
        sc = max(W / im.width, H / im.height)
        im = im.resize((int(im.width * sc + 0.5), int(im.height * sc + 0.5)), Image.LANCZOS)
        l, tp = (im.width - W) // 2, (im.height - H) // 2
        im = im.crop((l, tp, l + W, tp + H))
        _img[name] = (skia.Image.fromarray(np.array(im), colorType=skia.kRGBA_8888_ColorType), np.array(im))
    return _img[name]


def _largest_box(mask):
    """Bounding box of the largest connected blob in a boolean mask (simple flood fill on a 1/4 grid)."""
    m = mask[::4, ::4]; h, w = m.shape; seen = np.zeros_like(m, bool); best = None
    for y0 in range(0, h, 3):
        for x0 in range(0, w, 3):
            if not m[y0, x0] or seen[y0, x0]: continue
            st = [(y0, x0)]; seen[y0, x0] = True; ys = []; xs = []
            while st:
                y, x = st.pop(); ys.append(y); xs.append(x)
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    yy, xx = y + dy, x + dx
                    if 0 <= yy < h and 0 <= xx < w and m[yy, xx] and not seen[yy, xx]:
                        seen[yy, xx] = True; st.append((yy, xx))
            if best is None or len(ys) > best[0]:
                best = (len(ys), min(xs) * 4, min(ys) * 4, max(xs) * 4 + 4, max(ys) * 4 + 4)
    return best[1:]


def rects():
    p = os.path.join(AS, "rects.json")
    R = json.load(open(p)) if os.path.exists(p) else {}
    tests = {
        "a1_desk_notepad": lambda a: (a[..., 0] > 205) & (a[..., 1] > 195) & (a[..., 2] > 160) & (np.ptp(a[..., :3].astype(int), axis=2) < 60),
        "a2_chalkboard": lambda a: (a[..., 1] > a[..., 0] + 8) & (a[..., 1] < 140) & (a[..., 2] < 130),
        "a3_phone_hand": lambda a: (a[..., :3].min(axis=2) > 225),
        "a4_tv_blank": lambda a: (np.ptp(a[..., :3].astype(int), axis=2) < 18) & (a[..., :3].max(axis=2) < 110) & (a[..., :3].max(axis=2) > 25),
    }
    changed = False
    for k, f in tests.items():
        if k in R or not os.path.exists(os.path.join(AS, k + ".png")): continue
        R[k] = _largest_box(f(asset(k)[1])); changed = True
    if changed: json.dump(R, open(p, "w"), indent=1)
    return R


def draw_asset(c, name, t0, t, zoom=0.035):
    img = asset(name)[0]; u = min(1.0, max(0.0, (t - t0) / 6.0)); z = 1.0 + zoom * u
    c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-W / 2, -H / 2)
    c.drawImageRect(img, skia.Rect.MakeWH(W, H), skia.SamplingOptions(skia.FilterMode.kLinear), skia.Paint(AntiAlias=True))
    return z  # caller must c.restore()


def write(c, s, x, y, f, color, prog, align="l"):
    """Draw text revealed left to right (prog 0..1). Returns the pen tip position."""
    w = f.measureText(s); x0 = x - (w / 2 if align == "c" else 0)
    if prog <= 0: return x0, y
    c.save(); c.clipRect(skia.Rect.MakeLTRB(x0 - 10, y - f.getSize() * 1.3, x0 + w * min(1.0, prog), y + f.getSize() * 0.5))
    c.drawString(s, x0, y, f, skia.Paint(AntiAlias=True, Color=color)); c.restore()
    wob = math.sin(prog * 40) * f.getSize() * 0.12
    return x0 + w * min(1.0, prog), y - f.getSize() * 0.35 + wob


def pen(c, x, y, chalk=False):
    c.save(); c.translate(x, y); c.rotate(-35)
    if chalk:
        c.drawRoundRect(skia.Rect.MakeXYWH(-6, -90, 22, 92), 6, 6, skia.Paint(AntiAlias=True, Color=CHALK))
    else:
        c.drawPath(skia.Path().moveTo(0, 0).lineTo(-9, -26).lineTo(9, -26).close(), skia.Paint(AntiAlias=True, Color=skia.Color(230, 210, 170)))
        c.drawRect(skia.Rect.MakeXYWH(-2, -8, 4, 8), skia.Paint(Color=INK))
        c.drawRoundRect(skia.Rect.MakeXYWH(-11, -190, 22, 166), 8, 8, skia.Paint(AntiAlias=True, Color=skia.Color(35, 80, 190)))
        c.drawRect(skia.Rect.MakeXYWH(-11, -120, 22, 10), skia.Paint(Color=skia.Color(210, 214, 222)))
    c.restore()


def sentence(s):
    s = s.strip()
    return s if any(ch.islower() for ch in s) else s[:1] + s[1:].lower()


# ---------------- notepad: stats and lists are written by hand ----------------
def notepad(c, t, l, accent, t_in):
    R = rects()["a1_desk_notepad"]; x0, y0, x1, y1 = R
    draw_asset(c, "a1_desk_notepad", t_in, t)
    v = l["visual"]; lt = t - t_in; dur = max(2.0, l["end"] - t_in)
    px, py = None, None
    mx = x0 + (x1 - x0) * 0.09; maxw = (x1 - x0) * 0.82
    if v[0] == "card":
        big, sub = v[1], sentence(v[2]); src = v[3] if len(v) > 3 else ""
        fb = hfont("hand", 270); fs = hfont("hand", 92)
        while fb.measureText(big) > maxw: fb = hfont("hand", fb.getSize() * 0.92)
        while fs.measureText(sub) > maxw: fs = hfont("hand", fs.getSize() * 0.94)
        yb = y0 + (y1 - y0) * 0.45; ys = yb + 150
        p1 = (lt - 0.15) / 0.9; p2 = (lt - 1.15) / 1.4
        if p1 > 0: px, py = write(c, big, (x0 + x1) / 2, yb, fb, INK, p1, "c")
        if p2 > 0: px, py = write(c, sub, (x0 + x1) / 2, ys, fs, INK, p2, "c")
        if p1 > 1.0 and p1 < 1.6:   # underline the number
            w = fb.measureText(big) * ease((p1 - 1.0) / 0.5)
            c.drawLine((x0 + x1) / 2 - fb.measureText(big) / 2, yb + 22, (x0 + x1) / 2 - fb.measureText(big) / 2 + w, yb + 26, skia.Paint(AntiAlias=True, Color=skia.Color(200, 40, 40), StrokeWidth=7, StrokeCap=skia.Paint.kRound_Cap))
        elif p1 >= 1.6:
            c.drawLine((x0 + x1) / 2 - fb.measureText(big) / 2, yb + 22, (x0 + x1) / 2 + fb.measureText(big) / 2, yb + 26, skia.Paint(AntiAlias=True, Color=skia.Color(200, 40, 40), StrokeWidth=7, StrokeCap=skia.Paint.kRound_Cap))
        if src and p2 > 1.0:
            f = hfont("hand", 44); w = f.measureText(src)
            c.drawString(src, (x0 + x1) / 2 - min(w, maxw) / 2, y1 - (y1 - y0) * 0.1, f, skia.Paint(AntiAlias=True, Color=skia.Color(90, 90, 100, int(200 * ease(p2 - 1.0)))))
    else:   # list
        items = [sentence(i) for i in v[1]]; n = len(items)
        fi = hfont("hand", 118)
        while max(fi.measureText("• " + i) for i in items) > maxw: fi = hfont("hand", fi.getSize() * 0.94)
        gap = min(fi.getSize() * 1.35, (y1 - y0) * 0.78 / n); ytop = (y0 + y1) / 2 - gap * (n - 1) / 2 + fi.getSize() * 0.3
        slot = max(0.8, (dur - 0.4) / n); wr = min(1.0, slot * 0.75)
        for k, it in enumerate(items):
            p = (lt - 0.2 - k * slot) / wr
            if p > 0: px, py = write(c, "• " + it, mx, ytop + k * gap, fi, INK, p)
    done = (v[0] == "card" and lt > 1.15 + 1.4 + 0.4) or (v[0] != "card" and lt > 0.2 + (n - 1) * slot + wr + 0.4)
    if px is not None and not done: pen(c, px, py)
    c.restore()


# ---------------- chalkboard chapter titles ----------------
def chalk_card(c, t, ch):
    b0, b1 = ch["beat"]; lt = t - b0
    R = rects()["a2_chalkboard"]; x0, y0, x1, y1 = R
    draw_asset(c, "a2_chalkboard", b0, t, 0.02)
    fl = hfont("marker", 230); ft = hfont("marker", 80)
    cx = (x0 + x1) / 2; yl = y0 + (y1 - y0) * 0.52; yt = yl + 130
    while fl.measureText(ch["label"]) > (x1 - x0) * 0.85: fl = hfont("marker", fl.getSize() * 0.92)
    while ft.measureText(ch["tag"]) > (x1 - x0) * 0.85: ft = hfont("marker", ft.getSize() * 0.92)
    px, py = write(c, ch["label"], cx, yl, fl, CHALK, lt / 0.85, "c")
    if lt > 0.95: px, py = write(c, ch["tag"], cx, yt, ft, skia.Color(250, 214, 120), (lt - 0.95) / 0.8, "c")
    if lt < 1.8: pen(c, px, py, chalk=True)
    c.restore()


# ---------------- phone and TV screens ----------------
ALERTS = [("EMERGENCY ALERT", "Shelter in place. Stay indoors."), ("CITY OF RIVERTON", "Do not approach infected persons."),
          ("NEWS", "Hospital outbreak spreads overnight"), ("EMERGENCY ALERT", "Avoid highways. Roads closed."),
          ("MOM", "are you ok?? call me"), ("NEWS", "National Guard deployed downtown")]


def _screen(c, name):
    R = rects()[name]; x0, y0, x1, y1 = R
    return skia.Rect.MakeLTRB(x0 + 4, y0 + 4, x1 - 4, y1 - 4)


def phone(c, t, kind, t_in, l):
    lt = t - t_in
    draw_asset(c, "a3_phone_hand", t_in, t, 0.03)
    r = _screen(c, "a3_phone_hand"); sw = r.width(); sh = r.height()
    c.save(); c.clipRRect(skia.RRect.MakeRectXY(r, 34, 34), skia.ClipOp.kIntersect, True)
    if kind == "alerts":
        c.drawRect(r, skia.Paint(Color=skia.Color(16, 20, 30)))
        n = int(min(len(ALERTS), 1 + lt / 0.55)); bh = sh * 0.15; gap = sh * 0.02
        for i in range(n):
            a = ease((lt - i * 0.55) / 0.3); k = n - 1 - i
            y = r.top() + sh * 0.05 + k * (bh + gap) - (1 - a) * bh
            br = skia.Rect.MakeXYWH(r.left() + sw * 0.05, y, sw * 0.9, bh)
            red = ALERTS[i][0].startswith("EMERG")
            c.drawRoundRect(br, 22, 22, skia.Paint(AntiAlias=True, Color=skia.Color(200, 40, 45) if red else skia.Color(245, 245, 248)))
            ft = hfont("mono", bh * 0.24); fb = skia.Font(None, bh * 0.2)
            c.drawString(ALERTS[i][0], br.left() + sw * 0.05, br.top() + bh * 0.38, ft, skia.Paint(AntiAlias=True, Color=skia.Color(255, 255, 255) if red else skia.Color(30, 30, 40)))
            txt = ALERTS[i][1]
            while fb.measureText(txt) > br.width() * 0.9: fb = skia.Font(None, fb.getSize() * 0.93)
            c.drawString(txt, br.left() + sw * 0.05, br.top() + bh * 0.75, fb, skia.Paint(AntiAlias=True, Color=skia.Color(255, 235, 235) if red else skia.Color(60, 60, 70)))
    elif kind == "message":
        c.drawRect(r, skia.Paint(Color=skia.Color(236, 239, 244)))
        msg = "I'm safe at home. If the network dies, meet me at the north lake. Love you."
        f = skia.Font(None, sw * 0.072); n = int(len(msg) * min(1.0, max(0.0, (lt - 0.3) / 3.0)))
        words = msg[:n].split(" "); lines = [""]
        for w_ in words:
            test = (lines[-1] + " " + w_).strip()
            if f.measureText(test) > sw * 0.68: lines.append(w_)
            else: lines[-1] = test
        bx = r.right() - sw * 0.06; by = r.bottom() - sh * 0.22; lh = f.getSize() * 1.3
        bw = max(f.measureText(s) for s in lines) + sw * 0.08 if n else 0
        if n:
            br = skia.Rect.MakeLTRB(bx - bw, by - lh * len(lines) - sw * 0.03, bx, by + sw * 0.02)
            c.drawRoundRect(br, 28, 28, skia.Paint(AntiAlias=True, Color=skia.Color(10, 132, 255)))
            for i, s in enumerate(lines): c.drawString(s, br.left() + sw * 0.04, br.top() + lh * (i + 1) - f.getSize() * 0.15, f, skia.Paint(AntiAlias=True, Color=skia.Color(255, 255, 255)))
        if lt > 3.6:
            fs = skia.Font(None, sw * 0.045); c.drawString("Delivered", bx - fs.measureText("Delivered"), by + sw * 0.08, fs, skia.Paint(AntiAlias=True, Color=skia.Color(120, 125, 135)))
        c.drawRoundRect(skia.Rect.MakeXYWH(r.left() + sw * 0.05, r.bottom() - sh * 0.09, sw * 0.9, sh * 0.06), 30, 30, skia.Paint(AntiAlias=True, Color=skia.Color(255, 255, 255)))
    elif kind == "silent":
        c.drawRect(r, skia.Paint(Color=skia.Color(20, 22, 28)))
        on = lt > 1.1; cx, cy = r.centerX(), r.top() + sh * 0.42
        tw, th = sw * 0.5, sw * 0.25; k = ease((lt - 1.1) / 0.25)
        c.drawRoundRect(skia.Rect.MakeXYWH(cx - tw / 2, cy - th / 2, tw, th), th / 2, th / 2, skia.Paint(AntiAlias=True, Color=skia.Color(int(60 + 160 * k), int(200 - 150 * k), int(90 - 40 * k))))
        kx = cx - tw / 2 + th / 2 + (tw - th) * (1 - k)
        c.drawCircle(kx, cy, th * 0.42, skia.Paint(AntiAlias=True, Color=skia.Color(255, 255, 255)))
        f = hfont("mono", sw * 0.09); s = "SILENT" if on else "RING"
        c.drawString(s, cx - f.measureText(s) / 2, cy + th * 1.6, f, skia.Paint(AntiAlias=True, Color=skia.Color(255, 90, 80) if on else skia.Color(230, 230, 230)))
        bf = skia.Font(None, sw * 0.28); bell = "\U0001F515" if on else "\U0001F514"
        bf = skia.Font(skia.Typeface("DejaVu Sans"), sw * 0.22); g = "♪"
        c.drawString(g, cx - bf.measureText(g) / 2, cy - th * 1.0, bf, skia.Paint(AntiAlias=True, Color=skia.Color(230, 230, 230)))
        if on: c.drawLine(cx - sw * 0.15, cy - th * 1.9, cx + sw * 0.15, cy - th * 0.6, skia.Paint(AntiAlias=True, Color=skia.Color(255, 90, 80), StrokeWidth=sw * 0.025))
    c.restore(); c.restore()


def tv(c, t, t_in, l):
    lt = t - t_in
    draw_asset(c, "a4_tv_blank", t_in, t, 0.03)
    r = _screen(c, "a4_tv_blank"); sw, sh = r.width(), r.height()
    c.save(); c.clipRect(r)
    off = lt > 2.6; flick = 1.8 < lt < 2.6 and int(lt * 14) % 2 == 0
    if not off and not flick:
        c.drawRect(r, skia.Paint(Color=skia.Color(18, 40, 90)))
        f = hfont("marker", sh * 0.16); s = "BREAKING NEWS"
        c.drawRect(skia.Rect.MakeXYWH(r.left(), r.top() + sh * 0.18, sw, sh * 0.22), skia.Paint(Color=skia.Color(200, 30, 40)))
        c.drawString(s, r.centerX() - f.measureText(s) / 2, r.top() + sh * 0.35, f, skia.Paint(AntiAlias=True, Color=skia.Color(255, 255, 255)))
        f2 = hfont("mono", sh * 0.11); s2 = "POWER GRID FAILING ACROSS THE REGION  •  STAY INDOORS  •  "
        x = r.right() - (lt * sw * 0.35) % (f2.measureText(s2))
        c.drawRect(skia.Rect.MakeXYWH(r.left(), r.bottom() - sh * 0.2, sw, sh * 0.2), skia.Paint(Color=skia.Color(10, 10, 14)))
        for k in range(3): c.drawString(s2, x + k * f2.measureText(s2) - f2.measureText(s2), r.bottom() - sh * 0.06, f2, skia.Paint(AntiAlias=True, Color=skia.Color(255, 220, 90)))
    elif off:
        c.drawRect(r, skia.Paint(Color=skia.Color(8, 8, 10)))
    else:
        c.drawRect(r, skia.Paint(Color=skia.Color(200, 205, 215)))
    c.restore(); c.restore()
    if off:   # the room goes dark too
        a = ease((lt - 2.6) / 0.25) * 0.72
        c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Color=skia.Color(0, 0, 8, int(255 * a))))


# ---------------- red day badge and story clock ----------------
def badge(c, t, ch, clock0, a=1.0):
    f = hfont("marker", 54); s = ch["label"]; w = f.measureText(s)
    c.save(); c.translate(52, 46); c.rotate(-2.5)
    c.drawRoundRect(skia.Rect.MakeXYWH(0, 0, w + 54, 86), 14, 14, skia.Paint(AntiAlias=True, Color=skia.Color(255, 255, 255, int(255 * a))))
    c.drawRoundRect(skia.Rect.MakeXYWH(5, 5, w + 44, 76), 11, 11, skia.Paint(AntiAlias=True, Color=skia.Color(214, 38, 38, int(255 * a))))
    c.drawString(s, 27, 66, f, skia.Paint(AntiAlias=True, Color=skia.Color(255, 255, 255, int(255 * a))))
    c.restore()
    if clock0:
        hh, mm = map(int, clock0.split(":")); mins = hh * 60 + mm + int(max(0.0, t - ch["start"]) / 2.0)
        s2 = f"{(mins // 60) % 24:02d}:{mins % 60:02d}"; f2 = hfont("mono", 46); w2 = f2.measureText(s2)
        x = 52 + w + 54 + 26
        c.drawRoundRect(skia.Rect.MakeXYWH(x, 58, w2 + 34, 64), 12, 12, skia.Paint(AntiAlias=True, Color=skia.Color(10, 12, 18, int(215 * a))))
        c.drawString(s2, x + 17, 106, f2, skia.Paint(AntiAlias=True, Color=skia.Color(255, 255, 255, int(255 * a))))
