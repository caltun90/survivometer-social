"""Cartoon layer: a flat round-headed character and lit 2.5D sets, all drawn with skia (no image generation).

Sets are drawn in a 1920x1080 world. Each set function takes (c, t, cam) where cam.par(depth) gives the
parallax offset for a layer, and returns the character's ground point and the light direction.
"""
import math
import skia

W, H = 1920, 1080
INK = 0xFF2A1B14


def C(hexs, a=1.0):
    h = hexs.lstrip("#"); return skia.Color(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), int(255 * max(0, min(1, a))))


def P(color, **kw): return skia.Paint(AntiAlias=True, Color=color, **kw)
def stroke(color, w): return skia.Paint(AntiAlias=True, Color=color, Style=skia.Paint.kStroke_Style, StrokeWidth=w, StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)


def rect(c, x, y, w, h, color, r=0):
    if r: c.drawRoundRect(skia.Rect.MakeXYWH(x, y, w, h), r, r, P(color))
    else: c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), P(color))


def poly(c, pts, color, outline=0):
    p = skia.Path(); p.moveTo(*pts[0])
    for q in pts[1:]: p.lineTo(*q)
    p.close(); c.drawPath(p, P(color))
    if outline: c.drawPath(p, stroke(INK, outline))


def vgrad(c, x, y, w, h, top, bottom, stops=None):
    p = skia.Paint(AntiAlias=True)
    cols = [top, bottom] if not isinstance(top, list) else top
    p.setShader(skia.GradientShader.MakeLinear([(x, y), (x, y + h)], cols, stops))
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), p)


def glow(c, x, y, r, hexs, a=0.6, plus=True):
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeRadial((x, y), r, [C(hexs, a), C(hexs, a * 0.35), C(hexs, 0)], [0, 0.4, 1]))
    if plus: p.setBlendMode(skia.BlendMode.kPlus)
    c.drawCircle(x, y, r, p)


def shaft(c, x0, y0, x1, y1, w0, w1, hexs, a=0.22):
    """A soft light shaft from (x0,y0) to (x1,y1)."""
    dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy); nx, ny = -dy / L, dx / L
    p = skia.Path(); p.moveTo(x0 + nx * w0, y0 + ny * w0); p.lineTo(x1 + nx * w1, y1 + ny * w1); p.lineTo(x1 - nx * w1, y1 - ny * w1); p.lineTo(x0 - nx * w0, y0 - ny * w0); p.close()
    pa = skia.Paint(AntiAlias=True); pa.setBlendMode(skia.BlendMode.kPlus)
    pa.setShader(skia.GradientShader.MakeLinear([(x0, y0), (x1, y1)], [C(hexs, a), C(hexs, 0)]))
    c.drawPath(p, pa)


def tint(c, hexs, a, mode=skia.BlendMode.kMultiply):
    p = skia.Paint(Color=C(hexs, a)); p.setBlendMode(mode); c.drawRect(skia.Rect.MakeWH(W, H), p)


def vignette(c, a=0.8):
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeRadial((W / 2, H / 2), 1200, [0x00000000, 0x00000000, skia.Color(0, 0, 0, int(255 * a))], [0, 0.5, 1]))
    c.drawRect(skia.Rect.MakeWH(W, H), p)


class Cam:
    def __init__(self, t): self.t = t; self.dx = math.sin(t * 0.21) * 26; self.dy = math.cos(t * 0.17) * 8
    def par(self, depth): return self.dx * depth, self.dy * depth * 0.5


