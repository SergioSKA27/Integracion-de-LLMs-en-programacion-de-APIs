import google.generativeai as genai
import gradio as gr
import pypdf

APIKEY = ""  # YOUR API KEY HERE

genai.configure(api_key=APIKEY)


def save_txt(text, filename):
    with open(filename, "w", encoding="utf8") as f:
        f.write(text)


def read_pdf(file_path):
    """
    Reads the text content of a PDF file.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        str: The text content of the PDF file.
    """
    fi = pypdf.PdfReader(file_path)
    text = ""
    for page in fi.pages:
        text += page.extract_text()

    return text


pdf = read_pdf("static/cuento.pdf")


def conversacion_2(texto):
    model = genai.GenerativeModel("gemini-1.5-flash")
    inst = f"Genera una lista de 5 elementos que presenten los elementos más importantes de la historia contenida en el  siguiente texto: {texto}"
    response = model.generate_content(inst)
    log = f"User: {inst}\nModel: {response.text}\n"
    save_txt(log, "conversacion_2.txt")
    return response.text


iface = gr.Interface(
    fn=conversacion_2,
    inputs=gr.Dropdown([pdf], label="Texto"),
    outputs="text",
    title="Conversación 2",
)

iface.launch(share=False)
