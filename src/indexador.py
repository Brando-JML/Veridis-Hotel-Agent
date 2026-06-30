import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from procesador_textos import extraer_y_procesar_documentos

# 1. Definir la ruta donde se guardará la base de datos
DB_DIR = os.path.join(os.path.dirname(__file__), "..", "chroma_db")

def crear_base_vectorial():
    print("1/3 - Extrayendo y dividiendo documentos (Paso 2)...")
    fragmentos = extraer_y_procesar_documentos()
    
    print("2/3 - Inicializando modelo de Embeddings (HuggingFace)...")
    # Usamos un modelo multilingüe ligero y gratuito, ideal para español
    modelo_embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    
    print("🗄️ 3/3 - Creando base de datos vectorial en ChromaDB...")
    # Chroma tomará los textos, los convertirá a vectores y los guardará localmente
    vectorstore = Chroma.from_documents(
        documents=fragmentos,
        embedding=modelo_embeddings,
        persist_directory=DB_DIR
    )
    
    print(f"Éxito! Base de datos creada y guardada en la carpeta: {DB_DIR}")
    return vectorstore

if __name__ == "__main__":
    crear_base_vectorial()