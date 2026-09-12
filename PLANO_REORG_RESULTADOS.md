# Plano de reorganização do Capítulo 4 (Resultados e Discussão)

Base: sugestão do orientador (5 partes a partir do 4.5) + decisões do autor
(abandonar a numeração das 14 baterias; empurrar o fluxo ponta a ponta para
depois dos testes de ECG; dissolver o atual 4.9; fechamento geral no fim).
Estado de partida: `4_resultados.tex` com 11 seções e 669 linhas (ver `dissertacao.toc`).

---

## 1. Mapeamento bateria → parte do orientador (verificado nos dados)

Proveniência confirmada pelas datas dos arquivos em `dados/` e pelos relatórios
em `app/node/test/BATERIA*.md`:

| Lote de ECG | Data dos arquivos | Onde foi usado |
|---|---|---|
| **Lote inicial** (com erro de bloqueio/parada e BPM nos limiares) | 07–10/07/2026 (`arquivosParaColetar/`, `proxima_bancada/`, `bateria4*`, `bateria5_final/`, `bateria 7/`) | baterias 1, 2, 4, 4b, 5, 7 |
| **Lote final** (o que o orientador manda usar) | 24/07/2026 (`bancada7ou9/`), reconvertido em 28/07 e 30/07 (`bateria 11/`, `bateria 13/`) | baterias 9, 10, 11, 12, 13, 14 |

| Parte sugerida | Ensaios que a sustentam | Seções atuais |
|---|---|---|
| **1 — ECG do próprio autor** | coletas DIAG de 25–26/06 e 30/06; sessões em decúbito e sentado | 4.5 + 4.8.1 |
| **2 — ECG sintético gerado neste trabalho** | bateria 3 (soma de gaussianas) e bateria 5 (molde do batimento + ritmo sintetizado); diagnóstico da perda de amostras | 4.9.2, 4.9.3, 4.9.5 |
| **3 — ECG do orientador, algoritmo original** | bateria 9 (limpo, 4 classes × 30 = 120 + 2 classes de pausa remontadas × 30) e bateria 10 (ruído, 6 × 9 × 30 = 1.620; 93,5 %) | 4.9.7 (+ parte de 4.9.8) |
| **4 — ECG do orientador, versão final** | bateria 13 (limpo, 180/180) e bateria 14 (ruído, 1.500/1.620 = 92,6 %); baterias 11/12 como evidência do efeito isolado de cada revisão | 4.10.1, 4.10.4, 4.10.5 |
| **5 — ECG real de banco público** | bateria 6 (algoritmo isolado, 60 segmentos, 81,7 %), bateria 8 (cadeia completa, 150 ensaios) e reavaliação nas três configurações (81,7 → 71,7 → 85,0 %) | 4.9.6 |

---

## 2. Estrutura proposta

```
4.1  Construção do Protótipo do Dispositivo                      (mantém)
4.2  Desenvolvimento do Firmware Embarcado                        (mantém, ver nota A)
4.3  Configuração da Rede LoRaWAN e Transmissão de Dados          (mantém)
4.4  Determinação da Taxa de Amostragem Efetiva                   (mantém)

4.5  Aquisição do ECG do próprio autor                      ← PARTE 1
     4.5.1  Ausência da referência de modo comum e correção do RLD
     4.5.2  Efeito do RLD sobre a interferência de 60 Hz
     4.5.3  Especificidade do critério de arritmia sinusal em repouso

4.6  Ensaios com ECG sintetizado neste trabalho             ← PARTE 2
     4.6.1  Perda periódica de amostras na aquisição e sua correção
     4.6.2  Desempenho sobre ECG sintetizado e ressalvas do resultado

4.7  Ensaios com o ECG cedido pelo orientador — versão original do algoritmo   ← PARTE 3
     4.7.1  Desempenho sobre ECG sem ruído
     4.7.2  Desempenho sob ruído somado
     4.7.3  Causa da falha sob interferência de rede a 30 %

4.8  Limitações identificadas e modificações implementadas  ← seção de consolidação
     4.8.1  Critério de pausa: da duração absoluta à razão com o R-R de base
     4.8.2  Teto do critério de arritmia sinusal
     4.8.3  Cobertura dos critérios e a sexta classe (anomalia não caracterizada)
     4.8.4  Filtro rejeita-faixa de 60 Hz: avaliado e não adotado
     4.8.5  Procedimento de teste: descontinuidade entre segmentos e disparo único

4.9  Ensaios com o ECG cedido pelo orientador — versão final do algoritmo     ← PARTE 4
     4.9.1  Desempenho sobre ECG sem ruído
     4.9.2  Desempenho sob ruído e comparação pareada com 4.7.2

4.10 Ensaios com ECG real de banco público (MIT-BIH)        ← PARTE 5
     4.10.1  Desempenho do algoritmo isolado
     4.10.2  Desempenho da cadeia completa (comparação pareada)
     4.10.3  Efeito das revisões do critério sobre o ECG real

4.11 Validação do Fluxo de Dados de Ponta a Ponta           (vem do atual 4.6)
4.12 Verificação do Aplicativo Móvel                        (vem do atual 4.7)
4.13 Detecção na Borda e Redução do Payload                 (vem do atual 4.8)
4.14 Considerações sobre os Resultados                      (fechamento geral, reescrito)
```

