from sqlalchemy import create_engine, Column, Integer, String, Float, Date, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, date
import os

# Configuración de la base de datos
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///ud_atzeneta.db')
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelos de la base de datos

class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    email = Column(String(100), unique=True, index=True)
    nombre = Column(String(100))
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

class Jugador(Base):
    __tablename__ = 'jugadores'
    
    id = Column(Integer, primary_key=True, index=True)
    # Datos personales
    nombre_futbolistico = Column(String(50), nullable=False)
    nombre = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    email = Column(String(100))
    dni = Column(String(20), unique=True)
    telefono = Column(String(20))
    direccion = Column(Text)
    
    # Datos futbolísticos
    dorsal = Column(Integer)
    posicion = Column(String(50))
    pierna_dominante = Column(String(20))
    
    # Estadísticas
    goles = Column(Integer, default=0)
    asistencias = Column(Integer, default=0)
    tarjetas_amarillas = Column(Integer, default=0)
    tarjetas_rojas = Column(Integer, default=0)
    minutos_jugados = Column(Integer, default=0)
    partidos_titular = Column(Integer, default=0)
    partidos_suplente = Column(Integer, default=0)
    convocatorias = Column(Integer, default=0)
    
    # Datos físicos
    altura = Column(Float)
    foto_url = Column(String(255))
    activo = Column(Boolean, default=True)
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    pesos = relationship("PesoJugador", back_populates="jugador")
    lesiones = relationship("Lesion", back_populates="jugador")
    entrenamientos = relationship("AsistenciaEntrenamiento", back_populates="jugador")
    puntuaciones = relationship("Puntuacion", back_populates="jugador")
    multas = relationship("Multa", back_populates="jugador")

class PesoJugador(Base):
    __tablename__ = 'peso_jugadores'
    
    id = Column(Integer, primary_key=True, index=True)
    jugador_id = Column(Integer, ForeignKey('jugadores.id'))
    peso = Column(Float, nullable=False)
    fecha = Column(Date, nullable=False)
    
    jugador = relationship("Jugador", back_populates="pesos")

class Lesion(Base):
    __tablename__ = 'lesiones'
    
    id = Column(Integer, primary_key=True, index=True)
    jugador_id = Column(Integer, ForeignKey('jugadores.id'))
    tipo_lesion = Column(String(100), nullable=False)
    descripcion = Column(Text)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date)
    activa = Column(Boolean, default=True)
    
    jugador = relationship("Jugador", back_populates="lesiones")

class Calendario(Base):
    __tablename__ = 'calendario'
    
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False)
    hora = Column(String(10))
    competicion = Column(String(50), nullable=False)
    jornada = Column(String(20))
    equipo_local = Column(String(100), nullable=False)
    goles_equipo_local = Column(Integer)
    goles_equipo_visitante = Column(Integer)
    equipo_visitante = Column(String(100), nullable=False)
    arbitro = Column(String(100))
    asistentes = Column(Text)
    campo = Column(String(100))
    scrapeado = Column(Boolean, default=False)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow)

class Partido(Base):
    __tablename__ = 'partidos'
    
    id = Column(Integer, primary_key=True, index=True)
    calendario_id = Column(Integer, ForeignKey('calendario.id'))
    fecha = Column(Date, nullable=False)
    competicion = Column(String(50), nullable=False)
    jornada = Column(String(20))
    observaciones = Column(Text)
    
    # Relaciones
    eventos = relationship("EventoPartido", back_populates="partido")
    convocatorias = relationship("ConvocatoriaPartido", back_populates="partido")

class EventoPartido(Base):
    __tablename__ = 'eventos_partido'
    
    id = Column(Integer, primary_key=True, index=True)
    partido_id = Column(Integer, ForeignKey('partidos.id'))
    minuto = Column(Integer, nullable=False)
    jugador_id = Column(Integer, ForeignKey('jugadores.id'))
    tipo_evento = Column(String(50), nullable=False)  # gol, asistencia, tarjeta_amarilla, tarjeta_roja, etc.
    descripcion = Column(Text)
    
    partido = relationship("Partido", back_populates="eventos")
    jugador = relationship("Jugador")

