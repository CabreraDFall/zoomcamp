from pathlib import Path

# Directorio actual donde está el script
current_dir = Path(__file__).parent

# Nombre del archivo del script para ignorarlo
current_file = Path(__file__).name

# Carpeta "test" en el mismo nivel que el script
test_dir = current_dir / "test"

# Lista de directorios a explorar: el mismo nivel y "test" si existe
dirs_to_search = [current_dir]
if test_dir.exists() and test_dir.is_dir():
    dirs_to_search.append(test_dir)

for directory in dirs_to_search:
    print(f"Files in {directory}:")
    
    for filepath in directory.iterdir():
        if filepath.name == current_file:
            continue  # saltar el script mismo

        print(f"  - {filepath.name}")

        if filepath.is_file():
            try:
                content = filepath.read_text(encoding='utf-8')
                print(f"    Content: {content}")
            except Exception as e:
                print(f"    Could not read file: {e}")