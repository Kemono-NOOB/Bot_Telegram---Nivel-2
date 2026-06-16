from pathlib import Path

csv_path = Path('E:/academia/Archivos/Departamento.csv')

print("=== DIAGNÓSTICO DEL CSV ===")
print(f"¿Archivo existe? {csv_path.exists()}")
print(f"Ruta completa: {csv_path.absolute()}")

if csv_path.exists():
    with open(csv_path, 'r', encoding='utf-8') as f:
        lineas = f.readlines()
    
    print(f"\n📄 Líneas totales: {len(lineas)}")
    
    for i, linea in enumerate(lineas[:5]):  # Mostrar primeras 5 líneas
        print(f"Línea {i}: {repr(linea)}")
    
    # Probar tu método de limpieza
    print("\n=== PROBANDO LIMPIEZA ===")
    for i, linea in enumerate(lineas[:2]):
        linea_limpia = linea.strip(',"').replace('\t', ' ')
        print(f"Original: {repr(linea)}")
        print(f"Limpia:   {repr(linea_limpia)}")
        
        partes = linea_limpia.split(',')
        print(f"Partes: {len(partes)} -> {partes}")
        print("-" * 50)
else:
    print("❌ El archivo NO existe en esa ubicación")