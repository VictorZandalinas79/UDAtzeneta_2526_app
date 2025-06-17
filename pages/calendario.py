import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State, callback, dash_table
import pandas as pd
from datetime import datetime, date, timedelta
from database.db_manager import DatabaseManager, Calendario
from layouts.main_content import create_stats_card
from config.settings import COLORS, COMPETICIONES
from utils.header_utils import create_page_header

def create_calendario_layout():
    """Crea el layout principal de la página de calendario"""
    return html.Div([
        # Header de la página con el escudo del equipo
        create_page_header(
            title="Calendario de Partidos",
            subtitle="Gestiona todos los partidos de la temporada",
            actions=[
                dbc.Button([
                    html.I(className="fas fa-plus me-2"),
                    "Nuevo Partido"
                ], id="btn-nuevo-partido", color="primary"),
                dbc.Button([
                    html.I(className="fas fa-sync-alt me-2"),
                    "Scraping"
                ], id="btn-scraping", color="success", outline=True),
                dbc.Button([
                    html.I(className="fas fa-download me-2"),
                    "Exportar"
                ], id="btn-exportar-calendario", color="info", outline=True)
            ]
        ),
        
        # Estadísticas del calendario
        create_calendario_stats_section(),
        
        # Filtros de calendario
        create_calendario_filters(),
        
        # Vista de calendario
        create_calendario_view(),
        
        # Modal para nuevo/editar partido
        create_partido_modal(),
        
        # Modal de configuración de scraping
        create_scraping_modal(),
        
        # Stores
        dcc.Store(id="calendario-data"),
        dcc.Store(id="partido-selected"),
        dcc.Interval(id="calendario-interval", interval=30*1000, n_intervals=0)  # Actualizar cada 30 segundos
    ])

def create_calendario_stats_section():
    """Crea la sección de estadísticas del calendario"""
    return dbc.Row([
        dbc.Col([
            create_stats_card(
                "Total Partidos",
                "0",
                "fas fa-futbol",
                "primary",
                "Esta temporada"
            )
        ], width=6, md=3, className="mb-3"),
        
        dbc.Col([
            create_stats_card(
                "Próximo Partido",
                "0",
                "fas fa-calendar-day",
                "success",
                "días restantes"
            )
        ], width=6, md=3, className="mb-3"),
        
        dbc.Col([
            create_stats_card(
                "Liga",
                "0",
                "fas fa-trophy",
                "warning",
                "partidos"
            )
        ], width=6, md=3, className="mb-3"),
        
        dbc.Col([
            create_stats_card(
                "Copa",
                "0",
                "fas fa-medal",
                "info",
                "partidos"
            )
        ], width=6, md=3, className="mb-3")
    ], className="mb-4", id="calendario-stats-row")

def create_calendario_filters():
    """Crea los filtros para el calendario"""
    return dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Competición"),
                    dbc.Select(
                        id="filter-competicion",
                        options=[{"label": "Todas", "value": "all"}] +
                               [{"label": comp, "value": comp} for comp in COMPETICIONES],
                        value="all"
                    )
                ], width=12, md=3),
                
                dbc.Col([
                    dbc.Label("Fecha Desde"),
                    dbc.Input(
                        id="filter-fecha-desde",
                        type="date",
                        value=(datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
                    )
                ], width=12, md=3),
                
                dbc.Col([
                    dbc.Label("Fecha Hasta"),
                    dbc.Input(
                        id="filter-fecha-hasta",
                        type="date",
                        value=(datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d")
                    )
                ], width=12, md=3),
                
                dbc.Col([
                    dbc.Label("Vista"),
                    dbc.RadioItems(
                        id="vista-calendario",
                        options=[
                            {"label": "Tabla", "value": "table"},
                            {"label": "Calendario", "value": "calendar"}
                        ],
                        value="table",
                        inline=True
                    )
                ], width=12, md=3)
            ])
        ])
    ], className="mb-4")

def create_calendario_view():
    """Crea la vista principal del calendario"""
    return dbc.Card([
        dbc.CardHeader([
            html.H5([
                html.I(className="fas fa-calendar me-2"),
                "Calendario de Partidos"
            ], className="mb-0 text-white")
        ]),
        dbc.CardBody([
            html.Div(id="calendario-view-container")
        ])
    ], className="content-card")

