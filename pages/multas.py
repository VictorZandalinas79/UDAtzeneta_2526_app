import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State, callback, dash_table
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from datetime import datetime, date
from database.db_manager import DatabaseManager, Multa, PagoMulta
from layouts.main_content import create_stats_card
from config.settings import COLORS
from utils.header_utils import create_page_header

def create_multas_layout():
    """Crea el layout principal de la página de multas"""
    return html.Div([
        # Header de la página con el escudo del equipo
        create_page_header(
            title="Gestión de Multas",
            subtitle="Administra las multas y pagos del equipo",
            actions=[
                dbc.Button([
                    html.I(className="fas fa-plus me-2"),
                    "Nueva Multa"
                ], id="btn-nueva-multa", color="primary"),
                dbc.Button([
                    html.I(className="fas fa-euro-sign me-2"),
                    "Registrar Pago"
                ], id="btn-registrar-pago", color="success", outline=True),
                dbc.Button([
                    html.I(className="fas fa-chart-pie me-2"),
                    "Estadísticas"
                ], id="btn-stats-multas", color="info", outline=True)
            ]
        ),
        
        # Estadísticas de multas
        create_multas_stats_section(),
        
        # Pestañas principales
        dbc.Tabs([
            dbc.Tab(label="Multas Activas", tab_id="tab-activas"),
            dbc.Tab(label="Historial Completo", tab_id="tab-historial"),
            dbc.Tab(label="Resumen por Jugador", tab_id="tab-resumen")
        ], id="multas-tabs", active_tab="tab-activas", className="mb-4"),
        
        # Contenido dinámico según la pestaña
        html.Div(id="multas-content"),
        
        # Modal para nueva multa
        create_multa_modal(),
        
        # Modal para registrar pago
        create_pago_modal(),
        
        # Modal de estadísticas
        create_multas_stats_modal(),
        
        # Stores
        dcc.Store(id="multas-data"),
        dcc.Store(id="multa-selected"),
        dcc.Store(id="jugadores-multas-data")
    ])

def create_multas_stats_section():
    """Crea la sección de estadísticas de multas"""
    return dbc.Row([
        dbc.Col([
            create_stats_card(
                "Total Multas",
                "€0",
                "fas fa-euro-sign",
                "primary",
                "Acumulado"
            )
        ], width=6, md=3, className="mb-3"),
        
        dbc.Col([
            create_stats_card(
                "Pendiente de Cobro",
                "€0",
                "fas fa-exclamation-triangle",
                "warning",
                "Por cobrar"
            )
        ], width=6, md=3, className="mb-3"),
        
        dbc.Col([
            create_stats_card(
                "Cobrado",
                "€0",
                "fas fa-check-circle",
                "success",
                "Total pagado"
            )
        ], width=6, md=3, className="mb-3"),
        
        dbc.Col([
            create_stats_card(
                "Este Mes",
                "€0",
                "fas fa-calendar-alt",
                "info",
                "Nuevas multas"
            )
        ], width=6, md=3, className="mb-3")
    ], className="mb-4", id="multas-stats-row")

