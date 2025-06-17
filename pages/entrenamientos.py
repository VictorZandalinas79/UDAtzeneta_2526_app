import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State, callback, dash_table
import pandas as pd
from datetime import datetime, date
from database.db_manager import DatabaseManager, Entrenamiento, AsistenciaEntrenamiento
from layouts.main_content import create_page_header, create_stats_card
from config.settings import COLORS, RAZONES_AUSENCIA

def create_entrenamientos_layout():
    """Crea el layout principal de la página de entrenamientos"""
    return html.Div([
        # Header de la página
        create_page_header(
            "Gestión de Entrenamientos",
            "Controla la asistencia y registra entrenamientos",
            actions=[
                dbc.Button([
                    html.I(className="fas fa-plus me-2"),
                    "Nuevo Entrenamiento"
                ], id="btn-nuevo-entrenamiento", color="primary"),
                dbc.Button([
                    html.I(className="fas fa-chart-bar me-2"),
                    "Estadísticas"
                ], id="btn-stats-entrenamientos", color="info", outline=True),
                dbc.Button([
                    html.I(className="fas fa-download me-2"),
                    "Exportar"
                ], id="btn-exportar-entrenamientos", color="success", outline=True)
            ]
        ),
        
        # Estadísticas de entrenamientos
        create_entrenamientos_stats_section(),
        
        # Filtros
        create_entrenamientos_filters(),
        
        # Lista de entrenamientos
        create_entrenamientos_list(),
        
        # Modal para nuevo entrenamiento
        create_entrenamiento_modal(),
        
        # Modal para ver/editar asistencia
        create_asistencia_modal(),
        
        # Modal de estadísticas
        create_stats_modal(),
        
        # Stores
        dcc.Store(id="entrenamientos-data"),
        dcc.Store(id="entrenamiento-selected"),
        dcc.Store(id="jugadores-for-training")
    ])

def create_entrenamientos_stats_section():
    """Crea la sección de estadísticas de entrenamientos"""
    return dbc.Row([
        dbc.Col([
            create_stats_card(
                "Total Entrenamientos",
                "0",
                "fas fa-running",
                "primary",
                "Esta temporada"
            )
        ], width=6, md=3, className="mb-3"),
        
        dbc.Col([
            create_stats_card(
                "Este Mes",
                "0",
                "fas fa-calendar-alt",
                "success",
                "entrenamientos"
            )
        ], width=6, md=3, className="mb-3"),
        
        dbc.Col([
            create_stats_card(
                "Asistencia Media",
                "0%",
                "fas fa-percentage",
                "info",
                "del equipo"
            )
        ], width=6, md=3, className="mb-3"),
        
        dbc.Col([
            create_stats_card(
                "Último Entrenamiento",
                "0",
                "fas fa-clock",
                "warning",
                "días atrás"
            )
        ], width=6, md=3, className="mb-3")
    ], className="mb-4", id="entrenamientos-stats-row")

def create_entrenamientos_filters():
    """Crea los filtros para entrenamientos"""
    return dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Fecha Desde"),
                    dbc.Input(
                        id="filter-fecha-desde-ent",
                        type="date",
                        value=(datetime.now().replace(day=1)).strftime("%Y-%m-%d")
                    )
                ], width=12, md=3),
                
                dbc.Col([
                    dbc.Label("Fecha Hasta"),
                    dbc.Input(
                        id="filter-fecha-hasta-ent",
                        type="date",
                        value=datetime.now().strftime("%Y-%m-%d")
                    )
                ], width=12, md=3),
                
                dbc.Col([
                    dbc.Label("Buscar"),
                    dbc.InputGroup([
                        dbc.Input(
                            id="search-entrenamientos",
                            placeholder="Buscar por número o fecha...",
                            type="search"
                        ),
                        dbc.Button(
                            html.I(className="fas fa-search"),
                            id="btn-search-entrenamientos",
                            color="outline-secondary"
                        )
                    ])
                ], width=12, md=4),
                
                dbc.Col([
                    dbc.Label("Acciones"),
                    html.Br(),
                    dbc.Button([
                        html.I(className="fas fa-sync me-2"),
                        "Actualizar"
                    ], id="btn-refresh-entrenamientos", color="outline-primary", className="w-100")
                ], width=12, md=2)
            ])
        ])
    ], className="mb-4")

