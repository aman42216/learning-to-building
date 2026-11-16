
import os
import sys
import json
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq


# ==========================================
# PATH CONFIGURATION
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DAY06_DIR = PROJECT_ROOT / "Day-06"
DAY08_APP = PROJECT_ROOT / "Day-08" / "app"
DAY09_APP = PROJECT_ROOT / "Day-09" / "app"

sys.path.insert(0, str(DAY08_APP))
sys.path.insert(0, str(DAY09_APP))


# ==========================================
# GROQ CONFIGURATION
# ==========================================

load_dotenv(DAY06_DIR / ".env")

API_KEY = os.getenv("GROQ_API_KEY")

MODEL_NAME = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile"
)

if not API_KEY:
    raise ValueError(
        "Groq API key not found in Day-06/.env"
    )

client = Groq(api_key=API_KEY)


# ==========================================
# IMPORT PROJECT TOOLS
# ==========================================

from rag import ask_question
from tools import gratuity_and_wage_calculator


# ==========================================
# AVAILABLE AGENT TOOLS
# ==========================================

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_labour_info",
            "description": (
                "Search official labour law information "
                "using ShramikSathi RAG."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "Labour law question"
                    }
                },
                "required": ["question"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "gratuity_and_wage_calculator",
            "description": (
                "Calculate adjusted monthly wages and "
                "gratuity using the 50 percent wages rule."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "total_monthly_pay": {
                        "type": "number"
                    },
                    "excluded_allowances": {
                        "type": "number"
                    },
                    "completed_years": {
                        "type": "integer"
                    }
                },
                "required": [
                    "total_monthly_pay",
                    "excluded_allowances",
                    "completed_years"
                ]
            }
        }
    }
]


# ==========================================
# TOOL EXECUTION
# ==========================================

def execute_tool(tool_name, arguments):

    if tool_name == "search_labour_info":

        return ask_question(
            arguments["question"]
        )

    elif tool_name == "gratuity_and_wage_calculator":

        return gratuity_and_wage_calculator(
            total_monthly_pay=arguments["total_monthly_pay"],
            excluded_allowances=arguments["excluded_allowances"],
            completed_years=arguments["completed_years"]
        )

    else:
        return {
            "error": f"Unknown tool: {tool_name}"
        }


# ==========================================
# HAND-WRITTEN AGENT LOOP
# ==========================================

def run_agent(user_message):

    messages = [
        {
            "role": "system",
            "content": (
                "You are ShramikSathi, a labour law assistant. "

                "Use search_labour_info for labour law questions. "

                "Use gratuity_and_wage_calculator for calculations. "

                "Never invent missing calculation inputs. "

                "Use the calculator tool output as the single "
                "source of truth for all numerical values. "

                "Do not independently recalculate or change "
                "the values returned by the calculator. "

                "Explain excess allowances using the exact "
                "excess_allowances_added_back value returned "
                "by the tool. "

                "Do not invent legal provisions or claim "
                "legal eligibility. "

                "For labour law answers, preserve the citations "
                "returned by the RAG search tool. "

                "Clearly present the final answer."
            )
        },
        {
            "role": "user",
            "content": user_message
        }
    ]

    # Agent tool-calling loop
    for step in range(5):

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0
        )

        message = response.choices[0].message

        # If no tool is requested, return final answer
        if not message.tool_calls:

            return {
                "answer": message.content or "I don't know.",
                "tool_calls": step
            }

        # Add assistant tool-call message
        messages.append(
            message.model_dump(exclude_none=True)
        )

        # Execute requested tools
        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name

            arguments = json.loads(
                tool_call.function.arguments
            )

            result = execute_tool(
                tool_name,
                arguments
            )

            # Send tool result back to Groq
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(
                    result,
                    ensure_ascii=False,
                    default=str
                )
            })

    raise RuntimeError(
        "Agent reached maximum tool steps"
    )


# ==========================================
# TESTING
# ==========================================

if __name__ == "__main__":

    question = (
        "Calculate gratuity for total monthly pay "
        "Rs. 50000, excluded allowances Rs. 30000 "
        "and 10 completed years of service."
    )

    result = run_agent(question)

    print("\nSHRAMIKSATHI AGENT RESULT")
    print("=" * 40)
    print(result["answer"])
    print("\nTool calls:", result["tool_calls"])
