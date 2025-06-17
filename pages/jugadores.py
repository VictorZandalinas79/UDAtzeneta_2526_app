import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State, callback, dash_table, no_update
import pandas as pd
from datetime import datetime, date
from database.db_manager import DatabaseManager, Jugador, PesoJugador
from layouts.main_content import create_stats_card
from config.settings import COLORS, POSICIONES
from utils.header_utils import create_page_header

def create_jugadores_layout():
    """Crea el layout principal de la página de jugadores"""
    return html.Div([
        # Header de la página con el escudo del equipo
        create_page_header(
            title="Gestión de Jugadores",
            subtitle="Administra la plantilla del UD Atzeneta",
            actions=[
                dbc.Button([
                    html.I(className="fas fa-user-plus me-2"),
                    "Nuevo Jugador"
                ], id="btn-nuevo-jugador", color="primary"),
                dbc.Button([
                    html.I(className="fas fa-download me-2"),
                    "Exportar"
                ], id="btn-exportar-jugadores", color="success", outline=True)
            ]
        ),
        
        # Estadísticas rápidas
        create_jugadores_stats_section(),
        
        # Filtros y búsqueda
        create_jugadores_filters(),
        
        # Tabla de jugadores
        create_jugadores_table(),
        
        # Modal para nuevo/editar jugador
        create_jugador_modal(),
        
        # Modal para ver detalles del jugador
        create_jugador_details_modal(),
        
        # Store para datos
        dcc.Store(id="jugadores-data"),
        dcc.Store(id="jugador-selected")
    ])

def create_jugadores_stats_section():
    """Crea la sección de estadísticas de jugadores"""
    return dbc.Row([
        dbc.Col([
            create_stats_card(
                "Total Jugadores",
                "0",
                "fas fa-users",
                "primary",
                "En plantilla"
            )
        ], width=6, md=3, className="mb-3"),
        
        dbc.Col([
            create_stats_card(
                "Promedio Edad",
                "0",
                "fas fa-birthday-cake",
                "info",
                "años"
            )
        ], width=6, md=3, className="mb-3"),
        
        dbc.Col([
            create_stats_card(
                "Total Goles",
                "0",
                "fas fa-futbol",
                "success",
                "esta temporada"
            )
        ], width=6, md=3, className="mb-3"),
        
        dbc.Col([
            create_stats_card(
                "Lesionados",
                "0",
                "fas fa-medkit",
                "warning",
                "actualmente"
            )
        ], width=6, md=3, className="mb-3")
    ], className="mb-4", id="jugadores-stats-row")

def create_jugadores_filters():
    """Crea los filtros para la tabla de jugadores"""
    return dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.InputGroup([
                        dbc.Input(
                            id="search-jugadores",
                            placeholder="Buscar por nombre, posición...",
                            type="search"
                        ),
                        dbc.Button(
                            html.I(className="fas fa-search"),
                            id="btn-search-jugadores",
                            color="outline-secondary"
                        )
                    ])
                ], width=12, md=4),
                
                dbc.Col([
                    dbc.Select(
                        id="filter-posicion",
                        options=[{"label": "Todas las posiciones", "value": "all"}] +
                               [{"label": pos, "value": pos} for pos in POSICIONES],
                        value="all"
                    )
                ], width=12, md=3),
                
                dbc.Col([
                    dbc.Select(
                        id="filter-estado",
                        options=[
                            {"label": "Todos", "value": "all"},
                            {"label": "Activos", "value": "active"},
                            {"label": "Inactivos", "value": "inactive"}
                        ],
                        value="active"
                    )
                ], width=12, md=3),
                
                dbc.Col([
                    dbc.Button([
                        html.I(className="fas fa-sync me-2"),
                        "Actualizar"
                    ], id="btn-refresh-jugadores", color="outline-primary", className="w-100")
                ], width=12, md=2)
            ])
        ])
    ], className="mb-4")

def create_jugadores_table():
    """Crea la tabla de jugadores"""
    return dbc.Card([
        dbc.CardHeader([
            html.H5([
                html.I(className="fas fa-table me-2"),
                "Lista de Jugadores"
            ], className="mb-0 text-white")
        ]),
        dbc.CardBody([
            html.Div(id="jugadores-table-container")
        ])
    ], className="content-card")

def create_jugador_modal():
    """Crea el modal para añadir/editar jugador"""
    return html.Div([
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Nuevo Jugador", id="jugador-modal-title")),
                dbc.ModalBody([
                    dbc.Tabs(
                        [
                            dbc.Tab(label="Datos Personales", tab_id="tab-personal"),
                            dbc.Tab(label="Datos Futbolísticos", tab_id="tab-futbol"),
                            dbc.Tab(label="Datos Físicos", tab_id="tab-fisico")
                        ],
                        id="jugador-tabs",
                        active_tab="tab-personal",
                        className="mb-3"
                    ),
                    html.Div(id="jugador-form-content")
                ]),
                dbc.ModalFooter([
                    dbc.Button(
                        "Cancelar",
                        id="btn-cancel-jugador",
                        color="secondary",
                        className="me-2"
                    ),
                    dbc.Button(
                        "Guardar",
                        id="btn-save-jugador",
                        color="primary"
                    )
                ])
            ],
            id="jugador-modal",
            is_open=False,
            size="lg",
            backdrop="static"
        )
    ])

