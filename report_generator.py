import pandas as pd
from datetime import datetime
from inventory_manager import cargar_inventario, filtrar_vulnerables

def generar_informe_excel(archivo_salida: str = None) -> None:
    if archivo_salida is None:
        fecha = datetime.now().strftime("%Y-%m")
        archivo_salida = f"informe_vulnerables_{fecha}.xlsx"
    
    df = cargar_inventario()
    if df.empty:
        return
    
    vulnerables = filtrar_vulnerables(df)
    
    vulnerables.to_excel(archivo_salida, index=False, sheet_name="Servidores Vulnerables")
    
    print(f"\n📊 Informe Excel generado: {archivo_salida}")
    print(f"   Total servidores vulnerables: {len(vulnerables)}")

if __name__ == "__main__":
    generar_informe_excel()