# TCP Credentials Verification System

A complete, robust credentials verification system over TCP written in Python from scratch, adhering to the standard Berkeley TCP socket lifecycle.

## Architecture & Workflow

* **Server:** Binds to `127.0.0.1:12345`, listens for incoming client connections (up to 1 in the backlog queue), and manages them sequentially. It stores user credentials in a local `users.json` file. Passwords are hashed using SHA-256 for secure verification. 
* **Client:** Connects to the server, interactively prompts the user for credentials (masking the password cleanly using `getpass`), and transmits them sequentially for validation over the socket.

### Socket Lifecycle
* **Server:** `socket()` -> `bind()` -> `listen()` -> `accept()` -> `recv()`/`send()` -> `close()`
* **Client:** `socket()` -> `connect()` -> `send()`/`recv()` -> `close()`

## Directory Structure
```
.
├── server/
│   ├── server.py             # TCP Server implementation
│   └── users.json            # Hashed user credential database (auto-generated)
├── client/
│   └── client.py             # TCP Client implementation
└── README.md                 # Setup, architecture diagram, and execution steps
```

## Setup and Execution

Ensure you have Python 3 installed. No external dependencies or packages are required as it utilizes only the Python standard library.

### 1. Start the Server

Open your first terminal and start the server script:

```powershell
python server/server.py
```
*Note: Upon its first run, the server will automatically generate `server/users.json` with three demo accounts.*

### 2. Start the Client

Open a second terminal and start the client script:

```powershell
python client/client.py
```
*Follow the interactive prompts in the terminal to authenticate.*

## Demo Credentials

By default, the following demo credentials are seeded and stored as SHA-256 digests in the `users.json` file:
- Username: `admin` / Password: `adminpass`
- Username: `student` / Password: `studentpass`
- Username: `guest` / Password: `guestpass`

## Protocol Features
- Supports multiple consecutive client connections safely within a `while True` loop.
- Client socket disconnections or abrupt closures are gracefully handled using `try...finally` resource cleanups.
- Configured with `SO_REUSEADDR` to prevent address collision errors during restarts.
- Allows up to 3 failed authentication attempts per session before automatically terminating the connection and locking out.