def create_entrenamientos_list():
    """Crea la lista de entrenamientos"""
    return dbc.Card([
        dbc.CardHeader([
            html.H5([
                html.I(className="fas fa-list me-2"),
                "Historial de Entrenamientos"
            ], className="mb-0 text-white")
        ]),
        dbc.CardBody([
            html.Div(id="entrenamientos-list-container")
        ])
    ], className="content-card")

def create_entrenamiento_modal():
    """Crea el modal para nuevo entrenamiento"""
    return dbc.Modal([
        dbc.ModalHeader([
            dbc.ModalTitle(id="entrenamiento-modal-title")
        ]),
        dbc.ModalBody([
            dbc.Form([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Fecha del Entrenamiento *"),
                        dbc.Input(
                            id="input-fecha-entrenamiento",
                            type="date",
                            value=datetime.now().strftime("%Y-%m-%d")
                        )
                    ], width=6),
                    dbc.Col([
                        dbc.Label("Número de Entrenamiento"),
                        dbc.Input(
                            id="input-numero-entrenamiento",
                            type="number",
                            disabled=True,
                            placeholder="Se asigna automáticamente"
                        )
                    ], width=6)
                ], className="mb-3"),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Observaciones"),
                        dbc.Textarea(
                            id="input-observaciones-entrenamiento",
                            placeholder="Observaciones generales del entrenamiento (opcional)",
                            rows=3
                        )
                    ], width=12)
                ], className="mb-3"),
                
                html.Hr(),
                
                html.H6("Control de Asistencia", className="mb-3"),
                
                # Aquí se cargarán dinámicamente los jugadores
                html.Div(id="asistencia-form-container")
            ])
        ]),
        dbc.ModalFooter([
            dbc.Button("Cancelar", id="btn-cancel-entrenamiento", color="secondary", outline=True),
            dbc.Button("Guardar Entrenamiento", id="btn-save-entrenamiento", color="primary")
        ])
    ], id="entrenamiento-modal", size="xl", is_open=False)

def create_asistencia_modal():
    """Crea el modal para ver/editar asistencia"""
    return dbc.Modal([
        dbc.ModalHeader([
            dbc.ModalTitle(id="asistencia-modal-title")
        ]),
        dbc.ModalBody([
            html.Div(id="asistencia-details-container")
        ]),
        dbc.ModalFooter([
            dbc.Button("Editar", id="btn-edit-asistencia", color="primary", outline=True),
            dbc.Button("Cerrar", id="btn-close-asistencia", color="secondary")
        ])
    ], id="asistencia-modal", size="lg", is_open=False)

def create_stats_modal():
    """Crea el modal de estadísticas"""
    return dbc.Modal([
        dbc.ModalHeader([
            dbc.ModalTitle("Estadísticas de Entrenamientos")
        ]),
        dbc.ModalBody([
            html.Div(id="stats-entrenamientos-container")
        ]),
        dbc.ModalFooter([
            dbc.Button("Cerrar", id="btn-close-stats", color="secondary")
        ])
    ], id="stats-modal", size="xl", is_open=False)

