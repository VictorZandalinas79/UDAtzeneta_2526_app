import uuid
import time
from datetime import datetime, timedelta
from typing import Dict, Optional, Any, List
from config.settings import APP_CONFIG

class SessionManager:
    """Gestor de sesiones para la aplicación"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
            cls._instance.sessions = {}
            cls._instance.session_timeout = APP_CONFIG.get('session_timeout', 3600)  # 1 hora por defecto
        return cls._instance
    
    @classmethod
    def get_session(cls):
        """Obtiene la sesión actual (método de clase para facilitar el acceso)"""
        if cls._instance is None:
            return {}
        # Devolver la primera sesión activa (para simplificar)
        for session in cls._instance.sessions.values():
            if session.get('is_active', False) and cls._instance._is_session_valid(session):
                return session
        return {}
    
    def __init__(self):
        # Inicialización real solo ocurre una vez debido a __new__
        if not hasattr(self, 'sessions'):
            self.sessions = {}
            self.session_timeout = APP_CONFIG.get('session_timeout', 3600)
    
    def create_session(self, user_id: str, username: str, additional_data: Dict = None) -> str:
        """Crea una nueva sesión para un usuario"""
        session_id = str(uuid.uuid4())
        
        session_data = {
            'session_id': session_id,
            'user_id': user_id,
            'username': username,
            'created_at': datetime.utcnow(),
            'last_activity': datetime.utcnow(),
            'expires_at': datetime.utcnow() + timedelta(seconds=self.session_timeout),
            'is_active': True,
            'ip_address': None,  # Se puede añadir en el futuro
            'user_agent': None   # Se puede añadir en el futuro
        }
        
        # Añadir datos adicionales si se proporcionan
        if additional_data:
            session_data.update(additional_data)
        
        self.sessions[session_id] = session_data
        
        # Limpiar sesiones expiradas
        self._cleanup_expired_sessions()
        
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene los datos de una sesión"""
        if not session_id or session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        
        # Verificar si la sesión ha expirado
        if not self._is_session_valid(session):
            self.destroy_session(session_id)
            return None
        
        # Actualizar última actividad
        session['last_activity'] = datetime.utcnow()
        session['expires_at'] = datetime.utcnow() + timedelta(seconds=self.session_timeout)
        
        return session
    
    def update_session(self, session_id: str, data: Dict[str, Any]) -> bool:
        """Actualiza los datos de una sesión"""
        session = self.get_session(session_id)
        if not session:
            return False
        
        # No permitir actualizar ciertos campos críticos
        protected_fields = ['session_id', 'user_id', 'created_at']
        for key, value in data.items():
            if key not in protected_fields:
                session[key] = value
        
        session['last_activity'] = datetime.utcnow()
        return True
    
    def destroy_session(self, session_id: str) -> bool:
        """Destruye una sesión"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
    
    def is_session_valid(self, session_id: str) -> bool:
        """Verifica si una sesión es válida"""
        if not session_id or session_id not in self.sessions:
            return False
        
        session = self.sessions[session_id]
        return self._is_session_valid(session)
    
    def _is_session_valid(self, session: Dict[str, Any]) -> bool:
        """Verifica internamente si una sesión es válida"""
        if not session.get('is_active', False):
            return False
        
        expires_at = session.get('expires_at')
        if expires_at and datetime.utcnow() > expires_at:
            return False
        
        return True
    
    def extend_session(self, session_id: str, extension_time: int = None) -> bool:
        """Extiende el tiempo de vida de una sesión"""
        session = self.get_session(session_id)
        if not session:
            return False
        
        if extension_time is None:
            extension_time = self.session_timeout
        
        session['expires_at'] = datetime.utcnow() + timedelta(seconds=extension_time)
        session['last_activity'] = datetime.utcnow()
        return True
    
    def get_active_sessions(self) -> Dict[str, Dict[str, Any]]:
        """Obtiene todas las sesiones activas"""
        active_sessions = {}
        
        for session_id, session in self.sessions.items():
            if self._is_session_valid(session):
                active_sessions[session_id] = session
        
        return active_sessions
    
    def get_user_sessions(self, user_id: str) -> List[Dict[str, Any]]:
        """Obtiene todas las sesiones activas de un usuario"""
        user_sessions = []
        
        for session_id, session in self.sessions.items():
            if (session.get('user_id') == user_id and 
                self._is_session_valid(session)):
                user_sessions.append(session)
        
        return user_sessions
    
    def destroy_user_sessions(self, user_id: str) -> int:
        """Destruye todas las sesiones de un usuario"""
        sessions_to_destroy = []
        
        for session_id, session in self.sessions.items():
            if session.get('user_id') == user_id:
                sessions_to_destroy.append(session_id)
        
        for session_id in sessions_to_destroy:
            self.destroy_session(session_id)
        
        return len(sessions_to_destroy)
    
    def _cleanup_expired_sessions(self):
        """Limpia las sesiones expiradas"""
        expired_sessions = []
        
        for session_id, session in self.sessions.items():
            if not self._is_session_valid(session):
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            del self.sessions[session_id]
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas de las sesiones"""
        self._cleanup_expired_sessions()
        
        active_sessions = len(self.sessions)
        unique_users = len(set(session.get('user_id') for session in self.sessions.values()))
        
        # Calcular tiempo promedio de sesión activa
        total_duration = 0
        session_count = 0
        
        for session in self.sessions.values():
            if self._is_session_valid(session):
                duration = (datetime.utcnow() - session['created_at']).total_seconds()
                total_duration += duration
                session_count += 1
        
        avg_duration = total_duration / session_count if session_count > 0 else 0
        
        return {
            'active_sessions': active_sessions,
            'unique_users': unique_users,
            'average_session_duration': avg_duration,
            'session_timeout': self.session_timeout
        }

class DashSessionManager:
    """Adaptador del SessionManager para usar con Dash"""
    
    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager
    
    def create_dash_session(self, username: str, user_data: Dict = None) -> Dict[str, Any]:
        """Crea una sesión compatible con Dash"""
        session_id = self.session_manager.create_session(
            user_id=username,  # En este caso simple, usamos username como user_id
            username=username,
            additional_data=user_data or {}
        )
        
        return {
            'authenticated': True,
            'session_id': session_id,
            'username': username,
            'created_at': datetime.utcnow().isoformat(),
            **(user_data or {})
        }
    
    def validate_dash_session(self, session_data: Dict) -> bool:
        """Valida una sesión de Dash"""
        if not session_data or not session_data.get('authenticated'):
            return False
        
        session_id = session_data.get('session_id')
        if not session_id:
            return False
        
        return self.session_manager.is_session_valid(session_id)
    
    def refresh_dash_session(self, session_data: Dict) -> Dict[str, Any]:
        """Refresca una sesión de Dash"""
        if not self.validate_dash_session(session_data):
            return {'authenticated': False}
        
        session_id = session_data['session_id']
        self.session_manager.extend_session(session_id)
        
        # Actualizar timestamp
        session_data['last_activity'] = datetime.utcnow().isoformat()
        
        return session_data
    
    def destroy_dash_session(self, session_data: Dict) -> Dict[str, Any]:
        """Destruye una sesión de Dash"""
        session_id = session_data.get('session_id')
        if session_id:
            self.session_manager.destroy_session(session_id)
        
        return {'authenticated': False}

# Instancia global del gestor de sesiones
global_session_manager = SessionManager()
dash_session_manager = DashSessionManager(global_session_manager)