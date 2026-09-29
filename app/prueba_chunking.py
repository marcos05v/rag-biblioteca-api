texto = "El gato duerme en el sofá"
palabras = texto.split()
#print('Palabras:', palabras)

print(palabras[0:3])
print(palabras[3:6])

def trocear(texto, tamano=10, solape=3):
    palabras = texto.split()
    chunks = []
    i = 0
    while i < len(palabras):
        pedazo = palabras[i:i+tamano]
        chunks.append(' '.join(pedazo))
        i += tamano - solape
    return chunks

texto1 = "una dos tres cuatro cinco seis siete ocho nueve diez once doce trece catorce quince"
resultado = trocear(texto1)
for i, chunk  in enumerate(resultado):
    print(i, ':', chunk)