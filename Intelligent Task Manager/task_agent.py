# /task_agent.py
import openai
import json
from config import OPENAI_API_KEY, MODEL_NAME
from prompts import get_prioritization_prompt, get_scheduling_prompt # No change to imports
from tools.definitions import get_tool_definitions
from tools.implementations import AVAILABLE_TOOLS

class TaskManagerAgent:
    """Agent that prioritizes and schedules tasks in a multi-step process."""
    def __init__(self):
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)

    def _run_prioritization_step(self, tasks: list[dict]) -> list[str] | None:
        """Runs the first LLM call to get a prioritized list of task names."""
        print("🤖 Agent Step 1: Prioritizing tasks...")
        prompt = get_prioritization_prompt().format(tasks_json=json.dumps(tasks, indent=2))
        
        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "system", "content": prompt}],
            response_format={"type": "json_object"}
        )
        try:
            result = json.loads(response.choices[0].message.content)
            prioritized_task_names = result.get("prioritized_order", [])
            print(f"✅ Prioritized Order: {prioritized_task_names}")
            return prioritized_task_names
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error processing prioritization response: {e}")
            return None

    def _run_scheduling_step(self, prioritized_tasks: list[str]) -> tuple[str, list[str]]:
        """
        Runs the scheduling step by looping through each task and calling the LLM.
        """
        print("\n🤖 Agent Step 2: Scheduling tasks one by one...")
        
        tool_logs = []
        scheduling_tools = get_tool_definitions(use_cases=['schedule_task'])
        
        # --- Start of the new Python-controlled loop ---
        for task_name in prioritized_tasks:
            print(f"\n--- Scheduling task: {task_name} ---")
            
            # Create a simple, single-purpose prompt for each task
            prompt = get_scheduling_prompt(task_name)
            
            messages = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"Please schedule the task named: '{task_name}'"}
            ]
            
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                tools=scheduling_tools,
                tool_choice={"type": "function", "function": {"name": "schedule_task"}} # Force tool use
            )
            
            response_message = response.choices[0].message
            
            # Execute the tool call for this specific task
            if response_message.tool_calls:
                tool_call = response_message.tool_calls[0]
                function_to_call = AVAILABLE_TOOLS[tool_call.function.name]
                function_args = json.loads(tool_call.function.arguments)
                function_response = function_to_call(**function_args)
                tool_logs.append(function_response)
        # --- End of the loop ---
        
        # After all tasks are scheduled, ask for a final summary
        summary_prompt = "All tasks have been scheduled. Please provide a brief confirmation summary to the user."
        final_summary_response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "system", "content": summary_prompt}]
        )
        summary = final_summary_response.choices[0].message.content
        return summary, tool_logs

    def process_tasks(self, tasks: list[dict]) -> tuple[str, list[str]]:
        """Main method to run the agent's multi-step logic."""
        prioritized_task_names = self._run_prioritization_step(tasks)
        if not prioritized_task_names:
            return "Failed to prioritize tasks. Please check the logs.", []
            
        summary, logs = self._run_scheduling_step(prioritized_task_names)
        
        print(f"\n🤖 Agent Final Summary: {summary}")
        return summary, logs