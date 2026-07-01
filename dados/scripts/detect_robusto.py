import glob, os, statistics as st

def carregar(p):
    with open(p) as f:
        next(f, None)
        return [int(x)/1000.0 for x in f if x.strip().lstrip("-").isdigit()]

def detectar(v, fs=640, k=1.8, refrac_ms=300):
    """Picos R por amplitude (ambas polaridades) + período refratário."""
    n = len(v)
    mean = sum(v)/n
    dev = [abs(x-mean) for x in v]
    sd = st.pstdev(dev)
    thr = st.mean(dev) + k*sd
    refrac = int(refrac_ms/1000*fs)
    picos = []; i = 1; last = -refrac
    while i < n-1:
        if dev[i] > thr and dev[i] >= dev[i-1] and dev[i] >= dev[i+1] and (i-last) > refrac:
            picos.append(i); last = i; i += refrac
        else:
            i += 1
    return picos

print(f"{'arquivo':18} {'picos':>5} {'bpm':>5} {'rr_med':>7} {'rr_dp':>6} {'rr_dpr%':>7}")
for p in sorted(glob.glob(os.path.join(os.path.dirname(__file__), "raw_*.csv"))):
    v = carregar(p)
    pk = detectar(v)
    dur = len(v)/640.0
    bpm = len(pk)/dur*60 if dur else 0
    rr = [(pk[i+1]-pk[i])*1000/640 for i in range(len(pk)-1)]
    rrm = sum(rr)/len(rr) if rr else 0
    rrdp = st.pstdev(rr) if len(rr) > 1 else 0
    dpr = rrdp/rrm*100 if rrm else 0
    print(f"{os.path.basename(p):18} {len(pk):5d} {bpm:5.0f} {rrm:7.0f} {rrdp:6.0f} {dpr:7.1f}")
