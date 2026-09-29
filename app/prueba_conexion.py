import psycopg

DATADB = "host=localhost port=5432 dbname=rag user=rag password=rag"

with psycopg.connect(DATADB) as conexion:
    with conexion.cursor() as cur:
        cur.execute("SELECT version();")
        resultado = cur.fetchone()
        print('Conexión establecida')
        print(resultado)