# ------------------------------------------------------------------ character
EXPR = {  # brow tilt (inner end down = angry/determined, up = worried), eye scale, mouth kind
    "neutral": (0.0, 1.0, "flat"), "worried": (-0.35, 1.1, "wave"), "scared": (-0.5, 1.45, "open"),
    "smug": (0.25, 0.8, "smirk"), "determined": (0.45, 0.95, "flat"), "happy": (-0.1, 1.0, "smile"), "think": (0.2, 0.9, "side"),
}
POSE = {  # (left upper, left fore, right upper, right fore) arm angles in degrees, 90 = straight down
    "idle": (100, 95, 80, 85), "talk": (105, 60, 70, 20), "point": (100, 95, 20, 5), "shrug": (150, 240, 30, -60),
    "panic": (220, 260, -40, -80), "think": (100, 95, 60, -75), "hold": (110, 30, 70, 150), "cheer": (230, 265, -50, -85), "walk": (115, 100, 65, 80),
}


def character(c, x, y, s, t, pose="idle", expr="neutral", flip=False, talking=False, light="#FFD9A0", shirt="#1F8A8A", walk=False, bag=False):
    """x,y = feet; s = full body height in px."""
    c.save(); c.translate(x, y)
    if flip: c.scale(-1, 1)
    ow = max(4, s * 0.016)
    bob = math.sin(t * 2.2) * s * 0.006 + (abs(math.sin(t * 7)) * s * 0.012 if walk else 0)
    # ground shadow
    sp = skia.Paint(AntiAlias=True)
    sp.setShader(skia.GradientShader.MakeRadial((0, 0), s * 0.34, [skia.Color(0, 0, 0, 120), skia.Color(0, 0, 0, 0)]))
    c.save(); c.scale(1, 0.22); c.drawCircle(0, 0, s * 0.34, sp); c.restore()
    R = s * 0.20; hy = -s + R + bob; sh_y = hy + R * 1.02; hip_y = -s * 0.36 + bob
    # legs
    sw = math.sin(t * 7) * s * 0.07 if walk else 0
    for i, lx in enumerate((-s * 0.065, s * 0.065)):
        fx = lx + (sw if i == 0 else -sw)
        c.drawLine(lx, hip_y, fx, -s * 0.03, stroke(INK, s * 0.085 + ow * 2)); c.drawLine(lx, hip_y, fx, -s * 0.03, stroke(C("#2B3350"), s * 0.085))
        c.drawRoundRect(skia.Rect.MakeXYWH(fx - s * 0.05, -s * 0.05, s * 0.13, s * 0.05), s * 0.02, s * 0.02, P(INK))
    if bag:
        c.drawRoundRect(skia.Rect.MakeXYWH(-s * 0.21, sh_y + s * 0.02, s * 0.16, s * 0.26), s * 0.04, s * 0.04, P(INK))
        c.drawRoundRect(skia.Rect.MakeXYWH(-s * 0.21 + ow, sh_y + s * 0.02 + ow, s * 0.16 - 2 * ow, s * 0.26 - 2 * ow), s * 0.03, s * 0.03, P(C("#8A5A2B")))
    # torso
    tw = s * 0.27; body = skia.Path()
    body.moveTo(-tw * 0.42, sh_y); body.lineTo(tw * 0.42, sh_y); body.lineTo(tw * 0.5, hip_y + s * 0.03); body.lineTo(-tw * 0.5, hip_y + s * 0.03); body.close()
    c.drawPath(body, stroke(INK, ow * 2 + s * 0.03)); c.drawPath(body, stroke(C(shirt), s * 0.03)); c.drawPath(body, P(C(shirt)))
    hl = skia.Paint(AntiAlias=True); hl.setBlendMode(skia.BlendMode.kPlus)
    hl.setShader(skia.GradientShader.MakeLinear([(tw * 0.5, 0), (-tw * 0.2, 0)], [C(light, 0.35), C(light, 0)])); c.drawPath(body, hl)
    # arms
    la, lf, ra, rf = POSE.get(pose, POSE["idle"]); sway = math.sin(t * 3.1) * (10 if talking else 3)
    for side, (ua, fa) in ((-1, (la, lf)), (1, (ra + sway, rf + sway * 1.5))):
        sx = side * tw * 0.44; L1 = s * 0.15; L2 = s * 0.14
        a1 = math.radians(ua); ex, ey = sx + math.cos(a1) * L1, sh_y + s * 0.03 + math.sin(a1) * L1
        a2 = math.radians(fa); hx, hy2 = ex + math.cos(a2) * L2, ey + math.sin(a2) * L2
        for col, wd in ((INK, s * 0.062 + ow * 2), (C(shirt), s * 0.062)):
            c.drawLine(sx, sh_y + s * 0.03, ex, ey, stroke(col, wd)); c.drawLine(ex, ey, hx, hy2, stroke(col, wd))
        c.drawCircle(hx, hy2, s * 0.038 + ow, P(INK)); c.drawCircle(hx, hy2, s * 0.038, P(C("#F6EFE4")))
    # head
    c.drawCircle(0, hy, R + ow, P(INK)); c.drawCircle(0, hy, R, P(C("#F6EFE4")))
    rim = skia.Paint(AntiAlias=True); rim.setBlendMode(skia.BlendMode.kPlus)
    rim.setShader(skia.GradientShader.MakeRadial((R * 0.75, hy - R * 0.5), R * 1.3, [C(light, 0.5), C(light, 0)])); c.drawCircle(0, hy, R, rim)
    shd = skia.Paint(AntiAlias=True); shd.setShader(skia.GradientShader.MakeRadial((-R * 0.9, hy + R * 0.7), R * 1.4, [skia.Color(40, 30, 60, 90), skia.Color(40, 30, 60, 0)])); c.drawCircle(0, hy, R, shd)
    bt, es, mk = EXPR.get(expr, EXPR["neutral"])
    blink = 0.12 if (t % 3.7) < 0.12 else 1.0
    for side in (-1, 1):
        ex = side * R * 0.36 + R * 0.08; ey = hy - R * 0.08
        c.save(); c.translate(ex, ey); c.scale(1, blink); c.drawCircle(0, 0, R * 0.085 * es, P(INK)); c.restore()
        bx0, bx1 = ex - side * R * 0.20, ex + side * R * 0.20   # inner, outer
        c.drawLine(bx0, ey - R * 0.30 + bt * R * 0.16, bx1, ey - R * 0.30 - bt * R * 0.16, stroke(INK, R * 0.075))
    mx, my = R * 0.08, hy + R * 0.42; m = stroke(INK, R * 0.075)
    op = (0.5 + 0.5 * math.sin(t * 17)) if talking else 0
    if mk == "open" or (talking and op > 0.35):
        hh = R * (0.20 if mk == "open" else 0.10 + 0.10 * op)
        c.drawOval(skia.Rect.MakeXYWH(mx - R * 0.16, my - hh / 2, R * 0.32, hh + R * 0.04), P(INK))
    elif mk == "smile":
        p = skia.Path(); p.moveTo(mx - R * 0.26, my - R * 0.04); p.quadTo(mx, my + R * 0.2, mx + R * 0.26, my - R * 0.04); c.drawPath(p, m)
    elif mk == "smirk":
        p = skia.Path(); p.moveTo(mx - R * 0.22, my + R * 0.02); p.quadTo(mx + R * 0.05, my + R * 0.1, mx + R * 0.26, my - R * 0.1); c.drawPath(p, m)
    elif mk == "wave":
        p = skia.Path(); p.moveTo(mx - R * 0.24, my); p.quadTo(mx - R * 0.12, my - R * 0.1, mx, my); p.quadTo(mx + R * 0.12, my + R * 0.1, mx + R * 0.24, my); c.drawPath(p, m)
    elif mk == "side":
        c.drawLine(mx, my, mx + R * 0.26, my - R * 0.05, m)
    else:
        c.drawLine(mx - R * 0.2, my, mx + R * 0.2, my, m)
    c.restore()


