# Adoptar Mycelia Relay en un proyecto

Relay **no necesita ningún método de conocimiento**: se adopta solo, en un repositorio cualquiera, y lo que aporta funciona con las reglas escritas en el propio repositorio.

## Principio

El repositorio anfitrión sigue mandando: su `AGENTS.md` tiene prioridad y Relay no lo sustituye. Relay aporta una sola cosa: **coordinación durable entre agentes locales y cloud** — el issue como contrato, la rama con una sola escritora, el `HANDOFF` como relevo y el mapa de materiales que dice qué puede ver quién.

## La ejecución de la adopción no escala

Instalar Relay **toca las comprobaciones y las reglas duras por definición**: dos de las entradas que la propia lista de escalados manda subir a la dirección. Un equipo literal se bloquea en el paso 1 pidiendo permiso para instalar el permiso.

No hace falta: **la adopción viene autorizada por quien la encarga.** Lo que sí escala es cualquier decisión de contenido que surja al hacerla, y en particular una:

> **La transcripción de las reglas duras la revisa quien las escribió.** Va en su propio PR, separada del andamiaje, para que se pueda leer sin buscarla entre ficheros de configuración.

Sale de una adopción real: una coordinadora transcribió las reglas de su propia dirección, incluidas las de seguridad, sin que nadie las revisara. Salieron bien. El método no debería depender de que salgan bien.

## Paso 1 · Andamiaje, directo a la rama por defecto

El orden importa: las plantillas de issue y las etiquetas **solo surten efecto desde la rama por defecto**. Si todo entra por un PR que espera revisión, la primera tarea bajo Relay corre sin la mitad de lo que Relay promete.

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

Es casi inerte, con una excepción honesta: `relay-check` empieza a correr en los PR. Desde 0.4 solo mira los que llevan etiqueta de cruce de entornos, así que en el resto sale de puntillas.

`scripts/test_validate_config.py` y `.github/workflows/tests.yml` son **opcionales pero portables**: si copias el validador, cópialos y tendrás la prueba de que tu copia hace lo que dice — que es más de lo que tuvimos nosotros durante cinco versiones. El caso que solo tiene sentido en el repositorio del método se declara `skip` en voz alta. Copia el workflow **solo** si copias también el script: sin él, tu CI queda en rojo.

## Paso 2 · Contrato, por PR y con revisión

```text
AGENTS.relay.md
.relay.yml
```

En el `AGENTS.md` del proyecto, una referencia a `AGENTS.relay.md` dejando claro que las reglas específicas del proyecto tienen prioridad. Y en el documento de arranque: **se arranca desde el issue asignado**, no desde una lectura fija de todo el paquete.

## Paso 3 · El mapa de materiales, que es el trabajo de verdad

`data_map` llega vacío y **vacío no valida**: `validate_config.py` falla a propósito mientras lo esté. No es burocracia — mientras el mapa esté vacío nadie sabe qué puede ver una agente cloud, y Relay no está protegiendo nada aunque el fichero esté instalado.

Material a material: **dónde puede estar** (clase) y **qué se puede hacer con él** (derechos), con sus **rutas** reales.

```yaml
data_map:
  sinopsis-de-terceros:
    clase: repository        # vive en el repo, es el producto
    derechos: no-reproducir  # pero es obra ajena: se lee, no se copia
    rutas: ["data/sinopsis.json"]
  capa-electoral:
    clase: repository        # ya esta publicada: local-only seria falso
    derechos: no-publicar    # decision editorial: no se sirve ni se deriva
    rutas: ["data/electoral/**"]
  cache-fuente:
    clase: local-only
    derechos: solo-agregado  # trae correos: sale el agregado, no el dato
    rutas: ["cache/**"]
```

Tres errores que cuestan caro y se evitan aquí:

- **Lo que el proyecto publica deliberadamente no es `local-only`.** Lo protegido suele ser la materia prima, no el producto; marcar el producto como local obliga a despublicar para cumplirlo.
- **La clase más restrictiva no arrastra los derechos más restrictivos.** Son dos ejes independientes. Un material sin ninguna restricción de ubicación puede llevar el derecho que más te limita.
- **Un derecho que no nombra su frontera no se puede cumplir.** Si usas `no-publicar`, di en el `REGLAS.md` del proyecto dónde acaba tu producto: web, API, chat, allow-list de consultas.

## Antes de invitar a la primera agente cloud

Una agente cloud **clona el repositorio entero**. Declarar un material como `local-only` en `data_map` **no lo saca del repositorio** si ya estaba dentro.

Comprueba que lo marcado como local de verdad no está versionado. Si algo protegido ya entró en el historial, dilo antes de seguir: sacarlo es otra conversación, y es de la dirección. Si la declaración y la realidad no coinciden, `data_map` es un cartel de «prohibido el paso» en una puerta abierta.

## El primer piloto

Elige una tarea real con partición limpia entre nube y local. Ejemplo probado: especificar un conjunto de evaluación y su guía de etiquetado, entorno `hybrid`, datos `synthetic-only`. La agente cloud prepara esquema, guía y tests con ejemplos sintéticos; la local trabaja sobre las muestras protegidas y devuelve solo agregados. Se relevan con checkpoints y bloques `HANDOFF`, sin que el material protegido salga del ordenador autorizado.

Lo que se aprende ahí no es velocidad, es **distancia**: la agente entrante no arrastra el contexto de por qué las cosas son como son, así que lee lo escrito en vez de lo que recuerda. En el piloto real encontró cinco desacuerdos que la saliente no podía ver por estar demasiado cerca.

## Adopciones documentadas

- [`casos/datapoble-desde-cambium.md`](casos/datapoble-desde-cambium.md) — un equipo que llega con equipo montado y dos meses de otro marco. Cuatro fases, sin trabajo en vuelo, y cuatro huecos del método que salieron de ahí.
