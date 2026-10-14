# Parcial-Segundo-Corte-Ingenieria-de-Software

# La Última Transmisión - Motor de Ficción Interactiva

**Integrantes:**
* [NOMBRE COMPLETO DEL INTEGRANTE 1]
* [NOMBRE COMPLETO DEL INTEGRANTE 2]

## Descripción
Motor de historias interactivas por consola basado en consola. Permite cargar relatos estructurados en JSON, tomar decisiones basadas en condiciones lógicas booleanas, aplicar efectos al estado de la partida y alcanzar múltiples finales.

## Requisitos y Tecnología
*   **Lenguaje:** Python 3.8 o superior.
*   **Dependencias:** Ninguna (solo bibliotecas estándar `json`, `sys`, `unittest`).

## Instalación y Ejecución
1. Descomprimir el archivo ZIP en una carpeta local.
2. Abrir una terminal en dicha carpeta.
3. Para ejecutar la historia principal:
   `python cli.py la_ultima_transmision.json`
4. Para cargar la segunda historia:
   `python cli.py segunda_historia.json`

## Pruebas Automatizadas
Para ejecutar la suite de pruebas unitarias y de integración (U1-U5, I1):
`python -m unittest test_motor.py -v`

## Formato del Archivo de Historia (JSON)
El motor lee objetos JSON con la siguiente estructura:
* `titulo` (String).
* `inicio` (String): ID de la escena inicial.
* `variables` (Objeto): Mapa `{"nombre_variable": booleano}`.
* `escenas` (Lista de objetos):
  * `id` (String): Identificador único.
  * `texto` (String): Narrativa mostrada al jugador.
  * `final` (Booleano): `true` si es el final, `false` en caso contrario.
  * `opciones` (Lista de objetos): Vacía si `final` es true.
    * `id` (String).
    * `texto` (String).
    * `destino` (String): ID de la escena a la que dirige.
    * `condiciones` (Objeto): Mapa de variables que deben coincidir (ej. `{"conoce_origen": true}`). Si está vacío `{}`, la opción siempre está disponible.
    * `efectos` (Objeto): Mapa de variables a modificar (ej. `{"confia_en_la_voz": false}`). Si está vacío `{}`, el estado no cambia.

## Recorridos de la Historia Principal (La última transmisión)
*   **Final 1 (Rescate - E4):** Elegir `Revisar señal` -> `Investigar archivo` -> `Activar con código`.
*   **Final 2 (El eco - E5):** Elegir `Revisar señal` -> `Continuar sin investigar` -> `Activar sin verificar`.
*   **Final 3 (Silencio - E6):** Elegir `Revisar señal` -> `Investigar archivo` (o Continuar) -> `Cortar comunicación`.

## Manejo de Errores
Para provocar un error de contenido intencional: edita `segunda_historia.json`, cambia un destino de una opción a `"destino_falso"`. Ejecuta el programa y observarás el mensaje: `Error de validación del contenido: Destino inexistente 'destino_falso' en opción...`.

## Limitaciones Conocidas
* No existe funcionalidad de retroceso por decisión de diseño consensuada provisionalmente.
* Interfaz puramente de texto (CLI).

## Declaración de Herramientas (IA)
* Se utilizó un asistente de lenguaje (LLM) como apoyo para formatear los diagramas en sintaxis Mermaid y para validar la redacción de los requisitos no funcionales, bajo estricta revisión de los autores. Todo el código Python fue diseñado lógicamente por el equipo.

**Estado del Cambio (Hora 6):** PENDIENTE DE RECIBIR DOCUMENTO OFICIAL.