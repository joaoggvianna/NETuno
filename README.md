# NETuno v1.0

NETuno é um **assistente pessoal de desktop local orientado a voz, projetado
para evoluir em macOS, Windows e Linux**.

A v1.0 adiciona uma interface local de voz push-to-talk ao Core determinístico
existente. O usuário inicia cada gravação explicitamente, o áudio é transcrito
localmente, o comando percorre o mesmo parser e router das demais interfaces e
a resposta é falada por uma engine local do sistema operacional.

O projeto está sendo desenvolvido incrementalmente e sem depender de APIs pagas de IA. A base atual utiliza interpretação determinística de comandos, mantendo a arquitetura simples, testável e fácil de explicar.

## Visão do produto

O NETuno deve evoluir em torno de três pilares:

### Assistente

Responsável por ajudar o usuário com informações e contexto pessoal, como:

- notas;
- lembretes;
- tarefas;
- agenda;
- rotinas;
- memória local;
- respostas por texto e voz.

### Orquestrador

Responsável por executar ações e integrar serviços, como:

- abrir e controlar aplicativos;
- interagir com Spotify e outros serviços;
- consultar o estado do computador;
- executar automações;
- iniciar modos compostos, como "modo estudo";
- controlar futuramente dispositivos conectados.

### Interface

Responsável pelas formas de interação com o usuário:

- terminal;
- voz;
- wake word "NETuno";
- interface web local;
- Desktop Agent local;
- interface de voz push-to-talk.

A visão de longo prazo é permitir interações como:

```text
NETuno, abra o Spotify e toque Everlong.

NETuno, como está meu computador?

NETuno, me lembre de revisar banco de dados às 19h.

NETuno, iniciar modo estudo.
```

## Funcionalidades atuais

Na v1.0, o NETuno consegue:

- informar a hora local;
- informar a data local;
- mostrar uso de CPU, memória e disco, além do tempo desde a inicialização do computador;
- abrir Visual Studio Code no macOS;
- abrir Spotify no macOS;
- abrir YouTube no navegador padrão;
- criar, listar e remover notas persistidas localmente;
- executar o modo estudo como uma sequência de ações;
- executar composições explícitas de aplicativos e sites;
- controlar reprodução, pausa e troca de faixas no Spotify local;
- abrir buscas por música, álbum, artista ou termo no Spotify;
- expor o mesmo Core por uma API HTTP local;
- receber comandos por uma interface web responsiva;
- exibir o status do Core e o histórico visual da sessão;
- encerrar a aplicação;
- responder de forma previsível a comandos não reconhecidos.
- delegar aplicativos, métricas do sistema e Spotify a um Desktop Agent local.
- capturar um comando pelo microfone sob solicitação explícita;
- transcrever o áudio com Whisper executado localmente;
- enviar a transcrição ao mesmo NETuno Core usado pelas outras interfaces;
- falar a mensagem do `CommandResult` por Text-to-Speech local.

Exemplos de comandos:

```text
que horas são
qual a data de hoje
status do computador
status do pc
abrir vscode
abrir spotify
abrir youtube
criar nota comprar pão
listar notas
remover nota 1
modo estudo
abrir vscode e spotify
abrir spotify e youtube
tocar música
pausar spotify
próxima faixa
faixa anterior
toque a música Everlong
sair
```

## Como funciona hoje

O terminal, a API HTTP, o cliente web e a interface de voz utilizam o mesmo
Core. As ações que
controlam o computador são delegadas a um processo local separado:

```text
Terminal ──────┐
Web/API ───────┼→ NETuno Core → Desktop Agent → Sistema / Apps / Spotify
Voice ─────────┘
```

O fluxo principal da aplicação é:

```text
texto do usuário
      ↓
CommandParser
      ↓
ParsedCommand
      ↓
Router
      ↓
handler em commands/
      ↓
AgentClient (para ações locais migradas)
      ↓
Desktop Agent
      ↓
CommandResult
      ↓
resposta no terminal
```

### Responsabilidades

