import os
import json
import asyncio
import openai
from dotenv import load_dotenv

# Config Env and API
load_dotenv()
client = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Define Tool
def calculator_tool(expression: str) -> str:
    print(f"--- Calculator tool with expression {expression} called.")
    try:
        result = eval(expression, {"__builtins__": None}, {})
        return json.dumps({'result': result})
    except Exception as e:
        return json.dumps({"error": f"Error in calculation: {e}"})
    

# Main Function
async def run_calculator_agent(user_query: str) -> str:
    print("Agent: query received. Analyzing....")
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. If the user asks a math question, you MUST use the calculator_tool to find the answer. For all other questions, answer directly."
        },
        {
            "role": "user",
            "content": user_query
        }
    ]

    tools = [
        {
            "type": "function",
            "function": {
                "name": "calculator_tool",
                "description": "Calculates a mathematical expression and returns the result.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "expression": {"type": "string", "description": "The mathematical expression to evaluate, e.g., '120 / (1 - 0.20)'"},
                    },
                    "required": ["expression"],
                },
            }
        }
    ]

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        tool_choice='auto'
    )

    response_message = response.choices[0].message
    messages.append(response_message)

    if response_message.tool_calls:
        print("Agent: Decided to use tool.")

        # Tool calling
        tool_call = response_message.tool_calls[0]
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)

        function_response = calculator_tool(expression=function_args.get("expression"))

        messages.append(
            {
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response
            }
        )

        print(f"Agent: Generating results....")
        final_response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return final_response.choices[0].message.content
    else:
        print(f"Not mathematic question. Generating direct answer....")
        return response_message.content
    

async def main():
    question = "If a product costs $120 after a 20% discount, what was the original price?"
    final_answer = await run_calculator_agent(question)
    print("Final Answer: ")
    print(final_answer)


if __name__ == '__main__':
    asyncio.run(main())

