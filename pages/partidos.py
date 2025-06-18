import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State, callback, dash_table
import pandas as pd
from datetime import datetime, date
from database.db_manager import DatabaseManager, Partido, EventoPartido, ConvocatoriaPartido
from layouts.main_content import create_stats_card
from config.settings import COLORS, COMPETICIONES
from utils.header_utils import create_page_header
from utils.scraping import scraping_manager

def create_partidos_layout():
    """Crea el layout principal de la página de partidos"""
    return html.Div([
        # Header de la página con el escudo del equipo
        create_page_header(
            title="Control de Partidos",
            subtitle="Gestiona convocatorias, eventos y estadísticas de partidos",
            actions=[
                dbc.Button([
                    html.I(className="fas fa-plus me-2"),
                    "Nuevo Partido"
                ], id="btn-nuevo-partido-control", color="primary"),
                dbc.Button([
                    html.I(className="fas fa-users me-2"),
                    "Gestionar Convocatoria"
                ], id="btn-gestionar-convocatoria", color="success", outline=True),
                dbc.Button([
                    html.I(className="fas fa-chart-line me-2"),
                    "Estadísticas"
                ], id="btn-stats-partidos", color="info", outline=True)
            ]
        ),
        
        # Estadísticas de partidos
        create_partidos_stats_section(),
        
        # Pestañas de navegación
        dbc.Tabs([
            dbc.Tab(label="Próximos Partidos", tab_id="tab-proximos"),
            dbc.Tab(label="Partidos Jugados", tab_id="tab-jugados"),
            dbc.Tab(label="Convocatorias", tab_id="tab-convocatorias"),
            dbc.Tab(label="Eventos", tab_id="tab-eventos")
        ], id="partidos-tabs", active_tab="tab-proximos", className="mb-4"),
        
        # Contenido dinámico
        html.Div(id="partidos-content"),
        
        # Modal para gestionar partido
        create_partido_control_modal(),
        
        # Modal para convocatoria
        create_convocatoria_modal(),
        
        # Modal para eventos del partido
        create_eventos_modal(),
        
        # Stores
        dcc.Store(id="partidos-data"),
        dcc.Store(id="partido-control-selected"),
        dcc.Store(id="jugadores-convocatoria")
    ])

def create_partidos_stats_section():
    """Crea la sección de estadísticas de partidos"""
    return dbc.Row([
        dbc.Col([
            create_stats_card(
                "Partidos Jugados",
                "0",
                "fas fa-futbol",
                "primary",
                "Esta temporada"
            )
        ], width=6, md=3, className="mb-3"),
        
        dbc.Col([
            create_stats_card(
                "Victorias",
                "0",
                "fas fa-trophy",
                "success",
                "ganados"
            )
        ], width=6, md=3, className="mb-3"),
        
        dbc.Col([
            create_stats_card(
                "Goles a Favor",
                "0",
                "fas fa-bullseye",
                "info",
                "marcados"
            )
        ], width=6, md=3, className="mb-3"),
        
        dbc.Col([
            create_stats_card(
                "Próximo Partido",
                "0",
                "fas fa-calendar-day",
                "warning",
                "días"
            )
        ], width=6, md=3, className="mb-3")
    ], className="mb-4", id="partidos-stats-row")

def create_partido_control_modal():
    """Crea el modal para control detallado del partido"""
    return dbc.Modal([
        dbc.ModalHeader([
            dbc.ModalTitle(id="partido-control-modal-title")
        ]),
        dbc.ModalBody([
            dbc.Tabs([
                dbc.Tab(label="Información General", tab_id="tab-info-general"),
                dbc.Tab(label="Convocatoria", tab_id="tab-conv-partido"),
                dbc.Tab(label="Eventos", tab_id="tab-eventos-partido")
            ], id="partido-control-tabs", active_tab="tab-info-general"),
            
            html.Div(id="partido-control-content", className="mt-3")
        ]),
        dbc.ModalFooter([
            dbc.Button("Cerrar", id="btn-close-partido-control", color="secondary"),
            dbc.Button("Guardar Cambios", id="btn-save-partido-control", color="primary")
        ])
    ], id="partido-control-modal", size="xl", is_open=False)