def create_jugador_details_modal():
    """Crea el modal para ver detalles del jugador"""
    return dbc.Modal([
        dbc.ModalHeader([
            dbc.ModalTitle(id="jugador-details-title")
        ]),
        dbc.ModalBody([
            html.Div(id="jugador-details-content")
        ]),
        dbc.ModalFooter([
            dbc.Button("Editar", id="btn-edit-jugador", color="primary", outline=True),
            dbc.Button("Cerrar", id="btn-close-details", color="secondary")
        ])
    ], id="jugador-details-modal", size="xl", is_open=False)

def create_personal_form():
    """Crea el formulario de datos personales"""
    return [
        dbc.Row([
            dbc.Col([
                dbc.Label("Nombre Futbolístico *"),
                dbc.Input(id="input-nombre-futbolistico", placeholder="Ej: Ronaldinho")
            ], width=6),
            dbc.Col([
                dbc.Label("Dorsal"),
                dbc.Input(id="input-dorsal", type="number", min=1, max=99)
            ], width=6)
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Col([
                dbc.Label("Nombre *"),
                dbc.Input(id="input-nombre", placeholder="Nombre completo")
            ], width=6),
            dbc.Col([
                dbc.Label("Apellidos *"),
                dbc.Input(id="input-apellidos", placeholder="Apellidos completos")
            ], width=6)
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Col([
                dbc.Label("DNI"),
                dbc.Input(id="input-dni", placeholder="12345678A")
            ], width=6),
            dbc.Col([
                dbc.Label("Teléfono"),
                dbc.Input(id="input-telefono", placeholder="+34 600 000 000")
            ], width=6)
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Col([
                dbc.Label("Email"),
                dbc.Input(id="input-email", type="email", placeholder="jugador@email.com")
            ], width=12)
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Col([
                dbc.Label("Dirección"),
                dbc.Textarea(id="input-direccion", placeholder="Dirección completa")
            ], width=12)
        ])
    ]

def create_futbol_form():
    """Crea el formulario de datos futbolísticos"""
    return [
        dbc.Row([
            dbc.Col([
                dbc.Label("Posición *"),
                dbc.Select(
                    id="input-posicion",
                    options=[{"label": pos, "value": pos} for pos in POSICIONES]
                )
            ], width=6),
            dbc.Col([
                dbc.Label("Pierna Dominante"),
                dbc.Select(
                    id="input-pierna-dominante",
                    options=[
                        {"label": "Derecha", "value": "Derecha"},
                        {"label": "Izquierda", "value": "Izquierda"},
                        {"label": "Ambidiestro", "value": "Ambidiestro"}
                    ]
                )
            ], width=6)
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Col([
                dbc.Label("Goles"),
                dbc.Input(id="input-goles", type="number", min=0, value=0)
            ], width=4),
            dbc.Col([
                dbc.Label("Asistencias"),
                dbc.Input(id="input-asistencias", type="number", min=0, value=0)
            ], width=4),
            dbc.Col([
                dbc.Label("Minutos Jugados"),
                dbc.Input(id="input-minutos", type="number", min=0, value=0)
            ], width=4)
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Col([
                dbc.Label("Tarjetas Amarillas"),
                dbc.Input(id="input-tarjetas-amarillas", type="number", min=0, value=0)
            ], width=6),
            dbc.Col([
                dbc.Label("Tarjetas Rojas"),
                dbc.Input(id="input-tarjetas-rojas", type="number", min=0, value=0)
            ], width=6)
        ])
    ]

def create_fisico_form():
    """Crea el formulario de datos físicos"""
    return [
        dbc.Row([
            dbc.Col([
                dbc.Label("Altura (cm)"),
                dbc.Input(id="input-altura", type="number", min=150, max=220)
            ], width=6),
            dbc.Col([
                dbc.Label("Peso Actual (kg)"),
                dbc.Input(id="input-peso", type="number", min=50, max=150, step=0.1)
            ], width=6)
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Col([
                dbc.Label("Foto del Jugador"),
                dcc.Upload(
                    id="upload-foto",
                    children=html.Div([
                        html.I(className="fas fa-cloud-upload-alt fa-2x mb-2"),
                        html.P("Arrastra una imagen o haz clic para seleccionar")
                    ], className="text-center text-muted p-4 border border-dashed rounded"),
                    multiple=False,
                    accept="image/*"
                )
            ], width=12)
        ])
    ]