Nota A: o parágrafo do 4.2 que descreve a saturação do enlace serial deve sair de
lá e virar o primeiro problema da parte 1 ou 2 (é depuração de aquisição, não
descrição de firmware). O 4.2 fica com o que é entrega: aquisição por interrupção,
cadeia de filtros, LittleFS, montagem do payload.

---

## 3. O que sai do texto

| Conteúdo atual | Destino |
|---|---|
| 4.9 (seção-guarda-chuva) e os dois parágrafos que justificam relatar a progressão na íntegra | **removidos**; a justificativa passa a ser uma frase na abertura de 4.5 |
| Tabela `tab:progressaoBaterias` e figura `fig:progressaoBaterias` (progressão das 5 baterias) | **removidas** (são a estrutura cronológica que o orientador quer dissolver) |
| 4.9.1 Fronteira dos limiares (baterias 1 e 2) e matriz `tab:matrizInicial` | **removidas**; sobrevivem 3 frases em 4.8.5 justificando o descarte do lote inicial: normal a 60,0 bpm (R-R = 1000 ms, margem nula contra o limiar de bradicardia), taqui a 101 bpm (R-R = 594 ms, a 6 ms do limiar) e pausas fora de qualquer faixa do critério |
| 4.9.4 Baterias com o banco externo (4 e 4b; 60,6 % e 65,0 %) | **removida como resultado**; o artefato da descontinuidade vai para 4.8.5 sem taxa de acerto |
| 4.10.1 Décima primeira e décima segunda baterias (seções próprias) | **dissolvidas** em 4.8.1/4.8.2 como evidência do efeito de cada revisão (0/30 → 30/30 nas pausas, com os mesmos arquivos) e em 4.9.2 (efeito colateral sob 60 Hz) |
| Tabela `tab:bat12x14` (comparação pareada 12 × 14) | **reduzida a uma frase** em 4.9.2 |
| Todos os ordinais de bateria ("décima segunda bateria" etc.) | substituídos pela identificação por ECG + configuração; rastreabilidade preservada em **uma** tabela (início de 4.5 ou apêndice) ligando cada ensaio ao diretório `dados/bateria N/` |

Saldo estimado: de 11 seções/22 subseções para 10 seções/16 subseções, com queda
de 4 tabelas e 1 figura, e sem perda de nenhum fato medido.

---

## 4. Pontos de fricção com a sugestão (precisam de decisão)

### F1. A parte 3, como descrita, não existe em bancada
O orientador pede a parte 3 com o lote final de julho **e** o procedimento inicial
(descontinuidade entre segmentos). Mas as baterias em reprodução contínua (1, 2, 4,
4b) usaram o **lote inicial**, e as baterias com o lote final (9, 10) já empregavam
disparo único. Não existe a combinação pedida.

