import schedule
import time
from log_parser import analizar_logs
from report_generator import generar_informe_excel

def tarea_automatica() -> None:
    print("\n🤖 Ejecutando tarea automática...")
    analizar_logs()
    generar_informe_excel()
    print("✅ Tarea completada")

schedule.every(1).hours.do(tarea_automatica)

print("⏰ Scheduler iniciado — ejecutando cada hora")
print("   Presiona Ctrl+C para detener")

tarea_automatica()

while True:
    schedule.run_pending()
    time.sleep(60)