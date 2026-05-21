import requests
from log_parser import analizar_logs

def obtener_info_ip(ip: str) -> dict:
    try:
        respuesta = requests.get(f"https://ipinfo.io/{ip}/json", timeout=5)
        datos = respuesta.json()
        return {
            "ip": ip,
            "pais": datos.get("country", "Desconocido"),
            "org": datos.get("org", "Desconocido")
        }
    except Exception:
        return {"ip": ip, "pais": "Error", "org": "Error"}

def mostrar_tabla_amenazas() -> None:
    ips_fallidas = analizar_logs()
    
    print("\n{'='*65}")
    print(f"{'IP':<20} {'Intentos':<10} {'País':<10} {'Organización'}")
    print(f"{'='*65}")
    
    for ip, intentos in sorted(ips_fallidas.items(), key=lambda x: x[1], reverse=True):
        info = obtener_info_ip(ip)
        print(f"{ip:<20} {intentos:<10} {info['pais']:<10} {info['org']}")
    
    print(f"{'='*65}")