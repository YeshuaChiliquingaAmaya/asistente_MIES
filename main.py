# main.py
# Este es el servidor web que recibirá las preguntas y devolverá las respuestas.
# Versión optimizada que permite elegir el modelo LLM al iniciar.

import argparse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.llms import Ollama
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

# --- 1. Definición de Rutas y Constantes ---
CHROMA_PATH = "chroma_db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# --- 2. Definición del Modelo de Datos para la API ---
class Query(BaseModel):
    query_text: str

# --- 3. Inicialización de la Aplicación FastAPI ---
app = FastAPI()

# Configuración de CORS
origins = ["*"] # Permitir todos los orígenes para simplificar las pruebas
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 4. Lógica del Chatbot (El Corazón del Sistema) ---
PROMPT_TEMPLATE = """
Responde a la pregunta basándote únicamente en el siguiente contexto:

{context}

---

Responde a la pregunta basándote en el contexto anterior: {question}
"""

# Variable global para la cadena RAG
rag_chain = None

# Usamos un "evento" de FastAPI para configurar la cadena cuando el servidor inicia.
# Esto es más limpio que hacerlo en el scope global.
@app.on_event("startup")
async def startup_event():
    global rag_chain
    
    print("--- Evento de Inicio: Configurando la cadena RAG ---")
    
    # 1. Cargar la base de datos vectorial.
    embeddings = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL)
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    print(f"Base de datos cargada. Contiene {db._collection.count()} documentos.")

    # 2. Crear el retriever.
    retriever = db.as_retriever(search_kwargs={'k': 5}) # Aumentamos a 5 para más contexto

    # 3. Conectar con el modelo LLM local a través de Ollama.
    # El modelo se define al iniciar el servidor, no está quemado aquí.
    model = Ollama(model=cli_args.model)

    # 4. Crear el prompt.
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    # 5. Crear la cadena RAG.
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
    print("--- ¡Cadena RAG lista! ---")


# --- 5. Definición del Endpoint de la API ---
@app.post("/query")
async def handle_query(query: Query):
    """Maneja una petición de consulta."""
    if not rag_chain:
        return {"error": "La cadena RAG no está inicializada."}, 503

    print(f"Recibida pregunta: {query.query_text}")
    response = rag_chain.invoke(query.query_text)
    
    print(f"Respuesta generada: {response}")
    return {"response": response}

# --- 6. Punto de Entrada para Ejecutar el Servidor ---
if __name__ == "__main__":
    import uvicorn
    
    # Configuración para aceptar argumentos desde la línea de comandos.
    # Esto nos permite elegir el modelo al arrancar el servidor.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model", 
        type=str, 
        default="phi3:mini", # Usamos phi3:mini por defecto por ser más rápido
        help="El nombre del modelo de Ollama a utilizar (ej: 'llama3:8b', 'phi3:mini')."
    )
    cli_args = parser.parse_args()
    print(f"--- Iniciando servidor con el modelo: {cli_args.model} ---")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)