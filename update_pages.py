import os

# Lista de archivos de páginas a actualizar
pages = [
    'partidos.py',
    'entrenamientos.py',
    'objetivos.py',
    'puntuacion.py',
    'multas.py'
]

# Plantilla para añadir al final de cada archivo
template = """
# Registrar callbacks al importar
if 'register_{module_name}_callbacks' in globals():
    register_{module_name}_callbacks()

# Definir el layout de la página
layout = create_{module_name}_layout()
"""

# Directorio de páginas
pages_dir = os.path.join(os.path.dirname(__file__), 'pages')

# Actualizar cada archivo
for page in pages:
    file_path = os.path.join(pages_dir, page)
    module_name = os.path.splitext(page)[0]
    
    # Verificar si el archivo existe
    if os.path.exists(file_path):
        # Leer el contenido actual
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Verificar si ya tiene la variable layout
        if 'layout = create_' in content:
            print(f"El archivo {page} ya tiene la variable layout definida.")
            continue
            
        # Verificar si el archivo tiene la función de registro de callbacks
        if f'register_{module_name}_callbacks()' in content:
            # Reemplazar solo la línea de registro de callbacks
            new_content = content.replace(
                f'register_{module_name}_callbacks()',
                template.format(module_name=module_name).strip()
            )
        else:
            # Añadir todo al final del archivo
            new_content = content.rstrip() + '\n\n' + template.format(module_name=module_name).strip() + '\n'
        
        # Escribir el contenido actualizado
        with open(file_path, 'w') as f:
            f.write(new_content)
            
        print(f"Actualizado: {page}")
    else:
        print(f"Advertencia: No se encontró el archivo {page}")

print("\nProceso completado. Por favor, verifica que los cambios sean correctos.")
print("Si hay algún error, asegúrate de que cada archivo tenga una función 'create_*_layout()' definida.")
