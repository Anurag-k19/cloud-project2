import os
from dotenv import load_dotenv
import streamlit as st
from groq import Groq

load_dotenv()

#Enter your groq_api_key
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

#Used streamlit to create the heading and a text area
st.markdown("<h1 style='text-align: center;'>Code Explanation and Debugging Assistant</h1>", unsafe_allow_html=True)
user_input = st.text_area("Enter your code snippet or prompt here:", height=300)

#button to invoke explanation
if st.button("Explain Code"):
    if user_input:  #it is to check if the user has given input or not
        #sending an request to groq api to provide explanation
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": f"Explain the following code:\n\n{user_input}\n\nExplanation:"}],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )

        #display explanation based on the response of Api
        st.subheader("Explanation:")
        response_text = ""
        for chunk in completion:
            response_text += chunk.choices[0].delta.content or ""
        st.write(response_text)
    else: 
        st.warning("Please enter a code snippet or prompt.")

#button to invoke debugging
if st.button("Debug Code"):
    if user_input: #it is to check if the user has given input or not
        #sending an request to groq api to provide response
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": f"Identify bugs in the following code and suggest fixes:\n\n{user_input}\n\nBugs and Fixes:"}],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )
         #display debugging based on the response of Api
        st.subheader("Debugging Suggestions:")
        response_text = ""
        for chunk in completion:
            response_text += chunk.choices[0].delta.content or ""
        st.write(response_text)
    else: 
        st.warning("Please enter a code snippet or prompt.")
