# CLAUDE.md — Mestrado: Sistema ECG LoRaWAN (RhythmIQ)

## Visão geral do projeto

Sistema completo de monitoramento cardíaco remoto desenvolvido para dissertação de mestrado (UFMS).
Título: "Desenvolvimento de Sistema Embarcado para Aquisição e Transmissão de Sinais de ECG em Redes LoRaWAN".

### Estrutura de pastas

```
C:\Work\mestrado\
├── app/
│   ├── node/            ← Firmware Arduino (XIAO ESP32-S3 + ADS1293)
│   ├── rhythmiq/        ← App mobile (Expo 54 / React Native 0.81)
│   └── rhytmiq-server/  ← Backend (Node.js + Express + Prisma + Postgres)
├── dissertacao/         ← Texto LaTeX (tese.tex, compilar com build.ps1)
└── artigos/             ← PDFs dos artigos de referência
```

---

## Fluxo de dados completo

```
ADS1293 (SPI)
    → XIAO ESP32-S3 (ECG_abnormal.cpp detecta arritmia)
        → LoRaWAN (RadioLib, OTAA, DR5)
            → ChirpStack Gateway (10.21.39.253)
                → MQTT (application/+/device/+/event/up)
                    → rhytmiq-server (porta 3007)
                        → Prisma → PostgreSQL (Supabase)
                        → Socket.IO → rhythmiq (app mobile)
                        → Notificacao (banco) para profissionais
```

---

## 1. Firmware — `app/node/`

### Hardware

| Componente | Modelo | Detalhe |
|---|---|---|
| MCU | Seeed XIAO ESP32-S3 | 3.3V GPIO, USB-C |
| Radio LoRa | Wio SX1262 | OTAA, DR5, porta 2 |
| AFE ECG | CJMCU-1293 (ADS1293) | SPI, 24-bit, 3 canais |

**CRÍTICO: alimentar ADS1293 com 3.3V (AVDD máx = 3.6V). Nunca 5V.**

### Pinagem SPI

| Sinal | Pino XIAO |
|---|---|
| DRDY (IRQ) | D1 |
| CS | D3 |
| SCK | D8 |
| MISO | D9 |
| MOSI | D10 |

### Espelhamento Arduino IDE (junction Windows)

```
C:\Users\User\Documents\Arduino\nodeLoraWan\node  →  C:\Work\mestrado\app\node
```
Editar em qualquer dos dois reflete no outro. Git é feito em `app/`.

### Arquivos do firmware

| Arquivo | Função |
|---|---|
| `node.ino` | Loop principal, IRQ DRDY, filtros IIR, saída serial |
| `config.h` | Credenciais LoRaWAN (DevEUI, AppKey, NwkKey) |
| `ECG_abnormal.h` | Constantes, structs `ECG_abnormal_struct` e `ECG_RR_struct` |
| `ECG_abnormal.cpp` | Algoritmo de detecção R-peak e classificação de 5 arritmias |

### Derivações ECG

```
ch1  = Lead I   = LA − RA    (ADS1293 canal 1)
ch2  = Lead II  = LL − RA    (ADS1293 canal 2)
ch3  = Lead III = II − I     (calculado: ch2 − ch1, lei de Einthoven)
```

### Modo DIAG_MODE (`node.ino` linha 14)

```cpp
#define DIAG_MODE 1   // raw: sem filtro, relatório a cada 3 s — para debug
#define DIAG_MODE 0   // normal: filtros IIR + ECG_abnormal ativo
```

### Filtros IIR (modo 0, fs = 256 SPS)

```
LP (EMA):   fc = 40 Hz    α = 0.625   → remove 60 Hz e ruído muscular
HP (IIR):   fc = 0.5 Hz   α = 0.9878  → remove offset DC (~305 mV mid-supply)
```

### Conversão raw → mV

```cpp
const float ADC_FS  = 8388608.0f;  // 2^23
const float VREF_MV = 400.0f;      // estimativa; valor real ~2180 mV (ADS1293 + Vref interna)
```
A escala está errada mas não afeta a forma de onda, apenas a amplitude em mV.

### Detecção de arritmias (`ECG_abnormal.cpp`)

Processa segmentos de **30 s × 256 SPS = 7680 amostras** do Lead II.
Detecta 5 tipos: `Taquicardia`, `Bradicardia`, `Arritmia sinusal`, `Bloqueio sinoatrial`, `Parada sinoatrial`.

Limiares RR:
- Taquicardia: `rr_med < 600 ms`
- Bradicardia: `rr_med > 1000 ms`

### Payload LoRaWAN (decodificação no servidor)

