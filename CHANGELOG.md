# Changelog · Mycelia Relay

## 0.6.1 · 2026-08-02

**La guarda de versión era nuestra y el rojo iba a ser suyo.** La comprobación que 0.5 añadió —que `.relay.yml` y el CHANGELOG digan la misma versión— no miraba **de quién** era el CHANGELOG. En cualquier repositorio anfitrión con su propio `CHANGELOG.md` en la raíz, que son casi todos, comparaba la versión de Relay contra la del proyecto y fallaba: `version del fichero (0.6) distinta de la ultima del CHANGELOG (2.3.1)`. Un rojo por algo que no es un fallo, en el primer comando que ejecuta un equipo al adoptar. Ahora solo se dispara si el CHANGELOG es de Relay.

Los dos equipos que han adoptado hasta hoy vieron verde por casualidad: ninguno tenía `CHANGELOG.md` en la raíz.

Encontrado **escribiendo las instrucciones de migración a 0.6 para otro equipo**, no ejecutando nada. La lección va con la enmienda 5 de datapoble y la completa: una guarda se prueba en negativo, y además **se prueba en el sitio donde va a correr**. Las trece guardas del validador se probaban contra configuraciones sueltas en un directorio temporal — es decir, contra el repositorio de Relay, nunca contra un anfitrión. Caso nuevo en la suite: un `CHANGELOG.md` de proyecto no dispara la guarda.

## 0.6 · 2026-08-02

Cinco enmiendas de **datapoble** (observatorio de datos territoriales, 947 municipios), el primer equipo que llega **desde otro marco y con equipo ya montado** — dos meses de Cambium Charter, una coordinadora y cinco frentes. Su carta y el caso entero están en [`docs/casos/datapoble-desde-cambium.md`](docs/casos/datapoble-desde-cambium.md). Van con tres ajustes de la custodia, todos sacados de su propia evidencia.

**El encargo se contrasta, y la corrección se registra.** En una sola sesión, tres encargos escritos por la coordinadora llevaban una premisa falsa; las tres las cazó el agente que las ejecutaba y ninguna llegó a producción. La tercera enseña el mecanismo: obedecer al pie de la letra habría escrito «sobre 3.915.127 habitantes» bajo un porcentaje de *viviendas* — una procedencia falsa, bien maquetada. Y funciona al revés: una casilla de estado que decía «hecho» de algo que nadie hizo estuvo doce días.

El contrato ya tenía **media** regla: el paso 3 mandaba verificar el *estado de partida* contra el repositorio. Los tres casos no son estado de partida, son premisas sobre cómo funciona el sistema, así que la regla se generaliza en vez de añadirse: se contrasta **qué está hecho** y **cómo funciona el sistema**, y lo que difiera corrige el issue antes de trabajar. El campo nuevo del PR es el registro de esa corrección, porque contradecir hacia arriba tiene un coste social que un formulario elimina.

*Ajuste de la custodia:* la casilla propuesta —«el encargo era correcto en todo lo que pude comprobar»— se puede marcar sin haber comprobado nada, y eso fabrica una garantía falsa: exactamente la peor cicatriz de Relay (`data_map` vacío dando verde). Ahora afirma **lo que hiciste**, no lo que salió, y hay una tercera opción para declarar que no pudiste contrastarlo, igual que en «no comprobado y motivo».

**Derecho nuevo: `no-publicar`.** Material legítimamente versionado que una decisión editorial mantiene fuera del producto. El caso: una capa electoral que **está en un repositorio público** —así que `no-sale` es factualmente falso, ya salió— y que la dirección decidió no servir ni derivar. Ninguno de los cuatro derechos lo decía, y la señal de que el vocabulario estaba corto es la de siempre: **hubo que escribir un valor falso y anotarlo como tensión**, el mismo síntoma que trajo el cambio de 0.5 desde otro equipo.

Se distingue de `no-reproducir`, que se le parece: aquél es **autoría** (no copias el contenido a ningún sitio, y no cambia nunca), éste es **decisión editorial** (procésalo con libertad, no llega al producto, y puede revertirlo quien la tomó). Y solo es exigible si el producto está identificado: quien lo use dice en su `REGLAS.md` dónde acaba —web, API, chat, allow-list de consultas—, porque un derecho que no nombra su frontera no se puede cumplir ni comprobar.

*Tensión conocida, declarada y no resuelta:* datapoble diagnostica que los derechos mezclan **dos ejes** —qué puedo hacer con el fichero y qué puede publicar el producto— y el diagnóstico es correcto y más grande que el parche. La respuesta limpia sería un tercer eje. No se hace: pesa en cada material de cada proyecto para servir un caso que aún no existe. **Disparador para reabrirlo: el día que un material necesite dos derechos a la vez.**

**La membrana se cruza también por consecuencia.** La lista de escalados nombra actos —publicar, desplegar, enviar, gastar—, todos verbos de intención. Lo que pasó fue otra cosa: un agente en una tarea de tablero encontró un almacén electoral desactualizado; reconstruirlo era mecánicamente parte de su trabajo y **habría publicado datos electorales de 947 municipios como efecto lateral**. Se paró y lo escaló. No le paró la lista: le paró reconocer la consecuencia.

Esto le importa a Relay más de lo que la propuesta reclama. Las jurisdicciones rígidas de Cambium cazaban efectos laterales **por estructura** —no podías tocar lo que no era tuyo—; Relay las quitó por ligereza y no puso nada en su lugar para esa clase de captura. Ahora la pregunta es *qué queda publicado, desplegado o gastado cuando esto entre*, no solo qué dice la tarea que hace.

