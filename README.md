# ⚽ UD Atzeneta - Sistema de Gestión del Equipo

Una aplicación web completa para la gestión integral del equipo de fútbol UD Atzeneta, desarrollada con Dash (Python) y optimizada para despliegue en Render.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Dash](https://img.shields.io/badge/Dash-2.17+-green.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Características Principales

### 📊 Dashboard Completo
- Resumen general del equipo en tiempo real
- Estadísticas de jugadores y partidos
- Próximos eventos y actividad reciente
- Gráficos interactivos de rendimiento

### 👥 Gestión de Jugadores
- **Datos personales**: Nombre, contacto, dirección, DNI
- **Datos futbolísticos**: Posición, dorsal, estadísticas
- **Datos físicos**: Altura, peso (con seguimiento temporal), lesiones
- **Fotografías**: Subida y gestión de imágenes
- **Historial completo**: Seguimiento de evolución

### 📅 Calendario de Partidos
- **Web scraping automático** desde páginas de federación
- **Edición manual** de partidos amistosos
- **Gestión de competiciones**: Liga, Copa, Amistosos
- **Información completa**: Fecha, hora, rival, árbitro, campo
- **Resultados**: Registro y seguimiento automático

### ⚽ Control de Partidos
- **Convocatorias**: Titulares, suplentes, no convocados
- **Eventos**: Goles, asistencias, tarjetas, sustituciones
- **Estadísticas individuales**: Por jugador y partido
- **Análisis de rendimiento**: Métricas detalladas

### 🏃 Entrenamientos
- **Control de asistencia**: Registro completo por entrenamiento
- **Gestión de ausencias**: Razones y observaciones
- **Numeración automática**: Sistema de ID progresivo
- **Estadísticas**: Porcentajes de asistencia y tendencias

### 🎯 Objetivos Individuales
- **Seguimiento personalizado** por jugador
- **Control mensual**: Objetivos específicos por período
- **Progreso medible**: Sistema de porcentajes
- **Gráficas de evolución**: Visualización del desarrollo

### ⭐ Sistema de Puntuación
- **Puntuación en entrenamientos**: Recompensas y penalizaciones
- **Ranking dinámico**: Clasificación automática
- **Criterios configurables**: Sistema flexible de puntos
- **Histórico completo**: Seguimiento temporal

### 💰 Gestión de Multas
- **Registro de infracciones**: Diferentes tipos de multas
- **Control de pagos**: Sistema de seguimiento
- **Deudas pendientes**: Alertas y recordatorios
- **Estadísticas**: Análisis por jugador y período

## 🛠️ Tecnologías Utilizadas

- **Backend**: Python 3.11+
- **Framework Web**: Dash 2.17+
- **Base de Datos**: SQLite (compatible con Render gratuito)
- **ORM**: SQLAlchemy 2.0+
- **Autenticación**: bcrypt
- **Web Scraping**: BeautifulSoup4 + requests
- **Gráficos**: Plotly
- **Estilos**: Bootstrap + CSS personalizado
- **Despliegue**: Render

## 🚀 Instalación y Configuración

### Requisitos Previos
- Python 3.11 o superior
- pip (gestor de paquetes de Python)
- Git

### Instalación Local

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/ud-atzeneta.git
cd ud-atzeneta
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar la aplicación**
```bash
# La base de datos se crea automáticamente en el primer arranque
# Usuario por defecto: admin / admin123
```

5. **Ejecutar la aplicación**
```bash
python app.py
```

6. **Acceder a la aplicación**
```
http://localhost:8050
```

### Despliegue en Render

1. **Conectar repositorio** en Render
2. **Configurar variables de entorno** (opcional):
   - `DASH_DEBUG_MODE`: `False` para producción
   - `DATABASE_URL`: Se usa SQLite por defecto
3. **Desplegar automáticamente** desde la rama principal

## 🎨 Personalización

### Colores del Club
Los colores se pueden modificar en `config/settings.py`:
```python
COLORS = {
    'primary': '#DC143C',      # Rojo principal del club
    'secondary': '#8B0000',    # Rojo oscuro
    'dark': '#000000',         # Negro
    # ... más colores
}
```

### Logo del Club
Reemplazar el archivo `assets/logo_ud_atzeneta.png` con el logo oficial.

### Web Scraping
Configurar URLs y parámetros de scraping en la interfaz de administración.

## 📱 Características del Diseño

### Responsive Design
- ✅ Compatible con móviles y tablets
- ✅ Sidebar colapsable automático
- ✅ Tablas responsivas
- ✅ Imágenes adaptativas

### Interfaz Moderna
- 🎨 Gradientes y sombras elegantes
- 🌙 Modo oscuro en sidebar
- ⚡ Animaciones suaves
- 📊 Gráficos interactivos

### Experiencia de Usuario
- 🔍 Búsqueda y filtros avanzados
- 📥 Exportación a Excel
- 🔔 Notificaciones y alertas
- 💾 Guardado automático

## 📊 Base de Datos

### Estructura Principal
- **Usuarios**: Sistema de autenticación
- **Jugadores**: Información completa de la plantilla
- **Calendario**: Partidos y eventos
- **Entrenamientos**: Asistencia y observaciones
- **Objetivos**: Seguimiento individual
- **Puntuaciones**: Sistema de recompensas
- **Multas**: Control financiero

### Backup y Restauración
La aplicación incluye funciones automáticas de backup:
- Exportación completa de datos
- Formato JSON para máxima compatibilidad
- Restauración con validación de integridad

## 🔧 Funcionalidades Avanzadas

### Web Scraping Inteligente
- **Detección automática** de formatos de páginas
- **Reintentos automáticos** en caso de fallo
- **Validación de datos** antes de importar
- **Actualización incremental** de información

### Sistema de Notificaciones
- **Próximos partidos**: Alertas automáticas
- **Multas pendientes**: Recordatorios
- **Objetivos vencidos**: Seguimiento
- **Entrenamientos**: Confirmaciones

### Análisis y Estadísticas
- **Dashboards personalizables** por rol
- **Métricas avanzadas** de rendimiento
- **Comparativas temporales** y por jugador
- **Exportación de reportes** en múltiples formatos

## 🛡️ Seguridad

### Autenticación
- Contraseñas encriptadas con bcrypt
- Sesiones seguras con timeout automático
- Validación de datos en frontend y backend

### Privacidad
- Datos personales protegidos
- Acceso controlado por roles
- Auditoría de cambios

## 🤝 Contribución

1. Fork del proyecto
2. Crear rama para nueva funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

### Documentación
- [Wiki del proyecto](https://github.com/tu-usuario/ud-atzeneta/wiki)
- [FAQ](https://github.com/tu-usuario/ud-atzeneta/wiki/FAQ)
- [Troubleshooting](https://github.com/tu-usuario/ud-atzeneta/wiki/Troubleshooting)

### Contacto
- **Issues**: [GitHub Issues](https://github.com/tu-usuario/ud-atzeneta/issues)
- **Email**: soporte@udatzeneta.com
- **Documentación**: [Docs online](https://tu-usuario.github.io/ud-atzeneta/)

## 📈 Roadmap

### Versión 2.0 (Próximamente)
- [ ] API REST completa
- [ ] App móvil nativa
- [ ] Integración con redes sociales
- [ ] Sistema de mensajería interno
- [ ] Análisis avanzado con IA
- [ ] Modo offline

### Funcionalidades Planificadas
- [ ] Integración con GPS para entrenamientos
- [ ] Sistema de lesiones con seguimiento médico
- [ ] Planificación de entrenamientos
- [ ] Gestión de equipamiento
- [ ] Comunicación con padres/familiares

---

<div align="center">

**Desarrollado con ❤️ para el UD Atzeneta**

[🌟 Star en GitHub](https://github.com/tu-usuario/ud-atzeneta) • [🐛 Reportar Bug](https://github.com/tu-usuario/ud-atzeneta/issues) • [💡 Solicitar Funcionalidad](https://github.com/tu-usuario/ud-atzeneta/issues)

</div>