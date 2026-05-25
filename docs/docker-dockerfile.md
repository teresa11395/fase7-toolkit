# Docker: Imágenes por Capas y el Dockerfile

## 1. Sistema de Capas de Docker

### ¿Cómo funciona?
Cada instrucción del Dockerfile genera una capa inmutable que se apila
sobre la anterior. Docker usa un sistema de archivos por capas llamado
OverlayFS.

```
┌─────────────────────────┐
│   CAPA 4: Tu código     │  ← COPY . .
├─────────────────────────┤
│   CAPA 3: Librerías     │  ← RUN pip install
├─────────────────────────┤
│   CAPA 2: Directorio    │  ← WORKDIR /app
├─────────────────────────┤
│   CAPA 1: Python base   │  ← FROM python:3.11-alpine
└─────────────────────────┘
```

### ¿Por qué el orden de las instrucciones afecta el rendimiento?
Docker guarda en caché cada capa. Si una capa no ha cambiado, Docker
la reutiliza sin reconstruirla. Pero si una capa cambia, Docker
reconstruye esa capa y TODAS las que vienen después.

**Ejemplo malo — código antes que librerías:**
```dockerfile
COPY . .                          # Si cambias el código...
RUN pip install -r requirements.txt  # ...esto se reconstruye siempre
```

**Ejemplo bueno — librerías antes que código:**
```dockerfile
COPY requirements.txt .           # Solo cambia si añades librerías
RUN pip install -r requirements.txt  # Se cachea y no se repite
COPY . .                          # Solo esto se reconstruye al cambiar código
```

La regla es: coloca las instrucciones que cambian menos frecuentemente
primero, y las que cambian más frecuentemente al final.

---

## 2. Instrucciones del Dockerfile

### FROM
Define la imagen base sobre la que construimos.
```dockerfile
FROM python:3.11-alpine
```
Es siempre la primera instrucción. Todo lo que hagamos parte de esta imagen.

### WORKDIR
Define el directorio de trabajo dentro del contenedor.
```dockerfile
WORKDIR /app
```
Todos los comandos siguientes se ejecutarán desde esta carpeta.
Si no existe, Docker la crea automáticamente.

### COPY
Copia archivos desde tu ordenador al contenedor.
```dockerfile
COPY requirements.txt .
COPY . .
```
El primer punto es el origen (tu ordenador) y el segundo es el destino
(dentro del contenedor, en el WORKDIR).

### ADD
Similar a COPY pero con funciones extra: puede descomprimir archivos
.tar y descargar URLs. Se recomienda usar COPY salvo que necesites
estas funciones extra.
```dockerfile
ADD archivo.tar.gz /app/
```

### RUN
Ejecuta un comando durante la construcción de la imagen.
```dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```
Cada RUN crea una nueva capa. Para minimizar capas se pueden encadenar
comandos con &&.

### ENV
Define variables de entorno disponibles en el contenedor.
```dockerfile
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
```

### EXPOSE
Documenta el puerto que usa el contenedor. No abre el puerto
automáticamente — solo es informativo.
```dockerfile
EXPOSE 8000
```

### CMD
Define el comando por defecto al arrancar el contenedor.
```dockerfile
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```
Solo puede haber un CMD. Si se especifica un comando al hacer
docker run, este CMD se ignora.

### ENTRYPOINT
Define el ejecutable principal del contenedor.
```dockerfile
ENTRYPOINT ["python"]
CMD ["app.py"]
```
A diferencia de CMD, ENTRYPOINT no se puede sobreescribir fácilmente
desde docker run.

### ARG
Define variables disponibles solo durante la construcción de la imagen,
no en el contenedor en ejecución.
```dockerfile
ARG VERSION=1.0
```

---

## 3. Diferencia entre CMD y ENTRYPOINT

| | CMD | ENTRYPOINT |
|---|---|---|
| Se puede sobreescribir con docker run | Sí | No fácilmente |
| Uso principal | Comando por defecto | Ejecutable fijo |
| Combinados | CMD actúa como argumentos de ENTRYPOINT | ENTRYPOINT es el ejecutable |

**Ejemplo combinado:**
```dockerfile
ENTRYPOINT ["python"]
CMD ["app.py"]
```
Ejecuta `python app.py` pero puedes hacer `docker run imagen otro.py`
para cambiar el script sin cambiar el ejecutable.

---

## 4. Imagen Base Alpine

### ¿Qué es Alpine?
Alpine Linux es una distribución de Linux extremadamente ligera —
solo ocupa unos 5MB. Está diseñada para ser mínima y segura.

### ¿Por qué se prefiere frente a Ubuntu o Debian?

| Imagen base | Tamaño aproximado |
|-------------|------------------|
| python:3.11 (Debian) | ~900MB |
| python:3.11-slim | ~130MB |
| python:3.11-alpine | ~50MB |

**Ventajas de Alpine:**
- Mucho más pequeña — builds más rápidos y menos espacio en disco
- Menor superficie de ataque — menos software instalado significa
  menos vulnerabilidades de seguridad
- Más rápida de descargar y desplegar

**Desventajas de Alpine:**
- Usa musl libc en vez de glibc — algunas librerías de Python
  no son compatibles directamente y requieren compilación
- Puede requerir instalar dependencias adicionales manualmente
