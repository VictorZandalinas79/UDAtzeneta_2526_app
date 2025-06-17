import dash_bootstrap_components as dbc
from dash import html, dcc
from config.settings import NAVIGATION_PAGES, COLORS, APP_CONFIG

def create_sidebar():
    """Crea la barra lateral de navegación con diseño moderno"""
    return html.Div([
        # Header del sidebar con logo y nombre
        html.Div([
            # Logo
            html.Div(
                html.Img(
                    src="/assets/escudo.png",
                    style={
                        'width': '50px',
                        'height': '50px',
                        'objectFit': 'contain'
                    }
                ),
                style={
                    'background': 'white',
                    'padding': '5px',
                    'borderRadius': '50%',
                    'boxShadow': '0 4px 8px rgba(0,0,0,0.2)'
                }
            ),
            
            # Título y temporada
            html.Div([
                html.H4(
                    APP_CONFIG['club_name'],
                    className="mb-0",
                    style={
                        'color': 'white',
                        'fontWeight': '700',
                        'fontSize': '1.2rem',
                        'letterSpacing': '0.5px',
                        'marginBottom': '2px'
                    }
                ),
                html.Span(
                    f"Temporada {APP_CONFIG['season']}",
                    style={
                        'color': 'rgba(255,255,255,0.8)',
                        'fontSize': '0.8rem',
                        'fontWeight': '400'
                    }
                )
            ], style={'marginLeft': '15px'})
        ], 
        className="d-flex align-items-center p-4",
        style={
            'background': 'linear-gradient(135deg, #8B0000 0%, #DC143C 100%)',
            'borderBottom': '1px solid rgba(255,255,255,0.1)'
        }),
        
        # Menú de navegación
        html.Div([
            # Enlaces de navegación
            *[
                html.Div(
                    dcc.Link([
                        html.Div(
                            className="nav-icon",
                            children=html.I(
                                className=page['icon'],
                                style={
                                    'display': 'flex',
                                    'alignItems': 'center',
                                    'justifyContent': 'center',
                                    'width': '100%',
                                    'height': '100%',
                                    'fontSize': '1rem'
                                }
                            )
                        ),
                        html.Span(
                            page['name'],
                            className="nav-text"
                        ),
                        html.I(
                            className="fas fa-chevron-right arrow-icon",
                            style={'marginLeft': 'auto'}
                        )
                    ], 
                    href=page['path'],
                    id=f"nav-{page['path'].replace('/', '')}",
                    className="nav-link"
                    ),
                    className="nav-item"
                ) for page in NAVIGATION_PAGES
            ],
            
            # Separador
            html.Hr(style={
                'borderColor': 'rgba(255,255,255,0.1)',
                'margin': '15px 20px'
            }),
            
            # Perfil del usuario
            html.Div([
                html.Div(
                    html.I(className="fas fa-user-circle", style={'fontSize': '1.5rem'}),
                    className="nav-icon"
                ),
                html.Div([
                    html.Div("Entrenador", className="nav-text"),
                    html.Small(
                        "Administrador",
                        style={
                            'color': 'rgba(255,255,255,0.6)',
                            'fontSize': '0.75rem',
                            'display': 'block',
                            'marginTop': '2px'
                        }
                    )
                ], style={'flex': 1, 'marginLeft': '15px'}),
                
                # Botón de logout
                dbc.Button(
                    html.I(className="fas fa-sign-out-alt"),
                    id="logout-button",
                    color="link",
                    className="p-0",
                    style={
                        'color': 'rgba(255,255,255,0.7)',
                        'fontSize': '1.1rem',
                        'transition': 'all 0.3s',
                        'marginLeft': '10px'
                    },
                    title="Cerrar sesión"
                )
            ], 
            className="nav-item",
            style={
                'display': 'flex',
                'alignItems': 'center',
                'padding': '10px 15px',
                'margin': '5px 10px',
                'borderRadius': '8px',
                'transition': 'all 0.3s',
                'cursor': 'pointer',
                'border': '1px solid transparent'
            })
        ], 
        className="nav-menu",
        style={
            'flex': 1,
            'overflowY': 'auto',
            'padding': '15px 0',
            'marginBottom': '15px'
        })
    ], 
    className="sidebar d-flex flex-column",
    style={
        'width': '280px',
        'height': '100vh',
        'position': 'fixed',
        'left': '0',
        'top': '0',
        'zIndex': '1000',
        'background': '#1a1a2e',
        'boxShadow': '4px 0 20px rgba(0, 0, 0, 0.2)',
        'overflow': 'hidden',
        'transition': 'all 0.3s ease'
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