def create_partido_modal():
    """Crea el modal para añadir/editar partido"""
    return dbc.Modal([
        dbc.ModalHeader([
            dbc.ModalTitle(id="partido-modal-title")
        ]),
        dbc.ModalBody([
            dbc.Form([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Fecha *"),
                        dbc.Input(
                            id="input-fecha-partido",
                            type="date",
                            value=datetime.now().strftime("%Y-%m-%d")
                        )
                    ], width=6),
                    dbc.Col([
                        dbc.Label("Hora"),
                        dbc.Input(
                            id="input-hora-partido",
                            type="time",
                            value="16:00"
                        )
                    ], width=6)
                ], className="mb-3"),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Competición *"),
                        dbc.Select(
                            id="input-competicion-partido",
                            options=[{"label": comp, "value": comp} for comp in COMPETICIONES]
                        )
                    ], width=6),
                    dbc.Col([
                        dbc.Label("Jornada"),
                        dbc.Input(
                            id="input-jornada-partido",
                            placeholder="Ej: Jornada 15"
                        )
                    ], width=6)
                ], className="mb-3"),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Equipo Local *"),
                        dbc.Input(
                            id="input-equipo-local",
                            placeholder="Nombre del equipo local"
                        )
                    ], width=6),
                    dbc.Col([
                        dbc.Label("Equipo Visitante *"),
                        dbc.Input(
                            id="input-equipo-visitante",
                            placeholder="Nombre del equipo visitante"
                        )
                    ], width=6)
                ], className="mb-3"),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Goles Local"),
                        dbc.Input(
                            id="input-goles-local",
                            type="number",
                            min=0
                        )
                    ], width=6),
                    dbc.Col([
                        dbc.Label("Goles Visitante"),
                        dbc.Input(
                            id="input-goles-visitante",
                            type="number",
                            min=0
                        )
                    ], width=6)
                ], className="mb-3"),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Árbitro"),
                        dbc.Input(
                            id="input-arbitro",
                            placeholder="Nombre del árbitro principal"
                        )
                    ], width=6),
                    dbc.Col([
                        dbc.Label("Campo"),
                        dbc.Input(
                            id="input-campo",
                            placeholder="Nombre del campo de juego"
                        )
                    ], width=6)
                ], className="mb-3"),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Asistentes"),
                        dbc.Textarea(
                            id="input-asistentes",
                            placeholder="Árbitros asistentes"
                        )
                    ], width=12)
                ])
            ])
        ]),
        dbc.ModalFooter([
            dbc.Button("Cancelar", id="btn-cancel-partido", color="secondary", outline=True),
            dbc.Button("Guardar", id="btn-save-partido", color="primary")
        ])
    ], id="partido-modal", size="lg", is_open=False)

def create_scraping_modal():
    """Crea el modal de configuración de scraping"""
    return dbc.Modal([
        dbc.ModalHeader([
            dbc.ModalTitle("Configuración de Web Scraping")
        ]),
        dbc.ModalBody([
            dbc.Alert([
                html.H6("Información sobre Web Scraping", className="alert-heading"),
                html.P("El web scraping permite obtener automáticamente los partidos oficiales desde la página de la federación."),
                html.Hr(),
                html.P("Por favor, configura la URL y los parámetros necesarios:", className="mb-0")
            ], color="info"),
            
            dbc.Form([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("URL de la Federación"),
                        dbc.Input(
                            id="input-scraping-url",
                            placeholder="https://federacion.com/calendario",
                            value=""
                        )
                    ], width=12)
                ], className="mb-3"),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Código del Equipo"),
                        dbc.Input(
                            id="input-codigo-equipo",
                            placeholder="ID del equipo en la web"
                        )
                    ], width=6),
                    dbc.Col([
                        dbc.Label("Temporada"),
                        dbc.Input(
                            id="input-temporada-scraping",
                            value="2024-2025"
                        )
                    ], width=6)
                ], className="mb-3"),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Checkbox(
                            id="checkbox-scraping-automatico",
                            label="Activar scraping automático cada hora",
                            value=False
                        )
                    ], width=12)
                ])
            ])
        ]),
        dbc.ModalFooter([
            dbc.Button("Cancelar", id="btn-cancel-scraping", color="secondary", outline=True),
            dbc.Button("Ejecutar Scraping", id="btn-ejecutar-scraping", color="success"),
            dbc.Button("Guardar Configuración", id="btn-save-scraping", color="primary")
        ])
    ], id="scraping-modal", size="lg", is_open=False)

def create_calendario_table(data):
    """Crea la tabla del calendario"""
    if not data:
        return html.P("No hay partidos programados", className="text-center text-muted p-4")
    
    df = pd.DataFrame(data)
    
    return dash_table.DataTable(
        id="calendario-table",
        data=df.to_dict('records'),
        columns=[
            {"name": "Fecha", "id": "fecha", "type": "datetime"},
            {"name": "Hora", "id": "hora", "type": "text"},
            {"name": "Competición", "id": "competicion", "type": "text"},
            {"name": "Local", "id": "equipo_local", "type": "text"},
            {"name": "Resultado", "id": "resultado", "type": "text"},
            {"name": "Visitante", "id": "equipo_visitante", "type": "text"},
            {"name": "Campo", "id": "campo", "type": "text"},
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
                'if': {'filter_query': '{estado} = Próximo'},
                'backgroundColor': '#d4edda',
                'color': 'black',
            },
            {
                'if': {'filter_query': '{estado} = Jugado'},
                'backgroundColor': '#f8f9fa',
                'color': 'black',
            }
        ],
        row_selectable="single",
        page_size=15,
        sort_action="native",
        filter_action="native"
    )