def walker(c, x, y, s, t, a=0.85):
    """Distant shambling silhouette."""
    col = skia.Color(18, 14, 26, int(255 * a)); sw = math.sin(t * 2.4 + x) * s * 0.05
    c.drawCircle(x + sw * 0.4, y - s * 0.86, s * 0.11, P(col))
    c.drawLine(x + sw * 0.3, y - s * 0.76, x, y - s * 0.38, stroke(col, s * 0.16))
    c.drawLine(x, y - s * 0.38, x - s * 0.08 + sw, y, stroke(col, s * 0.07)); c.drawLine(x, y - s * 0.38, x + s * 0.08 - sw, y, stroke(col, s * 0.07))
    c.drawLine(x, y - s * 0.7, x + s * 0.3, y - s * 0.62 + sw, stroke(col, s * 0.06)); c.drawLine(x, y - s * 0.68, x + s * 0.27, y - s * 0.52 - sw, stroke(col, s * 0.06))


# ------------------------------------------------------------------ set pieces
def skyline(c, ox, base, seed, col, lit=None, hmin=160, hmax=420, step=110, t=0, lit_ratio=0.5):
    x = -200 + ox; i = 0
    while x < W + 200:
        k = (seed * 7919 + i * 104729) % 1000 / 1000
        w = step * (0.7 + 0.6 * ((seed * 31 + i * 17) % 100) / 100); h = hmin + (hmax - hmin) * k
        rect(c, x, base - h, w - 6, h + 400, col)
        if lit:
            for wy in range(int(base - h + 24), int(base - 10), 46):
                for wx in range(int(x + 14), int(x + w - 30), 34):
                    r = ((wx * 13 + wy * 7 + seed) % 100) / 100
                    if r < lit_ratio: rect(c, wx, wy, 16, 24, C(lit, 0.55 + 0.35 * r))
        x += w; i += 1