Há, porém, evidência melhor do que parecia: o ensaio prévio da bateria 9, com o
lote final **antes** da truncagem no último ciclo completo, classificou um dos dois
segmentos normais como arritmia (`flags=0x04`, R-R de 936 ms contra 951 ms),
exatamente pelo artefato da junção (`BATERIA9.md`). Isso permite documentar a
descontinuidade **com o lote que ele manda usar**, sem refazer bancada.

- **Opção A (recomendada):** relatar a descontinuidade em 4.8.5, com a evidência do
  ensaio prévio da bateria 9 + a aritmética dos arquivos (30 s não contêm número
  inteiro de ciclos: normal 31,51; taqui 52,45; bradi 28,52 ciclos), sem taxa de acerto.
- **Opção B:** refazer uma bateria em laço com o lote final para produzir o número.
  Custo: regravar o firmware da configuração original + ~1 h de bancada por classe.

### F2. As classes de pausa da parte 3 não são arquivos dele
Sob o critério absoluto (duas pausas de 4 a 6 s), as pausas do lote final — 1904 ms
(2×R-R) e 2856 ms (3×R-R) — não alcançavam o piso. Os ECGs de bloqueio e parada da
bateria 9 foram **remontados** a partir do `Normal.csv` dele (batimentos dele +
ciclos de silêncio dele). Isso precisa aparecer declarado em 4.7.1, e a afirmação
de "procedência integral" passa a valer só para a parte 4.

### F3. O "0/30" hoje no texto não tem coleta de 30 repetições
A linha 509 de `4_resultados.tex` afirma que os arquivos de bloqueio e parada "não
foram reconhecidos em nenhum dos 30 segmentos" na bateria 9. O que existe é um
ensaio de **2 repetições** (0/2, `flags=0x06` → bradicardia) mais o argumento
determinístico: nenhuma das pausas alcança o piso de 4 s. Reformular para "0/2 em
ensaio prévio, resultado determinístico pela definição do critério" ou coletar os
30. Nota: a referência `\ref{sec:resRevisaoEstimulos}` dessa mesma linha aponta para
um label que **não existe mais** no arquivo.

### F4. A seção 4.9.8 (notch) começa truncada
O texto de `sec:resNotch` abre com "A causa é de outra ordem." — falta o parágrafo
que enuncia o problema. Precisa ser reescrito ao migrar para 4.8.4.

### F5. O molde do ECG sintetizado vem do lote inicial
A bateria 5 (parte 2) usa como molde morfológico o batimento do lote inicial, com
ritmo e pausas sintetizados aqui. O defeito que o orientador aponta no lote inicial
é de **ritmo e pausas**, não de morfologia do batimento, de modo que ele não se
propaga — mas isso deve ser dito explicitamente em 4.6.2.

---

## 5. Avaliação dos critérios de classificação propostos

Conferidos contra `app/node/ECG_abnormal.cpp` e `ECG_abnormal.h`.

| Critério proposto | Implementado hoje | Situação |
|---|---|---|
| taqui: RR_base < 0,6 s | `RR_TAQUI = 600` ms | **igual** (observação: taqui/bradi usam o R-R **médio**, não a mediana) |
| bradi: RR_base > 1,0 s | `RR_BRADI = 1000` ms | **igual** |
| arritmia: ΔRR > 0,12 s | `drr > 120` ms | **igual** |
| arritmia: teto ΔRR < 1,9·RR_base | `drr < 0,8 · rr_ref` | **divergente — ver abaixo** |
| bloqueio: 1,9–2,1 e 2,85–3,15 RR_base | `|razão/2 − 1| ≤ 0,05` ou `|razão/3 − 1| ≤ 0,05` | **igual** (±5 % em torno de 2× e 3×) |
| parada: > 3,15·RR_base | `razão > 3,0 · 1,05` | **igual** |
| faixa descoberta 2,1–2,85 | `razão ≥ 1,5` e não contada como arritmia → não caracterizada | **igual**, e mais ampla (cobre também 1,80–1,89) |

Três observações a levar ao orientador:

1. **Diferença × razão.** Ele escreve os critérios de pausa em `|RR_n+1 − RR_n|`. O
   implementado usa `RR_n / RR_base` — a razão do próprio intervalo com a mediana.
   Tomada literalmente, a formulação em diferença desloca todas as faixas em um
   RR_base: uma pausa de 2·RR_base produz `|ΔRR| = 1,0·RR_base`, que não cai em
   1,9–2,1. A varredura de `test/varre_zona_morta.py` e a Tabela da zona morta
   (1,90–2,05 → bloqueio; 3,15–3,70 → parada) confirmam que é a razão que está
   implementada e validada. Vale pedir confirmação de que a intenção é a razão.

2. **Teto da arritmia: 0,8 e não 1,9.** Com teto de 1,9·RR_base em ΔRR, a pausa de
   2·RR_base (ΔRR = 1,0·RR_base) volta a ser contada como arritmia — exatamente a
   contaminação que a revisão de 28/07 eliminou e que obrigava a suprimir a arritmia
   à força nos segmentos com pausa. Medido no banco de validação, o teto de 0,8
   zera a contagem nos segmentos de bloqueio e parada e preserva a arritmia sinusal
   legítima (é por isso que a matriz da bateria 11 saiu com um único bit ativo por
   segmento). **Recomendação: manter 0,8·RR_base** (equivale a razão de pausa < 1,8).

3. **Suprimir a sexta classe: não recomendado.** Chamar a faixa 2,1–2,85 de "parada
   sinusal" faria o sistema afirmar um diagnóstico que a definição clínica não
   sustenta, com a mesma conduta subsequente (inspeção do traçado). A sexta classe
   já está implementada, validada sem efeito colateral (baterias 13/14: 180/180 no
   limpo, nenhuma ativação indevida; 1.500/1.620 sob ruído, idêntico à 12ª) e é o
   que eleva o MIT-BIH de 71,7 % para 85,0 %. Detalhe a explicitar para ele: na
   faixa 2,50–2,80 o rótulo exibido sai como **bradicardia** (a pausa desloca o R-R
   médio), com a flag de não caracterizada preservada na máscara.

4. **"Aumento de ordem de filtro" não foi implementado.** Ele cita isso entre as
   modificações. O passa-baixas segue de 1ª ordem; o que se avaliou foi o filtro
   rejeita-faixa de 60 Hz, **descartado** por não haver ganho líquido. A seção 4.8.4
   deve registrar isso como modificação avaliada e rejeitada, não como implementada.

---

## 6. Terminologia: "estímulo" → "ECG"

86 ocorrências (4_resultados 57, A_figuras_ruido 21, 3_met 6, resumo 1, conclusões 1).
Substituições propostas, preservando a precisão:

| Hoje | Proposto |
|---|---|
| banco de estímulos externo | conjunto de sinais de ECG cedido pelo orientador |
| estímulo de taquicardia | ECG de taquicardia |
| classes de estímulo | classes de ECG |
| estímulo limpo / perturbado | ECG sem ruído / com ruído somado |
| estímulos sintéticos | ECG sintetizado |
| procedência integral dos estímulos | procedência integral dos sinais de ECG |

Manter "estímulo" apenas onde o objeto é o sinal elétrico injetado na entrada do
AFE e não o ECG em si (por exemplo: "onda quadrada de teste interna do ADS1293").

---

## 7. Efeitos fora do capítulo 4

- **3.6 / 3.6.1 (Metodologia).** Fica na Metodologia o que é método estável: bancada
  com myDAQ, divisor resistivo, atenuação de ~2000:1, gabarito, métricas (matriz de
  confusão, sensibilidade, especificidade, VPP, VPN, MAE de FC). **Migra para 4.8.5**
  o que é decisão tomada em resposta a resultado: adoção do disparo único, truncagem
  no último ciclo completo, reamostragem 500 → 640 SPS abandonada. Hoje a 3.6.1
  narra a depuração ("a partir da sétima bateria...") e, com isso, antecipa
  resultado dentro da metodologia.
- **Capítulo 5 (Conclusões).** Reordenar na mesma sequência das 5 partes; as
  limitações já existentes continuam válidas, mas as referências de seção mudam.
- **Resumo.** Revisar por último, conforme ele pediu.
- **Labels.** Renomear os `sec:res*` para refletir a nova ordem e corrigir as
  referências vindas de 3_met.tex, 7_conclusoes.tex e A_figuras_ruido.tex.