def create_asistencia_form(jugadores):
    """Crea el formulario de asistencia para jugadores"""
    if not jugadores:
        return html.P("No hay jugadores registrados", className="text-muted text-center")
    
    form_items = []
    
    for jugador in jugadores:
        form_items.append(
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H6(jugador.nombre_futbolistico, className="mb-1"),
                            html.Small(f"{jugador.nombre} {jugador.apellidos}", className="text-muted")
                        ], width=4),
                        
                        dbc.Col([
                            dbc.RadioItems(
                                id=f"asistencia-{jugador.id}",
                                options=[
                                    {"label": "Entrena", "value": "entrena"},
                                    {"label": "No entrena", "value": "no_entrena"}
                                ],
                                value="entrena",
                                inline=True
                            )
                        ], width=4),
                        
                        dbc.Col([
                            dbc.Select(
                                id=f"razon-{jugador.id}",
                                options=[{"label": "Seleccionar razón", "value": ""}] +
                                       [{"label": razon, "value": razon} for razon in RAZONES_AUSENCIA],
                                disabled=True,
                                size="sm"
                            )
                        ], width=4)
                    ], align="center"),
                    
                    dbc.Collapse([
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Observaciones", size="sm"),
                                dbc.Input(
                                    id=f"obs-{jugador.id}",
                                    placeholder="Observaciones específicas...",
                                    size="sm"
                                )
                            ], width=12)
                        ], className="mt-2")
                    ], id=f"obs-collapse-{jugador.id}", is_open=False)
                ])
            ], className="mb-2", size="sm")
        )
    
    return html.Div(form_items)

def create_entrenamientos_table(data):
    """Crea la tabla de entrenamientos"""
    if not data:
        return html.P("No hay entrenamientos registrados", className="text-center text-muted p-4")
    
    # Crear filas para la tabla
    table_rows = []
    
    for ent in data:
        # Calcular estadísticas de asistencia
        total_jugadores = len(ent.get('asistencias', []))
        asistentes = len([a for a in ent.get('asistencias', []) if a.get('entrena', False)])
        porcentaje = round((asistentes / total_jugadores * 100) if total_jugadores > 0 else 0)
        
        # Crear badges para el estado
        if porcentaje >= 90:
            badge_color = "success"
        elif porcentaje >= 70:
            badge_color = "warning"
        else:
            badge_color = "danger"
        
        table_rows.append(
            html.Tr([
                html.Td(f"#{ent['numero_entrenamiento']}", className="fw-bold"),
                html.Td(ent['fecha']),
                html.Td(f"{asistentes}/{total_jugadores}"),
                html.Td([
                    dbc.Badge(f"{porcentaje}%", color=badge_color, className="me-2"),
                    dbc.Progress(value=porcentaje, color=badge_color, size="sm")
                ]),
                html.Td([
                    dbc.ButtonGroup([
                        dbc.Button(
                            html.I(className="fas fa-eye"),
                            id={"type": "btn-view-training", "index": ent['id']},
                            color="info",
                            size="sm",
                            outline=True
                        ),
                        dbc.Button(
                            html.I(className="fas fa-edit"),
                            id={"type": "btn-edit-training", "index": ent['id']},
                            color="primary",
                            size="sm",
                            outline=True
                        )
                    ], size="sm")
                ])
            ])
        )
    
    return dbc.Table([
        html.Thead([
            html.Tr([
                html.Th("Nº"),
                html.Th("Fecha"),
                html.Th("Asistencia"),
                html.Th("Porcentaje"),
                html.Th("Acciones")
            ])
        ]),
        html.Tbody(table_rows)
    ], striped=True, hover=True, responsive=True)

