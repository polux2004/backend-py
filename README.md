# API de ejemplo con FastAPI

## Requisitos

- Python 3.13 (versión usada para comprobar este proyecto).
- MongoDB local en `localhost:27017`, o acceso a una instancia de MongoDB Atlas.

## Instalación

Desde la carpeta del proyecto:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
openssl rand -hex 32
```

Pega el valor generado en `JWT_SECRET` dentro de `.env`. Ajusta `MONGODB_URI` y `MONGODB_DB` según tu base de datos. Si usas Atlas, crea tus propias credenciales y configura el acceso de red. El archivo `.env` es privado y Git lo ignora.

Para iniciar la API:

```bash
uvicorn main:app --reload
```

Abre `http://127.0.0.1:8000/docs` para ver las rutas. Las rutas de `/userdb` requieren MongoDB disponible. Los usuarios definidos en los routers de autenticación son ejemplos de aprendizaje; no los uses para proteger una aplicación pública.
