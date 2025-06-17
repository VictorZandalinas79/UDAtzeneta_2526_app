import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, callback
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
from database.db_manager import DatabaseManager
from layouts.main_content import create_page_header, create_stats_card
from config.settings import COLORS

def create_dashboard_layout():
    """Crea el layout del dashboard principal"""
    return html.Div([
        # Header de la página
        dbc.Row([
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
                        html.H1("Dashboard", className="mb-1", style={'fontWeight': 'bold'}),
                        html.P("Resumen general del equipo UD Atzeneta", className="text-muted mb-0")
                    ])
                ], className="d-flex align-items-center")
            ], width="auto"),
            dbc.Col([
                html.Div([
                    dbc.Button([
                        html.I(className="fas fa-sync-alt me-2"),
                        "Actualizar"
                    ], id="refresh-dashboard", color="primary", outline=True, className="me-2"),
                    dbc.Button([
                        html.I(className="fas fa-download me-2"),
                        "Exportar"
                    ], id="export-dashboard", color="success", outline=True)
                ], className="d-flex justify-content-end")
            ])
        ], className="mb-4"),
        
        # Tarjetas de estadísticas principales
        create_main_stats_section(),
        
        # Sección de gráficos
        dbc.Row([
            dbc.Col([
                create_calendar_overview_card()
            ], width=12, lg=6),
            dbc.Col([
                create_team_performance_card()
            ], width=12, lg=6)
        ], className="mb-4"),
        
        # Sección de actividad reciente
        dbc.Row([
            dbc.Col([
                create_recent_activity_card()
            ], width=12, lg=8),
            dbc.Col([
                create_quick_actions_card()
            ], width=12, lg=4)
        ])
    ])

def create_main_stats_section():
    """Crea la sección de estadísticas principales"""
    return dbc.Row([
        dbc.Col([
            create_stats_card(
                "Jugadores Activos",
                "0",
                "fas fa-users",
                "primary",
                "En plantilla"
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
                "Entrenamientos",
                "0",
                "fas fa-running",
                "info",
                "este mes"
            )
        ], width=6, md=3, className="mb-3"),
        
        dbc.Col([
            create_stats_card(
                "Multas Pendientes",
                "€0",
                "fas fa-euro-sign",
                "warning",
                "por cobrar"
            )
        ], width=6, md=3, className="mb-3")
    ], className="mb-4", id="main-stats-row")

def create_calendar_overview_card():
    """Crea la tarjeta de resumen del calendario"""
    return dbc.Card([
        dbc.CardHeader([
            html.H5([
                html.I(className="fas fa-calendar-alt me-2"),
                "Próximos Partidos"
            ], className="mb-0 text-white")
        ]),
        dbc.CardBody([
            html.Div(id="calendar-overview-content"),
            dcc.Graph(id="calendar-chart", config={'displayModeBar': False})
        ])
    ], className="content-card h-100")

def create_team_performance_card():
    """Crea la tarjeta de rendimiento del equipo"""
    return dbc.Card([
        dbc.CardHeader([
            html.H5([
                html.I(className="fas fa-chart-line me-2"),
                "Rendimiento del Equipo"
            ], className="mb-0 text-white")
        ]),
        dbc.CardBody([
            dcc.Graph(id="performance-chart", config={'displayModeBar': False})
        ])
    ], className="content-card h-100")

def create_recent_activity_card():
    """Crea la tarjeta de actividad reciente"""
    return dbc.Card([
        dbc.CardHeader([
            html.H5([
                html.I(className="fas fa-clock me-2"),
                "Actividad Reciente"
            ], className="mb-0 text-white")
        ]),
        dbc.CardBody([
            html.Div(id="recent-activity-content")
        ])
    ], className="content-card h-100")

