# Memoria de revisao - dissertacao ECG/LoRaWAN

Arquivo de apoio para revisao incremental. Nao entra na compilacao LaTeX.

## Escopo e narrativa que devem ser preservados

- Tema: sistema para deteccao de alteracoes no ECG com comunicacao LoRaWAN.
- Contribuicao central: aquisicao do sinal, integracao do detector, armazenamento local, transmissao de eventos por LoRaWAN, infraestrutura ChirpStack/MQTT/Firestore e aplicativo.
- O detector de QRS/arritmias nao e contribuicao original: e firmware de Moraes, Iaione e Spalding, cedido pelos autores.
- O sistema trabalha com segmentos de 30 s a 640 SPS: 19.200 amostras por segmento.
- Payload LoRaWAN: 10 bytes transmitidos; resumo local: 16 bytes gravados em LittleFS; forma de onda completa de segmento de 30 s a 2 bytes/amostra: 38.400 bytes.
- Validacao clinica com pacientes ainda nao foi feita; ensaios clinicos dependem de CEP e devem ficar como trabalho futuro.

## Fatos experimentais consolidados

- ADS1293: taxa efetiva confirmada de 640 SPS pela cadeia de divisores e por medicao.
- Defeitos de aquisicao corrigidos: saturacao da serial e consulta recorrente a LittleFS.usedBytes() no loop, que causava perda periodica de amostras.
- RLD de tres eletrodos: CMDET_EN = 0x05 e SELRLD = 010; reduziu energia de 60 Hz no ensaio de bancada.
- LoRaWAN: envio da forma de onda foi inviavel; teste com 15.000 amostras levou cerca de 392,2 s.
- Validacao por baterias: as baterias iniciais devem ser narradas como percurso de depuracao, nao como desempenho final.
- Bateria final limpa: 180/180 segmentos corretos.
- Robustez sob ruido: 1.500/1.620 na configuracao final; falhas concentradas em 60 Hz a 30%.
- MIT-BIH: acuracia final de 85,0% com pausa relativa + sexta classe; limitacao dominante continua sendo especificidade da arritmia sinusal.
- Duas baterias finais somam 1.800 segmentos, 15,0 h de ECG, 34,6 milhoes de amostras e 58.787 picos R detectados.

## Comentarios do professor a tratar

- Titulo: professor sugeriu "Sistema para Deteccao de Alteracoes no ECG com Comunicacao LoRaWAN", por ser mais fiel ao envio de alertas/eventos, nao da forma de onda.
- Palavras-chave: sugeridas "Sistema embarcado, IoT, Computacao na borda, alteracoes eletrocardiograficas, ECG, LoRaWAN".
- ChirpStack: evitar defini-lo apenas como servidor de rede se o contexto exigir a pilha completa.
- Metodologia: esclarecer melhor "ingestao" e o que e coleta, processamento e persistencia.
- Componentes: custo deve usar USD e explicar FOB como sem frete/impostos; custo total do sistema deve aparecer se o texto fala em baixo custo.
- Bateria 18650: ha marcador de dimensoes incertas; nao deixar "C=650mm, D=180mm".
- Verificar consistencia 10 bytes transmitidos x 16 bytes armazenados localmente.
- Professor sugere mesclar/mover parte da secao 3.6 para transmissao LoRaWAN e talvez mesclar 3.7 com resultados.
- Validacao com gerador: incluir diagrama do arranjo de bancada com divisor resistivo; esclarecer atenuacao e teste.
- Estimulos: remover ou justificar "ensemble" se os sinais cedidos eram sinteticos/periodicos e os complexos P-QRS-T eram iguais.
- Figura das seis classes: revisar bloqueio/parada; professor apontou exemplo de bloqueio que parecia parada e pediu coerencia com a definicao da metodologia.
- Pipeline ponta a ponta: seis payloads transmitidos uma vez e fraco; professor sugere 30 repeticoes por payload para avaliar perda.
- App nos resultados: reduzir repeticao do que ja esta na metodologia; focar em teste e resultado.
- Alarmes: professor considerou inseguro descartar a arritmia quando coocorre com outra alteracao; manter a flag/contador para X de N, mesmo se a classificacao principal priorizar evento mais grave.
- Resultados: professor achou a secao final extensa/confusa; preferir reorganizar para explicar a melhoria da regra de decisao e reduzir tabelas/figuras que nao acrescentam.
- Medidas faltantes importantes: autonomia de bateria de 4,2 V ate 3,0 V; tempo de processamento no XIAO apos cada segmento; tempo/envio LoRaWAN; cobertura da rede.
- Trabalhos futuros/limitacoes: eletrodo solto nao sinalizado; tensao da bateria nao medida para alerta de bateria descarregada.
- Objetivos: professor sugeriu retirar ou ajustar "avaliar qualidade do sinal e taxa de transmissao", se isso nao foi medido diretamente como objetivo.
- Conclusoes: revisar somente depois de reorganizar resultados.
- Resumo: professor pediu para revisar por ultimo.

## Problemas textuais ja localizados

- 3_met.tex: "istema embarcado" deve ser "sistema embarcado".
- 3_met.tex: titulo "Procesamento" deve ser "Processamento".
- 3_met.tex: "modelo 18650 (C=650mm, D=180mm)" parece incorreto e precisa de dado real ou remocao.
- 3_met.tex: "algoritmo original original" tem repeticao.
- 3_met.tex: ha pendencia textual explicita sobre classificar toda pausa superior a tres ciclos como parada.
- 1_introducao.tex: "eletcoardiograficas" deve ser "eletrocardiograficas".
- resumo.tex: falta espaco apos "Palavras-chave:".
- 2_conceitos.tex: ha erros como "decorre codigo", "transmissao ddos", "nsete".

## Bibliografia

- main.bib contem 47 entradas; 36 chaves sao citadas no conjunto atual de .tex.
- Nao apareceu chave citada ausente real; a falsa chave "#1" vem da macro citeay em dissertacao.tex.
- Entradas nao citadas existem, mas nao sao problema por si so; revisar somente se a banca/orientador exigir enxugar bibliografia.
- Em metodologia/resultados, as citacoes centrais atuais sao: TexasInstruments_ADS1293, AnalogDevices_AD8232, WioSX1262Datasheet, moraesFirmwareECG, hrvTaskForce1996, lorawanWaveform, 3-lead, ecgCompressionLora.

## Criterio de revisao dos proximos trechos

- Antes de propor reescrita: identificar se o trecho e metodologia, resultado, discussao, limitacao ou trabalho futuro.
- Nao inventar numero, fonte, modelo de caixa, autonomia, tempo de processamento, custo ou dado clinico.
- Quando faltar dado, oferecer duas saidas: deixar como limitacao/trabalho futuro ou marcar como medida pendente.
- Reduzir tracos de IA por precisao e voz autoral: menos repeticao, menos conectores genericos, mais causa-evidencia-limite.
- Em resultados, cada trecho deve responder: objetivo do ensaio, N/condicoes, resultado, interpretacao, alcance e limitacao.