def create_convocatoria_modal():
    """Crea el modal para gestionar convocatorias"""
    return dbc.Modal([
        dbc.ModalHeader([
            dbc.ModalTitle("Gestionar Convocatoria")
        ]),
        dbc.ModalBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Seleccionar Partido"),
                    dbc.Select(
                        id="select-partido-convocatoria",
                        placeholder="Seleccionar partido..."
                    )
                ], width=12)
            ], className="mb-4"),
            
            html.Div(id="convocatoria-form-container")
        ]),
        dbc.ModalFooter([
            dbc.Button("Cancelar", id="btn-cancel-convocatoria", color="secondary", outline=True),
            dbc.Button("Guardar Convocatoria", id="btn-save-convocatoria", color="success")
        ])
    ], id="convocatoria-modal", size="xl", is_open=False)

# Añadir esta función al create_partidos_layout()
def create_partidos_layout():
    """Crea el layout principal de la página de partidos"""
    return html.Div([
        # Header de la página con el escudo del equipo
        create_page_header(
            title="Control de Partidos",
            subtitle="Gestiona convocatorias, eventos y estadísticas de partidos",
            actions=[
                dbc.Button([
                    html.I(className="fas fa-plus me-2"),
                    "Nuevo Partido"
                ], id="btn-nuevo-partido-control", color="primary"),
                dbc.Button([
                    html.I(className="fas fa-users me-2"),
                    "Gestionar Convocatoria"
                ], id="btn-gestionar-convocatoria", color="success", outline=True),
                dbc.Button([
                    html.I(className="fas fa-chart-line me-2"),
                    "Estadísticas"
                ], id="btn-stats-partidos", color="info", outline=True),
                # NUEVO: Botón para scraping
                dbc.Button([
                    html.I(className="fas fa-download me-2"),
                    "Importar FFCV"
                ], id="btn-scraping-ffcv", color="warning", outline=True)
            ]
        ),
        
        # Estadísticas de partidos
        create_partidos_stats_section(),
        
        # NUEVO: Sección de configuración de scraping
        create_scraping_config_section(),
        
        # Pestañas de navegación
        dbc.Tabs([
            dbc.Tab(label="Próximos Partidos", tab_id="tab-proximos"),
            dbc.Tab(label="Partidos Jugados", tab_id="tab-jugados"),
            dbc.Tab(label="Convocatorias", tab_id="tab-convocatorias"),
            dbc.Tab(label="Eventos", tab_id="tab-eventos")
        ], id="partidos-tabs", active_tab="tab-proximos", className="mb-4"),
        
        # Contenido dinámico
        html.Div(id="partidos-content"),
        
        # Modal para gestionar partido
        create_partido_control_modal(),
        
        # Modal para convocatoria
        create_convocatoria_modal(),
        
        # Modal para eventos del partido
        create_eventos_modal(),
        
        # NUEVO: Modal para configurar scraping
        create_scraping_modal(),
        
        # Stores
        dcc.Store(id="partidos-data"),
        dcc.Store(id="partido-control-selected"),
        dcc.Store(id="jugadores-convocatoria"),
        dcc.Store(id="scraping-status")  # NUEVO
    ])

# NUEVA FUNCIÓN: Sección de configuración de scraping
def create_scraping_config_section():
    """Crea la sección de configuración del scraping"""
    return dbc.Collapse([
        dbc.Card([
            dbc.CardHeader([
                html.H6("Configuración de Importación FFCV", className="mb-0")
            ]),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("URL del Calendario FFCV"),
                        dbc.Input(
                            id="input-ffcv-url",
                            placeholder="https://resultadosffcv.isquad.es/equipo_calendario.php?...",
                            value="https://resultadosffcv.isquad.es/equipo_calendario.php?id_temp=20&id_modalidad=33327&id_competicion=903498407&id_equipo=18331&torneo_equipo=903498408&id_torneo=903498408"
                        )
                    ], width=8),
                    dbc.Col([
                        dbc.Label("Acciones"),
                        html.Br(),
                        dbc.ButtonGroup([
                            dbc.Button("Probar", id="btn-test-ffcv", color="info", size="sm"),
                            dbc.Button("Importar", id="btn-import-ffcv", color="success", size="sm")
                        ])
                    ], width=4)
                ]),
                html.Hr(),
                html.Div(id="scraping-status-display")
            ])
        ])
    ], id="scraping-config-collapse", is_open=False)

