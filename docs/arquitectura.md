## Flujo de datos

1. `auth.log` → `log_parser.py` → extrae IPs atacantes
2. IPs atacantes → `threat_intel.py` → consulta API → tabla de amenazas
3. `generate_inventory.py` → `inventory.csv` → `inventory_manager.py` → filtra vulnerables
4. Servidores vulnerables → `report_generator.py` → `informe_vulnerables.xlsx`
5. `scheduler.py` → ejecuta pasos 1-4 automáticamente cada hora

## Módulos y responsabilidades

**`sys_toolkit.py`** — punto de entrada principal. Muestra el menú y coordina todos los módulos.

**`os_utils.py`** — operaciones del sistema operativo. Usa `subprocess` para ping y `shutil` para disco.

**`log_parser.py`** — parsea logs línea a línea con `with open()`. Usa sets y diccionarios para contar IPs.

**`network_models.py`** — modela dispositivos de red con POO. Clase base `NetworkDevice` con hijos `Router` y `Server`.

**`threat_intel.py`** — consulta la API pública ipinfo.io con `requests` para geolocalizar IPs sospechosas.

**`inventory_manager.py`** — carga y filtra el CSV con Pandas. Agrupa por departamento y detecta servidores vulnerables.

**`report_generator.py`** — exporta datos filtrados a Excel con `.to_excel()` de Pandas/OpenPyXL.

**`scheduler.py`** — ejecuta tareas automáticamente cada hora usando la librería `schedule`.