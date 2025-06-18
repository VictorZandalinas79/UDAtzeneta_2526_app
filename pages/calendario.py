# pages/calendario.py - VERSIÓN SUPER DEBUG

import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State, callback, dash_table, no_update
import pandas as pd
from datetime import datetime, date, timedelta
from database.db_manager import DatabaseManager, Calendario
from layouts.main_content import create_stats_card
from config.settings import COLORS, COMPETICIONES
from utils.header_utils import create_page_header

print("🔄 CALENDARIO: Iniciando importaciones...")

# Importar scraping con fallback
try:
    from utils.scraping import scraping_manager, FFCVScraper
    SCRAPING_AVAILABLE = True
    print("✅ CALENDARIO: Scraping manager importado correctamente")
except ImportError as e:
    SCRAPING_AVAILABLE = False
    print(f"❌ CALENDARIO: Error importando scraping: {e}")

print("✅ CALENDARIO: Todas las importaciones completadas")

def create_calendario_layout():
    """Crea el layout principal de la página de calendario"""
    print("🔄 CALENDARIO: Creando layout...")
    
    layout = html.Div([
        # MENSAJE DE DEBUG VISIBLE
        dbc.Alert([
            html.H5("🔍 Modo Debug Activado"),
            html.P(id="debug-messages", children="Iniciando sistema..."),
            html.Small(f"Timestamp: {datetime.now().strftime('%H:%M:%S')}")
        ], color="info", className="mb-3"),
        
        # HEADER SIMPLIFICADO
        dbc.Row([
            dbc.Col([
                html.H2([
                    html.I(className="fas fa-calendar me-2"),
                    "Calendario de Partidos"
                ]),
                html.P("Gestiona todos los partidos de la temporada", className="text-muted")
            ], width=8),
            dbc.Col([
                dbc.ButtonGroup([
                    dbc.Button([
                        html.I(className="fas fa-sync me-2"),
                        "Forzar Recarga"
                    ], id="btn-forzar-recarga", color="primary"),
                    dbc.Button([
                        html.I(className="fas fa-download me-2"),
                        "Importar FFCV"
                    ], id="btn-scraping", color="success", outline=True)
                ])
            ], width=4, className="text-end")
        ], className="mb-4"),
        
        # CONTADOR DE EJECUCIONES
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("📊 Estado de Callbacks"),
                        html.P(id="callback-counter", children="Esperando ejecución..."),
                        html.P(id="last-update", children="Nunca ejecutado")
                    ])
                ])
            ], width=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("💾 Estado de Base de Datos"),
                        html.P(id="db-status", children="No verificado"),
                        html.P(id="db-details", children="")
                    ])
                ])
            ], width=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("🌐 Estado de Scraping"),
                        html.P(f"Disponible: {'✅' if SCRAPING_AVAILABLE else '❌'}"),
                        html.P(id="scraping-status", children="No ejecutado")
                    ])
                ])
            ], width=4)
        ], className="mb-4"),
        
        # DATOS RAW VISIBLES
        dbc.Card([
            dbc.CardHeader([
                html.H5("📋 Datos Raw del Calendario")
            ]),
            dbc.CardBody([
                html.Pre(id="raw-data-display", children="Esperando datos...", style={
                    'backgroundColor': '#f8f9fa',
                    'padding': '15px',
                    'borderRadius': '5px',
                    'fontSize': '12px',
                    'maxHeight': '300px',
                    'overflow': 'auto'
                })
            ])
        ], className="mb-4"),
        
        # TABLA SIMPLIFICADA
        dbc.Card([
            dbc.CardHeader([
                html.H5("📅 Tabla de Partidos")
            ]),
            dbc.CardBody([
                html.Div(id="tabla-simple", children="Esperando datos de la tabla...")
            ])
        ]),
        
        # MODAL SIMPLE
        create_super_simple_modal(),
        
        # STORES Y COMPONENTES
        dcc.Store(id="calendario-data", data={"inicializado": False}),
        dcc.Store(id="execution-counter", data=0),
        dcc.Interval(
            id="debug-interval", 
            interval=2000,  # Cada 2 segundos
            n_intervals=0,
            max_intervals=5  # Solo 5 veces para no sobrecargar
        )
    ])
    
    print("✅ CALENDARIO: Layout creado correctamente")
    return layout

