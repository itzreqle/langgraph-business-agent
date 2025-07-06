from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END

# Define state structures
class BusinessData(TypedDict):
    sales: float
    costs: float
    customers: int

class DailyData(TypedDict):
    today: BusinessData
    yesterday: BusinessData

class Metrics(TypedDict):
    profit_today: float
    profit_yesterday: float
    cac_today: float
    cac_yesterday: float
    sales_change: float
    cost_change: float

class Recommendations(TypedDict):
    profit_status: str
    alerts: list[str]
    recommendations: list[str]

class State(TypedDict):
    data: DailyData
    metrics: Optional[Metrics]
    recommendations: Optional[Recommendations]

# Input node: Validates the input data
def input_node(state: State) -> State:
    if not state.get("data") or not state["data"].get("today") or not state["data"].get("yesterday"):
        raise ValueError("Invalid input data: 'data' with 'today' and 'yesterday' required")
    return state

# Processing node: Calculates key business metrics
def processing_node(state: State) -> State:
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

# Recommendation node: Generates actionable advice
def recommendation_node(state: State) -> State:
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

# Build the LangGraph structure
def build_graph():
    graph = StateGraph(State)
    graph.add_node("input", input_node)
    graph.add_node("processing", processing_node)
    graph.add_node("recommendation", recommendation_node)
    
    graph.add_edge("input", "processing")
    graph.add_edge("processing", "recommendation")
    graph.add_edge("recommendation", END)
    
    graph.set_entry_point("input")
    
    return graph.compile()

# Run the agent with input data
def run_agent(input_data: dict) -> dict:
    initial_state = {"data": input_data}
    graph = build_graph()
    final_state = graph.invoke(initial_state)
    return final_state["recommendations"]

# Test the agent with sample data
if __name__ == "__main__":
    sample_input = {
        "today": {"sales": 1000, "costs": 800, "customers": 50},
        "yesterday": {"sales": 900, "costs": 750, "customers": 45}
    }
    result = run_agent(sample_input)
    import json
    print(json.dumps(result, indent=2))