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

## Instalación en un proyecto

Copia estos archivos:

```text
AGENTS.relay.md
.relay.yml
.github/ISSUE_TEMPLATE/agent-task.yml
.github/pull_request_template.md
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

## Regla de datos

- `repository`: accesible a cualquier agente con permisos del repo.
- `cloud-ok`: puede utilizarse desde un arnés cloud aprobado.
- `local-only`: solo puede abrirse en el ordenador autorizado; nunca se copia al repo, a Mycelia ni a un agente cloud.
- `synthetic-only`: los agentes cloud reciben únicamente muestras sintéticas o anonimizadas aprobadas.

## Relación con Mycelia

Una tarea puede consumir notas de Mycelia y devolver conocimiento reusable. Los logs, ramas, checkpoints y pendientes permanecen en el repositorio anfitrión.

Mycelia recuerda. Relay mantiene el relevo. El proyecto produce.
