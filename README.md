# Sistema de Gestión y Análisis de Objetos Perdidos en el Campus

Aplicación web para reportar, buscar y entregar objetos perdidos o encontrados en el campus de UNIMINUTO. Proyecto del curso *Arquitecturas de datos masivos y bases de datos distribuidas*.

**Equipo:** Danna Valentina Vera Pinzón, Samuel Esteban Bello Bejarano, Santiago Ahrat Nonsoque Pinilla y Juan Diego Cárdenas Torres.
**Docente:** Alonso Guevara Perez.

## ¿Qué hace?

- La comunidad reporta un objeto encontrado o perdido con sus datos y una foto opcional.
- El administrador ve los reportes en un panel y registra la entrega (se puede editar o deshacer).
- Funciona desde el celular o el computador con un navegador.

## Arquitectura de datos

| Almacén | Qué guarda |
|---|---|
| Datalake (carpeta `datalake_local/fotos`) | Fotos (JPEG, PNG o WEBP, máximo 5 MB) con nombre aleatorio |
| MongoDB Atlas | Reportes (con el reclamo como subdocumento) |
| MariaDB | Usuarios, sedes y administradores |

Solo MongoDB Atlas es distribuido (conjunto de réplicas). Las referencias entre almacenes (por ejemplo `usuario_id`) las mantiene la aplicación; no hay transacciones entre almacenes.

## Tecnologías

Python, FastAPI, Uvicorn, Jinja2, Bootstrap 5, PyMySQL, PyMongo, argon2-cffi, MariaDB 11, MongoDB Atlas, Docker Compose.

## Requisitos

- Docker y Docker Compose.
- Una cuenta de MongoDB Atlas (el plan gratuito sirve) con un cluster propio.
- Opcional: ngrok, para abrir la aplicación desde otros dispositivos.

## Puesta en marcha

1. Clona el repositorio y entra a la carpeta.

   ```bash
   git clone https://github.com/JuanCardenas2024/objetos-campus.git
   cd objetos-campus
   ```

2. Crea tu archivo de variables a partir del ejemplo.

   ```bash
   cp .env.example .env        # en Windows (PowerShell): copy .env.example .env
   ```

3. Edita `.env` con tus datos:

   - `MARIADB_USER` y `MARIADB_PASSWORD`: los que quieras para la base.
   - `MONGO_URI`: la cadena de conexión de tu cluster de Atlas.
   - `SECRET_KEY`: una cadena larga y aleatoria.

   No subas nunca `.env` a Git (ya está en `.gitignore`).

4. En Atlas, autoriza tu dirección IP (Network Access) para que la aplicación pueda conectarse.

5. Levanta los servicios.

   ```bash
   docker compose up --build
   ```

   MariaDB crea sus tablas sola a partir de `app/db/schema.sql` la primera vez.

6. En otra terminal, carga las sedes y crea el administrador.

   ```bash
   docker compose exec app python -m scripts.cargar_sedes
   docker compose exec app python -m scripts.crear_admin
   ```

7. Abre `http://localhost:8000` y revisa `http://localhost:8000/health`, que informa el estado de las tres fuentes.

## Cambiar la contraseña de MariaDB

MariaDB solo lee `MARIADB_USER` y `MARIADB_PASSWORD` al crear el volumen por primera vez. Si cambias la contraseña después, actualízala con `ALTER USER` dentro de la base, o recrea el volumen con `docker compose down -v` (esto borra usuarios, sedes y administradores).

## Publicar desde otros dispositivos (opcional)

```bash
ngrok http 8000
```

Usa el plan gratuito solo para pruebas. No subas el token de ngrok a Git.

## Estado del proyecto

Es un despliegue de piloto: la aplicación corre en el equipo del usuario y depende de que ese equipo esté encendido.

**Pruebas verificadas:** `/health` con las tres fuentes, reporte con foto en datalake y Atlas, extravío visible en el panel, acceso desde celular y otro computador, e ingreso del administrador desde otro equipo.

**Pendientes:** prueba de tamaño de archivo (P-07), entrega con deshacer (P-08), comprobar que un archivo rechazado no deja rastro (P-06), y proteger los formularios con inicio de sesión (RF-07).

## Seguridad y trabajo futuro

- Formularios de reporte sin inicio de sesión.
- El tipo de imagen se valida por el encabezado que declara el navegador, no por su contenido.
- Falta el aviso de privacidad (Ley 1581 de 2012), protección contra CSRF y límite de uso.
- El contenedor corre como root.
- Para producción: servidor institucional y fotos en un almacenamiento de objetos.

## Licencia

[Completar según indique el docente o la universidad.]
