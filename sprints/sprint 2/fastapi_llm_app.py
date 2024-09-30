import asyncio

import gradio as gr
import requests

with open("static/news_el_economista.txt", "r", encoding="utf8") as f:
    TEXT = f.read()


async def conversacion(inst, texto):
    """
    Generates a two-paragraph summary in Spanish of the given text using a generative AI model.

    Args:
        texto (str): The text to be summarized.

    Returns:
        str: The generated summary in Spanish.
    """
    response = await asyncio.to_thread(
        requests.post,
        "http://localhost:8000/chat/",
        json={"inst": inst, "text": texto},
        timeout=10,
    )
    return response.json()["text"]


iface = gr.Interface(
    fn=conversacion,
    inputs=[gr.Textbox("Instrucción"), gr.Dropdown([TEXT])],
    outputs="text",
    title="Prueba fastapi_llm",
)

iface.launch(share=False)
