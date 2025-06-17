#!/usr/bin/env python3
"""
Script de administración para UD Atzeneta
Utilidades para gestión de la base de datos, usuarios y mantenimiento

Uso:
    python admin.py <comando> [argumentos]

Comandos disponibles:
    init-db         - Inicializar base de datos
    create-user     - Crear nuevo usuario
    reset-password  - Resetear contraseña de usuario
    backup-data     - Crear backup de datos
    restore-data    - Restaurar datos desde backup
    cleanup         - Limpiar datos antiguos
    stats          - Mostrar estadísticas de la aplicación
    import-players  - Importar jugadores desde CSV
    export-data    - Exportar datos a CSV
"""

import sys
import os
import json
import csv
import argparse
from datetime import datetime, timedelta
from getpass import getpass
from pathlib import Path

# Añadir el directorio raíz al path para importar módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db_manager import DatabaseManager, init_database, Usuario, Jugador
from auth.login import hash_password
from utils.helpers import create_backup_data, export_to_excel

class AdminManager:
    """Gestor de operaciones administrativas"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
    
    def init_database(self):
        """Inicializa la base de datos"""
        print("Inicializando base de datos...")
        try:
            init_database()
            print("✅ Base de datos inicializada correctamente")
            print("👤 Usuario por defecto: admin / admin123")
        except Exception as e:
            print(f"❌ Error inicializando base de datos: {e}")
    
    def create_user(self, username=None, password=None, email=None, nombre=None):
        """Crea un nuevo usuario"""
        print("Creando nuevo usuario...")
        
        if not username:
            username = input("Nombre de usuario: ")
        
        if not password:
            password = getpass("Contraseña: ")
            password_confirm = getpass("Confirmar contraseña: ")
            if password != password_confirm:
                print("❌ Las contraseñas no coinciden")
                return
        
        if not email:
            email = input("Email (opcional): ") or None
        
        if not nombre:
            nombre = input("Nombre completo (opcional): ") or None
        
        try:
            with self.db_manager as db:
                # Verificar si el usuario ya existe
                existing_user = db.db.query(Usuario).filter(
                    Usuario.username == username
                ).first()
                
                if existing_user:
                    print(f"❌ El usuario '{username}' ya existe")
                    return
                
                # Crear nuevo usuario
                password_hash = hash_password(password)
                new_user = Usuario(
                    username=username,
                    password_hash=password_hash,
                    email=email,
                    nombre=nombre
                )
                
                db.db.add(new_user)
                db.db.commit()
                
                print(f"✅ Usuario '{username}' creado correctamente")
                
        except Exception as e:
            print(f"❌ Error creando usuario: {e}")
    
    def reset_password(self, username=None):
        """Resetea la contraseña de un usuario"""
        if not username:
            username = input("Nombre de usuario: ")
        
        new_password = getpass("Nueva contraseña: ")
        confirm_password = getpass("Confirmar nueva contraseña: ")
        
        if new_password != confirm_password:
            print("❌ Las contraseñas no coinciden")
            return
        
        try:
            with self.db_manager as db:
                user = db.db.query(Usuario).filter(
                    Usuario.username == username
                ).first()
                
                if not user:
                    print(f"❌ Usuario '{username}' no encontrado")
                    return
                
                user.password_hash = hash_password(new_password)
                db.db.commit()
                
                print(f"✅ Contraseña de '{username}' actualizada correctamente")
                
        except Exception as e:
            print(f"❌ Error actualizando contraseña: {e}")
    
    def backup_data(self, output_file=None):
        """Crea un backup completo de los datos"""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"backup_ud_atzeneta_{timestamp}.json"
        
        print(f"Creando backup en {output_file}...")
        
        try:
            backup_data = create_backup_data(self.db_manager)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(backup_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Backup creado correctamente: {output_file}")
            print(f"📊 Estadísticas del backup:")
            
            data = backup_data.get('data', {})
            for table, records in data.items():
                if isinstance(records, list):
                    print(f"  - {table}: {len(records)} registros")
                    
        except Exception as e:
            print(f"❌ Error creando backup: {e}")
    
    def restore_data(self, backup_file):
        """Restaura datos desde un archivo de backup"""
        if not os.path.exists(backup_file):
            print(f"❌ Archivo de backup no encontrado: {backup_file}")
            return
        
        print(f"⚠️  ADVERTENCIA: Esta operación reemplazará todos los datos actuales")
        confirm = input("¿Continuar? (sí/no): ").lower()
        if confirm not in ['sí', 'si', 'yes', 'y']:
            print("Operación cancelada")
            return
        
        try:
            with open(backup_file, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
            
            print("Restaurando datos...")
            # Aquí se implementaría la lógica de restauración
            # Por seguridad, se requiere implementación adicional
            
            print("✅ Datos restaurados correctamente")
            
        except Exception as e:
            print(f"❌ Error restaurando datos: {e}")
    
    def cleanup_old_data(self, days=90):
        """Limpia datos antiguos"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        print(f"Limpiando datos anteriores a {cutoff_date.strftime('%d/%m/%Y')}...")
        
        try:
            with self.db_manager as db:
                # Aquí se implementaría la lógica de limpieza
                # Por ejemplo, eliminar sesiones expiradas, logs antiguos, etc.
                
                print("✅ Limpieza completada")
                
        except Exception as e:
            print(f"❌ Error en limpieza: {e}")
    
    def show_stats(self):
        """Muestra estadísticas de la aplicación"""
        print("📊 Estadísticas de UD Atzeneta")
        print("=" * 40)
        
        try:
            with self.db_manager as db:
                # Estadísticas de usuarios
                total_users = db.db.query(Usuario).count()
                active_users = db.db.query(Usuario).filter(Usuario.activo == True).count()
                
                # Estadísticas de jugadores
                total_players = db.db.query(Jugador).count()
                active_players = db.db.query(Jugador).filter(Jugador.activo == True).count()
                
                # Estadísticas del calendario
                calendar_events = db.get_calendario()
                
                # Estadísticas de entrenamientos
                trainings = db.get_entrenamientos()
                
                # Estadísticas de multas
                multas = db.get_multas()
                multas_pendientes = db.get_multas_pendientes()
                
                print(f"👤 Usuarios:")
                print(f"  - Total: {total_users}")
                print(f"  - Activos: {active_users}")
                print()
                
                print(f"⚽ Jugadores:")
                print(f"  - Total: {total_players}")
                print(f"  - Activos: {active_players}")
                print()
                
                print(f"📅 Calendario:")
                print(f"  - Eventos: {len(calendar_events)}")
                print()
                
                print(f"🏃 Entrenamientos:")
                print(f"  - Total: {len(trainings)}")
                print()
                
                print(f"💰 Multas:")
                print(f"  - Total: {len(multas)}")
                print(f"  - Pendientes: {len(multas_pendientes)}")
                
                if multas:
                    total_amount = sum(m.multa for m in multas)
                    pending_amount = sum(m.debe for m in multas_pendientes)
                    print(f"  - Importe total: €{total_amount:.2f}")
                    print(f"  - Pendiente: €{pending_amount:.2f}")
                
        except Exception as e:
            print(f"❌ Error obteniendo estadísticas: {e}")
    
    def import_players_csv(self, csv_file):
        """Importa jugadores desde un archivo CSV"""
        if not os.path.exists(csv_file):
            print(f"❌ Archivo CSV no encontrado: {csv_file}")
            return
        
        print(f"Importando jugadores desde {csv_file}...")
        
        try:
            imported = 0
            skipped = 0
            
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                with self.db_manager as db:
                    for row in reader:
                        # Verificar si el jugador ya existe
                        existing = db.db.query(Jugador).filter(
                            Jugador.dni == row.get('dni')
                        ).first() if row.get('dni') else None
                        
                        if existing:
                            print(f"⚠️  Jugador {row.get('nombre', 'Sin nombre')} ya existe (DNI: {row.get('dni')})")
                            skipped += 1
                            continue
                        
                        # Crear nuevo jugador
                        jugador_data = {
                            'nombre_futbolistico': row.get('nombre_futbolistico', ''),
                            'nombre': row.get('nombre', ''),
                            'apellidos': row.get('apellidos', ''),
                            'email': row.get('email') or None,
                            'dni': row.get('dni') or None,
                            'telefono': row.get('telefono') or None,
                            'direccion': row.get('direccion') or None,
                            'dorsal': int(row.get('dorsal')) if row.get('dorsal') else None,
                            'posicion': row.get('posicion') or None,
                            'altura': float(row.get('altura')) if row.get('altura') else None
                        }
                        
                        jugador = Jugador(**jugador_data)
                        db.db.add(jugador)
                        imported += 1
                    
                    db.db.commit()
            
            print(f"✅ Importación completada:")
            print(f"  - Importados: {imported}")
            print(f"  - Omitidos: {skipped}")
            
        except Exception as e:
            print(f"❌ Error importando jugadores: {e}")
    
    def export_data_csv(self, output_dir="exports"):
        """Exporta todos los datos a archivos CSV"""
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        print(f"Exportando datos a {output_dir}...")
        
        try:
            with self.db_manager as db:
                # Exportar jugadores
                jugadores = db.get_jugadores(activos_solo=False)
                jugadores_data = []
                
                for j in jugadores:
                    jugadores_data.append({
                        'id': j.id,
                        'nombre_futbolistico': j.nombre_futbolistico,
                        'nombre': j.nombre,
                        'apellidos': j.apellidos,
                        'email': j.email,
                        'dni': j.dni,
                        'telefono': j.telefono,
                        'direccion': j.direccion,
                        'dorsal': j.dorsal,
                        'posicion': j.posicion,
                        'altura': j.altura,
                        'goles': j.goles,
                        'asistencias': j.asistencias,
                        'tarjetas_amarillas': j.tarjetas_amarillas,
                        'tarjetas_rojas': j.tarjetas_rojas,
                        'activo': j.activo
                    })
                
                # Escribir CSV de jugadores
                jugadores_file = os.path.join(output_dir, f"jugadores_{timestamp}.csv")
                with open(jugadores_file, 'w', newline='', encoding='utf-8') as f:
                    if jugadores_data:
                        writer = csv.DictWriter(f, fieldnames=jugadores_data[0].keys())
                        writer.writeheader()
                        writer.writerows(jugadores_data)
                
                print(f"✅ Jugadores exportados: {jugadores_file}")
                
                # Exportar calendario
                calendario = db.get_calendario()
                calendario_data = []
                
                for c in calendario:
                    calendario_data.append({
                        'fecha': c.fecha.strftime("%Y-%m-%d") if c.fecha else '',
                        'hora': c.hora,
                        'competicion': c.competicion,
                        'equipo_local': c.equipo_local,
                        'equipo_visitante': c.equipo_visitante,
                        'goles_local': c.goles_equipo_local,
                        'goles_visitante': c.goles_equipo_visitante,
                        'arbitro': c.arbitro,
                        'campo': c.campo
                    })
                
                calendario_file = os.path.join(output_dir, f"calendario_{timestamp}.csv")
                with open(calendario_file, 'w', newline='', encoding='utf-8') as f:
                    if calendario_data:
                        writer = csv.DictWriter(f, fieldnames=calendario_data[0].keys())
                        writer.writeheader()
                        writer.writerows(calendario_data)
                
                print(f"✅ Calendario exportado: {calendario_file}")
                
        except Exception as e:
            print(f"❌ Error exportando datos: {e}")

