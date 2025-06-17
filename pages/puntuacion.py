import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State, callback, dash_table
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from datetime import datetime, date, timedelta
from database.db_manager import DatabaseManager, Puntuacion
from layouts.main_content import create_stats_card
from config.settings import COLORS
from utils.header_utils import create_page_header

def create_puntuacion_layout():
    """Crea el layout principal de la página de puntuación"""
    return html.Div([
        # Header de la página con el escudo del equipo
        create_page_header(
            title="Sistema de Puntuación",
            subtitle="Registra y gestiona las puntuaciones de entrenamientos y objetivos",
            actions=[
                dbc.Button([
                    html.I(className="fas fa-plus me-2"),
                    "Añadir Puntos"
                ], id="btn-nueva-puntuacion", color="primary"),
                dbc.Button([
                    html.I(className="fas fa-trophy me-2"),
                    "Ranking"
                ], id="btn-ver-ranking", color="warning", outline=True),
                dbc.Button([
                    html.I(className="fas fa-chart-bar me-2"),
                    "Estadísticas"
                ], id="btn-stats-puntuacion", color="info", outline=True)
            ]
        ),
        
        # Estadísticas de puntuación
        create_puntuacion_stats_section(),
        
        # Pestañas principales
        dbc.Tabs([
            dbc.Tab(label="Ranking Actual", tab_id="tab-ranking"),
            dbc.Tab(label="Historial de Puntos", tab_id="tab-historial"),
            dbc.Tab(label="Evolución Temporal", tab_id="tab-evolucion"),
            dbc.Tab(label="Comparativas", tab_id="tab-comparativas")
        ], id="puntuacion-tabs", active_tab="tab-ranking", className="mb-4"),
        
        # Contenido dinámico
        html.Div(id="puntuacion-content"),
        
        # Modal para nueva puntuación
        create_puntuacion_modal(),
        
        # Modal de ranking detallado
        create_ranking_modal(),
        
        # Modal de estadísticas
        create_stats_puntuacion_modal(),
        
        # Stores
        dcc.Store(id="puntuaciones-data"),
        dcc.Store(id="ranking-data"),
        dcc.Store(id="jugadores-puntuacion-data")
    ])

def create_puntuacion_stats_section():
    """Crea la sección de estadísticas de puntuación"""
    return dbc.Row([
        dbc.Col([
            create_stats_card(
                "Total Puntos",
                "0",
                "fas fa-star",
                "primary",
                "Acumulados"
            )
        ], width=6, md=3, className="mb-3"),
        
        dbc.Col([
            create_stats_card(
                "Líder Actual",
                "-",
                "fas fa-crown",
                "warning",
                "Puntos"
            )
        ], width=6, md=3, className="mb-3"),
        
        dbc.Col([
            create_stats_card(
                "Promedio Equipo",
                "0",
                "fas fa-chart-line",
                "info",
                "Puntos/jugador"
            )
        ], width=6, md=3, className="mb-3"),
        
        dbc.Col([
            create_stats_card(
                "Esta Semana",
                "0",
                "fas fa-calendar-week",
                "success",
                "Nuevos puntos"
            )
        ], width=6, md=3, className="mb-3")
    ], className="mb-4", id="puntuacion-stats-row")

