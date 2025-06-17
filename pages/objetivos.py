import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State, callback, dash_table
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, date, timedelta
from database.db_manager import DatabaseManager, ObjetivoIndividual
from layouts.main_content import create_page_header, create_stats_card
from config.settings import COLORS

def create_objetivos_layout():
    """Crea el layout principal de la página de objetivos"""
    return html.Div([
        # Header de la página
        create_page_header(
            "Objetivos Individuales",
            "Seguimiento del desarrollo personal de cada jugador",
            actions=[
                dbc.Button([
                    html.I(className="fas fa-plus me-2"),
                    "Nuevo Objetivo"
                ], id="btn-nuevo-objetivo", color="primary"),
                dbc.Button([
                    html.I(className="fas fa-chart-line me-2"),
                    "Progreso General"
                ], id="btn-progreso-general", color="success", outline=True),
                dbc.Button([
                    html.I(className="fas fa-download me-2"),
                    "Exportar"
                ], id="btn-exportar-objetivos", color="info", outline=True)
            ]
        ),
        
        # Estadísticas de objetivos
        create_objetivos_stats_section(),
        
        # Filtros y navegación
        create_objetivos_filters(),
        
        # Contenido principal
        dbc.Row([
            dbc.Col([
                create_objetivos_table_card()
            ], width=12, lg=8),
            dbc.Col([
                create_objetivos_summary_card()
            ], width=12, lg=4)
        ]),
        
        # Modal para nuevo/editar objetivo
        create_objetivo_modal(),
        
        # Modal de progreso detallado
        create_progreso_modal(),
        
        # Stores
        dcc.Store(id="objetivos-data"),
        dcc.Store(id="objetivo-selected"),
        dcc.Store(id="jugadores-objetivos-data")
    ])

def create_objetivos_stats_section():
    """Crea la sección de estadísticas de objetivos"""
    return dbc.Row([
        dbc.Col([
            create_stats_card(
                "Objetivos Activos",
                "0",
                "fas fa-target",
                "primary",
                "En progreso"
            )
        ], width=6, md=3, className="mb-3"),
        
        dbc.Col([
            create_stats_card(
                "Completados",
                "0",
                "fas fa-check-circle",
                "success",
                "Este mes"
            )
        ], width=6, md=3, className="mb-3"),
        
        dbc.Col([
            create_stats_card(
                "Progreso Promedio",
                "0%",
                "fas fa-percentage",
                "info",
                "Del equipo"
            )
        ], width=6, md=3, className="mb-3"),
        
        dbc.Col([
            create_stats_card(
                "Vencidos",
                "0",
                "fas fa-exclamation-triangle",
                "warning",
                "Sin completar"
            )
        ], width=6, md=3, className="mb-3")
    ], className="mb-4", id="objetivos-stats-row")

def create_objetivos_filters():
    """Crea los filtros para objetivos"""
    return dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Jugador"),
                    dbc.Select(
                        id="filter-jugador-objetivos",
                        options=[{"label": "Todos los jugadores", "value": "all"}],
                        value="all"
                    )
                ], width=12, md=3),
                
                dbc.Col([
                    dbc.Label("Estado"),
                    dbc.Select(
                        id="filter-estado-objetivos",
                        options=[
                            {"label": "Todos", "value": "all"},
                            {"label": "En Progreso", "value": "progress"},
                            {"label": "Completados", "value": "completed"},
                            {"label": "Vencidos", "value": "overdue"}
                        ],
                        value="all"
                    )
                ], width=12, md=3),
                
                dbc.Col([
                    dbc.Label("Mes"),
                    dbc.Select(
                        id="filter-mes-objetivos",
                        options=[{"label": "Todos", "value": "all"}] +
                               [{"label": f"{i:02d}/2025", "value": f"2025-{i:02d}"} 
                                for i in range(1, 13)],
                        value=datetime.now().strftime("%Y-%m")
                    )
                ], width=12, md=3),
                
                dbc.Col([
                    dbc.Label("Acciones"),
                    html.Br(),
                    dbc.Button([
                        html.I(className="fas fa-sync me-2"),
                        "Actualizar"
                    ], id="btn-refresh-objetivos", color="outline-primary", className="w-100")
                ], width=12, md=3)
            ])
        ])
    ], className="mb-4")