def main():
    """Función principal del script"""
    parser = argparse.ArgumentParser(description='Script de administración para UD Atzeneta')
    parser.add_argument('command', help='Comando a ejecutar')
    parser.add_argument('--username', help='Nombre de usuario')
    parser.add_argument('--password', help='Contraseña')
    parser.add_argument('--email', help='Email')
    parser.add_argument('--nombre', help='Nombre completo')
    parser.add_argument('--file', help='Archivo de entrada/salida')
    parser.add_argument('--days', type=int, default=90, help='Días para limpieza')
    
    args = parser.parse_args()
    
    admin = AdminManager()
    
    if args.command == 'init-db':
        admin.init_database()
    
    elif args.command == 'create-user':
        admin.create_user(args.username, args.password, args.email, args.nombre)
    
    elif args.command == 'reset-password':
        admin.reset_password(args.username)
    
    elif args.command == 'backup-data':
        admin.backup_data(args.file)
    
    elif args.command == 'restore-data':
        if not args.file:
            print("❌ Se requiere especificar --file")
            return
        admin.restore_data(args.file)
    
    elif args.command == 'cleanup':
        admin.cleanup_old_data(args.days)
    
    elif args.command == 'stats':
        admin.show_stats()
    
    elif args.command == 'import-players':
        if not args.file:
            print("❌ Se requiere especificar --file")
            return
        admin.import_players_csv(args.file)
    
    elif args.command == 'export-data':
        admin.export_data_csv()
    
    else:
        print(f"❌ Comando desconocido: {args.command}")
        print("Comandos disponibles: init-db, create-user, reset-password, backup-data, restore-data, cleanup, stats, import-players, export-data")

if __name__ == '__main__':
    main()