class ConvocatoriaPartido(Base):
    __tablename__ = 'convocatorias_partido'
    
    id = Column(Integer, primary_key=True, index=True)
    partido_id = Column(Integer, ForeignKey('partidos.id'))
    jugador_id = Column(Integer, ForeignKey('jugadores.id'))
    estado = Column(String(20), nullable=False)  # titular, suplente, no_convocado
    minutos_jugados = Column(Integer, default=0)
    
    partido = relationship("Partido", back_populates="convocatorias")
    jugador = relationship("Jugador")

class Entrenamiento(Base):
    __tablename__ = 'entrenamientos'
    
    id = Column(Integer, primary_key=True, index=True)
    numero_entrenamiento = Column(Integer, unique=True, nullable=False)
    fecha = Column(Date, nullable=False)
    observaciones = Column(Text)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    asistencias = relationship("AsistenciaEntrenamiento", back_populates="entrenamiento")

class AsistenciaEntrenamiento(Base):
    __tablename__ = 'asistencia_entrenamientos'
    
    id = Column(Integer, primary_key=True, index=True)
    entrenamiento_id = Column(Integer, ForeignKey('entrenamientos.id'))
    jugador_id = Column(Integer, ForeignKey('jugadores.id'))
    entrena = Column(Boolean, default=True)
    razon_ausencia = Column(String(100))
    observaciones = Column(Text)
    
    entrenamiento = relationship("Entrenamiento", back_populates="asistencias")
    jugador = relationship("Jugador", back_populates="entrenamientos")

class ObjetivoIndividual(Base):
    __tablename__ = 'objetivos_individuales'
    
    id = Column(Integer, primary_key=True, index=True)
    jugador_id = Column(Integer, ForeignKey('jugadores.id'))
    objetivo = Column(String(200), nullable=False)
    descripcion = Column(Text)
    fecha_inicio = Column(Date, nullable=False)
    fecha_objetivo = Column(Date)
    completado = Column(Boolean, default=False)
    progreso = Column(Integer, default=0)  # Porcentaje de 0 a 100
    mes = Column(String(7))  # YYYY-MM
    
    jugador = relationship("Jugador")

class Puntuacion(Base):
    __tablename__ = 'puntuaciones'
    
    id = Column(Integer, primary_key=True, index=True)
    jugador_id = Column(Integer, ForeignKey('jugadores.id'))
    fecha = Column(Date, nullable=False)
    puntos = Column(Integer, nullable=False)
    concepto = Column(String(100))
    observaciones = Column(Text)
    
    jugador = relationship("Jugador", back_populates="puntuaciones")

class Multa(Base):
    __tablename__ = 'multas'
    
    id = Column(Integer, primary_key=True, index=True)
    jugador_id = Column(Integer, ForeignKey('jugadores.id'))
    fecha = Column(Date, nullable=False)
    razon_multa = Column(String(200), nullable=False)
    multa = Column(Float, nullable=False)  # Cantidad en euros
    pagado = Column(Float, default=0.0)
    debe = Column(Float, nullable=False)
    completamente_pagada = Column(Boolean, default=False)
    
    jugador = relationship("Jugador", back_populates="multas")
    pagos = relationship("PagoMulta", back_populates="multa")

class PagoMulta(Base):
    __tablename__ = 'pagos_multas'
    
    id = Column(Integer, primary_key=True, index=True)
    multa_id = Column(Integer, ForeignKey('multas.id'))
    fecha_pago = Column(Date, nullable=False)
    cantidad_pagada = Column(Float, nullable=False)
    observaciones = Column(Text)
    
    multa = relationship("Multa", back_populates="pagos")

# Funciones para gestionar la base de datos