def create_objetivos_table_card():
    """Crea la tarjeta con la tabla de objetivos"""
    return dbc.Card([
        dbc.CardHeader([
            html.H5([
                html.I(className="fas fa-list me-2"),
                "Lista de Objetivos"
            ], className="mb-0 text-white")
        ]),
        dbc.CardBody([
            html.Div(id="objetivos-table-container")
        ])
    ], className="content-card")

def create_objetivos_summary_card():
    """Crea la tarjeta de resumen de objetivos"""
    return dbc.Card([
        dbc.CardHeader([
            html.H5([
                html.I(className="fas fa-chart-pie me-2"),
                "Resumen de Progreso"
            ], className="mb-0 text-white")
        ]),
        dbc.CardBody([
            html.Div(id="objetivos-summary-container")
        ])
    ], className="content-card")

def create_objetivo_modal():
    """Crea el modal para nuevo/editar objetivo"""
    return dbc.Modal([
        dbc.ModalHeader([
            dbc.ModalTitle(id="objetivo-modal-title")
        ]),
        dbc.ModalBody([
            dbc.Form([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Jugador *"),
                        dbc.Select(
                            id="input-jugador-objetivo",
                            placeholder="Seleccionar jugador"
                        )
                    ], width=6),
                    dbc.Col([
                        dbc.Label("Mes/Año *"),
                        dbc.Input(
                            id="input-mes-objetivo",
                            type="month",
                            value=datetime.now().strftime("%Y-%m")
                        )
                    ], width=6)
                ], className="mb-3"),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Objetivo *"),
                        dbc.Input(
                            id="input-titulo-objetivo",
                            placeholder="Ej: Mejorar precisión en pases largos"
                        )
                    ], width=12)
                ], className="mb-3"),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Descripción Detallada"),
                        dbc.Textarea(
                            id="input-descripcion-objetivo",
                            placeholder="Describe específicamente qué se debe trabajar y cómo medirlo...",
                            rows=4
                        )
                    ], width=12)
                ], className="mb-3"),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Fecha de Inicio *"),
                        dbc.Input(
                            id="input-fecha-inicio-objetivo",
                            type="date",
                            value=datetime.now().strftime("%Y-%m-%d")
                        )
                    ], width=6),
                    dbc.Col([
                        dbc.Label("Fecha Objetivo"),
                        dbc.Input(
                            id="input-fecha-objetivo-objetivo",
                            type="date",
                            value=(datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
                        )
                    ], width=6)
                ], className="mb-3"),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Progreso Inicial (%)"),
                        dbc.Input(
                            id="input-progreso-objetivo",
                            type="number",
                            min=0,
                            max=100,
                            value=0
                        )
                    ], width=6),
                    dbc.Col([
                        dbc.Label("Estado"),
                        dbc.RadioItems(
                            id="input-estado-objetivo",
                            options=[
                                {"label": "En Progreso", "value": False},
                                {"label": "Completado", "value": True}
                            ],
                            value=False,
                            inline=True
                        )
                    ], width=6)
                ])
            ])
        ]),
        dbc.ModalFooter([
            dbc.Button("Cancelar", id="btn-cancel-objetivo", color="secondary", outline=True),
            dbc.Button("Guardar Objetivo", id="btn-save-objetivo", color="primary")
        ])
    ], id="objetivo-modal", size="lg", is_open=False)

def create_progreso_modal():
    """Crea el modal de progreso detallado"""
    return dbc.Modal([
        dbc.ModalHeader([
            dbc.ModalTitle("Progreso Detallado por Jugador")
        ]),
        dbc.ModalBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Seleccionar Jugador"),
                    dbc.Select(
                        id="select-jugador-progreso",
                        placeholder="Seleccionar jugador..."
                    )
                ], width=12)
            ], className="mb-4"),
            
            html.Div(id="progreso-detallado-container")
        ]),
        dbc.ModalFooter([
            dbc.Button("Cerrar", id="btn-close-progreso", color="secondary")
        ])
    ], id="progreso-modal", size="xl", is_open=False)

