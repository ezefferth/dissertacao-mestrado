# Dissertação de Mestrado — Sistema ECG sobre LoRaWAN (RhythmIQ)

Texto e fontes LaTeX da dissertação de mestrado:

> **Desenvolvimento de Sistema Embarcado para Aquisição e Transmissão de Sinais de ECG em Redes LoRaWAN**
>
> Programa de Pós-Graduação — Universidade Federal de Mato Grosso do Sul (UFMS)

## Sobre o trabalho

O trabalho descreve o projeto e a implementação de um sistema portátil e de baixo custo para o
monitoramento remoto do eletrocardiograma (ECG), voltado ao acompanhamento de pacientes durante
atividades físicas supervisionadas, especialmente idosos atendidos na Clínica Escola Integrada da UFMS.

A principal contribuição é a estratégia de **detecção de arritmias na borda** (*edge computing*): em vez de
transmitir a forma de onda completa do ECG — inviável sob as restrições de *duty cycle* e taxa de dados do
LoRaWAN —, o próprio dispositivo embarcado detecta os eventos cardíacos e transmite apenas um resumo
compacto de 10 bytes por segmento de 30 s.

### Arquitetura documentada

```
Eletrodos → XIAO ESP32-S3 + ADS1293 (detecção na borda)
          → Wio-SX1262 (LoRaWAN, AU915)
          → Gateway Radioenge + ChirpStack (Raspberry Pi 3)
          → MQTT → ingestor (Python) → Firestore (nuvem)
          → Aplicativo móvel (Expo / React Native)
```

## Estrutura do repositório

| Arquivo | Conteúdo |
|---|---|
| `tese.tex` | Arquivo principal (classe `book`, `natbib`/apalike, `babel` pt-BR) |
| `resumo.tex` | Resumo e *Abstract* |
| `1_introducao.tex` | Introdução, justificativa e objetivos |
| `2_conceitos.tex` | Revisão bibliográfica (ECG, tecnologias sem fio, LoRaWAN) |
| `3_met.tex` | Metodologia (hardware, firmware, rede, ingestão, app) |
| `4_resultados.tex` | Resultados preliminares |
| `7_conclusoes.tex` | Conclusões, limitações e trabalhos futuros |
| `acron.tex` | Lista de abreviaturas e termos técnicos |
| `capa.tex`, `macros.tex` | Capa e macros |
| `main.bib` | Referências bibliográficas |
| `assets/` | Figuras e diagramas |
| `build.ps1` | Script de compilação (Windows / MiKTeX) |
| `CLAUDE.md` | Documentação técnica do projeto completo (firmware, backend, app) |

## Como compilar

Requer **MiKTeX** (ou outra distribuição LaTeX com `pdflatex` e `bibtex`).

```powershell
# compilação completa (pdflatex ×4 + bibtex)
.\build.ps1 -bib

# atualização rápida (apenas pdflatex)
.\build.ps1

# limpar arquivos auxiliares
.\build.ps1 -clean
```

O resultado é gerado em `tese.pdf`.

## Status

Documento em evolução. O sistema embarcado, a infraestrutura de rede, o serviço de ingestão e o
aplicativo móvel foram implementados; a validação do sinal de ECG e os ensaios clínicos encontram-se
em andamento.

---

*Autor:* Ezefferth · UFMS
