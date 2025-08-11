# main.py
# Versión final y ultra rápida usando la API de Groq.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_groq import ChatGroq # Importamos el chat de Groq
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
import os
from dotenv import load_dotenv

# Cargar las variables de entorno (nuestra clave de API) desde el archivo .env
load_dotenv()

# --- 1. Definición de Rutas y Constantes ---
CHROMA_PATH = "chroma_db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
# Usaremos el modelo Llama 3 de 8B que está disponible en Groq
GROQ_MODEL = "llama3-8b-8192"

# --- 2. Definición del Modelo de Datos para la API ---
class Query(BaseModel):
    query_text: str

# --- 3. Inicialización de la Aplicación FastAPI ---
app = FastAPI()

# Configuración de CORS
origins = ["*"]
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

@app.on_event("startup")
async def startup_event():
    global rag_chain
    
    print("--- Evento de Inicio: Configurando la cadena RAG con Groq ---")
    
    # 1. Cargar la base de datos vectorial local.
    embeddings = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL)
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    print(f"Base de datos cargada. Contiene {db._collection.count()} documentos.")

    # 2. Crear el retriever.
    retriever = db.as_retriever(search_kwargs={'k': 5})

    # 3. Conectar con el modelo LLM en la nube de Groq.
    # LangChain automáticamente encontrará la API key en el archivo .env
    model = ChatGroq(model=GROQ_MODEL)

    # 4. Crear el prompt.
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    # 5. Crear la cadena RAG.
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
    print("--- ¡Cadena RAG con Groq lista! ---")


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
    uvicorn.run(app, host="0.0.0.0", port=8000)

