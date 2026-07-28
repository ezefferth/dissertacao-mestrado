# Sistema de ECG com transmissão LoRaWAN — resumo do que foi feito

**Ezefferth · Mestrado UFMS · Julho/2026**

Dissertação: *Desenvolvimento de Sistema Embarcado para Aquisição e Transmissão de Sinais de ECG em Redes LoRaWAN*.

O algoritmo de detecção embarcado **não é contribuição deste trabalho**: é o firmware de
Moraes, Iaione e Spalding (SEMISH 2026, p. 251–262), cedido pelos autores. A contribuição
está na aquisição, na integração do detector ao embarcado, no armazenamento local e,
sobretudo, na **transmissão dos eventos em LoRaWAN** + infraestrutura de rede e aplicativo.

---

## 1. O que foi construído

| Item | Solução | Situação |
|---|---|---|
| Dispositivo | XIAO ESP32-S3 + AFE ADS1293 (CJMCU-1293) + Wio-SX1262, bateria Li-ion, caixa 3D | Funcional |
| Aquisição | 3 derivações por SPI, IRQ de *Data Ready*, **640 SPS** (confirmado por medição e pela cadeia de divisores do ADS1293) | Funcional |
| Condicionamento | IIR passa-baixa 40 Hz + passa-alta 0,5 Hz; RLD de 3 eletrodos (`CMDET_EN=0x05`, `SELRLD=010`) | Funcional |
| Detecção na borda | Firmware de Moraes et al., segmentos de 30 s (19.200 amostras em PSRAM) | Integrado |
| Armazenamento local | LittleFS: resumo de 16 B por segmento + forma de onda dos segmentos anormais | Funcional |
| Rede | Gateway Radioenge + **ChirpStack local** em Raspberry Pi 3, AU915 sub-banda 2, OTAA | Funcional |
| Transmissão | Payload de **10 bytes** por segmento, 1 uplink/30 s, porta 2 | Funcional |
| Nuvem / app | Ingestor MQTT → Firestore → app React Native/Expo em tempo real, com push de alerta | Funcional |

**Decisão central — detecção na borda.** Enviar a forma de onda de 30 s custaria 38.400 bytes;
num teste, 15.000 amostras levaram **392 s** para transmitir (2–3 s por pacote), inviável.
O resumo de 10 bytes reduz o volume em mais de três ordens de grandeza e cabe em um uplink.

---

## 2. Como foi validado

Injeção de sinais de classe conhecida pelo gerador NI myDAQ, 30 segmentos de 30 s por classe
(180 ensaios por bateria). Não houve um experimento único: foram **dez baterias**, cada uma
expondo uma limitação diferente, cuja correção orientou a seguinte.

| # | Estímulo | Acurácia | O que a bateria revelou |
|---|---|---|---|
| 1 | Real (gerador), ritmo na fronteira dos limiares | 67,8 % | Baixa especificidade da arritmia; taqui a 101 bpm (6 ms do limiar) |
| 2 | Taquicardia e bloqueio ajustados | 78,3 % | Traçado normal continuava errando → causa não era o estímulo |
| 3 | Sintético, longe dos limiares | 100 % | Limite superior otimista (R-R casado com a grade de amostragem) |
| 4 / 4b | ECG real do professor, na fronteira | 60,6 / 65,0 % | Emenda do laço do gerador; bradi 3,3 % → 100 % ao corrigir |
| 5 | Molde de *ensemble* real + jitter, deriva e modulação ±8 % | 100 % | Bateria final; morfologia realista com ritmo controlado |
| 6 | MIT-BIH, 60 segmentos direto no detector (sem aquisição) | 81,7 % | **Teto do método** sobre ECG real |
| 7 | 6 arquivos originais do professor, disparo único | 77,8 % | Falhas em 2 arquivos, ambas por posição do ritmo no limiar |
| 8 | Mesmos segmentos MIT-BIH pela cadeia completa (150 ensaios) | 100 % | **Custo da aquisição = nulo** (comparação pareada com a bat. 6) |
| 9 | 2º lote do professor, ritmos afastados das fronteiras | 120/120 | Arritmia foi de 0/30 → 30/30, confirmando a predição da bat. 7 |
| 10 | Seis classes × 3 ruídos × 3 amplitudes (1.620 ensaios) | 93,5 % | Robustez; falha isolada sob rede de 60 Hz a 30 % |

> O resultado com peso científico **não é o 100 % de nenhuma bateria isolada**, e sim o
> contraste entre elas: o salto da 2ª para a 3ª isolou um defeito de firmware; a queda na 4ª
> e a recuperação na 5ª isolaram um artefato do banco de estímulos; o par 6 ↔ 8 separou a
> limitação do *método* do custo da *aquisição*.

### 2.1 Bateria final (nº 5) — matriz de confusão

| Esperada \ Detectada | Normal | Taqui. | Bradi. | Arrit. | Bloq. | Parada |
|---|---|---|---|---|---|---|
| Normal | **30** | 0 | 0 | 0 | 0 | 0 |
| Taquicardia | 0 | **30** | 0 | 0 | 0 | 0 |
| Bradicardia | 0 | 0 | **30** | 0 | 0 | 0 |
| Arritmia sinusal | 0 | 0 | 0 | **30** | 0 | 0 |
| Bloqueio sinoatrial | 0 | 0 | 0 | 0 | **30** | 0 |
| Parada sinoatrial | 0 | 0 | 0 | 0 | 0 | **30** |

Erro de estimativa de FC (não-nulo, por não haver alinhamento artificial com a grade):