def window(c, x, y, w, h, sky_top, sky_bot, frame="#3A2A22", t=0, draw=None):
    rect(c, x - 14, y - 14, w + 28, h + 28, C(frame), 6)
    c.save(); c.clipRect(skia.Rect.MakeXYWH(x, y, w, h)); vgrad(c, x, y, w, h, C(sky_top), C(sky_bot))
    if draw: draw()
    c.restore()
    rect(c, x + w / 2 - 6, y, 12, h, C(frame)); rect(c, x, y + h / 2 - 6, w, 12, C(frame))


def set_bedroom(c, t, cam):
    """HOUR 0: bedroom at sunrise, a TV warning, figures far outside."""
    vgrad(c, 0, 0, W, H, C("#3B2B4F"), C("#5A3550"))
    bx, by = cam.par(0.3)
    def outside():
        glow(c, 420 + bx, 520 + by, 420, "#FFB060", 0.9, plus=False)
        skyline(c, bx * 2, 640 + by, 3, C("#2A1E38"), hmin=60, hmax=220, step=80)
        for i, wx in enumerate((300, 380, 520)): walker(c, wx + bx * 2 + (t * 6) % 40, 660 + by, 70, t + i)
    window(c, 180 + bx, 170 + by, 520, 470, "#FF9A5A", "#FFD9A0", t=t, draw=outside)
    shaft(c, 440 + bx, 400, 1150, 1040, 230, 520, "#FFB060", 0.20)
    fx, fy = cam.par(0.6)
    rect(c, 0, 790 + fy, W, 400, C("#3A2538")); vgrad(c, 0, 790 + fy, W, 60, C("#000000", 0.35), C("#000000", 0))
    rect(c, 1080 + fx, 590 + fy, 640, 230, C("#6B3F4F"), 26); rect(c, 1080 + fx, 690 + fy, 640, 150, C("#8A4E5E"), 20)
    rect(c, 1560 + fx, 560 + fy, 190, 110, C("#F1E4D2"), 30); rect(c, 1620 + fx, 420 + fy, 150, 420, C("#4A2C3C"), 14)
    rect(c, 800 + fx, 420 + fy, 250, 160, C("#1B1420"), 12); rect(c, 812 + fx, 432 + fy, 226, 136, C("#B3261E", 0.75 + 0.2 * math.sin(t * 6)), 6)
    rect(c, 850 + fx, 486 + fy, 150, 26, C("#FFFFFF", 0.9), 4); rect(c, 905 + fx, 580 + fy, 40, 40, C("#1B1420")); rect(c, 760 + fx, 620 + fy, 330, 190, C("#4A2C3C"), 10)
    glow(c, 925 + fx, 500 + fy, 330, "#FF3B2E", 0.22 + 0.06 * math.sin(t * 6))
    return dict(x=560, y=930, s=560, light="#FFB060", amb=("#6A4A7A", 0.10))


