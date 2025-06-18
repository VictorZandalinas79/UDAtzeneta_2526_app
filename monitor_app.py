# monitor_app.py - Script para monitorear la aplicación

import time
import sys
from datetime import datetime

def monitor_logs():
    """Monitorea los logs de la aplicación"""
    
    print("🔍 MONITOR: Iniciando monitoreo de la aplicación...")
    print("=" * 60)
    print("INSTRUCCIONES:")
    print("1. Ejecuta este script en una terminal: python monitor_app.py")
    print("2. En otra terminal ejecuta: python app.py")
    print("3. Ve al calendario en el navegador")
    print("4. Observa los mensajes que aparecen aquí")
    print("=" * 60)
    
    print(f"\n🕐 {datetime.now().strftime('%H:%M:%S')} - Monitor iniciado")
    print("Esperando que ejecutes 'python app.py' en otra terminal...\n")
    
    # Instrucciones específicas
    print("🔍 QUÉ BUSCAR EN LOS LOGS:")
    print("✅ Mensajes que empiecen con '🔄 CALENDARIO:'")
    print("✅ Mensajes que empiecen con '🔥 [MAIN CALLBACK]'")
    print("✅ Mensajes que empiecen con '📊 [TABLE]'")
    print("✅ Mensajes que empiecen con '🔍 [RAW DATA]'")
    print("\n❌ SI NO VES ESTOS MENSAJES:")
    print("   → Los callbacks NO se están ejecutando")
    print("   → Hay un problema en el registro de callbacks")
    
    print("\n🌐 EN EL NAVEGADOR DEBERÍAS VER:")
    print("✅ Una página con información de debug")
    print("✅ Contador de ejecuciones que aumenta")
    print("✅ Datos raw que se actualizan")
    print("✅ Una tabla con al menos 1 partido (el de prueba)")
    
    print("\n" + "=" * 60)
    print("🚀 AHORA EJECUTA EN OTRA TERMINAL:")
    print("   python app.py")
    print("=" * 60)
    
    # Mantener el script vivo
    try:
        while True:
            time.sleep(5)
            current_time = datetime.now().strftime('%H:%M:%S')
            print(f"🕐 {current_time} - Monitor activo (Ctrl+C para salir)")
    except KeyboardInterrupt:
        print("\n🛑 Monitor detenido")

if __name__ == "__main__":
    monitor_logs()