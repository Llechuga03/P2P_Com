import socket
import threading

# Store active peer connections
peers = []

# Basic P2P system that handles secure message delivery using TCP and basic encode/decode functions.

def handle_peer(conn, addr):
    '''Function to handle incoming connections'''
    print(f"Connected to {addr}")
    while True:
        try:
            message = conn.recv(2048).decode()
            if not message:
                break
            print(f"{addr}: {message}")
            # Broadcast to other peers
            for peer in peers:
                if peer != conn:
                    peer.send(message.encode())
        except:
            break
    conn.close()
    peers.remove(conn)

def start_server(port):
    '''Function to start the server thread'''
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Using TCP protocol for message delivery
    server.bind(("0.0.0.0", port))
    server.listen(5)
    print(f"Listening for peers on port {port}...")
    
    while True:
        conn, addr = server.accept()
        peers.append(conn)  # Added to the list so they can receive messages in the future
        threading.Thread(target=handle_peer, args=(conn, addr)).start()

def connect_to_peer(peer_ip, peer_port):
    '''Function to connect to an existing peer'''
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((peer_ip, peer_port))
    peers.append(client)
    
    def listen_to_peer():
        '''Functions that prints out messages between peers'''
        while True:
            try:
                message = client.recv(2048).decode()
                if not message:
                    break
                print(f"Peer: {message}")
            except:
                break
        client.close()
    
    threading.Thread(target=listen_to_peer).start()
    
    while True:
        message = input("")
        if message.lower() == "exit":
            break
        client.send(message.encode())

# Run the server in a separate thread
port = 1234
threading.Thread(target=start_server, args=(port,)).start()

# Connect to an existing peer (Optional, if known)
peer_ip = input("Enter peer IP (leave blank if first node): ")
if peer_ip:
    peer_port = int(input("Enter peer Port: "))
    connect_to_peer(peer_ip, peer_port)
