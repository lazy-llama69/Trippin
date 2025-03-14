import streamlit as st
import google.generativeai as genai
genai.configure(api_key="AIzaSyAHBdAQOzjZiAXUkWD-TjzymkwDd7kxB5g")
model = genai.GenerativeModel('gemini-1.5-flash')
# Show title and description.
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses OpenAI's GPT-3.5 model to generate responses. "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
    "You can also learn how to build this app step by step by [following our tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
)

# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management

try:
    # Generate food title
    prompt = st.chat_input(f"Can you give me a funny joke")
    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=1.5,
        ),
    )
    filtered_text = ''.join([char for char in response.text if char.isalnum() or char.isspace()]) 
    st.markdown(filtered_text)
except Exception as e:
    print(f"Attempt failed: {e}")

