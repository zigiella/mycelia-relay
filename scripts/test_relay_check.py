#!/usr/bin/env python3
"""Prueba en negativo de relay-check: el check, visto caer.

Hasta 0.7 este check no tenia ni una prueba, y por eso dos defectos vivieron meses sin
que nadie los viera: con STRICT=0 y un aviso el job salia en rojo, y si Evidencia era el
ultimo apartado se perdia su ultima linea. Los encontro convoca en la primera pasada real
(carta de Clara, 16-11-2026). Y al alinear el check con la plantilla aparecio un tercero:
la plantilla SIN RELLENAR pasaba tres de las cuatro comprobaciones.

Este fichero saca el script del propio workflow -- no una copia escrita a mano, que se
separaria del original -- y lo ejecuta con bash -e, como Actions, sobre cuerpos de PR
inventados. Cada caso mira el codigo de salida Y el mensaje.

Uso: python scripts/test_relay_check.py
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
WORKFLOW = RAIZ / ".github" / "workflows" / "relay-check.yml"
PLANTILLA = RAIZ / ".github" / "pull_request_template.md"

LLENO = """\
## Issue

Closes #7

## Evidencia

- Comprobado con: python scripts/test_validate_config.py, 14/14
- No comprobado y motivo: nada pendiente
- Premisas del encargo: contrastadas contra el repositorio, nada falso

## Clase de datos

`repository` · `libre`

## Pendientes

Ninguno.
"""

# El caso exacto de la propuesta 7 de Clara: Evidencia es el ULTIMO apartado, y de una linea.
EVIDENCIA_ULTIMA = """\
Closes #7

repository

pendientes: ninguno

## Evidencia

probado en local"""

# La plantilla de 0.6.2, sin rellenar. Es historica: no puede separarse de nada.
VIEJA_SIN_RELLENAR = """\
## Issue

Closes #

## Evidencia

- Comprobaciones ejecutadas:
- Resultados:
- No comprobado y motivo:

## Política de datos

- Material tocado (nombre en `data_map`):
- Clase y derechos: repository | cloud-ok | local-only | synthetic-only · libre | no-sale

## Handoff o pendientes

"""

VIEJA_RELLENA = """\
## Issue

Seguimiento: #13

## Evidencia

- Comprobaciones ejecutadas: las tres pruebas de Clara, en vivo

## Política de datos

- Clase y derechos: `repository` · `libre`

## Handoff o pendientes

