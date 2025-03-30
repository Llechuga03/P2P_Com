import sqlite3
from datetime import datetime

# This file contains the database functions for the P2P application
# The database of choice is SQLite3 and stores the following information:
# 1. Sender
# 2. Receiver
# 3. Message
# 4. Timestamp
# 5. Direction (sent/received)
# 5. Status (delivered/undelivered)

DB_NAME = 'p2p.db'

def intialize_db():
    '''Function that creates the message table if it does not exist'''
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    #Following the syntax found in sqlite3 documentation
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            sender TEXT NOT NULL,
            receiver TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_message(sender, receiver, message, direction, status="delivered"):
    '''Function that stores a message in the database'''
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO messages (timestamp, sender, receiver, message, direction, status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (timestamp, sender, receiver, message, direction, status))
    conn.commit()
    conn.close()

def get_messages():
    '''Function to retrieve messages from the database'''
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages ORDER BY timestamp DESC")
    messages = cursor.fetchall()
    conn.close()
    return messages