- `main.py`: inicia o programa e mantém o loop do terminal.
- `api/app.py`: expõe o `Assistant` através dos endpoints HTTP locais.
- `api/schemas.py`: valida requests e define responses sem expor modelos internos.
- `frontend/src/App.jsx`: coordena status, envio e histórico visual da sessão.
- `frontend/src/api/netunoApi.js`: centraliza a comunicação HTTP com a API.
- `frontend/src/components/`: componentes visuais pequenos e reutilizáveis.
- `core/assistant.py`: conecta parser e router e expõe o fluxo principal do assistente.
- `core/command_parser.py`: normaliza o texto, reconhece aliases e produz uma intenção estruturada.
- `core/models.py`: define `Intent`, `ParsedCommand` e `CommandResult`.
- `core/router.py`: encaminha cada intenção para o handler correspondente.
- `core/agent_client.py`: centraliza ações HTTP estruturadas enviadas ao Agent.
- `voice/audio.py`: captura áudio mono do microfone apenas em memória.
- `voice/stt.py`: transforma áudio em texto com um modelo Whisper local.
- `voice/tts.py`: encapsula a síntese de voz local.
- `voice/voice_assistant.py`: coordena voz e `Assistant.process_command` sem interpretar intents.
- `voice_main.py`: inicia o loop push-to-talk independente.
- `desktop_agent/app.py`: expõe os endpoints locais do Desktop Agent.
- `desktop_agent/schemas.py`: define ações, targets e respostas permitidas.
- `desktop_agent/executor.py`: executa apenas ações explícitas no dispositivo.
- `commands/system.py`: mantém hora/data locais e formata o status vindo do Agent.
- `commands/apps.py`: solicita ao Agent a abertura de aplicativos suportados.
- `commands/web.py`: abertura dos sites explicitamente suportados.
- `commands/notes.py`: regras de criação, listagem e remoção de notas.
- `commands/modes.py`: orquestra modos e comandos compostos reutilizando handlers.
- `commands/music.py`: traduz intenções musicais em ações estruturadas do Agent.
- `integrations/spotify.py`: encapsula AppleScript e o protocolo local do Spotify.
- `database/database.py`: inicialização do SQLite e única camada que executa SQL.
- `data/netuno.db`: banco local criado automaticamente e não versionado.
- `tests/`: testes automatizados do parser, roteamento e handlers.

O parser não executa ações diretamente, e os handlers não imprimem na tela. Eles devolvem um `CommandResult`. Essa separação permite testar interpretação e roteamento sem disparar efeitos colaterais e prepara o projeto para futuras entradas por voz, interface gráfica e integrações externas.

## Arquitetura da v1.0

Conforme o projeto evoluir, a arquitetura tende a separar o núcleo do assistente, as integrações externas e os clientes de interface:

```text
microfone
   ↓
voice/audio.py
   ↓
voice/stt.py (Whisper local)
   ↓
VoiceAssistant
   ↓
Assistant.process_command(text)
   ↓
CommandParser → Router → handlers
   ↓
CommandResult
   ↓
voice/tts.py → alto-falante
```

Voz é somente uma interface. Ela não interpreta intents, não acessa handlers e
não conversa diretamente com o Desktop Agent. Comandos que exigem ações no
computador preservam a fronteira existente:

```text
    Voice Interface
          ↓
      NETuno Core
          │
          ↓
  NETuno Desktop Agent
          │
  ┌───────┼────────┐
  ↓       ↓        ↓
Sistema Spotify  Aplicativos
```

O cliente web não executa ações diretamente no computador. O Core envia ao
Agent somente ações enumeradas e argumentos validados, nunca comandos de shell
ou frases do usuário.

## Voice Interface

Cada interação começa somente após o usuário pressionar Enter. A captura dura
cinco segundos por padrão e permanece apenas em memória. `sounddevice` captura
o microfone, `faster-whisper` executa o modelo Whisper localmente e o adaptador
de TTS usa as vozes disponíveis no sistema operacional.

O prefixo falado `NETuno` ou `NETuno,` é opcional e apenas removido antes do
texto ser entregue ao Core. Isso não é uma wake word: a v1.0 não possui escuta
contínua, gravação em background ou microfone permanentemente ativo.

## Identidade visual futura

A interface futura do NETuno deve seguir uma identidade visual própria, com estética tecnológica e naval:

- azul-marinho escuro;
- azul aço;
- cinza metálico;
- branco frio;
- detalhes discretos em azul brilhante.

A proposta é uma interface limpa e sofisticada, evitando excesso de elementos de ficção científica ou neon.

## Requisitos atuais

- Python 3.9 ou superior
- macOS para a abertura de Visual Studio Code e Spotify
- microfone e saída de áudio para a interface de voz

Instale as dependências:

```bash
python3 -m pip install -r requirements.txt
```

A v1.0 utiliza `sounddevice` para captura, `faster-whisper` para STT local e a
engine nativa do sistema (`say`, PowerShell/SAPI ou `espeak`) para TTS. O
primeiro uso de um modelo Whisper pode exigir seu
download; depois de armazenado no cache local, a transcrição não depende de
uma API ou chamada externa. O modelo padrão é `base`, que oferece um equilíbrio
melhor entre precisão em português, tamanho e velocidade.

## Executar

### Desktop Agent

Inicie primeiro o processo local responsável pelas ações do computador:

```bash
python3 -m uvicorn desktop_agent.app:app --port 8001
```

O Uvicorn utiliza `127.0.0.1` por padrão. Não exponha o Agent em `0.0.0.0` ou
na internet. A URL usada pelo Core pode ser alterada com `NETUNO_AGENT_URL`, mas
somente endereços localhost são aceitos. O fallback é
`http://127.0.0.1:8001`.

Como proteção adicional, o próprio serviço rejeita com HTTP 403 qualquer
request cujo endereço real do cliente não seja `127.0.0.1` ou `::1`, mesmo se
for iniciado acidentalmente em uma interface de rede externa.

### Terminal

Em outro terminal, na raiz do projeto:

```bash
python3 main.py
```

### Voz

Inicie a interface push-to-talk em um terminal separado:

```bash
python3 voice_main.py
```

Pressione Enter quando quiser falar. O NETuno grava por até cinco segundos,
mostra a transcrição e a resposta no terminal e fala a mesma mensagem retornada
pelo Core. Para comandos de aplicativos, Spotify ou status, mantenha também o
Desktop Agent em execução.

Configurações simples disponíveis:

```bash
NETUNO_STT_MODEL=small python3 voice_main.py
NETUNO_STT_LANGUAGE=pt NETUNO_VOICE_DURATION=7 python3 voice_main.py
```

- `NETUNO_STT_MODEL`: modelo do faster-whisper; padrão `base`.
- `NETUNO_STT_LANGUAGE`: idioma esperado; padrão `pt`.
- `NETUNO_VOICE_DURATION`: limite da gravação em segundos; padrão `5`.

No macOS, conceda acesso ao microfone para o Terminal quando solicitado. Linux
pode exigir PortAudio instalado pelo gerenciador de pacotes. Vozes e qualidade
do TTS variam conforme o sistema operacional.

Exemplo:

```text
NETuno Voice

Pressione ENTER para falar.
Ouvindo...
Você: NETuno, que horas são
NETuno: Agora são 10:30.
```

O áudio não é salvo, enviado a serviços externos ou capturado em background.
Não há wake word na v1.0. Se não houver fala reconhecível, o Core não é chamado.
Falhas de microfone, STT e TTS são apresentadas no terminal sem encerrar o Core.

Exemplo:

```text
NETUNO > status do computador
CPU: 21% | Memória: 63% | Disco: 42% | Ligado há: 3h 18min

NETUNO > abrir youtube
Abrindo YouTube.

NETUNO > criar nota comprar pão
Nota criada.

NETUNO > listar notas
1. comprar pão

NETUNO > modo estudo
Modo estudo iniciado.

✓ Visual Studio Code
✓ Spotify
✓ ambiente de estudo

NETUNO > pausar spotify
Spotify pausado.

NETUNO > toque a música Everlong
Abri a busca pela música "Everlong" no Spotify, mas esta versão não consegue
iniciar o resultado automaticamente.

NETUNO > faça café
Não reconheci esse comando.
```

Os números exibidos representam a posição atual de cada nota na lista. Após
uma remoção, a lista é numerada novamente a partir de `1`; os identificadores
internos do SQLite permanecem estáveis.

Os valores do status variam de acordo com o computador no momento da consulta.
Se o Desktop Agent estiver desligado, as ações migradas retornam
`O NETuno Desktop Agent não está disponível.` sem fallback local. Hora, data,
notas e demais comandos independentes do Agent continuam funcionando.
Uma `NETUNO_AGENT_URL` externa ou inválida também não impede a inicialização do
Core; somente comandos dependentes do Agent retornam
`A configuração do NETuno Desktop Agent é inválida.`

## API local

A API reutiliza integralmente o fluxo `Assistant → CommandParser → Router →
handlers`. O terminal continua sendo uma interface válida e independente.

