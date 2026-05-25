
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json
import os
 
app = FastAPI(
    title="Toolkit de Administración de Sistemas",
    description="API REST para el toolkit de Python - Fase 7/8 Bootcamp",
    version="1.0.0"
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
        )# ─────────────────────────────────────────
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
 