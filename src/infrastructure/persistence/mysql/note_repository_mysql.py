from src.application.ports.note_repository import NoteRepository
from src.domain.model.note import Note
from src.config.mysql_connection import get_connection


def _row_to_note(row) -> Note:
    # row: (id, estudiante, materia, nota, fecha)
    nid, estudiante, materia, nota, fecha = row
    fecha_str = fecha.isoformat() if hasattr(fecha, "isoformat") else str(fecha)
    return Note(id=nid, estudiante=estudiante, materia=materia, nota=float(nota), fecha=fecha_str)


class NoteRepositoryMySQL(NoteRepository):
    def create(self, note: Note) -> int:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO notes(estudiante, materia, nota, fecha) VALUES(%s, %s, %s, %s)",
            (note.estudiante, note.materia, note.nota, note.fecha),
        )
        conn.commit()
        nid = cur.lastrowid
        cur.close()
        conn.close()
        return nid

    def find_all(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, estudiante, materia, nota, fecha FROM notes ORDER BY id")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [_row_to_note(r) for r in rows]

    def find_by_id(self, note_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, estudiante, materia, nota, fecha FROM notes WHERE id=%s", (note_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return _row_to_note(row) if row else None

    def update(self, note: Note):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE notes SET estudiante=%s, materia=%s, nota=%s, fecha=%s WHERE id=%s",
            (note.estudiante, note.materia, note.nota, note.fecha, note.id),
        )
        conn.commit()
        affected = cur.rowcount
        cur.close()
        conn.close()
        return affected

    def delete(self, note_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM notes WHERE id=%s", (note_id,))
        conn.commit()
        affected = cur.rowcount
        cur.close()
        conn.close()
        return affected
