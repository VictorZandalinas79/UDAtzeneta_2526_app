import dash_bootstrap_components as dbc
from dash import html, dcc
from config.settings import NAVIGATION_PAGES, COLORS, APP_CONFIG

def create_sidebar():
    """Crea la barra lateral de navegación"""
    return html.Div([
        # Header del sidebar
        html.Div([
            html.Img(
                src="/assets/logo_ud_atzeneta.png",
                style={
                    'width': '60px',
                    'height': '60px',
                    'margin-right': '15px'
                }
            ),
            html.Div([
                html.H4(
                    APP_CONFIG['club_name'],
                    className="mb-0",
                    style={'color': COLORS['light'], 'font-weight': 'bold'}
                ),
                html.Small(
                    f"Temporada {APP_CONFIG['season']}",
                    style={'color': COLORS['gray_light']}
                )
            ])
        ], className="d-flex align-items-center p-3 border-bottom border-secondary"),
        
        # Navegación principal
        dbc.Nav([
            dbc.NavLink([
                html.I(className=f"{page['icon']} me-3"),
                page['name']
            ], 
            href=page['path'],
            id=f"nav-{page['path'].replace('/', '')}",
            className="nav-link text-light",
            style={'padding': '12px 20px'}
            ) for page in NAVIGATION_PAGES
        ], 
        vertical=True,
        pills=True,
        className="pt-3"
        ),
        
        # Información adicional en la parte inferior
        html.Div([
            html.Hr(style={'border-color': COLORS['gray_medium']}),
            html.Div([
                html.I(className="fas fa-user-circle me-2"),
                html.Span("Entrenador", style={'color': COLORS['light']})
            ], className="mb-2"),
            html.Div([
                html.I(className="fas fa-calendar me-2"),
                html.Span("2024-2025", style={'color': COLORS['gray_light']})
            ], className="mb-2"),
            
            # Botón de logout
            dbc.Button([
                html.I(className="fas fa-sign-out-alt me-2"),
                "Cerrar Sesión"
            ],
            id="logout-button",
            color="outline-light",
            size="sm",
            className="w-100 mt-3"
            )
        ], className="p-3 mt-auto")
        
    ], 
    className="sidebar d-flex flex-column",
    style={
        'width': '280px',
        'min-height': '100vh',
        'position': 'fixed',
        'left': '0',
        'top': '0',
        'z-index': '1000'
    },
    id="sidebar"
    )

def create_mobile_navbar():
    """Crea la barra de navegación para móviles"""
    return dbc.Navbar([
        dbc.Container([
            # Botón toggle para móvil
            dbc.Button(
                html.I(className="fas fa-bars"),
                id="mobile-nav-toggle",
                color="primary",
                className="d-md-none",
                outline=True
            ),
            
            # Logo y título
            dbc.NavbarBrand([
                html.Img(
                    src="/assets/logo_ud_atzeneta.png",
                    height="40px",
                    className="me-2"
                ),
                APP_CONFIG['club_name']
            ], className="ms-2"),
            
            # Menú colapsable para móvil
            dbc.Collapse([
                dbc.Nav([
                    dbc.NavItem(dbc.NavLink(
                        [html.I(className=f"{page['icon']} me-2"), page['name']],
                        href=page['path']
                    )) for page in NAVIGATION_PAGES
                ], className="ms-auto", navbar=True)
            ], id="mobile-navbar-collapse", navbar=True)
        ], fluid=True)
    ], 
    color="dark",
    dark=True,
    className="d-md-none",
    style={'z-index': '1030'}
    )

def get_sidebar_callbacks():
    """Retorna los callbacks necesarios para el sidebar"""
    from dash import Input, Output, State, callback
    
    @callback(
        Output("mobile-navbar-collapse", "is_open"),
        [Input("mobile-nav-toggle", "n_clicks")],
        [State("mobile-navbar-collapse", "is_open")],
    )
    def toggle_mobile_navbar(n_clicks, is_open):
        if n_clicks:
            return not is_open
        return is_open
    
    @callback(
        [Output("sidebar", "className"),
         Output("main-content-container", "style")],
        [Input("mobile-nav-toggle", "n_clicks")],
        [State("sidebar", "className")],
    )
    def toggle_sidebar_mobile(n_clicks, current_class):
        if n_clicks:
            if "show" in current_class:
                return "sidebar d-flex flex-column", {"margin-left": "0"}
            else:
                return "sidebar d-flex flex-column show", {"margin-left": "280px"}
        return current_class, {"margin-left": "280px"}

# Función para resaltar la página activa
def highlight_active_nav(pathname):
    """Resalta el enlace de navegación activo"""
    active_styles = {}
    for page in NAVIGATION_PAGES:
        nav_id = f"nav-{page['path'].replace('/', '')}"
        if pathname == page['path']:
            active_styles[nav_id] = {
                'background-color': COLORS['primary'],
                'color': COLORS['light'],
                'border-radius': '10px'
            }
        else:
            active_styles[nav_id] = {}
    return active_styles