*Ajuste de la custodia:* llegó como comentario en `.relay.yml` y redactada como «antes de integrar». Pero su propio caso muestra al agente parándose **con el trabajo a medias**, y un comentario de configuración se lee una vez, el día de la instalación. Sube al contrato, a *Durante el trabajo* y a la lista de escalados; en `.relay.yml` queda un puntero.

**La ejecución de la propia adopción no escala.** Instalar Relay toca checks y reglas duras —dos entradas de la lista que esa misma instalación trae—, así que un equipo literal se bloquea pidiendo permiso para instalar el permiso. Queda dicho: la adopción viene autorizada por quien la encarga. Con el matiz que aporta el caso y que es la parte que importa: **la transcripción de las reglas duras sí escala**, y va en su propio PR, porque en datapoble la coordinadora transcribió las reglas de seguridad de su propia dirección sin que nadie las revisara. Salieron bien; el método no debería depender de eso.

**Una guarda que no has visto caer no es una guarda.** Llega presentada como «un quinto, más pequeño, por si sirve», y en la historia de Relay es la regla que habría cazado nuestro peor defecto. A datapoble el patrón «existe un verificador y no lo ejecuta nadie» les mordió **cinco veces**, una ocultando que dos almacenes servían números distintos para la misma métrica del mismo municipio en 917 de 947 casos.

Entra en el PR template (si el PR añade una comprobación, ¿la has visto caer?), entra en el contrato, y **Relay se la aplica a sí mismo**: `scripts/test_validate_config.py` inyecta cada fallo y comprueba que el validador cae *por el motivo correcto*, con un caso que fija `no-publicar` como regresión y otro que exige que la plantilla de este repositorio siga en rojo. Corre en CI. Hasta hoy no teníamos ninguna prueba de que nuestra guarda cayera: el fallo de 0.5 se encontró **leyendo el código**, no porque el validador fallara.

**Y tres defectos propios que la carta destapó sin buscarlos**, todos de la misma familia — el cambio llega a la doctrina y no al artefacto que los equipos copian:

- `AGENTS.relay.md` seguía pidiendo «impacto sobre Mycelia» en el cierre: 0.5 limpió las plantillas y se dejó el contrato. **Tercera vez** con este mismo fallo.
- `docs/adopcion-ejemplo.md` era **anterior a 0.4** entero: se titulaba «Adopción de Mycelia y Mycelia Relay» y su «configuración recomendada» era el bloque `mycelia:` que borramos en 0.4.1. Un equipo que adoptara leyéndolo escribía una configuración que el validador no conoce. Reescrito como [`docs/adopcion.md`](docs/adopcion.md). **Cuarta vez.**
- **La plantilla de issue podía ocultar un derecho**, y `no-publicar` lo habría empeorado. Pedía «la clase más restrictiva… sus derechos van con ella», pero la clase más restrictiva **no arrastra** los derechos más restrictivos: una tarea que toque `local-only` + `libre` y `repository` + `no-publicar` declara `local-only`, y `no-publicar` no aparecería en ninguna parte del contrato que la agente lee. Ahora se declara material a material.

Y uno menor: la lista de instalación **nunca incluyó `scripts/validate_config.py`**, y dos párrafos después el README te decía que lo ejecutaras. Dos equipos lo copiaron igual, por sentido común. Que funcionara por sentido común no lo hacía correcto.

## 0.5 · 2026-07-31

Cuatro cambios de la **segunda auditoría de Clara**, hecha ya con 0.4.1 instalado y funcionando. El primero es el más grave que ha tenido Relay.

**`data_map` vacío ya no valida.** `validate_config` comprobaba que existieran las claves `data_classes` y `data_rights`, que son **el vocabulario que la propia plantilla trae de fábrica**: validaba que no hubieras roto el fichero, disfrazado de que habías declarado tus reglas. Un equipo podía instalar Relay, ver «Configuración Relay válida» y dejar entrar a una agente cloud sin una sola regla escrita. Como dice Clara, es la lección del piloto con otra cara: el andamiaje que llega tarde no sirve, y **el que llega vacío tampoco, pero además parece que sí**. Ahora el validador lee el YAML de verdad, falla con el mapa vacío, exige clase, derechos y rutas por material, rechaza valores fuera del vocabulario, avisa de rutas que no existen, y si no puede verificar (falta PyYAML) **falla en vez de fingir**: un «no sé» no es un verde.

**Los derechos viajan con el dato, no con la clase.** Eran un eje solo: `motivo` calificaba una clase restrictiva. Pero el material de sinopsis de convoca es `repository` legítimamente **y** obra ajena: se puede leer y no reproducir, y el esquema no tenía sitio para decirlo (Clara lo coló poniendo motivo en una clase sin restricción, que es la señal de que el modelo estaba mal). Ahora son dos ejes independientes: `data_classes` dice **dónde** puede estar, `data_rights` dice **qué se puede hacer** (`libre`, `solo-agregado`, `no-reproducir`, `no-sale`), y valen aunque la clase no restrinja.

**`data_map` apunta a ficheros reales.** Cada material declara sus `rutas`. Una etiqueta como «corpus-de-terceros» no le dice a una agente cloud qué fichero es; el validador lo exige y avisa si la ruta no existe.

**Las plantillas dejan de nombrar el grafo.** 0.4.1 hizo Mycelia opcional en la configuración y el contrato, pero la plantilla de issue seguía pidiendo «Notas Mycelia» y la de PR, «Impacto sobre Mycelia». Segunda vez que el cambio llega a la doctrina y no a los artefactos que los equipos copian: la lección propia es mirar siempre lo que se copia, no lo que se lee.

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
