# ingest.py
# Este script se encarga de procesar los datos del MIES (CSVs y PDFs)
# y los convierte en una base de datos vectorial usando ChromaDB.

import os
import pandas as pd
from langchain_community.document_loaders import PyPDFLoader, UnstructuredCSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document

# --- 1. Definición de Rutas y Constantes ---
# Ruta a la carpeta donde guardaremos la base de datos vectorial.
CHROMA_PATH = "chroma_db"
# Ruta a la carpeta donde tenemos nuestros datos (CSVs, PDFs).
DATA_PATH = "data"
# Nombre del modelo de embeddings que usaremos. Es multilingüe y potente.
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

def load_documents():
    """
    Carga los documentos desde la carpeta 'data'.
    Procesa archivos PDF y CSV de manera diferente para formatear el contenido.
    """
    documents = []
    # Iteramos sobre cada archivo en la carpeta de datos.
    for filename in os.listdir(DATA_PATH):
        file_path = os.path.join(DATA_PATH, filename)
        
        # --- Procesamiento para archivos PDF ---
        if filename.endswith('.pdf'):
            # Usamos PyPDFLoader para cargar el contenido del PDF.
            loader = PyPDFLoader(file_path)
            # 'load' devuelve una lista de documentos, uno por cada página.
            documents.extend(loader.load())
            print(f"Cargado {filename} como PDF.")

        # --- Procesamiento para archivos CSV ---
        elif filename.endswith('.csv'):
            print(f"Procesando {filename} como CSV...")
            try:
                # Usamos pandas para leer el CSV.
                # AÑADIMOS EL PARÁMETRO 'encoding' PARA MANEJAR CARACTERES ESPECIALES.
                df = pd.read_csv(file_path, encoding='latin-1')
                
                # Convertimos cada fila del CSV en un "Documento" de LangChain.
                # Esto nos permite darle un formato de texto claro a cada fila.
                for index, row in df.iterrows():
                    # Creamos el contenido del documento combinando las columnas que nos interesan.
                    # Usamos .get(col, '') para evitar errores si una columna no existe.
                    content = f"""
                    Servicio o Unidad: {row.get('TIPO_BENEFICIO', row.get('NOMBRE_UNIDAD', 'No especificado'))}
                    Descripción: {row.get('DESCRIPCION_BENEFICIO', 'No especificado')}
                    Requisitos: {row.get('REQUISITOS_ELEGIBILIDAD', 'No aplica')}
                    Monto: {row.get('MONTO_ASIGNADO', 'No aplica')}
                    Provincia: {row.get('PROVINCIA', 'No especificado')}
                    Cantón: {row.get('CANTON', 'No especificado')}
                    Dirección: {row.get('DIRECCION', 'No especificado')}
                    Tipo de Servicio: {row.get('TIPO_SERVICIO', 'No especificado')}
                    """
                    # Creamos el objeto Document con el contenido y la fuente (metadata).
                    doc = Document(
                        page_content=content.strip(),
                        metadata={"source": filename, "row": index}
                    )
                    documents.append(doc)
                print(f"Cargadas {len(df)} filas de {filename}.")
            except Exception as e:
                print(f"Error al procesar el archivo {filename}: {e}")
            
    return documents

def split_documents(documents):
    """
    Divide los documentos cargados en trozos más pequeños.
    Esto es crucial para que el modelo de embeddings pueda procesarlos
    y para que las búsquedas sean más precisas.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,      # Tamaño de cada trozo de texto.
        chunk_overlap=100,   # Cuánto se superponen los trozos entre sí.
        length_function=len,
        add_start_index=True
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Se han dividido {len(documents)} documentos en {len(chunks)} trozos.")
    return chunks

def main():
    """
    Función principal que orquesta todo el proceso de ingesta.
    """
    print("Iniciando la ingesta de datos...")
    
    # 1. Cargar los documentos de la carpeta 'data'.
    documents = load_documents()
    
    # 2. Dividir los documentos en trozos más manejables.
    chunks = split_documents(documents)
    
    # 3. Crear los embeddings y almacenar en ChromaDB.
    print("Creando embeddings y guardando en ChromaDB...")
    
    # Inicializamos el modelo de embeddings.
    # La primera vez que se ejecute, descargará el modelo (puede tardar un poco).
    embeddings = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL)
    
    # Creamos la base de datos vectorial a partir de los trozos de documentos.
    # LangChain se encarga de generar los embeddings y guardarlos.
    vector_store = Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )
    
    # Opcional: Persistir la base de datos (aunque from_documents ya lo hace con persist_directory)
    vector_store.persist()
    
    print("¡Proceso completado!")
    print(f"Se han guardado {len(chunks)} trozos en la base de datos en '{CHROMA_PATH}'.")

# --- Punto de Entrada del Script ---
# Esto asegura que el código dentro del if solo se ejecute cuando
# corremos el script directamente (python ingest.py).
if __name__ == "__main__":
    main()
