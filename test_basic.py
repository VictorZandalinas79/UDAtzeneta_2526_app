#!/usr/bin/env python3
"""
Tests básicos para la aplicación UD Atzeneta
Ejecutar con: python -m pytest test_basic.py -v
"""

import pytest
import sys
import os
from datetime import datetime, date
import tempfile

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database.db_manager import DatabaseManager, init_database, Jugador, Usuario, Calendario
from auth.login import hash_password, verify_credentials
from utils.helpers import format_date, validate_email, validate_dni, validate_phone
from utils.session_manager import SessionManager


class TestDatabaseConnection:
    """Tests para conexión y operaciones básicas de base de datos"""
    
    def setup_method(self):
        """Configuración antes de cada test"""
        # Usar base de datos temporal para tests
        self.test_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.test_db.close()
        
        # Configurar base de datos de test
        os.environ['DATABASE_URL'] = f'sqlite:///{self.test_db.name}'
        init_database()
        
    def teardown_method(self):
        """Limpieza después de cada test"""
        os.unlink(self.test_db.name)
    
    def test_database_initialization(self):
        """Test de inicialización de base de datos"""
        # La base de datos debe crearse sin errores
        assert os.path.exists(self.test_db.name)
        
        # Debe existir el usuario admin por defecto
        with DatabaseManager() as db:
            admin_user = db.db.query(Usuario).filter(Usuario.username == 'admin').first()
            assert admin_user is not None
            assert admin_user.username == 'admin'
    
    def test_create_player(self):
        """Test de creación de jugador"""
        with DatabaseManager() as db:
            jugador_data = {
                'nombre_futbolistico': 'Test Player',
                'nombre': 'Jugador',
                'apellidos': 'De Prueba',
                'email': 'test@example.com',
                'dni': '12345678A',
                'posicion': 'Delantero',
                'dorsal': 10
            }
            
            jugador = db.create_jugador(**jugador_data)
            assert jugador.id is not None
            assert jugador.nombre_futbolistico == 'Test Player'
            assert jugador.dorsal == 10
    
    def test_get_players(self):
        """Test de obtención de jugadores"""
        with DatabaseManager() as db:
            # Crear jugadores de prueba
            for i in range(3):
                db.create_jugador(
                    nombre_futbolistico=f'Player {i}',
                    nombre=f'Nombre {i}',
                    apellidos='Apellido',
                    activo=i < 2  # Solo los 2 primeros activos
                )
            
            # Test obtener solo activos
            activos = db.get_jugadores(activos_solo=True)
            assert len(activos) == 2
            
            # Test obtener todos
            todos = db.get_jugadores(activos_solo=False)
            assert len(todos) == 3


class TestAuthentication:
    """Tests para sistema de autenticación"""
    
    def test_password_hashing(self):
        """Test de hash de contraseñas"""
        password = "test_password_123"
        hashed = hash_password(password)
        
        assert hashed != password
        assert len(hashed) > 50  # bcrypt genera hashes largos
    
    def test_credential_verification(self):
        """Test de verificación de credenciales"""
        # Usar base de datos temporal
        test_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        test_db.close()
        
        try:
            os.environ['DATABASE_URL'] = f'sqlite:///{test_db.name}'
            init_database()
            
            # Test con credenciales por defecto
            assert verify_credentials('admin', 'admin123') == True
            assert verify_credentials('admin', 'wrong_password') == False
            assert verify_credentials('wrong_user', 'admin123') == False
            
        finally:
            os.unlink(test_db.name)


class TestUtilityFunctions:
    """Tests para funciones de utilidad"""
    
    def test_format_date(self):
        """Test de formateo de fechas"""
        test_date = date(2024, 12, 17)
        formatted = format_date(test_date)
        assert formatted == "17/12/2024"
        
        # Test con formato personalizado
        formatted_custom = format_date(test_date, "%Y-%m-%d")
        assert formatted_custom == "2024-12-17"
    
    def test_email_validation(self):
        """Test de validación de emails"""
        assert validate_email("test@example.com") == True
        assert validate_email("user.name+tag@domain.co.uk") == True
        assert validate_email("invalid.email") == False
        assert validate_email("@domain.com") == False
        assert validate_email("user@") == False
        assert validate_email("") == False
    
    def test_dni_validation(self):
        """Test de validación de DNI español"""
        assert validate_dni("12345678Z") == True
        assert validate_dni("87654321X") == True
        assert validate_dni("12345678A") == False  # Letra incorrecta
        assert validate_dni("1234567890") == False  # Muy largo
        assert validate_dni("1234567Z") == False  # Muy corto
        assert validate_dni("") == False
    
    def test_phone_validation(self):
        """Test de validación de teléfonos españoles"""
        assert validate_phone("600123456") == True
        assert validate_phone("+34600123456") == True
        assert validate_phone("912345678") == True
        assert validate_phone("+34912345678") == True
        assert validate_phone("123456789") == False  # No válido
        assert validate_phone("") == False