def create_multa_modal():
    """Crea el modal para añadir nueva multa"""
    return dbc.Modal([
        dbc.ModalHeader([
            dbc.ModalTitle("Nueva Multa")
        ]),
        dbc.ModalBody([
            dbc.Form([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Jugador *"),
                        dbc.Select(
                            id="input-jugador-multa",
                            placeholder="Seleccionar jugador"
                        )
                    ], width=6),
                    dbc.Col([
                        dbc.Label("Fecha *"),
                        dbc.Input(
                            id="input-fecha-multa",
                            type="date",
                            value=datetime.now().strftime("%Y-%m-%d")
                        )
                    ], width=6)
                ], className="mb-3"),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Razón de la Multa *"),
                        dbc.Select(
                            id="input-razon-multa",
                            options=[
                                {"label": "Llegada tarde", "value": "Llegada tarde"},
                                {"label": "Falta no justificada", "value": "Falta no justificada"},
                                {"label": "Conducta antideportiva", "value": "Conducta antideportiva"},
                                {"label": "No traer equipación", "value": "No traer equipación"},
                                {"label": "Uso del móvil en entrenamiento", "value": "Uso del móvil"},
                                {"label": "Discusión con compañeros", "value": "Discusión con compañeros"},
                                {"label": "Falta de respeto", "value": "Falta de respeto"},
                                {"label": "Otros", "value": "Otros"}
                            ]
                        )
                    ], width=8),
                    dbc.Col([
                        dbc.Label("Importe (€) *"),
                        dbc.Input(
                            id="input-importe-multa",
                            type="number",
                            min=0,
                            step=0.01,
                            placeholder="0.00"
                        )
                    ], width=4)
                ], className="mb-3"),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Descripción Detallada"),
                        dbc.Textarea(
                            id="input-descripcion-multa",
                            placeholder="Describe los detalles de la infracción...",
                            rows=3
                        )
                    ], width=12)
                ], className="mb-3"),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Checkbox(
                            id="checkbox-pago-inmediato",
                            label="El jugador paga inmediatamente",
                            value=False
                        )
                    ], width=12)
                ], className="mb-3"),
                
                dbc.Collapse([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Cantidad Pagada (€)"),
                            dbc.Input(
                                id="input-pago-inmediato",
                                type="number",
                                min=0,
                                step=0.01
                            )
                        ], width=6),
                        dbc.Col([
                            dbc.Label("Observaciones del Pago"),
                            dbc.Input(
                                id="input-obs-pago-inmediato",
                                placeholder="Observaciones del pago..."
                            )
                        ], width=6)
                    ])
                ], id="collapse-pago-inmediato", is_open=False)
            ])
        ]),
        dbc.ModalFooter([
            dbc.Button("Cancelar", id="btn-cancel-multa", color="secondary", outline=True),
            dbc.Button("Guardar Multa", id="btn-save-multa", color="primary")
        ])
    ], id="multa-modal", size="lg", is_open=False)

def create_pago_modal():
    """Crea el modal para registrar pagos"""
    return dbc.Modal([
        dbc.ModalHeader([
            dbc.ModalTitle("Registrar Pago de Multa")
        ]),
        dbc.ModalBody([
            html.Div(id="pago-multa-info", className="mb-3"),
            dbc.Form([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Fecha del Pago *"),
                        dbc.Input(
                            id="input-fecha-pago",
                            type="date",
                            value=datetime.now().strftime("%Y-%m-%d")
                        )
                    ], width=6),
                    dbc.Col([
                        dbc.Label("Cantidad a Pagar (€) *"),
                        dbc.Input(
                            id="input-cantidad-pago",
                            type="number",
                            min=0,
                            step=0.01
                        )
                    ], width=6)
                ], className="mb-3"),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Observaciones"),
                        dbc.Textarea(
                            id="input-obs-pago",
                            placeholder="Observaciones sobre el pago...",
                            rows=2
                        )
                    ], width=12)
                ])
            ])
        ]),
        dbc.ModalFooter([
            dbc.Button("Cancelar", id="btn-cancel-pago", color="secondary", outline=True),
            dbc.Button("Registrar Pago", id="btn-save-pago", color="success")
        ])
    ], id="pago-modal", size="md", is_open=False)

def create_multas_stats_modal():
    """Crea el modal de estadísticas de multas"""
    return dbc.Modal([
        dbc.ModalHeader([
            dbc.ModalTitle("Estadísticas de Multas")
        ]),
        dbc.ModalBody([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id="grafico-multas-jugador")
                ], width=6),
                dbc.Col([
                    dcc.Graph(id="grafico-multas-razon")
                ], width=6)
            ]),
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id="grafico-multas-tiempo")
                ], width=12)
            ])
        ]),
        dbc.ModalFooter([
            dbc.Button("Cerrar", id="btn-close-stats-multas", color="secondary")
        ])
    ], id="multas-stats-modal", size="xl", is_open=False)

