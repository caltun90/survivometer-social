"""Voice: Gemini TTS per chapter group, sentence alignment, timeline and audio mix.

  GEMINI_API_KEY=... python3 engine/voice.py <episode_dir> tts [group ...]   -> voice/g<N>.wav
  GEMINI_API_KEY=... python3 engine/voice.py <episode_dir> align             -> voice/starts.json (Gemini timestamps)
  python3 engine/voice.py <episode_dir> build                                 -> voice/final.wav + timeline.json
"""
import sys, os, json, base64, re, subprocess, importlib.util, tempfile
import numpy as np, soundfile as sf

TTS_MODEL = os.environ.get("TTS_MODEL", "gemini-3.1-flash-tts-preview")
ASR_MODEL = os.environ.get("ASR_MODEL", "gemini-3-flash-preview")
SR = 24000
LEAD = 0.20            # voice starts this early (hook rule: sound by 0.5 s)
BEAT = float(os.environ.get("BEAT", "1.9"))            # chapter title card length
GAP_MIN, GAP_MAX = float(os.environ.get("GAP_MIN", "0.28")), float(os.environ.get("GAP_MAX", "0.55"))
TAIL = 1.6


def load_script(ep):
    spec = importlib.util.spec_from_file_location("script", os.path.join(ep, "script.py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def api(model, body, timeout=300):
    key = os.environ["GEMINI_API_KEY"]
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(body, f); path = f.name
    try:
        out = subprocess.run(["curl", "-sS", "--max-time", str(timeout),
                              f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                              "-H", "x-goog-api-key: " + key, "-H", "Content-Type: application/json",
                              "--data-binary", "@" + path], capture_output=True, text=True).stdout
    finally:
        os.unlink(path)
    d = json.loads(out)
    if "error" in d:
        raise SystemExit(f"API error {d['error'].get('code')}: {d['error'].get('message', '')[:300]}")
    return d


def group_lines(S, g):
    return [l for c in S.GROUPS[g] for l in S.CHAPTERS[c]["lines"]]


def tts_text(text, tag=""):
    # gemini-3.8-flash-tts reads a style instruction aloud, so it gets the plain text only
    prompt = text if "3.8" in TTS_MODEL else S_STYLE[0] + "\n\n" + text
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": S_STYLE[1]}}}}}
    for attempt in range(int(os.environ.get('TTS_TRIES', '2'))):   # the model sometimes returns an empty candidate; one retry only (daily quota is small)
        d = api(TTS_MODEL, body)
        cand = (d.get("candidates") or [{}])[0]
        if cand.get("content", {}).get("parts"): break
        print(f"{tag}: empty answer, finishReason={cand.get('finishReason')} {d.get('promptFeedback', '')}", flush=True)
    else:
        raise SystemExit(f"{tag}: no audio")
    part = cand["content"]["parts"][0]["inlineData"]
    raw = base64.b64decode(part["data"]); mime = part.get("mimeType", "")
    if "wav" in mime:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f: f.write(raw)
        x, sr = sf.read(f.name, dtype="float32"); os.unlink(f.name)
    else:
        m = re.search(r"rate=(\d+)", mime); sr = int(m.group(1)) if m else SR
        x = np.frombuffer(raw, dtype="<i2").astype(np.float32) / 32768.0
    if x.ndim > 1: x = x.mean(axis=1)
    assert sr == SR, sr
    return x


S_STYLE = ["", ""]


def tts(ep, S, g):
    S_STYLE[:] = [S.STYLE, S.VOICE]
    text = "\n".join(l[0] for l in group_lines(S, g))
    x = tts_text(text, f"g{g}")
    os.makedirs(os.path.join(ep, "voice"), exist_ok=True)
    sf.write(os.path.join(ep, "voice", f"g{g}.wav"), x, SR)
    print(f"g{g}: {len(x) / SR:.1f} s, {len(text.split())} words")


def fixline(ep, S, g, li):
    """Re-record one line and splice it into the group audio (use when psalign flags a line as BAD). Run psalign again afterwards."""
    S_STYLE[:] = [S.STYLE, S.VOICE]
    lines = group_lines(S, g); cuts = json.load(open(os.path.join(ep, "voice", "cuts.json")))[str(g)]
    path = os.path.join(ep, "voice", f"g{g}.wav"); x, _ = sf.read(path, dtype="float32")
    if not os.path.exists(path.replace(".wav", "_orig.wav")): sf.write(path.replace(".wav", "_orig.wav"), x, SR)
    new = tts_text(lines[li][0], f"g{g} line {li}")
    sil = silences(new, 0.3); n = len(new) / SR
    a = sil[0][1] - 0.03 if sil and sil[0][0] < 0.02 else 0.0
    b = sil[-1][0] + 0.06 if sil and sil[-1][1] > n - 0.02 else n
    new = new[int(a * SR):int(b * SR)]
    head = x[:int((cuts[li - 1][1] + 0.06) * SR)] if li else x[:0]
    tail = x[int((cuts[li + 1][0] - 0.03) * SR):] if li + 1 < len(cuts) else x[:0]
    z = np.zeros(int(0.9 * SR), dtype=np.float32)
    sf.write(path, np.concatenate([head, z, new, z, tail]), SR)
    print(f"g{g} line {li}: new take {len(new) / SR:.1f} s spliced")


ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
TENS = "x x twenty thirty forty fifty sixty seventy eighty ninety".split()


def _num(n):
    n = int(n)
    if n < 20: return ONES[n]
    if n < 100: return TENS[n // 10] + (" " + ONES[n % 10] if n % 10 else "")
    if n < 1000: return ONES[n // 100] + " hundred" + (" " + _num(n % 100) if n % 100 else "")
    return " ".join(ONES[int(c)] for c in str(n))


def psalign(ep, S, g):
    """Forced alignment of the script against the group audio with pocketsphinx (local, no API quota).
    Writes line cuts to voice/cuts.json and per-word timings to voice/words.json."""
    from pocketsphinx import Decoder
    lines = group_lines(S, g)
    path = os.path.join(ep, "voice", f"g{g}.wav"); x, _ = sf.read(path, dtype="float32")
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout
    dec = Decoder(samprate=16000, logfn=os.devnull)
    toks = []
    for li, l in enumerate(lines):
        for j, w in enumerate(l[0].split()):
            t = re.sub(r"(?<=\d),(?=\d)", "", w.lower()).replace("%", " percent").replace("-", " ").replace("\u2019", "'")
            t = re.sub(r"\d+", lambda m: " " + _num(m.group()) + " ", t)
            for tok in re.findall(r"[a-z']+", t):
                tok = tok.strip("'")
                if tok and dec.lookup_word(tok): toks.append((li, j, tok))
    dec.set_align_text(" ".join(t[2] for t in toks)); dec.start_utt(); dec.process_raw(raw, full_utt=True); dec.end_utt()
    segs = [(sg.start_frame / 100, (sg.end_frame + 1) / 100) for sg in dec.seg() if not sg.word.startswith("<") and sg.word != "(NULL)"]
    if len(segs) != len(toks): raise SystemExit(f"g{g}: aligner returned {len(segs)} words for {len(toks)}")
    n = len(lines); first, last, wt = {}, {}, {}
    for (li, j, _), (a, b) in zip(toks, segs):
        first.setdefault(li, (a, b)); last[li] = (a, b)
        wt[(li, j)] = (wt[(li, j)][0], b) if (li, j) in wt else (a, b)
    if len(first) != n: raise SystemExit(f"g{g}: some lines have no alignable words")
    sil = silences(x, 0.2); dur = len(x) / SR
    A = [first[i][0] for i in range(n)]; B = [last[i][1] for i in range(n)]
    lead = [q for q in sil if q[0] <= 0.05 and q[1] <= first[0][1]]
    if lead: A[0] = lead[0][1]
    for i in range(n - 1):
        cand = [(q[1] - q[0], q) for q in sil if q[0] >= last[i][0] - 0.05 and q[1] <= first[i + 1][1] + 0.05]
        if cand: q = max(cand)[1]; B[i], A[i + 1] = q[0], q[1]
    end = [q for q in sil if q[0] >= last[n - 1][0] and q[1] - q[0] >= 0.4]
    B[n - 1] = end[0][0] if end else dur
    cuts, words, bad = [], [], []
    for i, l in enumerate(lines):
        sw = l[0].split(); a0 = max(0.0, A[i] - 0.02)
        tm = [wt.get((i, j)) for j in range(len(sw))]
        for j in range(len(sw)):   # words the aligner does not know sit between their neighbours
            if tm[j] is None:
                pa = tm[j - 1][1] if j and tm[j - 1] else A[i]
                nx = next((tm[k][0] for k in range(j + 1, len(sw)) if tm[k]), B[i])
                tm[j] = (pa, max(pa + 0.05, nx))
        tm = [(min(max(a, A[i]), B[i]), min(max(b, A[i]), B[i])) for a, b in tm]
        tm[0] = (A[i], tm[0][1]) if tm[0][1] - tm[0][0] > 0.9 else tm[0]
        cw = (l[2] if len(l) > 2 else l[0]).split(); m = len(sw)
        out = []
        for k, w in enumerate(cw):
            j0 = k if len(cw) == m else min(m - 1, k * m // len(cw)); j1 = k if len(cw) == m else min(m - 1, max(j0, (k + 1) * m // len(cw) - 1))
            out.append([round(tm[j0][0] - a0, 3), round(tm[j1][1] - a0, 3), w])
        words.append(out)
        cuts.append([round(A[i], 2), round(B[i], 2), round((A[i + 1] - B[i]) if i + 1 < n else 0.5, 2)])
        d = B[i] - A[i]; inner = max([q[1] - q[0] for q in sil if q[0] > A[i] + 0.05 and q[1] < B[i] - 0.05] or [0])
        if d > 1.9 * len(sw) / 2.6 + 1.5 or d < 0.45 * len(sw) / 2.6 or inner > 2.5: bad.append(i)
    for name, val in (("cuts.json", cuts), ("words.json", words)):
        pth = os.path.join(ep, "voice", name); allv = json.load(open(pth)) if os.path.exists(pth) else {}
        allv[str(g)] = val; json.dump(allv, open(pth, "w"))
    extra = dur - B[n - 1] - sum(q[1] - q[0] for q in sil if q[0] >= B[n - 1])
    print(f"g{g}: {n} lines aligned" + (f"; BAD lines {bad} (re-record with: fixline {g} <line>)" if bad else "") + (f"; {extra:.1f} s of extra speech after the last line is ignored" if extra > 1 else ""))


def tts_kokoro(ep, S, g):
    """Local, quota-free narration with Kokoro (same voice every time). Lines are read one by one and joined with short silences."""
    from kokoro_onnx import Kokoro
    kd = os.environ.get("KOKORO_DIR", "/home/claude/kokoro")
    k = Kokoro(os.path.join(kd, "kokoro-v1.0.onnx"), os.path.join(kd, "voices-v1.0.bin"))
    v = getattr(S, "KOKORO_VOICE", "am_michael"); speed = float(os.environ.get("KOKORO_SPEED", getattr(S, "KOKORO_SPEED", 0.9)))
    parts = [np.zeros(int(0.3 * SR), dtype=np.float32)]; bounds = []
    for line in group_lines(S, g):
        x, sr = k.create(line[0], voice=v, speed=speed, lang="en-gb" if v.startswith("b") else "en-us")
        x = np.asarray(x, dtype=np.float32)
        if sr != SR:
            n = int(len(x) * SR / sr); x = np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x).astype(np.float32)
        t0 = sum(len(q) for q in parts) / SR; bounds.append([t0, t0 + len(x) / SR])
        parts += [x, np.zeros(int(0.75 * SR), dtype=np.float32)]
    bp = os.path.join(ep, "voice", "kokoro_bounds.json"); allb = json.load(open(bp)) if os.path.exists(bp) else {}
    allb[str(g)] = bounds; json.dump(allb, open(bp, "w"))
    y = np.concatenate(parts); y = y / max(1e-6, np.abs(y).max()) * 0.89
    os.makedirs(os.path.join(ep, "voice"), exist_ok=True)
    sf.write(os.path.join(ep, "voice", f"g{g}.wav"), y, SR)
    print(f"g{g}: {len(y) / SR:.1f} s (kokoro {v}, speed {speed})", flush=True)


def psalign_lines(ep, S, g):
    """Kokoro audio: line boundaries are known, so align each line on its own (robust) and write cuts and words."""
    from pocketsphinx import Decoder
    lines = group_lines(S, g); B = json.load(open(os.path.join(ep, "voice", "kokoro_bounds.json")))[str(g)]
    path = os.path.join(ep, "voice", f"g{g}.wav"); x, _ = sf.read(path, dtype="float32")
    cuts, words = [], []
    for i, l in enumerate(lines):
        a, b = B[i]; seg = x[int(a * SR):int(b * SR)]
        sil = silences(seg, 0.12); n = len(seg) / SR
        a2 = a + (sil[0][1] - 0.02 if sil and sil[0][0] < 0.02 else 0.0); b2 = a + (sil[-1][0] + 0.04 if sil and sil[-1][1] > n - 0.02 else n)
        seg = x[int(a2 * SR):int(b2 * SR)]
        pcm = (np.clip(np.interp(np.linspace(0, len(seg) - 1, int(len(seg) * 16000 / SR)), np.arange(len(seg)), seg), -1, 1) * 32767).astype("<i2").tobytes()
        dec = Decoder(samprate=16000, logfn=os.devnull)
        sw = l[0].split(); toks = []
        for j, w in enumerate(sw):
            t = re.sub(r"(?<=\d),(?=\d)", "", w.lower()).replace("%", " percent").replace("-", " ").replace("\u2019", "'")
            t = re.sub(r"\d+", lambda m: " " + _num(m.group()) + " ", t)
            for tok in re.findall(r"[a-z']+", t):
                tok = tok.strip("'")
                if tok and dec.lookup_word(tok): toks.append((j, tok))
        tm = {}
        try:
            dec.set_align_text(" ".join(t[1] for t in toks)); dec.start_utt(); dec.process_raw(pcm, full_utt=True); dec.end_utt()
            sg = [(q.start_frame / 100, (q.end_frame + 1) / 100) for q in dec.seg() if not q.word.startswith("<") and q.word != "(NULL)"]
            if len(sg) == len(toks):
                for (j, _), (u, v) in zip(toks, sg): tm[j] = (tm[j][0], v) if j in tm else (u, v)
        except Exception:
            pass
        d = b2 - a2
        if len(tm) < len(sw):   # fill gaps (or everything) by character share
            tot = sum(len(w) + 1 for w in sw); acc = 0.0; prop = []
            for w in sw: u = d * acc / tot; acc += len(w) + 1; prop.append((u, d * acc / tot))
            tm = {j: tm.get(j, prop[j]) for j in range(len(sw))}
        cw = (l[2] if len(l) > 2 else l[0]).split(); m = len(sw); out = []
        for k2, w in enumerate(cw):
            j0 = k2 if len(cw) == m else min(m - 1, k2 * m // len(cw)); j1 = k2 if len(cw) == m else min(m - 1, max(j0, (k2 + 1) * m // len(cw) - 1))
            out.append([round(min(tm[j0][0], d), 3), round(min(tm[j1][1], d), 3), w])
        words.append(out)
        nxt = B[i + 1][0] if i + 1 < len(lines) else b2 + 0.5
        cuts.append([round(a2, 2), round(b2, 2), round(max(0.0, nxt - b2), 2)])
    for name, val in (("cuts.json", cuts), ("words.json", words)):
        pth = os.path.join(ep, "voice", name); allv = json.load(open(pth)) if os.path.exists(pth) else {}
        allv[str(g)] = val; json.dump(allv, open(pth, "w"))
    print(f"g{g}: {len(lines)} lines aligned line by line", flush=True)


def silences(x, min_dur=0.14):
    hop = int(SR * 0.01); n = len(x) // hop
    rms = np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(axis=1) + 1e-12)
    quiet = rms < max(0.010, 0.035 * np.percentile(rms, 95))
    gaps, i = [], 0
    while i < n:
        if quiet[i]:
            j = i
            while j < n and quiet[j]: j += 1
            if (j - i) * 0.01 >= min_dur: gaps.append((i * 0.01, j * 0.01))
            i = j
        else:
            i += 1
    return gaps


def asr_starts(ep, S, g):
    """Ask Gemini when each line starts (seconds). Approximate; used to pick the right pause."""
    lines = [l[0] for l in group_lines(S, g)]
    wav = open(os.path.join(ep, "voice", f"g{g}.wav"), "rb").read()
    prompt = ("This audio is a narrator reading the numbered lines below, in order. For each line give the time in seconds "
              "(one decimal) at which the narrator STARTS speaking it. Return only a JSON array of numbers, one per line.\n\n"
              + "\n".join(f"{i + 1}. {t}" for i, t in enumerate(lines)))
    d = api(ASR_MODEL, {"contents": [{"parts": [{"inlineData": {"mimeType": "audio/wav", "data": base64.b64encode(wav).decode()}},
                                                 {"text": prompt}]}],
                        "generationConfig": {"responseMimeType": "application/json", "temperature": 0}})
    arr = json.loads(d["candidates"][0]["content"]["parts"][0]["text"])
    assert len(arr) == len(lines), (len(arr), len(lines))
    return [float(a) for a in arr]


def cut_points(x, lines, starts=None):
    """Choose one pause per line boundary by share of spoken (non-silent) time, preferring longer pauses."""
    total = len(x) / SR
    gaps = silences(x)
    lead = gaps[0][1] if gaps and gaps[0][0] < 0.05 else 0.0
    trail = gaps[-1][0] if gaps and gaps[-1][1] > total - 0.05 else total
    inner = [g for g in gaps if g[0] > lead + 0.05 and g[1] < trail - 0.05]
    durs = np.array([g[1] - g[0] for g in inner])
    voiced_before = np.array([(g[0] - lead) - durs[:i].sum() for i, g in enumerate(inner)])
    voiced_total = (trail - lead) - durs.sum()
    w = np.array([len(t) for t in lines], dtype=float)
    target = voiced_total * np.cumsum(w)[:-1] / w.sum()
    nb, ng = len(lines) - 1, len(inner)
    if ng < nb: raise SystemExit(f"not enough pauses ({ng} < {nb})")
    cap = float(np.percentile(durs, 80))
    cost = np.abs(voiced_before[None, :] - target[:, None]) - 1.2 * np.minimum(durs, cap)[None, :]
    INF = 1e9
    dp = np.full((nb, ng), INF); arg = np.zeros((nb, ng), dtype=int); dp[0] = cost[0]
    for i in range(1, nb):
        best, bj = INF, -1
        for j in range(ng):
            if j >= 1 and dp[i - 1, j - 1] < best: best, bj = dp[i - 1, j - 1], j - 1
            if bj >= 0: dp[i, j] = best + cost[i, j]; arg[i, j] = bj
    j = int(np.argmin(dp[-1])); pick = [j]
    for i in range(nb - 1, 0, -1):
        j = arg[i, j]; pick.append(j)
    pick = pick[::-1]
    if starts:   # manual override: {line index: pause index shift}
        pick = [k + int(starts.get(str(i + 1), 0)) for i, k in enumerate(pick)]
    segs, a = [], lead
    for k in pick:
        segs.append((a, inner[k][0], inner[k][1] - inner[k][0])); a = inner[k][1]
    segs.append((a, trail, 0.5))
    dev = float(np.max(np.abs(voiced_before[pick] - target))) if nb else 0.0
    return segs, dev


def autocut(ep, S, g):
    """Cut the audio at every pause, let Gemini transcribe each chunk, then map chunks to script lines by words."""
    import difflib
    x, _ = sf.read(os.path.join(ep, "voice", f"g{g}.wav"), dtype="float32")
    gl = [l[0] for l in group_lines(S, g)]
    total = len(x) / SR; gaps = silences(x, 0.22)
    lead = gaps[0][1] if gaps and gaps[0][0] < 0.05 else 0.0
    trail = gaps[-1][0] if gaps and gaps[-1][1] > total - 0.05 else total
    inner = [q for q in gaps if q[0] > lead + 0.05 and q[1] < trail - 0.05]
    edges = [lead] + [v for q in inner for v in q] + [trail]
    chunks = [(edges[i], edges[i + 1]) for i in range(0, len(edges), 2)]
    tt = np.arange(int(0.3 * SR)) / SR; beep = (0.3 * np.sin(2 * np.pi * 1000 * tt)).astype(np.float32); sil = np.zeros(int(0.2 * SR), np.float32)
    parts = []
    for a, b in chunks: parts += [x[int(a * SR):int(b * SR)], sil, beep, sil]
    tmp = os.path.join(ep, "voice", f"chunks{g}.wav"); sf.write(tmp, np.concatenate(parts), SR)
    prompt = (f"This audio has exactly {len(chunks)} short spoken chunks, each followed by a beep tone. Transcribe exactly what is said in each chunk "
              f"(a chunk may be only a few words). Return only a JSON array of exactly {len(chunks)} strings, in order.")
    d = api(ASR_MODEL, {"contents": [{"parts": [{"inlineData": {"mimeType": "audio/wav", "data": base64.b64encode(open(tmp, "rb").read()).decode()}}, {"text": prompt}]}],
                        "generationConfig": {"responseMimeType": "application/json", "temperature": 0}})
    raw = "".join(p.get("text", "") for p in d["candidates"][0].get("content", {}).get("parts", []))
    arr = json.loads(raw[raw.index("["):raw.rindex("]") + 1])
    if len(arr) != len(chunks): raise SystemExit(f"g{g}: heard {len(arr)} chunks, expected {len(chunks)}")
    norm = lambda t: re.sub(r"[^a-z0-9 ]", " ", t.lower()).split()
    E, eline = [], []
    for i, t in enumerate(gl):
        for wd in norm(t): E.append(wd); eline.append(i)
    Hw, hchunk = [], []
    for i, t in enumerate(arr[:len(chunks)]):
        for wd in norm(str(t)): Hw.append(wd); hchunk.append(i)
    sm = difflib.SequenceMatcher(None, E, Hw, autojunk=False)
    e2h = {}
    for blk in sm.get_matching_blocks():
        for k in range(blk.size): e2h[blk.a + k] = blk.b + k
    cuts, prev = [], -1
    for i in range(len(gl) - 1):
        last = max(k for k in range(len(E)) if eline[k] == i)
        k = last
        while k >= 0 and k not in e2h: k -= 1
        ci = hchunk[e2h[k]] if k >= 0 else prev + 1
        ci = max(ci, prev + 1); ci = min(ci, len(chunks) - (len(gl) - 1 - i) - 1)
        cuts.append(ci); prev = ci
    # ignore anything the voice added after the last script word (the model sometimes ad-libs a tail)
    kk = len(E) - 1
    while kk >= 0 and kk not in e2h: kk -= 1
    last_chunk = max(hchunk[e2h[kk]], cuts[-1] + 1) if kk >= 0 else len(chunks) - 1
    segs, a = [], chunks[0][0]
    bounds = [-1] + cuts + [last_chunk]
    for ci in cuts:
        segs.append((a, chunks[ci][1], chunks[ci + 1][0] - chunks[ci][1])); a = chunks[ci + 1][0]
    segs.append((a, chunks[last_chunk][1], 0.5))
    cp = os.path.join(ep, "voice", "cuts.json"); allc = json.load(open(cp)) if os.path.exists(cp) else {}
    allc[str(g)] = segs; json.dump(allc, open(cp, "w"))
    bad = []
    for i, t in enumerate(gl):
        heard = norm(" ".join(str(q) for q in arr[bounds[i] + 1:bounds[i + 1] + 1])); e = norm(t)
        if not heard or e[0] != heard[0] or e[-1][:3] != heard[-1][:3]: bad.append(f"{i}:{' '.join(e[:2])}..{e[-1]}|{' '.join(heard[:2])}..{heard[-1] if heard else ''}")
    print(f"g{g}: {len(chunks)} chunks, ratio {sm.ratio():.2f}, dropped tail chunks {len(chunks) - 1 - last_chunk}, edge mismatches: {bad}")


def get_cuts(ep, S, g, x):
    cp = os.path.join(ep, "voice", "cuts.json")
    if os.path.exists(cp):
        allc = json.load(open(cp))
        if str(g) in allc: return [tuple(q) for q in allc[str(g)]]
    return cut_points(x, [l[0] for l in group_lines(S, g)])[0]


def check(ep, S, g):
    """Verify cuts: join the line segments with beeps and let Gemini transcribe segment by segment."""
    x, _ = sf.read(os.path.join(ep, "voice", f"g{g}.wav"), dtype="float32")
    gl = [l[0] for l in group_lines(S, g)]
    segs = get_cuts(ep, S, g, x)
    tt = np.arange(int(0.35 * SR)) / SR; beep = (0.3 * np.sin(2 * np.pi * 1000 * tt)).astype(np.float32); sil = np.zeros(int(0.25 * SR), np.float32)
    parts = []
    for a, b, _ in segs:
        parts += [squeeze(x[int(a * SR):int(b * SR)].copy()), sil, beep, sil]
    tmp = os.path.join(ep, "voice", f"chk{g}.wav"); sf.write(tmp, np.concatenate(parts), SR)
    wav = open(tmp, "rb").read()
    prompt = (f"This audio has {len(segs)} spoken segments, each followed by a beep tone. Transcribe exactly what is said in each segment. "
              f"Return only a JSON array of {len(segs)} strings, in order, one per segment.")
    d = api(ASR_MODEL, {"contents": [{"parts": [{"inlineData": {"mimeType": "audio/wav", "data": base64.b64encode(wav).decode()}}, {"text": prompt}]}],
                        "generationConfig": {"responseMimeType": "application/json", "temperature": 0}})
    arr = json.loads(d["candidates"][0]["content"]["parts"][0]["text"])
    norm = lambda t: re.sub(r"[^a-z0-9 ]", "", t.lower()).split()
    bad = 0
    for i, exp in enumerate(gl):
        got = arr[i] if i < len(arr) else ""
        e, h = norm(exp), norm(got)
        ok = len(e) and e[:2] == h[:2] and e[-2:] == h[-2:]
        if not ok:
            bad += 1; print(f"  g{g} line {i}: expected [{exp[:50]} ... {exp[-30:]}] heard [{got[:50]} ... {got[-30:]}]")
    print(f"g{g}: {len(gl)} lines, {bad} mismatches (segments heard: {len(arr)})")


def squeeze(seg, spans=None):
    """Shorten long pauses inside a line to 0.45 s."""
    out, pos = [], 0
    for a, b in silences(seg, 0.6):
        cut_a = int((a + 0.22) * SR); cut_b = int((b - 0.23) * SR)
        if cut_b > cut_a and a > 0.05 and b < len(seg) / SR - 0.05:
            out.append(seg[pos:cut_a]); pos = cut_b
            if spans is not None: spans.append((cut_a / SR, cut_b / SR))
    out.append(seg[pos:])
    return np.concatenate(out)


def bed(total, beats, ticks):
    """Quiet drone, a riser on each chapter card, a soft tick when the odds change."""
    n = int(total * SR); t = np.arange(n) / SR; rng = np.random.default_rng(7)
    drone = sum(a * np.sin(2 * np.pi * f * t + p) * (0.75 + 0.25 * np.sin(2 * np.pi * lf * t))
                for f, a, p, lf in [(55, .5, 0, .05), (82.4, .32, 1, .07), (110.3, .2, 2, .04), (164.8, .08, .5, .09)])
    noise = np.cumsum(rng.standard_normal(n)); noise -= np.convolve(noise, np.ones(2000) / 2000, "same")
    x = 0.030 * drone + 0.004 * noise / (np.abs(noise).max() + 1e-9) * 6
    for b in beats:
        i = int(b * SR); m = int(1.5 * SR); tt = np.arange(m) / SR
        sweep = np.sin(2 * np.pi * (70 * tt + 60 * tt ** 2)) * (tt / 1.5) ** 2 * 0.10
        hit = np.sin(2 * np.pi * 48 * tt) * np.exp(-tt * 5) * 0.30
        j = max(0, i - int(0.9 * SR))
        x[j:j + m] += sweep[:max(0, min(m, n - j))]
        x[i:i + m] += hit[:max(0, min(m, n - i))]
    for k in ticks:
        i = int(k * SR); m = int(0.25 * SR); tt = np.arange(m) / SR
        x[i:i + m] += (np.sin(2 * np.pi * 880 * tt) * np.exp(-tt * 28) * 0.05)[:max(0, min(m, n - i))]
    fade = int(1.2 * SR); x[-fade:] *= np.linspace(1, 0, fade); x[:int(.05 * SR)] *= np.linspace(0, 1, int(.05 * SR))
    return x.astype(np.float32)


STRETCH = float(os.environ.get('STRETCH', '1.0'))


def build(ep, S):
    sp = os.path.join(ep, "voice", "fix.json")
    starts = json.load(open(sp)) if os.path.exists(sp) else {}
    t = LEAD; place, lines, chapters = [], [], []
    for g, chs in enumerate(S.GROUPS):
        x, _ = sf.read(os.path.join(ep, "voice", f"g{g}.wav"), dtype="float32")
        gl = group_lines(S, g)
        segs = get_cuts(ep, S, g, x)
        wp = os.path.join(ep, "voice", "words.json")
        gw = json.load(open(wp)).get(str(g)) if os.path.exists(wp) else None
        k = 0
        for c in chs:
            ch = S.CHAPTERS[c]; beat = None
            if c > 0:
                beat = (round(t, 3), round(t + BEAT, 3)); t += BEAT
            c_start = t if c else 0.0
            for li, line in enumerate(ch["lines"]):
                a, b, gap = segs[k]; lw = gw[k] if gw else None; k += 1
                s = x[int(max(0, a - 0.02) * SR):int((b + 0.05) * SR)].copy()
                spans = []; s = squeeze(s, spans); scale = 1.0
                f = int(0.008 * SR); s[:f] *= np.linspace(0, 1, f); s[-f:] *= np.linspace(1, 0, f)
                if c == 0 and li == 0 and len(s) / SR > 1.85:   # hook rule: the hook line ends before 2.0 s
                    tmp = os.path.join(ep, "voice", "hook")
                    sf.write(tmp + "_in.wav", s, SR)
                    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", tmp + "_in.wav", "-filter:a", f"atempo={len(s) / SR / 1.72:.3f}", tmp + "_out.wav"], check=True)
                    n_in = len(s); s, _ = sf.read(tmp + "_out.wav", dtype="float32"); scale = len(s) / n_in
                elif STRETCH != 1.0:   # slow the read a little when the episode runs short (hook excluded)
                    tmp = os.path.join(ep, "voice", "st")
                    sf.write(tmp + "_in.wav", s, SR)
                    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", tmp + "_in.wav", "-filter:a", f"atempo={STRETCH:.3f}", tmp + "_out.wav"], check=True)
                    n_in = len(s); s, _ = sf.read(tmp + "_out.wav", dtype="float32"); scale = len(s) / n_in
                d = len(s) / SR
                cap = (line[2] if len(line) > 2 else line[0])
                # word timings: spread the words over the voiced islands of this line
                sil = [q for q in silences(s, 0.16) if q[0] > 0.02 and q[1] < d - 0.02]
                edges = [0.0] + [v for q in sil for v in q] + [d]
                isl = [(edges[k], edges[k + 1]) for k in range(0, len(edges), 2)]
                voiced = sum(b - a for a, b in isl); ws = cap.split(); tot = sum(len(w) + 1 for w in ws); acc = 0.0; words = []
                def at(v):
                    for a, b in isl:
                        if v <= b - a: return a + v
                        v -= b - a
                    return d
                for w in ws:
                    a0 = at(acc); acc += voiced * (len(w) + 1) / tot; words.append([round(t + a0, 3), round(t + at(acc), 3), w])
                if lw:   # real timings from the aligner, moved through the pause squeeze and the hook speed-up
                    mp = lambda v: min(d, max(0.0, (v - sum(min(max(v - ca, 0.0), cb - ca) for ca, cb in spans)) * scale))
                    words = [[round(t + mp(wa), 3), round(t + mp(wb), 3), w] for wa, wb, w in lw]
                lines.append(dict(ch=c, i=li, text=cap, visual=line[1], start=round(t, 3), end=round(t + d, 3), words=words))
                place.append((t, s)); t += d + float(np.clip(gap, GAP_MIN, GAP_MAX))
            chapters.append(dict(i=c, label=ch["label"], tag=ch["tag"], accent=ch["accent"], beat=beat,
                                 start=round(c_start if beat is None else beat[0], 3), end=round(t, 3)))
            t += 0.25
    total = t + TAIL
    voice = np.zeros(int(total * SR) + 1, dtype=np.float32)
    for st, s in place:
        i = int(st * SR); voice[i:i + len(s)] += s
    voice = voice / max(1e-6, np.abs(voice).max()) * 0.92
    odds = [(l["start"] + 0.3, l["visual"][1]) for l in lines if l["visual"][0] in ("odds", "final")]
    b = bed(len(voice) / SR + 1, [c["beat"][0] for c in chapters if c["beat"]], [o[0] for o in odds])[:len(voice)]
    b[-int(1.2 * SR):] *= np.linspace(1, 0, int(1.2 * SR))
    mix = voice + b
    mix = np.clip(mix, -0.99, 0.99)
    sf.write(os.path.join(ep, "voice", "final.wav"), mix, SR)
    json.dump(dict(total=round(total, 3), title=S.TITLE, start_odds=S.START_ODDS, chapters=chapters, lines=lines),
              open(os.path.join(ep, "timeline.json"), "w"), ensure_ascii=False, indent=1)
    print(f"total {total:.1f} s = {total / 60:.2f} min; hook ends at {lines[0]['end']:.2f} s")


if __name__ == "__main__":
    ep, cmd = sys.argv[1], sys.argv[2]
    S = load_script(ep)
    if cmd == "tts":
        for g in ([int(a) for a in sys.argv[3:]] or range(len(S.GROUPS))): tts(ep, S, g)
    elif cmd == "align":
        sp = os.path.join(ep, "voice", "starts.json")
        st = json.load(open(sp)) if os.path.exists(sp) else {}
        for g in ([int(a) for a in sys.argv[3:]] or range(len(S.GROUPS))):
            st[str(g)] = asr_starts(ep, S, g); print(f"g{g}:", st[str(g)])
            json.dump(st, open(sp, "w"))
    elif cmd == "autocut":
        for g in ([int(a) for a in sys.argv[3:]] or range(len(S.GROUPS))): autocut(ep, S, g)
    elif cmd == "kokoro":
        for g in ([int(a) for a in sys.argv[3:]] or range(len(S.GROUPS))): tts_kokoro(ep, S, g)
    elif cmd == "psalign":
        kb = os.path.join(ep, "voice", "kokoro_bounds.json")
        for g in ([int(a) for a in sys.argv[3:]] or range(len(S.GROUPS))): (psalign_lines if os.path.exists(kb) else psalign)(ep, S, g)
    elif cmd == "fixline":
        fixline(ep, S, int(sys.argv[3]), int(sys.argv[4]))
    elif cmd == "check":
        for g in ([int(a) for a in sys.argv[3:]] or range(len(S.GROUPS))): check(ep, S, g)
    elif cmd == "build":
        build(ep, S)