def create_objetivos_table(objetivos_data):
    """Crea la tabla de objetivos"""
    if not objetivos_data:
        return html.P("No hay objetivos registrados", className="text-center text-muted p-4")
    
    table_rows = []
    
    for objetivo in objetivos_data:
        # Determinar color del progreso
        progreso = objetivo.get('progreso', 0)
        if progreso >= 100:
            progress_color = "success"
        elif progreso >= 70:
            progress_color = "info"
        elif progreso >= 40:
            progress_color = "warning"
        else:
            progress_color = "danger"
        
        # Determinar estado
        if objetivo.get('completado', False):
            estado_badge = dbc.Badge("Completado", color="success")
        elif objetivo.get('vencido', False):
            estado_badge = dbc.Badge("Vencido", color="danger")
        else:
            estado_badge = dbc.Badge("En Progreso", color="primary")
        
        table_rows.append(
            html.Tr([
                html.Td(objetivo['jugador_nombre']),
                html.Td(objetivo['objetivo']),
                html.Td(objetivo['mes']),
                html.Td([
                    dbc.Progress(
                        value=progreso,
                        color=progress_color,
                        className="mb-1"
                    ),
                    html.Small(f"{progreso}%", className="text-muted")
                ]),
                html.Td(estado_badge),
                html.Td([
                    dbc.ButtonGroup([
                        dbc.Button(
                            html.I(className="fas fa-edit"),
                            id={"type": "btn-edit-objetivo", "index": objetivo['id']},
                            color="primary",
                            size="sm",
                            outline=True
                        ),
                        dbc.Button(
                            html.I(className="fas fa-plus"),
                            id={"type": "btn-update-progreso", "index": objetivo['id']},
                            color="success",
                            size="sm",
                            outline=True,
                            title="Actualizar progreso"
                        )
                    ], size="sm")
                ])
            ])
        )
    
    return dbc.Table([
        html.Thead([
            html.Tr([
                html.Th("Jugador"),
                html.Th("Objetivo"),
                html.Th("Mes"),
                html.Th("Progreso"),
                html.Th("Estado"),
                html.Th("Acciones")
            ])
        ]),
        html.Tbody(table_rows)
    ], striped=True, hover=True, responsive=True)

def create_objetivos_summary(objetivos_data):
    """Crea el resumen visual de objetivos"""
    if not objetivos_data:
        return html.P("No hay datos para mostrar", className="text-center text-muted")
    
    # Calcular estadísticas
    total_objetivos = len(objetivos_data)
    completados = len([o for o in objetivos_data if o.get('completado', False)])
    en_progreso = len([o for o in objetivos_data if not o.get('completado', False) and not o.get('vencido', False)])
    vencidos = len([o for o in objetivos_data if o.get('vencido', False)])
    
    # Gráfico de dona
    fig = go.Figure(data=[
        go.Pie(
            labels=['Completados', 'En Progreso', 'Vencidos'],
            values=[completados, en_progreso, vencidos],
            hole=0.3,
            marker_colors=[COLORS['success'], COLORS['primary'], COLORS['danger']]
        )
    ])
    
    fig.update_layout(
        title="Distribución de Objetivos",
        height=300,
        margin=dict(t=50, b=0, l=0, r=0),
        showlegend=True
    )
    
    # Progreso promedio
    progreso_promedio = sum(o.get('progreso', 0) for o in objetivos_data) / total_objetivos if total_objetivos > 0 else 0
    
    return html.Div([
        dcc.Graph(figure=fig, config={'displayModeBar': False}),
        
        html.Hr(),
        
        html.H6("Estadísticas Generales", className="mb-3"),
        
        html.Div([
            html.P([
                html.Strong("Total objetivos: "),
                html.Span(str(total_objetivos))
            ], className="mb-1"),
            html.P([
                html.Strong("Progreso promedio: "),
                html.Span(f"{progreso_promedio:.1f}%")
            ], className="mb-1"),
            html.P([
                html.Strong("Tasa de éxito: "),
                html.Span(f"{(completados/total_objetivos*100):.1f}%" if total_objetivos > 0 else "0%")
            ], className="mb-1")
        ])
    ])

