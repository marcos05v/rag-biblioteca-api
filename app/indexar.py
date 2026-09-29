from sentence_transformers import SentenceTransformer
import psycopg

def trocear(texto, tamano=60, solape=15):
    palabras = texto.split()
    chunks = []
    i = 0
    while i < len(palabras):
        pedazo = palabras[i:i+tamano]
        chunks.append(' '.join(pedazo))
        i += tamano - solape

    return chunks

def a_pgvector(vector):
    return "["+",".join(str(x) for x in vector) + "]"


print('Cargando modelo..')
modelo = SentenceTransformer("all-MiniLM-L6-v2")
print('Modelo Cargado')

Guelaguetza = '''
La Guelaguetza es la festividad cultural y comunitaria más emblemática de Oaxaca, celebrada cada año durante los dos últimos lunes de julio en el Auditorio del Cerro del Fortín. Su nombre proviene del zapoteco guendalizaa, que significa «cooperación» o «acto de compartir», reflejando un principio ancestral de ayuda mutua que define la identidad oaxaqueña.

Su origen radica en un profundo sincretismo cultural. En la época prehispánica, los pueblos originarios subían al cerro para rendir culto a Centeótl, la diosa del maíz tierno, mediante rituales y ofrendas para asegurar buenas cosechas. Tras la colonización, la celebración se fusionó con la festividad católica de la Virgen del Carmen, hasta transformarse en 1932 en un encuentro folclórico formal que reúne a las ocho regiones del estado: Valles Centrales, La Cañada, La Costa, La Mixteca, La Sierra Norte, La Sierra Sur, El Istmo de Tehuantepec y La Cuenca del Papaloapan.

Durante la festividad, las delegaciones representativas comparten su música, trajes típicos y danzas icónicas, como la vistosa Flor de Piña, la majestuosa Danza de la Pluma o los alegres Sones e Istmeñas. Fieles al significado de su nombre, al concluir cada presentación, los danzantes obsequian al público productos característicos de sus tierras, como frutas, café, artesanías y mezcal. Más allá del escenario, la Guelaguetza envuelve a la ciudad de Oaxaca en un mes de fiesta que incluye desfiles de delegaciones, la elección de la Diosa Centeótl, la escenificación de la Leyenda de Donají y la tradicional Feria del Mezcal, consolidándose como la mayor expresión de diversidad, tradición y fraternidad del estado.
'''

chunkGuelaguetza = trocear(Guelaguetza)
Documento = 'Guelaguetza.txt'   

DATADB = "host=localhost port=5432 dbname=rag user=rag password=rag"

with psycopg.connect(DATADB) as conexion:
    with conexion.cursor() as cur:
        for contenido in chunkGuelaguetza:
            vector = modelo.encode(contenido)
            cur.execute(
                'INSERT INTO chunks (documento, contenido, embedding) VALUES (%s, %s, %s)',
                (Documento, contenido, a_pgvector(vector)),
            )
    conexion.commit()

print('Chunks e inserciones completadas')