import socket
import threading
import sys

# Store active peer connections
peers = {} #use a dictionary to store peer connections and their address, instead of a list

# Basic P2P system that handles secure message delivery using TCP and basic encode/decode functions.

def start_server(ip,port):
    '''Start the server to accept incoming connections'''
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((ip, port))
    server.listen(5)
    print(f"Listening for others on {ip}:{port}...")
    while True:
        conn, addr = server.accept()
        print(f"Connnected to {addr}")
        peers[addr] = conn
        threading.Thread(target=handle_peer, args=(conn, addr)).start()

def handle_peer(conn, addr):
    '''Function to handle incoming messages from peers'''
    try:
        while True:
            message = conn.recv(2048).decode()
            if message:
                print(f"<{addr[0]}> {message}")
                broadcast(f"<{addr[0]}> {message}", conn)
            else:
                remove_peer(conn, addr)
                break
    except:
            remove_peer(conn, addr)

def broadcast(message, sender_conn):
    ''''Function that sends a message to all peers except the sender'''
    for peer, addr in peers.items():
        if peer != sender_conn:
            try:
                peer.send(message.encode())
            except:
                remove_peer(peer, addr)

def remove_peer(conn):
    ''''Function to remove a peer from the list of active connections'''
    if conn in peers:
        conn.close()
        del peers[conn]
        print(f"Peer {peers[conn]} disconnected")

def connect_to_peer(peer_ip, peer_port):
    '''Function to connect to an existing peer'''
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((peer_ip, peer_port))
        peers[sock] = (peer_ip, peer_port)
        print(f"Connected to peer {peer_ip}:{peer_port}")
        threading.Thread(target=handle_peer, args=(sock, (peer_ip, peer_port)), daemon=True).start()
        return sock
    except Exception as e:
        print(f"Error connecting to peer {peer_ip}:{peer_port} - {e}")
        return None

def user_input_handler():
    ''''Function to handle user input and commands'''
    while True:
        message = input("(You): ")
        if message.lower == "/exit":
            print("Exiting...")
            sys.exit(0)
        elif message.startswith("/connect"):
            _, ip, port = message.split()
            connect_to_peer(ip, int(port))
        elif message.startswith("/peers"):
            print("Active peers:", list(peers.values()))
        elif message.startswith("/help"):
            print("Commands:")
            print("/connect <IP> <PORT> - Connect to a peer")
            print("/peers - List active peers")
            print("/exit - Exit the chat")
            print("/help - Show this list of commands")
        else:
            broadcast(f"{socket.gethostbyname(socket.gethostname())}: {message}", None)

# Main function to start the server and handle user input
if __name__ == "__main__":
    print("Welcome to the P2P Chat System!")
    print("To connect to a peer, use the command: /connect <IP> <PORT>")
    print("To list active peers, use the command: /peers")
    print("To exit, type: /exit")
    print("To print this message again, type: /help")
    print("To send a message, just type it and hit enter.")
    while True:
        if len(sys.argv) != 3 or not sys.argv[2].isdigit():
            print("Usage: python3 p2p_chat.py <IP> <PORT>")
            sys.exit(1)
        try:
            ip = sys.argv[1]
            port = int(sys.argv[2])
            break
        except ValueError:
            print("Invalid arguments. Please enter a valid IP and PORT.")
    
    threading.Thread(target=start_server, args=(ip, port), daemon=True).start()
    user_input_handler()
#Note: the code is not complete, but it should be enough to get you started.