# NUEVA FUNCIÓN: Modal de scraping
def create_scraping_modal():
    """Crea el modal para el proceso de scraping"""
    return dbc.Modal([
        dbc.ModalHeader([
            dbc.ModalTitle("Importación desde FFCV")
        ]),
        dbc.ModalBody([
            html.Div(id="scraping-modal-content")
        ]),
        dbc.ModalFooter([
            dbc.Button("Cerrar", id="btn-close-scraping-modal", color="secondary")
        ])
    ], id="scraping-modal", size="lg", is_open=False)

# ACTUALIZAR la función register_partidos_callbacks() con estos nuevos callbacks:
def register_partidos_callbacks():
    """Registra todos los callbacks de partidos"""
    
    # ... callbacks existentes ...
    
    # NUEVO: Callback para mostrar/ocultar configuración de scraping
    @callback(
        Output("scraping-config-collapse", "is_open"),
        Input("btn-scraping-ffcv", "n_clicks"),
        State("scraping-config-collapse", "is_open"),
        prevent_initial_call=True
    )
    def toggle_scraping_config(n_clicks, is_open):
        """Toggle de la configuración de scraping"""
        if n_clicks:
            return not is_open
        return is_open
    
    # NUEVO: Callback para probar conexión FFCV
    @callback(
        Output("scraping-status-display", "children"),
        Input("btn-test-ffcv", "n_clicks"),
        State("input-ffcv-url", "value"),
        prevent_initial_call=True
    )
    def test_ffcv_connection(n_clicks, ffcv_url):
        """Prueba la conexión con la FFCV"""
        if not n_clicks or not ffcv_url:
            return html.Div()
        
        try:
            # Configurar el scraper
            scraping_manager.configure_ffcv_scraper(ffcv_url)
            
            # Probar conexión
            soup = scraping_manager.ffcv_scraper.get_calendar_page(ffcv_url)
            
            if soup:
                # Verificar si encontramos la tabla
                tabla = soup.find('table', class_='table calendario_table')
                if tabla:
                    filas = tabla.find('tbody').find_all('tr') if tabla.find('tbody') else []
                    
                    return dbc.Alert([
                        html.I(className="fas fa-check-circle me-2"),
                        f"Conexión exitosa. Encontradas {len(filas)} filas en la tabla."
                    ], color="success")
                else:
                    return dbc.Alert([
                        html.I(className="fas fa-exclamation-triangle me-2"),
                        "Conexión exitosa pero no se encontró la tabla de partidos."
                    ], color="warning")
            else:
                return dbc.Alert([
                    html.I(className="fas fa-times-circle me-2"),
                    "Error de conexión. Verifica la URL."
                ], color="danger")
                
        except Exception as e:
            return dbc.Alert([
                html.I(className="fas fa-times-circle me-2"),
                f"Error: {str(e)}"
            ], color="danger")

def create_eventos_modal():
    """Crea el modal para gestionar eventos del partido"""
    return dbc.Modal([
        dbc.ModalHeader([
            dbc.ModalTitle("Eventos del Partido")
        ]),
        dbc.ModalBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Partido"),
                    html.H6(id="evento-partido-info", className="text-muted")
                ], width=12)
            ], className="mb-3"),
            
            # Formulario para nuevo evento
            dbc.Card([
                dbc.CardHeader("Agregar Nuevo Evento"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Minuto"),
                            dbc.Input(
                                id="input-minuto-evento",
                                type="number",
                                min=1,
                                max=120,
                                placeholder="90"
                            )
                        ], width=3),
                        dbc.Col([
                            dbc.Label("Jugador"),
                            dbc.Select(
                                id="input-jugador-evento",
                                placeholder="Seleccionar jugador..."
                            )
                        ], width=4),
                        dbc.Col([
                            dbc.Label("Tipo de Evento"),
                            dbc.Select(
                                id="input-tipo-evento",
                                options=[
                                    {"label": "Gol", "value": "gol"},
                                    {"label": "Asistencia", "value": "asistencia"},
                                    {"label": "Tarjeta Amarilla", "value": "tarjeta_amarilla"},
                                    {"label": "Tarjeta Roja", "value": "tarjeta_roja"},
                                    {"label": "Sustitución (Entra)", "value": "sustitucion_entra"},
                                    {"label": "Sustitución (Sale)", "value": "sustitucion_sale"},
                                    {"label": "Otros", "value": "otros"}
                                ]
                            )
                        ], width=3),
                        dbc.Col([
                            dbc.Label("Acciones"),
                            html.Br(),
                            dbc.Button(
                                "Agregar",
                                id="btn-add-evento",
                                color="primary",
                                size="sm",
                                className="w-100"
                            )
                        ], width=2)
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Descripción (opcional)"),
                            dbc.Input(
                                id="input-descripcion-evento",
                                placeholder="Descripción del evento..."
                            )
                        ], width=12)
                    ], className="mt-2")
                ])
            ], className="mb-4"),
            
            # Lista de eventos
            html.Div(id="eventos-list-container")
        ]),
        dbc.ModalFooter([
            dbc.Button("Cerrar", id="btn-close-eventos", color="secondary")
        ])
    ], id="eventos-modal", size="xl", is_open=False)

