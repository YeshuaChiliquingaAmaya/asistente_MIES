# Script de Ingesta Eficiente por Lotes

import os
import pandas as pd
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document
import time
import shutil

# --- 1. Definición de Rutas y Constantes ---
CHROMA_PATH = "chroma_db"
DATA_PATH = "data"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

def process_file(file_path, filename):
    """
    Procesa un único archivo (PDF o CSV) y devuelve una lista de documentos de LangChain.
    """
    # --- Procesamiento para archivos PDF ---
    if filename.endswith('.pdf'):
        print(f"Cargando {filename} como PDF...")
        loader = PyPDFLoader(file_path)
        return loader.load()

    # --- Procesamiento para archivos CSV ---
    elif filename.endswith('.csv'):
        print(f"Procesando {filename} como CSV...")
        try:
            # INTENTO 1: Leer con punto y coma como separador
            df = pd.read_csv(file_path, encoding='latin-1', sep=';', low_memory=False)
            print(f"Leído exitosamente con separador ';'")
        except Exception:
            try:
                # INTENTO 2: Leer con coma como separador
                df = pd.read_csv(file_path, encoding='latin-1', sep=',', low_memory=False)
                print(f"Leído exitosamente con separador ','")
            except Exception as e:
                print(f"Error definitivo al procesar el archivo {filename}: {e}")
                return [] # Devuelve lista vacía si falla

        # Formatear cada fila como un documento
        file_documents = []
        for index, row in df.iterrows():
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
            doc = Document(
                page_content=content.strip(),
                metadata={"source": filename, "row": index}
            )
            file_documents.append(doc)
        print(f"Cargadas {len(df)} filas de {filename}.")
        return file_documents
    
    return [] # Devuelve lista vacía si no es PDF o CSV

def split_documents(documents):
    """Divide los documentos en trozos."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Documento dividido en {len(chunks)} trozos.")
    return chunks

def main():
    """Función principal que orquesta el proceso por lotes."""
    start_time = time.time()
    print("Iniciando la ingesta de datos EFICIENTE en Colab...")

    # Si la base de datos ya existe, la borramos para empezar de cero.
    if os.path.exists(CHROMA_PATH):
        print("Borrando base de datos antigua...")
        shutil.rmtree(CHROMA_PATH)

    # Inicializamos el modelo de embeddings una sola vez.
    embeddings = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL)
    
    # Inicializamos una base de datos ChromaDB vacía.
    # Usamos un documento falso para la creación inicial.
    dummy_doc = Document(page_content="start")
    vector_store = Chroma.from_documents(
        [dummy_doc], 
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )

    total_chunks = 0
    # Iteramos sobre cada archivo en la carpeta de datos.
    for filename in os.listdir(DATA_PATH):
        file_path = os.path.join(DATA_PATH, filename)
        
        # 1. Cargar documentos de UN SOLO archivo.
        documents = process_file(file_path, filename)
        if not documents:
            continue # Pasa al siguiente archivo si no se pudo procesar

        # 2. Dividir los documentos de ESE archivo en trozos.
        chunks = split_documents(documents)
        
        # 3. Añadir los trozos a la base de datos existente.
        if chunks:
            print(f"Añadiendo {len(chunks)} trozos a ChromaDB...")
            vector_store.add_documents(chunks, embedding=embeddings)
            total_chunks += len(chunks)
        
        print("-" * 40)

    # Persistir todos los cambios al final.
    vector_store.persist()
    
    end_time = time.time()
    print("¡PROCESO EFICIENTE COMPLETADO!")
    print(f"Se han guardado un total de {total_chunks} trozos en la base de datos en '{CHROMA_PATH}'.")
    print(f"Tiempo total de ejecución: {((end_time - start_time) / 60):.2f} minutos.")

# --- Ejecutar el proceso ---
main()