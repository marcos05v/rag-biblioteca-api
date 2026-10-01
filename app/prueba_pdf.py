from pypdf import PdfReader

lector = PdfReader("uploads/Reporte_IEEE_WDBC.pdf")

texto = ""


for pagina in lector.pages:
    texto = texto + pagina.extract_text()
    
    
print(texto[:500])