# Programación Avanzada — Patrón Facade

CRUD de notas de estudiantes con Flask, arquitectura hexagonal (puertos y adaptadores) y patrón de diseño Facade.

## Autores

- JOAN SAMUEL ANACONA NARVAEZ
- DAVID NICOLAS MUESES MUCHAVISOY
- ILIAN MAURICIO GONZALES

## Descripción

Aplicación web con Flask para gestionar notas de estudiantes (`id, estudiante, materia, nota 0.0-5.0, fecha`).

- `src/domain/`: entidad `Note` con validación.
- `src/application/ports/`: puerto `NoteRepository`.
- `src/application/service/`: casos de uso (`NoteService`).
- `src/application/facade/`: fachada única `NotesFacade` (CRUD simplificado + operación compuesta `ficha_estudiante`).
- `src/infrastructure/persistence/mysql/`: adaptador MySQL.
- `src/infrastructure/web/controllers/`: controlador Flask (solo habla con el Facade).
- `src/views/templates/`: plantilla `index.html`.
- `app.py`: composición de dependencias.

## Requisitos

- Python 3.10+
- MySQL con base de datos `notas_db`
- Dependencias en `requirements.txt`

## Instalación y ejecución (Windows PowerShell)

```powershell
python -m venv env
.\env\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Abrir `http://127.0.0.1:5000/`.

## Pruebas

```powershell
pytest tests/test_qa.py -v
```
