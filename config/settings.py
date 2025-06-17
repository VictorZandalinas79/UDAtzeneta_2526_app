import dash_bootstrap_components as dbc

# Configuración de colores del club UD Atzeneta
COLORS = {
    'primary': '#DC143C',      # Rojo intenso
    'secondary': '#8B0000',    # Rojo oscuro
    'dark': '#000000',         # Negro
    'light': '#FFFFFF',        # Blanco
    'gray_light': '#F8F9FA',   # Gris claro
    'gray_medium': '#6C757D',  # Gris medio
    'success': '#28A745',      # Verde éxito
    'warning': '#FFC107',      # Amarillo advertencia
    'danger': '#DC3545',       # Rojo peligro
    'info': '#17A2B8'          # Azul información
}

# Estilos CSS personalizados
CUSTOM_CSS = f"""
.navbar-brand {{
    font-weight: bold;
    color: {COLORS['light']} !important;
}}

.sidebar {{
    background: linear-gradient(135deg, {COLORS['dark']} 0%, {COLORS['secondary']} 100%);
    min-height: 100vh;
    box-shadow: 2px 0 5px rgba(0,0,0,0.1);
}}

.sidebar .nav-link {{
    color: {COLORS['light']} !important;
    border-radius: 10px;
    margin: 5px 15px;
    transition: all 0.3s ease;
}}

.sidebar .nav-link:hover {{
    background-color: {COLORS['primary']} !important;
    color: {COLORS['light']} !important;
    transform: translateX(5px);
}}

.sidebar .nav-link.active {{
    background-color: {COLORS['primary']} !important;
    color: {COLORS['light']} !important;
}}

.main-content {{
    background-color: {COLORS['gray_light']};
    min-height: 100vh;
}}

.card {{
    border: none;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
}}

.card:hover {{
    transform: translateY(-5px);
}}

.card-header {{
    background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
    color: {COLORS['light']};
    border-radius: 15px 15px 0 0 !important;
    font-weight: bold;
}}

.btn-primary {{
    background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
    border: none;
    border-radius: 10px;
    transition: all 0.3s ease;
}}

.btn-primary:hover {{
    background: linear-gradient(135deg, {COLORS['secondary']} 0%, {COLORS['dark']} 100%);
    transform: scale(1.05);
}}

.table-hover tbody tr:hover {{
    background-color: rgba(220, 20, 60, 0.1);
}}

.login-container {{
    background: linear-gradient(135deg, {COLORS['dark']} 0%, {COLORS['secondary']} 50%, {COLORS['primary']} 100%);
    min-height: 100vh;
}}

.login-card {{
    backdrop-filter: blur(10px);
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
}}

.club-logo {{
    max-width: 150px;
    height: auto;
}}

.stat-card {{
    background: linear-gradient(135deg, {COLORS['light']} 0%, {COLORS['gray_light']} 100%);
    border-left: 5px solid {COLORS['primary']};
}}

.dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner table {{
    border-collapse: separate;
    border-spacing: 0;
}}

.dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner table th {{
    background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
    color: {COLORS['light']};
    font-weight: bold;
}}

.dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner table td {{
    border-bottom: 1px solid {COLORS['gray_light']};
}}

.form-control:focus {{
    border-color: {COLORS['primary']};
    box-shadow: 0 0 0 0.2rem rgba(220, 20, 60, 0.25);
}}

.navbar {{
    background: linear-gradient(135deg, {COLORS['dark']} 0%, {COLORS['secondary']} 100%);
}}

.progress-bar {{
    background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
}}

@media (max-width: 768px) {{
    .sidebar {{
        transform: translateX(-100%);
        transition: transform 0.3s ease;
    }}
    
    .sidebar.show {{
        transform: translateX(0);
    }}
}}
"""

# Hojas de estilo externas
EXTERNAL_STYLESHEETS = [
    dbc.themes.BOOTSTRAP,
    'https://use.fontawesome.com/releases/v6.4.0/css/all.css',
    {
        'href': 'data:text/css;charset=utf-8,' + CUSTOM_CSS.replace('\n', '').replace(' ', '%20'),
        'rel': 'stylesheet'
    }
]

# Configuración de la aplicación
APP_CONFIG = {
    'club_name': 'UD Atzeneta',
    'season': '2024-2025',
    'database_url': 'sqlite:///ud_atzeneta.db',
    'secret_key': 'ud-atzeneta-secret-key-2024',
    'session_timeout': 3600,  # 1 hora en segundos
}

# Configuración de scraping
SCRAPING_CONFIG = {
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'timeout': 30,
    'retry_attempts': 3,
    'delay_between_requests': 1
}

# Configuración de las páginas de navegación
NAVIGATION_PAGES = [
    {'name': 'Dashboard', 'path': '/dashboard', 'icon': 'fas fa-home'},
    {'name': 'Calendario', 'path': '/calendario', 'icon': 'fas fa-calendar-alt'},
    {'name': 'Jugadores', 'path': '/jugadores', 'icon': 'fas fa-users'},
    {'name': 'Partidos', 'path': '/partidos', 'icon': 'fas fa-futbol'},
    {'name': 'Entrenamientos', 'path': '/entrenamientos', 'icon': 'fas fa-running'},
    {'name': 'Objetivos', 'path': '/objetivos', 'icon': 'fas fa-target'},
    {'name': 'Puntuación', 'path': '/puntuacion', 'icon': 'fas fa-star'},
    {'name': 'Multas', 'path': '/multas', 'icon': 'fas fa-euro-sign'},
]

# Posiciones de jugadores
POSICIONES = [
    'Portero',
    'Lateral Derecho',
    'Lateral Izquierdo',
    'Central',
    'Mediocentro',
    'Interior',
    'Mediapunta',
    'Extremo Derecho',
    'Extremo Izquierdo',
    'Delantero'
]

# Tipos de competición
COMPETICIONES = [
    'Amistoso',
    'Liga',
    'Copa'
]

# Razones de ausencia en entrenamientos
RAZONES_AUSENCIA = [
    'Lesión',
    'Enfermedad',
    'Trabajo',
    'Estudios',
    'Personal',
    'Sin avisar',
    'Otros'
]