- Sin cambio de versión. Pendiente la PR B.
"""

SOLO_ETIQUETAS = LLENO.replace(
    "- Comprobado con: python scripts/test_validate_config.py, 14/14\n"
    "- No comprobado y motivo: nada pendiente\n"
    "- Premisas del encargo: contrastadas contra el repositorio, nada falso\n",
    "- Comprobado con:\n- No comprobado y motivo:\n")

COMENTARIO_EN_EVIDENCIA = LLENO.replace(
    "- Comprobado con: python scripts/test_validate_config.py, 14/14\n"
    "- No comprobado y motivo: nada pendiente\n"
    "- Premisas del encargo: contrastadas contra el repositorio, nada falso\n",
    "<!-- aqui iria\n     la evidencia,\n     si la hubiera -->\n")

CLASE_SOLO_EN_COMENTARIO = LLENO.replace("`repository` · `libre`", "<!-- repository -->")


def es_repo_de_relay() -> bool:
    ch = RAIZ / "CHANGELOG.md"
    if not ch.exists():
        return False
    sys.path.insert(0, str(RAIZ / "scripts"))
    from validate_config import es_changelog_de_relay
    return es_changelog_de_relay(ch.read_text(encoding="utf-8"))


def script_del_workflow() -> str:
    import yaml
    wf = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    return wf["jobs"]["contrato"]["steps"][0]["run"]


# La ruta COMPLETA del bash del PATH. En Windows, pedir "bash" a secas hace que el sistema
# encuentre antes el bash.exe de WSL en System32 que el Git Bash del PATH: WSL no ve las
# rutas C:/... ni hereda las variables, y el check parece roto sin estarlo. Nos paso dos
# veces seguidas al preparar 0.7, con dos sintomas distintos.
BASH = shutil.which("bash") or "bash"


def correr(script_path: str, body: str, strict: str = "0") -> tuple[int, str]:
    p = subprocess.run([BASH, "-e", script_path], capture_output=True, text=True,
                       env={**os.environ, "BODY": body, "STRICT": strict})
    return p.returncode, p.stdout + p.stderr


def main() -> int:
    try:
        script = script_del_workflow()
    except ImportError:
        print("No puedo verificar: falta PyYAML (pip install pyyaml). Un 'no se' no es un verde.")
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        # Por fichero y no por `bash -c`: en Windows, `-c` rompe las comillas del script y
        # el resultado parece un defecto del check. Nos paso al preparar 0.7.
        ruta = Path(tmp) / "check.sh"
        ruta.write_text(script, encoding="utf-8", newline="\n")
        ruta_bash = ruta.as_posix()

        # (nombre, cuerpo, STRICT, codigo esperado, fragmento que debe salir)
        casos = [
            ("cuerpo vacio, STRICT=0 -> verde con sus 4 avisos (propuesta 1)",
             "", "0", 0, "4 aviso"),
            ("cuerpo vacio, STRICT=1 -> rojo", "", "1", 1, "4 aviso"),
            ("plantilla rellena -> sin avisos", LLENO, "0", 0, "PR completo"),
            ("Evidencia ULTIMA y de una linea -> sin aviso falso (propuesta 7)",
             EVIDENCIA_ULTIMA, "0", 0, "PR completo"),
            ("plantilla de 0.6.2 rellena -> sigue valiendo",
             VIEJA_RELLENA, "0", 0, "PR completo"),
            ("plantilla de 0.6.2 SIN rellenar -> 4 avisos (antes pasaba 3 de 4)",
             VIEJA_SIN_RELLENAR, "0", 0, "4 aviso"),
            ("Evidencia con solo etiquetas vacias -> avisa",
             SOLO_ETIQUETAS, "0", 0, "Evidencia esta vacia"),
            ("Evidencia con solo un comentario de varias lineas -> avisa",
             COMENTARIO_EN_EVIDENCIA, "0", 0, "Evidencia esta vacia"),
            ("clase de datos solo dentro de un comentario -> avisa",
             CLASE_SOLO_EN_COMENTARIO, "0", 0, "No se declara la clase"),
            ("cuerpo con saltos de linea de Windows (CRLF) -> sin avisos",
             LLENO.replace("\n", "\r\n"), "0", 0, "PR completo"),
        ]

        fallos = 0
        for nombre, body, strict, codigo, fragmento in casos:
            c, salida = correr(ruta_bash, body, strict)
            ok = c == codigo and fragmento in salida
            print(f"{'ok  ' if ok else 'FALLA'} | {nombre}")
            if not ok:
                fallos += 1
                print(f"      esperaba codigo {codigo} y '{fragmento}'; obtuve codigo {c}:")
                print("      " + salida.strip().replace("\n", "\n      "))

        total = len(casos)
        # La plantilla de ESTE repositorio, sin rellenar, tiene que avisar en las cuatro.
        # Solo aqui: en un proyecto, la plantilla es suya y puede ser otra.
        if es_repo_de_relay() and PLANTILLA.exists():
            c, salida = correr(ruta_bash, PLANTILLA.read_text(encoding="utf-8"))
            ok = c == 0 and "4 aviso" in salida
            print(f"{'ok  ' if ok else 'FALLA'} | la plantilla de este repo, sin rellenar, "
                  "avisa en las cuatro")
            if not ok:
                fallos += 1
                print("      " + salida.strip().replace("\n", "\n      "))
            total += 1
        else:
            print("skip | plantilla sin rellenar: solo aplica en el repo de Relay")

    print(f"\n{total - fallos}/{total} casos del check comprobados.")
    return 1 if fallos else 0


if __name__ == "__main__":
    raise SystemExit(main())
