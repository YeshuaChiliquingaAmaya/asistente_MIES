# Asistente MIES con RAG

## Descripción

Este proyecto implementa un asistente basado en IA para el Ministerio de Inclusión Económica y Social (MIES) de Ecuador. Utiliza técnicas avanzadas de Procesamiento de Lenguaje Natural (NLP) y Recuperación Aumentada por Generación (RAG) para proporcionar respuestas precisas basadas en documentos institucionales.

## Características Principales

- **Procesamiento de Documentos**: Soporte para ingesta de archivos PDF y CSV.
- **Búsqueda Semántica**: Búsqueda de información basada en significado, no solo en palabras clave.
- **Generación de Respuestas**: Generación de respuestas contextuales utilizando modelos de lenguaje avanzados.
- **API REST**: Interfaz de programación para integración con otros sistemas.

## Tecnologías Utilizadas

- **Backend**: FastAPI (Python)
- **Base de Datos Vectorial**: ChromaDB
- **Modelos de Embedding**: Sentence Transformers (`all-MiniLM-L6-v2`)
- **Modelo de Lenguaje**: Ollama (con soporte para múltiples modelos)
- **Procesamiento de Documentos**: PyPDF, pandas

## Estructura del Proyecto

- `chroma_db/`: Almacena la base de datos vectorial de documentos procesados.
- `data/`: Directorio para almacenar los documentos fuente (PDF/CSV).
- `ingest.py`: Script para procesar documentos y crear la base de conocimiento.
- `main.py`: Servidor FastAPI con los endpoints de la API.
- `requirements.txt`: Dependencias del proyecto.

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/YeshuaChiliquingaAmaya/asistente_MIES.git
   cd asistente_MIES
   ```

2. Crea y activa un entorno virtual (recomendado):
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate  # Windows
   # o
   source .venv/bin/activate  # Linux/Mac
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Instala Ollama (si no lo tienes):
   - Descarga desde [ollama.ai](https://ollama.ai/)
   - Ejecuta `ollama pull llama3:8b` para descargar el modelo

## Uso

1. Coloca tus documentos en la carpeta `data/` (soporta PDF y CSV)

2. Procesa los documentos para crear la base de conocimiento:
   ```bash
   python ingest.py
   ```

3. Inicia el servidor de la API:
   ```bash
   python main.py
   ```

4. La API estará disponible en `http://localhost:8000`

## Uso de la API

### Realizar una consulta

```http
POST /query
Content-Type: application/json

{
    "query_text": "¿Cuáles son los beneficios del bono de desarrollo humano?"
}
```

### Parámetros de inicio

Puedes especificar el modelo de lenguaje al iniciar el servidor:

```bash
python main.py --model llama3:8b
```

## Configuración

- `CHROMA_PATH`: Directorio de la base de datos vectorial (por defecto: "chroma_db")
- `EMBEDDING_MODEL`: Modelo de embeddings a utilizar (por defecto: "all-MiniLM-L6-v2")

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir los cambios propuestos antes de hacer un pull request.

## Autores

- Cesar Loor - Desarrollador de esta rama
