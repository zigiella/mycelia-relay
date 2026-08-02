# Caso · convoca, la primera semana con una agente cloud

*Escrito por Clara (mp1-escritores/convoca) el 2026-08-01, el día que Tejuelo —nuestra
primera agente cloud— entregó, fue revisada y fusionada. Relay v0.5,
`validate_config` en verde con 8 materiales.*

Convoca fue el equipo que llegó **sin marco previo** y cuya primera auditoría movió
la 0.4. Este caso cuenta qué pasó cuando el contrato dejó de ser papel: una agente
real, dos PR reales, y tres cosas que el método todavía no decía.

## Los números del primer día

Tejuelo (Claude Code, cloud) recibió un issue-contrato con seis criterios medibles y
un alcance de 27 libros sin género. Entregó:

- **26 clasificados con fuente y 1 abstención declarada** — la abstención contaba
  como respuesta válida en el contrato, y eso cambia lo que la agente hace cuando no
  sabe: lo dice, en vez de rellenar.
- **2 aciertos sobre casos de control** que vivían fuera del repositorio. La agente
  sabía que existía verificación; no sabía cuáles eran los casos.
- **Un par comprobado/no-comprobado que ahorró una tarde**: declaró que no pudo abrir
  ninguna de las 26 URLs que citaba (su entorno bloqueaba el HTTPS de salida), así
  que la revisión local supo exactamente qué faltaba. 25 de 26 abrían.
- Su segundo PR no traía código: traía **su jaula medida** (`connect_rejected` host a
  host) y una objeción correcta al diseño del issue — pedía junto *juzgar un libro*
  (criterio, le basta buscar) y *comprobar que un enlace abre* (mecánico, necesita
  red). Cuando se piden juntas, la limitación del entorno se disfraza de problema de
  la tarea.

## Lo que Relay ya resolvía

El issue como contrato funcionó tal cual: la agente no oye el chat, y todo lo que
necesitaba estaba escrito. El par comprobado/no-comprobado es lo que más rinde por
línea de todo el método. Y `data_map` con rutas hizo su trabajo dos veces: al
definirla (solo ve `repository`) y al revisarla.

## Los dos arreglos de este PR

**1 · El bootstrap no crea `agent-task`.** La plantilla de issue declara
`labels: ["agent-task", "ready"]`, pero la línea de `gh label create` del README no
la incluye: el primer issue real falla al etiquetarse. Es la cicatriz del piloto
T3-004 —«las etiquetas no existen hasta que alguien las da de alta»— repetida con
otra etiqueta. Una palabra en el README.

**2 · La credencial delegada, como ejemplo en la plantilla.** Nuestra agente necesitó
dos credenciales en su entorno cloud: el token de un proxy de *solo lectura* y el de
un bot que *solo avisa*. El mapa decía `local-only` («una agente cloud no recibe una
clave») y la realidad decía otra cosa — lo señaló la propia agente: *la declaración
tiene que casar con la realidad*. La solución no tocó el método, y esa es la noticia:
v0.5 ya la expresaba, porque sus dos ejes son independientes — `cloud-ok` (dónde
puede estar) + `no-sale` (qué se hace con ella). Va como tercer ejemplo comentado en
la plantilla para que el siguiente equipo no crea que toda clave es `local-only`, con
las dos condiciones que la limitan: daño máximo pequeño y acotado, y rotable en
minutos. Una clave que gasta, despliega o escribe es `local-only` siempre.

## Lo que no es de Relay pero le pasará a quien adopte

- **Las variables de entorno entran en caliente; la política de red, no.** En el
  arnés cloud que usamos, cambiar los dominios permitidos exige sesión nueva y nada
  lo dice. A nuestra agente le costó tres intentos y una sesión.
- **La herramienta que invita al bucle trae la cortesía puesta.** Nuestra agente tuvo
  que escribir a mano el ritmo por host para no lanzar ráfagas a las editoriales. Si
  la pausa y la caché viven fuera de la herramienta de lectura, cada agente las
  reimplementa —o no— y el bloqueo se lo come el proyecto.
- **Explicar por chat es un agujero, no una ayuda.** Lo que la agente preguntó y el
  repositorio no respondía acabó como documentación, no como respuesta. La regla que
  nos dimos: *si tuviste que adivinar algo que debería estar escrito, es un hueco de
  nuestra documentación, no un fallo tuyo*.

---

*Clara <clara@mp1-escritores.local>*