def set_street(c, t, cam):
    """HOUR 1: a jammed street at golden hour."""
    vgrad(c, 0, 0, W, H, C("#F28B3B"), C("#FFD08A")); glow(c, 1500, 330, 520, "#FFF0C0", 0.9, plus=False)
    ax, ay = cam.par(0.15); skyline(c, ax, 640 + ay, 5, C("#B5603A"), hmin=180, hmax=420)
    bx, by = cam.par(0.35); skyline(c, bx, 700 + by, 11, C("#7C3B33"), lit="#FFE6A8", hmin=240, hmax=520, step=170, lit_ratio=0.25)
    rx, ry = cam.par(0.7)
    rect(c, 0, 740 + ry, W, 400, C("#3B3040")); rect(c, 0, 730 + ry, W, 16, C("#55465A"))
    for i in range(8): rect(c, -100 + i * 280 + rx, 905 + ry, 150, 12, C("#E8D9B8", 0.5))
    cols = ["#D8433B", "#3C7FBF", "#E6B93A", "#5FA36A", "#C9C4C0", "#7A5AA8", "#D8433B", "#3C7FBF", "#E6B93A"]
    for i, col in enumerate(cols):
        x = -80 + i * 235 + rx + math.sin(t * 1.3 + i) * 3; y = 800 + ry + (i % 2) * 16
        rect(c, x, y, 205, 62, C(col), 16); rect(c, x + 38, y - 44, 125, 52, C(col), 16); rect(c, x + 50, y - 36, 100, 34, C("#22262E", 0.85), 8)
        for wx in (x + 42, x + 160): c.drawCircle(wx, y + 64, 22, P(INK))
        glow(c, x + 6, y + 30, 60, "#FF3020", 0.5 + 0.2 * math.sin(t * 4 + i))
    shaft(c, 1500, 330, 500, 1080, 120, 620, "#FFE0A0", 0.14)
    return dict(x=520, y=1000, s=520, light="#FFD08A", amb=("#FF9A4A", 0.10))


def set_apartment(c, t, cam):
    """HOUR 6: living room at dusk, city in the window."""
    vgrad(c, 0, 0, W, H, C("#2E2F4F"), C("#3B3355"))
    bx, by = cam.par(0.3)
    def outside():
        glow(c, 1300 + bx, 640 + by, 500, "#FF7A4A", 0.8, plus=False)
        skyline(c, bx * 2, 690 + by, 21, C("#1C1830"), lit="#FFD27A", hmin=120, hmax=360, step=120, lit_ratio=0.45)
    window(c, 980 + bx, 150 + by, 760, 520, "#3A3F7A", "#E0705A", frame="#24202E", draw=outside)
    fx, fy = cam.par(0.6)
    rect(c, 0, 800 + fy, W, 400, C("#2A2238")); vgrad(c, 0, 800 + fy, W, 70, C("#000000", 0.35), C("#000000", 0))
    rect(c, 1060 + fx, 640 + fy, 640, 200, C("#5A4A7A"), 30); rect(c, 1030 + fx, 600 + fy, 110, 250, C("#6A5890"), 30); rect(c, 1620 + fx, 600 + fy, 110, 250, C("#6A5890"), 30)
    rect(c, 200 + fx, 380 + fy, 26, 440, C("#1B1826")); poly(c, [(140 + fx, 380 + fy), (286 + fx, 380 + fy), (256 + fx, 290 + fy), (170 + fx, 290 + fy)], C("#F2C36B"))
    glow(c, 213 + fx, 400 + fy, 520, "#FFC870", 0.42); shaft(c, 213 + fx, 390 + fy, 213 + fx, 1000, 80, 420, "#FFC870", 0.16)
    rect(c, 330 + fx, 700 + fy, 260, 20, C("#3A2E48"), 6); rect(c, 350 + fx, 720 + fy, 16, 110, C("#3A2E48")); rect(c, 555 + fx, 720 + fy, 16, 110, C("#3A2E48"))
    for i in range(4): rect(c, 350 + i * 60 + fx, 640 + fy, 40, 60, C("#7FC8E8", 0.85), 8)   # water containers
    return dict(x=760, y=960, s=540, light="#FFC870", amb=("#5A5AA0", 0.14))


