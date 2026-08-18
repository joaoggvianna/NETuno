# Jarvis v0.1

Assistente pessoal de terminal com interpretação determinística de comandos.
Esta versão informa a hora, informa a data e encerra a aplicação.

## Requisitos

- Python 3.9 ou superior

Não há dependências externas na v0.1.

## Executar

Na raiz do projeto:

```bash
python3 main.py
```

Comandos de exemplo:

```text
que horas são
qual a data de hoje
sair
```

## Testes

```bash
python3 -m unittest discover -v
```

## Fluxo

O terminal envia o texto para `Assistant`. O `CommandParser` produz um
`ParsedCommand`, o `Router` escolhe um handler em `commands/system.py` e o
resultado retorna como `CommandResult` para ser exibido no terminal.
