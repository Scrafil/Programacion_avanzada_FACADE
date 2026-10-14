from flask import Flask

from src.config.mysql_connection import init_db
from src.application.service.note_service import NoteService
from src.application.facade.notes_facade import NotesFacade
from src.infrastructure.persistence.mysql.note_repository_mysql import NoteRepositoryMySQL
from src.infrastructure.web.controllers.note_controller import note_bp, init_controller

app = Flask(__name__, template_folder="src/views/templates")

init_db()
facade = NotesFacade(NoteService(NoteRepositoryMySQL()))
init_controller(facade)
app.register_blueprint(note_bp)

if __name__ == "__main__":
    app.run(debug=True)
