from src.domain.model.note import Note


class NoteService:
    def __init__(self, repo):
        self.repo = repo

    def create_note(self, estudiante, materia, nota, fecha):
        n = Note(None, estudiante, materia, float(nota), fecha)
        n.validate()
        return self.repo.create(n)

    def list_notes(self):
        return self.repo.find_all()

    def get_note(self, nid):
        return self.repo.find_by_id(nid)

    def update_note(self, nid, estudiante=None, materia=None, nota=None, fecha=None, **kwargs):
        # Acepta dict de form (strings) o kwargs nombrados
        data = dict(kwargs)
        if estudiante is not None:
            data["estudiante"] = estudiante
        if materia is not None:
            data["materia"] = materia
        if nota is not None:
            data["nota"] = nota
        if fecha is not None:
            data["fecha"] = fecha
        current = self.repo.find_by_id(nid)
        if current is None:
            raise ValueError(f"nota {nid} no existe")
        merged = Note(
            id=nid,
            estudiante=data.get("estudiante", current.estudiante),
            materia=data.get("materia", current.materia),
            nota=float(data.get("nota", current.nota)),
            fecha=data.get("fecha", current.fecha),
        )
        merged.validate()
        return self.repo.update(merged)

    def delete_note(self, nid):
        return self.repo.delete(nid)

    def average_by_student(self, estudiante):
        notes = [x for x in self.repo.find_all() if x.estudiante == estudiante]
        if not notes:
            return 0.0
        return round(sum(x.nota for x in notes) / len(notes), 2)
