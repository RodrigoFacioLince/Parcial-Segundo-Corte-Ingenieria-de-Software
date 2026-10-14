import unittest
from motor import ValidadorHistoria, Partida
import json

class TestMotorHistorias(unittest.TestCase):
    
    def setUp(self):
        # Datos mock mínimos para pruebas unitarias U1 a U5
        self.datos_mock = {
            "titulo": "Test", "inicio": "e1",
            "variables": {"varA": False, "varB": True},
            "escenas": [
                {
                    "id": "e1", "texto": "Escena 1", "final": False,
                    "opciones": [
                        {"id": "op1", "texto": "Ir E2", "destino": "e2", "condiciones": {}, "efectos": {"varA": True}},
                        {"id": "op_bloqueada", "texto": "Bloqueada", "destino": "e2", "condiciones": {"varA": True}, "efectos": {}}
                    ]
                },
                {
                    "id": "e2", "texto": "Escena 2", "final": True, "opciones": []
                }
            ]
        }
        self.partida = Partida(self.datos_mock)

    def test_U1_condiciones_habilitan_opciones(self):
        """U1: Las condiciones cumplidas y no cumplidas habilitan únicamente las opciones correspondientes."""
        ops = self.partida.opciones_habilitadas()
        self.assertEqual(len(ops), 1)
        self.assertEqual(ops[0]["id"], "op1")

    def test_U2_eleccion_valida_aplica_efectos(self):
        """U2: Una elección válida aplica los efectos y avanza al destino correcto."""
        exito, _ = self.partida.procesar_eleccion("op1")
        self.assertTrue(exito)
        self.assertEqual(self.partida.escena_actual_id, "e2")
        self.assertTrue(self.partida.estado_variables["varA"])

    def test_U3_opcion_invalida_no_modifica_estado(self):
        """U3: Una opción inexistente o no habilitada deja intacto el estado."""
        estado_previo = self.partida.estado_variables.copy()
        exito, _ = self.partida.procesar_eleccion("op_bloqueada")
        self.assertFalse(exito)
        self.assertEqual(self.partida.escena_actual_id, "e1")
        self.assertEqual(self.partida.estado_variables, estado_previo)

    def test_U4_errores_de_contenido_obligatorios(self):
        """U4: Los errores de contenido producen diagnóstico controlado."""
        # Clonar e inyectar un destino inexistente
        datos_malos = json.loads(json.dumps(self.datos_mock))
        datos_malos["escenas"][0]["opciones"][0]["destino"] = "e_falsa"
        valido, msg = ValidadorHistoria.validar(datos_malos)
        self.assertFalse(valido)
        self.assertIn("Destino inexistente", msg)

        # Inyectar opción en escena final
        datos_malos_2 = json.loads(json.dumps(self.datos_mock))
        datos_malos_2["escenas"][1]["opciones"] = [{"id": "x", "destino": "e1"}]
        valido2, msg2 = ValidadorHistoria.validar(datos_malos_2)
        self.assertFalse(valido2)
        self.assertIn("no debe tener opciones", msg2)

    def test_U5_reiniciar_restaura_estado(self):
        """U5: Reiniciar restaura la escena y las variables iniciales."""
        self.partida.procesar_eleccion("op1")
        self.assertEqual(self.partida.escena_actual_id, "e2")
        self.partida.reiniciar()
        self.assertEqual(self.partida.escena_actual_id, "e1")
        self.assertFalse(self.partida.estado_variables["varA"])

    def test_I1_integracion_segunda_historia(self):
        """I1: Carga y decisiones con un archivo de historia real (segunda_historia.json)"""
        with open("segunda_historia.json", "r", encoding="utf-8") as f:
            datos_reales = json.load(f)
        
        partida = Partida(datos_reales)
        # Comprobar estado inicial
        self.assertEqual(partida.escena_actual_id, "celda")
        # Transitar sin robar tarjeta
        partida.procesar_eleccion("ir_pasillo")
        self.assertEqual(partida.escena_actual_id, "pasillo")
        # La opción de abrir compuerta debe estar bloqueada por falta de tarjeta
        ops = partida.opciones_habilitadas()
        self.assertEqual(len(ops), 1)
        self.assertEqual(ops[0]["id"], "forzar_compuerta")
        # Forzar compuerta y llegar a final malo
        partida.procesar_eleccion("forzar_compuerta")
        self.assertEqual(partida.escena_actual_id, "capturado")
        self.assertTrue(partida.obtener_escena("capturado")["final"])

if __name__ == "__main__":
    unittest.main()