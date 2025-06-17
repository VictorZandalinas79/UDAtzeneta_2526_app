import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import os
from config.settings import EXTERNAL_STYLESHEETS, APP_CONFIG
from auth.login import create_login_layout, verify_credentials
from database.db_manager import init_database
from layouts.sidebar import create_sidebar
from layouts.main_content import create_main_content
from utils.session_manager import SessionManager

# Inicializar la aplicación Dash
app = dash.Dash(
    __name__,
    external_stylesheets=EXTERNAL_STYLESHEETS,
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ]
)

# Configuración del servidor
server = app.server
app.title = "UD Atzeneta - Gestión del Equipo"

# Inicializar base de datos
init_database()

# Gestor de sesiones
session_manager = SessionManager()

# Layout principal de la aplicación
app.layout = dbc.Container([
    dcc.Store(id='session-store', data={'authenticated': False, 'user': None}),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
], fluid=True, className='p-0')

@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname'),
    State('session-store', 'data')
)
def display_page(pathname, session_data):
    """Controla la navegación y autenticación"""
    if not session_data.get('authenticated', False):
        return create_login_layout()
    
    return html.Div([
        create_sidebar(),
        create_main_content()
    ], className='d-flex')

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
    if n_clicks and verify_credentials(username, password):
        return {'authenticated': True, 'user': username}, '/dashboard'
    return {'authenticated': False, 'user': None}, '/'

# Importar callbacks de otras páginas
from pages import (
    dashboard_callbacks,
    calendario_callbacks,
    jugadores_callbacks,
    partidos_callbacks,
    entrenamientos_callbacks,
    objetivos_callbacks,
    puntuacion_callbacks,
    multas_callbacks
)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    debug_mode = os.environ.get('DASH_DEBUG_MODE', 'True') == 'True'
    
    app.run_server(
        host='0.0.0.0',
        port=port,
        debug=debug_mode
    )