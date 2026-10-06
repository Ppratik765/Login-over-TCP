import socket
import getpass
import sys

HOST = '127.0.0.1'
PORT = 12345

def main():
    # 1. socket()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # 2. connect()
        client_socket.connect((HOST, PORT))
        print(f"[*] Connected to server at {HOST}:{PORT}")
        
        while True:
            username = input("Enter Username: ").strip()
            
            # Use getpass to mask password input cleanly
            try:
                password = getpass.getpass("Enter Password: ").strip()
            except Exception:
                # Fallback if getpass fails in some IDE environments
                password = input("Enter Password: ").strip()
                
            # 3. send() - Transmit username
            client_socket.sendall(username.encode('utf-8'))
            
            # 4. recv() - Wait for server to acknowledge username
            ack = client_socket.recv(1024).decode('utf-8')
            if not ack:
                print("[-] Connection lost while waiting for server acknowledgment.")
                break
                
            if ack == "OK_USER":
                # 3. send() - Transmit password
                client_socket.sendall(password.encode('utf-8'))
                
                # 4. recv() - Wait for server verdict
                verdict = client_socket.recv(1024).decode('utf-8')
                if not verdict:
                    print("[-] Connection lost while waiting for server verdict.")
                    break
                    
                print(f"\n[SERVER VERDICT] {verdict}\n")
                
                if "Access Granted" in verdict or "Maximum attempts exceeded" in verdict:
                    break
            else:
                print("[-] Unexpected server protocol response.")
                break
                
    except ConnectionRefusedError:
        print(f"[-] Could not connect to server at {HOST}:{PORT}. Ensure the server is running.")
    except Exception as e:
        print(f"[-] Client error: {e}")
    finally:
        # 5. close()
        client_socket.close()
        print("[*] Connection closed.")

if __name__ == '__main__':
    main()
