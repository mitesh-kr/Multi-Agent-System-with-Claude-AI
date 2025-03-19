# Multi-Agent System with Claude AI

This project implements a multi-agent system using Anthropic's Claude API. The system consists of four specialized agents that work together to solve tasks:

1. **Coordinator**: Breaks down tasks and coordinates the workflow
2. **Researcher**: Gathers information and research related to tasks
3. **Implementer**: Creates solutions and implements code
4. **Critic**: Reviews and provides feedback on solutions

## Requirements

- Python 3.7+
- Anthropic API key

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/multi-agent-system.git
cd multi-agent-system
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up your Anthropic API key:
```bash
export ANTHROPIC_API_KEY=your_api_key_here
```

## Usage

You can use the multi-agent system by importing the `MultiAgentSystem` class and using the `process_task` method:

```python
import asyncio
from multi_agent_system import MultiAgentSystem

async def main():
    system = MultiAgentSystem()
    result = await system.process_task("Write a Python function to calculate the Fibonacci sequence")
    print(result)

asyncio.run(main())
```

Alternatively, you can use the provided `run_task` helper function:

```python
import asyncio
from multi_agent_system import run_task

async def main():
    result = await run_task("Write a Python function to calculate the Fibonacci sequence")
    print(result)

asyncio.run(main())
```

## Example

```python
import asyncio
from multi_agent_system import run_task

async def main():
    task_description = "Implement a simple web scraper in Python"
    result = await run_task(task_description)
    print(f"Final result: {result}")

asyncio.run(main())
```

## Project Structure

- `multi_agent_system.py`: Main implementation of the multi-agent system
- `requirements.txt`: List of required Python packages
- `examples/`: Directory containing example usage scripts

## License

[MIT License](LICENSE)