def create_quick_actions_card():
    """Crea la tarjeta de acciones rápidas"""
    return dbc.Card([
        dbc.CardHeader([
            html.H5([
                html.I(className="fas fa-bolt me-2"),
                "Acciones Rápidas"
            ], className="mb-0 text-white")
        ]),
        dbc.CardBody([
            dbc.ListGroup([
                dbc.ListGroupItem([
                    html.I(className="fas fa-user-plus me-3 text-primary"),
                    "Añadir Jugador"
                ], href="/jugadores", action=True),
                
                dbc.ListGroupItem([
                    html.I(className="fas fa-calendar-plus me-3 text-success"),
                    "Nuevo Entrenamiento"
                ], href="/entrenamientos", action=True),
                
                dbc.ListGroupItem([
                    html.I(className="fas fa-futbol me-3 text-info"),
                    "Registrar Partido"
                ], href="/partidos", action=True),
                
                dbc.ListGroupItem([
                    html.I(className="fas fa-euro-sign me-3 text-warning"),
                    "Gestionar Multas"
                ], href="/multas", action=True),
                
                dbc.ListGroupItem([
                    html.I(className="fas fa-star me-3 text-danger"),
                    "Añadir Puntuación"
                ], href="/puntuacion", action=True)
            ], flush=True)
        ])
    ], className="content-card h-100")

# Callbacks para el dashboard
def register_dashboard_callbacks():
    """Registra los callbacks del dashboard"""
    
    @callback(
        [Output("main-stats-row", "children"),
         Output("calendar-overview-content", "children"),
         Output("recent-activity-content", "children"),
         Output("calendar-chart", "figure"),
         Output("performance-chart", "figure")],
        [Input("refresh-dashboard", "n_clicks")],
        prevent_initial_call=False
    )
    def update_dashboard_data(n_clicks):
        """Actualiza todos los datos del dashboard"""
        try:
            with DatabaseManager() as db:
                # Estadísticas principales
                jugadores_activos = len(db.get_jugadores(activos_solo=True))
                entrenamientos_mes = len([e for e in db.get_entrenamientos() 
                                        if e.fecha.month == datetime.now().month])
                multas_pendientes = sum([m.debe for m in db.get_multas_pendientes()])
                
                # Próximo partido
                calendario = db.get_calendario()
                proximo_partido = None
                dias_proximo = 0
                
                for evento in calendario:
                    if evento.fecha >= datetime.now().date():
                        proximo_partido = evento
                        dias_proximo = (evento.fecha - datetime.now().date()).days
                        break
                
                # Crear tarjetas de estadísticas
                stats_cards = [
                    dbc.Col([
                        create_stats_card(
                            "Jugadores Activos",
                            str(jugadores_activos),
                            "fas fa-users",
                            "primary",
                            "En plantilla"
                        )
                    ], width=6, md=3, className="mb-3"),
                    
                    dbc.Col([
                        create_stats_card(
                            "Próximo Partido",
                            str(dias_proximo),
                            "fas fa-calendar-day",
                            "success",
                            "días restantes"
                        )
                    ], width=6, md=3, className="mb-3"),
                    
                    dbc.Col([
                        create_stats_card(
                            "Entrenamientos",
                            str(entrenamientos_mes),
                            "fas fa-running",
                            "info",
                            "este mes"
                        )
                    ], width=6, md=3, className="mb-3"),
                    
                    dbc.Col([
                        create_stats_card(
                            "Multas Pendientes",
                            f"€{multas_pendientes:.2f}",
                            "fas fa-euro-sign",
                            "warning",
                            "por cobrar"
                        )
                    ], width=6, md=3, className="mb-3")
                ]
                
                # Contenido del calendario
                calendario_content = create_calendar_content(calendario[:5])
                
                # Actividad reciente
                actividad_reciente = create_recent_activity_content(db)
                
                # Gráfico del calendario
                calendar_fig = create_calendar_chart(calendario)
                
                # Gráfico de rendimiento
                performance_fig = create_performance_chart(db)
                
                return stats_cards, calendario_content, actividad_reciente, calendar_fig, performance_fig
                
        except Exception as e:
            print(f"Error actualizando dashboard: {e}")
            return [], "Error cargando datos", "Error cargando actividad", {}, {}

