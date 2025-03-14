import streamlit as st
import google.generativeai as genai
genai.configure(api_key="AIzaSyAHBdAQOzjZiAXUkWD-TjzymkwDd7kxB5g")
model = genai.GenerativeModel('gemini-1.5-flash')
def generate_chat_response() -> str:
    """
    Function to send a user's input to the AI model and get a response.
    Replace this with your chatbot model or API interaction.
    """
    try:
        prompt = st.chat_input(f"Can you give me a funny joke")
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=1.5,
            ),
        )
        st.markdown(response.text)
    except Exception as e:
        print(f"Attempt failed: {e}")
