import requests
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime, date
from typing import List, Dict, Optional, Tuple
from config.settings import SCRAPING_CONFIG
from database.db_manager import DatabaseManager, Calendario

class FederacionScraper:
    """Scraper para obtener datos de partidos desde la web de la federación"""
    
    def __init__(self, base_url: str = None, team_code: str = None):
        self.base_url = base_url
        self.team_code = team_code
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': SCRAPING_CONFIG['user_agent']
        })
        
    def setup_config(self, base_url: str, team_code: str, season: str = "2024-2025"):
        """Configura los parámetros del scraper"""
        self.base_url = base_url
        self.team_code = team_code
        self.season = season
    
    def get_calendar_page(self, competition: str = "liga") -> Optional[BeautifulSoup]:
        """Obtiene la página del calendario de la federación"""
        try:
            if not self.base_url or not self.team_code:
                raise ValueError("URL base y código de equipo son requeridos")
            
            # Construir URL del calendario
            url = f"{self.base_url}?equipo={self.team_code}&competicion={competition}&temporada={self.season}"
            
            response = self.session.get(
                url, 
                timeout=SCRAPING_CONFIG['timeout']
            )
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
            
        except requests.RequestException as e:
            print(f"Error al obtener página del calendario: {e}")
            return None
        except Exception as e:
            print(f"Error procesando página del calendario: {e}")
            return None
    
    def parse_match_row(self, row) -> Optional[Dict]:
        """Parsea una fila de partido de la tabla HTML"""
        try:
            cells = row.find_all(['td', 'th'])
            if len(cells) < 6:  # Mínimo necesario para un partido
                return None
            
            # Extraer datos básicos (esto dependerá del formato específico de la web)
            match_data = {
                'jornada': self._clean_text(cells[0].get_text()),
                'fecha': self._parse_date(cells[1].get_text()),
                'hora': self._parse_time(cells[2].get_text()),
                'equipo_local': self._clean_text(cells[3].get_text()),
                'resultado': self._parse_result(cells[4].get_text()),
                'equipo_visitante': self._clean_text(cells[5].get_text()),
                'arbitro': self._clean_text(cells[6].get_text()) if len(cells) > 6 else None,
                'campo': self._clean_text(cells[7].get_text()) if len(cells) > 7 else None
            }
            
            # Parsear resultado si existe
            if match_data['resultado']:
                goles = self._parse_goals(match_data['resultado'])
                match_data['goles_equipo_local'] = goles[0]
                match_data['goles_equipo_visitante'] = goles[1]
            
            return match_data
            
        except Exception as e:
            print(f"Error parseando fila de partido: {e}")
            return None
    
    def scrape_calendar(self, competition: str = "liga") -> List[Dict]:
        """Realiza el scraping completo del calendario"""
        matches = []
        
        try:
            soup = self.get_calendar_page(competition)
            if not soup:
                return matches
            
            # Buscar tabla de partidos (esto puede variar según la web)
            tables = soup.find_all('table')
            
            for table in tables:
                # Buscar la tabla que contiene los partidos
                rows = table.find_all('tr')
                
                for row in rows[1:]:  # Saltar encabezado
                    match_data = self.parse_match_row(row)
                    if match_data:
                        match_data['competicion'] = competition.title()
                        match_data['scrapeado'] = True
                        matches.append(match_data)
            
            print(f"Scrapeados {len(matches)} partidos de {competition}")
            return matches
            
        except Exception as e:
            print(f"Error en scraping del calendario: {e}")
            return matches
    
    def scrape_all_competitions(self) -> List[Dict]:
        """Scrapea todas las competiciones"""
        all_matches = []
        competitions = ['liga', 'copa']
        
        for comp in competitions:
            time.sleep(SCRAPING_CONFIG['delay_between_requests'])
            matches = self.scrape_calendar(comp)
            all_matches.extend(matches)
        
        return all_matches
    
    def update_database(self, matches: List[Dict]) -> Tuple[int, int]:
        """Actualiza la base de datos con los partidos scrapeados"""
        created = 0
        updated = 0
        
        try:
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
    
    def _clean_text(self, text: str) -> str:
        """Limpia y normaliza texto"""
        if not text:
            return ""
        
        # Remover espacios extra y caracteres especiales
        text = re.sub(r'\s+', ' ', text.strip())
        text = text.replace('\n', '').replace('\t', '')
        
        return text
    
    def _parse_date(self, date_str: str) -> Optional[date]:
        """Parsea string de fecha a objeto date"""
        try:
            date_str = self._clean_text(date_str)
            
            # Formatos comunes de fecha
            date_formats = [
                '%d/%m/%Y',
                '%d-%m-%Y',
                '%Y-%m-%d',
                '%d/%m/%y',
                '%d-%m-%y'
            ]
            
            for fmt in date_formats:
                try:
                    return datetime.strptime(date_str, fmt).date()
                except ValueError:
                    continue
            
            # Si no coincide con ningún formato, intentar parseo manual
            # Ejemplo: "Sábado 15/03/2025"
            date_match = re.search(r'(\d{1,2})/(\d{1,2})/(\d{2,4})', date_str)
            if date_match:
                day, month, year = date_match.groups()
                if len(year) == 2:
                    year = f"20{year}"
                return date(int(year), int(month), int(day))
            
            return None
            
        except Exception as e:
            print(f"Error parseando fecha '{date_str}': {e}")
            return None
    
    def _parse_time(self, time_str: str) -> Optional[str]:
        """Parsea string de hora"""
        try:
            time_str = self._clean_text(time_str)
            
            # Buscar patrón de hora
            time_match = re.search(r'(\d{1,2}):(\d{2})', time_str)
            if time_match:
                hour, minute = time_match.groups()
                return f"{hour.zfill(2)}:{minute}"
            
            return None
            
        except Exception as e:
            print(f"Error parseando hora '{time_str}': {e}")
            return None
    
    def _parse_result(self, result_str: str) -> Optional[str]:
        """Parsea string de resultado"""
        try:
            result_str = self._clean_text(result_str)
            
            # Buscar patrón de resultado
            result_match = re.search(r'(\d+)\s*-\s*(\d+)', result_str)
            if result_match:
                return result_str
            
            # Si no hay resultado, verificar si dice "vs" o similar
            if any(word in result_str.lower() for word in ['vs', 'v', '-']):
                return "vs"
            
            return None
            
        except Exception as e:
            print(f"Error parseando resultado '{result_str}': {e}")
            return None
    
    def _parse_goals(self, result_str: str) -> Tuple[Optional[int], Optional[int]]:
        """Extrae goles del resultado"""
        try:
            result_match = re.search(r'(\d+)\s*-\s*(\d+)', result_str)
            if result_match:
                return int(result_match.group(1)), int(result_match.group(2))
            return None, None
            
        except Exception as e:
            print(f"Error parseando goles '{result_str}': {e}")
            return None, None

