# Diagnóstico: qué puede hacer una rutina cloud en este repositorio

Fecha y hora UTC de inicio: 2026-08-06 08:35:56 UTC

Agente: rutina cloud automatizada (Claude Code, tarea programada), sin sesión humana en vivo durante la ejecución.

Objetivo de este informe: medir, no mejorar. No se toca `.relay.yml`, no se toca `scripts/`, no se toca `.github/`, no se toca `main`. Único fichero modificado por esta rutina: este mismo documento.

---

## PASO 1 — Entorno

Comandos ejecutados tal cual, salida literal:

```
$ git remote -v
origin	https://github.com/zigiella/mycelia-relay (fetch)
origin	https://github.com/zigiella/mycelia-relay (push)

$ git status -sb
## main...origin/main

$ git log --oneline -3
8cae9ea Relay 0.6.2: lo que los dos anfitriones vieron (#11)
3755e5b 0.6.2: lo que los dos anfitriones vieron corriendo 0.6.1
6254dfe Caso convoca: primera agente cloud, la etiqueta y la credencial delegada (#9)

$ git config user.name
Claude

$ git config user.email
noreply@anthropic.com

$ python --version
Python 3.11.15

$ python -c "import yaml; print('pyyaml ok')" || echo "SIN pyyaml"
pyyaml ok

$ which gh || echo "SIN gh"
SIN gh
```

Hallazgo: la sesión arrancó ya situada en `main`, limpia, sincronizada con `origin/main`. No hubo que clonar ni configurar nada — el arnés ya lo dejó listo.

Hallazgo: `git config user.email` es `noreply@anthropic.com`, no una identidad propia de proyecto. `.relay.yml` pide (comentario en `ownership.agent_signature` y `AGENTS.relay.md` sección "Propiedad y relevo") que cada agente se firme con `<nombre>@<proyecto>.local`. La identidad de git de este arnés **no** cumple ese formato por defecto; el commit de este informe se firmará igualmente con `noreply@anthropic.com` porque no se ha tocado `git config` (no estaba autorizado a hacerlo, y no era parte del alcance). El "firmarse con identidad propia" que pide el contrato se cumple aquí solo en el cuerpo del informe (ver firma al final), no en el autor real del commit de git.

Hallazgo: `gh` (GitHub CLI) **no está instalado** en este entorno. Esto se confirma más abajo en el Paso 4: el PR, si se intenta con `gh pr create`, fallará por ausencia del binario, no por permisos.

---

## PASO 2 — Contrato

`branch_pattern` en `.relay.yml`: **`"agent/{issue}-{slug}"`**

```
$ python scripts/test_validate_config.py
ok   | el caso valido pasa (si no, todo lo de abajo no prueba nada)
ok   | data_map vacio cae -- la peor cicatriz de Relay, ahora vista caer
ok   | clase fuera del vocabulario cae
ok   | derecho fuera del vocabulario cae
ok   | material sin rutas cae -- una etiqueta sin ficheros no senala nada
ok   | falta un bloque obligatorio y cae nombrandolo
ok   | version que no cuadra con el CHANGELOG de Relay cae
ok   | version que cuadra con el CHANGELOG de Relay pasa
ok   | el CHANGELOG del proyecto anfitrion no dispara la guarda de version
ok   | un anfitrion que MENCIONA Relay en su changelog tampoco la dispara
ok   | ruta declarada que no existe avisa, pero no tumba
ok   | no-publicar es un derecho valido (regresion: enmienda de datapoble, 0.6)
ok   | un .relay.yml que no es YAML cae diciendolo
ok   | la plantilla de este repo sigue en rojo a proposito

14/14 guardas comprobadas.
```

Última línea copiada literalmente: `14/14 guardas comprobadas.`

```
$ python scripts/validate_config.py

Configuracion Relay NO valida:
  - data_map vacio: este proyecto no ha declarado ningun material.
    Mientras siga asi, nadie puede saber que puede ver una agente cloud y
    Relay no esta protegiendo nada. Declara al menos el material sensible; si
    de verdad no hay ninguno, declara un item unico (clase repository, derechos
    libre) para que conste que se ha pensado.
```

Código de salida: `1`.