def create_puntuacion_modal():
    """Crea el modal para añadir nueva puntuación"""
    return dbc.Modal([
        dbc.ModalHeader([
            dbc.ModalTitle("Añadir Puntuación")
        ]),
        dbc.ModalBody([
            dbc.Alert([
                html.H6("Sistema de Puntuación", className="alert-heading"),
                html.P("Asigna puntos a los jugadores según su rendimiento en entrenamientos y cumplimiento de objetivos."),
                html.Hr(),
                html.P("Criterios sugeridos:", className="mb-1"),
                html.Ul([
                    html.Li("Excelente entrenamiento: +3 puntos"),
                    html.Li("Buen entrenamiento: +2 puntos"),
                    html.Li("Entrenamiento regular: +1 punto"),
                    html.Li("Cumplimiento de objetivo: +5 puntos"),
                    html.Li("Comportamiento ejemplar: +2 puntos"),
                    html.Li("Llegada tarde: -1 punto"),
                    html.Li("Actitud negativa: -2 puntos")
                ], className="mb-0")
            ], color="info", className="mb-4"),
            
            dbc.Form([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Jugador *"),
                        dbc.Select(
                            id="input-jugador-puntuacion",
                            placeholder="Seleccionar jugador"
                        )
                    ], width=6),
                    dbc.Col([
                        dbc.Label("Fecha *"),
                        dbc.Input(
                            id="input-fecha-puntuacion",
                            type="date",
                            value=datetime.now().strftime("%Y-%m-%d")
                        )
                    ], width=6)
                ], className="mb-3"),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Puntos *"),
                        dbc.InputGroup([
                            dbc.Input(
                                id="input-puntos",
                                type="number",
                                min=-10,
                                max=10,
                                step=1,
                                value=1
                            ),
                            dbc.InputGroupText("pts")
                        ])
                    ], width=6),
                    dbc.Col([
                        dbc.Label("Concepto *"),
                        dbc.Select(
                            id="input-concepto-puntuacion",
                            options=[
                                {"label": "Excelente entrenamiento", "value": "Excelente entrenamiento"},
                                {"label": "Buen entrenamiento", "value": "Buen entrenamiento"},
                                {"label": "Entrenamiento regular", "value": "Entrenamiento regular"},
                                {"label": "Cumplimiento objetivo", "value": "Cumplimiento objetivo"},
                                {"label": "Comportamiento ejemplar", "value": "Comportamiento ejemplar"},
                                {"label": "Ayuda a compañeros", "value": "Ayuda a compañeros"},
                                {"label": "Iniciativa propia", "value": "Iniciativa propia"},
                                {"label": "Llegada tarde", "value": "Llegada tarde"},
                                {"label": "Actitud negativa", "value": "Actitud negativa"},
                                {"label": "Falta de esfuerzo", "value": "Falta de esfuerzo"},
                                {"label": "Otros", "value": "Otros"}
                            ]
                        )
                    ], width=6)
                ], className="mb-3"),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Observaciones"),
                        dbc.Textarea(
                            id="input-observaciones-puntuacion",
                            placeholder="Detalles específicos sobre la puntuación asignada...",
                            rows=3
                        )
                    ], width=12)
                ], className="mb-3"),
                
                # Puntuación rápida para múltiples jugadores
                html.Hr(),
                html.H6("Puntuación Rápida para Múltiples Jugadores", className="mb-3"),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Checkbox(
                            id="checkbox-puntuacion-multiple",
                            label="Activar puntuación múltiple",
                            value=False
                        )
                    ], width=12)
                ]),
                
                dbc.Collapse([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Seleccionar Jugadores"),
                            dbc.Checklist(
                                id="checklist-jugadores-multiple",
                                options=[],
                                value=[],
                                inline=False
                            )
                        ], width=12)
                    ], className="mt-3")
                ], id="collapse-puntuacion-multiple", is_open=False)
            ])
        ]),
        dbc.ModalFooter([
            dbc.Button("Cancelar", id="btn-cancel-puntuacion", color="secondary", outline=True),
            dbc.Button("Guardar Puntuación", id="btn-save-puntuacion", color="primary")
        ])
    ], id="puntuacion-modal", size="lg", is_open=False)