def create_super_simple_modal():
    """Modal súper simple"""
    return dbc.Modal([
        dbc.ModalHeader("Importar FFCV"),
        dbc.ModalBody([
            html.P("URL de FFCV:"),
            dbc.Input(
                id="ffcv-url-input",
                value="https://resultadosffcv.isquad.es/equipo_calendario.php?id_temp=20&id_modalidad=33327&id_competicion=903498407&id_equipo=18331&torneo_equipo=903498408&id_torneo=903498408"
            )
        ]),
        dbc.ModalFooter([
            dbc.Button("Cancelar", id="modal-cancel", color="secondary"),
            dbc.Button("Importar", id="modal-import", color="success")
        ])
    ], id="import-modal", is_open=False)

# CALLBACKS SUPER SIMPLIFICADOS CON LOGGING EXTREMO
def register_calendario_callbacks():
    """Registra callbacks súper simplificados con logging extremo"""
    
    print("🔄 CALENDARIO: Iniciando registro de callbacks...")
    
    try:
        # CALLBACK PRINCIPAL: Cargar datos
        @callback(
            [Output("calendario-data", "data"),
             Output("callback-counter", "children"),
             Output("last-update", "children"),
             Output("db-status", "children"),
             Output("db-details", "children"),
             Output("debug-messages", "children")],
            [Input("debug-interval", "n_intervals"),
             Input("btn-forzar-recarga", "n_clicks"),
             Input("execution-counter", "data")],
            prevent_initial_call=False
        )
        def main_callback(n_intervals, btn_clicks, counter):
            """Callback principal súper simplificado"""
            
            timestamp = datetime.now().strftime('%H:%M:%S')
            execution_num = (counter if counter else 0) + 1
            
            print(f"🔥 [MAIN CALLBACK] ===== EJECUCIÓN #{execution_num} - {timestamp} =====")
            print(f"🔥 [MAIN CALLBACK] n_intervals: {n_intervals}")
            print(f"🔥 [MAIN CALLBACK] btn_clicks: {btn_clicks}")
            
            try:
                # Test de base de datos
                print("🔄 [MAIN CALLBACK] Conectando a base de datos...")
                with DatabaseManager() as db:
                    calendario = db.get_calendario()
                    num_partidos = len(calendario) if calendario else 0
                    
                    print(f"📊 [MAIN CALLBACK] Partidos en BD: {num_partidos}")
                    
                    data = []
                    if calendario:
                        for i, evento in enumerate(calendario):
                            data.append({
                                'id': evento.id,
                                'fecha': evento.fecha.strftime("%d/%m/%Y") if evento.fecha else "Sin fecha",
                                'local': evento.equipo_local or "Sin equipo local",
                                'visitante': evento.equipo_visitante or "Sin equipo visitante",
                                'competicion': evento.competicion or "Sin competición"
                            })
                            
                            if i < 3:  # Solo log de los primeros 3
                                print(f"📋 [MAIN CALLBACK] Partido {i+1}: {data[-1]}")
                    
                    # Preparar respuestas
                    callback_info = f"✅ Ejecutado {execution_num} veces"
                    last_update_info = f"🕐 Última actualización: {timestamp}"
                    db_status_info = f"✅ {num_partidos} partidos encontrados"
                    db_details_info = f"Primera ejecución: {timestamp}" if execution_num == 1 else f"Última verificación: {timestamp}"
                    debug_msg = f"[{timestamp}] Callback ejecutado correctamente. Datos cargados: {len(data)} partidos"
                    
                    print(f"✅ [MAIN CALLBACK] Enviando {len(data)} partidos al frontend")
                    
                    return (
                        {"partidos": data, "timestamp": timestamp, "execution": execution_num},
                        callback_info,
                        last_update_info,
                        db_status_info,
                        db_details_info,
                        debug_msg
                    )
                    
            except Exception as e:
                error_msg = f"❌ Error en callback: {str(e)}"
                print(f"❌ [MAIN CALLBACK ERROR] {error_msg}")
                import traceback
                traceback.print_exc()
                
                return (
                    {"error": error_msg, "timestamp": timestamp},
                    f"❌ Error en ejecución #{execution_num}",
                    f"🕐 Error en: {timestamp}",
                    "❌ Error de conexión",
                    error_msg,
                    f"[{timestamp}] ERROR: {error_msg}"
                )
        
        # CALLBACK SECUNDARIO: Mostrar datos raw
        @callback(
            Output("raw-data-display", "children"),
            Input("calendario-data", "data"),
            prevent_initial_call=False
        )
        def show_raw_data(data):
            """Muestra los datos raw tal como llegan"""
            
            timestamp = datetime.now().strftime('%H:%M:%S')
            print(f"🔍 [RAW DATA] Actualizando datos raw - {timestamp}")
            print(f"🔍 [RAW DATA] Tipo de data: {type(data)}")
            print(f"🔍 [RAW DATA] Contenido: {str(data)[:200]}...")
            
            if not data:
                return f"[{timestamp}] Sin datos recibidos"
            
            if isinstance(data, dict) and 'error' in data:
                return f"[{timestamp}] ERROR: {data['error']}"
            
            if isinstance(data, dict) and 'partidos' in data:
                partidos = data['partidos']
                output = f"[{timestamp}] DATOS RECIBIDOS:\n"
                output += f"Número de partidos: {len(partidos)}\n"
                output += f"Timestamp: {data.get('timestamp', 'No timestamp')}\n"
                output += f"Ejecución: {data.get('execution', 'No execution')}\n\n"
                
                if partidos:
                    output += "PRIMEROS PARTIDOS:\n"
                    for i, partido in enumerate(partidos[:3]):
                        output += f"{i+1}. {partido}\n"
                else:
                    output += "NO HAY PARTIDOS\n"
                
                return output
            
            return f"[{timestamp}] Datos en formato inesperado: {str(data)}"
        
        # CALLBACK TERCIARIO: Mostrar tabla
        @callback(
            Output("tabla-simple", "children"),
            Input("calendario-data", "data"),
            prevent_initial_call=False
        )
        def show_simple_table(data):
            """Muestra una tabla súper simple"""
            
            timestamp = datetime.now().strftime('%H:%M:%S')
            print(f"📊 [TABLE] Actualizando tabla - {timestamp}")
            
            if not data or not isinstance(data, dict) or 'partidos' not in data:
                return dbc.Alert(f"[{timestamp}] Sin datos para la tabla", color="warning")
            
            partidos = data['partidos']
            
            if not partidos:
                return dbc.Alert(f"[{timestamp}] Lista de partidos vacía", color="info")
            
            print(f"📊 [TABLE] Creando tabla con {len(partidos)} partidos")
            
            # Crear tabla HTML simple
            filas = []
            for partido in partidos:
                fila = html.Tr([
                    html.Td(partido.get('fecha', 'Sin fecha')),
                    html.Td(partido.get('local', 'Sin local')),
                    html.Td("vs"),
                    html.Td(partido.get('visitante', 'Sin visitante')),
                    html.Td(partido.get('competicion', 'Sin competición'))
                ])
                filas.append(fila)
            
            tabla = html.Table([
                html.Thead([
                    html.Tr([
                        html.Th("Fecha"),
                        html.Th("Local"),
                        html.Th(""),
                        html.Th("Visitante"),
                        html.Th("Competición")
                    ])
                ]),
                html.Tbody(filas)
            ], className="table table-striped")
            
            return html.Div([
                html.P(f"✅ Tabla actualizada a las {timestamp} con {len(partidos)} partidos"),
                tabla
            ])
        
        # CALLBACK MODAL
        @callback(
            Output("import-modal", "is_open"),
            [Input("btn-scraping", "n_clicks"),
             Input("modal-cancel", "n_clicks"),
             Input("modal-import", "n_clicks")],
            State("import-modal", "is_open"),
            prevent_initial_call=True
        )
        def toggle_modal(btn_open, btn_cancel, btn_import, is_open):
            """Control del modal"""
            from dash import callback_context
            
            if callback_context.triggered:
                trigger_id = callback_context.triggered[0]['prop_id'].split('.')[0]
                print(f"🔄 [MODAL] Trigger: {trigger_id}")
                
                if trigger_id == "btn-scraping":
                    return True
                elif trigger_id in ["modal-cancel", "modal-import"]:
                    return False
            
            return is_open
        
        # CALLBACK COUNTER
        @callback(
            Output("execution-counter", "data"),
            Input("debug-interval", "n_intervals"),
            State("execution-counter", "data"),
            prevent_initial_call=False
        )
        def update_counter(n_intervals, current_counter):
            """Actualiza contador de ejecuciones"""
            new_counter = (current_counter if current_counter else 0) + 1
            print(f"🔢 [COUNTER] Actualizando contador: {new_counter}")
            return new_counter
        
        print("✅ CALENDARIO: Todos los callbacks registrados correctamente")
        
    except Exception as e:
        print(f"❌ CALENDARIO: Error registrando callbacks: {e}")
        import traceback
        traceback.print_exc()
        raise

# Función para app.py
def setup_calendario_callbacks(app):
    """Configura los callbacks del calendario"""
    print("🔧 CALENDARIO: Configurando callbacks SUPER DEBUG...")
    register_calendario_callbacks()
    print("✅ CALENDARIO: Configuración de callbacks completada")

# Layout por defecto
print("🔄 CALENDARIO: Creando layout por defecto...")
layout = create_calendario_layout()
print("✅ CALENDARIO: Layout por defecto creado")