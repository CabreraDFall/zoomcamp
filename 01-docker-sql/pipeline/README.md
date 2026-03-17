# Zoomcamp 01-Docker Data Pipeline

Este proyecto contiene un pipeline de datos en Python dockerizado y una base de datos PostgreSQL.

## Guía de Inicio Rápido

Para volver a estar en el punto actual rápidamente, sigue estos pasos:

### 1. Preparar la terminal (PowerShell)
Asegúrate de estar en la carpeta raíz del proyecto (`01-docker-sql`):
```powershell
cd 01-docker-sql
```

### 2. Iniciar la Base de Datos (Terminal 1)
Ejecuta el siguiente comando para arrancar Postgres con persistencia de datos:
```powershell
docker run -it --rm `
  --name pg-database `
  --network pg-network `
  -e POSTGRES_USER="root" `
  -e POSTGRES_PASSWORD="root" `
  -e POSTGRES_DB="ny_taxi" `
  -p 5432:5432 `
  -v "${PWD}/ny_taxi_postgres_data:/var/lib/postgresql/data" `
  postgres:13
```

### 3. Iniciar el Pipeline de Python (Terminal 2)
En una nueva terminal, levanta el contenedor de desarrollo del pipeline:
```powershell
docker run -it --rm `
  --network pg-network `
  -v "${PWD}/pipeline:/app" `
  --entrypoint bash `
  test:pandas
```

### 4. Probar la conexión (Dentro del contenedor)
Desde la terminal del contenedor de Python, verifica la conexión a la base de datos:
```bash
uv run pgcli -h pg-database -p 5432 -U root -d ny_taxi
```
*(Contraseña: `root`)*

## Notas Importantes
- **Red de Docker**: `pg-network` debe haber sido creada previamente (`docker network create pg-network`). Docker recordará esta configuración.
- **Persistencia**: Los datos de Postgres se guardan en el volumen montado `${PWD}/ny_taxi_postgres_data`.
- **Pipeline**: El código reside en la carpeta `/pipeline` y se monta en `/app` dentro del contenedor.
