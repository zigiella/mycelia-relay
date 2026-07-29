# Contrato Mycelia Relay

Estas reglas complementan el `AGENTS.md` del proyecto. Ante conflicto, mandan las reglas específicas del proyecto y las decisiones explícitas de la dirección.

## Antes de trabajar

1. Abre el issue asignado.
2. Comprueba objetivo, criterio de aceptación, alcance, entorno y política de datos.
3. Confirma que no existe otra escritora activa sobre la misma tarea o rama.
4. Crea o recupera `agent/<issue>-<tema>`.
5. Lee únicamente las notas de Mycelia enlazadas desde el issue.

Una instrucción recibida por chat que no esté reflejada en el issue todavía no cambia el contrato durable.

## Durante el trabajo

- Mantén una sola tarea activa por agente salvo partición expresa.
- Haz cambios pequeños, reversibles y comprobables.
- No toques rutas fuera del alcance sin ampliar el issue o dejar un handoff.
- Publica checkpoints cuando el trabajo pueda perderse o continuar en otro entorno.
- No escribas secretos, credenciales, rutas locales ni datos `local-only`.
- Declara las comprobaciones reales. Un check no ejecutado se marca como no ejecutado.

## Agente local

Antes de cerrar la aplicación o apagar el ordenador:

1. guarda cambios coherentes;
2. ejecuta las comprobaciones posibles;
3. crea commit de checkpoint;
4. haz push de la rama;
5. deja el bloque `HANDOFF` en el issue o PR;
6. cambia el estado a `paused-local` si la tarea no terminó.

Si existen cambios locales sin push, la tarea no es recuperable por el equipo.

## Agente cloud

- No asumas acceso a archivos locales, aplicaciones autenticadas o dispositivos.
- No solicites que se suban datos `local-only` para desbloquearte.
- Si la tarea depende de material local, deja el bloqueo y propone una partición segura.
- Publica commits y PR aunque la sesión cloud prometa conservar memoria.

## Propiedad y relevo

Una tarea tiene una sola escritora activa. El relevo exige:

- checkpoint publicado;
- bloque `HANDOFF`;
- cambio visible de propietaria;
- confirmación de la nueva agente antes de escribir.

La nueva agente continúa en la misma rama cuando el trabajo es lineal. Abre otra rama cuando vaya a competir con una solución anterior.

## Handoff

```text
HANDOFF
Estado: working-local | working-cloud | paused-local | blocked | review
Agente saliente: <nombre y arnés>
Entorno: local | cloud
Rama: <rama>
Último commit: <sha>
Hecho: <resultado verificable>
Comprobado con: <comandos, tests o revisión>
No comprobado: <qué y por qué>
Pendiente: <trabajo concreto>
Datos necesarios: repository | cloud-ok | local-only | synthetic-only
Siguiente acción: <acción ejecutable>
Siguiente propietaria: <agente o sin asignar>
```

## Cierre

El PR incluye alcance, evidencia, limitaciones, impacto sobre Mycelia y pendientes. La tarea termina al integrarse el PR o al cerrarse explícitamente el issue, no cuando una agente dice que ha acabado.
