# test_database.py - Verifica la base de datos

print("🔍 Verificando base de datos...")

try:
    from database.db_manager import DatabaseManager, Calendario
    
    print("\n1. Probando conexión a la base de datos...")
    with DatabaseManager() as db:
        print("✅ Conexión exitosa")
        
        # Verificar tabla calendario
        calendario = db.get_calendario()
        print(f"📊 Partidos en la base de datos: {len(calendario) if calendario else 0}")
        
        if calendario:
            print("\n📋 Primeros 3 partidos:")
            for i, partido in enumerate(calendario[:3]):
                print(f"  {i+1}. {partido.fecha} - {partido.equipo_local} vs {partido.equipo_visitante}")
                print(f"     Competición: {partido.competicion}")
                print(f"     Scrapeado: {getattr(partido, 'scrapeado', 'Campo no existe')}")
                print()
        else:
            print("\n⚠️  No hay partidos en la base de datos")
            print("   Esto es normal si es la primera vez")
            
            # Intentar crear un partido de prueba
            print("\n🧪 Creando partido de prueba...")
            try:
                from datetime import date
                partido_prueba = Calendario(
                    fecha=date.today(),
                    hora="16:00",
                    competicion="Liga",
                    jornada="1",
                    equipo_local="UD Atzeneta",
                    equipo_visitante="Equipo Test",
                    scrapeado=False
                )
                db.save(partido_prueba)
                print("✅ Partido de prueba creado")
                
                # Verificar que se creó
                calendario_nuevo = db.get_calendario()
                print(f"📊 Partidos después de crear: {len(calendario_nuevo)}")
                
            except Exception as e:
                print(f"❌ Error creando partido de prueba: {e}")
        
        print("\n2. Verificando estructura de la tabla...")
        try:
            # Obtener un partido para verificar campos
            if calendario:
                primer_partido = calendario[0]
                campos = [attr for attr in dir(primer_partido) if not attr.startswith('_')]
                print(f"✅ Campos disponibles: {campos}")
                
                # Verificar campo scrapeado específicamente
                if hasattr(primer_partido, 'scrapeado'):
                    print(f"✅ Campo 'scrapeado' existe: {primer_partido.scrapeado}")
                else:
                    print("⚠️  Campo 'scrapeado' no existe en el modelo")
                    
        except Exception as e:
            print(f"❌ Error verificando estructura: {e}")

except Exception as e:
    print(f"❌ Error conectando a la base de datos: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)

# Test específico del scraping
print("🔍 Verificando scraping...")

try:
    from utils.scraping import scraping_manager, FFCVScraper
    print("✅ Scraping manager importado")
    
    # Test básico de conexión FFCV
    print("\n🌐 Probando conexión FFCV...")
    url = "https://resultadosffcv.isquad.es/equipo_calendario.php?id_temp=20&id_modalidad=33327&id_competicion=903498407&id_equipo=18331&torneo_equipo=903498408&id_torneo=903498408"
    
    scraper = FFCVScraper()
    soup = scraper.get_calendar_page(url)
    
    if soup:
        print("✅ Conexión FFCV exitosa")
        
        tabla = soup.find('table', class_='table calendario_table')
        if tabla:
            filas = tabla.find('tbody').find_all('tr') if tabla.find('tbody') else []
            print(f"📊 Partidos encontrados en FFCV: {len(filas)}")
        else:
            print("❌ No se encontró tabla en FFCV")
    else:
        print("❌ No se pudo conectar a FFCV")
        
except Exception as e:
    print(f"❌ Error con scraping: {e}")

print("\n" + "="*60)
print("💡 DIAGNÓSTICO:")
print("1. ✅ Si hay partidos en BD → Deberían aparecer en la tabla")
print("2. ⚠️  Si no hay partidos → Usar 'Importar FFCV'")
print("3. 🔧 Si hay errores → Compartir el output completo")
print("\n🚀 Ejecuta: python app.py")