import glob, os, statistics as st

def carregar(p):
    with open(p) as f:
        next(f, None)
        return [int(x) for x in f if x.strip().lstrip("-").isdigit()]

def picos_simples(v, fs=640):
    if len(v) < fs: return 0
    mean = sum(v) / len(v)
    sd = st.pstdev(v)
    thr = mean + 2.5 * sd
    refrac = int(0.25 * fs)
    n = 0; last = -refrac
    for i in range(len(v)):
        if v[i] > thr and (i - last) > refrac:
            n += 1; last = i
    return n

print(f"{'arquivo':18} {'n':>6} {'dur_s':>6} {'min':>8} {'max':>8} {'mean':>7} {'sd':>7} {'picos~':>7} {'bpm~':>6}")
for p in sorted(glob.glob(os.path.join(os.path.dirname(__file__), "raw_*.csv"))):
    v = carregar(p)
    if not v:
        print(os.path.basename(p), "vazio"); continue
    dur = len(v) / 640.0
    npk = picos_simples(v)
    bpm = npk / dur * 60 if dur else 0
    print(f"{os.path.basename(p):18} {len(v):6d} {dur:6.1f} {min(v):8d} {max(v):8d} "
          f"{int(sum(v)/len(v)):7d} {st.pstdev(v):7.0f} {npk:7d} {bpm:6.0f}")
