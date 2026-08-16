import os
import streamlit as st

from google import genai
from google.genai import types
from dotenv import load_dotenv
from pypdf import PdfReader

st.set_page_config(page_title="Chatbot ITES", page_icon="🤖")

load_dotenv()

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    st.error("No hay una API_KEY en las variables de entorno.")
    st.stop()


MODEL_NAME = os.getenv("MODEL_NAME")

if not MODEL_NAME:
    st.error("No hay un MODEL_NAME en las variables de entorno.")
    st.stop()

client = genai.Client(api_key=API_KEY)

contexto_pdf = ""
try:
    reader = PdfReader("./data/ites_oferta_academica.pdf")   
    for pagina in reader.pages:
        contexto_pdf += pagina.extract_text()
except Exception as exec:
    st.error(exec)

SYSTEM_INSTRUCTION = f"""
Eres un asistente de atención al cliente altamente especializado.
Tu ÚNICA función es responder preguntas basadas estrictamente en la siguiente documentación provista:
=== DOCUMENTACIÓN DE REFERENCIA (MANUAL Y PRECIOS) ===
{contexto_pdf}
======================================================
REGLAS DE FUNCIONAMIENTO OBLIGATORIAS:
1. Responde únicamente con información que esté explícitamente respaldada en la documentación.
2. Si el usuario realiza una pregunta sobre un tema no incluido en el documento (ej. deportes, política, recetas), responde amablemente: "Lo siento, solo puedo responder consultas sobre las carreras del ITES."
3. Mantén un tono profesional, claro y conciso.
"""

st.title("Chatbot especializado en el ITES")

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

if st.sidebar.button("Reiniciar conversación"):
    st.session_state.mensajes = []
    st.rerun()

for mensaje in st.session_state.mensajes:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

if prompt := st.chat_input("Hacé tus preguntas sobre el ITES"):
    st.session_state.mensajes.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            formatted_contents = []

            for mensaje in st.session_state.mensajes:
                role = "user" if mensaje["role"] == "user" else "model"
                formatted_contents.append({
                    "role": role,
                    "parts": [{"text": mensaje["content"]}]
                })

            response_stream = client.models.generate_content_stream(
                model=MODEL_NAME,
                contents=formatted_contents,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=0.2
                )
            )

            full_response = ""

            for chunk in response_stream:
                if chunk.text:
                    full_response += chunk.text
                    message_placeholder.markdown(full_response + " ")

            message_placeholder.markdown(full_response)
            st.session_state.mensajes.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"Error de procesamiento: {e}")        