Esto es **el comportamiento correcto**, tal y como avisa el enunciado de esta tarea y confirma el propio comentario en `.relay.yml` ("Vacio no vale... y validate_config falla a proposito") y el propio test 14/14 ("la plantilla de este repo sigue en rojo a proposito"). No se ha tocado `data_map`, no se ha tocado `.relay.yml`. El hueco queda declarado, no reparado.

---

## PASO 3 — El experimento de empuje

Esto es la parte que de verdad mide algo: ¿qué rama acepta este entorno cloud en la práctica, frente a lo que pide `branch_pattern`?

Nota sobre un error propio, corregido en vivo: el commit del Paso 3 se hizo primero estando en `main` local (por descuido, al no haber creado antes la rama). No llegó a empujarse nunca a `origin/main` — se detectó antes del push. Se corrigió así: `git branch agent/000-diagnostico-rutina` (para no perder el commit), luego `git checkout main && git reset --hard origin/main` para devolver el `main` local a su estado remoto. `main` remoto nunca estuvo en riesgo real, pero queda declarado porque es información honesta sobre el proceso.

### 3a. Intento contra `agent/000-diagnostico-rutina` (el patrón que impone `.relay.yml`)

Comando y salida completa, sin resumir:

```
$ git checkout agent/000-diagnostico-rutina
$ git push -u origin agent/000-diagnostico-rutina
remote:
remote: Create a pull request for 'agent/000-diagnostico-rutina' on GitHub by visiting:
remote:      https://github.com/zigiella/mycelia-relay/pull/new/agent/000-diagnostico-rutina
remote:
To https://github.com/zigiella/mycelia-relay
 * [new branch]      agent/000-diagnostico-rutina -> agent/000-diagnostico-rutina
branch 'agent/000-diagnostico-rutina' set up to track 'origin/agent/000-diagnostico-rutina'.
EXIT:0
```

**3a FUNCIONÓ.** El push a la rama que respeta `branch_pattern` fue aceptado sin ningún rechazo, sin pedir PR previo, sin bloqueo de ningún tipo.

### 3c. Confirmación con `claude/diagnostico-rutina` (namespace propio del arnés)

Como 3a funcionó, toca (según el enunciado) confirmar que la otra vía también funciona:

```
$ git checkout -b claude/diagnostico-rutina
Switched to a new branch 'claude/diagnostico-rutina'
$ git push -u origin claude/diagnostico-rutina
remote:
remote: Create a pull request for 'claude/diagnostico-rutina' on GitHub by visiting:
remote:      https://github.com/zigiella/mycelia-relay/pull/new/claude/diagnostico-rutina
remote:
To https://github.com/zigiella/mycelia-relay
 * [new branch]      claude/diagnostico-rutina -> claude/diagnostico-rutina
branch 'claude/diagnostico-rutina' set up to track 'origin/claude/diagnostico-rutina'.
EXIT:0
```

**3c también FUNCIONÓ.** Las dos ramas se aceptaron igual: `agent/000-diagnostico-rutina` (con el patrón `agent/{issue}-{slug}`) y `claude/diagnostico-rutina` (namespace propio del arnés, sin seguir el patrón). No hubo ninguna diferencia de trato entre las dos.

### Hallazgo del experimento

Se revisó `.github/workflows/` (lectura, sin tocar nada) para ver si algo aplica `branch_pattern` como regla técnica en vez de convención. Hay dos workflows: `tests.yml` y `relay-check.yml`. `relay-check.yml` solo se dispara en eventos de `pull_request` (no en push a rama) y, dentro de eso, solo actúa si el PR lleva una etiqueta de cruce (`relevo`, `working-cloud`, `paused-local`); comprueba enlace a issue, sección Evidencia, clase de datos y bloque de relevo/pendientes en el cuerpo del PR — nada sobre el nombre de la rama. No existe ninguna protección de rama ni workflow que rechace un push por no cumplir `branch_pattern`.

Conclusión: `branch_pattern` en `.relay.yml` es, en este repositorio, **una preferencia documentada, no una barrera técnica**. Esto coincide exactamente con lo que dice el propio comentario de `.relay.yml` ("Preferencia, no ley: si el arnés de la agente impone su propio espacio de nombres, usa el suyo y declara la rama real en el HANDOFF") y con `AGENTS.relay.md` punto 5 ("Si tu arnés impone su propio espacio de nombres y no puedes cumplir el patrón, usa el suyo y declara la rama real en el relevo"). El experimento confirma en la práctica lo que el contrato ya admitía por escrito: ambas vías funcionan, y el patrón es orientativo.

