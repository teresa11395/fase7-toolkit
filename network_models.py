class NetworkDevice:
    def __init__(self, hostname: str, ip: str, mac: str) -> None:
        self.hostname = hostname
        self.ip = ip
        self.mac = mac

    def audit_device(self) -> None:
        print(f"\n🔍 Auditando {self.hostname} ({self.ip})")

class Router(NetworkDevice):
    def __init__(self, hostname: str, ip: str, mac: str, modelo: str) -> None:
        super().__init__(hostname, ip, mac)
        self.modelo = modelo

    def audit_device(self) -> None:
        print(f"\n🌐 Router: {self.hostname} ({self.ip})")
        print("   ✅ Verificar contraseña de administrador")
        print("   ✅ Actualizar firmware")
        print("   ✅ Revisar reglas de firewall")

class Server(NetworkDevice):
    def __init__(self, hostname: str, ip: str, mac: str, os: str) -> None:
        super().__init__(hostname, ip, mac)
        self.os = os

    def audit_device(self) -> None:
        print(f"\n🖥️  Servidor: {self.hostname} ({self.ip})")
        print("   ✅ Verificar actualizaciones del sistema")
        print("   ✅ Revisar logs de acceso")
        print("   ✅ Comprobar puertos abiertos")