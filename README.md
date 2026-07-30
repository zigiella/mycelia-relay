# Mycelia Relay

Capa operativa mínima para que agentes cloud y aplicaciones de escritorio colaboren sobre un proyecto sin compartir conversación ni depender de que una máquina siga encendida.

Mycelia Relay no guarda conocimiento de mundo. Para eso está Mycelia. Relay gobierna únicamente el trabajo en curso dentro del repositorio anfitrión.

## Modelo

```text
Mycelia                 repositorio anfitrión             agentes
conocimiento  <------>  issue -> rama -> PR  <------>  local / cloud
```

- El **issue** es el contrato y el estado de la tarea.
- La **rama** pertenece a una sola agente escritora en cada momento.
- El **commit** es un checkpoint recuperable.
- El **PR** es la entrega y la revisión.
- El **handoff** permite cambiar de agente o entorno.

## Instalación en un proyecto, en dos pasos

El orden importa: las plantillas de issue y las etiquetas **solo surten efecto desde la rama por defecto**. Si todo el andamiaje entra por un PR que espera revisión humana, la primera tarea bajo Relay se ejecuta sin la mitad de lo que Relay promete.

**Paso 1 · bootstrap (andamiaje, directo a la rama por defecto).** Son ficheros inertes y etiquetas: no cambian el proceso de nadie y por eso no necesitan puerta.

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

- `repository`: accesible a cualquier agente con permisos del repo.
- `cloud-ok`: puede utilizarse desde un arnés cloud aprobado.
- `local-only`: solo puede abrirse en el ordenador autorizado; nunca se copia al repo, a Mycelia ni a un agente cloud.
- `synthetic-only`: los agentes cloud reciben únicamente muestras sintéticas o anonimizadas aprobadas.

## Qué se verifica solo

`.github/workflows/relay-check.yml` comprueba en cada PR lo que se puede comprobar sin humano: que enlaza un issue, que la sección de evidencia no está vacía y que la clase de datos está declarada. Avisa por defecto; se endurece a fallo cuando el equipo lo quiera. Lo que no se puede automatizar (que la evidencia sea *cierta*) sigue siendo revisión humana: el workflow evita el olvido, no sustituye el criterio.

## Relación con Mycelia

Una tarea puede consumir notas de Mycelia y devolver conocimiento reusable. Los logs, ramas, checkpoints y pendientes permanecen en el repositorio anfitrión. Las agentes se firman con identidad propia (`<nombre>@<proyecto>.local`) y se registran en el roster de la instancia; el método lo detalla en `metodo/nucleo/identidad-y-nombres.md`.

Mycelia recuerda. Relay mantiene el relevo. El proyecto produce.

## Versión

`0.2` (2026-07-30). Cambios y su origen en [`CHANGELOG.md`](CHANGELOG.md). Cada regla de esta versión nació de una fricción real del primer piloto, no de una intuición.
