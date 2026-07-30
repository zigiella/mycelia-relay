# Changelog · Mycelia Relay

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
