# Chatbot ITES

Chatbot orientado a responder consultas sobre las carreras, requisitos, sedes y materias del Instituto Tecnológico de Estudios Superiores (ITES), utilizando un modelo de Gemini y un flujo de recuperación de información basado en un PDF institucional.

## Descripción

Este proyecto implementa una interfaz web con Streamlit para interactuar con un asistente inteligente que responde únicamente con información contenida en la documentación provista por la institución. El sistema usa:

- Google Gemini como modelo generativo
- Streamlit para la interfaz de chat
- Un PDF con la oferta académica del ITES como base de conocimiento
- RAG (Retrieval-Augmented Generation) mediante incorporación del texto del PDF como contexto del sistema

La intención es que el chatbot responda preguntas de tipo académico, como:

- cuáles son las carreras disponibles
- qué materias incluye cada carrera
- qué requisitos se necesitan para inscribirse o cursar una carrera
- en qué sedes se dicta cada propuesta

## Funcionalidades

- Chat en tiempo real desde la interfaz web
- Respuestas guiadas por un sistema de instrucciones explícitas
- Restricción de respuestas a información del documento institucional
- Soporte para preguntas acerca de carreras, materias y requisitos
- Reinicio de conversación desde la barra lateral
- Configuración sencilla mediante variables de entorno

## Tecnologías utilizadas

- Python
- Streamlit
- Google GenAI
- python-dotenv
- pypdf

## Estructura del proyecto

```text
Chatbot ITES/
├── main.py                  # Aplicación principal del chatbot
├── .env                    # Variables de entorno locales (no incluido por defecto)
├── requirements.txt         # Dependencias del proyecto
├── README.md               # Documentación del proyecto
├── data/
│   └── ites_oferta_academica.pdf  # PDF con la oferta académica
└── .venv/                  # Entorno virtual local (si se utiliza)
```

## Requisitos previos

Antes de ejecutar el proyecto, debes tener instalado:

- Python 3.10 o superior
- pip
- Un proyecto o cuenta con acceso a la API de Google Gemini

## Instalación

1. Clona o descarga este repositorio.
2. Abre una terminal en la carpeta del proyecto.
3. Crea y activa un entorno virtual, si lo deseas:

```bash
python -m venv .venv
.venv\Scripts\activate
```

4. Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Configuración de variables de entorno

Crea un archivo llamado .env en la raíz del proyecto con el siguiente contenido:

```env
API_KEY=tu_api_key_de_google_gemini
MODEL_NAME=gemini-3.5-flash-lite
```

### Explicación

- API_KEY: clave de acceso a la API de Gemini
- MODEL_NAME: nombre del modelo a utilizar, en este caso gemini-3.5-flash-lite

## Preparación del PDF

Coloca el archivo PDF institucional dentro de la carpeta data con el nombre:

```text
data/ites_oferta_academica.pdf
```

Este archivo debe contener la información relevante sobre:

- carreras disponibles
- materias de cada carrera
- requisitos de ingreso o cursado
- sedes y modalidad
- información institucional relevante para responder consultas

## Ejecución

Desde la raíz del proyecto, ejecuta:

```bash
streamlit run main.py
```

Luego, abre la URL local que muestra Streamlit en el navegador.

## Uso del chatbot

Una vez levantada la aplicación:

1. Escribe una pregunta en el chat.
2. El sistema integra el historial de conversación y el contexto del PDF.
3. El modelo responde usando únicamente la documentación provista.
4. Si la consulta no corresponde a las carreras o temas del ITES, responde con:

> Lo siento, solo puedo responder consultas sobre las carreras del ITES.