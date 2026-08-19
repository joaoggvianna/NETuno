# NETuno v0.3

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

Na v0.3, o NETuno consegue:

- informar a hora local;
- informar a data local;
- mostrar uso de CPU, memória e disco, além do tempo desde a inicialização do computador;
- abrir Visual Studio Code no macOS;
- abrir Spotify no macOS;
- abrir YouTube no navegador padrão;
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
sair
```

## Como funciona hoje

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
- `core/assistant.py`: conecta parser e router e expõe o fluxo principal do assistente.
- `core/command_parser.py`: normaliza o texto, reconhece aliases e produz uma intenção estruturada.
- `core/models.py`: define `Intent`, `ParsedCommand` e `CommandResult`.
- `core/router.py`: encaminha cada intenção para o handler correspondente.
- `commands/system.py`: hora, data, status do computador e encerramento.
- `commands/apps.py`: abertura dos aplicativos explicitamente suportados.
- `commands/web.py`: abertura dos sites explicitamente suportados.
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

A v0.3 utiliza `psutil` para consultar as métricas do computador.

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

NETUNO > faça café
Não reconheci esse comando.
```

Os valores do status variam de acordo com o computador no momento da consulta.

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

Planejado:

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
```

### v0.5 — Comandos compostos e modos

- representar ações compostas;
- sequenciar comandos;
- "modo estudo";
- "abra X e faça Y";
- reaproveitar handlers existentes em vez de duplicar lógica.

### v0.6 — Integrações de aplicativos

- criar uma camada `integrations/`;
- evoluir Spotify de simples abertura para controle de reprodução;
- buscar faixa, álbum ou artista;
- preparar suporte a outros serviços.

Exemplo desejado:

```text
NETuno, abra o Spotify e toque o álbum Songs for the Deaf.
```

### v0.7 — API do NETuno Core

- expor capacidades do Core por uma API local;
- separar interface e lógica de negócio;
- permitir que outros clientes enviem comandos ao NETuno.

### v0.8 — Interface web

- primeiro frontend visual;
- identidade azul-marinho/metálica;
- envio de comandos por texto;
- visualização de respostas e status;
- base para uma PWA.

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
- ainda não há memória persistente;
- não há reconhecimento ou síntese de voz;
- ainda não existe wake word;
- VS Code e Spotify só são abertos no macOS nesta versão;
- apenas aplicativos e sites explicitamente suportados podem ser executados;
- ainda não há frontend web/mobile ou Desktop Agent;
- não há LLM no projeto atual.