def create_convocatoria_form(jugadores, partido_info=None):
    """Crea el formulario de convocatoria"""
    if not jugadores:
        return html.P("No hay jugadores disponibles", className="text-muted")
    
    # Dividir en titulares, suplentes y no convocados
    titulares_section = create_jugadores_section(
        "Titulares (11 jugadores)", 
        jugadores, 
        "titular",
        max_players=11
    )
    
    suplentes_section = create_jugadores_section(
        "Suplentes", 
        jugadores, 
        "suplente",
        max_players=7
    )
    
    no_convocados_section = create_jugadores_section(
        "No Convocados", 
        jugadores, 
        "no_convocado"
    )
    
    return html.Div([
        dbc.Alert([
            html.H6("Instrucciones:", className="alert-heading"),
            html.P("Arrastra los jugadores entre las secciones para formar la convocatoria.", className="mb-0")
        ], color="info", className="mb-4"),
        
        dbc.Row([
            dbc.Col([titulares_section], width=4),
            dbc.Col([suplentes_section], width=4),
            dbc.Col([no_convocados_section], width=4)
        ])
    ])

def create_jugadores_section(title, jugadores, section_type, max_players=None):
    """Crea una sección de jugadores para la convocatoria"""
    jugadores_cards = []
    
    for jugador in jugadores:
        card = dbc.Card([
            dbc.CardBody([
                html.H6(jugador['nombre_futbolistico'], className="mb-1"),
                html.Small(jugador['posicion'] or "Sin posición", className="text-muted"),
                dbc.Checkbox(
                    id=f"check-{section_type}-{jugador['id']}",
                    className="float-end"
                )
            ])
        ], className="mb-2 player-card", size="sm")
        
        jugadores_cards.append(card)
    
    header_color = {
        "titular": "success",
        "suplente": "warning", 
        "no_convocado": "secondary"
    }.get(section_type, "primary")
    
    title_with_limit = title
    if max_players:
        title_with_limit += f" (máx. {max_players})"
    
    return dbc.Card([
        dbc.CardHeader([
            html.H6(title_with_limit, className="mb-0 text-white")
        ], color=header_color),
        dbc.CardBody([
            html.Div(
                jugadores_cards,
                id=f"section-{section_type}",
                className="player-section",
                style={"min-height": "400px"}
            )
        ])
    ])

