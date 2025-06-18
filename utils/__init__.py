# utils/__init__.py
# Reemplaza el contenido de tu utils/__init__.py con esto:

"""
Utilidades del sistema de gestión UD Atzeneta
"""

# Importaciones seguras con manejo de errores
try:
    from .session_manager import SessionManager
except ImportError as e:
    print(f"Warning: No se pudo importar SessionManager: {e}")
    SessionManager = None

try:
    from .header_utils import create_page_header
except ImportError as e:
    print(f"Warning: No se pudo importar header_utils: {e}")
    create_page_header = None

# Importaciones de scraping con manejo de errores
try:
    from .scraping import (
        FederacionScraper,
        FFCVScraper,
        ScrapingManager,
        scraping_manager
    )
except ImportError as e:
    print(f"Warning: No se pudo importar scraping: {e}")
    # Crear clases dummy para evitar errores
    class FederacionScraper:
        pass
    
    class FFCVScraper:
        pass
    
    class ScrapingManager:
        def __init__(self):
            self.scraping_enabled = False
        
        def configure_ffcv_scraper(self, url):
            pass
        
        def perform_ffcv_scraping(self):
            return {'success': False, 'error': 'Scraping no disponible'}
    
    scraping_manager = ScrapingManager()

# Exportar todo lo disponible
__all__ = [
    'SessionManager',
    'create_page_header', 
    'FederacionScraper',
    'FFCVScraper',
    'ScrapingManager',
    'scraping_manager'
]

# Función de utilidad para verificar dependencias
def check_dependencies():
    """Verifica que todas las dependencias estén disponibles"""
    missing = []
    
    if SessionManager is None:
        missing.append('SessionManager')
    
    if create_page_header is None:
        missing.append('create_page_header')
        
    if FederacionScraper is None:
        missing.append('FederacionScraper')
    
    return missing

# Función de ayuda para debugging
def debug_utils():
    """Muestra información de debug sobre las utilidades"""
    print("=== DEBUG UTILS ===")
    print(f"SessionManager: {'✅' if SessionManager else '❌'}")
    print(f"create_page_header: {'✅' if create_page_header else '❌'}")
    print(f"FederacionScraper: {'✅' if FederacionScraper else '❌'}")
    print(f"FFCVScraper: {'✅' if FFCVScraper else '❌'}")
    print(f"ScrapingManager: {'✅' if ScrapingManager else '❌'}")
    
    missing = check_dependencies()
    if missing:
        print(f"Dependencias faltantes: {missing}")
    else:
        print("✅ Todas las dependencias están disponibles")
    print("==================")