def create_multas_activas_content(multas_data):
    """Crea el contenido de multas activas (pendientes)"""
    multas_pendientes = [m for m in multas_data if not m['completamente_pagada']]
    
    if not multas_pendientes:
        return dbc.Alert([
            html.I(className="fas fa-check-circle fa-2x mb-3"),
            html.H5("¡Excelente!", className="alert-heading"),
            html.P("No hay multas pendientes de pago.")
        ], color="success", className="text-center")
    
    cards = []
    for multa in multas_pendientes:
        # Determinar color según la deuda
        if multa['debe'] > 50:
            card_color = "danger"
        elif multa['debe'] > 20:
            card_color = "warning"
        else:
            card_color = "info"
        
        cards.append(
            dbc.Card([
                dbc.CardHeader([
                    dbc.Row([
                        dbc.Col([
                            html.H6(multa['jugador_nombre'], className="mb-0")
                        ], width=8),
                        dbc.Col([
                            dbc.Badge(f"€{multa['debe']:.2f}", color=card_color, size="lg")
                        ], width=4, className="text-end")
                    ])
                ]),
                dbc.CardBody([
                    html.P([
                        html.Strong("Razón: "),
                        multa['razon_multa']
                    ], className="mb-2"),
                    html.P([
                        html.Strong("Fecha: "),
                        multa['fecha']
                    ], className="mb-2"),
                    html.P([
                        html.Strong("Total: "),
                        f"€{multa['multa']:.2f} | ",
                        html.Strong("Pagado: "),
                        f"€{multa['pagado']:.2f}"
                    ], className="mb-3"),
                    
                    dbc.ButtonGroup([
                        dbc.Button([
                            html.I(className="fas fa-euro-sign me-2"),
                            "Pagar"
                        ], 
                        id={"type": "btn-pagar-multa", "index": multa['id']},
                        color="success", 
                        size="sm"),
                        dbc.Button([
                            html.I(className="fas fa-eye me-2"),
                            "Ver"
                        ], 
                        id={"type": "btn-ver-multa", "index": multa['id']},
                        color="info", 
                        size="sm", 
                        outline=True)
                    ], size="sm")
                ])
            ], className="mb-3", color=card_color, outline=True)
        )
    
    return html.Div(cards)

def create_multas_historial_content(multas_data):
    """Crea el contenido del historial completo"""
    if not multas_data:
        return html.P("No hay multas registradas", className="text-center text-muted p-4")
    
    df = pd.DataFrame(multas_data)
    
    return dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[
            {"name": "Fecha", "id": "fecha", "type": "datetime"},
            {"name": "Jugador", "id": "jugador_nombre", "type": "text"},
            {"name": "Razón", "id": "razon_multa", "type": "text"},
            {"name": "Importe", "id": "multa", "type": "numeric", "format": {"specifier": "€.2f"}},
            {"name": "Pagado", "id": "pagado", "type": "numeric", "format": {"specifier": "€.2f"}},
            {"name": "Debe", "id": "debe", "type": "numeric", "format": {"specifier": "€.2f"}},
            {"name": "Estado", "id": "estado", "type": "text"}
        ],
        style_cell={
            'textAlign': 'left',
            'padding': '12px',
            'fontFamily': 'Arial'
        },
        style_header={
            'backgroundColor': COLORS['primary'],
            'color': 'white',
            'fontWeight': 'bold'
        },
        style_data_conditional=[
            {
                'if': {'filter_query': '{estado} = Pendiente'},
                'backgroundColor': '#fff3cd',
                'color': 'black',
            },
            {
                'if': {'filter_query': '{estado} = Pagada'},
                'backgroundColor': '#d4edda',
                'color': 'black',
            }
        ],
        sort_action="native",
        filter_action="native",
        page_size=15
    )

def create_multas_resumen_content(multas_data, jugadores_data):
    """Crea el contenido del resumen por jugador"""
    if not multas_data:
        return html.P("No hay datos para mostrar", className="text-center text-muted p-4")
    
    # Agrupar multas por jugador
    resumen = {}
    for multa in multas_data:
        jugador_id = multa['jugador_id']
        if jugador_id not in resumen:
            resumen[jugador_id] = {
                'jugador_nombre': multa['jugador_nombre'],
                'total_multas': 0,
                'total_importe': 0,
                'total_pagado': 0,
                'total_debe': 0,
                'multas_pendientes': 0
            }
        
        resumen[jugador_id]['total_multas'] += 1
        resumen[jugador_id]['total_importe'] += multa['multa']
        resumen[jugador_id]['total_pagado'] += multa['pagado']
        resumen[jugador_id]['total_debe'] += multa['debe']
        
        if not multa['completamente_pagada']:
            resumen[jugador_id]['multas_pendientes'] += 1
    
    # Crear cards para cada jugador
    cards = []
    for jugador_id, datos in resumen.items():
        # Determinar color según la deuda
        if datos['total_debe'] > 50:
            border_color = "danger"
        elif datos['total_debe'] > 0:
            border_color = "warning"
        else:
            border_color = "success"
        
        cards.append(
            dbc.Card([
                dbc.CardHeader([
                    html.H6(datos['jugador_nombre'], className="mb-0")
                ]),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Small("Total Multas", className="text-muted"),
                            html.H5(datos['total_multas'], className="mb-0")
                        ], width=6),
                        dbc.Col([
                            html.Small("Pendientes", className="text-muted"),
                            html.H5(datos['multas_pendientes'], className="mb-0 text-warning")
                        ], width=6)
                    ], className="mb-2"),
                    
                    dbc.Row([
                        dbc.Col([
                            html.Small("Total Importe", className="text-muted"),
                            html.H6(f"€{datos['total_importe']:.2f}", className="mb-0")
                        ], width=4),
                        dbc.Col([
                            html.Small("Pagado", className="text-muted"),
                            html.H6(f"€{datos['total_pagado']:.2f}", className="mb-0 text-success")
                        ], width=4),
                        dbc.Col([
                            html.Small("Debe", className="text-muted"),
                            html.H6(f"€{datos['total_debe']:.2f}", className="mb-0 text-danger")
                        ], width=4)
                    ])
                ])
            ], className="mb-3", color=border_color, outline=True)
        )
    
    return dbc.Row([
        dbc.Col(card, width=12, md=6, lg=4) for card in cards
    ])

