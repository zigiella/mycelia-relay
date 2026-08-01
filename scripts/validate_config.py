#!/usr/bin/env python3
from pathlib import Path
import sys

path = Path('.relay.yml')
if not path.exists():
    print('Falta .relay.yml')
    raise SystemExit(1)
text = path.read_text(encoding='utf-8')
required = ['version:', 'tracker:', 'single_writer_per_task:', 'data_classes:', 'data_reasons:']
missing = [key for key in required if key not in text]
if missing:
    print('Faltan claves: ' + ', '.join(missing))
    raise SystemExit(1)
print('Configuración Relay válida')
