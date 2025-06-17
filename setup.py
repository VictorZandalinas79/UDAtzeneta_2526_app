#!/usr/bin/env python3
"""
Script de instalación y configuración para UD Atzeneta
Automatiza la configuración inicial de la aplicación

Uso:
    python setup.py install    # Instalación completa
    python setup.py configure  # Solo configuración
    python setup.py test       # Ejecutar tests
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def print_banner():
    """Muestra el banner de bienvenida"""
    banner = """
    ⚽ UD ATZENETA - SISTEMA DE GESTIÓN ⚽
    =====================================
    
    Configurando la aplicación de gestión
    del equipo de fútbol UD Atzeneta
    
    Versión 1.0.0
    Desarrollado con ❤️ para el club
    """
    print(banner)

def check_python_version():
    """Verifica que se esté usando Python 3.11+"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print("❌ Se requiere Python 3.11 o superior")
        print(f"   Versión actual: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
    return True

def install_dependencies():
    """Instala las dependencias del proyecto"""
    print("\n📦 Instalando dependencias...")
    
    try:
        # Actualizar pip
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], 
                      check=True, capture_output=True)
        
        # Instalar dependencias desde requirements.txt
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True, capture_output=True)
        
        print("✅ Dependencias instaladas correctamente")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False

def create_directory_structure():
    """Crea la estructura de directorios necesaria"""
    print("\n📁 Creando estructura de directorios...")
    
    directories = [
        'assets/images',
        'logs',
        'backups',
        'exports',
        'temp'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   📂 {directory}")
    
    # Crear archivo .gitkeep en assets/images
    gitkeep_path = Path('assets/images/.gitkeep')
    if not gitkeep_path.exists():
        gitkeep_path.touch()
    
    print("✅ Estructura de directorios creada")

def create_env_file():
    """Crea el archivo .env si no existe"""
    print("\n⚙️  Configurando variables de entorno...")
    
    env_path = Path('.env')
    env_example_path = Path('.env.example')
    
    if env_path.exists():
        print("   ℹ️  Archivo .env ya existe, omitiendo...")
        return
    
    if not env_example_path.exists():
        print("   ⚠️  Archivo .env.example no encontrado")
        return
    
    # Copiar .env.example a .env
    with open(env_example_path, 'r') as source:
        with open(env_path, 'w') as dest:
            dest.write(source.read())
    
    print("✅ Archivo .env creado desde .env.example")
    print("   📝 Edita .env para personalizar la configuración")

def initialize_database():
    """Inicializa la base de datos"""
    print("\n🗄️  Inicializando base de datos...")
    
    try:
        # Importar e inicializar la base de datos
        sys.path.insert(0, os.getcwd())
        from database.db_manager import init_database
        
        init_database()
        print("✅ Base de datos inicializada correctamente")
        print("   👤 Usuario por defecto: admin / admin123")
        return True
        
    except Exception as e:
        print(f"❌ Error inicializando base de datos: {e}")
        return False

def run_tests():
    """Ejecuta los tests básicos"""
    print("\n🧪 Ejecutando tests básicos...")
    
    try:
        # Verificar que pytest está instalado
        subprocess.run([sys.executable, '-c', 'import pytest'], 
                      check=True, capture_output=True)
        
        # Ejecutar tests
        result = subprocess.run([sys.executable, '-m', 'pytest', 'test_basic.py', '-v'], 
                               capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Todos los tests pasaron correctamente")
            return True
        else:
            print("❌ Algunos tests fallaron:")
            print(result.stdout)
            return False
            
    except subprocess.CalledProcessError:
        print("⚠️  pytest no está instalado, omitiendo tests...")
        return True

def check_application():
    """Verifica que la aplicación se puede importar correctamente"""
    print("\n🔍 Verificando aplicación...")
    
    try:
        sys.path.insert(0, os.getcwd())
        
        # Verificar importaciones críticas
        from database.db_manager import DatabaseManager
        from auth.login import verify_credentials
        from config.settings import APP_CONFIG
        
        print("✅ Todas las importaciones son correctas")
        return True
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        return False

def create_startup_script():
    """Crea script de inicio para desarrollo"""
    print("\n🚀 Creando script de inicio...")
    
    startup_content = """#!/usr/bin/env python3
\"\"\"
Script de inicio para UD Atzeneta
\"\"\"

import os
import sys

def main():
    print("🚀 Iniciando UD Atzeneta...")
    
    # Configurar variables de entorno si existen
    if os.path.exists('.env'):
        from dotenv import load_dotenv
        load_dotenv()
    
    # Importar y ejecutar la aplicación
    from app import app, server
    
    port = int(os.environ.get('PORT', 8050))
    debug = os.environ.get('DASH_DEBUG_MODE', 'True') == 'True'
    
    print(f"📡 Servidor iniciado en http://localhost:{port}")
    print("👤 Usuario por defecto: admin / admin123")
    print("🛑 Presiona Ctrl+C para detener")
    
    app.run_server(
        host='0.0.0.0',
        port=port,
        debug=debug
    )

if __name__ == '__main__':
    main()
"""
    
    with open('start.py', 'w') as f:
        f.write(startup_content)
    
    # Hacer ejecutable en sistemas Unix
    if os.name != 'nt':
        os.chmod('start.py', 0o755)
    
    print("✅ Script de inicio creado: start.py")

def print_final_instructions():
    """Muestra las instrucciones finales"""
    instructions = """
    🎉 ¡INSTALACIÓN COMPLETADA!
    ===========================
    
    La aplicación UD Atzeneta está lista para usar.
    
    📋 PRÓXIMOS PASOS:
    
    1. Iniciar la aplicación:
       python start.py
       
    2. Abrir en navegador:
       http://localhost:8050
       
    3. Iniciar sesión:
       Usuario: admin
       Contraseña: admin123
    
    📚 COMANDOS ÚTILES:
    
    • Administración:     python admin.py --help
    • Tests:              python -m pytest test_basic.py
    • Backup:             python admin.py backup-data
    • Crear usuario:      python admin.py create-user
    
    📁 ARCHIVOS IMPORTANTES:
    
    • .env                - Configuración local
    • ud_atzeneta.db      - Base de datos
    • assets/images/      - Fotos de jugadores
    • backups/            - Copias de seguridad
    
    🆘 SOPORTE:
    
    • README.md           - Documentación completa
    • CHANGELOG.md        - Historial de cambios
    • GitHub Issues       - Reportar problemas
    
    ¡Disfruta gestionando tu equipo! ⚽
    """
    print(instructions)

def install_full():
    """Realiza la instalación completa"""
    print_banner()
    
    if not check_python_version():
        return False
    
    steps = [
        ("Instalando dependencias", install_dependencies),
        ("Creando directorios", create_directory_structure),
        ("Configurando entorno", create_env_file),
        ("Inicializando base de datos", initialize_database),
        ("Verificando aplicación", check_application),
        ("Creando script de inicio", create_startup_script),
    ]
    
    for step_name, step_func in steps:
        try:
            if not step_func():
                print(f"\n❌ Error en: {step_name}")
                return False
        except Exception as e:
            print(f"\n❌ Error inesperado en {step_name}: {e}")
            return False
    
    print_final_instructions()
    return True

def configure_only():
    """Solo realiza la configuración sin instalar dependencias"""
    print_banner()
    
    steps = [
        ("Creando directorios", create_directory_structure),
        ("Configurando entorno", create_env_file),
        ("Inicializando base de datos", initialize_database),
        ("Creando script de inicio", create_startup_script),
    ]
    
    for step_name, step_func in steps:
        try:
            step_func()
        except Exception as e:
            print(f"\n❌ Error en {step_name}: {e}")
            return False
    
    print("\n✅ Configuración completada")
    return True

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description='Setup para UD Atzeneta')
    parser.add_argument('command', 
                       choices=['install', 'configure', 'test'], 
                       help='Comando a ejecutar')
    
    args = parser.parse_args()
    
    if args.command == 'install':
        success = install_full()
    elif args.command == 'configure':
        success = configure_only()
    elif args.command == 'test':
        print_banner()
        success = run_tests()
    
    return 0 if success else 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)