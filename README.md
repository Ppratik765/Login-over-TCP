# Login over TCP

Simple client-server authentication system over standard TCP sockets in Python. Built for CNWT Lab 5.

## Overview

Socket-based authentication without any external libraries:
- **Server (`server/server.py`)**: Listens on `127.0.0.1:12345`, verifies credentials against SHA-256 hashes stored in `server/users.json`, and disconnects after 3 failed attempts.
- **Client (`client/client.py`)**: Connects to the server, prompts for username/password (masked with `getpass`), and displays the server verdict.

### Socket Flow
- **Server**: `socket()` → `bind()` → `listen()` → `accept()` → `recv()` / `send()` → `close()`
- **Client**: `socket()` → `connect()` → `send()` / `recv()` → `close()`

## Project Layout

```text
.
├── server/
│   ├── server.py      # TCP server
│   └── users.json     # User credentials (auto-created on first run)
├── client/
│   └── client.py      # TCP client CLI
└── README.md
```

## Running the Project

Requires Python 3.

### 1. Run the Server
In terminal 1:
```bash
python server/server.py
```

### 2. Run the Client
In terminal 2:
```bash
python client/client.py
```

## Default Test Accounts

Generated in `server/users.json` on initial server launch:

| Username | Password |
|---|---|
| `admin` | `adminpass` |
| `student` | `studentpass` |
| `guest` | `guestpass` |

## Notes
- `SO_REUSEADDR` is set to avoid port lock errors on restarts.
- Client teardown and unexpected disconnects are handled in `try...finally`.
- A session closes automatically after 3 invalid attempts.
