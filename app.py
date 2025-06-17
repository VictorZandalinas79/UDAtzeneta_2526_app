import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import os
from config.settings import EXTERNAL_STYLESHEETS, APP_CONFIG, NAVIGATION_PAGES
from auth.login import create_login_layout, verify_credentials
from database.db_manager import init_database
from utils.session_manager import SessionManager

# Importar los componentes necesarios
from layouts.main_content import create_top_bar, create_main_content
from layouts.sidebar import create_sidebar, get_sidebar_callbacks

# Inicializar la aplicación Dash
app = dash.Dash(
    __name__,
    external_stylesheets=EXTERNAL_STYLESHEETS,
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ]
)

# Configurar el servidor
server = app.server
app.title = "UD Atzeneta - Gestión del Equipo"

# Configuración de la plantilla HTML personalizada
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            /* Estilos base */
            body, html {
                margin: 0;
                padding: 0;
                height: 100%;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                background-color: #f8f9fa;
            }
            
            /* Asegurar que el contenido principal ocupe todo el espacio */
            #root, #react-entry-point, ._dash-loading, ._dash-loading-callback {
                height: 100%;
                min-height: 100vh;
            }
            
            /* 
            COMPORTAMIENTO DEL SIDEBAR (CORREGIDO):
            - Por defecto OCULTO en TODAS las pantallas (móviles, tablets, escritorio)
            - Solo visible cuando se hace clic en el botón toggle rojo
            - Se cierra automáticamente cuando:
              * Se hace clic en el botón toggle otra vez
              * Se hace clic en el overlay (fondo oscuro)
              * Se navega a otra página
            - El contenido principal NUNCA se mueve, solo aparece/desaparece el menú
            */
            
            /* Estilos para el sidebar deslizante - OCULTO POR DEFECTO */
            .sidebar {
                position: fixed !important;
                top: 0;
                left: -280px; /* Oculto por defecto en TODAS las pantallas */
                width: 280px;
                height: 100vh;
                background: linear-gradient(135deg, #1a1a1a 0%, #2c2c2c 100%) !important;
                color: white !important;
                transition: left 0.3s ease-in-out;
                z-index: 1050;
                overflow-y: auto;
                box-shadow: 2px 0 10px rgba(0, 0, 0, 0.3);
            }
            
            .sidebar.show {
                left: 0; /* Visible cuando tiene la clase show */
            }
            
            .sidebar .nav-link {
                color: white !important;
                margin: 5px 15px;
                border-radius: 8px;
                padding: 12px 16px !important;
                transition: all 0.3s ease;
                font-weight: 500;
                border: 1px solid transparent;
            }
            
            .sidebar .nav-link:hover, .sidebar .nav-link.active {
                background-color: #DC143C !important;
                color: white !important;
                border: 1px solid rgba(255, 255, 255, 0.2);
                transform: translateX(5px);
            }
            
            /* Estilos para los enlaces de navegación personalizados */
            .nav-link-custom {
                display: block !important;
                color: white !important;
                text-decoration: none !important;
                padding: 12px 20px !important;
                margin: 5px 15px !important;
                border-radius: 8px !important;
                transition: all 0.3s ease !important;
                font-weight: 500 !important;
                border: 1px solid transparent !important;
            }
            
            .nav-link-custom:hover {
                background-color: #DC143C !important;
                color: white !important;
                border: 1px solid rgba(255, 255, 255, 0.2) !important;
                transform: translateX(5px) !important;
                text-decoration: none !important;
            }
            
            .nav-link-custom:focus {
                color: white !important;
                text-decoration: none !important;
            }
            
            /* Asegurar que los enlaces funcionen correctamente */
            .nav-link-custom i {
                width: 20px;
                text-align: center;
                color: white !important;
            }
            
            /* Mejorar el espaciado en el sidebar */
            .sidebar .border-bottom {
                border-bottom: 1px solid #404040 !important;
            }
            
            /* Aplicar los mismos estilos a los NavLink de Dash Bootstrap */
            .sidebar .nav-link {
                color: white !important;
                margin: 5px 15px;
                border-radius: 8px;
                padding: 12px 16px !important;
                transition: all 0.3s ease;
                font-weight: 500;
                border: 1px solid transparent;
            }
            
            /* Overlay para cerrar el menú - FUNCIONA EN TODAS LAS PANTALLAS */
            .sidebar-overlay {
                position: fixed !important;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                background-color: rgba(0, 0, 0, 0.5);
                z-index: 1040;
                opacity: 0;
                visibility: hidden;
                transition: all 0.3s ease;
                cursor: pointer;
            }
            
            .sidebar-overlay.show {
                opacity: 1;
                visibility: visible;
            }
            
            /* Botón de toggle del menú - SIEMPRE VISIBLE */
            .menu-toggle-btn {
                position: fixed !important;
                top: 20px;
                left: 20px;
                z-index: 1060 !important;
                border-radius: 50%;
                width: 50px;
                height: 50px;
                display: flex !important;
                align-items: center;
                justify-content: center;
                background: linear-gradient(135deg, #DC143C 0%, #8B0000 100%);
                border: none;
                box-shadow: 0 4px 12px rgba(220, 20, 60, 0.3);
                transition: all 0.3s ease;
                cursor: pointer;
            }
            
            .menu-toggle-btn:hover {
                transform: scale(1.1);
                box-shadow: 0 6px 20px rgba(220, 20, 60, 0.5);
            }
            
            .menu-toggle-btn i {
                color: white !important;
                font-size: 18px;
            }
            
            .menu-toggle-btn.active {
                background: linear-gradient(135deg, #8B0000 0%, #DC143C 100%);
                transform: rotate(90deg);
            }
            
            .menu-toggle-btn.active:hover {
                transform: rotate(90deg) scale(1.1);
            }
            
            /* Estilos para el contenido principal - SIN MARGEN POR DEFECTO */
            .main-content {
                transition: all 0.3s ease;
                min-height: 100vh;
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                margin-left: 0 !important; /* Sin margen por defecto */
                padding-left: 80px; /* Espacio para el botón de toggle */
            }
            
            /* Para pantallas grandes - MISMO COMPORTAMIENTO DESLIZANTE */
            @media (min-width: 1201px) {
                .sidebar {
                    left: -280px !important; /* OCULTO por defecto incluso en desktop */
                }
                
                .sidebar.show {
                    left: 0 !important; /* Visible solo cuando se activa */
                }
                
                .main-content {
                    margin-left: 0 !important; /* Sin margen porque el sidebar está oculto */
                    padding-left: 80px !important; /* Solo espacio para el botón toggle */
                }
            }
            
            /* Responsive para móviles y tablets */
            @media (max-width: 1200px) {
                .menu-toggle-btn {
                    top: 15px;
                    left: 15px;
                    width: 45px;
                    height: 45px;
                }
                
                .main-content {
                    padding: 15px !important;
                    padding-top: 80px !important;
                    padding-left: 70px !important;
                }
            }
            
            /* Para móviles */
            @media (max-width: 768px) {
                .menu-toggle-btn {
                    top: 15px;
                    left: 15px;
                    width: 45px;
                    height: 45px;
                }
                
                .main-content {
                    padding: 15px !important;
                    padding-top: 80px !important;
                    padding-left: 70px !important;
                }
                
                .sidebar {
                    width: 280px;
                    left: -280px; /* Oculto en móviles también */
                }
                
                .sidebar.show {
                    left: 0;
                }
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Inicializar base de datos y verificar usuario admin
try:
    init_database()
    print("DEBUG: Database initialized successfully")
    
    # Verificar que el usuario admin existe
    from database.db_manager import DatabaseManager
    with DatabaseManager() as db:
        admin_user = db.db.query(db.Usuario).filter(db.Usuario.username == 'admin').first()
        if admin_user:
            print("DEBUG: Admin user exists in database")
        else:
            print("DEBUG: Admin user not found, creating...")
            from auth.login import hash_password
            admin_user = db.Usuario(
                username='admin',
                password_hash=hash_password('admin123'),
                nombre='Administrador',
                activo=True
            )
            db.db.add(admin_user)
            db.db.commit()
            print("DEBUG: Admin user created successfully")
            
except Exception as e:
    print(f"DEBUG: Database initialization error: {e}")

# Gestor de sesiones
session_manager = SessionManager()

# Layout principal de la aplicación
def serve_layout():
    # Para simplificar el debugging, empezar siempre con el login
    print("DEBUG: Serving layout - starting with login")
    
    try:
        return create_login_layout()
    except:
        return create_simple_login()

# Layout principal dinámico
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='session-store', data={'authenticated': False, 'user': None}),
    html.Div(id='app-content')
])

@app.callback(
    Output('app-content', 'children'),
    [Input('session-store', 'data')]
)
def update_app_content(session_data):
    """Actualiza el contenido principal según el estado de autenticación"""
    if session_data and session_data.get('authenticated', False):
        # Usuario autenticado - mostrar app principal
        return html.Div([
            # Botón para abrir/cerrar el menú
            dbc.Button(
                html.I(className="fas fa-bars"),
                id="menu-toggle-btn",
                className="menu-toggle-btn",
                n_clicks=0
            ),
            
            # Overlay para cerrar el menú
            html.Div(id="sidebar-overlay", className="sidebar-overlay"),
            
            # Sidebar deslizante (siempre usar la versión simple que funciona)
            create_simple_sidebar(),
            
            # Barra de navegación superior
            create_simple_topbar(),
            
            # Contenido principal
            html.Div(
                id='page-content',
                className='main-content',
                style={
                    'padding': '20px',
                    'paddingTop': '80px',
                    'paddingLeft': '80px',  # Espacio para el botón toggle
                    'minHeight': '100vh',
                    'transition': 'all 0.3s ease',
                    'backgroundColor': '#f8f9fa',
                    'marginLeft': '0'  # Sin margen por defecto
                }
            )
        ], style={'minHeight': '100vh'})
    else:
        # Usuario no autenticado - mostrar login
        try:
            return create_login_layout()
        except:
            return create_simple_login()

# Importar los módulos de páginas con manejo de errores
try:
    from pages import dashboard
except ImportError:
    dashboard = None

try:
    from pages import calendario
except ImportError:
    calendario = None

try:
    from pages import jugadores
except ImportError:
    jugadores = None

try:
    from pages import partidos
except ImportError:
    partidos = None

try:
    from pages import entrenamientos
except ImportError:
    entrenamientos = None

try:
    from pages import objetivos
except ImportError:
    objetivos = None

try:
    from pages import puntuacion
except ImportError:
    puntuacion = None

try:
    from pages import multas
except ImportError:
    multas = None

# Los callbacks del sidebar se registran directamente aquí en lugar de usar la función externa

# Callback para resaltar navegación deshabilitado temporalmente para evitar errores
# # Callback para validar inputs en tiempo real (comentado temporalmente para evitar errores)
# @app.callback(
#     [Output('username-input', 'valid'),
#      Output('username-input', 'invalid'),
#      Output('password-input', 'valid'),
#      Output('password-input', 'invalid')],
#     [Input('username-input', 'value'),
#      Input('password-input', 'value')],
#     prevent_initial_call=True
# )
# def validate_login_inputs(username, password):
#     """Valida los inputs del formulario de login"""
#     username_valid = username and len(username.strip()) > 0
#     password_valid = password and len(password.strip()) > 0
#     
#     return (
#         username_valid, not username_valid,
#         password_valid, not password_valid
#     )

# Callback para mostrar alertas de login (con verificación de existencia)
@app.callback(
    Output('login-alert', 'children'),
    [Input('login-button', 'n_clicks')],
    [State('username-input', 'value'),
     State('password-input', 'value')],
    prevent_initial_call=True
)
def show_login_alert(n_clicks, username, password):
    """Muestra alertas de error en el login"""
    try:
        if n_clicks:
            if not username or not password:
                return dbc.Alert(
                    "Por favor, introduce usuario y contraseña",
                    color="warning",
                    dismissable=True,
                    className="mb-3"
                )
            
            # Verificar credenciales hardcodeadas primero
            if username.strip() == 'admin' and password.strip() == 'admin123':
                return html.Div()  # No mostrar error si las credenciales son correctas
            
            try:
                is_valid = verify_credentials(username, password)
                if not is_valid:
                    return dbc.Alert([
                        html.Strong("Error de autenticación"),
                        html.Br(),
                        "Usuario o contraseña incorrectos",
                        html.Br(),
                        html.Small("Prueba con: admin / admin123")
                    ],
                    color="danger",
                    dismissable=True,
                    className="mb-3"
                    )
            except Exception as e:
                return dbc.Alert([
                    html.Strong("Error del sistema"),
                    html.Br(),
                    f"Error: {str(e)}",
                    html.Br(),
                    html.Small("Usando credenciales por defecto: admin / admin123")
                ],
                color="warning",
                dismissable=True,
                className="mb-3"
                )
        
        return html.Div()
    except:
        return html.Div()

# Callback para resaltar navegación - temporalmente deshabilitado
# @app.callback(
#     [Output(f"nav-{page['path'].replace('/', '')}", "className") for page in NAVIGATION_PAGES],
#     [Input("url", "pathname")],
#     prevent_initial_call=True
# )
# def highlight_active_nav(pathname):
#     """Resalta el enlace de navegación activo"""
#     return []
# Fin del callback comentado

@app.callback(
    [Output('sidebar', 'className'),
     Output('sidebar-overlay', 'className')],
    [Input('menu-toggle-btn', 'n_clicks'),
     Input('sidebar-overlay', 'n_clicks'),
     Input('url', 'pathname')],  # Agregar el cambio de URL para cerrar automáticamente
    [State('sidebar', 'className')],
    prevent_initial_call=True
)
def toggle_sidebar(toggle_clicks, overlay_clicks, pathname, current_class):
    """Controla la apertura y cierre del sidebar en TODAS las pantallas"""
    import dash
    
    ctx = dash.callback_context
    
    if not ctx.triggered:
        # Estado inicial: sidebar oculto
        return "sidebar", "sidebar-overlay"
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Si cambia la URL (navegación), cerrar el sidebar automáticamente
    if trigger_id == 'url':
        print(f"DEBUG: URL changed to {pathname}, closing sidebar")
        return "sidebar", "sidebar-overlay"
    
    # Si se hace clic en el overlay, SIEMPRE cerrar el sidebar
    if trigger_id == 'sidebar-overlay':
        print("DEBUG: Overlay clicked, closing sidebar")
        return "sidebar", "sidebar-overlay"
    
    # Si se hace clic en el botón de toggle, alternar el estado
    if trigger_id == 'menu-toggle-btn':
        # Verificar si el sidebar está actualmente visible
        is_open = current_class and 'show' in current_class
        
        if is_open:
            # Cerrar sidebar
            print("DEBUG: Toggle button clicked, closing sidebar")
            return "sidebar", "sidebar-overlay"
        else:
            # Abrir sidebar
            print("DEBUG: Toggle button clicked, opening sidebar")
            return "sidebar show", "sidebar-overlay show"
    
    # Estado por defecto: sidebar oculto
    return "sidebar", "sidebar-overlay"

@app.callback(
    Output('menu-toggle-btn', 'className'),
    [Input('sidebar', 'className')],
    prevent_initial_call=True
)
def update_toggle_button(sidebar_class):
    """Actualiza el estilo del botón según el estado del sidebar"""
    if sidebar_class and 'show' in sidebar_class:
        return "menu-toggle-btn active"
    return "menu-toggle-btn"

def create_simple_sidebar():
    """Crea un sidebar simple temporal"""
    return html.Div([
        # Header del sidebar
        html.Div([
            html.H5("UD Atzeneta", className="text-white text-center mb-1"),
            html.Small("Sistema de Gestión", className="text-white-50 text-center d-block")
        ], className="p-3 border-bottom", style={'border-bottom-color': '#404040'}),
        
        # Navegación con enlaces funcionales
        html.Div([
            dcc.Link([
                html.I(className="fas fa-tachometer-alt me-2"),
                "Dashboard"
            ], href="/dashboard", className="nav-link-custom"),
            
            dcc.Link([
                html.I(className="fas fa-calendar me-2"),
                "Calendario"
            ], href="/calendario", className="nav-link-custom"),
            
            dcc.Link([
                html.I(className="fas fa-users me-2"),
                "Jugadores"
            ], href="/jugadores", className="nav-link-custom"),
            
            dcc.Link([
                html.I(className="fas fa-futbol me-2"),
                "Partidos"
            ], href="/partidos", className="nav-link-custom"),
            
            dcc.Link([
                html.I(className="fas fa-running me-2"),
                "Entrenamientos"
            ], href="/entrenamientos", className="nav-link-custom"),
            
            dcc.Link([
                html.I(className="fas fa-target me-2"),
                "Objetivos"
            ], href="/objetivos", className="nav-link-custom"),
            
            dcc.Link([
                html.I(className="fas fa-star me-2"),
                "Puntuación"
            ], href="/puntuacion", className="nav-link-custom"),
            
            dcc.Link([
                html.I(className="fas fa-euro-sign me-2"),
                "Multas"
            ], href="/multas", className="nav-link-custom")
        ])
    ], 
    className="sidebar d-flex flex-column",
    id="sidebar"
    )

def create_simple_topbar():
    """Crea una barra superior simple"""
    return html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H6("UD Atzeneta - Sistema de Gestión", className="m-0 text-white d-none d-md-block")
                ], width=6),
                dbc.Col([
                    html.Div([
                        html.I(className="fas fa-user-circle me-2"),
                        html.Span("Entrenador", className="d-none d-md-inline"),
                        html.Span(" | "),
                        html.Span("2025-2026", className="d-none d-sm-inline")
                    ], className="text-end text-white")
                ], width=6)
            ], align="center")
        ], fluid=True)
    ], style={
        "background": "linear-gradient(135deg, #DC143C 0%, #8B0000 100%)",
        "position": "fixed",
        "top": "0",
        "left": "0",
        "right": "0",
        "zIndex": "1000",
        "height": "60px",
        "display": "flex",
        "alignItems": "center",
        "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"
    })

