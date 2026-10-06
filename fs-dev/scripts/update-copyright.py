#!/usr/bin/env python3
"""Actualiza el año de copyright en archivos de FacturaScripts.

Casos que gestiona (en modo normal):
1. Sin año → añade el año actual
   Copyright (C) Carlos → Copyright (C) 2026 Carlos
2. Año único igual al actual → sin cambios
   Copyright (C) 2026 Carlos → sin cambios
3. Año único diferente al actual → añade el año final
   Copyright (C) 2023 Carlos → Copyright (C) 2023-2026 Carlos
4. Rango con año final igual al actual → sin cambios
   Copyright (C) 2023-2026 Carlos → sin cambios
5. Rango con año final diferente al actual → actualiza el año final
   Copyright (C) 2023-2024 Carlos → Copyright (C) 2023-2026 Carlos

En modo archivo nuevo (--new):
- Reemplaza cualquier copyright con solo el año actual
  Copyright (C) 2023 Carlos → Copyright (C) 2026 Carlos

Solo actúa sobre archivos que pertenecen al core o a un plugin de FacturaScripts:
- Archivos con 'namespace FacturaScripts\\'.
- Archivos situados dentro de un plugin (carpeta con facturascripts.ini) o de una
  instalación del core (composer.json de facturascripts/facturascripts o carpetas
  Core, Plugins y Dinamic).
El resto de archivos, como los de proyectos Laravel o módulos de terceros, se ignoran.

Uso: update-copyright.py <file_path> <current_year> [--new]
"""
import json
import re
import sys
from pathlib import Path


def _is_copyright_update_enabled() -> bool:
    """Comprueba si updateCopyright está activado en ~/.fs-claude.json (por defecto: True)."""
    fs_claude = Path.home() / '.fs-claude.json'
    if not fs_claude.exists():
        return True
    try:
        config = json.loads(fs_claude.read_text(encoding='utf-8'))
        return bool(config.get('settings', {}).get('updateCopyright', True))
    except Exception:
        return True


def _is_facturascripts_root(directory: Path) -> bool:
    """Indica si el directorio es la raíz de una instalación del core de FacturaScripts."""
    composer = directory / 'composer.json'
    if composer.is_file():
        try:
            data = json.loads(composer.read_text(encoding='utf-8'))
            if data.get('name') == 'facturascripts/facturascripts':
                return True
        except Exception:
            pass

    return all((directory / name).is_dir() for name in ('Core', 'Plugins', 'Dinamic'))


def is_facturascripts_file(file_path: Path, content: str) -> bool:
    """Indica si el archivo pertenece al core o a un plugin de FacturaScripts.

    Se considera de FacturaScripts si declara un namespace FacturaScripts\\ o si
    algún directorio ascendente es la raíz de un plugin (contiene facturascripts.ini)
    o de una instalación del core.
    """
    if 'namespace FacturaScripts\\' in content:
        return True

    for directory in file_path.resolve().parents:
        if (directory / 'facturascripts.ini').is_file() or _is_facturascripts_root(directory):
            return True
    return False


def update_copyright_year(content: str, current_year: int, is_new_file: bool = False) -> str:
    """Actualiza las líneas de copyright con el año actual según las reglas definidas."""

    def replace_match(match) -> str:
        prefix = match.group(1)     # "Copyright (C) "
        year_part = match.group(2)  # None | "2023 " | "2023-2024 "
        rest = match.group(3)       # "Carlos Garcia Gomez ..."

        # Para archivos nuevos: siempre usar solo el año actual
        if is_new_file:
            return f"{prefix}{current_year} {rest}"

        # Caso 1: sin año → añadir el año actual
        if year_part is None:
            return f"{prefix}{current_year} {rest}"

        year_str = year_part.strip()

        if '-' in year_str:
            parts = year_str.split('-', 1)
            start_year = parts[0]
            end_year = int(parts[1])

            # Caso 4: rango con año final igual al actual → sin cambios
            if end_year == current_year:
                return match.group(0)

            # Caso 5: rango con año final diferente → actualizar año final
            return f"{prefix}{start_year}-{current_year} {rest}"
        else:
            single_year = int(year_str)

            # Caso 2: año único igual al actual → sin cambios
            if single_year == current_year:
                return match.group(0)

            # Caso 3: año único diferente → añadir año final
            return f"{prefix}{year_str}-{current_year} {rest}"

    # Patrón: "Copyright (C) " seguido de años opcionales (con espacio) y el resto
    pattern = r'(Copyright \(C\) )(\d{4}(?:-\d{4})? )?(.+)'
    return re.sub(pattern, replace_match, content)


def main() -> None:
    """Lee los argumentos, comprueba que el archivo es de FacturaScripts y actualiza su copyright."""
    if not _is_copyright_update_enabled():
        sys.exit(0)
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print(f"Uso: {sys.argv[0]} <file_path> <current_year> [--new]", file=sys.stderr)
        sys.exit(1)

    file_path = sys.argv[1]
    is_new_file = '--new' in sys.argv

    try:
        current_year = int(sys.argv[2])
    except ValueError:
        print(f"Error: el año debe ser un número entero, recibido: {sys.argv[2]}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            original = f.read()
    except (OSError, IOError) as e:
        print(f"Error leyendo {file_path}: {e}", file=sys.stderr)
        sys.exit(1)

    if not is_facturascripts_file(Path(file_path), original):
        sys.exit(0)

    updated = update_copyright_year(original, current_year, is_new_file)

    if updated != original:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated)
        except (OSError, IOError) as e:
            print(f"Error escribiendo {file_path}: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == '__main__':
    main()