def create_proximos_partidos_content(partidos_data):
    """Crea el contenido de próximos partidos"""
    proximos = [p for p in partidos_data if p.get('fecha_obj', date.today()) >= date.today()]
    
    if not proximos:
        return dbc.Alert([
            html.I(className="fas fa-calendar-times fa-2x mb-3"),
            html.H5("No hay próximos partidos", className="alert-heading"),
            html.P("No hay partidos programados próximamente.")
        ], color="info", className="text-center")
    
    cards = []
    for partido in proximos[:6]:  # Mostrar máximo 6
        # Determinar días restantes
        dias_restantes = (partido.get('fecha_obj', date.today()) - date.today()).days
        
        if dias_restantes == 0:
            badge_text = "HOY"
            badge_color = "danger"
        elif dias_restantes == 1:
            badge_text = "MAÑANA"
            badge_color = "warning"
        else:
            badge_text = f"{dias_restantes} DÍAS"
            badge_color = "primary"
        
        card = dbc.Card([
            dbc.CardHeader([
                dbc.Row([
                    dbc.Col([
                        html.H6(partido['competicion'], className="mb-0")
                    ], width=8),
                    dbc.Col([
                        dbc.Badge(badge_text, color=badge_color)
                    ], width=4, className="text-end")
                ])
            ]),
            dbc.CardBody([
                html.H5(f"{partido['equipo_local']} vs {partido['equipo_visitante']}", className="mb-2"),
                html.P([
                    html.I(className="fas fa-calendar me-2"),
                    partido['fecha']
                ], className="mb-1"),
                html.P([
                    html.I(className="fas fa-clock me-2"),
                    partido.get('hora', 'Por confirmar')
                ], className="mb-1"),
                html.P([
                    html.I(className="fas fa-map-marker-alt me-2"),
                    partido.get('campo', 'Por confirmar')
                ], className="mb-3"),
                
                dbc.ButtonGroup([
                    dbc.Button([
                        html.I(className="fas fa-users me-1"),
                        "Convocatoria"
                    ], 
                    id={"type": "btn-conv-partido", "index": partido['id']},
                    color="success", 
                    size="sm"),
                    dbc.Button([
                        html.I(className="fas fa-edit me-1"),
                        "Gestionar"
                    ], 
                    id={"type": "btn-manage-partido", "index": partido['id']},
                    color="primary", 
                    size="sm",
                    outline=True)
                ], size="sm", className="w-100")
            ])
        ], className="mb-3")
        
        cards.append(card)
    
    return dbc.Row([
        dbc.Col(card, width=12, md=6, lg=4) for card in cards
    ])

def create_partidos_jugados_content(partidos_data):
    """Crea el contenido de partidos jugados"""
    jugados = [p for p in partidos_data if p.get('fecha_obj', date.today()) < date.today()]
    
    if not jugados:
        return html.P("No hay partidos jugados registrados", className="text-center text-muted p-4")
    
    # Crear tabla
    df = pd.DataFrame(jugados)
    
    return dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[
            {"name": "Fecha", "id": "fecha", "type": "datetime"},
            {"name": "Competición", "id": "competicion", "type": "text"},
            {"name": "Rival", "id": "rival", "type": "text"},
            {"name": "Resultado", "id": "resultado", "type": "text"},
            {"name": "Local/Visitante", "id": "local_visitante", "type": "text"},
            {"name": "Campo", "id": "campo", "type": "text"}
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
                'if': {'filter_query': '{resultado} contains Victoria'},
                'backgroundColor': '#d4edda',
                'color': 'black',
            },
            {
                'if': {'filter_query': '{resultado} contains Derrota'},
                'backgroundColor': '#f8d7da',
                'color': 'black',
            }
        ],
        sort_action="native",
        page_size=15
    )