# Callbacks para la página de jugadores
def register_jugadores_callbacks():
    """Registra todos los callbacks de la página de jugadores"""
    
    @callback(
        Output("jugadores-data", "data"),
        [Input("btn-refresh-jugadores", "n_clicks"),
         Input("filter-estado", "value")],
        prevent_initial_call=False
    )
    def load_jugadores_data(n_clicks, estado_filter):
        """Carga los datos de jugadores"""
        try:
            with DatabaseManager() as db:
                if estado_filter == "active":
                    jugadores = db.get_jugadores(activos_solo=True)
                elif estado_filter == "inactive":
                    jugadores = [j for j in db.get_jugadores(activos_solo=False) if not j.activo]
                else:
                    jugadores = db.get_jugadores(activos_solo=False)
                
                data = []
                for j in jugadores:
                    data.append({
                        'id': j.id,
                        'nombre_futbolistico': j.nombre_futbolistico,
                        'nombre_completo': f"{j.nombre} {j.apellidos}",
                        'dorsal': j.dorsal or "-",
                        'posicion': j.posicion or "-",
                        'goles': j.goles,
                        'asistencias': j.asistencias,
                        'tarjetas_amarillas': j.tarjetas_amarillas,
                        'tarjetas_rojas': j.tarjetas_rojas,
                        'activo': j.activo
                    })
                
                return data
        except Exception as e:
            print(f"Error cargando jugadores: {e}")
            return []
    
    @callback(
        Output("jugadores-table-container", "children"),
        [Input("jugadores-data", "data"),
         Input("search-jugadores", "value"),
         Input("filter-posicion", "value")]
    )
    def update_jugadores_table(data, search_term, posicion_filter):
        """Actualiza la tabla de jugadores"""
        if not data:
            return html.P("No hay jugadores registrados", className="text-center text-muted p-4")
        
        # Filtrar datos
        filtered_data = data
        
        if search_term:
            filtered_data = [
                j for j in filtered_data 
                if search_term.lower() in j['nombre_futbolistico'].lower() or 
                   search_term.lower() in j['nombre_completo'].lower() or
                   search_term.lower() in (j['posicion'] or "").lower()
            ]
        
        if posicion_filter and posicion_filter != "all":
            filtered_data = [j for j in filtered_data if j['posicion'] == posicion_filter]
        
        # Crear DataFrame
        df = pd.DataFrame(filtered_data)
        
        return dash_table.DataTable(
            id="jugadores-table",
            data=df.to_dict('records'),
            columns=[
                {"name": "Dorsal", "id": "dorsal", "type": "text"},
                {"name": "Nombre", "id": "nombre_futbolistico", "type": "text"},
                {"name": "Posición", "id": "posicion", "type": "text"},
                {"name": "Goles", "id": "goles", "type": "numeric"},
                {"name": "Asistencias", "id": "asistencias", "type": "numeric"},
                {"name": "T.A.", "id": "tarjetas_amarillas", "type": "numeric"},
                {"name": "T.R.", "id": "tarjetas_rojas", "type": "numeric"},
                {"name": "Estado", "id": "activo", "type": "text"}
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
                    'if': {'filter_query': '{activo} = False'},
                    'backgroundColor': '#f8d7da',
                    'color': 'black',
                }
            ],
            row_selectable="single",
            page_size=10,
            sort_action="native",
            filter_action="native"
        )
    
    @callback(
        [Output("jugador-modal", "is_open"),
         Output("jugador-modal-title", "children"),
         Output("jugador-tabs", "active_tab")],
        [Input("btn-nuevo-jugador", "n_clicks"),
         Input("btn-cancel-jugador", "n_clicks"),
         Input("btn-save-jugador", "n_clicks")],
        [State("jugador-modal", "is_open")],
        prevent_initial_call=True
    )
    def toggle_jugador_modal(btn_nuevo, btn_cancel, btn_save, is_open):
        """Controla la apertura/cierre del modal de jugador"""
        import dash
        ctx = dash.callback_context
        
        print("\n=== toggle_jugador_modal llamado ===")
        print(f"btn_nuevo: {btn_nuevo}")
        print(f"btn_cancel: {btn_cancel}")
        print(f"btn_save: {btn_save}")
        print(f"is_open actual: {is_open}")
        
        if not ctx.triggered:
            print("No hay trigger identificado")
            return is_open, "Nuevo Jugador", "tab-personal"
            
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        print(f"Botón presionado: {button_id}")
        
        if button_id == "btn-nuevo-jugador":
            print("Abriendo modal de nuevo jugador")
            return True, "Nuevo Jugador", "tab-personal"
        elif button_id in ["btn-cancel-jugador", "btn-save-jugador"]:
            print("Cerrando modal de jugador")
            return False, "Nuevo Jugador", "tab-personal"
            
        print("Ninguna condición cumplida, retornando estado actual")
        return is_open, "Nuevo Jugador", "tab-personal"
    
    @callback(
        Output("jugador-form-content", "children"),
        Input("jugador-tabs", "active_tab")
    )
    def update_jugador_form_content(active_tab):
        """Actualiza el contenido del formulario según la pestaña activa"""
        if active_tab == "tab-personal":
            return create_personal_form()
        elif active_tab == "tab-futbol":
            return create_futbol_form()
        elif active_tab == "tab-fisico":
            return create_fisico_form()
        return []

    # Callback para guardar un nuevo jugador
    @callback(
        [Output("jugador-modal", "is_open", allow_duplicate=True),
         Output("jugadores-data", "data", allow_duplicate=True)],
        [Input("btn-save-jugador", "n_clicks")],
        [State("jugador-tabs", "active_tab"),
         State("jugador-form-content", "children")],
        prevent_initial_call=True
    )
    def save_jugador(n_clicks, active_tab, form_content):
        """Guarda un nuevo jugador en la base de datos"""
        from dash.exceptions import PreventUpdate
        
        if n_clicks is None or n_clicks == 0:
            raise PreventUpdate
            
        print(f"\n=== Intentando guardar jugador ===")
        
        # Obtener los valores de los inputs del formulario
        ctx = dash.callback_context
        inputs = {}
        
        # Obtener todos los inputs del formulario
        if form_content:
            from dash import dcc, html
            
            def get_input_values(component):
                if hasattr(component, 'children') and component.children:
                    if isinstance(component.children, list):
                        for child in component.children:
                            get_input_values(child)
                    else:
                        get_input_values(component.children)
                
                if hasattr(component, 'id'):
                    component_id = component.id
                    if isinstance(component_id, dict):
                        component_id = component_id.get('type')
                    if component_id:
                        value = ctx.states.get(f"{component_id}.value")
                        if value is not None:
                            inputs[component_id] = value
            
            get_input_values(form_content)
        
        print("Valores del formulario:", inputs)
        
        # Validar campos requeridos
        required_fields = ['input-nombre', 'input-apellidos']
        for field in required_fields:
            if field not in inputs or not inputs[field]:
                print(f"Error: El campo {field} es requerido")
                return dash.no_update, dash.no_update
        
        try:
            # Crear el objeto Jugador con los valores por defecto
            jugador = Jugador(
                nombre=inputs.get('input-nombre', ''),
                apellidos=inputs.get('input-apellidos', ''),
                dni=inputs.get('input-dni'),
                telefono=inputs.get('input-telefono'),
                email=inputs.get('input-email'),
                direccion=inputs.get('input-direccion'),
                dorsal=inputs.get('input-dorsal'),
                posicion=inputs.get('input-posicion'),
                peso=float(inputs['input-peso']) if inputs.get('input-peso') else None,
                altura=float(inputs['input-altura']) if inputs.get('input-altura') else None,
                goles=int(inputs.get('input-goles', 0)) if inputs.get('input-goles') is not None else 0,
                asistencias=int(inputs.get('input-asistencias', 0)) if inputs.get('input-asistencias') is not None else 0,
                tarjetas_amarillas=int(inputs.get('input-tarjetas-amarillas', 0)) if inputs.get('input-tarjetas-amarillas') is not None else 0,
                tarjetas_rojas=int(inputs.get('input-tarjetas-rojas', 0)) if inputs.get('input-tarjetas-rojas') is not None else 0,
                activo=True
            )
            
            # Guardar en la base de datos
            with DatabaseManager() as db:
                db.save(jugador)
                db.commit()
                print(f"Jugador guardado con ID: {jugador.id}")
                
                # Obtener la lista actualizada de jugadores
                jugadores = db.get_jugadores(activos_solo=True)
                jugadores_data = [{
                    'id': j.id,
                    'nombre_futbolistico': j.nombre_futbolistico,
                    'nombre_completo': f"{j.nombre} {j.apellidos}",
                    'dorsal': j.dorsal or "-",
                    'posicion': j.posicion or "-",
                    'goles': j.goles or 0,
                    'asistencias': j.asistencias or 0,
                    'tarjetas_amarillas': j.tarjetas_amarillas or 0,
                    'tarjetas_rojas': j.tarjetas_rojas or 0,
                    'activo': j.activo
                } for j in jugadores]
                
                return False, jugadores_data
                
        except Exception as e:
            print(f"Error al guardar el jugador: {str(e)}")
            import traceback
            traceback.print_exc()
            return dash.no_update, dash.no_update

# Registrar callbacks al importar
register_jugadores_callbacks()

# Definir el layout de la página de jugadores
layout = create_jugadores_layout()