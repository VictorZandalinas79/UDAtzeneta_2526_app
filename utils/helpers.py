import pandas as pd
import io
import base64
from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional, Union
import re
import json
from decimal import Decimal
import plotly.graph_objs as go
import plotly.express as px
from config.settings import COLORS

def format_date(date_obj: Union[date, datetime, str], format_str: str = "%d/%m/%Y") -> str:
    """Formatea una fecha a string"""
    if isinstance(date_obj, str):
        return date_obj
    
    if isinstance(date_obj, datetime):
        date_obj = date_obj.date()
    
    if isinstance(date_obj, date):
        return date_obj.strftime(format_str)
    
    return ""

def parse_date(date_str: str) -> Optional[date]:
    """Convierte string a objeto date"""
    if not date_str:
        return None
    
    date_formats = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%Y/%m/%d",
        "%d/%m/%y",
        "%d-%m-%y"
    ]
    
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    
    return None

def calculate_age(birth_date: Union[date, datetime]) -> int:
    """Calcula la edad a partir de la fecha de nacimiento"""
    if isinstance(birth_date, datetime):
        birth_date = birth_date.date()
    
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def format_currency(amount: Union[float, int, Decimal], currency: str = "€") -> str:
    """Formatea cantidad monetaria"""
    if amount is None:
        return f"0.00 {currency}"
    
    return f"{float(amount):.2f} {currency}"

def format_percentage(value: Union[float, int], decimals: int = 1) -> str:
    """Formatea porcentaje"""
    if value is None:
        return "0.0%"
    
    return f"{float(value):.{decimals}f}%"

def sanitize_filename(filename: str) -> str:
    """Limpia nombre de archivo para que sea seguro"""
    # Remover caracteres peligrosos
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    
    # Reemplazar espacios con guiones bajos
    filename = filename.replace(' ', '_')
    
    # Limitar longitud
    if len(filename) > 200:
        filename = filename[:200]
    
    return filename

def validate_email(email: str) -> bool:
    """Valida formato de email"""
    if not email:
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone: str) -> bool:
    """Valida formato de teléfono español"""
    if not phone:
        return False
    
    # Limpiar número
    phone = re.sub(r'[^\d+]', '', phone)
    
    # Patrones válidos para España
    patterns = [
        r'^\+34[6-9]\d{8}$',  # +34 seguido de móvil
        r'^[6-9]\d{8}$',      # Móvil directo
        r'^\+349\d{8}$',      # +34 seguido de fijo
        r'^9\d{8}$'           # Fijo directo
    ]
    
    return any(re.match(pattern, phone) for pattern in patterns)

def validate_dni(dni: str) -> bool:
    """Valida DNI español"""
    if not dni or len(dni) != 9:
        return False
    
    # Extraer número y letra
    number = dni[:-1]
    letter = dni[-1].upper()
    
    if not number.isdigit():
        return False
    
    # Tabla de letras para validación
    letters = "TRWAGMYFPDXBNJZSQVHLCKE"
    expected_letter = letters[int(number) % 23]
    
    return letter == expected_letter

def export_to_excel(data: List[Dict], filename: str, sheet_name: str = "Datos") -> bytes:
    """Exporta datos a Excel"""
    df = pd.DataFrame(data)
    
    # Crear buffer en memoria
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        # Formatear worksheet
        workbook = writer.book
        worksheet = writer.sheets[sheet_name]
        
        # Formato para encabezados
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': COLORS['primary'],
            'font_color': 'white',
            'border': 1
        })
        
        # Aplicar formato a encabezados
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
        
        # Ajustar ancho de columnas
        for i, col in enumerate(df.columns):
            max_length = max(
                df[col].astype(str).str.len().max(),
                len(str(col))
            )
            worksheet.set_column(i, i, min(max_length + 2, 50))
    
    output.seek(0)
    return output.getvalue()