def set_blackout(c, t, cam):
    """DAY 1: rooftop view of a dark city under the moon."""
    vgrad(c, 0, 0, W, H, C("#0B1026"), C("#1B2A52")); glow(c, 1480, 250, 420, "#9FC2FF", 0.55, plus=False); c.drawCircle(1480, 250, 74, P(C("#EAF2FF")))
    for i in range(70):
        sx = (i * 733) % W; sy = (i * 379) % 520; c.drawCircle(sx, sy, 1.6 + (i % 3) * 0.6, P(C("#FFFFFF", 0.35 + 0.3 * math.sin(t * 1.5 + i))))
    ax, ay = cam.par(0.15); skyline(c, ax, 700 + ay, 9, C("#1C2850"), hmin=160, hmax=420)
    bx, by = cam.par(0.35); skyline(c, bx, 780 + by, 15, C("#141C3A"), lit="#FFB648", hmin=220, hmax=520, step=160, lit_ratio=0.02)
    fx, fy = cam.par(0.7)
    rect(c, 0, 880 + fy, W, 300, C("#151A2E")); rect(c, 0, 850 + fy, W, 40, C("#20284A"))
    rect(c, 1400 + fx, 700 + fy, 170, 160, C("#1B2140")); rect(c, 1445 + fx, 610 + fy, 16, 100, C("#1B2140"))
    shaft(c, 1480, 250, 700, 1080, 90, 520, "#9FC2FF", 0.10)
    glow(c, 640, 620, 520, "#6F8FD8", 0.30)
    return dict(x=640, y=900, s=520, light="#BBD4FF", amb=("#25336B", 0.12))


def set_store(c, t, cam):
    """DAY 3: an empty supermarket aisle."""
    vgrad(c, 0, 0, W, H, C("#3B4A4F"), C("#55676B"))
    fl = 0.75 + 0.25 * (1 if math.sin(t * 23) > -0.86 else 0.2)
    bx, by = cam.par(0.35)
    for sx in (120, 1240):
        rect(c, sx + bx, 250 + by, 560, 560, C("#2E3A40"), 8)
        for r in range(4):
            y = 290 + r * 132 + by; rect(c, sx + 14 + bx, y + 96, 532, 14, C("#8A979A"))
            for k in range(3):
                if (sx + r * 7 + k * 3) % 5 == 0: rect(c, sx + 60 + k * 150 + bx, y + 40, 46, 56, C(["#D8433B", "#E6B93A", "#5FA36A"][k]), 6)
    rect(c, 700 + bx * 0.6, 150 + by, 520, 520, C("#2A3338")); vgrad(c, 700 + bx * 0.6, 150 + by, 520, 520, C("#101518", 0.6), C("#101518", 0.1))
    fx, fy = cam.par(0.7)
    rect(c, 0, 800 + fy, W, 400, C("#6F7F80")); vgrad(c, 0, 800 + fy, W, 90, C("#000000", 0.35), C("#000000", 0))
    for i in range(7): rect(c, i * 300 + fx, 800 + fy, 3, 400, C("#55676B"))
    for lx in (420, 960, 1500):
        rect(c, lx - 130, 60, 260, 22, C("#E8F4F2", fl)); glow(c, lx, 90, 520, "#CFEFE8", 0.26 * fl); shaft(c, lx, 80, lx, 950, 120, 360, "#CFEFE8", 0.07 * fl)
    rect(c, 1280 + fx, 720 + fy, 200, 110, C("#9AA7A8"), 8); c.drawCircle(1310 + fx, 850 + fy, 16, P(INK)); c.drawCircle(1450 + fx, 850 + fy, 16, P(INK)); rect(c, 1470 + fx, 660 + fy, 14, 120, C("#9AA7A8"))
    return dict(x=880, y=980, s=540, light="#CFEFE8", amb=("#3B5A5F", 0.16))


