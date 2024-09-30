import google.generativeai as genai
import gradio as gr

APIKEY = ""  # YOUR API KEY HERE

genai.configure(api_key=APIKEY)
def save_txt(text, filename):
    with open(filename, "w", encoding="utf8") as f:
        f.write(text)

with open("static/news_digital_bank.txt", "r", encoding="utf8") as f:
    TEXT = f.read()


def conversacion_1(texto):
    """
    Generates a two-paragraph summary in Spanish of the given text using a generative AI model.

    Args:
        texto (str): The text to be summarized.

    Returns:
        str: The generated summary in Spanish.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    inst = f"Obten un resumen en español, de dos párrafos de longitud, del contenido del siguiente texto: {texto}"
    response = model.generate_content(
        inst,
        )
    log = f"User: {inst}\nModel: {response.text}\n"
    save_txt(log, "conversacion_1.txt")

    return response.text


# generate a gradio interface to use the function conversacion_1
iface = gr.Interface(
    fn=conversacion_1,
    inputs=gr.Dropdown([TEXT]),
    outputs="text",
    title="Conversación 1",
)
iface.launch(share=False)
