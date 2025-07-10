# main.py
from client import get_openai_client # Import the new client function
from agts.planner import plan_tasks
from agts.executor import execute_task

def main():
    # Create the client ONCE at the start of your application
    try:
        client = get_openai_client()
    except ValueError as e:
        print(e)
        return

    goal = "Plan a 3-day trip to Paris"
    
    print("🎯 Generating plan...")
    tasks = plan_tasks(client, goal) # Pass the client to the function
    print("✅ Plan Generated:")
    for task in tasks:
        print(f"Step {task.step}: {task.title}")

    print("\n🚀 Executing tasks...")
    executed_tasks = []
    for task in tasks:
        print(f"⚡️ Running step {task.step}: {task.title}")
        executed_task = execute_task(client, task) # Pass the client here too
        executed_tasks.append(executed_task)
        print(f"💡 Result: {executed_task.result}\n")

    print("🎉 All tasks completed!")

if __name__ == "__main__":
    main()