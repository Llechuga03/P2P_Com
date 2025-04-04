import socket
import threading
import sys
from database.P2P_db import save_message, get_messages, intialize_db

# Initialize the database so that messages can be saved as soon as connection is established
intialize_db()

# Store active peer connections
peers = {} #use a dictionary to store peer connections and their address, instead of a list

# Basic P2P system that handles secure message delivery using TCP and basic encode/decode functions.

#THINGS TO DO:
# 1. Add encryption to the messages
# 2. Add a GUI to the chat system
# 3. Allow users to block other users
# 4. Add a feature to mute other users for a certain time
# 5. Create a messaging API system using REDIS


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
        peers[conn] = addr #using socket as the key
        threading.Thread(target=handle_peer, args=(conn, addr)).start()

def handle_peer(conn, addr):
    """Handle messages from a connected peer."""
    try:
        while True:
            message = conn.recv(2048).decode()
            if message:
                sender_ip = addr[0]
                receiver_ip = socket.gethostbyname(socket.gethostname())
                # Save the message to the database
                save_message(sender_ip, receiver_ip, message, "received")

                # clear current line to display messages on seprate lines
                print("\r\033[K", end="")
                print(f"\r{message}\n(You): ", end="")
                broadcast(f"<{addr[0]}> {message}", conn)
            else:
                remove_peer(conn)
                break
    except:
        remove_peer(conn)

def broadcast(message, sender_conn):
    ''''Function that sends a message to all peers except the sender'''
    sender_ip = socket.gethostbyname(socket.gethostname())

    for peer_conn, (peer_ip, peer_port) in list(peers.items()):
        if peer_conn != sender_conn:
            try:
                peer_conn.send(message.encode())

                #Save the message to the database, indicating it was delivered
                save_message(sender_ip, peer_ip, message, "sent", "delivered")
            except:
                #Save the message to the database, indicating it was not delivered
                print(f"Failed to send message to {peer_ip}:{peer_port}")
                save_message(sender_ip, peer_ip, message, "sent", "failed")
                remove_peer(peer_conn)

def remove_peer(conn):
    ''''Function to remove a peer from the list of active connections'''
    if conn in peers:
        addr = peers[conn]
        conn.close()
        del peers[conn]
        print(f"Peer {addr} disconnected")

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
        message = input("(You): ").strip()
        if message.lower() == "/exit":
            print("Exiting...")
            sys.exit(0)
        elif message.startswith("/connect"):
            try:
                _, ip, port = message.split()
                connect_to_peer(ip, int(port))
            except ValueError:
                print("Invalid format. Use: /connect <IP> <PORT>")
        elif message.startswith("/peers"):
            print("Active peers:", list(peers.values()))
        elif message.startswith("/help"):
            print("Commands:")
            print("/connect <IP> <PORT> - Connect to a peer")
            print("/peers - List active peers")
            print("/exit - Exit the chat")
            print("/help - Show this list of commands")
        elif message.startswith("/history"):
            messages = get_messages()
            print("\n Message History:")
            for msg in messages:
                print(f"{msg[1]} -> {msg[2]} -> {msg[3]}: {msg[4]} ({msg[5]})")
            print(" End of history\n")
        else:
            broadcast(f"{socket.gethostbyname(socket.gethostname())}: {message}", None)

# Main function to start the server and handle user input
if __name__ == "__main__":
    print("Welcome to this basic P2P Chat System!")
    print("To connect to a peer, use the command: /connect <IP> <PORT>")
    print("To list active peers, use the command: /peers")
    print("To exit, type: /exit")
    print("To print this message again, type: /help")
    print("To send a message, just type it and hit enter.")
    print("To view message history, type: /history")
    while True:
        if len(sys.argv) != 3:
            print("ERROR, invalid syntax. Please use the following syntax: python3 P2P.py <IP> <PORT>")
            sys.exit(1)
        try:
            ip = sys.argv[1]
            port = int(sys.argv[2])
            break
        except ValueError:
            print("Invalid arguments. Please enter a valid IP and PORT.")
            sys.exit(1)
    
    threading.Thread(target=start_server, args=(ip, port), daemon=True).start()
    user_input_handler()

#Note: the code is not complete, but it should be enough to get you started.