# Catálogo de dados experimentais — ECG LoRaWAN (RhythmIQ)

Acervo de coletas, sinais e resultados usados na dissertação. **Não mover os CSVs**
(scripts e memória apontam para estes nomes). Para regenerar tabelas/figuras/métricas
após uma coleta nova, rodar:

```
C:\Work\mestrado\.venv\Scripts\python.exe scripts\gerar_resultados.py
```

## Estrutura

```
dados/
  CATALOGO.md            ← este arquivo (proveniência curada)
  diag_*.csv             ← coletas DIAG_MODE 1 (Lead I/II/III, mV)
  raw_*.csv              ← Lead II filtrado de segmentos anormais (via LittleFS)
  log.csv                ← resumo dos segmentos processados no firmware
  figuras/               ← figuras prontas para o LaTeX (.pdf) + PNGs
  resultados/            ← saídas do script (coletas.csv/.md, detector.json)
  scripts/               ← análise/geração (gerar_resultados.py + ad-hoc antigos)
```

## ⚠️ Duas escalas de conversão mV

- **Coletas de 25–26/jun (baseline ~305 mV):** fórmula antiga (offset DC não removido).
  A amplitude em mV **não é comparável** com as coletas novas. Servem como histórico.
- **Coletas de 30/jun (baseline ~0 mV):** já usam a **Eq.13 do datasheet ADS1293**
  (`mV = (raw/12.800.000 − 0,5)·1371,43`), centradas em zero e com escala fisiológica correta.

Só cite amplitudes em mV a partir das coletas Eq.13.

## Coletas DIAG (Lead II = derivação de detecção)

Métricas objetivas em `resultados/coletas.md` (regeneráveis). Papel curado:

| Arquivo | Escala | HR | rr_dp | Papel na dissertação |
|---|---|---|---|---|
| **`diag_20260630_204926.csv`** | Eq.13 | 87 bpm | 218 ms | **CANÔNICA** — sinal bom, Lead II vivo, escala correta. Base da figura cru×filtrado e do detector. |
| `diag_20260626_150408.csv` | antiga | 80 bpm | 229 ms | 1ª validação do sinal (ritmo regular ~77–80 bpm). Escala antiga. |
| `diag_20260630_203809.csv` | Eq.13 | — | 2810 ms | **Exemplo de FALHA:** lead-off no IN3 (cabo verde). Lead II morto → detecção pega só ruído. Escala correta. |
| `diag_20260630_203850.csv` | Eq.13 | — | 1992 ms | Idem (lead-off IN3, antes do reparo do cabo). |
| `diag_20260625_223703.csv` | antiga | — | irregular | Depuração de eletrodos/cabo (ruído/lead-off parcial). Histórico. |
| `diag_20260625_224556.csv` | antiga | — | irregular | Idem. |
| `diag_20260625_225438.csv` | antiga | — | irregular | Idem. |
| `diag_20260625_230227.csv` | antiga | — | irregular | Idem. |
| `diag_20260625_230755.csv` | antiga | — | irregular | Idem. |
| `diag_20260625_231955.csv` | antiga | — | irregular | Idem. |
| `diag_20260625_232138.csv` | antiga | — | irregular | Idem. |

> `rr_dp` (desvio-padrão do RR) discrimina bem: **~220 ms** nas boas × **>900 ms** quando é
> ruído/lead-off (o detector "conta" picos espúrios sem QRS real).

## Sinais brutos e log do firmware (26/jun)

- `raw_00000011.csv … raw_00000040.csv` (30 arquivos): Lead II **filtrado** de segmentos
  marcados anormais/erro, extraídos da flash (LittleFS), mV×1000, ~19200 amostras/30 s.
  Origem do diagnóstico do detector atual (dupla contagem → HR ~2× o real).
- `log.csv`: resumo por segmento (id, uptimeMs, bpm, rrMed, rrDp, picos, flags).
  Evidência dos bugs do detector `ECG_abnormal.cpp` (flags=0x80/erro dominante, bpm absurdos).

## Figuras

- `figuras/figura_raw_vs_filt.pdf` — ECG cru (DIAG 1) × filtrado (cascata IIR replicada em SW),
  derivação II, coleta canônica. Para o capítulo de resultados.
- `figuras/analise_diag_150408.png` — análise da 1ª validação do sinal.

## Resultados do detector

- `resultados/detector.json` — Pan-Tompkins na coleta canônica (protótipo Python).
  Estado atual: HR ~87 bpm correto, mas `rr_dp` ainda alto por 1 falso-positivo e 1
  batimento perdido → em refinamento antes de portar para `ECG_abnormal.cpp`.
- `resultados/coletas.csv` / `.md` — tabela de todas as coletas (regenerável).

## Rastreabilidade para a tese

Cada afirmação experimental deve citar o arquivo de origem. Referências principais:
- **Sinal de ECG válido:** `diag_20260630_204926.csv` → `figura_raw_vs_filt.pdf`.
- **Efeito dos filtros (offset DC + ruído):** mesma figura (cru × filtrado).
- **Falha por lead-off (importância do contato do eletrodo):** `diag_20260630_203809/203850.csv`.
- **Limitação do detector embarcado atual:** `log.csv` + `raw_*.csv`.