class ScrapingManager:
    """Gestor principal de scraping"""
    
    def __init__(self):
        self.scraper = FederacionScraper()
        self.last_scraping = None
        self.scraping_enabled = False
    
    def configure_scraper(self, url: str, team_code: str, season: str = "2024-2025"):
        """Configura el scraper"""
        self.scraper.setup_config(url, team_code, season)
        self.scraping_enabled = True
    
    def perform_scraping(self, competition: str = None) -> Dict[str, any]:
        """Realiza el proceso completo de scraping"""
        if not self.scraping_enabled:
            return {
                'success': False,
                'error': 'Scraping no configurado',
                'created': 0,
                'updated': 0
            }
        
        try:
            start_time = time.time()
            
            if competition:
                matches = self.scraper.scrape_calendar(competition)
            else:
                matches = self.scraper.scrape_all_competitions()
            
            if not matches:
                return {
                    'success': False,
                    'error': 'No se encontraron partidos',
                    'created': 0,
                    'updated': 0
                }
            
            created, updated = self.scraper.update_database(matches)
            
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
    
    def test_connection(self, url: str, team_code: str) -> Dict[str, any]:
        """Prueba la conexión con la web de la federación"""
        try:
            test_scraper = FederacionScraper(url, team_code)
            soup = test_scraper.get_calendar_page()
            
            if soup:
                # Verificar si la página contiene datos de partidos
                tables = soup.find_all('table')
                has_matches = any(
                    len(table.find_all('tr')) > 1 
                    for table in tables
                )
                
                return {
                    'success': True,
                    'has_data': has_matches,
                    'tables_found': len(tables),
                    'message': 'Conexión exitosa'
                }
            else:
                return {
                    'success': False,
                    'error': 'No se pudo obtener datos de la página'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_scraping_status(self) -> Dict[str, any]:
        """Obtiene el estado del scraping"""
        return {
            'enabled': self.scraping_enabled,
            'last_scraping': self.last_scraping.isoformat() if self.last_scraping else None,
            'configured': bool(self.scraper.base_url and self.scraper.team_code)
        }

# Instancia global del gestor de scraping
scraping_manager = ScrapingManager()