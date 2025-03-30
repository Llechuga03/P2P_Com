import unittest
import socket
import threading
from src.P2P import start_server, connect_to_peer, broadcast, remove_peer, peers

class TestP2P(unittest.TestCase):
    def setUp(self):
        '''Setup a server for testing'''
        self.test_ip = "127.0.0.1"
        self.test_port = 9000
        self.server_thread = threading.Thread(target=start_server, args=(self.test_ip, self.test_port), daemon=True)
        self.server_thread.start()

    def test_peer_connection(self):
        '''Test if a peer can connect to the server'''
        sock = connect_to_peer(self.test_ip, self.test_port)
        self.assertIsNotNone(sock)
        self.assertIn(sock, peers)
    
    def test_broadcast(self):
        ''''Test if broadcasting messages works'''
        sock = connect_to_peer(self.test_ip, self.test_port)
        broadcast("Hello, World!", sock)
        # Check if the message was received by other peers

    def test_remove_peer(self):
        '''Test if a peer can be removed from the server properly'''
        sock = connect_to_peer(self.test_ip, self.test_port)
        remove_peer(sock)
        self.assertNotIn(sock, peers)

    if __name__ == "__main__":
        unittest.main()