def hills(c, ox, base, amp, col, seed):
    p = skia.Path(); p.moveTo(-200, H + 200); x = -200
    while x <= W + 200:
        p.lineTo(x + ox, base - amp * (0.5 + 0.5 * math.sin(x * 0.0031 + seed) * math.cos(x * 0.0017 + seed * 2))); x += 40
    p.lineTo(W + 200, H + 200); p.close(); c.drawPath(p, P(col))


def set_road(c, t, cam):
    """WEEK 1: the road out of the city at dawn."""
    vgrad(c, 0, 0, W, H, C("#5B4B8A"), C("#FFB37A")); glow(c, 1320, 600, 600, "#FFE2A8", 0.95, plus=False)
    ax, ay = cam.par(0.1); skyline(c, ax + 200, 640 + ay, 4, C("#6B5590"), hmin=40, hmax=200, step=70)
    for i in range(3): glow(c, 300 + i * 150 + ax, 470 - i * 30, 120, "#3A2E48", 0.35, plus=False)
    hills(c, cam.par(0.25)[0], 690, 110, C("#7A5A8A"), 1.0); hills(c, cam.par(0.45)[0], 780, 120, C("#4E6B5A"), 2.3)
    fx, fy = cam.par(0.7); hills(c, fx, 900, 60, C("#3E5A45"), 4.1)
    poly(c, [(820 + fx, 1090), (1250 + fx, 1090), (1150 + fx, 760), (1110 + fx, 760)], C("#5A4E58")); poly(c, [(1025 + fx, 1090), (1050 + fx, 1090), (1132 + fx, 760), (1128 + fx, 760)], C("#E8D9B8", 0.6))
    for tx, th in ((260, 300), (1560, 360), (1740, 260)):
        rect(c, tx + fx, 900 - th * 0.4 + fy, 22, th * 0.5, C("#3A2A22")); c.drawCircle(tx + 11 + fx, 900 - th * 0.55 + fy, th * 0.3, P(C("#2F4A3A"))); c.drawCircle(tx + 60 + fx, 900 - th * 0.42 + fy, th * 0.22, P(C("#35543F")))
    shaft(c, 1320, 600, 300, 1080, 100, 700, "#FFD9A0", 0.16)
    return dict(x=620, y=1010, s=500, light="#FFD9A0", amb=("#FF9A6A", 0.10), bag=True)