| Classe | Erro médio abs. | Erro máx. | Desvio-padrão |
|---|---|---|---|
| Normal | 0,4 bpm | 1,0 | 0,5 |
| Taquicardia | 0,2 bpm | 1,0 | 0,4 |
| Bradicardia | 0,5 bpm | 1,0 | 0,5 |

### 2.2 MIT-BIH (bateria 6) — 60 segmentos, 15 por classe

| Esperada \ Detectada | Normal | Taqui. | Bradi. | Arrit. |
|---|---|---|---|---|
| Normal | **11** | 0 | 0 | 4 |
| Taquicardia | 0 | **11** | 0 | 4 |
| Bradicardia | 0 | 0 | **13** | 2 |
| Arritmia sinusal | 0 | 1 | 0 | **14** |

Das 11 falhas, **10 são detecções de arritmia sobre outras classes** (VPP da arritmia = 58 %).
É a mesma baixa especificidade descrita abaixo, agora sobre ECG real.

### 2.3 Robustez ao ruído (bateria 10) — 1.620 ensaios

| Perturbação | 10 % | 20 % | 30 % |
|---|---|---|---|
| Deriva respiratória (0,33 Hz) | 100 % | 100 % | 100 % |
| Rede elétrica (60 Hz) | 100 % | 100 % | **50 %** |
| Aleatório de banda larga | 99,4 % | 100 % | 92,2 % |

Sob 60 Hz a 30 %, normal/taqui/arritmia caem a 0/30 (perda de picos R eleva o R-R médio em
22 %); bradicardia, bloqueio e parada permanecem em 100 %, por não dependerem da contagem
exata de picos.

**Notch de 60 Hz — testado e descartado.** Biquad de 2ª ordem, dois fatores de qualidade.
Recupera taquicardia e arritmia sob 30 %, mas o transitório do filtro injeta ~2 picos
espúrios por segmento e quebra a bradicardia sob 20 % e 30 %. O nº de condições em falha não
diminui — o filtro só redistribui quais classes falham. Mantida a cadeia original. A conclusão
é que a rejeição de rede é atribuição do **estágio analógico** (CMRR + RLD), não do filtro
digital; a bancada injeta a rede em modo **diferencial**, contornando de propósito essa defesa,
o que torna o ensaio mais severo que o uso real.

---

## 3. Dois defeitos de aquisição encontrados e corrigidos

Ambos se manifestavam como *arritmia falsa* em sinal regular, e ambos estavam na aquisição,
não no detector:

1. **Saturação da serial** — imprimir as 3 derivações a cada amostra bloqueava o laço e
   derrubava a taxa de 640 para ~560 SPS. Corrigido por decimação da saída de depuração.
2. **`LittleFS.usedBytes()` dentro do `loop()`** — a cada 5 s bloqueava o processador por
   ~105 ms, colapsando ~67 amostras (perda de 2,08 %). Comprimia o R-R de 800 para ~710 ms,
   variação de 89–114 ms, muito próxima do limiar de arritmia de 120 ms. Corrigido
   desacoplando o diagnóstico do laço de aquisição.

O segundo caso também explicava a "taxa aparente de 627 SPS": chegou-se a cogitar recalibrar
o firmware para 627, o que teria **mascarado o defeito** em vez de corrigi-lo. Os 640 SPS
sempre estiveram certos.

---

## 4. Limitação conhecida — arritmia sinusal

O critério marca o segmento quando há ≥1 variação batimento-a-batimento do R-R > 120 ms. Em
repouso, a arritmia sinusal **respiratória** (fisiológica, benigna) produz por si só 8–15
dessas variações por segmento de 30 s. Em teste no próprio autor:

| Condição | FC média | Variações R-R > 120 ms/segmento | Segmentos sinalizados |
|---|---|---|---|
| Decúbito (repouso) | ≈67 bpm | ≈7,8 | 100 % |
| Sentado | ≈92 bpm | ≈8,6 | 100 % |

Taquicardia, bradicardia, bloqueio e parada **não** produziram falsos positivos.

**Decisões tomadas:** (a) a arritmia sinusal passou a ser tratada como informação de contexto,
com a menor prioridade na regra de colapso das flags — um segmento só é classificado como
arritmia quando essa é a *única* anomalia, para não mascarar taquicardia; (b) o app exige
**confirmação por persistência** (X de N segmentos) antes de promover a alarme, com janela
mais longa para arritmia e alarme imediato para as pausas. Nada disso alterou o detector.

---

## 5. Fluxo de ponta a ponta — validado

`dispositivo → LoRaWAN → ChirpStack → MQTT → ingestor → Firestore → app`

Seis payloads representativos (um por classe) foram publicados e, em todos, o ingestor
decodificou os campos, derivou o tipo de evento pela prioridade clínica
(parada > bloqueio > taquicardia > bradicardia > arritmia), gravou no Firestore e propagou em
tempo real ao app. Os registros do banco foram conferidos contra o log local do dispositivo,
sem divergências.

---

## 6. O que falta

- **Ensaios clínicos com pacientes** na Clínica Escola Integrada da UFMS (exige CEP) — é a
  limitação central e está no capítulo de conclusões como etapa subsequente.
- Testes de cobertura da rede e de autonomia energética.
- Refinamento do invólucro (ergonomia, segurança elétrica, fixação durante atividade física).
- Aprimoramento do estágio analógico de entrada para rejeição de rede (ver §2.3).

---

## 7. Situação do texto

Capítulos 1 a 5 escritos e compilando (93 páginas, sem referências pendentes). A referência
do artigo do Moraes foi inserida com os dados definitivos do SEMISH 2026. A atribuição do
detector aos autores originais consta do resumo, da introdução, do capítulo 2, do capítulo 3,
do capítulo 4 e das conclusões.
