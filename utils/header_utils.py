from dash import html
import dash_bootstrap_components as dbc

def create_page_header(title, subtitle, actions=None):
    """
    Crea un encabezado de página consistente con el escudo del equipo
    
    Args:
        title (str): Título de la página
        subtitle (str): Subtítulo descriptivo
        actions (list, optional): Lista de componentes de Dash para las acciones del encabezado
    
    Returns:
        dbc.Row: Fila con el encabezado de la página
    """
    return dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(
                    src="/assets/escudo.png",
                    style={
                        'height': '60px',
                        'width': 'auto',
                        'marginRight': '15px',
                        'objectFit': 'contain'
                    }
                ),
                html.Div([
                    html.H1(title, className="mb-1", style={'fontWeight': 'bold'}),
                    html.P(subtitle, className="text-muted mb-0")
                ])
            ], className="d-flex align-items-center")
        ], width="auto"),
        dbc.Col([
            html.Div(actions or [], className="d-flex justify-content-end")
        ]) if actions else None
    ], className="mb-4")

def create_simple_header(title, subtitle):
    """
    Crea un encabezado simple sin acciones
    
    Args:
        title (str): Título de la página
        subtitle (str): Subtítulo descriptivo
    
    Returns:
        dbc.Row: Fila con el encabezado de la página
    """
    return dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(
                    src="/assets/escudo.png",
                    style={
                        'height': '60px',
                        'width': 'auto',
                        'marginRight': '15px',
                        'objectFit': 'contain'
                    }
                ),
                html.Div([
                    html.H1(title, className="mb-1", style={'fontWeight': 'bold'}),
                    html.P(subtitle, className="text-muted mb-0")
                ])
            ], className="d-flex align-items-center")
        ])
    ], className="mb-4")