def create_backup_data(db_manager) -> Dict[str, Any]:
    """Crea un backup de todos los datos"""
    backup_data = {
        'timestamp': datetime.now().isoformat(),
        'version': '1.0',
        'data': {}
    }
    
    try:
        # Exportar jugadores
        jugadores = db_manager.get_jugadores(activos_solo=False)
        backup_data['data']['jugadores'] = [
            {
                'id': j.id,
                'nombre_futbolistico': j.nombre_futbolistico,
                'nombre': j.nombre,
                'apellidos': j.apellidos,
                'email': j.email,
                'dni': j.dni,
                'telefono': j.telefono,
                'direccion': j.direccion,
                'dorsal': j.dorsal,
                'posicion': j.posicion,
                'pierna_dominante': j.pierna_dominante,
                'goles': j.goles,
                'asistencias': j.asistencias,
                'tarjetas_amarillas': j.tarjetas_amarillas,
                'tarjetas_rojas': j.tarjetas_rojas,
                'minutos_jugados': j.minutos_jugados,
                'partidos_titular': j.partidos_titular,
                'partidos_suplente': j.partidos_suplente,
                'convocatorias': j.convocatorias,
                'altura': j.altura,
                'activo': j.activo,
                'fecha_registro': j.fecha_registro.isoformat() if j.fecha_registro else None
            } for j in jugadores
        ]
        
        # Exportar calendario
        calendario = db_manager.get_calendario()
        backup_data['data']['calendario'] = [
            {
                'id': c.id,
                'fecha': c.fecha.isoformat() if c.fecha else None,
                'hora': c.hora,
                'competicion': c.competicion,
                'jornada': c.jornada,
                'equipo_local': c.equipo_local,
                'goles_equipo_local': c.goles_equipo_local,
                'goles_equipo_visitante': c.goles_equipo_visitante,
                'equipo_visitante': c.equipo_visitante,
                'arbitro': c.arbitro,
                'asistentes': c.asistentes,
                'campo': c.campo,
                'scrapeado': c.scrapeado
            } for c in calendario
        ]
        
        # Exportar entrenamientos
        entrenamientos = db_manager.get_entrenamientos()
        backup_data['data']['entrenamientos'] = [
            {
                'id': e.id,
                'numero_entrenamiento': e.numero_entrenamiento,
                'fecha': e.fecha.isoformat() if e.fecha else None,
                'observaciones': e.observaciones
            } for e in entrenamientos
        ]
        
        # Exportar multas
        multas = db_manager.get_multas()
        backup_data['data']['multas'] = [
            {
                'id': m.id,
                'jugador_id': m.jugador_id,
                'fecha': m.fecha.isoformat() if m.fecha else None,
                'razon_multa': m.razon_multa,
                'multa': float(m.multa),
                'pagado': float(m.pagado),
                'debe': float(m.debe),
                'completamente_pagada': m.completamente_pagada
            } for m in multas
        ]
        
    except Exception as e:
        backup_data['error'] = str(e)
    
    return backup_data

