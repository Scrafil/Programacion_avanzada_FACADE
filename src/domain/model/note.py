from dataclasses import dataclass


@dataclass
class Note:
    id: int | None
    estudiante: str
    materia: str
    nota: float
    fecha: str  # YYYY-MM-DD

    def validate(self):
        if not self.estudiante.strip():
            raise ValueError("estudiante requerido")
        if not self.materia.strip():
            raise ValueError("materia requerida")
        if not (0.0 <= self.nota <= 5.0):
            raise ValueError("nota debe estar entre 0.0 y 5.0")
