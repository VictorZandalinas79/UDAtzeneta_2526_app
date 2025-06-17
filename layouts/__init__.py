# Paquete de layouts para UD Atzeneta
# Contiene los componentes de interfaz principal

from .sidebar import (
    create_sidebar,
    create_mobile_navbar,
    get_sidebar_callbacks,
    highlight_active_nav
)

from .main_content import (
    create_main_content,
    create_top_bar,
    create_loading_component,
    create_error_component,
    create_empty_state,
    create_page_header,
    create_stats_card,
    create_action_buttons,
    create_search_filter_bar,
    MAIN_CONTENT_CSS
)

__all__ = [
    'create_sidebar',
    'create_mobile_navbar',
    'get_sidebar_callbacks',
    'highlight_active_nav',
    'create_main_content',
    'create_top_bar',
    'create_loading_component',
    'create_error_component',
    'create_empty_state',
    'create_page_header',
    'create_stats_card',
    'create_action_buttons',
    'create_search_filter_bar',
    'MAIN_CONTENT_CSS'
]