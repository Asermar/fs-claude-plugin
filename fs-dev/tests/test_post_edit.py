"""Pruebas del hook de edición compatible con Claude Code y Codex."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).parents[1] / 'scripts' / 'post-edit.py'
SPEC = importlib.util.spec_from_file_location('post_edit', SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
POST_EDIT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = POST_EDIT
SPEC.loader.exec_module(POST_EDIT)


class ModifiedFilesTest(unittest.TestCase):
    """Comprueba la normalización de las entradas de ambos hosts."""

    def test_claude_write_marks_new_file(self) -> None:
        """Write de Claude debe conservar la ruta y marcar el archivo como nuevo."""
        payload = {
            'cwd': '/tmp/project',
            'tool_name': 'Write',
            'tool_input': {'file_path': 'Model/Test.php'},
        }

        files = POST_EDIT.modified_files(payload)

        self.assertEqual(Path('/tmp/project/Model/Test.php').resolve(), files[0].path)
        self.assertTrue(files[0].is_new)

    def test_codex_patch_extracts_and_deduplicates_files(self) -> None:
        """apply_patch debe aceptar altas, cambios y movimientos sin duplicados."""
        payload = {
            'cwd': '/tmp/project',
            'tool_name': 'apply_patch',
            'tool_input': {
                'command': '\n'.join([
                    '*** Begin Patch',
                    '*** Add File: Model/New.php',
                    '*** Update File: Model/Test.php',
                    '*** Update File: Model/Test.php',
                    '*** Move to: Model/Renamed.php',
                    '*** End Patch',
                ]),
            },
        }

        files = POST_EDIT.modified_files(payload)

        self.assertEqual(3, len(files))
        self.assertEqual(Path('/tmp/project/Model/New.php').resolve(), files[0].path)
        self.assertTrue(files[0].is_new)
        self.assertEqual(Path('/tmp/project/Model/Test.php').resolve(), files[1].path)
        self.assertEqual(Path('/tmp/project/Model/Renamed.php').resolve(), files[2].path)


class ProcessFileTest(unittest.TestCase):
    """Comprueba la ejecución real y secuencial de los transformadores."""

    def test_updates_copyright_and_sorts_php(self) -> None:
        """Un PHP de FacturaScripts debe recibir ambas transformaciones."""
        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / 'Example.php'
            file_path.write_text(
                """<?php
/** Copyright (C) 2020 Example */
namespace FacturaScripts\\Plugins\\Demo;

class Example
{
    public function zebra(): void
    {
    }

    public function alpha(): void
    {
    }
}
""",
                encoding='utf-8',
            )

            result = POST_EDIT.process_file(
                POST_EDIT.ModifiedFile(file_path),
                SCRIPT_PATH.parent,
            )
            content = file_path.read_text(encoding='utf-8')

        self.assertEqual(0, result)
        self.assertIn(f'Copyright (C) 2020-{POST_EDIT.datetime.now().year}', content)
        self.assertLess(content.index('function alpha'), content.index('function zebra'))


if __name__ == '__main__':
    unittest.main()
