# main.py
# Este es el servidor web que recibirá las preguntas y devolverá las respuestas.
# Utiliza FastAPI para crear la API, y LangChain para orquestar la lógica.

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
OLLAMA_MODEL = "llama3:8b" # Asegúrate de tener este modelo con 'ollama pull llama3:8b'

# --- 2. Definición del Modelo de Datos para la API ---
# Pydantic nos ayuda a validar los tipos de datos de entrada.
# Esperamos recibir un JSON con una clave "query_text".
class Query(BaseModel):
    query_text: str

# --- 3. Inicialización de la Aplicación FastAPI ---
app = FastAPI()

# Configuración de CORS (Cross-Origin Resource Sharing)
# Esto es MUY importante para permitir que tu app de Flutter (que se ejecuta
# en un "origen" diferente) pueda comunicarse con este servidor.
origins = [
    "http://localhost",
    "http://localhost:8080", # Origen común para apps web locales
    # Aquí podrías añadir el origen de tu app Flutter cuando la despliegues
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"], # Permite todas las cabeceras
)

# --- 4. Lógica del Chatbot (El Corazón del Sistema) ---

# Plantilla del Prompt: Esta es la instrucción que le damos al LLM.
# Le decimos cómo debe comportarse y qué información debe usar.
PROMPT_TEMPLATE = """
Responde a la pregunta basándote únicamente en el siguiente contexto:

{context}

---

Responde a la pregunta basándote en el contexto anterior: {question}
"""

def setup_rag_chain():
    """
    Configura y devuelve la cadena RAG (Retrieval-Augmented Generation).
    Esta función se llamará una vez al iniciar el servidor.
    """
    print("Configurando la cadena RAG...")
    # 1. Cargar la base de datos vectorial que creamos en Colab.
    embeddings = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL)
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    print(f"Base de datos cargada. Contiene {db._collection.count()} documentos.")

    # 2. Crear un "retriever" para buscar en la base de datos.
    # search_kwargs={'k': 3} significa que buscará los 3 trozos más relevantes.
    retriever = db.as_retriever(search_kwargs={'k': 3})

    # 3. Conectar con el modelo LLM local a través de Ollama.
    model = Ollama(model=OLLAMA_MODEL)

    # 4. Crear el prompt a partir de la plantilla.
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    # 5. Crear la "cadena" o "pipeline" de LangChain.
    # Esto define el flujo de datos:
    # - La pregunta del usuario pasa al retriever.
    # - El retriever busca documentos y los pasa al prompt junto con la pregunta.
    # - El prompt formateado pasa al modelo.
    # - La salida del modelo se convierte a texto.
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
    print("¡Cadena RAG lista!")
    return rag_chain

# Creamos la cadena una vez al inicio.
rag_chain = setup_rag_chain()

# --- 5. Definición del Endpoint de la API ---
# Aquí es donde nuestra app de Flutter hará las peticiones.
@app.post("/query")
async def handle_query(query: Query):
    """
    Maneja una petición de consulta.
    Recibe una pregunta, la procesa con la cadena RAG y devuelve la respuesta.
    """
    print(f"Recibida pregunta: {query.query_text}")
    # Usamos la cadena RAG para obtener la respuesta.
    # 'invoke' ejecuta la cadena con la entrada dada.
    response = rag_chain.invoke(query.query_text)
    
    print(f"Respuesta generada: {response}")
    return {"response": response}

# --- 6. Punto de Entrada para Ejecutar el Servidor ---
# (Opcional, pero útil para ejecutar directamente)
if __name__ == "__main__":
    import uvicorn
    # Esto permite ejecutar el servidor con 'python main.py'
    uvicorn.run(app, host="0.0.0.0", port=8000)

