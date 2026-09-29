CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE chunks(
    id SERIAL PRIMARY KEY,
    contenido TEXT NOT NULL,
    embedding vector(384) NOT NULL,
    documento TEXT NOT NULL
);