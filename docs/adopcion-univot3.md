# Adopción de Mycelia y Mycelia Relay en univot3

## Principio

`univot3` sigue siendo el repositorio anfitrión y su `AGENTS.md` sigue mandando. Mycelia aporta conocimiento durable. Relay aporta coordinación durable entre agentes locales y cloud.

## Archivos a añadir

- `.relay.yml`
- `AGENTS.relay.md`
- `.github/ISSUE_TEMPLATE/agent-task.yml`
- `.github/pull_request_template.md`

## Archivos a editar

- `AGENTS.md`: referencia a Relay y sustitución de registros duplicados por issues/PR cuando proceda.
- `MYCELIA.md`: referencia a `METHOD.yml`, al tag sellado y al nuevo reparto de planos.
- `START_HERE.md`: arranque desde issue asignado, no desde una lectura fija de todo el paquete.

## Configuración recomendada

```yaml
mycelia:
  repository: zigiella/mycelia
  method_ref: metodo-v0.1
  project_note: proyectos/univot3/univot3.md
```

## Primer piloto

Crear un issue para `T3-004 · conjunto gold y guía de etiquetado` con entorno `either` y datos `synthetic-only`. El agente cloud puede preparar esquema, guía y tests. El agente local trabaja sobre muestras protegidas. Ambos se relevan mediante checkpoints sin compartir el corpus real.
