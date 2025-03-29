# app.py - Streamlit application with dark anonymous theme and fixed search
import streamlit as st
import sqlite3
import datetime
import pandas as pd
import re

# Initialize the database
def init_db():
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    
    # Create messages table if it doesn't exist
    c.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create FTS5 virtual table for full-text search if it doesn't exist
    c.execute('''
    CREATE VIRTUAL TABLE IF NOT EXISTS message_fts USING fts5(
        content,
        content='messages',
        content_rowid='id'
    )
    ''')
    
    # Create trigger for auto-updating FTS index on insert
    c.execute('''
    CREATE TRIGGER IF NOT EXISTS messages_ai AFTER INSERT ON messages
    BEGIN
        INSERT INTO message_fts(rowid, content) 
        VALUES (new.id, new.content);
    END
    ''')
    
    # Create trigger for auto-updating FTS index on update
    c.execute('''
    CREATE TRIGGER IF NOT EXISTS messages_au AFTER UPDATE ON messages
    BEGIN
        INSERT INTO message_fts(message_fts, rowid, content) 
        VALUES('delete', old.id, old.content);
        INSERT INTO message_fts(rowid, content) 
        VALUES (new.id, new.content);
    END
    ''')
    
    # Create trigger for auto-updating FTS index on delete
    c.execute('''
    CREATE TRIGGER IF NOT EXISTS messages_ad AFTER DELETE ON messages
    BEGIN
        INSERT INTO message_fts(message_fts, rowid, content) 
        VALUES('delete', old.id, old.content);
    END
    ''')
    
    conn.commit()
    conn.close()

# Database operations
def add_message(content):
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO messages (content, timestamp) VALUES (?, ?)", (content, timestamp))
    conn.commit()
    conn.close()

def search_messages(query):
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    
    # Using LIKE operator for partial matching instead of FTS wildcard
    # This works for any substring in the message
    c.execute("""
    SELECT content 
    FROM messages
    WHERE content LIKE ?
    ORDER BY timestamp DESC
    """, (f'%{query}%',))
    
    results = c.fetchall()
    conn.close()
    
    return [r[0] for r in results]

def get_all_messages(limit=100):
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute("SELECT content FROM messages ORDER BY timestamp DESC LIMIT ?", (limit,))
    results = c.fetchall()
    conn.close()
    
    return [r[0] for r in results]

# Custom CSS for dark theme
def apply_custom_css():
    st.markdown("""
    <style>
    /* Overall page styling */
    .stApp {
        background-color: #0a0a0a;
        color: #33ff00;
    }
    
    /* Search box styling */
    .stTextInput > div > div > input {
        background-color: #1a1a1a;
        color: #33ff00;
        border: 1px solid #33ff00;
        border-radius: 0px;
    }
    
    /* Message input styling */
    .stTextArea > div > div > textarea {
        background-color: #1a1a1a;
        color: #33ff00;
        border: 1px solid #33ff00;
        border-radius: 0px;
        font-family: monospace;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #1a1a1a;
        color: #33ff00;
        border: 1px solid #33ff00;
        border-radius: 0px;
    }
    
    /* Message styling */
    .message-container {
        background-color: #1a1a1a;
        border-left: 2px solid #33ff00;
        padding: 10px;
        margin: 5px 0;
        font-family: monospace;
    }
    
    /* Highlight search matches */
    .highlight {
        background-color: #1f3d1f;
        padding: 0 2px;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 5px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0a0a0a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #33ff00;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Highlight search term in results
def highlight_term(text, term):
    if not term or not text:
        return text
    
    # Use case-insensitive replacement
    pattern = re.compile(f'({re.escape(term)})', re.IGNORECASE)
    highlighted = pattern.sub(r'<span class="highlight">\1</span>', text)
    return highlighted

# UI Layout and Functionality
def main():
    st.set_page_config(
        page_title="void",
        page_icon="👻",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Apply custom CSS
    apply_custom_css()
    
    # Initialize the database on first run
    init_db()
    
    # Initialize session state
    if 'filter_active' not in st.session_state:
        st.session_state.filter_active = False
        st.session_state.search_results = []
        st.session_state.search_term = ""
    
    # Create a three-row layout
    search_row, messages_row, input_row = st.container(), st.container(), st.container()
    
    # Search box (top row)
    with search_row:
        search_query = st.text_input("Search", placeholder="search the void...", key="search_box", label_visibility="collapsed")
        if search_query:
            st.session_state.filter_active = True
            st.session_state.search_term = search_query
            st.session_state.search_results = search_messages(search_query)
        else:
            st.session_state.filter_active = False
    
    # Messages (middle row)
    with messages_row:
        if st.session_state.filter_active:
            if st.session_state.search_results:
                for msg in st.session_state.search_results:
                    # Highlight matching terms
                    highlighted_msg = highlight_term(msg, st.session_state.search_term)
                    st.markdown(f'<div class="message-container">{highlighted_msg}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div style="text-align:center;margin:50px;">no matches found</div>', unsafe_allow_html=True)
        else:
            messages = get_all_messages()
            if messages:
                for msg in messages:
                    st.markdown(f'<div class="message-container">{msg}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div style="text-align:center;margin:50px;">the void is empty... speak into it</div>', unsafe_allow_html=True)
    
    # Message input (bottom row)
    with input_row:
        col1, col2 = st.columns([6, 1])
        
        with col1:
            message_content = st.text_area("Message", placeholder="speak into the void...", height=100, key="message_box", label_visibility="collapsed")
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)  # Add some spacing
            if st.button("transmit"):
                if message_content.strip():
                    add_message(message_content)
                    st.rerun()  # Refresh to show the new message

if __name__ == "__main__":
    main()