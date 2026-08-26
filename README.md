# Chatbot ITES

Chatbot orientado a responder consultas sobre las carreras, requisitos, sedes y materias del Instituto Tecnológico de Estudios Superiores (ITES), utilizando un modelo de Gemini y un flujo de recuperación de información basado en un PDF institucional.

![Proyecto funcionando](/data/Chatbot.png)

Se utilizó el modelo de ```gemini-3.5-flash-lite```. Que tiene los siguientes coste por millón de tokens:
TOKEN INPUT = $0.30
TOKEN OUTPUT = $2.50

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