def analizar_logs(archivo: str = "auth.log") -> dict:
    ips_fallidas: dict = {}
    ips_unicas: set = set()

    try:
        with open(archivo, "r") as f:
            for linea in f:
                if "Failed password" in linea:
                    partes = linea.split()
                    ip = partes[-4]
                    if not ip[0].isdigit():
                        continue
                    ips_unicas.add(ip)
                    if ip in ips_fallidas:
                        ips_fallidas[ip] += 1
                    else:
                        ips_fallidas[ip] = 1
    except FileNotFoundError:
        print(f"❌ No se encontró el archivo {archivo}")
        return {}

    print("\n🔍 IPs atacantes detectadas:")
    for ip, intentos in sorted(ips_fallidas.items(), key=lambda x: x[1], reverse=True):
        print(f"   {ip:<20} → {intentos} intentos")

    print(f"\n📊 Total IPs únicas atacantes: {len(ips_unicas)}")
    return ips_fallidas