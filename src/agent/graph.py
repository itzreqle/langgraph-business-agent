"""LangGraph AI agent for analyzing business data and generating recommendations.

This module defines a graph with input, processing, and recommendation nodes to
analyze daily sales, costs, and customer data, producing a summary report with
actionable advice.
"""

from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END

# Define state structures
class BusinessData(TypedDict):
    """Typed dictionary for daily business data."""
    sales: float
    costs: float
    customers: int

class DailyData(TypedDict):
    """Typed dictionary for today's and yesterday's business data."""
    today: BusinessData
    yesterday: BusinessData

class Metrics(TypedDict):
    """Typed dictionary for calculated business metrics."""
    profit_today: float
    profit_yesterday: float
    cac_today: float
    cac_yesterday: float
    sales_change: float
    cost_change: float

class Recommendations(TypedDict):
    """Typed dictionary for recommendations and alerts."""
    profit_status: str
    alerts: list[str]
    recommendations: list[str]

class State(TypedDict):
    """Typed dictionary for the agent's state."""
    data: DailyData
    metrics: Optional[Metrics]
    recommendations: Optional[Recommendations]

def input_node(state: State) -> State:
    """Validate the input data for required fields.

    Args:
        state: The current state containing input data.

    Returns:
        The validated state.

    Raises:
        ValueError: If required data fields are missing.
    """
    if not state.get("data") or not state["data"].get("today") or not state["data"].get("yesterday"):
        raise ValueError("Invalid input data: 'data' with 'today' and 'yesterday' required")
    return state

def processing_node(state: State) -> State:
    """Calculate key business metrics from input data.

    Args:
        state: The current state with validated input data.

    Returns:
        The state updated with calculated metrics.
    """
    today = state["data"]["today"]
    yesterday = state["data"]["yesterday"]
    
    # Calculate profits
    profit_today = today["sales"] - today["costs"]
    profit_yesterday = yesterday["sales"] - yesterday["costs"]
    
    # Calculate Customer Acquisition Cost (CAC)
    cac_today = today["costs"] / today["customers"] if today["customers"] > 0 else 0
    cac_yesterday = yesterday["costs"] / yesterday["customers"] if yesterday["customers"] > 0 else 0
    
    # Calculate percentage changes
    sales_change = ((today["sales"] - yesterday["sales"]) / yesterday["sales"] * 100) if yesterday["sales"] > 0 else 0
    cost_change = ((today["costs"] - yesterday["costs"]) / yesterday["costs"] * 100) if yesterday["costs"] > 0 else 0
    
    state["metrics"] = {
        "profit_today": profit_today,
        "profit_yesterday": profit_yesterday,
        "cac_today": cac_today,
        "cac_yesterday": cac_yesterday,
        "sales_change": sales_change,
        "cost_change": cost_change
    }
    return state

def recommendation_node(state: State) -> State:
    """Generate actionable recommendations based on calculated metrics.

    Args:
        state: The current state with calculated metrics.

    Returns:
        The state updated with recommendations and alerts.
    """
    metrics = state["metrics"]
    profit_today = metrics["profit_today"]
    cac_today = metrics["cac_today"]
    cac_yesterday = metrics["cac_yesterday"]
    sales_change = metrics["sales_change"]
    
    alerts = []
    recommendations = []
    
    # Profit or loss status
    if profit_today >= 0:
        profit_status = f"Profit: ${profit_today:.2f}"
    else:
        profit_status = f"Loss: ${-profit_today:.2f}"
        recommendations.append("Reduce costs to improve profitability")
    
    # Check for significant CAC increase
    if cac_yesterday > 0:
        cac_change = ((cac_today - cac_yesterday) / cac_yesterday) * 100
        if cac_change > 20:
            alerts.append(f"CAC increased by {cac_change:.2f}%, which is significant.")
            recommendations.append("Review marketing campaigns for efficiency")
    
    # Suggest budget increase if sales are growing
    if sales_change > 0:
        recommendations.append(f"Consider increasing advertising budget due to {sales_change:.2f}% sales growth")
    
    state["recommendations"] = {
        "profit_status": profit_status,
        "alerts": alerts,
        "recommendations": recommendations
    }
    return state

def build_graph():
    """Build and compile the LangGraph structure.

    Returns:
        The compiled LangGraph object.
    """
    graph = StateGraph(State)
    graph.add_node("input", input_node)
    graph.add_node("processing", processing_node)
    graph.add_node("recommendation", recommendation_node)
    
    graph.add_edge("input", "processing")
    graph.add_edge("processing", "recommendation")
    graph.add_edge("recommendation", END)
    
    graph.set_entry_point("input")
    
    return graph.compile()

def run_agent(input_data: dict) -> dict:
    """Run the agent with the provided input data.

    Args:
        input_data: A dictionary containing business data for today and yesterday.

    Returns:
        A dictionary with recommendations and alerts.
    """
    initial_state = {"data": input_data}
    graph = build_graph()
    final_state = graph.invoke(initial_state)
    return final_state["recommendations"]

if __name__ == "__main__":
    sample_input = {
        "today": {"sales": 1000, "costs": 800, "customers": 50},
        "yesterday": {"sales": 900, "costs": 750, "customers": 45}
    }
    result = run_agent(sample_input)
    # Output: json.dumps(result, indent=2)