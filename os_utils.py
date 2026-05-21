import subprocess
import shutil
import os

def check_ping(ip: str) -> bool:
    resultado = subprocess.run(
        ["ping", "-n", "1", ip],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return resultado.returncode == 0

def check_disk_space(particion: str = "C:\\") -> None:
    total, usado, libre = shutil.disk_usage(particion)
    porcentaje_libre = (libre / total) * 100
    
    print(f"\n📁 Disco: {particion}")
    print(f"   Total: {total // (2**30)} GB")
    print(f"   Usado: {usado // (2**30)} GB")
    print(f"   Libre: {libre // (2**30)} GB ({porcentaje_libre:.1f}%)")
    
    if porcentaje_libre < 20:
        print("   ⚠️  ALERTA: Espacio libre menor al 20%")
    else:
        print("   ✅ Espacio en disco correcto")