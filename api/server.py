# api/server.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from agents.openai_agent import OpenAIAgent
from agents.internal_improvement_agent import InternalImprovementAgent
from agents.scenario_generator_agent import ScenarioGeneratorAgent  # Новый агент
from core.app import CoreApp
from core.task import Task

from commands.echo_command import EchoCommand
from commands.add_numbers_command import AddNumbersCommand
from commands.get_datetime_command import GetDateTimeCommand
from commands.read_file_command import ReadFileCommand
from commands.write_file_command import WriteFileCommand
from commands.diff_file_command import DiffFileCommand
from commands.list_directory_command import ListDirectoryCommand
from commands.delete_file_command import DeleteFileCommand

from agents.simple_task_agent import SimpleTaskAgent
from agents.planner_agent import PlannerAgent
from agents.task_planner_agent import TaskPlannerAgent
from agents.prompt_engineer_agent import PromptEngineerAgent
from agents.goal_validator_agent import GoalValidatorAgent
from agents.parameter_corrector_agent import ParameterCorrectorAgent
from agents.logger_agent import LoggerAgent
from agents.filesystem_agent import FilesystemAgent
from agents.validation_agent import ValidationAgent
from agents.inner_developer_agent import InnerDeveloperAgent

from core.chain import ProcessingChain
from core.scenario_dynamic import Scenario, ScenarioStep

app = FastAPI()

core_app = CoreApp()

# Регистрация команд и агентов
core_app.register_command(EchoCommand())
core_app.register_command(AddNumbersCommand())
core_app.register_command(GetDateTimeCommand())
core_app.register_command(ReadFileCommand())
core_app.register_command(WriteFileCommand())
core_app.register_command(DiffFileCommand())
core_app.register_command(ListDirectoryCommand())
core_app.register_command(DeleteFileCommand())

core_app.register_agent(SimpleTaskAgent())
core_app.register_agent(PlannerAgent())
core_app.register_agent(TaskPlannerAgent())

core_app.register_agent(OpenAIAgent(model="gpt-4", temperature=0.3))

core_app.register_agent(PromptEngineerAgent())
core_app.register_agent(GoalValidatorAgent())
core_app.register_agent(ParameterCorrectorAgent())
core_app.register_agent(LoggerAgent())
core_app.register_agent(FilesystemAgent())
core_app.register_agent(ValidationAgent())
core_app.register_agent(InnerDeveloperAgent())
core_app.register_agent(InternalImprovementAgent())
core_app.register_agent(ScenarioGeneratorAgent())  # Регистрация нового агента

# Создание сессии
core_app.create_session("default")

# Регистрация цепочки обработки
core_app.register_chain(ProcessingChain(
    name="standard_preprocessing",
    agent_sequence=[
        "prompt_engineer_agent",
        "goal_validator_agent",
        "parameter_corrector_agent",
        "logger_agent"
    ]
))

core_app.register_chain(ProcessingChain(
    name="file_edit_flow",
    agent_sequence=[
        "inner_developer_agent",
        "filesystem_agent",
        "validation_agent",
        "filesystem_agent"
    ]
))

# Базовый сценарий
steps = {
    "validate": ScenarioStep("validate", "standard_preprocessing", "validator", "execute", None),
    "execute": ScenarioStep("execute", None, "executor", None, None)
}
scenario = Scenario(name="basic_execution", steps=steps, start_step="validate")
core_app.register_scenario(scenario)

from core.scenario_dynamic import Scenario, ScenarioStep

file_edit_steps = {
    "generate_change": ScenarioStep(
        name="generate_change",
        chain_name=None,
        required_role="inner_developer",
        next_step_on_success="diff_file"
    ),
    "diff_file": ScenarioStep(
        name="diff_file",
        chain_name=None,
        required_role="filesystem_operator",
        next_step_on_success="validate_change"
    ),
    "validate_change": ScenarioStep(
        name="validate_change",
        chain_name=None,
        required_role="change_validator",
        next_step_on_success="apply_change",
        next_step_on_failure=None
    ),
    "apply_change": ScenarioStep(
        name="apply_change",
        chain_name=None,
        required_role="filesystem_operator",
        next_step_on_success=None,
        next_step_on_failure=None
    )
}

file_edit_scenario = Scenario(
    name="file_edit_scenario",
    steps=file_edit_steps,
    start_step="generate_change"
)

core_app.register_scenario(file_edit_scenario)

class TaskRequest(BaseModel):
    description: str
    parameters: dict

class ChainTaskRequest(BaseModel):
    chain_name: str
    agent_name: str
    description: str
    parameters: dict

class ScenarioTaskRequest(BaseModel):
    scenario_name: str
    description: str
    parameters: dict

@app.get("/commands")
def get_commands():
    return core_app.list_commands()

@app.get("/agents")
def get_agents():
    return core_app.list_agents()

@app.post("/sessions/{session_id}/task")
def post_task(session_id: str, task_request: TaskRequest):
    if session_id not in core_app.sessions:
        core_app.create_session(session_id)
    task = Task(description=task_request.description, parameters=task_request.parameters)
    result = core_app.delegate_task(session_id, "simple_task_agent", task)
    return {"result": result}

@app.post("/sessions/{session_id}/chain_task")
def post_chain_task(session_id: str, request: ChainTaskRequest):
    if session_id not in core_app.sessions:
        core_app.create_session(session_id)
    task = Task(description=request.description, parameters=request.parameters)
    task = core_app.process_task_via_chain(request.chain_name, task)
    result = core_app.delegate_task(session_id, request.agent_name, task)
    return {"result": result}

@app.post("/sessions/{session_id}/scenario_task")
def post_scenario_task(session_id: str, request: ScenarioTaskRequest):
    if session_id not in core_app.sessions:
        core_app.create_session(session_id)
    task = Task(description=request.description, parameters=request.parameters)
    result = core_app.execute_scenario(request.scenario_name, session_id, task)
    return result

# Новый эндпоинт для задач на улучшение системы
@app.post("/sessions/{session_id}/improvement_task")
def post_improvement_task(session_id: str, task_request: TaskRequest):
    if session_id not in core_app.sessions:
        core_app.create_session(session_id)
    task = Task(description=task_request.description, parameters=task_request.parameters)
    result = core_app.delegate_task(session_id, "internal_improvement_agent", task)
    return {"result": result}