def create_ranking_modal():
    """Crea el modal de ranking detallado"""
    return dbc.Modal([
        dbc.ModalHeader([
            dbc.ModalTitle("Ranking Detallado")
        ]),
        dbc.ModalBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Período"),
                    dbc.Select(
                        id="select-periodo-ranking",
                        options=[
                            {"label": "Todo el tiempo", "value": "all"},
                            {"label": "Este mes", "value": "month"},
                            {"label": "Esta semana", "value": "week"},
                            {"label": "Últimos 30 días", "value": "30days"}
                        ],
                        value="all"
                    )
                ], width=6),
                dbc.Col([
                    dbc.Label("Tipo de Puntos"),
                    dbc.Select(
                        id="select-tipo-ranking",
                        options=[
                            {"label": "Todos los puntos", "value": "all"},
                            {"label": "Solo positivos", "value": "positive"},
                            {"label": "Solo negativos", "value": "negative"}
                        ],
                        value="all"
                    )
                ], width=6)
            ], className="mb-4"),
            
            html.Div(id="ranking-detallado-container")
        ]),
        dbc.ModalFooter([
            dbc.Button("Cerrar", id="btn-close-ranking", color="secondary")
        ])
    ], id="ranking-modal", size="xl", is_open=False)

def create_stats_puntuacion_modal():
    """Crea el modal de estadísticas de puntuación"""
    return dbc.Modal([
        dbc.ModalHeader([
            dbc.ModalTitle("Estadísticas de Puntuación")
        ]),
        dbc.ModalBody([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id="grafico-distribucion-puntos")
                ], width=6),
                dbc.Col([
                    dcc.Graph(id="grafico-tendencia-puntos")
                ], width=6)
            ]),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id="grafico-conceptos-puntos")
                ], width=12)
            ])
        ]),
        dbc.ModalFooter([
            dbc.Button("Cerrar", id="btn-close-stats-puntuacion", color="secondary")
        ])
    ], id="stats-puntuacion-modal", size="xl", is_open=False)

def create_ranking_content(ranking_data):
    """Crea el contenido del ranking actual"""
    if not ranking_data:
        return dbc.Alert([
            html.I(className="fas fa-trophy fa-2x mb-3"),
            html.H5("No hay puntuaciones registradas", className="alert-heading"),
            html.P("Comienza a añadir puntuaciones para ver el ranking del equipo.")
        ], color="info", className="text-center")
    
    # Crear podium para los top 3
    podium = create_podium(ranking_data[:3])
    
    # Crear tabla para el resto
    tabla_ranking = create_ranking_table(ranking_data)
    
    return html.Div([
        podium,
        html.Hr(),
        tabla_ranking
    ])

def create_podium(top_3):
    """Crea el podium visual para los top 3"""
    if len(top_3) < 1:
        return html.Div()
    
    podium_cards = []
    colors = ["warning", "secondary", "dark"]  # Oro, Plata, Bronce
    icons = ["fas fa-crown", "fas fa-medal", "fas fa-award"]
    positions = ["1º", "2º", "3º"]
    
    for i, jugador in enumerate(top_3):
        if i >= 3:
            break
            
        card = dbc.Card([
            dbc.CardBody([
                html.Div([
                    html.I(className=f"{icons[i]} fa-3x text-{colors[i]} mb-3"),
                    html.H4(positions[i], className=f"text-{colors[i]} mb-2"),
                    html.H5(jugador['jugador_nombre'], className="mb-2"),
                    html.H3(f"{jugador['total_puntos']}", className=f"text-{colors[i]} mb-1"),
                    html.Small("puntos", className="text-muted")
                ], className="text-center")
            ])
        ], className="h-100")
        
        podium_cards.append(card)
    
    # Rellenar con cards vacías si hay menos de 3
    while len(podium_cards) < 3:
        podium_cards.append(
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.I(className="fas fa-user fa-3x text-muted mb-3"),
                        html.H4(positions[len(podium_cards)], className="text-muted mb-2"),
                        html.H5("Vacante", className="text-muted mb-2"),
                        html.H3("0", className="text-muted mb-1"),
                        html.Small("puntos", className="text-muted")
                    ], className="text-center")
                ])
            ], className="h-100", color="light")
        )
    
    return dbc.Row([
        dbc.Col(card, width=4) for card in podium_cards
    ], className="mb-4")

