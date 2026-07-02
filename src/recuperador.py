import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# 1. Definir la ruta de tu base de datos vectorial
DB_DIR = os.path.join(os.path.dirname(__file__), "..", "chroma_db")

def buscar_contexto(pregunta_usuario, n_fragmentos=3):
    print(f"🔎 Analizando la pregunta: '{pregunta_usuario}'\n")
    
    # 2. Inicializar el mismo modelo de Embeddings del Paso 3
    modelo_embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    
    # 3. Conectarse a la base de datos Chroma existente
    vectorstore = Chroma(
        persist_directory=DB_DIR,
        embedding_function=modelo_embeddings
    )
    
    # 4. Búsqueda Semántica (Retorna los N chunks más relevantes)
    resultados = vectorstore.similarity_search(pregunta_usuario, k=n_fragmentos)
    
    return resultados

if __name__ == "__main__":
    # Prueba de fuego: Hacemos una pregunta que no usa las palabras exactas del manual
    pregunta = "¿Qué pasa si mi mascota hace mucho ruido en la habitación?"
    
    fragmentos_recuperados = buscar_contexto(pregunta)
    
    print("=== FRAGMENTOS ENCONTRADOS PARA EL LLM ===")
    for i, doc in enumerate(fragmentos_recuperados, 1):
        origen = doc.metadata.get("Archivo_Origen", "Desconocido")
        seccion = doc.metadata.get("Titulo_Principal", "General")
        
        print(f"\n[{i}] Origen: {origen} | Sección: {seccion}")
        print(f"Texto extraído: {doc.page_content[:250]}...")