import dash_bootstrap_components as dbc
from dash import html, dcc
from config.settings import COLORS

def create_main_content():
    """Crea el contenedor principal para el contenido dinámico"""
    return html.Div([
        # Barra superior con información contextual
        create_top_bar(),
        
        # Contenido principal dinámico
        html.Div(id="dynamic-content", className="p-4")
        
    ], 
    className="main-content flex-grow-1",
    style={'margin-left': '280px'},  # Espacio para el sidebar
    id="main-content-container"
    )

def create_top_bar():
    """Crea la barra superior con información contextual"""
    return html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H4("", id="page-title", className="mb-0 text-dark"),
                    html.P("", id="page-subtitle", className="text-muted mb-0")
                ], width="auto"),
                
                dbc.Col([
                    html.Div([
                        # Indicadores rápidos
                        dbc.Badge(
                            "En línea",
                            color="success",
                            className="me-2"
                        ),
                        html.I(
                            className="fas fa-wifi text-success me-3",
                            title="Conexión activa"
                        ),
                        
                        # Fecha actual
                        html.Span(
                            id="current-date",
                            className="text-muted me-3"
                        ),
                        
                        # Notificaciones
                        dbc.Button([
                            html.I(className="fas fa-bell"),
                            dbc.Badge(
                                "3",
                                color="danger",
                                pill=True,
                                className="ms-1"
                            )
                        ],
                        id="notifications-button",
                        color="outline-secondary",
                        size="sm",
                        className="me-2"
                        ),
                        
                        # Configuración
                        dbc.Button(
                            html.I(className="fas fa-cog"),
                            id="settings-button",
                            color="outline-secondary",
                            size="sm"
                        )
                    ], className="d-flex align-items-center")
                ], width="auto", className="ms-auto")
            ])
        ], fluid=True)
    ],
    className="bg-white border-bottom shadow-sm",
    style={'padding': '1rem 0', 'margin-bottom': '0'}
    )

def create_loading_component():
    """Crea un componente de carga personalizado"""
    return html.Div([
        dbc.Spinner([
            html.Div([
                html.I(className="fas fa-futbol fa-3x text-primary mb-3"),
                html.H5("Cargando...", className="text-muted")
            ], className="text-center")
        ], 
        size="lg",
        color="primary",
        type="border"
        )
    ], 
    className="d-flex justify-content-center align-items-center",
    style={'min-height': '300px'}
    )

def create_error_component(error_message="Ha ocurrido un error"):
    """Crea un componente de error personalizado"""
    return dbc.Alert([
        html.Div([
            html.I(className="fas fa-exclamation-triangle fa-2x mb-3"),
            html.H5("¡Ups! Algo salió mal", className="alert-heading"),
            html.P(error_message),
            html.Hr(),
            dbc.Button(
                "Recargar página",
                id="reload-button",
                color="danger",
                outline=True
            )
        ], className="text-center")
    ], color="danger", className="m-4")

def create_empty_state(title="No hay datos", description="No se encontraron elementos", icon="fas fa-inbox"):
    """Crea un estado vacío personalizado"""
    return html.Div([
        html.I(className=f"{icon} fa-4x text-muted mb-4"),
        html.H4(title, className="text-muted mb-2"),
        html.P(description, className="text-muted")
    ], className="text-center py-5")

def create_page_header(title, subtitle=None, actions=None):
    """Crea un header estándar para las páginas"""
    header_content = [
        dbc.Row([
            dbc.Col([
                html.H2(title, className="mb-1 text-dark"),
                html.P(subtitle, className="text-muted mb-0") if subtitle else None
            ], width="auto"),
            
            dbc.Col([
                html.Div(actions if actions else [], className="d-flex gap-2")
            ], width="auto", className="ms-auto") if actions else None
        ], align="center")
    ]
    
    return html.Div(
        header_content,
        className="mb-4 pb-3 border-bottom"
    )

def create_stats_card(title, value, icon, color="primary", subtitle=None):
    """Crea una tarjeta de estadística"""
    return dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.H6(title, className="text-muted mb-2"),
                    html.H3(value, className=f"text-{color} mb-0 fw-bold"),
                    html.Small(subtitle, className="text-muted") if subtitle else None
                ], width=8),
                dbc.Col([
                    html.I(
                        className=f"{icon} fa-2x text-{color}",
                        style={'opacity': '0.7'}
                    )
                ], width=4, className="text-end")
            ])
        ])
    ], className="stat-card h-100")

def create_action_buttons(buttons):
    """Crea un grupo de botones de acción"""
    return dbc.ButtonGroup([
        dbc.Button([
            html.I(className=f"{btn.get('icon', 'fas fa-circle')} me-2"),
            btn['text']
        ],
        id=btn['id'],
        color=btn.get('color', 'primary'),
        outline=btn.get('outline', False),
        size=btn.get('size', 'md')
        ) for btn in buttons
    ], className="mb-3")

def create_search_filter_bar():
    """Crea una barra de búsqueda y filtros"""
    return dbc.Row([
        dbc.Col([
            dbc.InputGroup([
                dbc.Input(
                    id="search-input",
                    placeholder="Buscar...",
                    type="search"
                ),
                dbc.Button(
                    html.I(className="fas fa-search"),
                    id="search-button",
                    color="outline-secondary"
                )
            ])
        ], width=12, md=6),
        
        dbc.Col([
            dbc.Select(
                id="filter-select",
                options=[
                    {"label": "Todos", "value": "all"},
                    {"label": "Activos", "value": "active"},
                    {"label": "Inactivos", "value": "inactive"}
                ],
                value="all"
            )
        ], width=12, md=3),
        
        dbc.Col([
            dbc.Button([
                html.I(className="fas fa-filter me-2"),
                "Filtros"
            ],
            id="advanced-filter-button",
            color="outline-secondary",
            className="w-100"
            )
        ], width=12, md=3)
    ], className="mb-3")

# CSS personalizado para el contenido principal
MAIN_CONTENT_CSS = f"""
.main-content {{
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    min-height: 100vh;
    transition: margin-left 0.3s ease;
}}

.page-header {{
    background: white;
    border-radius: 15px;
    padding: 2rem;
    margin-bottom: 2rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}}

.content-card {{
    background: white;
    border-radius: 15px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    border: none;
}}

.stat-card {{
    transition: all 0.3s ease;
    border: none;
    border-radius: 15px;
}}

.stat-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}}

@media (max-width: 768px) {{
    .main-content {{
        margin-left: 0 !important;
    }}
}}
"""