class TestSessionManager:
    """Tests para el gestor de sesiones"""
    
    def setup_method(self):
        """Configuración antes de cada test"""
        self.session_manager = SessionManager()
    
    def test_create_session(self):
        """Test de creación de sesión"""
        session_id = self.session_manager.create_session(
            user_id="test_user",
            username="testuser"
        )
        
        assert session_id is not None
        assert len(session_id) > 20  # UUID debe ser largo
        
        # Verificar que la sesión existe
        session = self.session_manager.get_session(session_id)
        assert session is not None
        assert session['username'] == 'testuser'
    
    def test_session_validation(self):
        """Test de validación de sesiones"""
        # Crear sesión válida
        session_id = self.session_manager.create_session(
            user_id="test_user",
            username="testuser"
        )
        
        assert self.session_manager.is_session_valid(session_id) == True
        assert self.session_manager.is_session_valid("invalid_session") == False
        assert self.session_manager.is_session_valid("") == False
    
    def test_destroy_session(self):
        """Test de destrucción de sesión"""
        session_id = self.session_manager.create_session(
            user_id="test_user",
            username="testuser"
        )
        
        # Verificar que existe
        assert self.session_manager.is_session_valid(session_id) == True
        
        # Destruir sesión
        destroyed = self.session_manager.destroy_session(session_id)
        assert destroyed == True
        
        # Verificar que ya no existe
        assert self.session_manager.is_session_valid(session_id) == False


class TestDataValidation:
    """Tests para validación de datos"""
    
    def test_player_data_validation(self):
        """Test de validación de datos de jugador"""
        # Datos válidos
        valid_data = {
            'nombre_futbolistico': 'Messi',
            'nombre': 'Lionel',
            'apellidos': 'Messi',
            'email': 'messi@example.com',
            'dni': '12345678Z',
            'telefono': '600123456',
            'dorsal': 10,
            'posicion': 'Delantero'
        }
        
        # Verificar validaciones individuales
        assert validate_email(valid_data['email']) == True
        assert validate_dni(valid_data['dni']) == True
        assert validate_phone(valid_data['telefono']) == True
        assert 1 <= valid_data['dorsal'] <= 99
        
        # Datos inválidos
        invalid_data = {
            'email': 'invalid_email',
            'dni': 'invalid_dni',
            'telefono': '123',
            'dorsal': 100  # Fuera de rango
        }
        
        assert validate_email(invalid_data['email']) == False
        assert validate_dni(invalid_data['dni']) == False
        assert validate_phone(invalid_data['telefono']) == False
        assert not (1 <= invalid_data['dorsal'] <= 99)


class TestApplicationIntegration:
    """Tests de integración de la aplicación"""
    
    def setup_method(self):
        """Configuración antes de cada test"""
        self.test_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.test_db.close()
        os.environ['DATABASE_URL'] = f'sqlite:///{self.test_db.name}'
        init_database()
    
    def teardown_method(self):
        """Limpieza después de cada test"""
        os.unlink(self.test_db.name)
    
    def test_complete_workflow(self):
        """Test de flujo completo: crear jugador, calendario, etc."""
        with DatabaseManager() as db:
            # 1. Crear jugador
            jugador = db.create_jugador(
                nombre_futbolistico='Test Player',
                nombre='Test',
                apellidos='Player',
                email='test@example.com',
                posicion='Delantero'
            )
            
            assert jugador.id is not None
            
            # 2. Crear evento de calendario
            evento = db.create_evento_calendario(
                fecha=date(2024, 12, 25),
                hora="16:00",
                competicion="Liga",
                equipo_local="UD Atzeneta",
                equipo_visitante="Rival FC",
                campo="Campo Municipal"
            )
            
            assert evento.id is not None
            
            # 3. Verificar que se pueden obtener los datos
            jugadores = db.get_jugadores()
            calendario = db.get_calendario()
            
            assert len(jugadores) >= 1
            assert len(calendario) >= 1
            assert jugadores[0].nombre_futbolistico == 'Test Player'
            assert calendario[0].equipo_local == 'UD Atzeneta'


def run_tests():
    """Ejecuta todos los tests"""
    print("🧪 Ejecutando tests para UD Atzeneta...")
    
    # Ejecutar tests con pytest
    exit_code = pytest.main([__file__, '-v', '--tb=short'])
    
    if exit_code == 0:
        print("✅ Todos los tests pasaron correctamente")
    else:
        print("❌ Algunos tests fallaron")
    
    return exit_code


if __name__ == '__main__':
    run_tests()