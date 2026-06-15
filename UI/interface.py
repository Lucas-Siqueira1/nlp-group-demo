import asyncio
import sys
import uuid
from pathlib import Path

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def ask_agent(prompt: str, session_id: str) -> str:
    from main import run

    return asyncio.run(run(prompt, session_id=session_id))


st.set_page_config(
    page_title="Assistente de Saúde",
    layout="centered",
)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = f"streamlit-{uuid.uuid4()}"

with st.sidebar:
    st.title("Assistente de Saúde")
    st.caption("Demonstração com agentes para busca e análise de informações de saúde.")

    if st.button("Limpar conversa", use_container_width=True):
        st.session_state.messages = []
        st.session_state.session_id = f"streamlit-{uuid.uuid4()}"
        st.rerun()

st.title("Assistente de Saúde")
st.info(
    "Este assistente oferece informações gerais e não substitui avaliação médica. "
    "Em caso de emergência, procure atendimento imediatamente.",
)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Digite sua dúvida ou informe seus dados de saúde...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analisando sua mensagem..."):
            try:
                response = ask_agent(prompt, st.session_state.session_id)
            except Exception as exc:
                response = (
                    "Não consegui processar sua mensagem agora. "
                    "Verifique as credenciais e tente novamente.\n\n"
                    f"Erro: `{exc}`"
                )

        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
