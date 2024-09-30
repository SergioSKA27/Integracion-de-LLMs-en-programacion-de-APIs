"""
Ejemplo 4: Draft de la interfaz grafica para CueBot
Sin embargo falta la conexion al LLM de tu eleccion :(
"""

import random
import time

import gradio as gr
import requests
from pypdf import PdfReader

# Variable auxiliar para guardar el texto del PDF
CORPUS_TEXT = ""

# Respuestas aleatorias para prueba del chatbot
RESPUESTAS_ALEATORIAS = [
    "Soy la respuesta aleatoria 1...",
    "Soy la respuesta aleatoria 2...",
    CORPUS_TEXT,
]


def get_response(input_text):
    """
    Obtiene la respuesta del LLM
    """
    global CORPUS_TEXT
    response = requests.post(
        "http://localhost:8000/complete/",
        json={"user": "user", "input": input_text, "corpus": CORPUS_TEXT},
        timeout=10,
    )
    return response.json()


def add_text(history, text):
    """
    Agrega texto a la historia del chat y actualiza la
    interfaz
    """

    history = history + [(text, None)]

    return history, gr.update(value="", interactive=False)


def add_file(history, file):
    """
    Permite agrega un texto pdf a la conversacion del chat
    y guardar
    """
    # agrega el nombre del archivo al Chat
    try:
        history = history + [((file.name,), None)]
    except AttributeError:
        history = history 

    # Leemos el texto del archivo PDF y lo guardamos en
    # CORPUS_TEXT para el futuro

    # Abre el archivo PDF en modo lectura binaria
    with open(file.name, "rb") as pdf_file:
        # Crea un lector de PDF
        pdf_reader = PdfReader(pdf_file)

        # Inicializa una variable para almacenar el texto extraído
        extracted_text = ""

        # Itera sobre todas las páginas del PDF y extrae el texto
        for page_num in range(len(pdf_reader.pages)):
            extracted_text += pdf_reader.pages[page_num].extract_text()

        # Comunica el texto recien leido a la variable global CORPUS_TEXT
        global CORPUS_TEXT
        CORPUS_TEXT = extracted_text
        print(CORPUS_TEXT)
    return history


def bot(history):
    """
    Obtiene la respuesta del Bot
    """
    # Genera una respuesta aleatoria para hacer prueba
    # trunk-ignore(bandit/B311)
    response = random.choice(RESPUESTAS_ALEATORIAS)

    # Extrae el ultimo input de texto de la historia de la
    # conversacion del bot
    input_text = history[-1][0]
    if "pregunta" in input_text: # añade el prefijo "pregunta" para probar el LLM con el archivo subido
        try:
            response = get_response(input_text)["input"]
        except Exception as e:
            response = f"No se pudo obtener respuesta del modelo LLM\n error: {e}"
    else:
        response = response

    # Define entrada de texto vacio
    history[-1][1] = ""

    # Genera el efecto de escribir lento con una pausa
    # Como si el texto se generara lentamente
    for character in response:
        history[-1][1] += character
        time.sleep(0.05)
        yield history


# Crea la aplicacion de Gradio
with gr.Blocks() as demo:

    # Crea ek chatbot
    chatbot = gr.Chatbot([], elem_id="chatbot", height=750)

    with gr.Row():

        # Cuadro de texto de conversacion
        with gr.Column(scale=1):
            txt = gr.Textbox(
                show_label=False,
                placeholder="Especifica el archivo pdf o ingresa un texto (para poder preguntar sobre el archivo usando el prefijo 'pregunta')",
                container=False,
            )

        # Cuadro de subida de archivo
        with gr.Column(scale=0.15, min_width=0):
            btn = gr.UploadButton("📁 Subir Archivo:", file_types=["pdf"])

    # Controlador de acciones para retroalimentar al bot
    # Con su respuesta
    txt_msg = txt.submit(
        fn=add_text, inputs=[chatbot, txt], outputs=[chatbot, txt], queue=False
    ).success(fn=bot, inputs=chatbot, outputs=chatbot)

    # Actualiza la convesacion con el texto generado
    txt_msg.success(
        fn=lambda: gr.update(interactive=True), inputs=None, outputs=[txt], queue=False
    )

    # Sube el archivo  y actualiza la conversacion
    file_msg = btn.upload(
        fn=add_file, inputs=[chatbot, btn], outputs=[chatbot], queue=False
    ).success(bot, chatbot, chatbot)


demo.queue()
if __name__ == "__main__":
    demo.launch(share=False)
