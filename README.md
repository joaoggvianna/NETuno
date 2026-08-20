# NETuno v0.8

NETuno é um assistente pessoal digital em desenvolvimento, criado para combinar **assistência**, **automação** e **orquestração de dispositivos e serviços** em uma única experiência.

A visão do produto é ir além de um simples administrador do computador. O objetivo é que o NETuno consiga receber comandos por texto e voz, responder ao usuário, lembrar informações, executar ações em aplicativos, consultar serviços conectados e, futuramente, operar a partir de uma interface web ou mobile como um assistente portátil.

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
- interface web;
- interface mobile/PWA;
- aplicação desktop/agent local.

A visão de longo prazo é permitir interações como:

```text
NETuno, abra o Spotify e toque Everlong.

NETuno, como está meu computador?

NETuno, me lembre de revisar banco de dados às 19h.

NETuno, iniciar modo estudo.
```

## Funcionalidades atuais

Na v0.8, o NETuno consegue:

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

O terminal, a API HTTP e o cliente web utilizam o mesmo Core:

```text
Terminal ───────────────┐
                        ↓
                    NETuno Core
                        ↑
Web Client → HTTP API ──┘
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
- `commands/system.py`: hora, data, status do computador e encerramento.
- `commands/apps.py`: abertura dos aplicativos explicitamente suportados.
- `commands/web.py`: abertura dos sites explicitamente suportados.
- `commands/notes.py`: regras de criação, listagem e remoção de notas.
- `commands/modes.py`: orquestra modos e comandos compostos reutilizando handlers.
- `commands/music.py`: traduz intenções musicais em operações do Spotify.
- `integrations/spotify.py`: encapsula AppleScript e o protocolo local do Spotify.
- `database/database.py`: inicialização do SQLite e única camada que executa SQL.
- `data/netuno.db`: banco local criado automaticamente e não versionado.
- `tests/`: testes automatizados do parser, roteamento e handlers.

O parser não executa ações diretamente, e os handlers não imprimem na tela. Eles devolvem um `CommandResult`. Essa separação permite testar interpretação e roteamento sem disparar efeitos colaterais e prepara o projeto para futuras entradas por voz, interface gráfica e integrações externas.

## Arquitetura futura

Conforme o projeto evoluir, a arquitetura tende a separar o núcleo do assistente, as integrações externas e os clientes de interface:

```text
                Usuário
                  │
        ┌─────────┴─────────┐
        │                   │
      Texto                Voz
                            │
                     Speech-to-Text
        │                   │
        └─────────┬─────────┘
                  ↓
             NETuno Core
                  ↓
          Parser / Intents
                  ↓
                Router
                  ↓
      ┌───────────┼───────────┐
      ↓           ↓           ↓
   Sistema     Spotify      Memória
      │
      ↓
 CommandResult
      │
 ┌────┴────┐
 ↓         ↓
Texto     Text-to-Speech
```

Para acesso portátil, a visão inclui também:

```text
NETuno Web/Mobile Client
          │
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

O cliente web/mobile não executaria ações diretamente no computador. Essas ações seriam delegadas ao agent local.

## Voz e wake word

A voz faz parte da visão principal do produto, não apenas como recurso estético.

O fluxo desejado é:

```text
microfone
   ↓
wake word: "NETuno"
   ↓
gravação do comando
   ↓
Speech-to-Text
   ↓
NETuno Core
   ↓
CommandResult
   ↓
Text-to-Speech
   ↓
resposta falada
```

A intenção é priorizar tecnologias locais e gratuitas sempre que possível, evitando dependência obrigatória de APIs pagas.

A detecção contínua da wake word será adicionada apenas quando o núcleo do assistente estiver mais maduro, pois envolve decisões adicionais de desempenho, privacidade e execução em segundo plano.

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

Instale as dependências:

```bash
python3 -m pip install -r requirements.txt
```

A v0.8 utiliza `psutil` para consultar as métricas do computador e `sqlite3`,
da biblioteca padrão, para persistir notas localmente.

## Executar

Na raiz do projeto:

```bash
python3 main.py
```

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

## API local

A API reutiliza integralmente o fluxo `Assistant → CommandParser → Router →
handlers`. O terminal continua sendo uma interface válida e independente.

Inicie a API durante o desenvolvimento:

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
exibe `Online` ou `Offline`. Comandos podem ser enviados pelo botão ou pela tecla
Enter, e as mensagens ficam no histórico da sessão até a página ser recarregada.

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

Os testes de aplicativos e navegador usam mocks para evitar efeitos colaterais durante a execução.

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

- processo local responsável por ações no computador;
- comunicação com o NETuno Core;
- execução controlada de comandos no dispositivo;
- preparação para controle remoto seguro.

### v1.0 — NETuno portátil

- integração entre Client, Core e Desktop Agent;
- acesso pela web/PWA;
- status remoto do dispositivo;
- execução remota de ações autorizadas.

### v1.1 — Entrada e saída por voz

- Speech-to-Text local;
- Text-to-Speech local;
- camada de voz desacoplada do Core;
- respostas faladas.

### v1.2 — Wake word "NETuno"

- detecção local da palavra de ativação;
- escuta passiva controlada;
- gravação apenas após ativação;
- indicadores claros de microfone ativo;
- configurações de privacidade e ativação/desativação.

### v1.3 — Linguagem mais flexível

- melhorar interpretação de frases;
- aliases dinâmicos;
- extração de entidades e argumentos;
- avaliar NLP local antes de introduzir LLM.

### v2.0 — Inteligência local opcional

- integração opcional com modelo local;
- uso como fallback para comandos não reconhecidos;
- preservar intents estruturadas e handlers determinísticos;
- evitar tornar a arquitetura dependente de uma LLM.

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
- o histórico visual desaparece ao recarregar a página;
- não há reconhecimento ou síntese de voz;
- ainda não existe wake word;
- VS Code e Spotify só são abertos no macOS nesta versão;
- apenas aplicativos e sites explicitamente suportados podem ser executados;
- ainda não há frontend web/mobile ou Desktop Agent;
- não há LLM no projeto atual.
