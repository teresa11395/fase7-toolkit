# Docker: Redes

## 1. Tipos de red nativos de Docker

### Bridge (puente)
Es la red por defecto cuando creas un contenedor sin especificar red.
Docker crea una red virtual privada y los contenedores conectados a
ella pueden comunicarse entre sí por nombre.

**¿Cuándo usarla?**
Es la opción más común para desarrollo local. En esta tarea usaremos
una red bridge personalizada para conectar el backend, Redis y NGINX.
Host (mi ordenador)
└── Red bridge
├── contenedor-backend (172.17.0.2)
├── contenedor-redis   (172.17.0.3)
└── contenedor-nginx   (172.17.0.4)
### Host
El contenedor comparte directamente la red del host — no tiene su
propia IP, usa la misma que tu ordenador.

**¿Cuándo usarla?**
Cuando necesitas máximo rendimiento de red y no te importa el
aislamiento. Poco común en producción por razones de seguridad.

### None
El contenedor no tiene ninguna interfaz de red — completamente
aislado de cualquier comunicación de red.

**¿Cuándo usarla?**
Para tareas de procesamiento que no necesitan red, como scripts
de análisis de datos o trabajos batch.

---

## 2. Service Discovery en Docker Compose

Cuando usas Docker Compose, cada servicio puede encontrar a los
demás usando su nombre como hostname — sin necesidad de IPs.

**Ejemplo:**
Si tienes un servicio llamado `redis` en el Compose, tu aplicación
Python puede conectarse así:

```python
redis_client = Redis(host="redis", port=6379)
```

Docker resuelve automáticamente el nombre `redis` a la IP interna
del contenedor. Esto funciona porque Docker Compose crea una red
interna compartida y un DNS interno que resuelve los nombres de
los servicios.

**Ventaja:** Si el contenedor de Redis cambia de IP (por un reinicio),
no necesitas cambiar nada en tu código — el nombre siempre funciona.

---

## 3. Puerto publicado vs puerto expuesto internamente

### Puerto publicado (-p 8080:80)
El puerto es accesible desde fuera del contenedor — desde tu
ordenador o desde internet.