def create_calendar_content(proximos_partidos):
    """Crea el contenido de próximos partidos"""
    if not proximos_partidos:
        return html.P("No hay partidos programados", className="text-muted text-center")
    
    items = []
    for partido in proximos_partidos:
        items.append(
            dbc.ListGroupItem([
                dbc.Row([
                    dbc.Col([
                        html.Strong(f"{partido.equipo_local} vs {partido.equipo_visitante}"),
                        html.Br(),
                        html.Small(f"{partido.fecha} - {partido.competicion}", className="text-muted")
                    ], width=8),
                    dbc.Col([
                        dbc.Badge(
                            partido.competicion,
                            color="primary" if partido.competicion == "Liga" else "info",
                            className="mb-1"
                        )
                    ], width=4, className="text-end")
                ])
            ])
        )
    
    return dbc.ListGroup(items, flush=True)

def create_recent_activity_content(db):
    """Crea el contenido de actividad reciente"""
    activities = []
    
    # Últimos entrenamientos
    entrenamientos = db.get_entrenamientos()[:3]
    for ent in entrenamientos:
        activities.append({
            'icon': 'fas fa-running',
            'text': f"Entrenamiento #{ent.numero_entrenamiento}",
            'date': ent.fecha,
            'type': 'entrenamiento'
        })
    
    # Últimas multas
    multas = db.get_multas()[:2]
    for multa in multas:
        jugador = db.get_jugador_by_id(multa.jugador_id)
        activities.append({
            'icon': 'fas fa-euro-sign',
            'text': f"Multa a {jugador.nombre_futbolistico if jugador else 'Jugador'}",
            'date': multa.fecha,
            'type': 'multa'
        })
    
    # Ordenar por fecha
    activities.sort(key=lambda x: x['date'], reverse=True)
    
    if not activities:
        return html.P("No hay actividad reciente", className="text-muted text-center")
    
    items = []
    for activity in activities[:5]:
        color = {
            'entrenamiento': 'primary',
            'multa': 'warning',
            'partido': 'success'
        }.get(activity['type'], 'secondary')
        
        items.append(
            html.Div([
                html.I(className=f"{activity['icon']} me-3 text-{color}"),
                html.Span(activity['text']),
                html.Small(
                    f" - {activity['date']}",
                    className="text-muted"
                )
            ], className="d-flex align-items-center mb-2")
        )
    
    return html.Div(items)

def create_calendar_chart(calendario_data):
    """Crea el gráfico del calendario"""
    if not calendario_data:
        return go.Figure().add_annotation(
            text="No hay datos disponibles",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            showarrow=False
        )
    
    # Contar partidos por competición
    competiciones = {}
    for partido in calendario_data:
        comp = partido.competicion
        competiciones[comp] = competiciones.get(comp, 0) + 1
    
    fig = go.Figure(data=[
        go.Pie(
            labels=list(competiciones.keys()),
            values=list(competiciones.values()),
            hole=0.3,
            marker_colors=[COLORS['primary'], COLORS['success'], COLORS['info']]
        )
    ])
    
    fig.update_layout(
        title="Distribución de Partidos por Competición",
        showlegend=True,
        height=300,
        margin=dict(t=50, b=0, l=0, r=0)
    )
    
    return fig

def create_performance_chart(db):
    """Crea el gráfico de rendimiento"""
    try:
        jugadores = db.get_jugadores()
        if not jugadores:
            return go.Figure().add_annotation(
                text="No hay datos de jugadores",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False
            )
        
        # Top 5 goleadores
        top_goleadores = sorted(jugadores, key=lambda x: x.goles, reverse=True)[:5]
        
        fig = go.Figure(data=[
            go.Bar(
                x=[j.nombre_futbolistico for j in top_goleadores],
                y=[j.goles for j in top_goleadores],
                marker_color=COLORS['primary']
            )
        ])
        
        fig.update_layout(
            title="Top 5 Goleadores",
            xaxis_title="Jugadores",
            yaxis_title="Goles",
            height=300,
            margin=dict(t=50, b=50, l=50, r=50)
        )
        
        return fig
        
    except Exception as e:
        print(f"Error creando gráfico de rendimiento: {e}")
        return go.Figure()

# Registrar callbacks al importar
register_dashboard_callbacks()

# Definir el layout del dashboard
layout = create_dashboard_layout()