def process_uploaded_image(contents: str, filename: str) -> Optional[str]:
    """Procesa imagen subida y retorna path relativo"""
    try:
        # Verificar que es una imagen
        if not any(filename.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif']):
            return None
        
        # Decodificar imagen
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        
        # Generar nombre único
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = sanitize_filename(filename)
        new_filename = f"{timestamp}_{safe_filename}"
        
        # Guardar en directorio de assets/images
        import os
        images_dir = os.path.join('assets', 'images')
        os.makedirs(images_dir, exist_ok=True)
        
        file_path = os.path.join(images_dir, new_filename)
        
        with open(file_path, 'wb') as f:
            f.write(decoded)
        
        # Retornar path relativo para usar en la app
        return f"/assets/images/{new_filename}"
        
    except Exception as e:
        print(f"Error procesando imagen: {e}")
        return None

def create_performance_chart(jugadores_data: List[Dict], metric: str = "goles") -> go.Figure:
    """Crea gráfico de rendimiento de jugadores"""
    if not jugadores_data:
        fig = go.Figure()
        fig.add_annotation(
            text="No hay datos disponibles",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            showarrow=False
        )
        return fig
    
    # Ordenar por métrica
    sorted_data = sorted(jugadores_data, key=lambda x: x.get(metric, 0), reverse=True)
    top_10 = sorted_data[:10]
    
    fig = go.Figure(data=[
        go.Bar(
            x=[j['nombre_futbolistico'] for j in top_10],
            y=[j.get(metric, 0) for j in top_10],
            marker_color=COLORS['primary'],
            text=[j.get(metric, 0) for j in top_10],
            textposition='auto'
        )
    ])
    
    fig.update_layout(
        title=f"Top 10 - {metric.replace('_', ' ').title()}",
        xaxis_title="Jugadores",
        yaxis_title=metric.replace('_', ' ').title(),
        height=400,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    return fig

def create_attendance_chart(asistencia_data: List[Dict]) -> go.Figure:
    """Crea gráfico de asistencia a entrenamientos"""
    if not asistencia_data:
        return go.Figure()
    
    # Procesar datos de asistencia
    df = pd.DataFrame(asistencia_data)
    
    if 'fecha' not in df.columns or 'asistentes' not in df.columns:
        return go.Figure()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['fecha'],
        y=df['asistentes'],
        mode='lines+markers',
        name='Asistentes',
        line=dict(color=COLORS['primary'], width=3),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=df['fecha'],
        y=df['total_jugadores'],
        mode='lines+markers',
        name='Total Jugadores',
        line=dict(color=COLORS['gray_medium'], width=2, dash='dash'),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        title="Evolución de Asistencia a Entrenamientos",
        xaxis_title="Fecha",
        yaxis_title="Número de Jugadores",
        height=400,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    
    return fig

def calculate_team_stats(jugadores_data: List[Dict]) -> Dict[str, Any]:
    """Calcula estadísticas generales del equipo"""
    if not jugadores_data:
        return {}
    
    total_jugadores = len(jugadores_data)
    total_goles = sum(j.get('goles', 0) for j in jugadores_data)
    total_asistencias = sum(j.get('asistencias', 0) for j in jugadores_data)
    total_tarjetas_amarillas = sum(j.get('tarjetas_amarillas', 0) for j in jugadores_data)
    total_tarjetas_rojas = sum(j.get('tarjetas_rojas', 0) for j in jugadores_data)
    total_minutos = sum(j.get('minutos_jugados', 0) for j in jugadores_data)
    
    # Calcular promedios
    promedio_goles = total_goles / total_jugadores if total_jugadores > 0 else 0
    promedio_asistencias = total_asistencias / total_jugadores if total_jugadores > 0 else 0
    
    # Top goleador
    top_goleador = max(jugadores_data, key=lambda x: x.get('goles', 0))
    
    # Jugador más disciplinado (menos tarjetas)
    menos_tarjetas = min(jugadores_data, key=lambda x: x.get('tarjetas_amarillas', 0) + x.get('tarjetas_rojas', 0) * 2)
    
    return {
        'total_jugadores': total_jugadores,
        'total_goles': total_goles,
        'total_asistencias': total_asistencias,
        'total_tarjetas_amarillas': total_tarjetas_amarillas,
        'total_tarjetas_rojas': total_tarjetas_rojas,
        'total_minutos': total_minutos,
        'promedio_goles': round(promedio_goles, 2),
        'promedio_asistencias': round(promedio_asistencias, 2),
        'top_goleador': top_goleador['nombre_futbolistico'] if top_goleador else None,
        'top_goleador_goles': top_goleador.get('goles', 0) if top_goleador else 0,
        'mas_disciplinado': menos_tarjetas['nombre_futbolistico'] if menos_tarjetas else None
    }

def generate_report_summary(data_type: str, data: List[Dict]) -> str:
    """Genera resumen de reporte"""
    if not data:
        return f"No hay datos de {data_type} para mostrar."
    
    total_items = len(data)
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    summary = f"""
    REPORTE DE {data_type.upper()}
    Generado el: {fecha_actual}
    Total de elementos: {total_items}
    
    """
    
    if data_type == "jugadores":
        activos = len([j for j in data if j.get('activo', True)])
        summary += f"Jugadores activos: {activos}\n"
        summary += f"Jugadores inactivos: {total_items - activos}\n"
    
    elif data_type == "multas":
        total_importe = sum(m.get('multa', 0) for m in data)
        pendientes = len([m for m in data if not m.get('completamente_pagada', False)])
        summary += f"Total importe: {format_currency(total_importe)}\n"
        summary += f"Multas pendientes: {pendientes}\n"
    
    return summary