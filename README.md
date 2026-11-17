# Mycelia Relay

Capa operativa mínima para que agentes cloud y aplicaciones de escritorio colaboren sobre un proyecto sin compartir conversación ni depender de que una máquina siga encendida.

Mycelia Relay **no necesita Mycelia**. Se puede adoptar solo, en un repositorio cualquiera: lo que aporta (el issue como contrato, el bloque `HANDOFF`, el mapa de materiales con sus clases y derechos, los estados y las comprobaciones) funciona con las reglas escritas en el `REGLAS.md` del propio repositorio. El grafo de conocimiento aparece cuando hay **varios proyectos que quieren leerse entre sí**, no antes; entonces se enchufa el bloque `knowledge` de `.relay.yml`.

## Modelo

```text
repositorio anfitrión                       agentes
issue -> rama -> PR   <------------>   local / cloud
     (reglas en REGLAS.md)

    ...y si hay varios proyectos que quieren leerse entre sí,
    un grafo de conocimiento opcional colgando del issue.
```

- El **issue** es el contrato y el estado de la tarea.
- La **rama** pertenece a una sola agente escritora en cada momento.
- El **commit** es un checkpoint recuperable.
- El **PR** es la entrega y la revisión.
- El **handoff** permite cambiar de agente o entorno.

## Instalación en un proyecto, en dos pasos

Guía completa en [`docs/adopcion.md`](docs/adopcion.md). Y antes de empezar: **instalar Relay toca checks y reglas duras por definición, así que la ejecución de la adopción no escala** — viene autorizada por quien la encarga. Lo que sí escala es la transcripción de las reglas duras del proyecto, que la revisa quien las escribió.

El orden importa: las plantillas de issue y las etiquetas **solo surten efecto desde la rama por defecto**. Si todo el andamiaje entra por un PR que espera revisión humana, la primera tarea bajo Relay se ejecuta sin la mitad de lo que Relay promete.

**Paso 1 · bootstrap (andamiaje, directo a la rama por defecto).** Ficheros y etiquetas. Casi inerte, con una excepción honesta: `relay-check` empieza a correr en los PR. Por eso desde 0.4 **solo mira los que llevan etiqueta de cruce de entornos** (`relevo`, `working-cloud`, `paused-local`); en el resto sale de puntillas. Un aviso que salta en todos los PR se deja de leer, y el día que importa nadie lo mira.

```text
.github/ISSUE_TEMPLATE/agent-task.yml
.github/pull_request_template.md
.github/workflows/relay-check.yml
scripts/validate_config.py
```

Y las etiquetas de estado, una vez:

```bash
for l in agent-task ready working-local working-cloud paused-local blocked review done relevo; do gh label create "$l" --force; done
```

**Paso 2 · contrato (por PR, con revisión).** Lo que sí cambia cómo se trabaja:

```text
AGENTS.relay.md
.relay.yml
```

No sustituyas el `AGENTS.md` del proyecto. Añade en él una referencia a `AGENTS.relay.md` y deja que las reglas específicas del proyecto tengan prioridad.

**Y decide el perfil, en `.relay.yml`.** `perfil: minimo` es el núcleo: el mapa de materiales, el issue como contrato cuando el trabajo cambia de manos, el check con `relevo` y quién integra. Basta para un proyecto que trabaja en local, aunque tenga varias agentes. `perfil: completo` añade los relevos entre local y nube: los estados, el bloque `HANDOFF` y los checkpoints. Lo que un perfil mínimo no usa no se cumple a medias, se deja fuera a propósito. Sin el campo, el proyecto se lee como `completo`, que es lo que eran todos hasta 0.7.

## Estados · perfil completo

Solo con `perfil: completo`. Un proyecto con perfil mínimo no los usa, y no pasa nada.

- `ready`: tarea definida y reclamable.
- `working-local`: agente de escritorio activo.
- `working-cloud`: agente cloud activo.
- `paused-local`: el ordenador está apagado o la aplicación local cerrada.
- `blocked`: falta una decisión, permiso, dato o servicio.
- `review`: PR listo para revisión.
- `done`: PR integrado.

Cerrar el ordenador cambia disponibilidad, no propiedad. Una tarea `paused-local` solo pasa a otra agente mediante un handoff explícito.

Una tarea puede necesitar **varios legs** (la parte que ejecuta cada entorno). Mientras un `HANDOFF` deje "Siguiente acción" sin ejecutar, el issue sigue abierto aunque haya PRs integrados: `done` es del issue, no de cada PR.

## Regla de datos

La clase dice **dónde puede estar** el dato:

- `repository`: accesible a cualquier agente con permisos del repo.
- `cloud-ok`: puede utilizarse desde un arnés cloud aprobado.
- `local-only`: solo se abre en el ordenador autorizado; no se copia al repo ni a un agente cloud.
- `synthetic-only`: la nube recibe únicamente muestras sintéticas o anonimizadas aprobadas.

Y los **derechos** dicen qué se puede hacer con él, **con independencia de la clase**:

