# Adopción de Mycelia y Mycelia Relay en un proyecto (ejemplo anonimizado)

## Principio

El repositorio anfitrión sigue mandando: su `AGENTS.md` tiene prioridad. Mycelia aporta conocimiento durable. Relay aporta coordinación durable entre agentes locales y cloud.

## Archivos a añadir al anfitrión

- `.relay.yml`
- `AGENTS.relay.md`
- `.github/ISSUE_TEMPLATE/agent-task.yml`
- `.github/pull_request_template.md`

## Archivos a editar

- `AGENTS.md`: referencia a Relay y sustitución de registros duplicados por issues/PR cuando proceda.
- El documento de arranque del proyecto: arranque desde el issue asignado, no desde una lectura fija de todo el paquete.

## Configuración recomendada

```yaml
mycelia:
  repository: <owner>/mycelia          # metodo publico
  method_ref: <tag sellado>
  project_note: proyectos/<proyecto>/<proyecto>.md   # en la instancia privada
```

## Primer piloto

Elegir una tarea real con partición limpia entre nube y local. Ejemplo: especificar un conjunto de evaluación y su guía de etiquetado, con entorno `hybrid` y datos `synthetic-only`. El agente cloud prepara esquema, guía y tests con ejemplos sintéticos; el agente local trabaja sobre las muestras protegidas y devuelve solo resultados agregados. Ambos se relevan mediante checkpoints y bloques `HANDOFF`, sin que el material protegido salga del ordenador autorizado.