```
ecg[0] = tipo_evento (1=BRADICARDIA, 2=TAQUICARDIA, 3=ARRITMIA, 0=NORMAL)
ecg[1..n] = amostras do sinal (int[])
```
Decodificado em `mqtt.ts` via `data.object?.ecg`.

### Problemas conhecidos no firmware

**Taxa de amostragem real ≠ 256 SPS** — DIAG mediu ~640 SPS (1920 amostras / 3 s).
Causa provável: mapeamento interno do enum `SPS_256` na lib `protocentral_ads1293`.
Impacto: `SAM_FREQ` e alfas dos filtros estão desajustados enquanto não confirmado.

Para corrigir quando a taxa real for confirmada:
```cpp
// ECG_abnormal.h → SAM_FREQ = <taxa_real>
// node.ino → recalcular:
// LP: alpha = 1 - exp(-2π × fc / fs)
// HP: alpha = 1 / (1 + 2π × fc / fs)
```

---

## 2. Backend — `app/rhytmiq-server/`

### Stack

- Node.js + Express 5 + TypeScript
- Prisma 6 + PostgreSQL (Supabase)
- MQTT 5 (escuta ChirpStack)
- Socket.IO 4 (push para app)
- JWT (`expiresIn: "1d"`)
- bcryptjs (hash de senha)
- FCM e Supabase JS: **comentados / não ativos**

### Executar

```bash
cd app/rhytmiq-server
npm run dev        # tsx watch src/index.ts (hot reload)
npm run build      # tsc
npm start          # node dist/index.js
```

### Portas e IPs fixos no código

| Recurso | Valor |
|---|---|
| Porta HTTP | `3007` (`src/index.ts`) |
| MQTT ChirpStack | `mqtt://10.21.39.253:1883` (`src/mqtt.ts`) |
| Socket.IO client (app) | `http://10.21.39.74:3007` (`rhythmiq/src/context/SocketContext.tsx`) |

Se a rede mudar, atualizar os dois arquivos acima.

### Variáveis de ambiente necessárias (`.env`)

```
DATABASE_URL=       # Prisma (pooled) — Supabase
DIRECT_URL=         # Prisma (direct) — Supabase
JWT_SECRET=
```
FCM e Supabase JS não precisam de variáveis (código comentado).

### Schema Prisma (modelos)

```
Instituicao (id uuid)
  └─ usuarios     → Usuario (perfil: PROFISSIONAL_SAUDE | PACIENTE | ADMIN)
  └─ pacientes    → Paciente (cpf?, dataNascimento?)
  └─ dispositivos → Dispositivo (devEui unique, int id autoincrement)
                        └─ eventoCardiacos → EventoCardiaco
                        └─ historicoUso    → AlocacaoDispositivo

EventoCardiaco
  bpm, tipoEvento (BRADICARDIA|TAQUICARDIA|ARRITMIA|NORMAL)
  sinalCritico bool, origem (AUTOMATICO|MANUAL), sinal int[]

Notificacao → Usuario (lida bool)
AlocacaoDispositivo (dataInicio, dataFim nullable — null = ainda em uso)
```

### Rotas da API

| Método | Rota | Perfil | Descrição |
|---|---|---|---|
| POST | `/usuario/cadastrar` | público | Criar usuário |
| POST | `/login` | público | Autenticar |
| GET | `/usuarios` | autenticado | Listar usuários |
| GET/PUT/DELETE | `/usuarios/:id` | autenticado | CRUD usuário |
| GET | `/dispositivos` | ADMIN, PROF | Listar dispositivos |
| POST | `/dispositivos` | ADMIN | Cadastrar dispositivo |
| PUT | `/dispositivos/:id` | ADMIN, PROF | Vincular/desvincular paciente |
| DELETE | `/dispositivos/:id` | ADMIN | Remover dispositivo |
| GET | `/pacientes` | autenticado | Listar pacientes |
| POST | `/pacientes` | autenticado | Criar paciente |
| GET/PUT/DELETE | `/pacientes/:id` | autenticado | CRUD paciente |
| GET/POST | `/eventos` | ADMIN, PROF | Listar / criar manual |
| DELETE | `/eventos/:id` | ADMIN | Remover evento |
| GET/POST | `/instituicoes` | autenticado | CRUD instituição |

### Fluxo MQTT → Socket.IO

```
ChirpStack publica em: application/+/device/+/event/up
mqtt.ts decodifica payload → cria EventoCardiaco + Notificacoes (transação Prisma)
→ io.emit("novoEvento", evento)          ← todos os dashboards atualizam
→ io.to(prof.id).emit("notificacao", …)  ← notificação individual por sala
```

Socket.IO: cliente entra na sala com `socket.emit("entrarSala", usuarioId)`.

---

## 3. App mobile — `app/rhythmiq/`

