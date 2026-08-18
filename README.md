# Jarvis v0.2

Assistente pessoal de terminal com interpretação determinística de comandos.
Esta versão informa hora e data, abre aplicativos suportados no macOS, abre o
YouTube no navegador padrão e encerra a aplicação.

## Requisitos

- Python 3.9 ou superior

Não há dependências externas na v0.2.

## Executar

Na raiz do projeto:

```bash
python3 main.py
```

Comandos de exemplo:

```text
que horas são
qual a data de hoje
abrir vscode
abrir spotify
abrir youtube
sair
```

## Testes

```bash
python3 -m unittest discover -v
```

## Fluxo

O terminal envia o texto para `Assistant`. O `CommandParser` produz um
`ParsedCommand`, o `Router` escolhe um handler em `commands/system.py`,
`commands/apps.py` ou `commands/web.py`, e o resultado retorna como
`CommandResult` para ser exibido no terminal.

## Limitações da v0.2

- A abertura de Visual Studio Code e Spotify está implementada para macOS.
- Apenas aplicativos e sites explicitamente suportados podem ser abertos.
