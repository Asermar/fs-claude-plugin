#!/usr/bin/env python3
"""Procesa de forma secuencial los archivos modificados por Claude Code o Codex.

El hook acepta el campo ``tool_input.file_path`` usado por Write/Edit de Claude
Code y los bloques ``*** ... File:`` incluidos en ``tool_input.command`` por
``apply_patch`` de Codex. Primero actualiza el copyright y después ordena los
miembros de las clases PHP para evitar escrituras concurrentes sobre el mismo
archivo.
"""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable


@dataclass(frozen=True)
class ModifiedFile:
    """Representa un archivo afectado por la herramienta de edición."""

    path: Path
    is_new: bool = False


SUPPORTED_SUFFIXES = ('.php', '.xml', '.html.twig')


def _absolute_path(raw_path: str, cwd: Path) -> Path:
    """Convierte una ruta de la entrada del hook en una ruta absoluta."""
    path = Path(raw_path).expanduser()
    return path if path.is_absolute() else cwd / path


def _parse_apply_patch(command: str, cwd: Path) -> list[ModifiedFile]:
    """Extrae archivos creados, actualizados o movidos de un parche de Codex."""
    files: list[ModifiedFile] = []
    pending_is_new = False

    for line in command.splitlines():
        if line.startswith('*** Add File: '):
            files.append(ModifiedFile(_absolute_path(line[14:].strip(), cwd), True))
            pending_is_new = True
        elif line.startswith('*** Update File: '):
            files.append(ModifiedFile(_absolute_path(line[17:].strip(), cwd)))
            pending_is_new = False
        elif line.startswith('*** Move to: '):
            files.append(ModifiedFile(_absolute_path(line[13:].strip(), cwd), pending_is_new))

    return files


def modified_files(payload: dict[str, Any]) -> list[ModifiedFile]:
    """Normaliza la entrada del hook y devuelve archivos únicos en orden estable."""
    cwd = Path(str(payload.get('cwd') or Path.cwd())).expanduser()
    tool_name = str(payload.get('tool_name') or '')
    tool_input = payload.get('tool_input')
    if not isinstance(tool_input, dict):
        return []

    candidates: Iterable[ModifiedFile]
    if tool_name in {'Write', 'Edit'}:
        file_path = tool_input.get('file_path')
        candidates = (
            [ModifiedFile(_absolute_path(str(file_path), cwd), tool_name == 'Write')]
            if file_path
            else []
        )
    elif tool_name == 'apply_patch':
        candidates = _parse_apply_patch(str(tool_input.get('command') or ''), cwd)
    else:
        candidates = []

    unique: dict[Path, ModifiedFile] = {}
    for item in candidates:
        resolved = item.path.resolve(strict=False)
        previous = unique.get(resolved)
        unique[resolved] = ModifiedFile(
            resolved,
            item.is_new or (previous.is_new if previous else False),
        )
    return list(unique.values())


def _run(script: Path, *args: str) -> int:
    """Ejecuta un transformador y conserva su salida de error para diagnóstico."""
    result = subprocess.run(
        [sys.executable, str(script), *args],
        check=False,
        text=True,
    )
    return result.returncode


def process_file(item: ModifiedFile, scripts_dir: Path) -> int:
    """Aplica en orden los transformadores compatibles al archivo indicado."""
    file_path = item.path
    if not file_path.is_file() or not str(file_path).endswith(SUPPORTED_SUFFIXES):
        return 0

    copyright_args = [str(file_path), str(datetime.now().year)]
    if item.is_new:
        copyright_args.append('--new')

    result = _run(scripts_dir / 'update-copyright.py', *copyright_args)
    if result != 0:
        return result

    if file_path.suffix == '.php':
        return _run(scripts_dir / 'sort-class-members.py', str(file_path))
    return 0


def main() -> int:
    """Lee la entrada estándar del hook y procesa todos los archivos detectados."""
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, TypeError):
        return 0

    if not isinstance(payload, dict):
        return 0

    scripts_dir = Path(__file__).resolve().parent
    exit_code = 0
    for item in modified_files(payload):
        result = process_file(item, scripts_dir)
        if result != 0:
            exit_code = result
    return exit_code


if __name__ == '__main__':
    sys.exit(main())
