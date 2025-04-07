# main.py

from fastapi import FastAPI, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import uvicorn

from api.server import app as api_app, core_app  # Импорт API и CoreApp
from core.task import Task

app = FastAPI()

# Mount API
app.mount("/api", api_app)

# Static and templates
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

@app.get("/ui")
async def ui_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/ui/new_task")
async def ui_new_task_form(request: Request):
    return templates.TemplateResponse("new_task.html", {"request": request})

@app.post("/ui/new_task")
async def ui_submit_task(request: Request, description: str = Form(...), task_type: str = Form(...)):
    session_id = "default"
    if session_id not in core_app.sessions:
        core_app.create_session(session_id)
    task = Task(description=description, parameters={})
    if task_type == "simple":
        # Делегируем обычную задачу агенту simple_task_agent
        core_app.delegate_task(session_id, "simple_task_agent", task)
    elif task_type == "improvement":
        # Делегируем задачу на улучшение системы агенту internal_improvement_agent
        core_app.delegate_task(session_id, "internal_improvement_agent", task)
    elif task_type == "scenario":
        # Делегируем задачу на генерацию сценария агенту scenario_generator_agent
        core_app.delegate_task(session_id, "scenario_generator_agent", task)
    else:
        # По умолчанию, обычная задача
        core_app.delegate_task(session_id, "simple_task_agent", task)
    return RedirectResponse(f"/ui/task/{task.task_id}", status_code=303)

@app.get("/ui/improvement")
async def ui_improvement_form(request: Request):
    return templates.TemplateResponse("improvement.html", {"request": request})

@app.post("/ui/improvement")
async def ui_submit_improvement(request: Request, description: str = Form(...)):
    session_id = "default"
    if session_id not in core_app.sessions:
        core_app.create_session(session_id)
    task = Task(description=description, parameters={})
    core_app.delegate_task(session_id, "internal_improvement_agent", task)
    return RedirectResponse(f"/ui/task/{task.task_id}", status_code=303)

@app.get("/ui/scenario")
async def ui_scenario_form(request: Request):
    return templates.TemplateResponse("scenario.html", {"request": request})

@app.post("/ui/scenario")
async def ui_submit_scenario(request: Request, description: str = Form(...)):
    session_id = "default"
    if session_id not in core_app.sessions:
        core_app.create_session(session_id)
    task = Task(description=description, parameters={})
    core_app.delegate_task(session_id, "scenario_generator_agent", task)
    return RedirectResponse(f"/ui/task/{task.task_id}", status_code=303)

@app.get("/ui/session/{session_id}", response_class=HTMLResponse)
async def ui_session_view(request: Request, session_id: str):
    session = core_app.sessions.get(session_id)
    if not session:
        return HTMLResponse(content="Session not found", status_code=404)
    tasks = session.get_history()
    return templates.TemplateResponse("session_view.html", {"request": request, "session": session, "tasks": tasks})

@app.get("/ui/task/{task_id}", response_class=HTMLResponse)
async def ui_task_view(request: Request, task_id: str):
    task = None
    for session in core_app.sessions.values():
        for t in session.get_history():
            if t.task_id == task_id:
                task = t
                break
    if not task:
        return HTMLResponse(content="Task not found", status_code=404)
    return templates.TemplateResponse("task_view.html", {"request": request, "task": task})

@app.get("/ui/sessions", response_class=HTMLResponse)
async def ui_sessions_view(request: Request):
    sessions = list(core_app.sessions.values())
    return templates.TemplateResponse("sessions.html", {"request": request, "sessions": sessions})

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