# Layouts simples temporales para evitar errores
def create_simple_layout(page_name):
    """Crea un layout simple temporal"""
    
    # Iconos para cada página
    page_icons = {
        "Dashboard": "fas fa-tachometer-alt",
        "Calendario": "fas fa-calendar",
        "Jugadores": "fas fa-users", 
        "Partidos": "fas fa-futbol",
        "Entrenamientos": "fas fa-running",
        "Objetivos": "fas fa-target",
        "Puntuación": "fas fa-star",
        "Multas": "fas fa-euro-sign"
    }
    
    # Descripciones para cada página
    page_descriptions = {
        "Dashboard": "Resumen general del equipo, estadísticas y próximos eventos",
        "Calendario": "Gestión de partidos, horarios y competiciones",
        "Jugadores": "Información completa de la plantilla del equipo",
        "Partidos": "Control de convocatorias, resultados y eventos",
        "Entrenamientos": "Registro de asistencia y planificación",
        "Objetivos": "Seguimiento del desarrollo individual de jugadores",
        "Puntuación": "Sistema de puntos y ranking del equipo",
        "Multas": "Control de sanciones económicas y pagos"
    }
    
    icon = page_icons.get(page_name, "fas fa-cogs")
    description = page_descriptions.get(page_name, f"Gestión de {page_name.lower()}")
    
    return html.Div([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.I(className=f"{icon} fa-4x text-primary mb-3"),
                            html.H2(f"{page_name}", className="text-center mb-3"),
                            html.P(description, className="text-center text-muted mb-4"),
                            
                            dbc.Alert([
                                html.H5("🚧 Sección en Desarrollo", className="alert-heading"),
                                html.P([
                                    f"La página {page_name} está siendo desarrollada. ",
                                    "Pronto estará disponible con todas sus funcionalidades:"
                                ]),
                                html.Ul([
                                    html.Li("Interfaz completa y funcional"),
                                    html.Li("Gestión de datos en tiempo real"),
                                    html.Li("Estadísticas y gráficos interactivos"),
                                    html.Li("Exportación de datos"),
                                    html.Li("Notificaciones automáticas")
                                ], className="mb-3"),
                                html.Hr(),
                                html.P([
                                    "Mientras tanto, puedes navegar por otras secciones usando el menú ",
                                    html.I(className="fas fa-bars text-danger"),
                                    " en la esquina superior izquierda."
                                ], className="mb-0")
                            ], color="info")
                        ], className="text-center")
                    ])
                ], className="shadow-sm")
            ], width=12, lg=8)
        ], justify="center"),
        
        # Información adicional
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H6([
                            html.I(className="fas fa-info-circle me-2"),
                            "Estado del Desarrollo"
                        ], className="mb-0")
                    ]),
                    dbc.CardBody([
                        html.P("🔄 En progreso", className="mb-2"),
                        html.P("📅 Próximamente disponible", className="mb-2"),
                        html.P("✅ Navegación funcional", className="mb-0")
                    ])
                ], className="shadow-sm")
            ], width=12, lg=4)
        ], justify="center", className="mt-4")
    ])

