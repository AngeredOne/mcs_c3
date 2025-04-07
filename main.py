# main.py

from fastapi import FastAPI, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import uvicorn

from api.server import app as api_app, core_app  # <--- Важно!
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
async def ui_submit_task(request: Request, description: str = Form(...)):
    session_id = "default"
    if session_id not in core_app.sessions:
        core_app.start_session(session_id=session_id)

    session = core_app.sessions[session_id]

    task = Task(
        description=description,
        parameters={}
    )

    session.add_task(task)

    return RedirectResponse(f"/ui/session/{session_id}", status_code=303)


@app.get("/ui/session/{session_id}", response_class=HTMLResponse)
async def ui_session_view(request: Request, session_id: str):
    session = core_app.sessions.get(session_id)
    if not session:
        return HTMLResponse(content="Session not found", status_code=404)

    # ПРАВИЛЬНЫЙ доступ к задачам:
    # Стало (правильно)
    tasks = session.get_history()

    return templates.TemplateResponse(
        "session_view.html",
        {
            "request": request,
            "session": session,
            "tasks": tasks,
        }
    )

@app.get("/ui/task/{task_id}", response_class=HTMLResponse)
async def ui_task_view(request: Request, task_id: str):
    task = None
    for session in core_app.sessions.values():
        for ltask in session.get_history():
            if ltask.task_id == task_id:
                task = ltask
                break

    if not task:
        return HTMLResponse(content="Task not found", status_code=404)

    return templates.TemplateResponse(
        "task_view.html",
        {
            "request": request,
            "task": task,
            #"task_final_state": task.task_final_state,
            #"execution_history": task.execution_history,
        }
    )

@app.get("/ui/sessions", response_class=HTMLResponse)
async def ui_sessions(request: Request):
    sessions = core_app.sessions.values()
    return templates.TemplateResponse(
        "sessions.html",
        {
            "request": request,
            "sessions": sessions,
        }
    )



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
