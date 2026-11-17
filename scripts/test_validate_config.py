#!/usr/bin/env python3
"""Prueba en negativo del validador: cada guarda, vista caer.

Una guarda que no has visto caer no es una guarda. La regla llega de datapoble, donde
el patron "existe un verificador y no lo ejecuta nadie" mordio cinco veces, una de
ellas ocultando que dos almacenes servian numeros distintos para la misma metrica del
mismo municipio en 917 de 947 casos.

Relay tiene esa cicatriz en su propio validador, y por eso este fichero existe: hasta
0.5, validate_config daba verde con el data_map vacio. Se encontro LEYENDO EL CODIGO,
no porque la guarda fallara: nadie la habia visto caer nunca. Y la version corregida
tampoco se habia visto caer hasta hoy.

Cada caso inyecta un fallo y comprueba dos cosas: que el validador cae, y que cae POR
EL MOTIVO CORRECTO. Una guarda que salta por otra razon tampoco esta verificada.

Uso: python scripts/test_validate_config.py
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
VALIDADOR = RAIZ / "scripts" / "validate_config.py"

MAPA = """\
data_map:
  material-de-prueba:
    clase: repository
    derechos: libre
    rutas: ["dato.txt"]
"""

DERECHOS = """\
data_rights:
  libre: "Sin restriccion de derivacion"
  solo-agregado: "Sale agregado o anonimizado"
  no-reproducir: "Se lee, no se copia"
  no-publicar: "Se puede leer y procesar; no sale al producto"
  no-sale: "Ni se copia, ni se imprime, ni se deriva"
"""

BASE = """\
version: 0.6

project:
  tracker: github-issues
  default_branch: main

ownership:
  single_writer_per_task: true

checks:
  require_pull_request: true

data_classes:
  repository: "Puede vivir en el repo"
  cloud-ok: "Puede procesarse en un arnes cloud aprobado"
  local-only: "Solo ordenador autorizado"
  synthetic-only: "Cloud recibe solo muestras sinteticas o aprobadas"

