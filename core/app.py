# core/app.py

import importlib
import inspect
from typing import Dict, Any, List
from core.command import Command
from core.agent import Agent
from core.session import Session
from core.task import Task
from core.chain import ProcessingChain
from core.context_qdrant import QdrantVectorStore
from core.scenario_dynamic import Scenario, ScenarioExecutor

class CoreApp:
    def __init__(self):
        self.commands: Dict[str, Command] = {}
        self.agents: Dict[str, Agent] = {}
        self.sessions: Dict[str, Session] = {}
        self.chains: Dict[str, ProcessingChain] = {}
        self.context = QdrantVectorStore()
        self.scenarios: Dict[str, Scenario] = {}

    def register_command(self, command: Command):
        if command.name in self.commands:
            raise ValueError(f"Command '{command.name}' already registered.")
        self.commands[command.name] = command

    def register_agent(self, agent: Agent):
        if agent.name in self.agents:
            raise ValueError(f"Agent '{agent.name}' already registered.")
        agent.bind_app(self)
        self.agents[agent.name] = agent

    def create_session(self, session_id: str) -> Session:
        if session_id in self.sessions:
            raise ValueError(f"Session '{session_id}' already exists.")
        session = Session(session_id)
        self.sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> Session:
        if session_id not in self.sessions:
            raise ValueError(f"Session '{session_id}' not found.")
        return self.sessions[session_id]

    def run_command(self, name: str, **kwargs) -> Any:
        if name not in self.commands:
            raise ValueError(f"Command '{name}' not found.")
        command = self.commands[name]
        return command.execute(**kwargs)

    def delegate_task(self, session_id: str, agent_name: str, task: Task) -> Any:
        if agent_name not in self.agents:
            raise ValueError(f"Agent '{agent_name}' not found.")
        if session_id not in self.sessions:
            raise ValueError(f"Session '{session_id}' not found.")
        agent = self.agents[agent_name]
        session = self.sessions[session_id]
        result = agent.handle_task(task)
        task.set_result(result)
        session.add_task(task)
        return result

    def list_commands(self) -> Dict[str, str]:
        return {name: cmd.description for name, cmd in self.commands.items()}

    def list_agents(self) -> Dict[str, str]:
        return {name: agent.role or agent.__class__.__name__ for name, agent in self.agents.items()}

    def list_chains(self) -> Dict[str, List[str]]:
        return {name: chain.agent_sequence for name, chain in self.chains.items()}

    def register_chain(self, chain: ProcessingChain):
        if chain.name in self.chains:
            raise ValueError(f"Chain '{chain.name}' already exists.")
        self.chains[chain.name] = chain

    def process_task_via_chain(self, chain_name: str, task: Task) -> Task:
        if chain_name not in self.chains:
            raise ValueError(f"Chain '{chain_name}' not found.")
        chain = self.chains[chain_name]
        return chain.process(self, task)

    def load_command_from_module(self, module_path: str):
        module = importlib.import_module(module_path)
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, Command) and obj is not Command:
                self.register_command(obj())

    def load_agent_from_module(self, module_path: str):
        module = importlib.import_module(module_path)
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, Agent) and obj is not Agent:
                self.register_agent(obj())

    def register_scenario(self, scenario: Scenario):
        if scenario.name in self.scenarios:
            raise ValueError(f"Scenario '{scenario.name}' already exists.")
        self.scenarios[scenario.name] = scenario

    def execute_scenario(self, scenario_name: str, session_id: str, task: Task) -> Any:
        if scenario_name not in self.scenarios:
            raise ValueError(f"Scenario '{scenario_name}' not found.")
        scenario = self.scenarios[scenario_name]
        executor = ScenarioExecutor(self, session_id)
        return executor.execute(scenario, task)
