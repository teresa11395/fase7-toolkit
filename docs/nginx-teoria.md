# NGINX: Fundamentos Teóricos

## 1. ¿Qué es un proxy inverso?

### Proxy directo
Un proxy directo actúa en nombre del cliente — el cliente le pide
al proxy que acceda a internet por él. Se usa para anonimizar
tráfico o filtrar contenido en redes corporativas.

Cliente → Proxy directo → Internet

### Proxy inverso
Un proxy inverso actúa en nombre del servidor — recibe las
peticiones de los clientes y las redirige al servidor correcto.
El cliente nunca sabe qué hay detrás.

Internet → NGINX (proxy inverso) → Backend (Python)
→ Redis (interno)
→ Archivos estáticos
---

## 2. ¿Por qué NGINX se coloca delante de la aplicación?

### Gestión SSL/HTTPS
NGINX gestiona los certificados SSL y el cifrado. El backend
recibe tráfico HTTP limpio sin necesidad de implementar SSL.

### Rate Limiting
NGINX puede limitar el número de peticiones por IP — protege
la API de ataques de fuerza bruta o DDoS.

### Caché
NGINX puede cachear respuestas del backend — si 1000 usuarios
piden lo mismo, NGINX responde directamente sin tocar el backend.

### Balanceo de carga
Si hay varios contenedores del backend, NGINX reparte las
peticiones entre ellos automáticamente.

### Servir archivos estáticos
NGINX sirve imágenes, CSS y JavaScript directamente sin
molestar al backend de Python.

---

## 3. Upstream y Server Block en NGINX

### Upstream
Define un grupo de servidores backend a los que NGINX
puede redirigir tráfico.

```nginx
upstream backend {
    server backend:8000;
}
```

### Server Block
Define cómo NGINX escucha y responde a las peticiones.

```nginx
server {
    listen 80;

    location / {
        proxy_pass http://backend;
    }
}
```

---

## 4. NGINX vs Apache bajo grandes cargas

### Apache
Crea un proceso o hilo nuevo por cada conexión. Con miles
de conexiones simultáneas consume mucha RAM y CPU.

### NGINX
Usa un modelo asíncrono y no bloqueante — un solo proceso
puede gestionar miles de conexiones simultáneas con muy
poco consumo de recursos.

**Resultado:** NGINX puede manejar 10x más tráfico que Apache
con el mismo hardware. Por eso es el servidor web más usado
en el mundo para aplicaciones de alto tráfico.