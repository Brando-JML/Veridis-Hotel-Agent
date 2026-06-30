import os
from langchain_text_splitters import MarkdownHeaderTextSplitter


DOCS_DIR = os.path.join(os.path.dirname(__file__), "..", "veridis_doc")


headers_to_split_on = [
    ("#", "Titulo_Principal"),
    ("##", "Subtitulo_Categoria"),
    ("###", "Seccion_Especifica")
]


markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

def extraer_y_procesar_documentos():
    chunks_totales = []
    
    # 3. Iterar sobre cada archivo en nuestra carpeta veridis_doc
    for nombre_archivo in os.listdir(DOCS_DIR):
        if nombre_archivo.endswith(".md"):
            ruta_completa = os.path.join(DOCS_DIR, nombre_archivo)
            
            # Leer el archivo en texto plano
            with open(ruta_completa, 'r', encoding='utf-8') as f:
                texto_puro = f.read()
                
            # 4. Dividir el texto inteligentemente (Chunking)
            chunks = markdown_splitter.split_text(texto_puro)
            
            # 5. Atribución de Metadatos extra (Agregamos el nombre del archivo)
            for chunk in chunks:
                chunk.metadata["Archivo_Origen"] = nombre_archivo
                chunks_totales.append(chunk)
                
    return chunks_totales

if __name__ == "__main__":
    # Ejecutamos la función
    fragmentos_listos = extraer_y_procesar_documentos()
    
    # Imprimir resultados en la terminal para verificar
    print(f" ¡Éxito! Se generaron {len(fragmentos_listos)} fragmentos (chunks) estructurados.\n")
    
    # Ver un ejemplo de cómo quedó la data para la IA
    print("--- EJEMPLO DE UN FRAGMENTO PROCESADO ---")
    print(f" METADATOS: {fragmentos_listos[5].metadata}")
    print(f" CONTENIDO:\n{fragmentos_listos[5].page_content[:200]}...")