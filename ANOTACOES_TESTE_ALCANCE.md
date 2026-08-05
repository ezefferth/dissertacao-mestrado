# Anotações — teste de alcance LoRaWAN e coleta em uso real

> Rascunho de planejamento. Registrado em 2026-08-05. **Nada aqui foi executado
> ainda.** Quando os dados existirem, o teste de alcance vira seção nova do
> capítulo 4; a coleta no corpo fica como material de defesa.

---

## 1. O que falta e por quê

As baterias 1 a 14 validaram aquisição, filtragem, detecção e o formato do
payload — mas **nenhuma mediu o alcance real do enlace LoRaWAN**. Esse é o
argumento central do título da dissertação ("Transmissão de Sinais de ECG em
Redes LoRaWAN"): sem número de cobertura, o capítulo de resultados prova o
processamento e não prova a transmissão à distância.

Dois experimentos distintos, que **não devem ser rodados juntos**:

| | Experimento A — Alcance | Experimento B — Uso real |
|---|---|---|
| O que mede | o enlace rádio | a cadeia completa num humano em movimento |
| Fonte do sinal | gerador / sinal sintético | ECG do próprio pesquisador |
| Destino | **capítulo 4 (texto)** | **apresentação de defesa** |
| Exige CEP | não | **sim — bloqueante** |

Motivo de separar: se um pacote falhar durante um passeio de bicicleta com
eletrodos no corpo, não há como distinguir perda por distância de artefato de
movimento no eletrodo. Um experimento contamina a leitura do outro.

---

## 2. Experimento A — alcance indoor × outdoor

### Roteiro

1. Nó ligado em casa (ambiente fechado), gateway ChirpStack fixo em `10.21.39.253`.
2. Série **indoor**: pontos dentro da residência/prédio, com paredes e laje no
   caminho até o gateway.
3. Série **outdoor**: sair à rua e afastar-se progressivamente, até o ponto em
   que o uplink deixa de chegar.
4. Em cada ponto, **N = 10 uplinks** (não um só) para haver média e taxa.

### Métricas por ponto

| Campo | Origem |
|---|---|
| Distância (m) | GPS do celular |
| Ambiente | indoor / outdoor |
| Obstáculos | descrição curta (paredes, prédios, vegetação, linha de visada) |
| RSSI (dBm) | ChirpStack — `rxInfo[0].rssi` |
| SNR (dB) | ChirpStack — `rxInfo[0].snr` |
| DR / SF | fixo no firmware (ver limitação abaixo) |
| Uplinks enviados × recebidos | contagem → taxa de entrega (%) |
| Dado íntegro? | o evento decodificou com a classificação correta, não só "chegou" |

### Limitações a resolver ANTES de sair a campo

**(a) O ingestor descarta RSSI e SNR.**
`app/rhytmiq-server/ingestor.py` não lê `rxInfo` do uplink. Duas saídas:
ler os valores manualmente na interface/API do ChirpStack a cada ponto, ou
adicionar a captura de `rxInfo[0].rssi` / `.snr` no ingestor e gravar junto com
o evento. A segunda é melhor: deixa o dado rastreável como nas baterias
anteriores.

**(b) ADR desligado, DR5 fixo.**
O firmware usa `setADR(false)` e `setDatarate(5)` (`node.ino`, pós-join).
DR5 = SF7 = o **menor** alcance da faixa. Bom para comparabilidade entre pontos,
mas o número de distância máxima sairá pessimista.
Sugestão: rodar a série completa em DR5 e repetir apenas os 2–3 pontos de
fronteira em DR0/SF12. Resultado: "alcance mínimo garantido × alcance máximo do
rádio" — comparação que rende bem no texto.

### Montagem

- **Alimentação por powerbank** (USB-C), para desacoplar do notebook e permitir
  deslocamento com o conjunto.
  ⚠️ Muitos powerbanks cortam a saída quando a corrente cai abaixo de ~50–100 mA.
  O nó fica em consumo baixo entre uplinks e pode desligar sozinho no meio da
  rua. Verificar em bancada antes: deixar o nó 15 min ocioso no powerbank.
- **Antena RadioEng** (externa) no lugar da que veio com o Wio SX1262.
  O Wio usa conector IPEX — pode ser necessário rabicho IPEX→SMA.
  Anotar ganho (dBi), conector e polarização.
  ⚠️ A comparação entre antenas só é válida com potência de TX, DR, altura e
  orientação do nó **idênticos** nos dois casos.
  Se der tempo, medir os mesmos pontos com as duas antenas: a tabela
  "antena original × RadioEng" e o delta de RSSI são um resultado limpo.

---

## 3. Experimento B — uso real, andando de bicicleta

Funde-se ao roteiro já existente em `app/node/test/COLETA_CORPO.md`
(repouso → esforço → recuperação). O powerbank e a antena externa dão
justamente a mobilidade que faltava para levar a coleta à rua.

- Firmware em `DIAG_MODE 0` (filtros + detector ativos), como no roteiro.
- **Gravar a tela do app** mostrando as frequências cardíacas chegando ao vivo.
- Gravar com **relógio visível** e anotar o horário de início de cada fase
  (parado → pedalando → recuperação), para casar o que o app exibe com o
  segmento correspondente da captura serial.

### Ética — PRÉ-REQUISITO BLOQUEANTE

Confirmar com o orientador se a UFMS exige aprovação do **Comitê de Ética em
Pesquisa (Plataforma Brasil / CEP)** para registrar ECG humano, **mesmo sendo o
próprio pesquisador o sujeito**. Não coletar antes de resolver isso.

### Expectativa realista do resultado

O pedal vai produzir **artefato de movimento** nos eletrodos, e o detector
provavelmente marcará arritmia/anomalia em vários segmentos por ruído — não por
ritmo. Isso **não é falha a esconder**: é a mesma limitação de especificidade da
flag de arritmia já documentada nas baterias 6 e 10.
Na defesa, "o sistema acusou anomalia sob movimento e eu sei explicar por quê"
é mais forte que um vídeo sem intercorrência.

---

## 4. Checklist

- [ ] Confirmar CEP com o orientador (bloqueia só o experimento B)
- [ ] Decidir: ler RSSI/SNR no ChirpStack ou patch no `ingestor.py`
- [ ] Testar autonomia/auto-desligamento do powerbank em bancada
- [ ] Conferir conector da antena RadioEng (IPEX → SMA?) e anotar dBi
- [ ] Definir os pontos de medição (indoor e outdoor) antes de sair
- [ ] Experimento A — série indoor
- [ ] Experimento A — série outdoor até a perda do enlace
- [ ] Experimento A — repetir pontos de fronteira em SF12 (opcional)
- [ ] Experimento B — coleta na bicicleta + vídeo do app
- [ ] Escrever a seção de alcance no `4_resultados.tex`
