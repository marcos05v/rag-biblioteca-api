SISTEMA RAG DE UNA BIBLIOTECA

Sistema que repsonde preguntas en base a los libros y/o documentos que se han subido a la biblioteca en la base de datos.

El sistema inicia cuando se sube un documento pdf. El sistema trocea el documento en chunks, ya con los chunks creados se convierten en embeddings, se guardan en pgvector.
Cuando se hace una pregunta se recuperan los chunks más relevantes por similitud semántica y se le pasa a un LLM que redacta la respuesta en base a ese contexto.

##STACK Tecnologico##
FastApi: Para la creación de las Apis, para indexar, y buscar
Postgres: Para la creación de las tablas  