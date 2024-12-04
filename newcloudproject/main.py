import os
from dotenv import load_dotenv
import streamlit as st
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# Custom CSS for styling the app
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@400;700&family=Open+Sans:wght@300;400;600&display=swap');

    body {
        background: #020205;
        color: #ecf0f1;
        font-family: 'Open Sans', sans-serif;
    }
    .stApp {
        background-color: #020205;
        color: #ecf0f1;
        font-family: 'Open Sans', sans-serif;
    }
    .css-1d391kg { /* Sidebar container */
        background-color: #020205 !important;
    }
    .css-1e5imcs { /* Sidebar title and text color */
        color: #f5d061 !important;
    }
    h1 {
        text-align: center;
        color: #f5d061;
        font-family: 'Arial', sans-serif;
        text-shadow: 2px 2px 5px black;
        font-size: 40px;
    }
    textarea {
        background-color: #1e1e1e;
        color: #dcdcdc;
        width: 100%;
        height: 100%;
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
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1>Code Explanation and Debugging Assistant</h1>", unsafe_allow_html=True)

# Initialize session state for previous searches and current input
if "previous_searches" not in st.session_state:
    st.session_state.previous_searches = []
if "current_input" not in st.session_state:
    st.session_state.current_input = ""

# Sidebar for displaying and selecting previous searches
sidebar = st.sidebar
sidebar.title("Previous Searches")

selected_search = sidebar.selectbox(
    "Click to populate a previous search:",
    options=[""] + st.session_state.previous_searches,
    index=0,
)

if selected_search and selected_search != st.session_state.current_input:
    st.session_state.current_input = selected_search

# Text area for input
user_input = st.text_area(
    "Enter your code snippet or prompt here:",
    value=st.session_state.current_input,
    height=300,
    key="user_input_area",
)

# Buttons positioned above and below the text area
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

# Footer
st.markdown(
    """
    <div class="footer">
        <p> &#169; 2024 &nbsp;&nbsp;Code Companion : Your Cloud-Based Code Debugger private Ltd. 
    </div>
    """,
    unsafe_allow_html=True
)
