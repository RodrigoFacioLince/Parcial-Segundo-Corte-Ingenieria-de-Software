import json

class ValidadorHistoria:
    @staticmethod
    def validar(datos):
        if not isinstance(datos, dict): return False, "Estructura principal no es un objeto JSON."
        campos_req = ["titulo", "inicio", "variables", "escenas"]
        for c in campos_req:
            if c not in datos: return False, f"Falta el campo obligatorio '{c}'."
        
        variables_declaradas = set(datos["variables"].keys())
        ids_escenas = set()
        
        for escena in datos["escenas"]:
            eid = escena.get("id")
            if not eid: return False, "Escena sin ID."
            if eid in ids_escenas: return False, f"ID de escena duplicado: {eid}."
            ids_escenas.add(eid)
            
            es_final = escena.get("final", False)
            opciones = escena.get("opciones", [])
            
            if es_final and len(opciones) > 0:
                return False, f"Escena final '{eid}' no debe tener opciones."
            if not es_final and len(opciones) == 0:
                return False, f"Escena no final '{eid}' debe tener al menos una opción."
                
            ids_opciones = set()
            for op in opciones:
                oid = op.get("id")
                if oid in ids_opciones: return False, f"Opción duplicada '{oid}' en escena '{eid}'."
                ids_opciones.add(oid)
                
                if op.get("destino") not in [e["id"] for e in datos["escenas"]]:
                    return False, f"Destino inexistente '{op.get('destino')}' en opción '{oid}'."
                for cond in op.get("condiciones", {}).keys():
                    if cond not in variables_declaradas: return False, f"Variable no declarada '{cond}' en condiciones."
                for ef in op.get("efectos", {}).keys():
                    if ef not in variables_declaradas: return False, f"Variable no declarada '{ef}' en efectos."

        if datos["inicio"] not in ids_escenas: return False, f"Escena inicial '{datos['inicio']}' inexistente."
        return True, "OK"

class Partida:
    def __init__(self, datos):
        self.datos = datos
        self.reiniciar()
        
    def reiniciar(self):
        self.estado_variables = self.datos["variables"].copy()
        self.escena_actual_id = self.datos["inicio"]
        self.historial = None  
        
    def obtener_escena(self, id_escena):
        for e in self.datos["escenas"]:
            if e["id"] == id_escena: return e
        return None

    def opciones_habilitadas(self):
        escena = self.obtener_escena(self.escena_actual_id)
        if escena["final"]: return []
        
        habilitadas = []
        for op in escena["opciones"]:
            cumple = all(self.estado_variables.get(k) == v for k, v in op.get("condiciones", {}).items())
            if cumple: habilitadas.append(op)
        return habilitadas

    def procesar_eleccion(self, id_opcion):
        habilitadas = self.opciones_habilitadas()
        opcion = next((o for o in habilitadas if o["id"] == id_opcion), None)
        
        if not opcion: return False, "Opción no válida o no habilitada."
        
        self.historial = (
            self.escena_actual_id,
            self.estado_variables.copy()
        )
        
        for k, v in opcion.get("efectos", {}).items():
            self.estado_variables[k] = v
            
        self.escena_actual_id = opcion["destino"]
        return True, "Transición exitosa."

    def deshacer(self):
        if not self.historial:
            return False, "No hay acciones para deshacer o ya se usó el retroceso."
        
        self.escena_actual_id, self.estado_variables = self.historial
        self.historial = None
        return True, "Se ha deshecho la última decisión con éxito."