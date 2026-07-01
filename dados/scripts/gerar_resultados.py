"""
gerar_resultados.py — Regenera TODOS os artefatos experimentais para a dissertação
a partir dos CSVs em dados/. Executar sempre que houver coleta nova.

Saídas (em dados/resultados/ e dados/figuras/):
  resultados/coletas.csv     — tabela de todas as coletas DIAG (baseline, HR, veredito)
  resultados/coletas.md      — mesma tabela em Markdown (para colar no CATALOGO/tese)
  resultados/detector.json   — métricas do detector Pan-Tompkins na coleta canônica
  figuras/figura_raw_vs_filt.(png|pdf) — ECG cru vs filtrado (via bench)

Uso:
  <.venv>/Scripts/python.exe gerar_resultados.py
Requer: numpy, scipy, matplotlib (venv em C:\\Work\\mestrado\\.venv).
"""
import os, glob, json, csv
import numpy as np
from scipy.signal import butter, filtfilt, find_peaks

FS = 640                                  # ODR real do ADS1293 (ver CLAUDE.md)
DADOS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(DADOS, "resultados")
FIG = os.path.join(DADOS, "figuras")
CANONICA = "diag_20260630_204926.csv"     # coleta de referência (Eq.13, Lead II vivo)

# Filtro IIR do firmware (réplica de applyFilter em node.ino, fs=640)
LP_ALPHA, HP_ALPHA = 0.3247, 0.9951


def col_leadII(path):
    d = np.genfromtxt(path, delimiter=",", names=True)
    name = [c for c in d.dtype.names if c.lower().startswith("leadii_")][0]
    return d[name].astype(float)


def filtro_firmware(x):
    y = np.empty_like(x); lp = hp = prev = 0.0
    for i, xi in enumerate(x):
        lp = LP_ALPHA*xi + (1-LP_ALPHA)*lp
        hp = HP_ALPHA*(hp + lp - prev); prev = lp
        y[i] = hp
    return y


def pan_tompkins(x, fs=FS):
    """Detector R-peak. Robusto a escala (limiar por MAD)."""
    x = x - np.median(x)
    b, a = butter(2, [5/(fs/2), 15/(fs/2)], btype="band")
    f = filtfilt(b, a, x)
    integ = np.convolve(np.diff(f, prepend=f[0])**2,
                        np.ones(int(0.15*fs))/int(0.15*fs), mode="same")
    thr = np.median(integ) + 5*np.median(np.abs(integ - np.median(integ)))
    pk, _ = find_peaks(integ, distance=int(0.25*fs), height=thr)
    # refina para o pico do sinal filtrado (±50 ms)
    w = int(0.05*fs)
    pk = sorted({max(0, i-w) + int(np.argmax(np.abs(f[max(0, i-w):i+w]))) for i in pk})
    return np.array(pk)


def metricas(pk, fs=FS):
    if len(pk) < 3:
        return dict(n_picos=len(pk), hr=None, rr_med=None, rr_dp=None)
    rr = np.diff(pk)/fs*1000
    return dict(n_picos=int(len(pk)), hr=round(60000/rr.mean(), 1),
                rr_med=round(rr.mean(), 1), rr_dp=round(rr.std(), 1),
                rr_min=round(rr.min(), 1), rr_max=round(rr.max(), 1))


def tabela_coletas():
    linhas = []
    for f in sorted(glob.glob(os.path.join(DADOS, "diag_*.csv"))):
        nome = os.path.basename(f)
        l2 = col_leadII(f)
        base = l2.mean()
        escala = "Eq.13 (0 mV)" if abs(base) < 50 else "antiga (~305 mV)"
        m = metricas(pan_tompkins(l2))
        # sem veredito categórico: rr_dp alto = ritmo irregular (ruído/lead-off).
        # A classificação do papel de cada coleta fica curada no CATALOGO.md.
        linhas.append(dict(arquivo=nome, n=len(l2), dur_s=round(len(l2)/FS, 1),
                           baseline_mV=round(base, 1), escala=escala,
                           hr_bpm=m["hr"], n_picos=m["n_picos"],
                           rr_dp_ms=m["rr_dp"]))
    return linhas


def salvar_tabela(linhas):
    os.makedirs(RES, exist_ok=True)
    campos = ["arquivo", "n", "dur_s", "baseline_mV", "escala",
              "hr_bpm", "n_picos", "rr_dp_ms"]
    with open(os.path.join(RES, "coletas.csv"), "w", newline="") as fp:
        w = csv.DictWriter(fp, fieldnames=campos); w.writeheader(); w.writerows(linhas)
    with open(os.path.join(RES, "coletas.md"), "w", encoding="utf-8") as fp:
        fp.write("| " + " | ".join(campos) + " |\n")
        fp.write("|" + "|".join(["---"]*len(campos)) + "|\n")
        for l in linhas:
            fp.write("| " + " | ".join(str(l[c]) for c in campos) + " |\n")


def figura():
    """Regenera a figura cru vs filtrado via o script do bench, se disponível."""
    bench = os.path.join(DADOS, "..", "app", "node", "test", "plot_raw_vs_filtered.py")
    canon = os.path.join(DADOS, CANONICA)
    if os.path.exists(bench):
        import subprocess, sys, shutil
        subprocess.run([sys.executable, bench, "--raw", canon,
                        "--lead", "LeadII", "--start", "2", "--secs", "6"], check=False)
        d = os.path.dirname(os.path.abspath(bench))
        for ext in ("png", "pdf"):
            src = os.path.join(d, f"figura_raw_vs_filt.{ext}")
            if os.path.exists(src):
                shutil.copy(src, os.path.join(FIG, f"figura_raw_vs_filt.{ext}"))


def main():
    os.makedirs(RES, exist_ok=True); os.makedirs(FIG, exist_ok=True)
    linhas = tabela_coletas()
    salvar_tabela(linhas)

    # detector na coleta canônica
    l2 = col_leadII(os.path.join(DADOS, CANONICA))
    det = dict(coleta=CANONICA, fs_sps=FS, detector="Pan-Tompkins",
               **metricas(pan_tompkins(l2)))
    with open(os.path.join(RES, "detector.json"), "w", encoding="utf-8") as fp:
        json.dump(det, fp, indent=2, ensure_ascii=False)

    figura()

    print(f"coletas analisadas: {len(linhas)}")
    print(f"detector (canônica {CANONICA}): {det}")
    print(f"artefatos em: {RES} e {FIG}")


if __name__ == "__main__":
    main()
