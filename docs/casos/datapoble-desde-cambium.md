# Caso · datapoble, el primer equipo que llega desde Cambium con equipo montado

*Escrito por Talaia (coordinadora de datapoble) el 2026-08-01, al terminar la adopción de Relay
v0.5. Cuatro fases, sin trabajo en vuelo, `validate_config` en verde con 9 materiales.*

Este documento no viene a quejarse del método: viene a devolverle lo que el proyecto aprendió.
Cada propuesta lleva un número real detrás, porque una opinión sin caso no debería mover un
contrato que otros equipos usan.

## Qué somos

datapoble es un observatorio de datos territoriales (947 municipios de Cataluña, foco profundo en
los 31 del Berguedà), **repositorio público**, con una coordinadora y cinco frentes que son
subagentes con nombre. Veníamos de dos meses de Cambium Charter.

La adopción fue limpia y el `data_map` es la pieza que más nos aporta: nuestra regla 9 (el carril
de datos en silencio) dejó de ser una frase en un documento y pasó a ser una entrada con rutas que
un agente cloud puede leer antes de tocar nada.

## Lo que Relay ya resuelve y no hace falta tocar

Para que se lea con proporción: el `HANDOFF`, el issue como contrato, los estados y la separación
clase/derechos funcionan. El PR template ya pide **verificación ejecutada y declarada**, incluido
*«no comprobado y motivo»*, que es exactamente la disciplina correcta. Lo que sigue son cuatro
huecos concretos, no una enmienda a la totalidad.

---

## Propuesta 1 · Un campo para «qué tenía de falso el encargo»

**Es la más importante de las cuatro.**

En **una sola sesión** de trabajo, tres encargos escritos por mí —la coordinadora— llevaban una
premisa falsa. Las tres las cazó el agente que las ejecutaba. **Ninguna llegó a producción:**

| Lo que afirmé | Lo que era |
|---|---|
| «el ingestor ya trae el año» | la columna existía, el valor era NULL en **12 de 13** indicadores |
| «los recuentos sí se publican» | cierto en el almacén, **falso en lo que se sirve** |
| «una ponderada se dice *sobre N habitantes*» | falso en **2 de 9** métricas |

La tercera es la que mejor enseña el mecanismo. Si el agente me hubiera obedecido al pie de la
letra, la ficha habría escrito **«sobre 3.915.127 habitantes»** debajo de un porcentaje de
*viviendas*: una procedencia falsa, bien maquetada, que es justo lo que la regla de procedencia
existe para impedir.

Y funciona en las dos direcciones: un agente encontró que **una casilla de estado de nuestra propia
documentación decía «✅ hecho» de algo que nadie había hecho**. Estuvo así doce días.

**El hueco:** el PR template pide «Qué cambia» y «Conocimiento reusable», pero **nada invita al
ejecutor a contradecir a quien le asignó**. Y contradecir hacia arriba tiene un coste social que un
formulario elimina: si hay una casilla, corregir a tu coordinadora deja de ser un acto de valentía
y pasa a ser rellenar un campo.

**Propuesta:** un campo obligatorio en el PR template, con el vacío como respuesta legítima.

```markdown
## El encargo, contrastado

- [ ] El encargo era correcto en todo lo que pude comprobar.
- [ ] Encontré esto de falso o impreciso (y qué hice con ello):
```

En nuestros `role.md` esto ya es una obligación escrita de cada frente —*«digues quines premisses
del brief has trobat falses»*— y es, sin discusión, la práctica que más errores nos ha evitado.
Creemos que pertenece al método, no a un proyecto.

---

## Propuesta 2 · Un derecho que falta: `no-publicar`

Los cuatro derechos actuales (`libre`, `solo-agregado`, `no-reproducir`, `no-sale`) **mezclan dos
ejes**: qué puedo hacer con *el fichero* y qué puede publicar *el producto*.

**El caso:** nuestra capa electoral. El parquet **está versionado en un repositorio público** —así
que `no-sale` («ni se copia, ni se imprime, ni se deriva») es factualmente falso: ya salió—, pero
la dirección decidió que **no se sirve ni se deriva** en el producto: fuera del chat, fuera del
web, fuera del allow-list de SQL.

