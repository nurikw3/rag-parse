import streamlit as st
import requests

st.title("🧠 RAG-Parse Chat")

st.sidebar.title("⚙️ Model Config")


model = st.sidebar.selectbox(
    "Choose model:",
    ["deepseek-ai/DeepSeek-R1-0528", "openai/gpt-oss-120b", "LLM360/K2-Think"]
)
st.sidebar.markdown(f"**Selected:** `{model}`")


if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ask your question:")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("⌛ Thinking...")

        try:
            response = requests.post(
                "http://backend:8000/ask",
                json={"question": prompt, "model": model},
                timeout=60
            )
            if response.status_code == 200:
                answer = response.json()["answer"]
                placeholder.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                placeholder.markdown(f"❌ Error: {response.text}")
        except Exception as e:
            placeholder.markdown(f"⚠️ Request failed: {e}")