# Callbacks para partidos
def register_partidos_callbacks():
    """Registra todos los callbacks de partidos"""
    
    @callback(
        [Output("partidos-data", "data"),
         Output("jugadores-convocatoria", "data")],
        Input("btn-nuevo-partido-control", "n_clicks"),
        prevent_initial_call=False
    )
    def load_partidos_data(n_clicks):
        """Carga los datos de partidos"""
        try:
            with DatabaseManager() as db:
                # Obtener partidos del calendario
                calendario = db.get_calendario()
                partidos_data = []
                
                for evento in calendario:
                    # Determinar rival y si es local o visitante
                    if evento.equipo_local == "UD Atzeneta":
                        rival = evento.equipo_visitante
                        local_visitante = "Local"
                    else:
                        rival = evento.equipo_local
                        local_visitante = "Visitante"
                    
                    # Determinar resultado
                    if evento.goles_equipo_local is not None and evento.goles_equipo_visitante is not None:
                        if evento.equipo_local == "UD Atzeneta":
                            if evento.goles_equipo_local > evento.goles_equipo_visitante:
                                resultado = f"Victoria {evento.goles_equipo_local}-{evento.goles_equipo_visitante}"
                            elif evento.goles_equipo_local < evento.goles_equipo_visitante:
                                resultado = f"Derrota {evento.goles_equipo_local}-{evento.goles_equipo_visitante}"
                            else:
                                resultado = f"Empate {evento.goles_equipo_local}-{evento.goles_equipo_visitante}"
                        else:
                            if evento.goles_equipo_visitante > evento.goles_equipo_local:
                                resultado = f"Victoria {evento.goles_equipo_visitante}-{evento.goles_equipo_local}"
                            elif evento.goles_equipo_visitante < evento.goles_equipo_local:
                                resultado = f"Derrota {evento.goles_equipo_visitante}-{evento.goles_equipo_local}"
                            else:
                                resultado = f"Empate {evento.goles_equipo_visitante}-{evento.goles_equipo_local}"
                    else:
                        resultado = "Por jugar"
                    
                    partidos_data.append({
                        'id': evento.id,
                        'fecha': evento.fecha.strftime("%d/%m/%Y"),
                        'fecha_obj': evento.fecha,
                        'hora': evento.hora,
                        'competicion': evento.competicion,
                        'jornada': evento.jornada,
                        'equipo_local': evento.equipo_local,
                        'equipo_visitante': evento.equipo_visitante,
                        'rival': rival,
                        'local_visitante': local_visitante,
                        'resultado': resultado,
                        'campo': evento.campo,
                        'arbitro': evento.arbitro
                    })
                
                # Cargar jugadores para convocatorias
                jugadores = db.get_jugadores(activos_solo=True)
                jugadores_data = [
                    {
                        'id': j.id,
                        'nombre_futbolistico': j.nombre_futbolistico,
                        'nombre': j.nombre,
                        'apellidos': j.apellidos,
                        'posicion': j.posicion,
                        'dorsal': j.dorsal
                    } for j in jugadores
                ]
                
                return partidos_data, jugadores_data
                
        except Exception as e:
            print(f"Error cargando partidos: {e}")
            return [], []
    
    @callback(
        Output("partidos-content", "children"),
        [Input("partidos-tabs", "active_tab"),
         Input("partidos-data", "data")]
    )
    def update_partidos_content(active_tab, partidos_data):
        """Actualiza el contenido según la pestaña activa"""
        if active_tab == "tab-proximos":
            return create_proximos_partidos_content(partidos_data)
        elif active_tab == "tab-jugados":
            return create_partidos_jugados_content(partidos_data)
        elif active_tab == "tab-convocatorias":
            return html.P("Gestión de convocatorias en desarrollo", className="text-center text-muted p-4")
        elif active_tab == "tab-eventos":
            return html.P("Gestión de eventos en desarrollo", className="text-center text-muted p-4")
        return html.Div()
    
    @callback(
        [Output("convocatoria-modal", "is_open")],
        [Input("btn-gestionar-convocatoria", "n_clicks"),
         Input("btn-cancel-convocatoria", "n_clicks"),
         Input("btn-save-convocatoria", "n_clicks")],
        [State("convocatoria-modal", "is_open")],
        prevent_initial_call=True
    )
    def toggle_convocatoria_modal(btn_gestionar, btn_cancel, btn_save, is_open):
        """Controla la apertura/cierre del modal de convocatoria"""
        from dash.callback_context import triggered
        
        if not triggered:
            return [is_open]
        
        trigger_id = triggered[0]['prop_id'].split('.')[0]
        
        if trigger_id == "btn-gestionar-convocatoria":
            return [True]
        elif trigger_id in ["btn-cancel-convocatoria", "btn-save-convocatoria"]:
            return [False]
        
        return [is_open]
