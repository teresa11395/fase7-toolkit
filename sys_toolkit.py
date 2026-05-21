from os_utils import check_ping, check_disk_space
from log_parser import analizar_logs
from network_models import Router, Server
from threat_intel import mostrar_tabla_amenazas
from inventory_manager import analizar_inventario
from report_generator import generar_informe_excel

def mostrar_menu() -> None:
    print("\n=== Kit de Herramientas para Administradores de Sistemas ===")
    print("1. Comprobar ping a una IP")
    print("2. Comprobar espacio en disco")
    print("3. Analizar logs de SSH")
    print("4. Consultar IP sospechosa")
    print("5. Generar inventario de red")
    print("6. Generar informe Excel")
    print("7. Salir")

def main() -> None:
    while True:
        mostrar_menu()
        opcion: str = input("\nElige una opción (1-7): ")
        
        if opcion == "1":
            ip: str = input("Introduce una IP: ")
            if check_ping(ip):
                print(f"✅ {ip} responde correctamente")
            else:
                print(f"❌ {ip} no responde")
        elif opcion == "2":
            check_disk_space("C:\\")
        elif opcion == "3":
            analizar_logs()
        elif opcion == "4":
            mostrar_tabla_amenazas()
        e