Ninguno de los cuatro derechos dice eso. Puse `no-sale` porque describe bien *la decisión*, y lo
dejé anotado como tensión en el propio `data_map`.

**Propuesta:** añadir

```yaml
no-publicar: "Se puede leer y procesar; no sale al producto"
```

Es distinto de `no-sale` (el material no sale de ningún sitio) y de `solo-agregado` (sale, pero
agregado). Y cubre un caso que sospechamos común: **material legítimamente versionado que una
decisión editorial mantiene fuera de lo que se publica.**

---

## Propuesta 3 · La membrana se cruza por efecto lateral, no solo por intención

La lista de escalados nombra **actos**: publicar, desplegar, enviar, gastar. Pero lo que nos pasó
fue otra cosa.

**El caso:** un agente, haciendo una tarea de tablero, encontró que un almacén de datos electorales
estaba desactualizado. Reconstruirlo era **mecánicamente parte de su trabajo** («mantener los
almacenes al día») y habría **publicado datos electorales de 947 municipios como efecto lateral**
de una tarea rutinaria. Se paró y lo escaló. Hizo bien.

Lo que le hizo pararse no fue la lista —su tarea no era «publicar»— sino reconocer que **la
consecuencia sí cruzaba la membrana**.

**Propuesta:** una línea en la lista de escalados y en `AGENTS.relay.md`:

> La membrana se cruza también **por consecuencia**: una tarea cuyo propósito es rutinario puede
> cruzarla por efecto lateral. Antes de integrar, pregúntate no solo *qué estoy haciendo* sino
> *qué queda publicado, desplegado o gastado cuando esto entre*.

Esto es también lo que nos consuela de haber perdido las jurisdicciones rígidas de Cambium. La
valla nos paró cosas reales; lo que la sustituye no puede ser solo la buena voluntad.

---

## Propuesta 4 · La ejecución de la propia adopción no escala

Las fases 1, 2 y 4 de la adopción **tocan las comprobaciones y las reglas duras** — dos entradas de
la lista de escalados que esa misma adopción instala. Lo hice porque la adopción *es* la orden de
la dirección, pero un equipo más literal que yo se queda bloqueado en la fase 1 pidiendo permiso
para instalar el permiso.

**Propuesta:** decirlo explícitamente en el documento de adopción:

> Instalar Relay toca checks y reglas por definición. **La ejecución de la adopción no escala**: ya
> viene autorizada por quien la encarga. Lo que sí escala es cualquier decisión de contenido que
> surja al hacerla — y muy en particular **la transcripción de las reglas duras**, que debería
> revisar quien las escribió.

Este último matiz nos importa: yo transcribí las reglas de mi propia dirección, incluidas las de
seguridad, **sin que nadie las revisara**. Salieron bien, pero el método no debería depender de eso.

---

## Un quinto, más pequeño, por si sirve

**Una guarda que no has visto caer no es una guarda.** En este proyecto el patrón «existe un
verificador y no lo ejecuta nadie» ha mordido **cinco veces**, una de ellas ocultando que dos
almacenes servían **números distintos para la misma métrica del mismo municipio** en 917 de 947
casos.

Desde que probamos cada guarda **en negativo** (inyectar el fallo y verla caer con el mensaje
correcto), una guarda cazó un error del propio agente **mientras la escribía**.

No pedimos que Relay lo imponga. Solo que el PR template, cuando el PR *añade* una comprobación,
pregunte: **¿la has visto caer?**

---

## Lo que nos llevamos de Cambium y no perdimos

Por si otro equipo hace el mismo viaje: las reglas de producto y seguridad se promovieron enteras,
con su numeración y su idioma. Los `role.md` se quedaron donde estaban. Y lo mejor que teníamos
—que cada frente esté obligado a decir qué encontró falso en su encargo— **no estaba en Cambium
tampoco**: estaba en nuestros `role.md`. Por eso la Propuesta 1 no es «devolvednos algo», sino
«esto deberíais tenerlo vosotros».

*Talaia · datapoble*
