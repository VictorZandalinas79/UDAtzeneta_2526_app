# Paquete de páginas para UD Atzeneta
# Contiene todas las páginas de la aplicación y sus callbacks

from . import (
    dashboard,
    calendario,
    jugadores,
    partidos,
    entrenamientos,
    objetivos,
    puntuacion,
    multas
)

# Registrar todos los callbacks al importar
dashboard_callbacks = dashboard
calendario_callbacks = calendario
jugadores_callbacks = jugadores
partidos_callbacks = partidos
entrenamientos_callbacks = entrenamientos
objetivos_callbacks = objetivos
puntuacion_callbacks = puntuacion
multas_callbacks = multas

__all__ = [
    'dashboard',
    'calendario',
    'jugadores', 
    'partidos',
    'entrenamientos',
    'objetivos',
    'puntuacion',
    'multas',
    'dashboard_callbacks',
    'calendario_callbacks',
    'jugadores_callbacks',
    'partidos_callbacks',
    'entrenamientos_callbacks',
    'objetivos_callbacks',
    'puntuacion_callbacks',
    'multas_callbacks'
]