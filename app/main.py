from fastapi import FastAPI, UploadFile, File, HTTPException
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

@app.post('/subir-pdf')
async def subir_pdf(archivo: UploadFile = File(...)):
    ... # Guardar el archivo PDF en una ubicación temporal
    contenido_bytes = await archivo.read()
    ruta = f"uploads/{archivo.filename}"
    with open(ruta, "wb") as f:
        f.write(contenido_bytes)
    resultado = rag.indexar_pdf(archivo.filename, ruta)
    return {"mensaje": resultado}

@app.delete('/documentos/{documento}')
def borrar(documento: str):
    borrados = rag.borrar_documento(documento)
    if borrados == 0:
        raise HTTPException(status_code=404, detail='No existe este documento')
    return {"mensaje": f"se borraron {borrados} chunks del documento {documento}"}

@app.get('/documentos')
def listar():
    return {'documentos': rag.listar_documentos()}
