
import sys
import json
from pathlib import Path
from typing import TypedDict, Optional, Any

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DAY06_APP = PROJECT_ROOT / "Day-06" / "app"
DAY08_APP = PROJECT_ROOT / "Day-08" / "app"
DAY09_APP = PROJECT_ROOT / "Day-09" / "app"

sys.path.insert(0, str(DAY06_APP))
sys.path.insert(0, str(DAY08_APP))
sys.path.insert(0, str(DAY09_APP))

from agent_loop import client, MODEL_NAME, TOOLS
from tools import gratuity_and_wage_calculator
from rag import ask_question


# ==========================================
# GRAPH STATE
# ==========================================

class AgentState(TypedDict):
    messages: list
    tool_name: Optional[str]
    tool_arguments: Optional[dict]
    tool_result: Optional[Any]
    answer: Optional[str]
    approved: Optional[bool]


# ==========================================
# AGENT NODE
# ==========================================

def agent_node(state: AgentState):

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=state["messages"],
        tools=TOOLS,
        tool_choice="auto",
        temperature=0
    )

    message = response.choices[0].message

    if not message.tool_calls:
        return {
            "answer": message.content or "I don't know.",
            "tool_name": None
        }

    tool_call = message.tool_calls[0]

    return {
        "messages": state["messages"] + [
            message.model_dump(exclude_none=True)
        ],
        "tool_name": tool_call.function.name,
        "tool_arguments": json.loads(
            tool_call.function.arguments
        )
    }


# ==========================================
# ROUTING
# ==========================================

def route_tool(state: AgentState):

    tool_name = state.get("tool_name")

    if tool_name == "search_labour_info":
        return "search"

    if tool_name == "gratuity_and_wage_calculator":
        return "approval"

    return "end"


# ==========================================
# RAG SEARCH NODE
# ==========================================

def search_node(state: AgentState):

    result = ask_question(
        state["tool_arguments"]["question"]
    )

    return {
        "tool_result": result,
        "messages": state["messages"] + [
            {
                "role": "tool",
                "tool_call_id": (
                    state["messages"][-1]["tool_calls"][0]["id"]
                ),
                "content": json.dumps(
                    result,
                    ensure_ascii=False,
                    default=str
                )
            }
        ],
        "tool_name": None
    }


# ==========================================
# APPROVAL NODE
# ==========================================

def approval_node(state: AgentState):

    approval = interrupt({
        "message": "Gratuity calculation requires your approval.",
        "tool": "gratuity_and_wage_calculator",
        "arguments": state["tool_arguments"],
        "question": "Do you approve this calculation?"
    })

    return {
        "approved": bool(approval)
    }


# ==========================================
# CALCULATOR NODE
# ==========================================

def calculator_node(state: AgentState):

    if not state.get("approved"):
        result = {
            "status": "rejected",
            "message": "User did not approve the calculation."
        }

    else:
        result = gratuity_and_wage_calculator(
            total_monthly_pay=state["tool_arguments"][
                "total_monthly_pay"
            ],
            excluded_allowances=state["tool_arguments"][
                "excluded_allowances"
            ],
            completed_years=state["tool_arguments"][
                "completed_years"
            ]
        )

    return {
        "tool_result": result,
        "messages": state["messages"] + [
            {
                "role": "tool",
                "tool_call_id": (
                    state["messages"][-1]["tool_calls"][0]["id"]
                ),
                "content": json.dumps(
                    result,
                    ensure_ascii=False,
                    default=str
                )
            }
        ]
    }


# ==========================================
# FINAL ANSWER NODE
# ==========================================


def final_node(state: AgentState):

    # Handle rejected calculation directly
    tool_result = state.get("tool_result")

    if (
        isinstance(tool_result, dict)
        and tool_result.get("status") == "rejected"
    ):
        return {
            "answer": (
                "Calculation cancelled. "
                "User did not approve the gratuity calculation. "
                "No calculation was performed."
            )
        }

    if state.get("tool_name") is None and state.get("answer"):
        return {}

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=state["messages"],
        temperature=0
    )

    return {
        "answer": response.choices[0].message.content
        or "I don't know."
    }



# ==========================================
# BUILD LANGGRAPH
# ==========================================

builder = StateGraph(AgentState)

builder.add_node("agent", agent_node)
builder.add_node("search", search_node)
builder.add_node("approval", approval_node)
builder.add_node("calculator", calculator_node)
builder.add_node("final", final_node)

builder.add_edge(START, "agent")

builder.add_conditional_edges(
    "agent",
    route_tool,
    {
        "search": "search",
        "approval": "approval",
        "end": END
    }
)

builder.add_edge("search", "final")
builder.add_edge("approval", "calculator")
builder.add_edge("calculator", "final")
builder.add_edge("final", END)

memory = MemorySaver()

graph = builder.compile(
    checkpointer=memory
)


# ==========================================
# GRAPH RUN FUNCTION
# ==========================================

def run_graph(
    question: str,
    thread_id: str,
    approved: Optional[bool] = None
):

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    if approved is None:

        initial_state = {
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are ShramikSathi, a labour law assistant. "
                        "Use search_labour_info for labour questions. "
                        "Use gratuity_and_wage_calculator for calculations. "
                        "Never invent missing inputs. "
                        "Use calculator output as the source of truth. "
                        "Preserve RAG citations in your answer."
                    )
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            "tool_name": None,
            "tool_arguments": None,
            "tool_result": None,
            "answer": None,
            "approved": None
        }

        result = graph.invoke(
            initial_state,
            config=config
        )

    else:

        from langgraph.types import Command

        result = graph.invoke(
            Command(resume=approved),
            config=config
        )

    if "__interrupt__" in result:
        return {
            "status": "approval_required",
            "approval_request": result["__interrupt__"][0].value,
            "thread_id": thread_id
        }

    return {
        "status": "completed",
        "answer": result.get("answer"),
        "tool_result": result.get("tool_result"),
        "thread_id": thread_id
    }
