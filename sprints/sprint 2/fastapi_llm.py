import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel

APIKEY = ""  # YOUR API KEY HERE

genai.configure(api_key=APIKEY)

def save_txt(text, filename):
    with open(filename, "w", encoding="utf8") as f:
        f.write(text)


class ConversationTurn(BaseModel):
    inst: str  # the instruction to the model
    text: str  # the text to be used as context for the model

app = FastAPI() # create a FastAPI app

@app.post("/chat/")
async def chat(contextTurn: ConversationTurn):
    """
    Generates a response to the user input using a generative AI model.

    Args:
        contextTurn (ConversationTurn): The user input and the model response.

    Returns:
        ConversationTurn: The user input and the model response.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    inst = f"{contextTurn.inst}   El texto que deberás analizar es el siguiente: {contextTurn.text}"
    response = model.generate_content(inst)
    log = f"User: {inst}\nModel: {response.text}\n"
    save_txt(log, "conversacion_1.txt")
    return ConversationTurn(inst=inst, text=response.text)

