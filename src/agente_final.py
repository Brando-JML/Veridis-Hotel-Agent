import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_cohere import ChatCohere
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 1. Cargar variables de entorno
load_dotenv()

DB_DIR = os.path.join(os.path.dirname(__file__), "..", "chroma_db")

def inicializar_agente():
    print("[INFO] Inicializando servicios del agente RAG...")
    
    # 2. Conexion a la Base de Datos Vectorial
    modelo_embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    vectorstore = Chroma(persist_directory=DB_DIR, embedding_function=modelo_embeddings)
    recuperador = vectorstore.as_retriever(search_kwargs={"k": 4})
    
    # 3. Inicializacion del LLM (Cohere)
    llm = ChatCohere(model="command-r-plus-08-2024", temperature=0.1)
    
    # 4. EL PROMPT MAESTRO (Modificado sin instrucciones de citacion)
    instrucciones_sistema = (
        "Eres el asistente virtual corporativo de Veridis Eco-Park & Resort. "
        "Tu objetivo es asistir a los usuarios basandote exclusivamente en el contexto proporcionado.\n\n"
        "Reglas de operacion:\n"
        "1. Si la informacion solicitada no se encuentra en el contexto, responde textualmente: "
        "'No dispongo de esta informacion en los documentos actuales. Por favor, comuniquese a la extension 911 (Recepcion).'\n"
        "2. No generes ni asumas datos, precios o politicas externas al contexto.\n\n"
        "Contexto recuperado:\n{context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", instrucciones_sistema),
        ("human", "{input}"),
    ])
    
    # Formateo limpio (Sin inyectar el nombre del archivo origen)
    def formatear_documentos(docs):
        return "\n\n---\n\n".join([doc.page_content for doc in docs])
    
    # Cadena de ejecucion LCEL
    cadena_rag = (
        {"context": recuperador | formatear_documentos, "input": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    print("[INFO] Agente inicializado correctamente.")
    return cadena_rag

if __name__ == "__main__":
    agente = inicializar_agente()
    
    print("\n" + "="*50)
    print("Terminal de Asistencia Veridis (Escriba 'salir' para terminar)")
    print("="*50 + "\n")
    
    while True:
        pregunta = input("Usuario: ")
        if pregunta.lower() in ['salir', 'exit', 'quit']:
            print("[INFO] Sesion finalizada por el usuario.")
            break
            
        print("[INFO] Consultando base de conocimientos...")
        respuesta = agente.invoke(pregunta) 
        
        print(f"\nVeridis AI:\n{respuesta}\n")