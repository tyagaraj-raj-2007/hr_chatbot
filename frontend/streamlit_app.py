import streamlit as st
import requests

st.title("HR Resource Query Chatbot")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Enter your query (e.g., 'Find Python developers with 3+ years experience')"):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Call FastAPI backend
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json={"text": prompt}
        )
        response.raise_for_status()
        result = response.json()["response"]

        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(result)
        st.session_state.messages.append({"role": "assistant", "content": result})
    except requests.exceptions.RequestException as e:
        st.error(f"Error: Could not connect to backend. {str(e)}")