def set_camp(c, t, cam):
    """MONTH 1: riverside camp at blue hour with a fire."""
    vgrad(c, 0, 0, W, H, C("#16284A"), C("#3D6B8A")); glow(c, 400, 260, 300, "#BFD8FF", 0.4, plus=False); c.drawCircle(400, 260, 46, P(C("#EAF2FF")))
    hills(c, cam.par(0.2)[0], 640, 150, C("#1F3A55"), 0.7); hills(c, cam.par(0.4)[0], 730, 90, C("#1A3040"), 3.3)
    rx, ry = cam.par(0.5); vgrad(c, 0, 760 + ry, W, 130, C("#5FA3C8", 0.8), C("#2A5A7A", 0.9))
    for i in range(9): rect(c, (i * 240 + t * 30) % (W + 200) - 100, 790 + (i % 4) * 26 + ry, 120, 5, C("#CFEFFF", 0.35), 3)
    fx, fy = cam.par(0.75); rect(c, 0, 880 + fy, W, 300, C("#1E3327"))
    for tx in (1280, 1500):
        poly(c, [(tx + fx, 900 + fy), (tx + 110 + fx, 700 + fy), (tx + 220 + fx, 900 + fy)], C("#C96A3A")); poly(c, [(tx + 90 + fx, 900 + fy), (tx + 110 + fx, 760 + fy), (tx + 130 + fx, 900 + fy)], C("#3A2018"))
    for gx in range(160, 520, 60): rect(c, gx + fx, 900 + fy, 44, 14, C("#3A2A22"), 4); c.drawCircle(gx + 22 + fx, 892 + fy, 14, P(C("#5FA36A")))
    cx0, cy0 = 980 + fx, 930 + fy; fl = 1 + 0.12 * math.sin(t * 11) + 0.08 * math.sin(t * 17)
    glow(c, cx0, cy0 - 30, 560 * fl, "#FF9A3A", 0.42)
    for w, h, col in ((70, 130, "#FF7A2A"), (46, 92, "#FFC24A"), (24, 54, "#FFF0B0")):
        poly(c, [(cx0 - w / 2, cy0), (cx0 + math.sin(t * 9) * 8, cy0 - h * fl), (cx0 + w / 2, cy0)], C(col))
    rect(c, cx0 - 70, cy0 - 6, 140, 18, C("#3A2A22"), 8)
    return dict(x=700, y=1000, s=500, light="#FF9A3A", amb=("#2A4A7A", 0.22), bag=False)


def set_farm(c, t, cam):
    """YEAR 1: a small community in the first snow."""
    vgrad(c, 0, 0, W, H, C("#8FB3D9"), C("#F6D9C4")); glow(c, 1500, 420, 560, "#FFF3D6", 0.85, plus=False)
    hills(c, cam.par(0.2)[0], 640, 130, C("#C9D8EA"), 1.7); hills(c, cam.par(0.4)[0], 740, 90, C("#E6EEF7"), 2.9)
    bx, by = cam.par(0.5)
    for hx, col in ((1120, "#8A4E3A"), (1420, "#6B5A7A")):
        rect(c, hx + bx, 620 + by, 230, 170, C(col)); poly(c, [(hx - 24 + bx, 624 + by), (hx + 115 + bx, 520 + by), (hx + 254 + bx, 624 + by)], C("#F4F7FB"))
        rect(c, hx + 40 + bx, 680 + by, 54, 54, C("#FFD27A")); glow(c, hx + 67 + bx, 707 + by, 120, "#FFC870", 0.45); rect(c, hx + 150 + bx, 690 + by, 50, 100, C("#3A2A22"))
    poly(c, [(820 + bx, 700 + by), (1010 + bx, 660 + by), (1010 + bx, 700 + by), (820 + bx, 740 + by)], C("#24406B")); rect(c, 900 + bx, 720 + by, 12, 70, C("#55606B"))
    fx, fy = cam.par(0.75); rect(c, 0, 800 + fy, W, 400, C("#F4F7FB")); vgrad(c, 0, 800 + fy, W, 200, C("#B7C9E0", 0.5), C("#B7C9E0", 0))
    for i in range(6): rect(c, 180 + i * 90 + fx, 840 + fy, 12, 70, C("#6B4A32"));
    rect(c, 170 + fx, 860 + fy, 480, 10, C("#6B4A32"))
    for i in range(60):
        sx = (i * 547 + t * (20 + i % 5 * 6)) % W; sy = (i * 211 + t * (60 + i % 7 * 12)) % H; c.drawCircle(sx, sy, 2.5 + i % 3, P(C("#FFFFFF", 0.8)))
    shaft(c, 1500, 420, 500, 1080, 110, 640, "#FFF3D6", 0.12)
    return dict(x=640, y=980, s=520, light="#FFF3D6", amb=("#9FB8D8", 0.06), bag=False)


SETS = [set_bedroom, set_street, set_apartment, set_blackout, set_store, set_road, set_camp, set_farm]