""" + DERECHOS + "\n" + MAPA


def correr(config: str, *, changelog: str | None = None, ficheros=("dato.txt",)):
    """Ejecuta el validador sobre una configuracion aislada y devuelve (codigo, salida)."""
    with tempfile.TemporaryDirectory() as tmp:
        raiz = Path(tmp)
        (raiz / ".relay.yml").write_text(config, encoding="utf-8")
        for nombre in ficheros:
            (raiz / nombre).write_text("dato\n", encoding="utf-8")
        if changelog is not None:
            (raiz / "CHANGELOG.md").write_text(changelog, encoding="utf-8")
        p = subprocess.run(
            [sys.executable, str(VALIDADOR), str(raiz / ".relay.yml")],
            capture_output=True, text=True,
        )
        return p.returncode, p.stdout + p.stderr


# (nombre, kwargs para correr(), codigo esperado, fragmento que debe salir)
CASOS = [
    (
        "el caso valido pasa (si no, todo lo de abajo no prueba nada)",
        dict(config=BASE), 0, "valida",
    ),
    (
        "data_map vacio cae -- la peor cicatriz de Relay, ahora vista caer",
        dict(config=BASE.replace(MAPA, "data_map: {}\n")), 1, "data_map vacio",
    ),
    (
        "clase fuera del vocabulario cae",
        dict(config=BASE.replace("clase: repository", "clase: repositorio")), 1, "desconocida",
    ),
    (
        "derecho fuera del vocabulario cae",
        dict(config=BASE.replace("derechos: libre", "derechos: no-tocar")), 1, "desconocido",
    ),
    (
        "material sin rutas cae -- una etiqueta sin ficheros no senala nada",
        dict(config=BASE.replace('    rutas: ["dato.txt"]\n', "")), 1, "sin rutas",
    ),
    (
        "falta un bloque obligatorio y cae nombrandolo",
        dict(config=BASE.replace(DERECHOS, "")), 1, "data_rights",
    ),
    (
        "version que no cuadra con el CHANGELOG de Relay cae",
        dict(config=BASE, changelog="# Changelog - Mycelia Relay\n\n## 0.7 - 2026-01-01\n\nAlgo.\n"),
        1, "CHANGELOG",
    ),
    (
        "version que cuadra con el CHANGELOG de Relay pasa",
        dict(config=BASE, changelog="# Changelog - Mycelia Relay\n\n## 0.6 - 2026-01-01\n\nAlgo.\n"),
        0, "valida",
    ),
    (
        # La guarda es nuestra y el rojo iba a ser suyo: casi todo repositorio
        # anfitrion tiene su propio CHANGELOG.md en la raiz, junto al .relay.yml.
        "el CHANGELOG del proyecto anfitrion no dispara la guarda de version",
        dict(config=BASE, changelog="# Changelog de datapoble\n\n## 2.3.1 - 2026-07-20\n\nAlgo suyo.\n"),
        0, "valida",
    ),
    (
        # Lo que escribe cualquier equipo en SU changelog el dia que adopta Relay.
        # Con el criterio de "buscar en el cuerpo", el falso rojo volvia por aqui.
        "un anfitrion que MENCIONA Relay en su changelog tampoco la dispara",
        dict(config=BASE,
             changelog="# Changelog de convoca\n\n## 2.2 - 2026-08-02\n\nAdoptado Mycelia Relay 0.6.1.\n"),
        0, "valida",
    ),
    (
        "ruta declarada que no existe avisa, pero no tumba",
        dict(config=BASE, ficheros=()), 0, "aviso",
    ),
    (
        "no-publicar es un derecho valido (regresion: enmienda de datapoble, 0.6)",
        dict(config=BASE.replace("derechos: libre", "derechos: no-publicar")), 0, "valida",
    ),
    (
        "un .relay.yml que no es YAML cae diciendolo",
        dict(config="version: [0.6\nproject: {"), 1, "YAML",
    ),
    (
        # Desde 0.7. Un perfil mal escrito no puede leerse como "completo" en silencio.
        "un perfil fuera del vocabulario cae",
        dict(config=BASE.replace("version: 0.6\n", "version: 0.6\nperfil: ligero\n")), 1, "perfil='ligero'",
    ),
    (
        "perfil minimo es valido, y el validador dice cual ha leido",
        dict(config=BASE.replace("version: 0.6\n", "version: 0.6\nperfil: minimo\n")), 0, "perfil minimo",
    ),
    (
        "sin perfil se lee como completo: no se le quita nada a quien ya usaba Relay entero",
        dict(config=BASE), 0, "perfil completo",
    ),
]


def es_repo_de_relay() -> bool:
    """True solo dentro del repositorio del metodo, no en un proyecto que lo adopta.

    El criterio NO se reimplementa aqui: se importa del validador, que es donde vive
    desde 0.6.2. La primera version de esta funcion buscaba "Mycelia Relay" en los
    primeros 2000 caracteres del CHANGELOG, y eso es exactamente lo que un equipo
    escribe en SU changelog el dia que adopta Relay -- con lo que el falso rojo volvia
    por la puerta de al lado. Dos copias del mismo criterio divergen, y esta decide si
    una guarda corre.
    """
    ch = RAIZ / "CHANGELOG.md"
    if not ch.exists():
        return False
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from validate_config import es_changelog_de_relay
    return es_changelog_de_relay(ch.read_text(encoding="utf-8"))


def main() -> int:
    if not VALIDADOR.exists():
        print(f"No encuentro el validador en {VALIDADOR}")
        return 1

    fallos = 0
    for nombre, kwargs, codigo_esperado, fragmento in CASOS:
        codigo, salida = correr(**kwargs)
        ok = codigo == codigo_esperado and fragmento.lower() in salida.lower()
        print(f"{'ok  ' if ok else 'FALLA'} | {nombre}")
        if not ok:
            fallos += 1
            print(f"      esperaba codigo {codigo_esperado} y '{fragmento}'; "
                  f"obtuve codigo {codigo} y:")
            print("      " + salida.strip().replace("\n", "\n      "))

    # La plantilla de ESTE repositorio tiene que seguir EN ROJO: es una plantilla, no
    # una configuracion. Si algun dia alguien la "arregla" rellenandola, los equipos
    # se llevarian un data_map de mentira que valida. Esto lo caza.
    #
    # SOLO APLICA EN EL REPO DE RELAY. En un anfitrion, `RAIZ/.relay.yml` es la CONFIG
    # REAL del proyecto y esta legitimamente llena: alli este caso falla siempre, y un
    # rojo permanente se deja de leer -- la regla del propio Relay. Es la misma clase
    # de defecto que la guarda del CHANGELOG corregida en 0.6.1: escrita desde el punto
    # de vista del repo del metodo, rota en un anfitrion. La encontro datapoble al ser
    # el primer anfitrion que corrio este fichero.
    total = len(CASOS)
    if es_repo_de_relay():
        plantilla = RAIZ / ".relay.yml"
        p = subprocess.run([sys.executable, str(VALIDADOR), str(plantilla)],
                           capture_output=True, text=True, cwd=RAIZ)
        salida = p.stdout + p.stderr
        # En rojo POR EL MAPA VACIO Y SOLO POR ESO. Hasta 0.7 este caso solo miraba que el
        # rojo incluyera el mapa vacio, y un segundo motivo pasaba desapercibido: al preparar
        # 0.7, `.relay.yml` dijo 0.7 con el CHANGELOG aun en 0.6.2, y este caso dio verde.
        motivos = salida.count("\n  - ")
        ok = p.returncode == 1 and "data_map vacio" in salida and motivos == 1
        print(f"{'ok  ' if ok else 'FALLA'} | la plantilla de este repo sigue en rojo a proposito, "
              "y solo por el mapa vacio")
        if not ok:
            fallos += 1
            print("      el .relay.yml de Relay es una plantilla y debe fallar SOLO por el mapa vacio:")
            print("      " + salida.strip().replace("\n", "\n      "))
        total += 1
    else:
        print("skip | plantilla en rojo: solo aplica en el repo de Relay, no en un anfitrion")

    print(f"\n{total - fallos}/{total} guardas comprobadas.")
    if fallos:
        print("Hay guardas que no hacen lo que dicen.")
    return 1 if fallos else 0


if __name__ == "__main__":
    raise SystemExit(main())
