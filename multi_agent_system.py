import os
from typing import List, Dict, Optional
import json
import asyncio
import nest_asyncio
from anthropic import AsyncAnthropic
from dataclasses import dataclass
from enum import Enum

# Enable nested event loop for Colab/Jupyter
nest_asyncio.apply()

class AgentRole(Enum):
    COORDINATOR = "coordinator"
    RESEARCHER = "researcher"
    CRITIC = "critic"
    IMPLEMENTER = "implementer"

@dataclass
class Message:
    role: str
    content: str

@dataclass
class Task:
    id: str
    description: str
    status: str
    assigned_to: Optional[str] = None
    result: Optional[str] = None

class Agent:
    def __init__(self, role: AgentRole, system_prompt: str):
        self.role = role
        self.system_prompt = system_prompt
        self.conversation_history: List[Message] = []
        self.client = AsyncAnthropic()

    async def process_message(self, message: str) -> str:
        # Add the new message to conversation history
        self.conversation_history.append(Message(role="user", content=message))

        # Construct the messages for Claude
        messages = [
            {
                "role": "assistant",
                "content": self.system_prompt
            }
        ]

        # Add conversation history
        for msg in self.conversation_history[-5:]:  # Keep last 5 messages for context
            messages.append({
                "role": msg.role,
                "content": msg.content
            })

        try:
            response = await self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1024,
                messages=messages
            )

            response_content = response.content[0].text
            self.conversation_history.append(Message(role="assistant", content=response_content))
            return response_content

        except Exception as e:
            return f"Error processing message: {str(e)}"

class MultiAgentSystem:
    def __init__(self):
        self.agents: Dict[AgentRole, Agent] = {
            AgentRole.COORDINATOR: Agent(
                AgentRole.COORDINATOR,
                "You are the coordinator agent. Your role is to break down tasks, assign them to appropriate agents, and ensure completion."
            ),
            AgentRole.RESEARCHER: Agent(
                AgentRole.RESEARCHER,
                "You are the researcher agent. Your role is to search latest research related to the tasks."
            ),
            AgentRole.CRITIC: Agent(
                AgentRole.CRITIC,
                "You are the critic agent. Your role is to review and provide constructive feedback on solutions."
            ),
            AgentRole.IMPLEMENTER: Agent(
                AgentRole.IMPLEMENTER,
                "You are the implementer agent. Your role is to execute tasks and implement solutions."
            )
        }
        self.tasks: List[Task] = []

    async def process_task(self, task_description: str) -> str:
        # Create new task
        task_id = f"task_{len(self.tasks) + 1}"
        task = Task(id=task_id, description=task_description, status="new")
        self.tasks.append(task)

        # Step 1: Coordinator breaks down the task
        coordinator_response = await self.agents[AgentRole.COORDINATOR].process_message(
            f"Please break down this task into subtasks: {task_description}"
        )

        # Step 2: Researcher gathers information
        research_response = await self.agents[AgentRole.RESEARCHER].process_message(
            f"Please research the following task: {task_description}\n\nContext: {coordinator_response}"
        )

        # Step 3: Implementer creates solution
        implementation_response = await self.agents[AgentRole.IMPLEMENTER].process_message(
            f"Please implement a solution for: {task_description}\n\nResearch findings: {research_response}"
        )

        # Step 4: Critic reviews solution
        critic_response = await self.agents[AgentRole.CRITIC].process_message(
            f"Please review this solution: {implementation_response}\n\nOriginal task: {task_description}"
        )

        # Step 5: Coordinator synthesizes final response
        final_response = await self.agents[AgentRole.COORDINATOR].process_message(
            f"Please synthesize a final response for the task: {task_description}\n\n"
            f"Implementation: {implementation_response}\n\n"
            f"Critic's review: {critic_response}"
        )

        task.status = "completed"
        task.result = final_response
        return final_response

# Helper function to run tasks
async def run_task(task_description: str):
    system = MultiAgentSystem()
    result = await system.process_task(task_description)
    return result


if __name__ == "__main__":
    import asyncio
    
    async def main():
        task_description = "write a simple Python function to calculate the Fibonacci sequence"
        result = await run_task(task_description)
        print(f"Final result: {result}")
    
    asyncio.run(main())
