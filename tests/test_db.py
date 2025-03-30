import unittest
import sqlite3
from database.P2P_db import initialize_db, save_message, get_messages

class TestDatabase(unittest.TestCase):
    def setUp(self):
        '''Setup an in-memory SQLite database for testing'''
        self.db_name = ":memory:" #Temporary database
        initialize_db(self.db_name)
    
    def test_save_message(self):
        '''Test if messages are stored correctly in the database'''
        save_message(self.db_name, "Alice", "Bob", "Hello Bob", "sent", True)
        messages = get_messages(self.db_name)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0][1], "Alice")
        self.assertEqual(messages[0][2], "Bob")
        self.assertEqual(messages[0][3], "Hello Bob")
        self.assertEqual(messages[0][4], "sent")
        self.assertEqual(messages[0][5], 1)
    
    def test_get_message_empty(self):
        '''Test fetching messages from an empty database'''
        messages = get_messages(self.db_name)
        self.assertEqual(len(messages), 0)

if __name__ == "__main__":
    unittest.main() #Run the tests