# NUEVO: Callback para importar datos de FFCV
    @callback(
        [Output("scraping-modal", "is_open"),
         Output("scraping-modal-content", "children"),
         Output("partidos-data", "data", allow_duplicate=True)],
        [Input("btn-import-ffcv", "n_clicks"),
         Input("btn-close-scraping-modal", "n_clicks")],
        [State("input-ffcv-url", "value"),
         State("scraping-modal", "is_open"),
         State("partidos-data", "data")],
        prevent_initial_call=True
    )
    def import_ffcv_data(btn_import, btn_close, ffcv_url, modal_open, current_data):
        """Importa datos desde FFCV"""
        from dash.callback_context import triggered
        
        if not triggered:
            return modal_open, html.Div(), current_data
        
        trigger_id = triggered[0]['prop_id'].split('.')[0]
        
        if trigger_id == "btn-close-scraping-modal":
            return False, html.Div(), current_data
        
        if trigger_id == "btn-import-ffcv" and ffcv_url:
            try:
                # Configurar y ejecutar scraping
                scraping_manager.configure_ffcv_scraper(ffcv_url)
                result = scraping_manager.perform_ffcv_scraping()
                
                if result['success']:
                    # Recargar datos de partidos
                    with DatabaseManager() as db:
                        calendario = db.get_calendario()
                        partidos_data = []
                        
                        for evento in calendario:
                            # Determinar rival y si es local o visitante
                            if evento.equipo_local == "U.D. Atzeneta de Castellón 'A'":
                                rival = evento.equipo_visitante
                                local_visitante = "Local"
                            else:
                                rival = evento.equipo_local
                                local_visitante = "Visitante"
                            
                            # Determinar resultado
                            if evento.goles_equipo_local is not None and evento.goles_equipo_visitante is not None:
                                if evento.equipo_local == "U.D. Atzeneta de Castellón 'A'":
                                    if evento.goles_equipo_local > evento.goles_equipo_visitante:
                                        resultado = f"Victoria {evento.goles_equipo_local}-{evento.goles_equipo_visitante}"
                                    elif evento.goles_equipo_local < evento.goles_equipo_visitante:
                                        resultado = f"Derrota {evento.goles_equipo_local}-{evento.goles_equipo_visitante}"
                                    else:
                                        resultado = f"Empate {evento.goles_equipo_local}-{evento.goles_equipo_visitante}"
                                else:
                                    if evento.goles_equipo_visitante > evento.goles_equipo_local:
                                        resultado = f"Victoria {evento.goles_equipo_visitante}-{evento.goles_equipo_local}"
                                    elif evento.goles_equipo_visitante < evento.goles_equipo_local:
                                        resultado = f"Derrota {evento.goles_equipo_visitante}-{evento.goles_equipo_local}"
                                    else:
                                        resultado = f"Empate {evento.goles_equipo_visitante}-{evento.goles_equipo_local}"
                            else:
                                resultado = "Por jugar"
                            
                            partidos_data.append({
                                'id': evento.id,
                                'fecha': evento.fecha.strftime("%d/%m/%Y"),
                                'fecha_obj': evento.fecha,
                                'hora': evento.hora,
                                'competicion': evento.competicion,
                                'jornada': evento.jornada,
                                'equipo_local': evento.equipo_local,
                                'equipo_visitante': evento.equipo_visitante,
                                'rival': rival,
                                'local_visitante': local_visitante,
                                'resultado': resultado,
                                'campo': evento.campo,
                                'arbitro': evento.arbitro
                            })
                    
                    modal_content = dbc.Alert([
                        html.H5("¡Importación Exitosa!", className="alert-heading"),
                        html.P(f"Se han importado {result['total_matches']} partidos."),
                        html.Hr(),
                        html.P([
                            html.Strong("Nuevos: "), f"{result['created']} partidos", html.Br(),
                            html.Strong("Actualizados: "), f"{result['updated']} partidos", html.Br(),
                            html.Strong("Tiempo: "), f"{result['elapsed_time']:.2f} segundos"
                        ])
                    ], color="success")
                    
                    return True, modal_content, partidos_data
                    
                else:
                    modal_content = dbc.Alert([
                        html.H5("Error en la Importación", className="alert-heading"),
                        html.P(f"Error: {result['error']}")
                    ], color="danger")
                    
                    return True, modal_content, current_data
                    
            except Exception as e:
                modal_content = dbc.Alert([
                    html.H5("Error Inesperado", className="alert-heading"),
                    html.P(f"Error: {str(e)}")
                ], color="danger")
                
                return True, modal_content, current_data
        
        return modal_open, html.Div(), current_data

# Registrar callbacks al importar
if 'register_partidos_callbacks' in globals():
    register_partidos_callbacks()

# Definir el layout de la página
layout = create_partidos_layout()