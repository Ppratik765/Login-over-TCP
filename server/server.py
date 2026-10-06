import socket
import json
import hashlib
import os
import datetime

HOST = '127.0.0.1'
PORT = 12345
USERS_FILE = 'users.json'
MAX_ATTEMPTS = 3

def generate_default_users():
    default_users = {
        'admin': hashlib.sha256('adminpass'.encode('utf-8')).hexdigest(),
        'student': hashlib.sha256('studentpass'.encode('utf-8')).hexdigest(),
        'guest': hashlib.sha256('guestpass'.encode('utf-8')).hexdigest()
    }
    with open(USERS_FILE, 'w') as f:
        json.dump(default_users, f, indent=4)
    print(f"[*] Generated default {USERS_FILE} with demo accounts.")

def load_users():
    if not os.path.exists(USERS_FILE):
        generate_default_users()
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def log_event(client_addr, message):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] [{client_addr[0]}:{client_addr[1]}] {message}")

def main():
    users = load_users()
    
    # 1. socket()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Use SO_REUSEADDR to prevent 'Address already in use' error on restart
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        # 2. bind()
        server_socket.bind((HOST, PORT))
        # 3. listen()
        server_socket.listen(1)
        print(f"[*] Server listening on {HOST}:{PORT}")
        
        while True:
            try:
                # 4. accept()
                conn, addr = server_socket.accept()
                log_event(addr, "Connection established.")
                
                try:
                    attempts = 0
                    while attempts < MAX_ATTEMPTS:
                        # 5. recv() - receive username
                        username_data = conn.recv(1024)
                        if not username_data:
                            log_event(addr, "Client disconnected abruptly before sending username.")
                            break
                        username = username_data.decode('utf-8').strip()
                        
                        # 5. send() - acknowledge username receipt and wait for password
                        conn.sendall(b"OK_USER")
                        
                        # 5. recv() - receive password
                        password_data = conn.recv(1024)
                        if not password_data:
                            log_event(addr, "Client disconnected abruptly before sending password.")
                            break
                        password = password_data.decode('utf-8').strip()
                        
                        # Verify credentials
                        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
                        
                        if username in users and users[username] == hashed_password:
                            # 5. send() - verdict
                            conn.sendall(b"Access Granted")
                            log_event(addr, f"Authentication successful for user '{username}'.")
                            break
                        else:
                            attempts += 1
                            if attempts >= MAX_ATTEMPTS:
                                # 5. send() - verdict
                                conn.sendall(b"Access Denied: Maximum attempts exceeded")
                                log_event(addr, f"Authentication failed for user '{username}'. Maximum attempts exceeded.")
                                break
                            else:
                                # 5. send() - verdict
                                conn.sendall(f"Access Denied: {MAX_ATTEMPTS - attempts} attempts remaining".encode('utf-8'))
                                log_event(addr, f"Authentication failed for user '{username}'. Attempts remaining: {MAX_ATTEMPTS - attempts}")
                except Exception as e:
                    log_event(addr, f"Error handling client data: {e}")
                finally:
                    # 6. close()
                    conn.close()
                    log_event(addr, "Connection closed.")
            except Exception as e:
                print(f"[*] Server error accepting connection: {e}")
                
    except Exception as e:
        print(f"[*] Server bind/listen error: {e}")
    finally:
        # 6. close()
        server_socket.close()
        print("[*] Server socket closed.")

if __name__ == '__main__':
    # Ensure working directory is the same as the script's directory for users.json
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