### NETuno Core API

Inicie a API durante o desenvolvimento em outro terminal:

```bash
uvicorn api.app:app --reload
```

Se o executável instalado pelo `pip` não estiver no `PATH`, use:

```bash
python3 -m uvicorn api.app:app --reload
```

O Uvicorn utiliza `127.0.0.1:8000` por padrão. Endpoints disponíveis:

```http
GET /health
POST /commands
```

Exemplo:

```bash
curl -X POST http://127.0.0.1:8000/commands \
  -H "Content-Type: application/json" \
  -d '{"command":"status do computador"}'
```

Resposta:

```json
{
  "success": true,
  "message": "CPU: 21% | Memória: 63% | Disco: 42% | Ligado há: 3h 18min",
  "should_exit": false
}
```

O comando `sair` apenas retorna `should_exit: true`; ele não encerra o servidor.
A documentação automática padrão fica disponível em `http://127.0.0.1:8000/docs`.

> A API da v0.7 foi projetada para execução local e não deve ser exposta diretamente à internet.

## Frontend Web

O cliente React oferece uma interface visual local para o mesmo NETuno Core. O
fluxo é:

```text
Browser
   ↓
React
   ↓
HTTP
   ↓
FastAPI
   ↓
NETuno Core
```

Com a API rodando, inicie o frontend em outro terminal:

```bash
cd frontend
npm install
npm run dev
```

Abra `http://localhost:5173/`. Ao carregar, a interface consulta `/health` e
exibe um aviso se o Core estiver offline. Comandos podem ser enviados pelo botão
ou pela tecla Enter, e as mensagens ficam no histórico da sessão até a página
ser recarregada.

A URL da API pode ser alterada durante o desenvolvimento com
`VITE_NETUNO_API_URL`; sem essa variável, o cliente utiliza
`http://127.0.0.1:8000`.

O backend aceita CORS somente de `http://localhost:5173`. A interface permanece
local e não deve ser exposta diretamente à internet.

## Testes

Execute a suíte com:

```bash
python3 -m unittest discover -v
```

Execute também os testes e o build do frontend:

```bash
cd frontend
npm test -- --run
npm run build
```

Os testes do Agent, aplicativos, Spotify e navegador usam mocks para evitar
efeitos colaterais durante a execução.

## Roadmap

### v0.1 — Núcleo mínimo

Primeiro fluxo completo da arquitetura:

- parser;
- intents;
- router;
- hora;
- data;
- encerramento;
- interface de terminal.

### v0.2 — Primeiras ações

- abertura de VS Code;
- abertura de Spotify;
- abertura de YouTube;
- primeiros handlers com efeitos reais no sistema.

### v0.3 — Observabilidade local

- status de CPU;
- memória;
- disco;
- uptime;
- integração com `psutil`.

### v0.4 — Memória local

Objetivo: transformar o NETuno de um executor de comandos em um assistente capaz de guardar informações.

Entregue:

- SQLite;
- criação de notas;
- listagem de notas;
- remoção de notas;
- persistência entre execuções;
- novas intents relacionadas a memória;
- testes do banco usando uma base temporária.

Exemplos esperados:

```text
NETUNO > criar nota comprar presente
Nota criada.

NETUNO > listar notas
1. comprar presente
2. terminar trabalho de redes

NETUNO > remover nota 1
Nota removida.
```

### v0.5 — Comandos compostos e modos

Entregue:

- representação explícita de sequências cadastradas;
- modo estudo com VS Code, Spotify e ambiente de estudo;
- comandos compostos `abrir vscode e spotify` e `abrir spotify e youtube`;
- execução completa mesmo quando uma ação individual falha;
- reaproveitamento dos handlers existentes sem duplicar efeitos externos.

### v0.6 — Integrações de aplicativos

Entregue:

- camada `integrations/` separada dos comandos do usuário;
- reprodução, retomada, pausa, próxima faixa e faixa anterior no Spotify;
- busca segura por música, álbum, artista ou termo usando `spotify:search:`;
- mensagens explícitas quando o Spotify não está disponível;
- fallback honesto quando a busca não pode iniciar automaticamente o resultado;
- testes sem reprodução real ou outros efeitos externos.

Exemplo desejado:

```text
NETuno, abra o Spotify e toque o álbum Songs for the Deaf.
```

