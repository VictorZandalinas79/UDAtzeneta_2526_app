import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
from datetime import datetime

def scrape_ffcv_calendar(url):
    """
    Función para hacer scraping del calendario de la FFCV
    """
    
    # Headers para simular un navegador real
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Realizar la petición
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Parsear el HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Lista para almacenar los datos
        partidos = []
        
        # Buscar la tabla principal
        tabla = soup.find('table', class_='table calendario_table')
        if not tabla:
            print("No se encontró la tabla de partidos")
            return []
        
        # Buscar todas las filas
        filas = tabla.find('tbody').find_all('tr')
        
        jornada_actual = None
        
        for fila in filas:
            try:
                # Verificar si es una fila de jornada
                if 'info_jornada' in fila.get('class', []):
                    # Extraer número de jornada
                    jornada_text = fila.find('td').get_text().strip()
                    jornada_actual = jornada_text.replace('JORNADA ', '')
                    continue
                
                # Es una fila de partido
                columnas = fila.find_all('td')
                if len(columnas) >= 6:
                    
                    # Extraer datos del partido
                    datos_partido = {
                        'fecha': extraer_fecha(columnas[4]),
                        'jornada': jornada_actual,
                        'tipo_competicion': 'Liga',  # Por defecto, se puede mejorar
                        'equipo_local': extraer_equipo_local(columnas[2]),
                        'goles_equipo_local': extraer_goles_local(columnas[3]),
                        'equipo_visitante': extraer_equipo_visitante(columnas[2]),
                        'goles_equipo_visitante': extraer_goles_visitante(columnas[3]),
                        'hora': extraer_hora(columnas[4]),
                        'arbitro': extraer_arbitro(columnas[5]),
                        'campo': extraer_campo(columnas[5])
                    }
                    
                    partidos.append(datos_partido)
                    
            except Exception as e:
                print(f"Error procesando fila: {e}")
                continue
        
        return partidos
    
    except requests.exceptions.RequestException as e:
        print(f"Error en la petición: {e}")
        return []

def extraer_fecha(elemento):
    """Extrae la fecha del partido"""
    try:
        fecha_div = elemento.find('div', class_='negrita')
        if fecha_div:
            return fecha_div.get_text().strip()
        return None
    except:
        return None

def extraer_jornada(elemento):
    """Extrae la jornada - se maneja en la función principal"""
    return None

def extraer_tipo_competicion(elemento):
    """Extrae el tipo de competición"""
    # Por ahora devolvemos 'Liga' por defecto
    # Se podría mejorar extrayendo de otra parte de la página
    return 'Liga'

def extraer_equipo_local(elemento):
    """Extrae el equipo local"""
    try:
        # Los equipos están dentro de elementos <a>
        enlaces = elemento.find_all('a')
        if len(enlaces) >= 1:
            # El primer enlace contiene el equipo local
            equipo_local = enlaces[0].get_text().strip()
            return equipo_local
        return None
    except:
        return None

def extraer_goles_local(elemento):
    """Extrae los goles del equipo local"""
    try:
        # Los goles están en spans dentro del elemento
        spans = elemento.find_all('span')
        if len(spans) >= 2:
            # El primer span tiene los goles del equipo local
            goles_text = spans[0].get_text().strip()
            if goles_text.isdigit():
                return int(goles_text)
        return None
    except:
        return None

def extraer_equipo_visitante(elemento):
    """Extrae el equipo visitante"""
    try:
        # Los equipos están dentro de elementos <a>
        enlaces = elemento.find_all('a')
        if len(enlaces) >= 2:
            # El segundo enlace contiene el equipo visitante
            equipo_visitante = enlaces[1].get_text().strip()
            return equipo_visitante
        return None
    except:
        return None

def extraer_goles_visitante(elemento):
    """Extrae los goles del equipo visitante"""
    try:
        # Los goles están en spans dentro del elemento
        spans = elemento.find_all('span')
        if len(spans) >= 2:
            # El segundo span tiene los goles del equipo visitante
            goles_text = spans[1].get_text().strip()
            if goles_text.isdigit():
                return int(goles_text)
        return None
    except:
        return None

def extraer_hora(elemento):
    """Extrae la hora del partido"""
    try:
        # Buscar todos los divs en el elemento
        divs = elemento.find_all('div')
        if len(divs) >= 2:
            # La hora está en el segundo div (sin clase)
            hora_div = divs[1]
            return hora_div.get_text().strip()
        return None
    except:
        return None

def extraer_arbitro(elemento):
    """Extrae el árbitro"""
    try:
        # El campo/estadio está en el texto del elemento, pero no veo árbitro
        # Por ahora devolvemos None, se podría extraer de otra parte si está disponible
        return None
    except:
        return None

def extraer_campo(elemento):
    """Extrae el campo/estadio"""
    try:
        # El campo está después del icono del mapa en la última columna
        texto_completo = elemento.get_text().strip()
        # Eliminar el icono y espacios extra, quedarnos con el nombre del campo
        # El texto viene como " Campo Mpal. El Porrejat F-11 Atzeneta Maestrat (HN)"
        if texto_completo:
            # Limpiar el texto removiendo espacios extra
            campo = re.sub(r'\s+', ' ', texto_completo).strip()
            return campo
        return None
    except:
        return None

def guardar_csv(partidos, nombre_archivo='partidos_ffcv.csv'):
    """Guarda los datos en un archivo CSV"""
    if partidos:
        df = pd.DataFrame(partidos)
        
        # Reordenar columnas según el orden solicitado
        columnas_ordenadas = [
            'fecha', 'jornada', 'tipo_competicion', 'equipo_local', 
            'goles_equipo_local', 'equipo_visitante', 'goles_equipo_visitante', 
            'hora', 'arbitro', 'campo'
        ]
        
        # Seleccionar solo las columnas que existen
        columnas_disponibles = [col for col in columnas_ordenadas if col in df.columns]
        df = df[columnas_disponibles]
        
        df.to_csv(nombre_archivo, index=False, encoding='utf-8')
        print(f"Datos guardados en {nombre_archivo}")
        print(f"Total de partidos extraídos: {len(partidos)}")
        print(f"Columnas guardadas: {list(df.columns)}")
        return df
    else:
        print("No se encontraron datos para guardar")
        return None

def main():
    # URL de la página
    url = "https://resultadosffcv.isquad.es/equipo_calendario.php?id_temp=20&id_modalidad=33327&id_competicion=903498407&id_equipo=18331&torneo_equipo=903498408&id_torneo=903498408"
    
    print("Iniciando scraping de FFCV...")
    
    # Realizar scraping
    partidos = scrape_ffcv_calendar(url)
    
    if partidos:
        # Guardar en CSV
        df = guardar_csv(partidos)
        
        # Mostrar preview de los datos
        if df is not None:
            print("\nPreview de los datos:")
            print(df.head())
    else:
        print("No se pudieron extraer datos")

if __name__ == "__main__":
    main()