# Paquete de utilidades para UD Atzeneta
# Contiene funciones auxiliares, manejo de sesiones y web scraping

from .session_manager import (
    SessionManager,
    DashSessionManager,
    global_session_manager,
    dash_session_manager
)

from .scraping import (
    FederacionScraper,
    ScrapingManager,
    scraping_manager
)

from .helpers import (
    format_date,
    parse_date,
    calculate_age,
    format_currency,
    format_percentage,
    sanitize_filename,
    validate_email,
    validate_phone,
    validate_dni,
    export_to_excel,
    create_backup_data,
    process_uploaded_image,
    create_performance_chart,
    create_attendance_chart,
    calculate_team_stats,
    generate_report_summary
)

__all__ = [
    'SessionManager',
    'DashSessionManager',
    'global_session_manager',
    'dash_session_manager',
    'FederacionScraper',
    'ScrapingManager',
    'scraping_manager',
    'format_date',
    'parse_date',
    'calculate_age',
    'format_currency',
    'format_percentage',
    'sanitize_filename',
    'validate_email',
    'validate_phone',
    'validate_dni',
    'export_to_excel',
    'create_backup_data',
    'process_uploaded_image',
    'create_performance_chart',
    'create_attendance_chart',
    'calculate_team_stats',
    'generate_report_summary'
]