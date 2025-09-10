# executor.py
from openai import OpenAI # Import the client type hint
from models.schema import Task, ExecutedTask

# The function now requires the client
def execute_task(client: OpenAI, task: Task) -> ExecutedTask:
    prompt = f"""You are an executor AI agent. 
                Your job is to perform the following task:
                Step {task.step}: {task.title}
                Description: {task.description}
                Please complete it and return a short result or summary."""
    
    # Use the passed-in client
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    result = response.choices[0].message.content

    return ExecutedTask(
        step=task.step,
        title=task.title,
        description=task.description,
        result=result
    )