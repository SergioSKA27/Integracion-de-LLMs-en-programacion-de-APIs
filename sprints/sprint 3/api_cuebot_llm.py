import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel

APIKEY = ""  # YOUR API KEY HERE

genai.configure(api_key=APIKEY)


class ConversationTurn(BaseModel):
    user: str  # who made the request or responded
    input: str  # the response of the model or user
    corpus: str  # the text to be used as context for the model


app = FastAPI()



@app.post("/complete/")
async def complete(contextTurn: ConversationTurn):
    """
    Generates a response to the user input using a generative AI model.

    Args:
        contextTurn (ConversationTurn): The user input and the model response.

    Returns:
        ConversationTurn: The user input and the model response.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    inst = f"{contextTurn.input}  basado en el siguiente contexto: {contextTurn.corpus}"
    response = model.generate_content(inst)
    return ConversationTurn(user="model", input=response.text, corpus=contextTurn.corpus)