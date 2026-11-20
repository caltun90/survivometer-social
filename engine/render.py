"""Render: timeline.json + voice/final.wav -> video.

  python3 engine/render.py <episode_dir> frames 0 0.5 1.0 1.9 30 ...   -> chk/f_<t>.jpg (frame check)
  python3 engine/render.py <episode_dir> seg <t0> <t1> <out.mp4>        -> silent segment
  python3 engine/render.py <episode_dir> join <out.mp4> <seg1> <seg2>.. -> segments + audio
"""
import sys, os, json, math, subprocess
import numpy as np, skia
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import toon
import fx

W, H, FPS = 1920, 1080, 30
FD = "/usr/share/fonts/opentype/inter/"
TF = {k: skia.Typeface.MakeFromFile(p) for k, p in dict(
    black=FD + "InterDisplay-Black.otf", bold=FD + "Inter-Bold.otf", semi=FD + "Inter-SemiBold.otf",
    sym="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf").items()}
BG = 0xFF06080C
GLYPH = {"bolt": "⚡", "cross": "✚", "warn": "⚠", "house": "⌂", "snow": "❄", "bio": "☣"}


def col(hexs, a=1.0):
    h = hexs.lstrip("#"); return skia.Color(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), int(255 * max(0, min(1, a))))


def ease(x): x = max(0.0, min(1.0, x)); return 1 - (1 - x) ** 3
def font(k, size): return skia.Font(TF[k], size)


def fit(text, k, size, maxw):
    f = font(k, size); w = f.measureText(text)
    if w > maxw: size = size * maxw / w; f = font(k, size)
    return f, f.measureText(text), size


def text(c, s, x, y, k, size, color, maxw=None, align="c"):
    f, w, size = fit(s, k, size, maxw or 1e9)
    p = skia.Paint(AntiAlias=True, Color=color)
    c.drawString(s, x - (w / 2 if align == "c" else w if align == "r" else 0), y, f, p)
    return w, size


