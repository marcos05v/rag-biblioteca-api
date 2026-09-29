from sentence_transformers import SentenceTransformer
from sentence_transformers import util


print('Cargando modelo...')
modelo = SentenceTransformer("all-MiniLM-L6-V2")
print('Modelo cargado.')

    # frase = 'Los libros de la Biblioteca se prestan por quince días'
    # vector = modelo.encode(frase)

    # print('Cantidad de dimensiones:', len(vector))
    # print('El vector:', vector)


print('Cargando frases...')
frases = [
    'Los libro no pueden salir de la Biblioteca sin autorización',
    'Los libros de la Biblioteca se deben colocar en su lugar después de ser usados',
    'El partido inicia a las 8:00 pm y termina a las 10:00 pm'
]
print('Frases cargadas.')

vectores = modelo.encode(frases)

vectorA = vectores[0]
vectorB = vectores[1]
vectorC = vectores[2]

print('Similitud entre frase 1 y 2: ', util.cos_sim(vectorA, vectorB))
print('Similitud entre frase 1 y 3: ', util.cos_sim(vectorA, vectorC))

