from pypdf import PdfReader

def leer_pdf(ruta):
    lector = PdfReader(ruta)
    texto = ""
    for pagina in lector.pages:
        texto = texto + pagina.extract_text()
    return texto 