import sys
import json
from motor import ValidadorHistoria, Partida

def cargar_json(ruta):
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        return None

def iniciar_juego(ruta_archivo):
    datos = cargar_json(ruta_archivo)
    if not datos:
        print("Error: No se pudo leer el archivo JSON.")
        return

    valido, mensaje = ValidadorHistoria.validar(datos)
    if not valido:
        print(f"Error de validación del contenido: {mensaje}")
        return

    partida = Partida(datos)
    print(f"--- Iniciando: {datos['titulo']} ---")

    while True:
        escena = partida.obtener_escena(partida.escena_actual_id)
        print(f"\n[{escena['id']}]")
        print(escena['texto'])

        if escena['final']:
            print("\n*** FIN DE LA HISTORIA ***")
            print("Opciones: [u] Deshacer última decisión | [r] Reiniciar partida | [salir] Terminar")
            resp = input("Elige una opción: ").strip().lower()
            if resp == 'u':
                exito, msg = partida.deshacer()
                print(f"\n>>> {msg} <<<")
                continue
            elif resp == 'r':
                partida.reiniciar()
                continue
            else:
                break

        opciones_hab = partida.opciones_habilitadas()
        
        if not opciones_hab:
            print("\n*** BLOQUEO: No hay opciones habilitadas en este punto ***")
            print("Opciones: [u] Deshacer última decisión | [r] Reiniciar partida")
            resp = input("Elige una opción: ").strip().lower()
            if resp == 'u':
                exito, msg = partida.deshacer()
                print(f"\n>>> {msg} <<<")
                continue
            elif resp == 'r':
                partida.reiniciar()
                continue
            else:
                break

        print("\nOpciones disponibles:")
        for idx, op in enumerate(opciones_hab):
            print(f"  {idx + 1}. {op['texto']} ({op['id']})")
        
        print("\nComandos adicionales: [u] Deshacer última decisión | [r] Reiniciar | [salir] Terminar")
        seleccion = input("\nElige el ID de la opción o comando: ").strip()
        
        if seleccion.lower() == 'salir':
            break
        elif seleccion.lower() == 'u':
            exito, msg = partida.deshacer()
            print(f"\n>>> {msg} <<<")
            continue
        elif seleccion.lower() == 'r':
            partida.reiniciar()
            print("\n>>> Partida reiniciada <<<")
            continue

        exito, msg = partida.procesar_eleccion(seleccion)
        if not exito:
            print(f"\n>>> {msg} Intenta de nuevo. <<<")

if __name__ == "__main__":
    archivo = sys.argv[1] if len(sys.argv) > 1 else "segunda_historia.json"
    iniciar_juego(archivo)