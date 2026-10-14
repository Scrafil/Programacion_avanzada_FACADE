"""Facade: unico punto de entrada para la capa web.

Oculta Service + validaciones + estadisticas.
No depende de web ni de BD. Solo habla con el service.
"""


class NotesFacade:
    def __init__(self, service):
        self._s = service

    # --- CRUD simplificado (data viene del form como dict) ---
    def crear_nota(self, data: dict):
        return self._s.create_note(
            data["estudiante"], data["materia"], data["nota"], data["fecha"]
        )

    def listar_notas(self):
        return self._s.list_notes()

    def obtener_nota(self, nid):
        return self._s.get_note(nid)

    def actualizar_nota(self, nid, data: dict):
        return self._s.update_note(nid, **data)

    def eliminar_nota(self, nid):
        return self._s.delete_note(nid)

    # --- Operacion compuesta (valor del Facade) ---
    def ficha_estudiante(self, estudiante: str) -> dict:
        notas = [n for n in self._s.list_notes() if n.estudiante == estudiante]
        return {
            "estudiante": estudiante,
            "total": len(notas),
            "promedio": self._s.average_by_student(estudiante),
            "notas": notas,
        }
