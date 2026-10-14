"""QA Tester WAVE7 - Verifica patron Facade + CRUD.
Ejecutar: PYTHONPATH=. env/Scripts/python tests/test_qa.py
"""
import ast
import pathlib

PASS = []


def check(name, fn):
    try:
        fn()
        PASS.append(name)
        print(f"[PASS] {name}")
    except AssertionError as e:
        print(f"[FAIL] {name}: {e}")
        raise SystemExit(f"QA BLOQUEADO en: {name}: {e}")


def imports_of(path):
    tree = ast.parse(pathlib.Path(path).read_text(encoding="utf-8"))
    mods = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            mods += [a.name for a in n.names]
        if isinstance(n, ast.ImportFrom):
            mods.append(n.module or "")
    return " ".join(mods).lower()


# --- 7.1 Estaticos ---
def t_facade_exists():
    p = pathlib.Path("src/application/facade/notes_facade.py")
    assert p.exists(), "falta notes_facade.py"
    src = p.read_text(encoding="utf-8")
    assert "class NotesFacade" in src, "falta clase NotesFacade"
    for m in ["crear_nota", "listar_notas", "obtener_nota", "actualizar_nota", "eliminar_nota", "ficha_estudiante"]:
        assert m in src, f"facade sin metodo {m}"


def t_facade_aislamiento():
    mods = imports_of("src/application/facade/notes_facade.py")
    assert "flask" not in mods, f"facade importa web: {mods}"
    assert "mysql" not in mods and "mysql_connection" not in mods, f"facade importa db: {mods}"


def t_controller_solo_facade():
    mods = imports_of("src/infrastructure/web/controllers/note_controller.py")
    assert "notesfacade" in mods.replace("_", "") or "facade" in mods, f"controller no usa facade: {mods}"
    assert "noteservice" not in mods.replace("_", ""), f"controller viola facade, importa service: {mods}"
    assert "repositorymysql" not in mods.replace("_", "") and "mysql" not in mods, f"controller viola facade, importa db: {mods}"


def t_grep_plan():
    import subprocess
    r1 = subprocess.run(["powershell", "-c", "Select-String -Path src\\infrastructure\\web\\controllers\\*.py -Pattern 'NoteService|RepositoryMySQL|mysql'"],
                        capture_output=True, text=True)
    assert "NoteService" not in r1.stdout and "RepositoryMySQL" not in r1.stdout, r1.stdout
    r2 = subprocess.run(["powershell", "-c", "Select-String -Path src\\application\\facade\\*.py -Pattern 'flask|mysql|Blueprint'"],
                        capture_output=True, text=True)
    # filtrar: solo fallan hits reales de codigo (el grep del plan es literal)
    assert r2.stdout.strip() == "", f"hits facade: {r2.stdout}"


# --- 7.2 Funcionales ---
class FakeRepo:
    def __init__(self):
        self.data = {}
        self.seq = 0
    def create(self, note):
        self.seq += 1
        note.id = self.seq
        self.data[self.seq] = note
        return self.seq
    def find_all(self):
        return list(self.data.values())
    def find_by_id(self, nid):
        return self.data.get(int(nid))
    def update(self, note):
        self.data[note.id] = note
        return 1
    def delete(self, nid):
        return self.data.pop(int(nid), None) is not None


def t_aislamiento_fake():
    from src.application.service.note_service import NoteService
    from src.application.facade.notes_facade import NotesFacade
    f = NotesFacade(NoteService(FakeRepo()))
    nid = f.crear_nota({"estudiante": "Ana", "materia": "Mat", "nota": "4.5", "fecha": "2026-10-14"})
    f.crear_nota({"estudiante": "Ana", "materia": "Fis", "nota": "3.5", "fecha": "2026-10-15"})
    assert f.ficha_estudiante("Ana")["promedio"] == 4.0
    try:
        f.crear_nota({"estudiante": "Ana", "materia": "X", "nota": "9", "fecha": "2026-10-14"})
        assert False, "debió rechazar nota=9"
    except ValueError:
        pass
    f.actualizar_nota(nid, {"nota": "5.0"})
    assert f.obtener_nota(nid).nota == 5.0
    f.eliminar_nota(nid)
    assert f.obtener_nota(nid) is None


def t_e2e_mysql():
    from app import app
    from src.infrastructure.persistence.mysql.note_repository_mysql import NoteRepositoryMySQL
    c = app.test_client()
    repo = NoteRepositoryMySQL()
    # 1. crear valida
    r = c.post("/crear", data={"estudiante": "QA_FINAL", "materia": "Matematicas", "nota": "4.5", "fecha": "2026-10-14"}, follow_redirects=True)
    assert r.status_code == 200 and "QA_FINAL" in r.get_data(as_text=True), "crear valida"
    nid = [x for x in repo.find_all() if x.estudiante == "QA_FINAL"][-1].id
    # 2. crear invalida
    r = c.post("/crear", data={"estudiante": "QA_FINAL", "materia": "X", "nota": "9", "fecha": "2026-10-14"})
    assert r.status_code == 302 and "error" in r.headers.get("Location", ""), "crear invalida debe redirigir con error"
    # 3. listar
    r = c.get("/")
    assert r.status_code == 200 and "<table>" in r.get_data(as_text=True), "listar"
    # 4. actualizar
    c.post(f"/actualizar/{nid}", data={"nota": "5.0"}, follow_redirects=True)
    assert repo.find_by_id(nid).nota == 5.0, "actualizar"
    # 5. ficha compuesta
    r = c.get("/?estudiante=QA_FINAL")
    assert "promedio" in r.get_data(as_text=True).lower(), "ficha"
    # 6. eliminar
    c.post(f"/eliminar/{nid}", follow_redirects=True)
    assert repo.find_by_id(nid) is None, "eliminar"


for name, fn in [
    ("7.1 facade existe + API", t_facade_exists),
    ("7.1 facade aislamiento", t_facade_aislamiento),
    ("7.1 controller solo-facade", t_controller_solo_facade),
    ("7.1 grep PLAN", t_grep_plan),
    ("7.2 aislamiento fake + ficha", t_aislamiento_fake),
    ("7.2 E2E MySQL CRUD", t_e2e_mysql),
]:
    check(name, fn)

print(f"\nQA VERDE: {len(PASS)}/{6} checks. Facade verificado, CRUD E2E verificado.")
