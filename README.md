# A Python Chess Server/Client

A Python Chess Server/Client using websockets.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install websockets
```

## Server

```bash
python server.py
```

## Client

```bash
python client.py
```

## Commands

`USERNAME <username>` set your username
`LIST` list all connected clients
`NEWGAME` start a new game
`MOVE <from> <to>` move a piece (Example: `MOVE E2 E4`)

## License

MIT

