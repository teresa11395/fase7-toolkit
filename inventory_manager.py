import pandas as pd

def cargar_inventario(archivo: str = "inventory.csv") -> pd.DataFrame:
    try:
        df = pd.read_csv(archivo)
        print(f"✅ Inventario cargado: {len(df)} servidores")
        return df
    except FileNotFoundError:
        print(f"❌ No se encontró {archivo}")
        return pd.DataFrame()

def filtrar_vulnerables(df: pd.DataFrame) -> pd.DataFrame:
    vulnerables = df[
        (df["os"].str.contains("Windows Server")) |
        (df["ram_gb"] < 4)
    ]
    print(f"\n⚠️  Servidores vulnerables o antiguos: {len(vulnerables)}")
    print(vulnerables[["hostname", "ip", "os", "ram_gb", "departamento"]].to_string(index=False))
    return vulnerables

def agrupar_por_departamento(df: pd.DataFrame) -> None:
    grupos = df.groupby("departamento").size().sort_values(ascending=False)
    print("\n📊 Servidores por departamento:")
    for dept, cantidad in grupos.items():
        print(f"   {dept:<15} → {cantidad} servidores")

def analizar_inventario() -> pd.DataFrame:
    df = cargar_inventario()
    if df.empty:
        return df
    agrupar_por_departamento(df)
    vulnerables = filtrar_vulnerables(df)
    return vulnerables

if __name__ == "__main__":
    analizar_inventario()