# Callbacks para el calendario
def register_calendario_callbacks():
    """Registra todos los callbacks del calendario"""
    
    @callback(
        Output("calendario-data", "data"),
        [Input("calendario-interval", "n_intervals"),
         Input("filter-competicion", "value"),
         Input("filter-fecha-desde", "value"),
         Input("filter-fecha-hasta", "value")],
        prevent_initial_call=False
    )
    def load_calendario_data(n_intervals, competicion_filter, fecha_desde, fecha_hasta):
        """Carga los datos del calendario"""
        try:
            with DatabaseManager() as db:
                calendario = db.get_calendario()
                
                data = []
                for evento in calendario:
                    # Filtrar por competición
                    if competicion_filter != "all" and evento.competicion != competicion_filter:
                        continue
                    
                    # Filtrar por fechas
                    if fecha_desde:
                        if evento.fecha < datetime.strptime(fecha_desde, "%Y-%m-%d").date():
                            continue
                    
                    if fecha_hasta:
                        if evento.fecha > datetime.strptime(fecha_hasta, "%Y-%m-%d").date():
                            continue
                    
                    # Determinar estado del partido
                    hoy = date.today()
                    if evento.fecha > hoy:
                        estado = "Próximo"
                    elif evento.fecha == hoy:
                        estado = "Hoy"
                    else:
                        estado = "Jugado"
                    
                    # Formatear resultado
                    if evento.goles_equipo_local is not None and evento.goles_equipo_visitante is not None:
                        resultado = f"{evento.goles_equipo_local} - {evento.goles_equipo_visitante}"
                    else:
                        resultado = "vs"
                    
                    data.append({
                        'id': evento.id,
                        'fecha': evento.fecha.strftime("%d/%m/%Y"),
                        'hora': evento.hora or "-",
                        'competicion': evento.competicion,
                        'jornada': evento.jornada or "-",
                        'equipo_local': evento.equipo_local,
                        'goles_local': evento.goles_equipo_local,
                        'goles_visitante': evento.goles_equipo_visitante,
                        'resultado': resultado,
                        'equipo_visitante': evento.equipo_visitante,
                        'arbitro': evento.arbitro or "-",
                        'campo': evento.campo or "-",
                        'estado': estado,
                        'scrapeado': evento.scrapeado
                    })
                
                return sorted(data, key=lambda x: x['fecha'], reverse=True)
                
        except Exception as e:
            print(f"Error cargando calendario: {e}")
            return []
    
    @callback(
        Output("calendario-view-container", "children"),
        [Input("calendario-data", "data"),
         Input("vista-calendario", "value")]
    )
    def update_calendario_view(data, vista_type):
        """Actualiza la vista del calendario"""
        if vista_type == "table":
            return create_calendario_table(data)
        else:
            # Aquí se implementaría la vista de calendario
            return html.P("Vista de calendario en desarrollo", className="text-center text-muted p-4")
    
    @callback(
        [Output("partido-modal", "is_open"),
         Output("partido-modal-title", "children")],
        [Input("btn-nuevo-partido", "n_clicks"),
         Input("btn-cancel-partido", "n_clicks"),
         Input("btn-save-partido", "n_clicks")],
        [State("partido-modal", "is_open")],
        prevent_initial_call=True
    )
    def toggle_partido_modal(btn_nuevo, btn_cancel, btn_save, is_open):
        """Controla la apertura/cierre del modal de partido"""
        from dash.callback_context import triggered
        
        if not triggered:
            return is_open, "Nuevo Partido"
        
        trigger_id = triggered[0]['prop_id'].split('.')[0]
        
        if trigger_id == "btn-nuevo-partido":
            return True, "Nuevo Partido"
        elif trigger_id in ["btn-cancel-partido", "btn-save-partido"]:
            return False, "Nuevo Partido"
        
        return is_open, "Nuevo Partido"
    
    @callback(
        [Output("scraping-modal", "is_open")],
        [Input("btn-scraping", "n_clicks"),
         Input("btn-cancel-scraping", "n_clicks"),
         Input("btn-save-scraping", "n_clicks")],
        [State("scraping-modal", "is_open")],
        prevent_initial_call=True
    )
    def toggle_scraping_modal(btn_scraping, btn_cancel, btn_save, is_open):
        """Controla la apertura/cierre del modal de scraping"""
        from dash.callback_context import triggered
        
        if not triggered:
            return [is_open]
        
        trigger_id = triggered[0]['prop_id'].split('.')[0]
        
        if trigger_id == "btn-scraping":
            return [True]
        elif trigger_id in ["btn-cancel-scraping", "btn-save-scraping"]:
            return [False]
        
        return [is_open]

# Registrar callbacks al importar
register_calendario_callbacks()

# Definir el layout del calendario
layout = create_calendario_layout()