import os
from dotenv import load_dotenv
import streamlit as st
from psycopg2 import connect
import bcrypt
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# Database Connection
host = os.getenv("DB_HOST")
database = os.getenv("DB_DATABASE")
username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
conn_str = f"dbname={database} user={username} password={password} host={host}"

def get_db_connection():
    return connect(conn_str)

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(stored_hash, password):
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash)

# Signup 
def signup(username, password, email):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if user already registered
    cursor.execute("SELECT * FROM users WHERE username = %s", (username))
    if cursor.fetchone():
        st.warning("Username already taken.")
        return False
    
    password_hash = hash_password(password)
    cursor.execute("INSERT INTO users (username, password_hash, email) VALUES (%s, %s, %s)",
                   (username, password_hash, email))
    conn.commit()
    cursor.close()
    conn.close()
    st.success("Signup successful!")
    return True

# Login 
def login(username, password):
 def login(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    

    cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    
    if result:
        stored_hash = result[0]
        
     
        if check_password(stored_hash, password):
            st.success("Login successful!")
            return True
        else:
            st.warning("Incorrect password.")
            return False
    else:
        st.warning("User not found.")
        return False
    
    cursor.close()
    conn.close()



# Custom CSS for styling the app
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@400;700&family=Open+Sans:wght@300;400;600&display=swap');

    body {
        background: #020205;
        color: #ecf0f1;
        font-family: 'Open Sans', sans-serif;
        height:100%;
        width:100%;
    }
    .stApp {
        background-color: #020205;
        color: #ecf0f1;
        font-family: 'Open Sans', sans-serif;
        height:100%;
        width:100%;
    }
    h1 {
        text-align: center;
        color: #f5d061;
        font-family: 'Arial', sans-serif;
        text-shadow: 2px 2px 5px black;
        font-size: 40px;
        width:100%;
    }

    /* Style for the login/signup form in the top-right navbar */
    .top-nav {
        position: fixed;
        top: 10px;
        right: 10px;
        padding: 10px;
        background-color: #1e1e1e;
        border-radius: 8px;
        z-index: 999;
    }
    
    .top-nav a {
        color: #ecf0f1;
        text-decoration: none;
        margin: 0 10px;
        font-size: 18px;
        font-weight: 600;
    }

    .top-nav a:hover {
        color: #a80038;
    }

    /* Style for the footer */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #1e1e1e;
        color: #ecf0f1;
        text-align: center;
        padding: 10px 0;
        font-size: 14px;
    }

    .stButton > button {
        background-color: #a80038;
        color: white;
        border: none;
        border-radius: 5px;
        width: 18%;
    }
    .stButton > button:hover {
        background-color: #87002f;
        color: white;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# Heading
st.markdown("<h1>Code Explanation and Debugging Assistant</h1>", unsafe_allow_html=True)

# Navbar with login/signup options in the top-right
st.markdown(
    """
    <div class="top-nav">
        <a href="#signup" onclick="document.getElementById('signup').style.display='block';">Sign Up</a>
        <a href="#login" onclick="document.getElementById('login').style.display='block';">Login</a>
    </div>
    """,
    unsafe_allow_html=True
)

if "previous_searches" not in st.session_state:
    st.session_state.previous_searches = []
if "current_input" not in st.session_state:
    st.session_state.current_input = ""

# Sidebar for previous searches
sidebar = st.sidebar
sidebar.title("Previous Searches")

selected_search = sidebar.selectbox(
    "Click to see previous searches:",
    options=[""] + st.session_state.previous_searches,
    index=0,
)

if selected_search and selected_search != st.session_state.current_input:
    st.session_state.current_input = selected_search

# Text area for code input
user_input = st.text_area(
    "Enter your code snippet or prompt here:",
    value=st.session_state.current_input,
    height=235,
    key="user_input_area",
)

# Buttons for explanation and debugging
if st.button("Explain Code"):
    if user_input:
        st.session_state.previous_searches.append(user_input)
        st.session_state.previous_searches = list(set(st.session_state.previous_searches))  # Remove duplicates
        st.session_state.current_input = ""  # Clear input field
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": f"Explain the following code:\n\n{user_input}\n\nExplanation:"}],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )
        st.subheader("Explanation:")
        response_text = ""
        for chunk in completion:
            response_text += chunk.choices[0].delta.content or ""
        st.write(response_text)
    else:
        st.warning("Please enter a code snippet or prompt.")

if st.button("Debug Code"):
    if user_input:
        st.session_state.previous_searches.append(user_input)
        st.session_state.previous_searches = list(set(st.session_state.previous_searches))  # Remove duplicates
        st.session_state.current_input = ""  # Clear input field
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": f"Identify bugs in the following code and suggest fixes:\n\n{user_input}\n\nBugs and Fixes:"}],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )
        st.subheader("Debugging Suggestions:")
        response_text = ""
        for chunk in completion:
            response_text += chunk.choices[0].delta.content or ""
        st.write(response_text)
    else:
        st.warning("Please enter a code snippet or prompt.")

# User Authentication Form (Signup/Login)
page = st.radio("Choose an option", ("Login", "Signup"))

if page == "Signup":
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    email = st.text_input("Email")
    
    if st.button("Sign Up"):
        if username and password and email:
            signup(username, password, email)
        else:
            st.warning("Please fill out all fields.")

elif page == "Login":
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Log In"):
        if username and password:
            login(username, password)
        else:
            st.warning("Please fill out all fields.")

# Footer
st.markdown(
    """
    <div class="footer">
        <p> &#169; 2024 &nbsp;&nbsp;Code Companion : Your Cloud-Based Code Debugger private Ltd. 
    </div>
    """,
    unsafe_allow_html=True
)
