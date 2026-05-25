# Docker: Volúmenes y Persistencia de Datos

## ¿Por qué necesitamos volúmenes?
Los contenedores son efímeros — cuando se eliminan, todos los datos
que contenían desaparecen. Los volúmenes son la solución: almacenan
datos fuera del contenedor para que persistan aunque el contenedor
se elimine y recree.

## Experimento realizado

### Sin volumen
1. Se guarda un mensaje dentro del contenedor
2. Se elimina el contenedor
3. Se recrea el contenedor
4. El mensaje ha desaparecido

### Con volumen nombrado
1. Se arranca el contenedor montando el volumen toolkit-data en /data
2. Se guarda el mensaje "hola desde docker"
3. Se elimina el contenedor
4. Se recrea el contenedor con el mismo volumen
5. El mensaje sigue ahí — el volumen sobrevivió

### Comando usado
docker run -d --name toolkit -p 8000:8000 -v toolkit-data:/data toolkit-api
## Gestión de volúmenes

### Ver todos los volúmenes
docker volume ls
### Inspeccionar un volumen
docker volume inspect toolkit-data
### Eliminar un volumen
docker volume rm toolkit-data
## Volumen nombrado vs Bind Mount

### Volumen nombrado
Docker gestiona dónde se guardan los datos.
-v toolkit-data:/data
**Cuándo usarlo:** bases de datos, archivos generados por la app,
cualquier dato que necesite persistir en producción.

### Bind Mount
Montas una carpeta específica de tu ordenador.
-v /home/tborr/datos:/data
**Cuándo usarlo:** desarrollo local, cuando quieres editar archivos
desde tu ordenador y que los cambios se reflejen inmediatamente
en el contenedor.