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
    reader = PdfReader("./data/ITES_guia_completa_oferta_academica_2026.pdf")   
    for pagina in reader.pages:
        contexto_pdf += pagina.extract_text()
except Exception as exec:
    st.error(exec)

SYSTEM_INSTRUCTION = f"""
Eres un asistente de atención al cliente altamente especializado.
Tu ÚNICA función es responder preguntas basadas estrictamente en la siguiente documentación provista:
=== DOCUMENTACIÓN DE REFERENCIA ===
{contexto_pdf}
======================================================
REGLAS DE FUNCIONAMIENTO OBLIGATORIAS:
1. Responde únicamente con información que esté explícitamente respaldada en la documentación.
2. Si el usuario realiza una pregunta sobre un tema no incluido en el documento, responde amablemente: "Lo siento, solo puedo responder consultas sobre las carreras del ITES."
3. Mantén un tono profesional, claro y conciso.
"""

st.title("Chatbot especializado en el ITES")

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []
    st.session_state.token_input_total = 0
    st.session_state.token_output_total = 0    
    st.session_state.coste_total_input = 0
    st.session_state.coste_total_output = 0

with st.sidebar:
    st.subheader("Entrada")
    st.metric("Tokens Entrada", f"{st.session_state.token_input_total:.0f}")
    st.metric("Costo Entrada", f"${st.session_state.coste_total_input:.6f}")

    st.subheader("Salida")
    st.metric("Tokens Salida", f"{st.session_state.token_output_total:.0f}")
    st.metric("Costo Salida", f"${st.session_state.coste_total_output:.6f}")

    tokens_totales = st.session_state.token_input_total + st.session_state.token_output_total
    coste_totales = st.session_state.coste_total_input + st.session_state.coste_total_output

    st.subheader("Total")
    st.metric("Tokens Totales", f"{tokens_totales:.0f}")
    st.metric("Costes Totales", f"${coste_totales:.6f}")    

    if st.sidebar.button("Reiniciar conversación"):
        st.session_state.mensajes = []
        st.session_state.token_input_total = 0
        st.session_state.token_output_total = 0
        st.session_state.coste_total_input = 0
        st.session_state.coste_total_output = 0        
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
        caption_placeholder = st.empty()        

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

            full_response= ""
            ultima_metadata = None

            for chunk in response_stream:
                if chunk.text:
                    full_response += chunk.text
                    message_placeholder.markdown(full_response + " ")

                if getattr(chunk, "usage_metadata", None):
                    ultima_metadata = chunk.usage_metadata

            token_entrada = ultima_metadata.prompt_token_count or 0
            token_salida = ultima_metadata.candidates_token_count or 0
            tokens_razonamiento = ultima_metadata.thoughts_token_count or 0
            token_total = token_entrada + token_salida + tokens_razonamiento or 0

            coste_input = (token_entrada/1000000) * 0.30
            coste_output = ((token_salida + tokens_razonamiento)/1000000) * 2.50
            coste_total = coste_input + coste_output

            st.session_state.token_input_total += token_entrada
            st.session_state.token_output_total += token_salida   
            st.session_state.coste_total_input += coste_input
            st.session_state.coste_total_output += coste_output

            caption_placeholder.caption(
                f"Entrada {token_entrada} tokens, Coste {coste_input:.6f} - "
                f"Salida {token_salida + tokens_razonamiento} tokens - Coste {coste_output:.6f} - "
                f"Total {token_total} tokens - Coste {coste_total:.6f}"                                
            )


            message_placeholder.markdown(full_response)
            st.session_state.mensajes.append({"role": "assistant", "content": full_response})

            # Si querés que se vea el uso de tokens y el coste por mensaje sacá esto.
            st.rerun()

        except Exception as e:
            st.error(f"Hubo un error procesando el mensaje. Lo siento.")
            print(e)