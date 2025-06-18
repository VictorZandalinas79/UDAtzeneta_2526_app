# Solución 1: Actualizar utils/scraping.py
# Reemplaza el contenido de utils/scraping.py con esto:

import requests
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime, date
from typing import List, Dict, Optional, Tuple

class FederacionScraper:
    """Scraper base para federaciones - Clase base requerida"""
    
    def __init__(self, base_url: str = None, team_code: str = None):
        self.base_url = base_url
        self.team_code = team_code
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def get_calendar_page(self, url: str) -> Optional[BeautifulSoup]:
        """Método base para obtener páginas"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(f"Error obteniendo página: {e}")
            return None
    
    def update_database(self, matches: List[Dict]) -> Tuple[int, int]:
        """Método base para actualizar base de datos"""
        return 0, 0

class FFCVScraper(FederacionScraper):
    """Scraper específico para la FFCV"""
    
    def __init__(self):
        super().__init__()
    
    def get_calendar_page(self, url: str) -> Optional[BeautifulSoup]:
        """Obtiene la página del calendario de la FFCV"""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
            
        except requests.RequestException as e:
            print(f"Error al obtener página del calendario FFCV: {e}")
            return None
    
    def parse_ffcv_calendar(self, soup: BeautifulSoup) -> List[Dict]:
        """Parsea específicamente el calendario de la FFCV"""
        matches = []
        
        try:
            # Buscar la tabla principal
            tabla = soup.find('table', class_='table calendario_table')
            if not tabla:
                print("No se encontró la tabla de partidos")
                return matches
            
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
                        match_data = {
                            'fecha': self._extract_fecha_ffcv(columnas[4]),
                            'jornada': jornada_actual,
                            'competicion': 'Liga',  # Por defecto
                            'equipo_local': self._extract_equipo_local_ffcv(columnas[2]),
                            'goles_equipo_local': self._extract_goles_local_ffcv(columnas[3]),
                            'equipo_visitante': self._extract_equipo_visitante_ffcv(columnas[2]),
                            'goles_equipo_visitante': self._extract_goles_visitante_ffcv(columnas[3]),
                            'hora': self._extract_hora_ffcv(columnas[4]),
                            'arbitro': None,  # No disponible en esta tabla
                            'campo': self._extract_campo_ffcv(columnas[5]) if len(columnas) > 5 else None,
                            'scrapeado': True
                        }
                        
                        # Solo agregar si tiene datos válidos
                        if match_data['equipo_local'] and match_data['equipo_visitante']:
                            matches.append(match_data)
                        
                except Exception as e:
                    print(f"Error procesando fila: {e}")
                    continue
            
            return matches
            
        except Exception as e:
            print(f"Error parseando calendario FFCV: {e}")
            return matches
    
    def scrape_ffcv_calendar(self, url: str) -> List[Dict]:
        """Realiza el scraping completo del calendario FFCV"""
        matches = []
        
        try:
            soup = self.get_calendar_page(url)
            if not soup:
                return matches
            
            matches = self.parse_ffcv_calendar(soup)
            print(f"Scrapeados {len(matches)} partidos de FFCV")
            return matches
            
        except Exception as e:
            print(f"Error en scraping FFCV: {e}")
            return matches
    
    def _extract_fecha_ffcv(self, elemento) -> Optional[date]:
        """Extrae la fecha del partido"""
        try:
            fecha_div = elemento.find('div', class_='negrita')
            if fecha_div:
                fecha_str = fecha_div.get_text().strip()
                # Formato DD-MM-YYYY
                return datetime.strptime(fecha_str, '%d-%m-%Y').date()
            return None
        except:
            return None
    
    def _extract_equipo_local_ffcv(self, elemento) -> Optional[str]:
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
    
    def _extract_equipo_visitante_ffcv(self, elemento) -> Optional[str]:
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
    
    def _extract_goles_local_ffcv(self, elemento) -> Optional[int]:
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
    
    def _extract_goles_visitante_ffcv(self, elemento) -> Optional[int]:
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
    
    def _extract_hora_ffcv(self, elemento) -> Optional[str]:
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
    
    def _extract_campo_ffcv(self, elemento) -> Optional[str]:
        """Extrae el campo/estadio"""
        try:
            # El campo está después del icono del mapa en la última columna
            texto_completo = elemento.get_text().strip()
            # Eliminar el icono y espacios extra, quedarnos con el nombre del campo
            if texto_completo:
                # Limpiar el texto removiendo espacios extra
                campo = re.sub(r'\s+', ' ', texto_completo).strip()
                return campo
            return None
        except:
            return None
    
    def update_database(self, matches: List[Dict]) -> Tuple[int, int]:
        """Actualiza la base de datos con los partidos de FFCV"""
        created = 0
        updated = 0
        
        try:
            # Importar aquí para evitar errores circulares
            from database.db_manager import DatabaseManager, Calendario
            
            with DatabaseManager() as db:
                for match in matches:
                    # Buscar si el partido ya existe
                    existing = db.db.query(Calendario).filter(
                        Calendario.fecha == match['fecha'],
                        Calendario.equipo_local == match['equipo_local'],
                        Calendario.equipo_visitante == match['equipo_visitante'],
                        Calendario.competicion == match['competicion']
                    ).first()
                    
                    if existing:
                        # Actualizar partido existente
                        for key, value in match.items():
                            if hasattr(existing, key) and value is not None:
                                setattr(existing, key, value)
                        existing.fecha_actualizacion = datetime.utcnow()
                        updated += 1
                    else:
                        # Crear nuevo partido
                        new_match = Calendario(**match)
                        db.db.add(new_match)
                        created += 1
                
                db.db.commit()
                
        except Exception as e:
            print(f"Error actualizando base de datos: {e}")
            
        return created, updated

class ScrapingManager:
    """Gestor principal de scraping"""
    
    def __init__(self):
        self.ffcv_scraper = FFCVScraper()
        self.last_scraping = None
        self.scraping_enabled = False
        self.ffcv_url = None
    
    def configure_ffcv_scraper(self, url: str):
        """Configura el scraper específico de FFCV"""
        self.ffcv_url = url
        self.scraping_enabled = True
    
    def perform_ffcv_scraping(self) -> Dict[str, any]:
        """Realiza el scraping específico de FFCV"""
        if not self.ffcv_url:
            return {
                'success': False,
                'error': 'URL de FFCV no configurada',
                'created': 0,
                'updated': 0
            }
        
        try:
            start_time = time.time()
            
            matches = self.ffcv_scraper.scrape_ffcv_calendar(self.ffcv_url)
            
            if not matches:
                return {
                    'success': False,
                    'error': 'No se encontraron partidos en FFCV',
                    'created': 0,
                    'updated': 0
                }
            
            created, updated = self.ffcv_scraper.update_database(matches)
            
            elapsed_time = time.time() - start_time
            self.last_scraping = datetime.now()
            
            return {
                'success': True,
                'created': created,
                'updated': updated,
                'total_matches': len(matches),
                'elapsed_time': elapsed_time,
                'timestamp': self.last_scraping.isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'created': 0,
                'updated': 0
            }

# Instancia global del gestor de scraping
scraping_manager = ScrapingManager()