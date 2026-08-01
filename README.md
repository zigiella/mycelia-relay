# Mycelia Relay

Capa operativa mínima para que agentes cloud y aplicaciones de escritorio colaboren sobre un proyecto sin compartir conversación ni depender de que una máquina siga encendida.

Mycelia Relay **no necesita Mycelia**. Se puede adoptar solo, en un repositorio cualquiera: lo que aporta (el issue como contrato, el bloque `HANDOFF`, las clases de datos con su motivo, los estados y `relay-check`) funciona con las reglas escritas en el `REGLAS.md` del propio repositorio. El grafo de conocimiento aparece cuando hay **varios proyectos que quieren leerse entre sí**, no antes; entonces se enchufa el bloque `knowledge` de `.relay.yml`.

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

El orden importa: las plantillas de issue y las etiquetas **solo surten efecto desde la rama por defecto**. Si todo el andamiaje entra por un PR que espera revisión humana, la primera tarea bajo Relay se ejecuta sin la mitad de lo que Relay promete.

**Paso 1 · bootstrap (andamiaje, directo a la rama por defecto).** Ficheros y etiquetas. Casi inerte, con una excepción honesta: `relay-check` empieza a correr en los PR. Por eso desde 0.4 **solo mira los que llevan etiqueta de cruce de entornos** (`relevo`, `working-cloud`, `paused-local`); en el resto sale de puntillas. Un aviso que salta en todos los PR se deja de leer, y el día que importa nadie lo mira.

```text
.github/ISSUE_TEMPLATE/agent-task.yml
.github/pull_request_template.md
.github/workflows/relay-check.yml
```

Y las etiquetas de estado, una vez:

```bash
for l in ready working-local working-cloud paused-local blocked review done; do gh label create "$l" --force; done
```

**Paso 2 · contrato (por PR, con revisión).** Lo que sí cambia cómo se trabaja:

```text
AGENTS.relay.md
.relay.yml
```

No sustituyas el `AGENTS.md` del proyecto. Añade en él una referencia a `AGENTS.relay.md` y deja que las reglas específicas del proyecto tengan prioridad.

## Estados

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

Y el motivo dice **qué se puede derivar** de él, que es lo que de verdad pregunta quien trabaja desde la nube:

- `personal`: de ahí puede salir un agregado anónimo.
- `derechos-de-terceros`: obra ajena; no sale nada derivado de su contenido, por muy anonimizado que esté.
- `secreto-operativo`: no sale, y no se imprime.

Un mismo `local-only` con motivos distintos da permisos opuestos: por eso la clase sola no basta. Y una regla que ahorra un error caro: **lo que el proyecto publica deliberadamente no es `local-only`**; lo protegido suele ser la materia prima, no el producto.

## Qué se verifica solo

`.github/workflows/relay-check.yml` comprueba en cada PR lo que se puede comprobar sin humano: que enlaza un issue, que la sección de evidencia no está vacía y que la clase de datos está declarada. Avisa por defecto; se endurece a fallo cuando el equipo lo quiera. Lo que no se puede automatizar (que la evidencia sea *cierta*) sigue siendo revisión humana: el workflow evita el olvido, no sustituye el criterio.

## Con o sin grafo de conocimiento

**Sin grafo** (lo normal al empezar): las reglas duras y las clases de datos del proyecto viven en su `REGLAS.md`, el issue enlaza lo que haga falta del propio repositorio, y el bloque `knowledge` de `.relay.yml` se queda vacío. Relay funciona entero.

**Con grafo**, cuando hay varios proyectos que quieren leerse entre sí: una tarea puede consumir notas enlazadas desde el issue y devolver conocimiento reusable. Los logs, ramas, checkpoints y pendientes se quedan en el repositorio anfitrión de todas formas.

En ambos casos, las agentes se firman con identidad propia (`<nombre>@<proyecto>.local`): el dominio nombra el proyecto, no la tecnología, porque un nombre sobrevive al cambio de modelo.

Relay mantiene el relevo. El proyecto produce. El conocimiento compartido, si hace falta, viene después.

## Versión

`0.2` (2026-07-30). Cambios y su origen en [`CHANGELOG.md`](CHANGELOG.md). Cada regla de esta versión nació de una fricción real del primer piloto, no de una intuición.
