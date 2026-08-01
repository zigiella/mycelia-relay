# Changelog · Mycelia Relay

## 0.4.1 · 2026-07-31

Corrige el defecto de `v0.4`: **el cambio principal no llegó a `.relay.yml`**, que es justo el fichero que los equipos copian. Seguía en `version: 0.2` (mal desde 0.3) y encabezado por un bloque `mycelia:` con `method_repository`, o sea exactamente la dependencia visible que 0.4 venía a quitar. El README y el contrato sí decían lo correcto; la plantilla no.

Ahora `.relay.yml` no menciona ningún método de conocimiento hasta el final, en un bloque `knowledge:` **opcional y vacío por defecto**, y trae `data_map` para declarar clase y motivo de cada material del proyecto.

La cicatriz que deja: se selló `v0.4` sin abrir el artefacto sellado. El tag no se reescribe; se supera. Verificar antes de sellar, no después.

## 0.4 · 2026-07-31

**Relay se sostiene solo.** Cuatro cambios de una auditoría de Clara (mp1-escritores), el primer equipo que llegó sin marco previo y por eso vio costuras que un equipo con reglas propias ya tapa sin darse cuenta.

**Sin dependencia de Mycelia** (decisión de la dirección, confirmada por el hallazgo de Clara). El contrato asumía el grafo: `.relay.yml` pedía repositorio de conocimiento y nota de proyecto, y el contrato mandaba leer las notas enlazadas desde el issue. La dependencia era **incidental, no esencial**: lo que Relay aporta funciona con las reglas escritas en el `REGLAS.md` del propio repositorio. El bloque `knowledge` pasa a opcional y el grafo se enchufa cuando hay varios proyectos que quieren leerse entre sí. Sin esto, un equipo con un problema urgente y acotado tenía que adoptar dos marcos a la vez, y la mitad diría que no a los dos.

**El issue es el contrato cuando el trabajo cruza entornos o cambia de manos.** La regla estaba bien y su alcance no: escrita para todo el trabajo, obligaba a abrir un issue por cada observación de la dirección, que es el cuello de botella que el método quiere evitar. La razón real de la regla es que **una agente cloud no oye el chat**; fuera de ese caso, la dirección manda por su canal.

**La clase de datos va con su motivo.** La clase dice dónde puede estar el dato; el motivo (`personal`, `derechos-de-terceros`, `secreto-operativo`) dice qué se puede derivar de él. Un mismo `local-only` puede ser un corpus con datos personales (de ahí sale un agregado anónimo) u obra ajena (de ahí no sale nada), y hasta ahora se etiquetaban igual. Se añade la regla que evita el error inverso: **lo que el proyecto publica deliberadamente no es `local-only`**; lo protegido suele ser la materia prima, no el producto.

**El bootstrap deja de prometer lo que no cumple.** `relay-check` corría en todos los PR y avisaba en todos los de un proyecto en marcha; ahora solo mira los marcados como cruce de entornos. Un aviso que salta siempre se deja de leer.

## 0.3 · 2026-07-30

**Quién integra**, el hueco que la auditoría del método destapó: v0.2 del método decía quién *no* integra (el verificador) y nunca decía quién *sí*. Decisión de la dirección: **el par de cada proyecto integra el trabajo de su proyecto cuando el merge es rutinario**; escalan a la dirección la membrana, las reglas duras, **lo que toca comprobaciones o permisos** (quien controla los checks controla la verificación futura), el cambio masivo, y sobre todo **la duda**: preguntar es gratis, integrar con dudas lo paga quien viene detrás.

Sustituye `human_merge: true` por `merge_authority` + `escalate_to_direction` en `.relay.yml`. Descartadas por la dirección: la integración cruzada entre proyectos (daría a cada agente acceso a repos que no le tocan) y que el par de la dirección integrara el trabajo ajeno de todos los proyectos (propuesta tumbada por un adversario: creaba cuello de botella y coordinadora encubierta, y la escribía quien se beneficiaba de ella).

## 0.2 · 2026-07-30

Primera versión con cicatrices: **las ocho reglas nuevas nacieron de la fricción del primer piloto real** (relevo local→cloud sobre una tarea de evaluación), no de intuiciones. Tres las trajo la agente local; cinco, la mano cloud que la relevó.

**Instalación en dos pasos** (huevo-y-gallina, hallazgo local). Las plantillas de issue y las etiquetas solo surten efecto desde la rama por defecto; si todo el andamiaje entra por un PR con revisión humana, la primera tarea bajo Relay corre sin la mitad de lo que Relay promete. Ahora: bootstrap inerte directo (plantillas, workflow, etiquetas) y contrato por PR.

**Estado de partida en el issue** (hallazgo local). Al instalar Relay sobre un proyecto en marcha, la mayoría de tareas están hechas en parte: en el piloto, 4 de 7 criterios ya estaban cubiertos y solo se supo al escribir el issue. Campo nuevo en la plantilla y regla de verificar esa cobertura contra el repo *antes* de escribir.

**Qué hacer cuando no puedes cumplir el entorno declarado** (hallazgo local). Un issue `hybrid` puede tocarte solo una mitad. Orden fijado: particiona y entrega tu leg; bloquea solo si no es separable; **nunca simules el otro entorno** (un relevo imitado con un subagente del mismo arnés produce evidencia falsa).

**Definición de leg cumplido** (hallazgo cloud). No estaba escrito qué debe producir la parte de una tarea para contar: artefacto, verificación ejecutada y declarada, relevo publicado y entrega por PR. Un leg que solo produce conversación no está cumplido.

**Un issue con relevo vivo no se cierra** (hallazgo cloud). En el piloto, un `Closes #N` de un PR parcial cerró el issue con la "Siguiente acción" del relevo sin ejecutar. `Closes` solo con el criterio de aceptación completo; y qué hacer si te encuentras un issue cerrado con relevo vivo.

**La rama es preferencia, no ley** (hallazgo cloud). Algunos arneses imponen su espacio de nombres. Usa el suyo y declara la rama real en el relevo: el patrón existe para encontrar la rama, no para justificar no entregar.

**Propiedad declarativa, dicho en voz alta** (hallazgo cloud). Con una sola cuenta de plataforma, la asignación no prueba nada; la firma del commit es el único rastro. Se añade la firma por agente (`<nombre>@<proyecto>.local`) y se documenta el límite en vez de fingir garantía.

**Los checks se materializan** (hallazgo cloud). `.relay.yml` declaraba comprobaciones que no existían en ningún sitio: se cumplían por disciplina. Nuevo `relay-check.yml` que verifica lo automatizable (enlaza issue, evidencia no vacía, clase de datos, relevo o pendientes); avisa por defecto, endurecible a fallo. Lo que no se puede automatizar (que la evidencia sea cierta) sigue siendo humano.

**Además:** ampliar el alcance se declara y no se cuela; el par *Comprobado con / No comprobado* se señala como la pieza que sostiene el relevo (fue lo que más sirvió a la entrante); y `.relay.yml` separa el repo del método (público, sellado) del de conocimiento (privado).

## 0.1 · 2026-07-28

Génesis: issue como contrato, rama con una sola escritora, commit como checkpoint, PR como entrega, `HANDOFF` como relevo, y clases de datos (`repository`, `cloud-ok`, `local-only`, `synthetic-only`) para que el material protegido no salga del ordenador autorizado.
