import csv
import random
from faker import Faker

fake = Faker()

sistemas_operativos = [
    "Ubuntu 22.04", "Ubuntu 20.04", "CentOS 7", "CentOS 8",
    "Windows Server 2019", "Windows Server 2022", "Debian 11"
]

departamentos = [
    "IT", "Finanzas", "RRHH", "Marketing", "Operaciones",
    "Desarrollo", "Seguridad", "Logística"
]

estados = ["Activo", "Mantenimiento", "Degradado"]

def generar_inventario(archivo: str = "inventory.csv", filas: int = 1000) -> None:
    with open(archivo, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["hostname", "ip", "os", "ram_gb", "departamento", "estado"])
        
        for i in range(filas):
            writer.writerow([
                f"srv-{fake.lexify('????')}-{i:04d}",
                fake.ipv4(),
                random.choice(sistemas_operativos),
                random.choice([2, 4, 8, 16, 32, 64]),
                random.choice(departamentos),
                random.choice(estados)
            ])
    
    print(f"✅ Inventario generado: {archivo} ({filas} servidores)")

if __name__ == "__main__":
    generar_inventario()