class Ep:
    def __init__(self, ep):
        self.ep = ep
        T = json.load(open(os.path.join(ep, "timeline.json")))
        self.T, self.total, self.lines, self.ch = T, T["total"], T["lines"], T["chapters"]
        self.odds = [(0.0, T["start_odds"])] + [(l["start"] + 0.35, l["visual"][1]) for l in self.lines if l["visual"][0] == "odds"]
        self.caps = []
        for l in self.lines:
            words, parts, cur = l["text"].split(), [], ""
            for w in words:
                if cur and (len(cur) + 1 + len(w) > 44 or (cur[-1] in ".?!" and len(cur) > 14)):
                    parts.append(cur); cur = w
                else:
                    cur = (cur + " " + w).strip()
            if cur: parts.append(cur)
            tot = sum(len(p) for p in parts); t = l["start"]; d = l["end"] - l["start"]
            for p in parts:
                e = t + d * len(p) / tot; self.caps.append((t, e, p)); t = e

    def odds_at(self, t):
        v = self.odds[0][1]
        for (tk, val) in self.odds[1:]:
            if t >= tk: v0 = v; v = v0 + (val - v0) * ease((t - tk) / 0.9)
        return v

    # ---------- pieces ----------
    def bg(self, c, t, accent):
        c.clear(BG)
        cx, cy = W * 0.5 + 70 * math.sin(t * 0.13), H * 0.47 + 30 * math.cos(t * 0.11)
        p = skia.Paint(AntiAlias=True)
        p.setShader(skia.GradientShader.MakeRadial((cx, cy), 980, [col(accent, 0.20 + 0.03 * math.sin(t * 0.9)), col(accent, 0.0)]))
        c.drawRect(skia.Rect.MakeWH(W, H), p)
        g = skia.Paint(Color=skia.Color(255, 255, 255, 11), StrokeWidth=1)
        off = (t * 9) % 120
        for x in range(-120, W + 120, 120): c.drawLine(x + off, 0, x + off, H, g)
        for y in range(-120, H + 120, 120): c.drawLine(0, y + off * 0.5, W, y + off * 0.5, g)
        v = skia.Paint(AntiAlias=True)
        v.setShader(skia.GradientShader.MakeRadial((W / 2, H / 2), 1250, [0x00000000, 0x00000000, 0xC8000000], [0, 0.55, 1]))
        c.drawRect(skia.Rect.MakeWH(W, H), v)

    def gauge(self, c, cx, cy, r, value, accent, big=False):
        sw = r * 0.16
        segs = [(0, 33, "#FF3B3B"), (33, 66, "#FFB020"), (66, 100, "#22D37A")]
        oval = skia.Rect.MakeLTRB(cx - r, cy - r, cx + r, cy + r)
        for a, b, hx in segs:
            p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=sw, Color=col(hx, 0.95))
            c.drawArc(oval, 180 + a * 1.8 + 1.2, (b - a) * 1.8 - 2.4, False, p)
        ang = math.radians(180 + value * 1.8)
        nx, ny = cx + math.cos(ang) * r * 0.86, cy + math.sin(ang) * r * 0.86
        c.drawLine(cx, cy, nx, ny, skia.Paint(AntiAlias=True, Color=0xFFFFFFFF, StrokeWidth=r * 0.055, StrokeCap=skia.Paint.kRound_Cap))
        c.drawCircle(cx, cy, r * 0.09, skia.Paint(AntiAlias=True, Color=0xFFFFFFFF))
        hx = segs[0][2] if value < 33 else segs[1][2] if value < 66 else segs[2][2]
        if big:
            text(c, f"{round(value)}%", cx, cy + r * 0.62, "black", r * 0.52, col(hx))
        else:
            text(c, f"{round(value)}%", cx, cy + r * 0.50, "black", r * 0.42, 0xFFFFFFFF)
            text(c, "SURVIVAL ODDS", cx, cy + r * 0.74, "bold", r * 0.155, col("#FFFFFF", 0.72))

    def icon(self, c, key, cx, cy, s, accent, a):
        if key in GLYPH:
            text(c, GLYPH[key], cx, cy + s * 0.36, "sym", s, col(accent, a)); return
        p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=s * 0.075, Color=col(accent, a),
                       StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)
        f = skia.Paint(AntiAlias=True, Color=col(accent, a))
        u = s / 2
        if key == "drop":
            path = skia.Path(); path.moveTo(cx, cy - u); path.cubicTo(cx + u * 1.1, cy + u * 0.1, cx + u * 0.75, cy + u, cx, cy + u)
            path.cubicTo(cx - u * 0.75, cy + u, cx - u * 1.1, cy + u * 0.1, cx, cy - u); c.drawPath(path, p)
        elif key == "phone":
            c.drawRoundRect(skia.Rect.MakeLTRB(cx - u * 0.5, cy - u, cx + u * 0.5, cy + u), u * 0.14, u * 0.14, p)
            for i, hh in enumerate((0.25, 0.45, 0.65)):
                x = cx - u * 0.22 + i * u * 0.22; c.drawLine(x, cy + u * 0.3, x, cy + u * 0.3 - u * hh, p)
        elif key == "car":
            c.drawRoundRect(skia.Rect.MakeLTRB(cx - u * 1.2, cy - u * 0.1, cx + u * 1.2, cy + u * 0.5), u * 0.15, u * 0.15, p)
            path = skia.Path(); path.moveTo(cx - u * 0.7, cy - u * 0.1); path.lineTo(cx - u * 0.4, cy - u * 0.65)
            path.lineTo(cx + u * 0.4, cy - u * 0.65); path.lineTo(cx + u * 0.75, cy - u * 0.1); c.drawPath(path, p)
            for dx in (-0.65, 0.65): c.drawCircle(cx + u * dx, cy + u * 0.55, u * 0.26, f)
        elif key == "map":
            path = skia.Path(); pts = [(-1.1, -0.6), (-0.37, -0.85), (0.37, -0.6), (1.1, -0.85), (1.1, 0.6), (0.37, 0.85), (-0.37, 0.6), (-1.1, 0.85)]
            path.moveTo(cx + pts[0][0] * u, cy + pts[0][1] * u)
            for x, y in pts[1:]: path.lineTo(cx + x * u, cy + y * u)
            path.close(); c.drawPath(path, p)
            c.drawLine(cx - u * 0.37, cy - u * 0.85, cx - u * 0.37, cy + u * 0.6, p); c.drawLine(cx + u * 0.37, cy - u * 0.6, cx + u * 0.37, cy + u * 0.85, p)
        elif key == "cart":
            path = skia.Path(); path.moveTo(cx - u * 1.2, cy - u * 0.8); path.lineTo(cx - u * 0.8, cy - u * 0.8); path.lineTo(cx - u * 0.45, cy + u * 0.35)
            path.lineTo(cx + u * 0.8, cy + u * 0.35); path.lineTo(cx + u * 1.05, cy - u * 0.45); path.lineTo(cx - u * 0.7, cy - u * 0.45); c.drawPath(path, p)
            for dx in (-0.3, 0.65): c.drawCircle(cx + u * dx, cy + u * 0.75, u * 0.16, f)
        elif key == "fire":
            path = skia.Path(); path.moveTo(cx, cy - u); path.cubicTo(cx + u * 0.2, cy - u * 0.3, cx + u * 0.9, cy - u * 0.1, cx + u * 0.65, cy + u * 0.55)
            path.cubicTo(cx + u * 0.45, cy + u * 1.05, cx - u * 0.45, cy + u * 1.05, cx - u * 0.65, cy + u * 0.55)
            path.cubicTo(cx - u * 0.85, cy, cx - u * 0.3, cy - u * 0.2, cx, cy - u); c.drawPath(path, p)
        elif key == "bike":
            for dx in (-0.8, 0.8): c.drawCircle(cx + u * dx, cy + u * 0.35, u * 0.5, p)
            path = skia.Path(); path.moveTo(cx - u * 0.8, cy + u * 0.35); path.lineTo(cx - u * 0.25, cy - u * 0.45); path.lineTo(cx + u * 0.45, cy - u * 0.45)
            path.lineTo(cx + u * 0.8, cy + u * 0.35); path.moveTo(cx - u * 0.25, cy - u * 0.45); path.lineTo(cx + u * 0.05, cy + u * 0.35)
            path.lineTo(cx - u * 0.8, cy + u * 0.35); path.moveTo(cx + u * 0.05, cy + u * 0.35); path.lineTo(cx + u * 0.45, cy - u * 0.45)
            path.moveTo(cx - u * 0.4, cy - u * 0.62); path.lineTo(cx - u * 0.1, cy - u * 0.62); c.drawPath(path, p)

    def visual(self, c, t, l, accent):
        v = l["visual"]; kind = v[0]; lt = t - l["start"]; dur = max(0.5, l["end"] - l["start"])
        a = ease(lt / 0.30); dy = (1 - a) * 46; cx, cy = W / 2, H * 0.47
        c.save(); z = 1 + 0.03 * min(1.0, lt / 6); c.translate(cx, cy); c.scale(z, z); c.translate(-cx, -cy)
        white = col("#FFFFFF", a)
        if kind == "hook":
            zz = 1.32 - 0.32 * ease(lt / 0.55) + 0.02 * lt
            c.translate(cx, cy); c.scale(zz, zz); c.translate(-cx, -cy)
            text(c, GLYPH["bio"], cx, cy + 250, "sym", 760, col(accent, 0.20 + 0.06 * math.sin(lt * 9)))
            words = v[1].split(); mid = (len(words) + 1) // 2
            text(c, " ".join(words[:mid]), cx, cy - 20, "black", 215, 0xFFFFFFFF, 1700)
            text(c, " ".join(words[mid:]), cx, cy + 190, "black", 215, col(accent), 1700)
        elif kind == "big":
            _, sz = text(c, v[1], cx, cy + 40 + dy, "black", 250, white, 1560)
            if len(v) > 2 and v[2]: text(c, v[2], cx, cy + 40 + sz * 0.62 + dy, "bold", 62, col(accent, a), 1500)
        elif kind == "card":
            _, sz = text(c, v[1], cx, cy + 20 + dy, "black", 330, col(accent, a), 1500)
            text(c, v[2], cx, cy + 20 + sz * 0.42 + dy, "bold", 66, white, 1560)
            if len(v) > 3 and v[3]: text(c, v[3], cx, H - 215, "semi", 30, col("#FFFFFF", 0.55 * a))
        elif kind == "icon":
            self.icon(c, v[1], cx, cy - 90 + dy, 330, accent, a)
            text(c, v[2], cx, cy + 250 + dy, "black", 120, white, 1500)
        elif kind == "list":
            items = v[1]; n = len(items); gap = 138 if n <= 3 else 118; size = 104 if n <= 3 else 90
            y0 = cy - (n - 1) * gap / 2 + 36
            for i, it in enumerate(items):
                ai = ease((lt - i * dur * 0.8 / n) / 0.28)
                if ai <= 0: continue
                f, w, s2 = fit(it, "black", size, getattr(self, "_listw", 1400)); x0 = cx - w / 2
                c.drawRoundRect(skia.Rect.MakeXYWH(x0 - 46 - (1 - ai) * 40, y0 + i * gap - s2 * 0.72, 16, s2 * 0.78), 6, 6, skia.Paint(AntiAlias=True, Color=col(accent, ai)))
                c.drawString(it, x0 - (1 - ai) * 40, y0 + i * gap, f, skia.Paint(AntiAlias=True, Color=col("#FFFFFF", ai)))
        elif kind == "choice":
            text(c, "YOUR CHOICE", cx, cy - 250, "bold", 54, col(accent, a))
            for i, lab in enumerate((v[1], v[2])):
                ai = ease((lt - 0.25 - i * dur * 0.35) / 0.3)
                if ai <= 0: continue
                bx = cx + (-1 if i == 0 else 1) * 430
                r = skia.Rect.MakeXYWH(bx - 370, cy - 150, 740, 300)
                c.drawRoundRect(r, 30, 30, skia.Paint(AntiAlias=True, Color=col("#FFFFFF", 0.07 * ai)))
                c.drawRoundRect(r, 30, 30, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=6, Color=col(accent if i else "#FFFFFF", ai)))
                text(c, "AB"[i], bx - 300, cy - 78, "black", 64, col(accent, ai))
                text(c, lab, bx, cy + 40, "black", 110, col("#FFFFFF", ai), 640)
            text(c, "OR", cx, cy + 22, "black", 60, col("#FFFFFF", 0.6 * a))
        elif kind in ("odds", "final"):
            if kind == "odds":
                val = self.odds_at(t); label = "YOUR ODDS RIGHT NOW"
            else:
                val = v[1] * ease(lt / 1.4); label = v[2]
            self.gauge(c, cx, cy + 150, 360, val, accent, big=True)
            text(c, label, cx, cy - 290, "bold", 58, col("#FFFFFF", 0.9 * a), 1500)
            if kind == "final": text(c, "An estimate for fun, not a forecast.", cx, cy - 228, "semi", 30, col("#FFFFFF", 0.55 * a))
        c.restore()

    def card(self, c, t, ch):
        b0, b1 = ch["beat"]; lt = t - b0; a = ease(lt / 0.35) * (1 - ease((lt - (b1 - b0 - 0.25)) / 0.25))
        cx, cy = W / 2, H / 2; z = 1.25 - 0.25 * ease(lt / 0.5) + 0.015 * lt
        c.save(); c.translate(cx, cy); c.scale(z, z); c.translate(-cx, -cy)
        text(c, ch["label"], cx, cy + 60, "black", 330, col("#FFFFFF", a), 1600)
        w = 520 * ease(lt / 0.6)
        c.drawRoundRect(skia.Rect.MakeXYWH(cx - w / 2, cy + 110, w, 12), 6, 6, skia.Paint(AntiAlias=True, Color=col(ch["accent"], a)))
        text(c, ch["tag"], cx, cy + 210, "bold", 70, col(ch["accent"], a), 1500)
        c.restore()

    def hud(self, c, t, ch, on_card, full_gauge):
        a = ease((t - 2.3) / 0.5)
        if a <= 0: return
        if on_card: a = 0.0
        if hasattr(self, "clocks") and a > 0:
            fx.badge(c, t, ch, self.clocks[self.ch.index(ch)], a)
        elif not hasattr(self, "clocks"):
            f, w, _ = fit(ch["label"], "black", 46, 600)
            c.drawRoundRect(skia.Rect.MakeXYWH(70, 62, w + 56, 74), 14, 14, skia.Paint(AntiAlias=True, Color=col(ch["accent"], a)))
            c.drawString(ch["label"], 98, 115, f, skia.Paint(AntiAlias=True, Color=col("#06080C", a)))
        if a <= 0: return
        if not full_gauge:
            c.saveLayerAlpha(None, int(255 * a)); self.gauge(c, W - 210, 205, 128, self.odds_at(t), ch["accent"]); c.restore()
        c.drawRect(skia.Rect.MakeXYWH(0, H - 8, W * t / self.total, 8), skia.Paint(Color=col(ch["accent"], 0.9 * a)))

    def caption(self, c, t):
        for (s, e, p) in self.caps:
            if s <= t < e + 0.12:
                f, w, _ = fit(p, "bold", 54, 1640)
                c.drawRoundRect(skia.Rect.MakeXYWH(W / 2 - w / 2 - 34, H - 156, w + 68, 88), 18, 18, skia.Paint(AntiAlias=True, Color=0xB8000000))
                c.drawString(p, W / 2 - w / 2, H - 94, f, skia.Paint(AntiAlias=True, Color=0xFFFFFFFF))
                return

    def frame(self, c, t):
        ch = [x for x in self.ch if x["start"] <= t][-1] if t >= 0 else self.ch[0]
        self.bg(c, t, ch["accent"])
        on_card = bool(ch["beat"]) and ch["beat"][0] <= t < ch["beat"][1]
        full = False
        if on_card:
            self.card(c, t, ch)
        else:
            cur = [l for l in self.lines if l["start"] <= t]
            l = cur[-1] if cur else self.lines[0]
            full = l["visual"][0] in ("odds", "final")
            self.visual(c, max(t, l["start"]), l, ch["accent"])
        self.hud(c, t, ch, on_card, full)
        if not on_card: self.caption(c, t)

    # ---------- cartoon mode ----------
    CH_EXPR = ["scared", "worried", "think", "worried", "worried", "determined", "neutral", "happy"]
    POSES = ["talk", "point", "shrug", "idle", "talk", "hold"]
    SHOTS = [(1.0, 0.0), (1.42, 0.60), (1.0, 0.0), (1.95, 0.84), (1.42, 0.60)]   # zoom, focus height on the character

    def groups(self):
        if hasattr(self, "_g"): return self._g
        g = []
        for l in self.lines:
            cur = []
            for (a, b, w) in l.get("words", []):
                cur.append((a, b, w))
                if len(cur) == 2 or len(" ".join(x[2] for x in cur)) > 9 or w[-1] in ".?!,":
                    g.append((cur[0][0], cur[-1][1], " ".join(x[2] for x in cur))); cur = []
            if cur: g.append((cur[0][0], cur[-1][1], " ".join(x[2] for x in cur)))
        self._g = g; return g

    def caption2(self, c, t, y=None):
        g = self.groups(); y = y or H * 0.845
        for i, (a, b, txt) in enumerate(g):
            nxt = g[i + 1][0] if i + 1 < len(g) else b + 0.4
            if a <= t < min(nxt, b + 0.45):
                k = 0.86 + 0.14 * ease((t - a) / 0.07)
                f, w, size = fit(txt, "black", 104 * k, 1500)
                x = W / 2 - w / 2
                st = skia.Paint(AntiAlias=True, Color=toon.INK, Style=skia.Paint.kStroke_Style, StrokeWidth=size * 0.17, StrokeJoin=skia.Paint.kRound_Join)
                c.drawString(txt, x, y, f, st); c.drawString(txt, x, y, f, skia.Paint(AntiAlias=True, Color=0xFFFFFFFF))
                return

    def frame2(self, c, t):
        ci = max(i for i, x in enumerate(self.ch) if x["start"] <= t) if t >= 0 else 0
        ch = self.ch[ci]; on_card = bool(ch["beat"]) and ch["beat"][0] <= t < ch["beat"][1]
        cur = [l for l in self.lines if l["start"] <= t]
        l = cur[-1] if cur else self.lines[0]
        if on_card: l = [x for x in self.lines if x["ch"] == ci][0]
        kind = l["visual"][0]; overlay = kind in ("card", "list", "choice", "odds", "final")
        idx = self.lines.index(l); lt = max(0.0, t - l["start"])
        z, fh = (1.0, 0.0) if (overlay or on_card) else self.SHOTS[idx % len(self.SHOTS)]
        if kind == "hook": z, fh = 1.55, 0.98
        cam = toon.Cam(t)
        # the set returns where the character stands; draw once off-screen to learn it, then for real under the camera
        c.save()
        c.restore()
        probe = self._info[ci % len(toon.SETS)]
        fx, fy = (probe["x"], probe["y"] - probe["s"] * fh) if fh else (W / 2, H / 2)
        zz = z * (1 + 0.035 * min(1.0, lt / 5.0))
        hw, hh = W / 2 / zz, H / 2 / zz; mx, my = min(30.0, max(0.0, W / 2 - hw)), min(20.0, max(0.0, H / 2 - hh))   # never show past the edge of the set
        fx = min(max(fx, hw + mx), W - hw - mx) if hw <= W / 2 else W / 2
        fy = min(max(fy, hh + my), H - hh - my) if hh <= H / 2 else H / 2
        c.save(); c.translate(W / 2, H / 2); c.scale(zz, zz); c.translate(-fx, -fy)
        info = toon.SETS[ci % len(toon.SETS)](c, t, cam)
        talking = any(a <= t < b for (a, b, _) in l.get("words", [])) and not on_card
        expr = "scared" if kind == "hook" else ("think" if kind == "choice" else self.CH_EXPR[ci % len(self.CH_EXPR)])
        pose = "panic" if kind == "hook" else ("think" if kind == "choice" else self.POSES[idx % len(self.POSES)])
        toon.character(c, info["x"], info["y"], info["s"], t, pose=pose, expr=expr, talking=talking, light=info["light"], bag=info.get("bag", False))
        c.restore()
        toon.tint(c, info["amb"][0], info["amb"][1]); toon.vignette(c, 0.78)
        if kind == "hook":
            a = 1.0   # hook rule: the first frame is already complete
            words = l["visual"][1].split(); mid = (len(words) + 1) // 2
            for j, (line_txt, colr) in enumerate(((" ".join(words[:mid]), "#FFFFFF"), (" ".join(words[mid:]), ch["accent"]))):
                f, w, size = fit(line_txt, "black", 148, 1700); yy = 190 + j * 150
                c.drawString(line_txt, W / 2 - w / 2, yy, f, skia.Paint(AntiAlias=True, Color=toon.INK, Style=skia.Paint.kStroke_Style, StrokeWidth=22, StrokeJoin=skia.Paint.kRound_Join))
                c.drawString(line_txt, W / 2 - w / 2, yy, f, skia.Paint(AntiAlias=True, Color=col(colr, a)))
        if on_card:
            c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Color=skia.Color(4, 6, 10, 150))); self.card(c, t, ch)
        elif overlay:
            c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Color=skia.Color(4, 6, 10, 190)))
            c.save()
            if kind in ("odds", "final"): c.translate(W / 2, H * 0.455); c.scale(0.84, 0.84); c.translate(-W / 2, -H / 2)   # leave room for the caption
            self.visual(c, max(t, l["start"]), l, ch["accent"]); c.restore()
        self.hud(c, t, ch, on_card, kind in ("odds", "final") and not on_card)
        if not on_card: self.caption2(c, t, H * 0.90 if overlay else None)

    def prep(self):
        rec = skia.PictureRecorder(); cc = rec.beginRecording(skia.Rect.MakeWH(W, H))
        self._info = [f(cc, 0.0, toon.Cam(0.0)) for f in toon.SETS]; self._scratch = None

    # ---------- image mode: one illustration per shot (episodes/<ep>/shots.py + img/), slow camera moves, overlays ----------
    def prep_images(self):
        import importlib.util, glob
        spec = importlib.util.spec_from_file_location("shots", os.path.join(self.ep, "shots.py")); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        line_img = {}
        for sid, name, lines, side, desc in m.SHOTS:
            for li in lines: line_img[li] = sid
        for li, sid in m.REUSE.items(): line_img[li] = sid
        self.inserts = getattr(m, "INSERTS", {})
        spec2 = importlib.util.spec_from_file_location("script", os.path.join(self.ep, "script.py")); m2 = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(m2)
        self.clocks = [c.get("clock") for c in m2.CHAPTERS]
        files = {}
        for sid, name, *_ in m.SHOTS:
            f = sorted(glob.glob(os.path.join(self.ep, "img", f"{sid}_*.png")) + glob.glob(os.path.join(self.ep, "img", f"{sid}_*.jpg")))
            if not f and os.environ.get("ALLOW_MISSING"): f = sorted(glob.glob(os.path.join(self.ep, "img", "*.png")))[:1]
            if not f: raise SystemExit(f"missing image for {sid}")
            files[sid] = f[-1]
        cache = {}
        def load(sid):
            if sid not in cache:
                from PIL import Image
                im = Image.open(files[sid]).convert("RGBA"); sc = max(W / im.width, H / im.height)
                im = im.resize((int(im.width * sc + 0.5), int(im.height * sc + 0.5)), Image.LANCZOS)
                l, tp = (im.width - W) // 2, (im.height - H) // 2; im = im.crop((l, tp, l + W, tp + H))
                cache[sid] = skia.Image.fromarray(np.array(im), colorType=skia.kRGBA_8888_ColorType)
            return cache[sid]
        self.load_img = load
        # segments: a line's picture starts at its chapter start (first line) or at the end of the previous line
        segs = []
        for i, l in enumerate(self.lines):
            t0 = self.ch[l["ch"]]["start"] if (i == 0 or self.lines[i - 1]["ch"] != l["ch"]) else l["start"]
            sid = line_img[i]
            if segs and segs[-1][2] == sid: continue
            segs.append([t0, None, sid])
        for k in range(len(segs)): segs[k][1] = segs[k + 1][0] if k + 1 < len(segs) else self.total + 1
        self.isegs = segs

    def draw_img(self, c, k, t, alpha=1.0):
        t0, t1, sid = self.isegs[k]; d = max(1.0, t1 - t0); u = min(1.0, max(0.0, (t - t0) / d))
        im = self.load_img(sid)
        zin = k % 2 == 0
        z = 1.05 + 0.09 * (u if zin else 1 - u)
        dirs = [(1, 0.3), (-1, -0.2), (0.6, -0.5), (-0.7, 0.4)]; dx, dy = dirs[k % 4]
        ox = dx * (u - 0.5) * W * (z - 1.0) * 0.8; oy = dy * (u - 0.5) * H * (z - 1.0) * 0.8
        c.save(); c.translate(W / 2 + ox, H / 2 + oy); c.scale(z, z); c.translate(-W / 2, -H / 2)
        p = skia.Paint(AntiAlias=True); p.setAlphaf(alpha)
        c.drawImageRect(im, skia.Rect.MakeWH(W, H), skia.SamplingOptions(skia.FilterMode.kLinear), p)
        c.restore()

    def frame3(self, c, t):
        ci = max(i for i, x in enumerate(self.ch) if x["start"] <= t) if t >= 0 else 0
        ch = self.ch[ci]; on_card = bool(ch["beat"]) and ch["beat"][0] <= t < ch["beat"][1]
        cur = [l for l in self.lines if l["start"] <= t]
        l = cur[-1] if cur else self.lines[0]
        if on_card: l = [x for x in self.lines if x["ch"] == ci][0]
        kind = l["visual"][0]
        k = max(j for j, sg in enumerate(self.isegs) if sg[0] <= t) if t >= self.isegs[0][0] else 0
        self.draw_img(c, k, t)
        FADE = 0.45
        if k > 0 and t - self.isegs[k][0] < FADE:   # cross-fade from the previous picture
            self.draw_img(c, k - 1, t, 1.0 - ease((t - self.isegs[k][0]) / FADE))
        toon.vignette(c, 0.55)
        if kind == "hook":
            words = l["visual"][1].split(); mid = (len(words) + 1) // 2
            c.drawRect(skia.Rect.MakeXYWH(0, 0, W, 420), skia.Paint(Shader=skia.GradientShader.MakeLinear([(0, 0), (0, 420)], [skia.Color(0, 0, 0, 170), skia.Color(0, 0, 0, 0)])))
            for j, (line_txt, colr) in enumerate(((" ".join(words[:mid]), "#FFFFFF"), (" ".join(words[mid:]), ch["accent"]))):
                f, w, size = fit(line_txt, "black", 148, 1700); yy = 190 + j * 150
                c.drawString(line_txt, W / 2 - w / 2, yy, f, skia.Paint(AntiAlias=True, Color=toon.INK, Style=skia.Paint.kStroke_Style, StrokeWidth=22, StrokeJoin=skia.Paint.kRound_Join))
                c.drawString(line_txt, W / 2 - w / 2, yy, f, skia.Paint(AntiAlias=True, Color=col(colr)))
        dur = l["end"] - l["start"]; idx = self.lines.index(l); ins = self.inserts.get(idx)
        if on_card:
            fx.chalk_card(c, t, ch)
        elif ins:
            t_in = l["start"] + ins[1] * dur
            if t >= t_in:
                if ins[0].startswith("phone_"): fx.phone(c, t, ins[0][6:], t_in, l)
                elif ins[0] == "tv": fx.tv(c, t, t_in, l)
        elif kind in ("card", "list"):
            t_in = l["start"] + (0.0 if kind == "card" else min(1.8, 0.3 * dur))
            if t >= t_in: fx.notepad(c, t, l, ch["accent"], t_in)
        elif kind in ("choice", "odds", "final"):
            c.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Color=skia.Color(4, 6, 10, 175)))
            c.save()
            if kind in ("odds", "final"): c.translate(W / 2, H * 0.455); c.scale(0.84, 0.84); c.translate(-W / 2, -H / 2)
            self.visual(c, max(t, l["start"]), l, ch["accent"]); c.restore()
        self.hud(c, t, ch, on_card, kind in ("odds", "final") and not on_card)
        if not on_card: self.caption2(c, t, H * 0.90 if kind in ("choice", "odds", "final") else None)