# Callbacks para multas
def register_multas_callbacks():
    """Registra los callbacks de la página de multas"""
    
    @callback(
        [Output("multas-data", "data"),
         Output("jugadores-multas-data", "data")],
        Input("btn-nueva-multa", "n_clicks"),
        prevent_initial_call=False
    )
    def load_multas_data(n_clicks):
        """Carga los datos de multas y jugadores"""
        try:
            with DatabaseManager() as db:
                # Cargar multas
                multas = db.get_multas()
                multas_data = []
                
                for multa in multas:
                    jugador = db.get_jugador_by_id(multa.jugador_id)
                    multas_data.append({
                        'id': multa.id,
                        'jugador_id': multa.jugador_id,
                        'jugador_nombre': jugador.nombre_futbolistico if jugador else 'Desconocido',
                        'fecha': multa.fecha.strftime("%d/%m/%Y"),
                        'razon_multa': multa.razon_multa,
                        'multa': multa.multa,
                        'pagado': multa.pagado,
                        'debe': multa.debe,
                        'completamente_pagada': multa.completamente_pagada,
                        'estado': 'Pagada' if multa.completamente_pagada else 'Pendiente'
                    })
                
                # Cargar jugadores
                jugadores = db.get_jugadores(activos_solo=True)
                jugadores_options = [
                    {"label": j.nombre_futbolistico, "value": j.id}
                    for j in jugadores
                ]
                
                return multas_data, jugadores_options
                
        except Exception as e:
            print(f"Error cargando multas: {e}")
            return [], []
    
    @callback(
        Output("multas-content", "children"),
        [Input("multas-tabs", "active_tab"),
         Input("multas-data", "data"),
         Input("jugadores-multas-data", "data")]
    )
    def update_multas_content(active_tab, multas_data, jugadores_data):
        """Actualiza el contenido según la pestaña activa"""
        if active_tab == "tab-activas":
            return create_multas_activas_content(multas_data)
        elif active_tab == "tab-historial":
            return create_multas_historial_content(multas_data)
        elif active_tab == "tab-resumen":
            return create_multas_resumen_content(multas_data, jugadores_data)
        return html.Div()
    
    @callback(
        [Output("multa-modal", "is_open")],
        [Input("btn-nueva-multa", "n_clicks"),
         Input("btn-cancel-multa", "n_clicks"),
         Input("btn-save-multa", "n_clicks")],
        [State("multa-modal", "is_open")],
        prevent_initial_call=True
    )
    def toggle_multa_modal(btn_nueva, btn_cancel, btn_save, is_open):
        """Controla la apertura/cierre del modal de multa"""
        from dash.callback_context import triggered
        
        if not triggered:
            return [is_open]
        
        trigger_id = triggered[0]['prop_id'].split('.')[0]
        
        if trigger_id == "btn-nueva-multa":
            return [True]
        elif trigger_id in ["btn-cancel-multa", "btn-save-multa"]:
            return [False]
        
        return [is_open]
    
    @callback(
        [Output("input-jugador-multa", "options")],
        Input("jugadores-multas-data", "data")
    )
    def update_jugadores_options(jugadores_data):
        """Actualiza las opciones de jugadores en el modal"""
        return [jugadores_data or []]

# Registrar callbacks al importar
if 'register_multas_callbacks' in globals():
    register_multas_callbacks()

# Definir el layout de la página
layout = create_multas_layout()