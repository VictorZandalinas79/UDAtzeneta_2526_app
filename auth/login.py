import dash_bootstrap_components as dbc
from dash import html, dcc
import bcrypt
from database.db_manager import DatabaseManager, Usuario
from config.settings import COLORS

def create_login_layout():
    """Crea el layout de la página de login"""
    return html.Div([
        html.Div([
            dbc.Container([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Div([
                                    html.Img(
                                        src="/assets/logo_ud_atzeneta.png",
                                        className="club-logo mx-auto d-block mb-4",
                                        style={'max-width': '120px'}
                                    ),
                                    html.H2(
                                        "UD Atzeneta",
                                        className="text-center mb-2",
                                        style={'color': COLORS['primary'], 'font-weight': 'bold'}
                                    ),
                                    html.P(
                                        "Sistema de Gestión del Equipo",
                                        className="text-center text-muted mb-4"
                                    ),
                                    
                                    # Formulario de login
                                    dbc.Form([
                                        dbc.Row([
                                            dbc.Col([
                                                dbc.Label("Usuario", html_for="username-input"),
                                                dbc.Input(
                                                    id="username-input",
                                                    type="text",
                                                    placeholder="Ingresa tu usuario",
                                                    className="mb-3"
                                                )
                                            ])
                                        ]),
                                        dbc.Row([
                                            dbc.Col([
                                                dbc.Label("Contraseña", html_for="password-input"),
                                                dbc.Input(
                                                    id="password-input",
                                                    type="password",
                                                    placeholder="Ingresa tu contraseña",
                                                    className="mb-3"
                                                )
                                            ])
                                        ]),
                                        dbc.Row([
                                            dbc.Col([
                                                dbc.Button(
                                                    [
                                                        html.I(className="fas fa-sign-in-alt me-2"),
                                                        "Iniciar Sesión"
                                                    ],
                                                    id="login-button",
                                                    color="primary",
                                                    className="w-100 mb-3",
                                                    size="lg"
                                                )
                                            ])
                                        ]),
                                        
                                        # Mensaje de error
                                        html.Div(id="login-error", className="text-center"),
                                        
                                        # Información de acceso por defecto
                                        dbc.Alert([
                                            html.H6("Acceso por defecto:", className="alert-heading"),
                                            html.P("Usuario: admin", className="mb-1"),
                                            html.P("Contraseña: admin123", className="mb-0")
                                        ], color="info", className="mt-3")
                                    ])
                                ])
                            ])
                        ], className="login-card shadow-lg")
                    ], width=12, md=6, lg=4, xl=3)
                ], justify="center", className="min-vh-100 align-items-center")
            ], fluid=True)
        ], className="login-container")
    ])

def verify_credentials(username, password):
    """Verifica las credenciales del usuario"""
    if not username or not password:
        return False
    
    try:
        with DatabaseManager() as db_manager:
            usuario = db_manager.db.query(Usuario).filter(
                Usuario.username == username,
                Usuario.activo == True
            ).first()
            
            if usuario:
                # Verificar contraseña
                if bcrypt.checkpw(password.encode('utf-8'), usuario.password_hash.encode('utf-8')):
                    return True
    except Exception as e:
        print(f"Error verificando credenciales: {e}")
    
    return False

def hash_password(password):
    """Genera hash de contraseña"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def create_user(username, password, email=None, nombre=None):
    """Crea un nuevo usuario"""
    try:
        with DatabaseManager() as db_manager:
            # Verificar si el usuario ya existe
            existing_user = db_manager.db.query(Usuario).filter(
                Usuario.username == username
            ).first()
            
            if existing_user:
                return False, "El usuario ya existe"
            
            # Crear nuevo usuario
            password_hash = hash_password(password)
            new_user = Usuario(
                username=username,
                password_hash=password_hash,
                email=email,
                nombre=nombre
            )
            
            db_manager.db.add(new_user)
            db_manager.db.commit()
            return True, "Usuario creado exitosamente"
            
    except Exception as e:
        return False, f"Error creando usuario: {str(e)}"