def create_ranking_table(ranking_data):
    """Crea la tabla completa del ranking"""
    table_rows = []
    
    for i, jugador in enumerate(ranking_data, 1):
        # Determinar color de la posición
        if i <= 3:
            pos_color = "success"
        elif i <= 10:
            pos_color = "primary"
        else:
            pos_color = "secondary"
        
        # Calcular tendencia (simulada por ahora)
        tendencia_icon = "fas fa-arrow-up text-success"  # Se puede calcular realmente
        
        table_rows.append(
            html.Tr([
                html.Td([
                    dbc.Badge(str(i), color=pos_color, className="me-2"),
                    html.Strong(jugador['jugador_nombre'])
                ]),
                html.Td(str(jugador['total_puntos'])),
                html.Td(str(jugador.get('puntos_positivos', 0))),
                html.Td(str(jugador.get('puntos_negativos', 0))),
                html.Td(f"{jugador.get('promedio_puntos', 0):.1f}"),
                html.Td([
                    html.I(className=tendencia_icon)
                ]),
                html.Td([
                    dbc.Button(
                        html.I(className="fas fa-eye"),
                        id={"type": "btn-ver-detalle", "index": jugador['jugador_id']},
                        color="info",
                        size="sm",
                        outline=True
                    )
                ])
            ])
        )
    
    return dbc.Table([
        html.Thead([
            html.Tr([
                html.Th("Posición / Jugador"),
                html.Th("Total"),
                html.Th("Positivos"),
                html.Th("Negativos"),
                html.Th("Promedio"),
                html.Th("Tendencia"),
                html.Th("Acciones")
            ])
        ]),
        html.Tbody(table_rows)
    ], striped=True, hover=True, responsive=True)

def create_historial_content(puntuaciones_data):
    """Crea el contenido del historial de puntuaciones"""
    if not puntuaciones_data:
        return html.P("No hay puntuaciones registradas", className="text-center text-muted p-4")
    
    df = pd.DataFrame(puntuaciones_data)
    
    return dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[
            {"name": "Fecha", "id": "fecha", "type": "datetime"},
            {"name": "Jugador", "id": "jugador_nombre", "type": "text"},
            {"name": "Puntos", "id": "puntos", "type": "numeric"},
            {"name": "Concepto", "id": "concepto", "type": "text"},
            {"name": "Observaciones", "id": "observaciones", "type": "text"}
        ],
        style_cell={
            'textAlign': 'left',
            'padding': '12px',
            'fontFamily': 'Arial',
            'maxWidth': '200px',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis'
        },
        style_header={
            'backgroundColor': COLORS['primary'],
            'color': 'white',
            'fontWeight': 'bold'
        },
        style_data_conditional=[
            {
                'if': {'filter_query': '{puntos} > 0'},
                'backgroundColor': '#d4edda',
                'color': 'black',
            },
            {
                'if': {'filter_query': '{puntos} < 0'},
                'backgroundColor': '#f8d7da',
                'color': 'black',
            }
        ],
        sort_action="native",
        filter_action="native",
        page_size=15
    )

