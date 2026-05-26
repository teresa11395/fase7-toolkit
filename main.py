from fastapi import FastAPI
from fastapi.responses import JSONResponse
import os
import redis

app = FastAPI(
    title="Toolkit de Administración de Sistemas",
    description="API REST para el toolkit de Python - Fase 7/8 Bootcamp",
    version="1.0.0"
)


# ─────────────────────────────────────────
# CONEXIÓN A REDIS
# ─────────────────────────────────────────
def get_redis():
    return redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        password=os.getenv("REDIS_PASSWORD", None),
        decode_responses=True
    )


# ─────────────────────────────────────────
# ENDPOINT 1: Estado de la API
# ─────────────────────────────────────────
@app.get("/status", tags=["General"])
def get_status():
    """
    Devuelve el estado actual de la API.
    """
    return {
        "status": "ok",
        "message": "Toolkit API funcionando correctamente",
        "version": "1.0.0"
    }


# ─────────────────────────────────────────
# ENDPOINT 2: Inventario de servidores
# ─────────────────────────────────────────
@app.get("/inventory", tags=["Inventario"])
def get_inventory():
    """
    Devuelve los primeros 10 servidores del inventario.
    """
    try:
        import pandas as pd
        csv_path = os.path.join(os.path.dirname(__file__), "inventory.csv")
        if not os.path.exists(csv_path):
            return JSONResponse(
                status_code=404,
                content={"error": "Archivo inventory.csv no encontrado"}
            )
        df = pd.read_csv(csv_path)
        servidores = df.head(10).to_dict(orient="records")
        return {
            "total": len(df),
            "mostrando": 10,
            "servidores": servidores
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


# ─────────────────────────────────────────
# ENDPOINT 3: Análisis de logs
# ─────────────────────────────────────────
@app.get("/logs/suspicious", tags=["Logs"])
def get_suspicious_ips():
    """
    Devuelve las IPs sospechosas detectadas en auth.log.
    """
    try:
        from log_parser import parse_failed_attempts
        log_path = os.path.join(os.path.dirname(__file__), "auth.log")
        if not os.path.exists(log_path):
            return JSONResponse(
                status_code=404,
                content={"error": "Archivo auth.log no encontrado"}
            )
        ips = parse_failed_attempts(log_path)
        return {
            "total_ips_sospechosas": len(ips),
            "ips": ips
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


# ─────────────────────────────────────────
# ENDPOINT 4: Guardar entrada en archivo
# ─────────────────────────────────────────
@app.post("/entries", tags=["Persistencia"])
def add_entry(mensaje: str):
    """
    Guarda un mensaje en un archivo dentro del contenedor.
    """
    import datetime
    entry = f"{datetime.datetime.now()} - {mensaje}\n"
    with open("/data/entries.txt", "a") as f:
        f.write(entry)
    return {"guardado": mensaje}


@app.get("/entries", tags=["Persistencia"])
def get_entries():
    """
    Lee las entradas guardadas en el archivo.
    """
    try:
        with open("/data/entries.txt", "r") as f:
            contenido = f.readlines()
        return {"entradas": contenido}
    except FileNotFoundError:
        return {"entradas": []}


# ─────────────────────────────────────────
# ENDPOINT 5: Caché de logs con Redis
# ─────────────────────────────────────────
@app.get("/cache/logs", tags=["Redis"])
def get_cached_logs():
    """
    Devuelve IPs sospechosas usando Redis como caché.
    """
    try:
        r = get_redis()
        cached = r.get("suspicious_ips")
        if cached:
            return {"source": "cache", "data": cached}
        from log_parser import parse_failed_attempts
        log_path = os.path.join(os.path.dirname(__file__), "auth.log")
        ips = parse_failed_attempts(log_path)
        r.setex("suspicious_ips", 300, str(ips))
        return {"source": "fresh", "data": str(ips)}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# ─────────────────────────────────────────
# ENDPOINT 6: Reportar IP sospechosa
# ─────────────────────────────────────────
@app.post("/suspicious-ips", tags=["Redis"])
def report_suspicious_ip(ip: str):
    """
    Añade una IP al conjunto de IPs sospechosas en Redis.
    """
    try:
        r = get_redis()
        r.sadd("suspicious_set", ip)
        return {"mensaje": f"IP {ip} añadida", "total": r.scard("suspicious_set")}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# ─────────────────────────────────────────
# ENDPOINT 7: Listar IPs sospechosas
# ─────────────────────────────────────────
@app.get("/suspicious-ips", tags=["Redis"])
def list_suspicious_ips():
    """
    Lista todas las IPs sospechosas guardadas en Redis.
    """
    try:
        r = get_redis()
        ips = list(r.smembers("suspicious_set"))
        return {"total": len(ips), "ips": ips}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})