def init_database():
    """Inicializa la base de datos y crea las tablas"""
    Base.metadata.create_all(bind=engine)
    
    # Crear usuario admin por defecto si no existe
    db = SessionLocal()
    try:
        existing_user = db.query(Usuario).filter(Usuario.username == 'admin').first()
        if not existing_user:
            import bcrypt
            hashed_password = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt())
            admin_user = Usuario(
                username='admin',
                password_hash=hashed_password.decode('utf-8'),
                email='admin@udatzeneta.com',
                nombre='Administrador'
            )
            db.add(admin_user)
            db.commit()
            print("Usuario admin creado con contraseña: admin123")
    except Exception as e:
        print(f"Error creando usuario admin: {e}")
        db.rollback()
    finally:
        db.close()

def get_db():
    """Obtiene una sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class DatabaseManager:
    """Clase para gestionar operaciones de base de datos"""
    
    def __init__(self):
        self.db = SessionLocal()
    
    def close(self):
        self.db.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    # Métodos para jugadores
    def get_jugadores(self, activos_solo=True):
        query = self.db.query(Jugador)
        if activos_solo:
            query = query.filter(Jugador.activo == True)
        return query.all()
    
    def get_jugador_by_id(self, jugador_id):
        return self.db.query(Jugador).filter(Jugador.id == jugador_id).first()
    
    def create_jugador(self, **kwargs):
        jugador = Jugador(**kwargs)
        self.db.add(jugador)
        self.db.commit()
        self.db.refresh(jugador)
        return jugador
    
    def update_jugador(self, jugador_id, **kwargs):
        jugador = self.get_jugador_by_id(jugador_id)
        if jugador:
            for key, value in kwargs.items():
                setattr(jugador, key, value)
            self.db.commit()
            self.db.refresh(jugador)
        return jugador
    
    # Métodos para calendario
    def get_calendario(self):
        return self.db.query(Calendario).order_by(Calendario.fecha.desc()).all()
    
    def create_evento_calendario(self, **kwargs):
        evento = Calendario(**kwargs)
        self.db.add(evento)
        self.db.commit()
        self.db.refresh(evento)
        return evento
    
    # Métodos para entrenamientos
    def get_entrenamientos(self):
        return self.db.query(Entrenamiento).order_by(Entrenamiento.fecha.desc()).all()
    
    def get_siguiente_numero_entrenamiento(self):
        ultimo = self.db.query(Entrenamiento).order_by(Entrenamiento.numero_entrenamiento.desc()).first()
        return (ultimo.numero_entrenamiento + 1) if ultimo else 1
    
    def create_entrenamiento(self, **kwargs):
        if 'numero_entrenamiento' not in kwargs:
            kwargs['numero_entrenamiento'] = self.get_siguiente_numero_entrenamiento()
        entrenamiento = Entrenamiento(**kwargs)
        self.db.add(entrenamiento)
        self.db.commit()
        self.db.refresh(entrenamiento)
        return entrenamiento
    
    # Métodos para multas
    def get_multas(self):
        return self.db.query(Multa).order_by(Multa.fecha.desc()).all()
    
    def get_multas_pendientes(self):
        return self.db.query(Multa).filter(Multa.completamente_pagada == False).all()
    
    def create_multa(self, **kwargs):
        kwargs['debe'] = kwargs.get('multa', 0) - kwargs.get('pagado', 0)
        kwargs['completamente_pagada'] = kwargs['debe'] <= 0
        multa = Multa(**kwargs)
        self.db.add(multa)
        self.db.commit()
        self.db.refresh(multa)
        return multa
    
    def pagar_multa(self, multa_id, cantidad_pagada, observaciones=""):
        multa = self.db.query(Multa).filter(Multa.id == multa_id).first()
        if multa:
            # Crear registro de pago
            pago = PagoMulta(
                multa_id=multa_id,
                fecha_pago=date.today(),
                cantidad_pagada=cantidad_pagada,
                observaciones=observaciones
            )
            self.db.add(pago)
            
            # Actualizar multa
            multa.pagado += cantidad_pagada
            multa.debe = multa.multa - multa.pagado
            multa.completamente_pagada = multa.debe <= 0
            
            self.db.commit()
            return multa
        return None