def create_simple_login():
    """Crea un login simple si hay problemas con el principal"""
    return html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            html.H3("🔐 UD Atzeneta", className="text-center mb-0 text-white"),
                            html.P("Sistema de Gestión del Equipo", className="text-center mb-0 text-light")
                        ], style={'background': 'linear-gradient(135deg, #DC143C 0%, #8B0000 100%)'}),
                        dbc.CardBody([
                            html.Div(id="login-alert"),  # Para mostrar errores
                            dbc.Form([
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Label("Usuario", style={'color': '#212529', 'font-weight': '600'}),
                                        dbc.Input(
                                            id="username-input",
                                            type="text",
                                            placeholder="Introduce tu usuario",
                                            value="",
                                            style={'border': '2px solid #dee2e6'}
                                        ),
                                        html.Small("Usuario por defecto: admin", className="text-muted")
                                    ], width=12)
                                ], className="mb-3"),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Label("Contraseña", style={'color': '#212529', 'font-weight': '600'}),
                                        dbc.Input(
                                            id="password-input",
                                            type="password",
                                            placeholder="Introduce tu contraseña",
                                            value="",
                                            style={'border': '2px solid #dee2e6'}
                                        ),
                                        html.Small("Contraseña por defecto: admin123", className="text-muted")
                                    ], width=12)
                                ], className="mb-4"),
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Button([
                                            html.I(className="fas fa-sign-in-alt me-2"),
                                            "Iniciar Sesión"
                                        ],
                                            id="login-button",
                                            color="primary",
                                            className="w-100",
                                            style={
                                                'background': 'linear-gradient(135deg, #DC143C 0%, #8B0000 100%)',
                                                'border': 'none',
                                                'font-weight': '500'
                                            }
                                        )
                                    ], width=12)
                                ])
                            ]),
                            html.Hr(className="my-4"),
                            html.Div([
                                html.H6("Credenciales de prueba:", className="mb-2"),
                                html.P([
                                    html.Strong("Usuario: "), "admin", html.Br(),
                                    html.Strong("Contraseña: "), "admin123"
                                ], className="mb-0 text-muted small")
                            ], className="text-center")
                        ])
                    ], className="shadow-lg")
                ], width=12, md=6, lg=4)
            ], justify="center", className="min-vh-100 align-items-center")
        ], fluid=True, style={'background': 'linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)'})
    ])

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')],
    [State('session-store', 'data')]
)
def display_page(pathname, session_data):
    """Controla la navegación y autenticación"""
    print(f"DEBUG: Navigating to: {pathname}")
    
    if not session_data or not session_data.get('authenticated', False):
        print("DEBUG: User not authenticated, showing login")
        try:
            return create_login_layout()
        except:
            return create_simple_login()
    
    # Manejar la ruta actual
    if pathname == '/' or pathname is None:
        pathname = '/dashboard'
        print("DEBUG: Redirecting to dashboard")
    
    # Títulos de las páginas
    title_mapping = {
        '/dashboard': 'Dashboard',
        '/calendario': 'Calendario',
        '/jugadores': 'Jugadores',
        '/partidos': 'Partidos',
        '/entrenamientos': 'Entrenamientos',
        '/objetivos': 'Objetivos',
        '/puntuacion': 'Puntuación',
        '/multas': 'Multas'
    }
    
    # Obtener el título
    title = title_mapping.get(pathname, 'Dashboard')
    print(f"DEBUG: Page title: {title}")
    
    # Por ahora, usar layouts simples
    try:
        # Intentar cargar el layout específico
        if pathname == '/dashboard':
            if dashboard and hasattr(dashboard, 'create_dashboard_layout'):
                try:
                    layout = dashboard.create_dashboard_layout()
                except:
                    layout = create_simple_layout("Dashboard")
            else:
                layout = create_simple_layout("Dashboard")
        elif pathname == '/calendario':
            if calendario and hasattr(calendario, 'create_calendario_layout'):
                try:
                    layout = calendario.create_calendario_layout()
                except:
                    layout = create_simple_layout("Calendario")
            else:
                layout = create_simple_layout("Calendario")
        elif pathname == '/jugadores':
            if jugadores and hasattr(jugadores, 'create_jugadores_layout'):
                try:
                    layout = jugadores.create_jugadores_layout()
                except:
                    layout = create_simple_layout("Jugadores")
            else:
                layout = create_simple_layout("Jugadores")
        elif pathname == '/partidos':
            if partidos and hasattr(partidos, 'create_partidos_layout'):
                try:
                    layout = partidos.create_partidos_layout()
                except:
                    layout = create_simple_layout("Partidos")
            else:
                layout = create_simple_layout("Partidos")
        elif pathname == '/entrenamientos':
            if entrenamientos and hasattr(entrenamientos, 'create_entrenamientos_layout'):
                try:
                    layout = entrenamientos.create_entrenamientos_layout()
                except:
                    layout = create_simple_layout("Entrenamientos")
            else:
                layout = create_simple_layout("Entrenamientos")
        elif pathname == '/objetivos':
            if objetivos and hasattr(objetivos, 'create_objetivos_layout'):
                try:
                    layout = objetivos.create_objetivos_layout()
                except:
                    layout = create_simple_layout("Objetivos")
            else:
                layout = create_simple_layout("Objetivos")
        elif pathname == '/puntuacion':
            if puntuacion and hasattr(puntuacion, 'create_puntuacion_layout'):
                try:
                    layout = puntuacion.create_puntuacion_layout()
                except:
                    layout = create_simple_layout("Puntuación")
            else:
                layout = create_simple_layout("Puntuación")
        elif pathname == '/multas':
            if multas and hasattr(multas, 'create_multas_layout'):
                try:
                    layout = multas.create_multas_layout()
                except:
                    layout = create_simple_layout("Multas")
            else:
                layout = create_simple_layout("Multas")
        else:
            layout = create_simple_layout("Dashboard")
            
    except Exception as e:
        print(f"DEBUG: Error loading layout: {e}")
        # Si hay cualquier error, mostrar un layout de error
        layout = html.Div([
            dbc.Alert([
                html.H4("⚠️ Error de Carga", className="alert-heading"),
                html.P(f"Error cargando la página: {str(e)}"),
                html.Hr(),
                html.P("La aplicación está en desarrollo. Por favor, inténtalo de nuevo.", className="mb-0")
            ], color="warning")
        ])
    
    # Retornar el contenido de la página
    return html.Div([
        html.Div(className='container-fluid py-3', children=[
            dbc.Row([
                dbc.Col([
                    html.H3([
                        html.I(className=get_page_icon(pathname), style={'marginRight': '10px'}),
                        title
                    ], className='mb-4', style={'color': '#212529', 'font-weight': '600'}),
                    layout
                ])
            ])
        ])
    ])

