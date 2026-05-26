# 🛠️ Toolkit de Administración de Sistemas

API REST para administradores de sistemas con Docker, Redis y NGINX.

## 📋 Descripción

Este proyecto dockeriza el toolkit de Python de la Fase 7, exponiendo
sus funcionalidades a través de una API REST construida con FastAPI.
La infraestructura incluye tres servicios orquestados con Docker Compose:
un backend Python, una base de datos Redis y un proxy inverso NGINX.

## 🏗️ Arquitectura
Internet → NGINX (puerto 80) → Backend FastAPI (puerto 8000) → Redis (puerto 6379)

## 🚀 Arranque rápido

### Requisitos
- Docker Engine
- Docker Compose v2

### Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/teresa11395/fase7-toolkit.git
cd fase7-toolkit
```

2. Crea el archivo de variables de entorno:
```bash
cp .env.example .env
```

3. Edita `.env` con tus valores:
REDIS_PASSWORD=tu_contraseña_segura

4. Arranca la infraestructura:
```bash
docker compose up --build
```

5. Accede a la API en: http://localhost/docs

## 📡 Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | /status | Estado de la API |
| GET | /inventory | Inventario de servidores |
| GET | /logs/suspicious | IPs sospechosas en auth.log |
| POST | /entries | Guardar entrada persistente |
| GET | /entries | Leer entradas guardadas |
| GET | /cache/logs | Logs con caché Redis |
| POST | /suspicious-ips | Reportar IP sospechosa |
| GET | /suspicious-ips | Listar IPs sospechosas |

## 🗂️ Estructura del proyecto
fase7-toolkit/
├── docs/                    # Documentación técnica
│   ├── docker-teoria.md
│   ├── docker-dockerfile.md
│   ├── docker-redes.md
│   ├── docker-volumenes.md
│   └── nginx-teoria.md
├── main.py                  # API FastAPI
├── Dockerfile               # Imagen del backend
├── docker-compose.yml       # Orquestación de servicios
├── nginx.conf               # Configuración del proxy
├── .env.example             # Plantilla de variables
├── .dockerignore            # Archivos excluidos del build
└── requirements.txt         # Dependencias Python

## 🔧 Servicios

### Backend (Python + FastAPI)
- Imagen base: `python:3.11-alpine`
- Puerto interno: 8000
- Healthcheck: GET /status cada 30s

### Redis
- Imagen: `redis:7-alpine`
- Puerto interno: 6379
- Autenticación por contraseña
- Datos persistentes en volumen

### NGINX
- Imagen: `nginx:alpine`
- Puerto externo: 80
- Rate limiting: 10 req/s por IP
- Proxy inverso hacia el backend

## 📚 Documentación técnica

Toda la documentación teórica está en la carpeta `docs/`:
- **docker-teoria.md** — Conceptos fundamentales de Docker
- **docker-dockerfile.md** — Imágenes por capas y Dockerfile
- **docker-redes.md** — Redes en Docker
- **docker-volumenes.md** — Persistencia de datos
- **nginx-teoria.md** — NGINX y proxy inverso

## ⚙️ Comandos útiles

```bash
# Arrancar en segundo plano
docker compose up -d --build

# Ver logs
docker compose logs -f

# Parar todo
docker compose down

# Ver recursos en uso
docker stats
```