def surface():
    arr = np.zeros((H, W, 4), dtype=np.uint8); return arr, skia.Surface(arr)


if __name__ == "__main__":
    ep, cmd = sys.argv[1], sys.argv[2]; E = Ep(ep); E.prep(); E.frame = E.frame2
    if os.path.exists(os.path.join(ep, "shots.py")) and os.environ.get("RENDER_MODE", "img") == "img":
        E.prep_images(); E.frame = E.frame3
    if cmd == "frames":
        os.makedirs(os.path.join(ep, "chk"), exist_ok=True)
        for a in sys.argv[3:]:
            from PIL import Image
            arr, s = surface(); E.frame(s.getCanvas(), float(a)); s.flushAndSubmit()
            Image.fromarray(arr, "RGBA").convert("RGB").resize((960, 540), Image.LANCZOS).save(os.path.join(ep, "chk", f"f_{float(a):07.2f}.jpg"), quality=82)
        print("ok")
    elif cmd == "seg":
        t0, t1, out = float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
        ff = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                               "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", "-threads", "1", out], stdin=subprocess.PIPE)
        arr, s = surface(); c = s.getCanvas()
        for n in range(int(round(t0 * FPS)), int(round(t1 * FPS))):
            E.frame(c, n / FPS); ff.stdin.write(arr.tobytes())
        ff.stdin.close(); ff.wait(); print("seg done", out)
    elif cmd == "join":
        out, segs = sys.argv[3], sys.argv[4:]
        lst = os.path.join(ep, "segs.txt"); open(lst, "w").write("".join(f"file '{os.path.abspath(s)}'\n" for s in segs))
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-i", os.path.join(ep, "voice", "final.wav"),
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-shortest", "-movflags", "+faststart", out], check=True)
        print("joined", out)