- `libre`: sin restricción de derivación.
- `solo-agregado`: sale agregado o anonimizado, nunca el dato individual.
- `no-reproducir`: se puede leer y usar; no copiar ni reproducir su contenido.
- `no-publicar`: se puede leer y procesar; no sale al producto.
- `no-sale`: ni se copia, ni se imprime, ni se deriva.

**Son dos ejes independientes, y ese es el punto.** Un material puede vivir legítimamente en el repositorio y ser obra ajena que se lee pero no se reproduce: `repository` + `no-reproducir`. Los derechos viajan con el dato, no con su ubicación. Y de ahí se sigue una consecuencia que hay que decir en voz alta: **la clase más restrictiva no arrastra los derechos más restrictivos**, así que se miran material por material y no por el peor de una sola columna.

Dos reglas que ahorran errores caros. **Lo que el proyecto publica deliberadamente no es `local-only`**: lo protegido suele ser la materia prima, no el producto — para el producto que se guarda pero no se sirve está `no-publicar`. Y **un derecho que no nombra su frontera no se puede cumplir**: si usas `no-publicar`, di en el `REGLAS.md` del proyecto dónde acaba tu producto (web, API, chat, allow-list de consultas).

Todo esto se declara en `data_map`, material a material, **con sus rutas**: una etiqueta sin ficheros no le dice a una agente cloud a qué te refieres. Y `data_map` vacío **no valida**: mientras lo esté, Relay no está protegiendo nada y `validate_config` lo dice en rojo.

## Qué se verifica solo

`scripts/validate_config.py` comprueba que el proyecto **ha declarado sus materiales**: `data_map` con clase, derechos y rutas de cada uno. Falla si está vacío, si un valor no es del vocabulario o si una entrada no apunta a ficheros; avisa si una ruta no existe hoy. Un verde aquí significa que alguien ha pensado qué puede ver la nube, no que la plantilla siga entera.

`.github/workflows/relay-check.yml` comprueba **cuatro cosas** en cada PR que lleva la etiqueta `relevo` (o `working-cloud`, `paused-local`), y solo en esos: que **enlaza un issue**, que la **Evidencia** tiene contenido, que declara la **clase de datos** y que dice qué queda **pendiente**. Lee los cuatro apartados de la plantilla por su encabezado y mira su contenido: la guía de la plantilla, entre `<!--` y `-->`, no cuenta, y una línea que es solo una etiqueta tampoco. Hasta 0.6.2 buscaba palabras sueltas por todo el cuerpo, y la plantilla **sin rellenar** pasaba tres de las cuatro. Un PR sin esas etiquetas sale `skipped` y no gasta minutos. Avisa por defecto; se endurece a fallo cuando el equipo lo quiera.

Y **las guardas se prueban en negativo**: `scripts/test_validate_config.py` inyecta cada fallo y comprueba que el validador cae *por el motivo correcto*, incluido que la plantilla de este repositorio siga en rojo **y solo** por su `data_map` vacío; y desde 0.7, `scripts/test_relay_check.py` hace lo mismo con el check, sacando su script del propio workflow. Corren en CI ([`tests.yml`](.github/workflows/tests.yml)), solo cuando cambia lo que prueban. Existe por una razón concreta: hasta 0.5 nuestro validador daba verde con el mapa vacío y **nadie lo había visto fallar nunca**; se descubrió leyendo el código. Una guarda que no has visto caer no es una guarda.

Lo que no se puede automatizar —que la evidencia sea *cierta*, que la clasificación sea *correcta*— sigue siendo criterio humano. Estas herramientas evitan el olvido; no sustituyen el juicio.

## Con o sin grafo de conocimiento

**Sin grafo** (lo normal al empezar): las reglas duras y las clases de datos del proyecto viven en su `REGLAS.md`, el issue enlaza lo que haga falta del propio repositorio, y el bloque `knowledge` de `.relay.yml` se queda vacío. Relay funciona entero.

**Con grafo**, cuando hay varios proyectos que quieren leerse entre sí: una tarea puede consumir notas enlazadas desde el issue y devolver conocimiento reusable. Los logs, ramas, checkpoints y pendientes se quedan en el repositorio anfitrión de todas formas.

En ambos casos, las agentes se firman con identidad propia (`<nombre>@<proyecto>.local`): el dominio nombra el proyecto, no la tecnología, porque un nombre sobrevive al cambio de modelo.

Relay mantiene el relevo. El proyecto produce. El conocimiento compartido, si hace falta, viene después.

## Versión

`0.7` (2026-11-17). Cambios y su origen en [`CHANGELOG.md`](CHANGELOG.md). **Ninguna regla de Relay nació de una intuición**: todas salieron de fricción medida en equipos reales — un piloto de relevo local↔cloud, dos auditorías de un equipo que llegó sin marco previo, la adopción de un equipo que llegó desde otro marco con equipo ya montado, y el uso diario de convoca desde agosto, medido por quien lo usaba.