# Callbacks para objetivos
def register_objetivos_callbacks():
    """Registra todos los callbacks de objetivos"""
    
    @callback(
        [Output("objetivos-data", "data"),
         Output("jugadores-objetivos-data", "data")],
        [Input("btn-refresh-objetivos", "n_clicks"),
         Input("filter-jugador-objetivos", "value"),
         Input("filter-estado-objetivos", "value"),
         Input("filter-mes-objetivos", "value")],
        prevent_initial_call=False
    )
    def load_objetivos_data(n_clicks, jugador_filter, estado_filter, mes_filter):
        """Carga los datos de objetivos"""
        try:
            with DatabaseManager() as db:
                # Cargar objetivos
                objetivos = db.db.query(ObjetivoIndividual).all()
                objetivos_data = []
                
                today = date.today()
                
                for objetivo in objetivos:
                    jugador = db.get_jugador_by_id(objetivo.jugador_id)
                    
                    # Filtrar por jugador
                    if jugador_filter != "all" and str(objetivo.jugador_id) != jugador_filter:
                        continue
                    
                    # Determinar si está vencido
                    vencido = False
                    if objetivo.fecha_objetivo and objetivo.fecha_objetivo < today and not objetivo.completado:
                        vencido = True
                    
                    # Filtrar por estado
                    if estado_filter == "completed" and not objetivo.completado:
                        continue
                    elif estado_filter == "progress" and (objetivo.completado or vencido):
                        continue
                    elif estado_filter == "overdue" and not vencido:
                        continue
                    
                    # Filtrar por mes
                    if mes_filter != "all" and objetivo.mes != mes_filter:
                        continue
                    
                    objetivos_data.append({
                        'id': objetivo.id,
                        'jugador_id': objetivo.jugador_id,
                        'jugador_nombre': jugador.nombre_futbolistico if jugador else 'Desconocido',
                        'objetivo': objetivo.objetivo,
                        'descripcion': objetivo.descripcion,
                        'fecha_inicio': objetivo.fecha_inicio.strftime("%d/%m/%Y") if objetivo.fecha_inicio else None,
                        'fecha_objetivo': objetivo.fecha_objetivo.strftime("%d/%m/%Y") if objetivo.fecha_objetivo else None,
                        'completado': objetivo.completado,
                        'progreso': objetivo.progreso,
                        'mes': objetivo.mes,
                        'vencido': vencido
                    })
                
                # Cargar jugadores
                jugadores = db.get_jugadores(activos_solo=True)
                jugadores_options = [
                    {"label": j.nombre_futbolistico, "value": j.id}
                    for j in jugadores
                ]
                
                return objetivos_data, jugadores_options
                
        except Exception as e:
            print(f"Error cargando objetivos: {e}")
            return [], []
    
    @callback(
        [Output("objetivos-table-container", "children"),
         Output("objetivos-summary-container", "children")],
        Input("objetivos-data", "data")
    )
    def update_objetivos_content(objetivos_data):
        """Actualiza el contenido de objetivos"""
        table = create_objetivos_table(objetivos_data)
        summary = create_objetivos_summary(objetivos_data)
        return table, summary
    
    @callback(
        [Output("objetivo-modal", "is_open"),
         Output("objetivo-modal-title", "children")],
        [Input("btn-nuevo-objetivo", "n_clicks"),
         Input("btn-cancel-objetivo", "n_clicks"),
         Input("btn-save-objetivo", "n_clicks")],
        [State("objetivo-modal", "is_open")],
        prevent_initial_call=True
    )
    def toggle_objetivo_modal(btn_nuevo, btn_cancel, btn_save, is_open):
        """Controla la apertura/cierre del modal de objetivo"""
        from dash.callback_context import triggered
        
        if not triggered:
            return is_open, "Nuevo Objetivo"
        
        trigger_id = triggered[0]['prop_id'].split('.')[0]
        
        if trigger_id == "btn-nuevo-objetivo":
            return True, "Nuevo Objetivo"
        elif trigger_id in ["btn-cancel-objetivo", "btn-save-objetivo"]:
            return False, "Nuevo Objetivo"
        
        return is_open, "Nuevo Objetivo"
    
    @callback(
        Output("input-jugador-objetivo", "options"),
        Input("jugadores-objetivos-data", "data")
    )
    def update_jugadores_options(jugadores_data):
        """Actualiza las opciones de jugadores en el modal"""
        return jugadores_data or []

# Registrar callbacks al importar
register_objetivos_callbacks()