def get_page_icon(pathname):
    """Obtiene el icono correspondiente a cada página"""
    icons = {
        '/dashboard': 'fas fa-tachometer-alt',
        '/calendario': 'fas fa-calendar',
        '/jugadores': 'fas fa-users',
        '/partidos': 'fas fa-futbol',
        '/entrenamientos': 'fas fa-running',
        '/objetivos': 'fas fa-target',
        '/puntuacion': 'fas fa-star',
        '/multas': 'fas fa-euro-sign'
    }
    return icons.get(pathname, 'fas fa-home')

@app.callback(
    [Output('session-store', 'data'),
     Output('url', 'pathname')],
    [Input('login-button', 'n_clicks')],
    [State('username-input', 'value'),
     State('password-input', 'value')],
    prevent_initial_call=True
)
def handle_login(n_clicks, username, password):
    """Maneja el proceso de login"""
    print(f"DEBUG: Login attempt - clicks: {n_clicks}, username: '{username}', password: '{password}'")
    
    if n_clicks and username and password:
        # Primero probamos con credenciales hardcodeadas para debuggear
        if username.strip() == 'admin' and password.strip() == 'admin123':
            print("DEBUG: Hardcoded credentials match - allowing login")
            return {'authenticated': True, 'user': username}, '/dashboard'
        
        try:
            # Luego probamos con la base de datos
            is_valid = verify_credentials(username, password)
            print(f"DEBUG: Database credentials valid: {is_valid}")
            
            if is_valid:
                print(f"DEBUG: Login successful for {username}")
                return {'authenticated': True, 'user': username}, '/dashboard'
            else:
                print(f"DEBUG: Login failed for {username}")
                return {'authenticated': False, 'user': None}, '/'
        except Exception as e:
            print(f"DEBUG: Login error: {e}")
            # Si hay error con la base de datos, usar credenciales hardcodeadas
            if username.strip() == 'admin' and password.strip() == 'admin123':
                print("DEBUG: Fallback to hardcoded credentials")
                return {'authenticated': True, 'user': username}, '/dashboard'
            return {'authenticated': False, 'user': None}, '/'
    
    print("DEBUG: Login attempt failed - missing data or no clicks")
    return {'authenticated': False, 'user': None}, '/'

# Callback para el botón de logout
@app.callback(
    Output('url', 'refresh'),
    [Input('logout-button', 'n_clicks')],
    prevent_initial_call=True
)
def handle_logout(n_clicks):
    """Maneja el cierre de sesión"""
    if n_clicks:
        # Limpiar la sesión
        session_manager.clear_all_sessions()
        return True
    return False

# Los imports de pages ya están arriba y se cargan con manejo de errores
# Los callbacks se registran automáticamente al importar los módulos

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    debug_mode = os.environ.get('DASH_DEBUG_MODE', 'True') == 'True'
    
    app.run_server(
        host='0.0.0.0',
        port=port,
        debug=debug_mode
    )