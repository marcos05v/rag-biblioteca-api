from sentence_transformers import SentenceTransformer
from sentence_transformers import util
import psycopg
from dotenv import load_dotenv
import os
from google import genai

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print('no se encontro la API Key')

cliente = genai.Client(api_key=api_key)
def a_pgvector(vector):
    return "["+",".join(str(x) for x in vector) + "]"


print('Cargando modelo...')
modelo = SentenceTransformer('all-MiniLM-L6-v2')
print('Modelo cargado')

pregunta = '¿Qué es la Guelaguetza?'
vector = modelo.encode(pregunta)


DATADB = "host=localhost port=5432 dbname=rag user=rag password=rag"

with psycopg.connect(DATADB) as conexion:
    with conexion.cursor() as cur:
        
            cur.execute(
                'SELECT contenido, embedding <=> %s AS distancia FROM chunks ORDER BY distancia LIMIT 5',
                (a_pgvector(vector),)
            )
            filas = cur.fetchall()


contexto = "\n\n".join(fila[0] for fila in filas)

prompt = f""" Responde la pregunta usando unicamente el siguiente contexto.

Si la respuesta no esta en el contexto, di que no tienes esa informacion.

Contexto:
{contexto}

Pregunta: {pregunta}"""

respuesta = cliente.models.generate_content(
    model="gemini-3.6-flash",
    contents= prompt
)
print(respuesta.text)









# with psycopg.connect(DATADB) as conexion:
#     with conexion.cursor() as cur:
        
#         cur.execute(
#             'SELECT id, documento, contenido FROM chunks ORDER BY embedding <=> %s LIMIT 5',
#             (a_pgvector(vector),)
#         )
#         filas = cur.fetchall()
#         for fila in filas:
#             print(fila[1], '|', fila[2])

