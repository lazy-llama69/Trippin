import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Configure Gemini API key from environment variable
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_chat_response():

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input and handle it
    if prompt := st.chat_input("Ask me anything!"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
            with st.spinner("Thinking..."):
        # Generate assistant's response using Gemini
                try:
                    response = model.generate_content(
                        prompt,
                        generation_config=genai.types.GenerationConfig(
                            temperature=1.5,  # You can adjust the temperature here
                        ),
                    )
                    # Add assistant message to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response.text})

                    # Display assistant message in chat message container
                    with st.chat_message("assistant"):
                        st.markdown(response.text)
                except Exception as e:
                    # Handle any errors that may occur
                    st.error(f"Error generating response: {e}")