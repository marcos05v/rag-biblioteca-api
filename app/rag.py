from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import psycopg
import os
from google import genai
from . import pdf

#Bloque 1: conexopnes y cosas que se carguen 1 vez

print('Cargando modelo...')
modelo = SentenceTransformer('all-MiniLM-L6-v2')
print('Modelo cargado')

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print('No se encontro la API key')

cliente = genai.Client(api_key = api_key)

DATADB = "host=localhost port=5432 dbname=rag user=rag password=rag"

# Bloque 2: funciones

def trocear(texto, tamano=80, solape=20):
    palabras = texto.split()
    chunks = []
    i = 0
    while i < len(palabras):
        pedazo = palabras[i:i+tamano]
        chunks.append(' '.join(pedazo))
        i += tamano -solape
    return chunks

def a_pgvector(vector):
    return "["+",".join(str(x) for x in vector) + "]"


#Bloque 3



def indexar(documento,texto):
    chunkTexto = trocear(texto)

    with psycopg.connect(DATADB) as conexion:
        with conexion.cursor() as cur:
            cur.execute("DELETE FROM chunks WHERE documento = %s", (documento,))
            for contenido in chunkTexto:
                vector = modelo.encode(contenido)
                cur.execute(
                    'INSERT INTO chunks (documento, contenido, embedding) VALUES (%s, %s, %s)',
                    (documento, contenido, a_pgvector(vector)),
                )
        conexion.commit()
    return f'se guardaron {len(chunkTexto)} chunks'

#Uso de leer pdf del archivo pdf.py para que se comunique con indexar pdf

def indexar_pdf(documento,ruta):
    texto = pdf.leer_pdf(ruta)
    return indexar(documento, texto)

def borrar_documento(documento):
    with psycopg.connect(DATADB) as conexion:
        with conexion.cursor() as cur:
            cur.execute(
                'DELETE FROM chunks WHERE documento = %s',(documento,)
            )
            borrados = cur.rowcount
        conexion.commit()
    return borrados

def recuperar(pregunta, k=10):
    vector = modelo.encode(pregunta)

    with psycopg.connect(DATADB) as conexion:
        with conexion.cursor() as cur:

            cur.execute(
                'SELECT contenido, embedding <=> %s AS distancia FROM chunks ORDER BY distancia LIMIT %s',
                (a_pgvector(vector), k)
            )
            filas = cur.fetchall()
    return filas

def responder(pregunta):
    filas = recuperar(pregunta)
    contexto = "\n\n".join(fila[0] for fila in filas)
    prompt = f"""
    Responde la pregunta usando unicamente el siguiente contexto.
    Si la respuesta no esta en el contexto, di que no tienes esa informacion.

    Contexto: {contexto}

    Pregunta: {pregunta}
    """

    respuesta = cliente.models.generate_content(
        model = "gemini-3.6-flash",
        contents = prompt
    )
    return respuesta.text
