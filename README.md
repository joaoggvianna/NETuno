# Jarvis v0.3

Jarvis é um assistente pessoal de terminal escrito em Python. O projeto usa interpretação determinística de comandos: em vez de depender de uma LLM ou de APIs pagas de IA, frases conhecidas são normalizadas, convertidas em intenções explícitas e encaminhadas para handlers responsáveis por executar cada ação.

A ideia do projeto é evoluir incrementalmente para um assistente pessoal mais completo sem esconder a arquitetura atrás de uma caixa-preta de IA.

## Funcionalidades atuais

Na v0.3, o Jarvis consegue:

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

## Como funciona

O fluxo principal é:

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

O parser não executa ações diretamente, e os handlers não imprimem na tela. Eles devolvem um `CommandResult`. Essa separação permite testar a interpretação e o roteamento sem abrir programas durante os testes e prepara o projeto para futuras entradas por voz ou outras interfaces.

## Requisitos

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
JARVIS > status do computador
CPU: 21% | Memória: 63% | Disco: 42% | Ligado há: 3h 18min

JARVIS > abrir youtube
Abrindo YouTube.

JARVIS > faça café
Não reconheci esse comando.
```

Os valores do status variam de acordo com o computador no momento da consulta.

## Testes

Execute a suíte com:

```bash
python3 -m unittest discover -v
```

Os testes de aplicativos e navegador usam mocks para evitar efeitos colaterais durante a execução.

## Evolução do projeto

### v0.1

Primeiro fluxo completo da arquitetura: hora, data, saída, parser, router e interface de terminal.

### v0.2

Primeiras ações reais: abertura de VS Code e Spotify no macOS e YouTube no navegador padrão.

### v0.3

Adiciona observabilidade básica do computador por meio do comando de status, utilizando `psutil` para CPU, memória, disco e uptime.

## Limitações atuais

- a interpretação de linguagem é baseada em comandos e aliases explicitamente cadastrados;
- não há LLM, reconhecimento de voz ou síntese de voz;
- VS Code e Spotify só são abertos no macOS nesta versão;
- apenas aplicativos e sites explicitamente suportados podem ser executados;
- o Jarvis ainda não possui memória persistente ou banco de dados.

## Próximos passos possíveis

As próximas versões podem adicionar persistência local de notas com SQLite, comandos compostos, suporte a voz e, posteriormente, interpretação opcional com um modelo local. Essas funcionalidades ainda não fazem parte da v0.3.
