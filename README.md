# Asistente de Trámites del Gobierno de Ecuador

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

Un asistente conversacional inteligente que ayuda a los ciudadanos a encontrar información sobre trámites gubernamentales en Ecuador, utilizando técnicas modernas de procesamiento de lenguaje natural y búsqueda semántica.

## Características

- Búsqueda semántica de trámites gubernamentales
- Extracción automática de datos del portal gob.ec
- Interfaz de chat intuitiva
- Respuestas precisas basadas en información oficial
- Arquitectura escalable y modular

## Arquitectura

El proyecto sigue una arquitectura de tres capas principales:

1. **Capa de Extracción de Datos**
   - Web Scraping del portal gob.ec
   - Procesamiento y limpieza de datos
   - Almacenamiento estructurado en JSON

2. **Capa de Procesamiento**
   - Vectorización de documentos con Sentence Transformers
   - Almacenamiento en base de datos vectorial (ChromaDB)
   - Búsqueda semántica

3. **Capa de Servicio**
   - API REST con FastAPI
   - Integración con modelo de lenguaje (Groq)
   - Generación de respuestas naturales

## Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Clave de API de Groq
- Conexión a internet para la descarga de modelos

## Instalación

1. Clona el repositorio:
   ```bash
   git clone [URL_DEL_REPOSITORIO]
   cd asistente_tramites_EC
   ```

2. Crea y activa un entorno virtual (recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Crea un archivo `.env` en la raíz del proyecto con tu clave de Groq:
   ```
   GROQ_API_KEY=tu_clave_aquí
   ```

## Uso

### 1. Extracción de Datos (Opcional)

Para actualizar la base de datos de trámites:

```bash
python scraper_robusto.py  # Versión principal del scraper
# o
python scraper_lista.py    # Versión alternativa
```

### 2. Procesamiento e Indexación

Procesa los datos y crea la base de datos vectorial:

```bash
python ingest_chroma.py    # Versión estándar
# o
python ingest_dinamico.py  # Versión con procesamiento dinámico
```

### 3. Iniciar el Servidor

Inicia el servidor de la API:

```bash
uvicorn main:app --reload --port 8000
```

### 4. Acceder a la Aplicación

Abre tu navegador y visita:
```
http://127.0.0.1:8000
```

O utiliza la API directamente:
```bash
curl -X POST "http://127.0.0.1:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"question": "¿Cómo obtengo mi pasaporte?"}'
```

## Estructura del Proyecto

```
asistente_tramites_EC/
├── .gitignore
├── README.md
├── requirements.txt
├── .env.example
├── main.py                 # Servidor FastAPI principal
├── scraper_robusto.py      # Script principal de web scraping
├── scraper_lista.py        # Versión alternativa de scraping
├── scraper_duplicado_cedula.py  # Utilidad para manejo de cédulas
├── ingest_chroma.py        # Script de ingesta a ChromaDB
├── ingest_dinamico.py      # Versión dinámica de ingesta
├── list_search.py          # Utilidades de búsqueda
├── tramites_chroma_db/     # Base de datos vectorial
├── tramites_extraidos_*.json  # Datos extraídos
└── urls_encontradas.json   # URLs recolectadas
```

## Tecnologías Utilizadas

- **Lenguaje**: Python 3.8+
- **Web Scraping**: BeautifulSoup4, Requests
- **Procesamiento de Lenguaje**: LangChain, Sentence Transformers
- **Base de Datos Vectorial**: ChromaDB
- **API Web**: FastAPI, Uvicorn
- **Modelo de Lenguaje**: Groq (LLM)

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, lee nuestras pautas de contribución antes de enviar un pull request.

## Contacto

¿Preguntas o sugerencias? ¡No dudes en abrir un issue!