O Spotify instalado no macOS expõe controles locais e reprodução por URI
conhecido, mas não oferece busca por nome via AppleScript. Por isso, consultas
por texto abrem a tela de busca e não simulam que a reprodução foi iniciada.

## Fim da fase determinística

Com a v0.6, o NETuno conclui sua primeira fase. O Core determinístico agora é
capaz de:

- interpretar comandos conhecidos e extrair argumentos explícitos;
- guardar notas em memória local persistente;
- executar ações no computador e no navegador;
- compor ações cadastradas;
- operar modos reutilizáveis;
- integrar aplicativos sem expor seus detalhes ao parser ou ao router.

As versões seguintes iniciam a arquitetura de produto e interfaces sem alterar
o Core determinístico já validado.

### v0.7 — API do NETuno Core

Entregue:

- endpoints locais `GET /health` e `POST /commands`;
- schemas explícitos de request e response;
- reutilização da fachada `Assistant` sem duplicar o pipeline;
- validação de comandos vazios na fronteira HTTP;
- preservação de `should_exit` como decisão do cliente;
- documentação automática do FastAPI;
- testes HTTP e de integração API → Core.

### v0.8 — Interface web

Entregue:

- primeiro frontend React/Vite do NETuno;
- identidade naval, tecnológica e metálica responsiva;
- status inicial Online/Offline consultado via `/health`;
- envio de comandos via `/commands` com bloqueio durante requisições;
- histórico visual mantido apenas durante a sessão;
- tratamento separado para respostas do Core e falhas de rede;
- CORS restrito à origem local do Vite.

### v0.9 — NETuno Desktop Agent

Entregue:

- processo FastAPI local responsável por ações no computador;
- contrato enumerado para aplicativos, métricas e Spotify;
- `AgentClient` como única camada HTTP entre Core e Agent;
- allowlists e rejeição de campos/comandos arbitrários;
- tratamento explícito de Agent offline sem fallback local;
- testes completos sem efeitos reais no dispositivo.

### v1.0 — Voice Interface

- captura local push-to-talk;
- Speech-to-Text local;
- integração com o Core determinístico;
- Text-to-Speech local.

### v1.1 — Wake Word "NETuno"

- ativação explícita por palavra-chave local;
- controles claros de privacidade e microfone.

### v1.2 — Desktop Agent multiplataforma

- ações locais equivalentes em macOS, Windows e Linux.

### v1.3 — Empacotamento e execução em background

- distribuição instalável;
- ciclo de vida controlado do Agent e das interfaces.

### v1.4 — Refinamento da experiência de voz

- feedback de captura;
- configuração simples de voz e dispositivos;
- melhoria de latência e precisão.

### v2.0 — Interpretação inteligente local opcional

- interpretação local como recurso opcional;
- preservação do Core determinístico e das ações estruturadas.

## Princípios do projeto

- evolução incremental;
- arquitetura compreensível;
- sem overengineering;
- ações explícitas e seguras;
- testes para comportamento determinístico;
- preferência por soluções gratuitas e locais;
- IA como capacidade opcional, não como dependência estrutural;
- privacidade como requisito importante para voz e automação.

## Limitações atuais

- a interpretação de linguagem é baseada em comandos e aliases explicitamente cadastrados;
- as notas não possuem edição, categorias, tags ou busca;
- a memória local está limitada às notas armazenadas neste computador;
- buscas por nome no Spotify abrem resultados, mas não iniciam automaticamente;
- os controles avançados do Spotify dependem do aplicativo instalado no macOS;
- a API não possui autenticação e deve permanecer restrita a `127.0.0.1`;
- o frontend é local e não possui autenticação ou acesso remoto;
- o Desktop Agent deve ser iniciado separadamente e aceita somente localhost;
- não há autenticação, pareamento ou descoberta de dispositivos no Agent;
- o histórico visual desaparece ao recarregar a página;
- a voz exige que o usuário pressione Enter antes de cada captura;
- o modelo `base` pode ser mais lento em computadores antigos; `small` melhora
  a precisão ao custo de um download maior e mais processamento;
- a primeira configuração do Whisper pode precisar baixar o modelo;
- vozes de TTS e suporte a dispositivos dependem do sistema operacional;
- ainda não existe wake word ou escuta contínua;
- VS Code e Spotify só são abertos no macOS nesta versão;
- apenas aplicativos e sites explicitamente suportados podem ser executados;
- não há cliente mobile nem acesso remoto;
- não há LLM no projeto atual.
