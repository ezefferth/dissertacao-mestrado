import math, sys, os

def carregar(p):
    with open(p) as f:
        next(f, None)
        return [int(x)/1000.0 for x in f if x.strip().lstrip("-").isdigit()]

def detect(ecg, fs=640, tf=4):
    N = len(ecg); M = 10; FC = 0.08
    window = int(140*fs/1000)
    # 1) derivada
    d = [0.0]*N
    for n in range(1, N): d[n] = ecg[n]-ecg[n-1]
    # 2) janela-sinc LP
    H=[0.0]*M; m2=M//2
    for i in range(M):
        H[i] = (2*math.pi*FC) if i==m2 else math.sin(2*math.pi*FC*(i-m2))/(i-m2)
        H[i]*= (0.54-0.46*math.cos(2*math.pi*i/M))
    s=sum(H); H=[h/s for h in H]
    f=[0.0]*N
    for j in range(M-1,N):
        acc=0.0
        for i in range(M): acc+=d[j-i]*H[i]
        f[j]=acc
    # 3) limiares adaptativos
    pos=[x for x in f if x>0]; neg=[x for x in f if x<0]
    mvp=sum(pos)/len(pos) if pos else 0; mvn=sum(neg)/len(neg) if neg else 0
    t1=tf*mvp; t2=tf*mvn
    g=[0.0]*N
    for i in range(N):
        if f[i]>0 and f[i]<t1: g[i]=0
        elif f[i]<0 and f[i]>t2: g[i]=0
        else: g[i]=f[i]
    # separa
    xp=[v if v>0 else 0.0 for v in g]; xn=[v if v<0 else 0.0 for v in g]
    # 5) extremos locais em janelas
    pe=[]; i=0
    while i<N:
        we=min(i+window,N); mv=0.0; mi=-1
        for n in range(i,we):
            if xp[n]>mv: mv=xp[n]; mi=n
        if mi!=-1 and mv>0 and len(pe)<100: pe.append((mi,mv))
        i+=window
    ne=[]; i=0
    while i<N:
        we=min(i+window,N); mv=0.0; mi=-1
        for n in range(i,we):
            if xn[n]<mv: mv=xn[n]; mi=n
        if mi!=-1 and mv<0 and len(ne)<100: ne.append((mi,mv))
        i+=window
    # 6) junta, ordena, pares de polaridade oposta < window
    allx=sorted(pe+ne, key=lambda e:e[0])
    pares=0
    for i in range(len(allx)-1):
        e1=allx[i]; e2=allx[i+1]
        if (e1[1]>0 and e2[1]<0) or (e1[1]<0 and e2[1]>0):
            if (e2[0]-e1[0])<window: pares+=1
    return pares

for p in sys.argv[1:]:
    ecg = carregar(p)
    print(os.path.basename(p))
    for tf in [4, 3, 2, 1.5, 1.0, 0.8]:
        pares = detect(ecg, tf=tf)
        bpm = pares/(len(ecg)/640.0)*60
        print(f"  tf={tf:<4} pares={pares:3d}  bpm~{bpm:5.0f}")