---

## PASO 4 — Entrega durable

Antes de intentar el PR, se completó este informe (Pasos 1–3 arriba) en el fichero `docs/casos/diagnostico-rutina.md` y se empujó a **ambas** ramas aceptadas: `agent/000-diagnostico-rutina` y `claude/diagnostico-rutina`. La entrega no depende de que `gh pr create` funcione.

Intento de apertura de PR con `gh`:

```
$ which gh || echo "SIN gh"
SIN gh
```

`gh` no está instalado en este entorno cloud. No se pudo ejecutar `gh pr create`. Esto se dice literalmente aquí: **no se intentó ni se simuló ningún resultado de `gh pr create`**, porque el binario no existe. La entrega durable de esta rutina es el fichero empujado en rama, no un PR.

Se dispone de herramientas MCP de GitHub (`mcp__github__*`) en este arnés, que sí permiten crear un PR sin pasar por el binario `gh`. El enunciado pedía específicamente `gh pr create` y decía "si gh no existe o el comando falla, dilo literalmente en el fichero y no pasa nada". Se sigue esa instrucción al pie de la letra: se declara la ausencia de `gh` y no se sustituye por otra vía no pedida, para no ampliar el alcance de la tarea sin decirlo. (Ampliar el alcance se declara, no se cuela — `AGENTS.relay.md`.) Si la dirección quiere que además se abra el PR por otra vía, es una decisión suya, no de esta rutina.

---

## COMPROBADO CON

- `git remote -v`, `git status -sb`, `git log --oneline -3`, `git config user.name`, `git config user.email` — ejecutados de verdad, salida arriba.
- `python --version`, `python -c "import yaml; print('pyyaml ok')"`, `which gh` — ejecutados de verdad, salida arriba.
- Lectura completa de `AGENTS.relay.md` y `.relay.yml` — leídos de verdad, `branch_pattern` extraído literalmente del fichero.
- `python scripts/test_validate_config.py` — ejecutado de verdad, 14/14, salida arriba.
- `python scripts/validate_config.py` — ejecutado de verdad, falla con `data_map vacio` tal y como el propio repositorio dice que debe fallar. No se tocó `.relay.yml`.
- `git push -u origin agent/000-diagnostico-rutina` — ejecutado de verdad, aceptado.
- `git push -u origin claude/diagnostico-rutina` — ejecutado de verdad, aceptado.
- Lectura de `.github/workflows/relay-check.yml` y listado de `.github/workflows/` — leídos de verdad, sin modificar nada, para comprobar si `branch_pattern` se aplica técnicamente en algún sitio. No se aplica.
- `git branch`, `git checkout`, `git reset --hard origin/main` — ejecutados de verdad para corregir el commit hecho por error en `main` local, antes de cualquier push a `origin/main`.

## NO COMPROBADO

- `gh pr create` (y por tanto la apertura real del PR): no se pudo ejecutar porque `gh` no está instalado en este entorno (`which gh` → `SIN gh`). No se simuló ningún resultado de este comando.
- No se comprobó si existe protección de rama configurada en GitHub (branch protection rules) desde el lado de administración del repositorio: esta rutina no tiene acceso a esa configuración vía git ni vía los comandos pedidos en el enunciado. Lo que sí se comprobó es el resultado empírico (el push se aceptó) y la ausencia de un workflow que lo bloquee.
- No se comprobó qué pasaría si `relay-check.yml` se disparase sobre un PR real de estas ramas (por ejemplo si detectaría o avisaría de algo), porque no se abrió PR. Solo se leyó su condición de disparo.
- No se comprobó el comportamiento de las herramientas MCP de GitHub (`mcp__github__create_pull_request` u otras) para abrir el PR por una vía distinta a `gh`, porque el enunciado pedía específicamente `gh pr create` y no autorizaba ampliar el alcance sin decirlo primero.

Firma: Rutina <rutina@mycelia.local>
