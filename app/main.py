from fastapi import FastAPI
from pydantic import BaseModel
from . import rag

app = FastAPI()

#Modelos de entradas, como los DTO en nest
class IndexarEntrada(BaseModel):
    documento : str
    texto : str

class PreguntaEntrada(BaseModel):
    pregunta : str


#Endpoints
@app.post('/indexar')
def indexar(entrada : IndexarEntrada):
    resultado = rag.indexar(entrada.documento, entrada.texto)
    return{"mensaje": resultado}

@app.post('/preguntar')
def preguntar(entrada: PreguntaEntrada):
    respuesta = rag.responder(entrada.pregunta)
    return{"respuesta": respuesta}