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
    background: linear-gradient(135deg, #1a1a1a 0%, #2c2c2c 100%);
    min-height: 100vh;
    box-shadow: 2px 0 5px rgba(0,0,0,0.3);
    border-right: 1px solid #333;
}}

.sidebar .nav-link {{
    color: #ffffff !important;
    border-radius: 10px;
    margin: 5px 15px;
    padding: 12px 16px !important;
    transition: all 0.3s ease;
    font-weight: 500;
    border: 1px solid transparent;
}}

.sidebar .nav-link:hover {{
    background-color: {COLORS['primary']} !important;
    color: #ffffff !important;
    transform: translateX(5px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 2px 8px rgba(220, 20, 60, 0.3);
}}

.sidebar .nav-link.active {{
    background-color: {COLORS['primary']} !important;
    color: #ffffff !important;
    border: 1px solid rgba(255, 255, 255, 0.3);
    box-shadow: 0 2px 12px rgba(220, 20, 60, 0.4);
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
    color: #ffffff !important;
    border-radius: 15px 15px 0 0 !important;
    font-weight: 600;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
    border-bottom: 2px solid rgba(255, 255, 255, 0.1);
}}

.btn-primary {{
    background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
    border: none;
    border-radius: 10px;
    transition: all 0.3s ease;
    color: #ffffff !important;
    font-weight: 500;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}}

.btn-primary:hover {{
    background: linear-gradient(135deg, {COLORS['secondary']} 0%, {COLORS['dark']} 100%);
    transform: scale(1.05);
    color: #ffffff !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}}

.table-hover tbody tr:hover {{
    background-color: rgba(220, 20, 60, 0.1);
}}

.login-container {{
    background: linear-gradient(135deg, #1a1a1a 0%, {COLORS['secondary']} 50%, {COLORS['primary']} 100%);
    min-height: 100vh;
}}

.login-card {{
    backdrop-filter: blur(10px);
    background: rgba(255, 255, 255, 0.98);
    border-radius: 20px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.2);
}}

/* Mejorar contraste en formularios */
.form-label {{
    color: #212529 !important;
    font-weight: 600;
}}

.form-control {{
    border: 2px solid #dee2e6;
    color: #212529;
    background-color: #ffffff;
}}

.form-control::placeholder {{
    color: #6c757d;
}}

/* Mejorar badges y alertas */
.badge {{
    font-weight: 600;
    letter-spacing: 0.5px;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
}}

.alert {{
    border: none;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}}

.alert-info {{
    background-color: rgba(23, 162, 184, 0.15);
    border-left: 4px solid #17a2b8;
    color: #0c5460;
}}

.alert-success {{
    background-color: rgba(40, 167, 69, 0.15);
    border-left: 4px solid #28a745;
    color: #155724;
}}

.alert-warning {{
    background-color: rgba(255, 193, 7, 0.15);
    border-left: 4px solid #ffc107;
    color: #856404;
}}

.alert-danger {{
    background-color: rgba(220, 53, 69, 0.15);
    border-left: 4px solid #dc3545;
    color: #721c24;
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
    color: #ffffff !important;
    font-weight: 600;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
    border-bottom: 2px solid rgba(255, 255, 255, 0.2);
}}

.dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner table td {{
    border-bottom: 1px solid #dee2e6;
    color: #212529;
    background-color: #ffffff;
}}

.dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner table tr:nth-child(even) td {{
    background-color: #f8f9fa;
}}

.dash-table-container .dash-spreadsheet-container .dash-spreadsheet-inner table tr:hover td {{
    background-color: rgba(220, 20, 60, 0.1) !important;
    color: #212529 !important;
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
    {'name': 'Objetivos', 'path': '/objetivos', 'icon': 'fas fa-eye'},
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