### Stack

- Expo 54 + Expo Router 6 (App Router, `/app`)
- React Native 0.81.5 + TypeScript
- React 19

### Executar

```bash
cd app/rhythmiq
npx expo start          # QR code (Expo Go ou build dev)
npx expo start --android
npx expo start --ios
```

### Variável de ambiente obrigatória

```
EXPO_PUBLIC_SERVER_URL=http://10.21.39.74:3007   # no .env
```
Usada em `src/config/api.ts` como `API_URL`.

### Estrutura de rotas (App Router)

```
app/
  index.tsx             → redirect para (auth) ou (home)
  _layout.tsx           → AuthProvider + DataProvider + SocketProvider
  (auth)/
    login.tsx
    cadastro.tsx
    recuperar.tsx
  (home)/
    dashboard/index.tsx  → lista EventoCardiaco em tempo real (Socket.IO)
    pacientes/
      index.tsx
      cadastrarPacientes.tsx
    config/
      index.tsx
      dispositivos.tsx
      alterarSenha.tsx
```

### Contexts

| Context | Função |
|---|---|
| `AuthContext` | token JWT + usuario em AsyncStorage |
| `DataContext` | CRUD dispositivos, pacientes, eventos via API REST |
| `SocketContext` | conexão Socket.IO, `ultimoEvento` dispara reload da lista |

### Tipos principais (`src/types/index.ts`)

```ts
Usuario  { perfil: "PROFISSIONAL_SAUDE" | "PACIENTE" | "ADMIN" }
Dispositivo { id, devEui, pacienteId?, usuarioId? }
Paciente { id, nome, cpf?, ativo, dataNascimento }
EventoCardiaco { bpm, tipoEvento, sinal: number[], criadoEm }
```

---

## 4. Dissertação — `dissertacao/`

### Compilar

```powershell
cd C:\Work\mestrado\dissertacao

.\build.ps1 -bib   # compilação completa (pdflatex × 4 + bibtex)
.\build.ps1        # atualização rápida (só pdflatex)
.\build.ps1 -clean # limpa auxiliares
```

MiKTeX instalado em: `%USERPROFILE%\AppData\Local\Programs\MiKTeX\miktex\bin\x64\`
Já adicionado ao PATH do usuário. Em novo terminal, `pdflatex` funciona diretamente.

### Arquivo principal

`tese.tex` — `\documentclass[12pt,twoside]{book}`, `natbib` (apalike), `babel[brazil]`.

Capítulos incluídos: 1_introducao, 2_conceitos, 3_met, 4_resultados, 5_cronograma, 7_conclusoes.
Capítulo 6 está comentado no `tese.tex`.

### Aviso `babel: Name 'brazil' is deprecated`

Inofensivo. Pode ser corrigido renomeando para `brazilian` quando conveniente.

---

## 5. Base de conhecimento — `.claude/skills/ecg-remote-monitoring/`

54 artigos científicos indexados sobre ECG IoT + LoRaWAN.
Para consultar: ler `SKILL.md` (índice geral), `chapters/cheatsheet.md` (tabelas de referência rápida), `chapters/patterns.md` (padrões de design recorrentes).

---

## Convenções e regras do projeto

- **Não commitar `config.h`** com chaves LoRaWAN reais. Usar `.gitignore` ou substituir por placeholders.
- **IPs hardcoded** em `mqtt.ts` e `SocketContext.tsx` — atualizar se a rede da clínica mudar.
- **Prisma**: sempre rodar `npx prisma generate` após alterar `schema.prisma`. Migration com `npx prisma migrate dev`.
- **Expo Router**: projeto usa App Router (`/app`). Não criar rotas no estilo Pages Router.
- **`use client`** não se aplica (React Native); usar context + hooks sem diretiva.
- **Banco**: não fazer `DELETE`/`UPDATE` sem `WHERE`. `AlocacaoDispositivo.dataFim = null` significa dispositivo em uso.
- **Prisma está em `devDependencies`** no server — isso é intencional (não alterar).

---

## Comandos rápidos

```bash
# Firmware — via Arduino IDE (pasta espelhada via junction)
# Abrir: C:\Users\User\Documents\Arduino\nodeLoraWan\node\node.ino

# Backend
cd C:\Work\mestrado\app\rhytmiq-server
npm run dev

# App mobile
cd C:\Work\mestrado\app\rhythmiq
npx expo start

# Dissertação
cd C:\Work\mestrado\dissertacao
.\build.ps1 -bib

# Prisma
cd C:\Work\mestrado\app\rhytmiq-server
npx prisma studio          # interface visual do banco
npx prisma migrate dev     # nova migration
npx prisma generate        # regerar cliente após schema change
```