# Callbacks para puntuación
def register_puntuacion_callbacks():
    """Registra los callbacks de la página de puntuación"""
    
    @callback(
        [Output("puntuaciones-data", "data"),
         Output("ranking-data", "data"),
         Output("jugadores-puntuacion-data", "data")],
        Input("btn-nueva-puntuacion", "n_clicks"),
        prevent_initial_call=False
    )
    def load_puntuacion_data(n_clicks):
        """Carga los datos de puntuación"""
        try:
            with DatabaseManager() as db:
                # Cargar puntuaciones
                puntuaciones = db.db.query(Puntuacion).order_by(Puntuacion.fecha.desc()).all()
                puntuaciones_data = []
                
                for punt in puntuaciones:
                    jugador = db.get_jugador_by_id(punt.jugador_id)
                    puntuaciones_data.append({
                        'id': punt.id,
                        'jugador_id': punt.jugador_id,
                        'jugador_nombre': jugador.nombre_futbolistico if jugador else 'Desconocido',
                        'fecha': punt.fecha.strftime("%d/%m/%Y"),
                        'puntos': punt.puntos,
                        'concepto': punt.concepto,
                        'observaciones': punt.observaciones
                    })
                
                # Calcular ranking
                ranking_dict = {}
                for punt in puntuaciones_data:
                    jugador_id = punt['jugador_id']
                    if jugador_id not in ranking_dict:
                        ranking_dict[jugador_id] = {
                            'jugador_id': jugador_id,
                            'jugador_nombre': punt['jugador_nombre'],
                            'total_puntos': 0,
                            'puntos_positivos': 0,
                            'puntos_negativos': 0,
                            'total_registros': 0
                        }
                    
                    puntos = punt['puntos']
                    ranking_dict[jugador_id]['total_puntos'] += puntos
                    ranking_dict[jugador_id]['total_registros'] += 1
                    
                    if puntos > 0:
                        ranking_dict[jugador_id]['puntos_positivos'] += puntos
                    else:
                        ranking_dict[jugador_id]['puntos_negativos'] += puntos
                
                # Calcular promedios y ordenar
                ranking_data = []
                for jugador_id, data in ranking_dict.items():
                    data['promedio_puntos'] = data['total_puntos'] / data['total_registros'] if data['total_registros'] > 0 else 0
                    ranking_data.append(data)
                
                ranking_data.sort(key=lambda x: x['total_puntos'], reverse=True)
                
                # Cargar jugadores
                jugadores = db.get_jugadores(activos_solo=True)
                jugadores_options = [
                    {"label": j.nombre_futbolistico, "value": j.id}
                    for j in jugadores
                ]
                
                return puntuaciones_data, ranking_data, jugadores_options
                
        except Exception as e:
            print(f"Error cargando puntuaciones: {e}")
            return [], [], []
    
    @callback(
        Output("puntuacion-content", "children"),
        [Input("puntuacion-tabs", "active_tab"),
         Input("puntuaciones-data", "data"),
         Input("ranking-data", "data")]
    )
    def update_puntuacion_content(active_tab, puntuaciones_data, ranking_data):
        """Actualiza el contenido según la pestaña activa"""
        if active_tab == "tab-ranking":
            return create_ranking_content(ranking_data)
        elif active_tab == "tab-historial":
            return create_historial_content(puntuaciones_data)
        elif active_tab == "tab-evolucion":
            return html.P("Gráficos de evolución en desarrollo", className="text-center text-muted p-4")
        elif active_tab == "tab-comparativas":
            return html.P("Análisis comparativo en desarrollo", className="text-center text-muted p-4")
        return html.Div()
    
    @callback(
        [Output("puntuacion-modal", "is_open")],
        [Input("btn-nueva-puntuacion", "n_clicks"),
         Input("btn-cancel-puntuacion", "n_clicks"),
         Input("btn-save-puntuacion", "n_clicks")],
        [State("puntuacion-modal", "is_open")],
        prevent_initial_call=True
    )
    def toggle_puntuacion_modal(btn_nueva, btn_cancel, btn_save, is_open):
        """Controla la apertura/cierre del modal de puntuación"""
        from dash.callback_context import triggered
        
        if not triggered:
            return [is_open]
        
        trigger_id = triggered[0]['prop_id'].split('.')[0]
        
        if trigger_id == "btn-nueva-puntuacion":
            return [True]
        elif trigger_id in ["btn-cancel-puntuacion", "btn-save-puntuacion"]:
            return [False]
        
        return [is_open]

# Registrar callbacks al importar
if 'register_puntuacion_callbacks' in globals():
    register_puntuacion_callbacks()

# Definir el layout de la página
layout = create_puntuacion_layout()