# Callbacks para entrenamientos
def register_entrenamientos_callbacks():
    """Registra todos los callbacks de entrenamientos"""
    
    @callback(
        [Output("entrenamientos-data", "data"),
         Output("jugadores-for-training", "data")],
        [Input("btn-refresh-entrenamientos", "n_clicks"),
         Input("filter-fecha-desde-ent", "value"),
         Input("filter-fecha-hasta-ent", "value")],
        prevent_initial_call=False
    )
    def load_entrenamientos_data(n_clicks, fecha_desde, fecha_hasta):
        """Carga los datos de entrenamientos y jugadores"""
        try:
            with DatabaseManager() as db:
                # Cargar entrenamientos
                entrenamientos = db.get_entrenamientos()
                
                ent_data = []
                for ent in entrenamientos:
                    # Filtrar por fechas
                    if fecha_desde:
                        if ent.fecha < datetime.strptime(fecha_desde, "%Y-%m-%d").date():
                            continue
                    
                    if fecha_hasta:
                        if ent.fecha > datetime.strptime(fecha_hasta, "%Y-%m-%d").date():
                            continue
                    
                    # Cargar asistencias
                    asistencias = db.db.query(AsistenciaEntrenamiento).filter(
                        AsistenciaEntrenamiento.entrenamiento_id == ent.id
                    ).all()
                    
                    asistencias_data = []
                    for asist in asistencias:
                        jugador = db.get_jugador_by_id(asist.jugador_id)
                        asistencias_data.append({
                            'jugador_id': asist.jugador_id,
                            'jugador_nombre': jugador.nombre_futbolistico if jugador else 'Desconocido',
                            'entrena': asist.entrena,
                            'razon_ausencia': asist.razon_ausencia,
                            'observaciones': asist.observaciones
                        })
                    
                    ent_data.append({
                        'id': ent.id,
                        'numero_entrenamiento': ent.numero_entrenamiento,
                        'fecha': ent.fecha.strftime("%d/%m/%Y"),
                        'observaciones': ent.observaciones,
                        'asistencias': asistencias_data
                    })
                
                # Cargar jugadores activos
                jugadores = db.get_jugadores(activos_solo=True)
                jugadores_data = [
                    {
                        'id': j.id,
                        'nombre_futbolistico': j.nombre_futbolistico,
                        'nombre': j.nombre,
                        'apellidos': j.apellidos
                    } for j in jugadores
                ]
                
                return sorted(ent_data, key=lambda x: x['numero_entrenamiento'], reverse=True), jugadores_data
                
        except Exception as e:
            print(f"Error cargando entrenamientos: {e}")
            return [], []
    
    @callback(
        Output("entrenamientos-list-container", "children"),
        [Input("entrenamientos-data", "data"),
         Input("search-entrenamientos", "value")]
    )
    def update_entrenamientos_list(data, search_term):
        """Actualiza la lista de entrenamientos"""
        filtered_data = data
        
        if search_term:
            filtered_data = [
                ent for ent in data
                if search_term.lower() in str(ent['numero_entrenamiento']).lower() or
                   search_term.lower() in ent['fecha'].lower()
            ]
        
        return create_entrenamientos_table(filtered_data)
    
    @callback(
        [Output("entrenamiento-modal", "is_open"),
         Output("entrenamiento-modal-title", "children"),
         Output("input-numero-entrenamiento", "value")],
        [Input("btn-nuevo-entrenamiento", "n_clicks"),
         Input("btn-cancel-entrenamiento", "n_clicks"),
         Input("btn-save-entrenamiento", "n_clicks")],
        [State("entrenamiento-modal", "is_open")],
        prevent_initial_call=True
    )
    def toggle_entrenamiento_modal(btn_nuevo, btn_cancel, btn_save, is_open):
        """Controla la apertura/cierre del modal de entrenamiento"""
        from dash.callback_context import triggered
        
        if not triggered:
            return is_open, "Nuevo Entrenamiento", None
        
        trigger_id = triggered[0]['prop_id'].split('.')[0]
        
        if trigger_id == "btn-nuevo-entrenamiento":
            # Obtener siguiente número de entrenamiento
            try:
                with DatabaseManager() as db:
                    next_number = db.get_siguiente_numero_entrenamiento()
                return True, "Nuevo Entrenamiento", next_number
            except:
                return True, "Nuevo Entrenamiento", 1
        elif trigger_id in ["btn-cancel-entrenamiento", "btn-save-entrenamiento"]:
            return False, "Nuevo Entrenamiento", None
        
        return is_open, "Nuevo Entrenamiento", None
    
    @callback(
        Output("asistencia-form-container", "children"),
        Input("jugadores-for-training", "data")
    )
    def update_asistencia_form(jugadores_data):
        """Actualiza el formulario de asistencia"""
        if not jugadores_data:
            return html.P("No hay jugadores disponibles", className="text-muted")
        
        # Simular objetos jugador para la función
        class MockJugador:
            def __init__(self, data):
                self.id = data['id']
                self.nombre_futbolistico = data['nombre_futbolistico']
                self.nombre = data['nombre']
                self.apellidos = data['apellidos']
        
        jugadores = [MockJugador(j) for j in jugadores_data]
        return create_asistencia_form(jugadores)

# Registrar callbacks al importar
register_entrenamientos_callbacks()