# Proyecto: Comparación de Hash y Detección de Colisiones

## Descripción

Este proyecto consiste en una aplicación web diseñada para permitir a los usuarios subir archivos y calcular diferentes tipos de hashes (MD5, SHA-1 y SHA-256) en el backend. Además, incluye un sistema de historial que registra los archivos procesados, sus hashes, fechas y usuarios asociados, con funcionalidades CRUD (Crear, Leer, Actualizar, Eliminar). La aplicación detecta colisiones teóricas al comparar hashes existentes en la base de datos y muestra alertas visuales en el frontend.

## Características Principales

- **Subida de Archivos**: Los usuarios pueden cargar archivos desde el navegador.
- **Cálculo de Hashes**: Generación de MD5, SHA-1 y SHA-256 utilizando la librería `crypto` de Node.js.
- **Detección de Colisiones**: Alerta si un hash coincide con uno previo en la base de datos.
- **Historial CRUD**: Listado, edición y eliminación de registros de hashes.
- **Autenticación**: Registro e inicio de sesión con JWT para gestionar usuarios.
- **Interfaz Amigable**: Visualización de resultados en tablas y alertas con PrimeNG.

## Tecnologías Utilizadas

- **Frontend**: Angular 20.1.5 (standalone components), PrimeNG para UI.
- **Backend**: Node.js 22.15.1 con Express, librería `crypto` para hashing.
- **Base de Datos**: MongoDB para almacenar historial y usuarios.
- **Autenticación**: JWT con `jsonwebtoken` y `bcryptjs`.
- **Otras**: Multer para subida de archivos, CORS para comunicación frontend-backend.

## Estructura del Proyecto

- `backend/`: Contiene el servidor Node.js, rutas y modelos de MongoDB.
- `frontend/`: Contiene la aplicación Angular con componentes standalone.
- `uploads/`: Carpeta temporal para archivos subidos.

## Instalación

1. Clona el repositorio: `git clone <url_del_repositorio>`.
2. Instala MongoDB y asegúrate de que el servidor esté corriendo (`mongod`).
3. En la carpeta `backend/`:
   - Instala dependencias: `npm install`.
   - Inicia el servidor: `node server.js`.
4. En la carpeta `frontend/hash-app/`:
   - Instala dependencias: `npm install`.
   - Inicia la app: `ng serve`.

## Uso

1. Accede a `http://localhost:4200`.
2. Regístrate con un usuario y contraseña.
3. Inicia sesión para acceder a las funcionalidades.
4. Sube un archivo para ver sus hashes y verificar colisiones.
5. Gestiona el historial en la sección correspondiente.

## Contribuciones

Cualquier mejora o reporte de bugs es bienvenido. Por favor, abre un issue o envía un pull request.

## Autores

- Cesar Loor - Desarrollador de esta rama
