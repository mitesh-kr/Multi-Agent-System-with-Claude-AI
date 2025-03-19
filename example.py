import asyncio
import os
from multi_agent_system import run_task

# Set your API key here or use environment variable
# os.environ["ANTHROPIC_API_KEY"] = "your_api_key_here"

async def main():
    # Example task
    task_description = "write python code to implement ResNet on ImageNet for classification"
    
    print(f"Processing task: {task_description}")
    result = await run_task(task_description)
    print(f"Final result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
