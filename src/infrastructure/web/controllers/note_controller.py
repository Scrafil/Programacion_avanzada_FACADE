from flask import Blueprint, render_template, request, redirect, url_for

from src.application.facade.notes_facade import NotesFacade

note_bp = Blueprint("notes", __name__)

facade: NotesFacade | None = None  # inyectado desde app.py


def init_controller(f: NotesFacade):
    global facade
    facade = f


@note_bp.get("/")
def index():
    filtro = request.args.get("estudiante", "").strip()
    notas = facade.listar_notas()
    ficha = facade.ficha_estudiante(filtro) if filtro else None
    error = request.args.get("error", "")
    return render_template("index.html", notas=notas, ficha=ficha, filtro=filtro, error=error)


@note_bp.post("/crear")
def crear():
    try:
        facade.crear_nota(request.form.to_dict())
    except ValueError as e:
        return redirect(url_for("notes.index", error=str(e)))
    return redirect(url_for("notes.index"))


@note_bp.post("/eliminar/<int:nid>")
def eliminar(nid):
    facade.eliminar_nota(nid)
    return redirect(url_for("notes.index"))


@note_bp.post("/actualizar/<int:nid>")
def actualizar(nid):
    try:
        facade.actualizar_nota(nid, request.form.to_dict())
    except ValueError as e:
        return redirect(url_for("notes.index", error=str(e)))
    return redirect(url_for("notes.index"))
