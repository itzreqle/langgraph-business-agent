# LangGraph Business Agent

[![CI](https://github.com/langchain-ai/new-langgraph-project/actions/workflows/unit-tests.yml/badge.svg)](https://github.com/langchain-ai/new-langgraph-project/actions/workflows/unit-tests.yml)  
[![Integration Tests](https://github.com/langchain-ai/new-langgraph-project/actions/workflows/integration-tests.yml/badge.svg)](https://github.com/langchain-ai/new-langgraph-project/actions/workflows/integration-tests.yml)

This project is a simple AI agent built using [LangGraph](https://github.com/langchain-ai/langgraph). The agent analyzes daily business data, such as sales and costs, and generates a summary report with actionable recommendations. It is designed to help businesses make informed decisions based on their daily performance. The project leverages [LangGraph Server](https://langchain-ai.github.io/langgraph/concepts/langgraph_server/#langgraph-server) and [LangGraph Studio](https://langchain-ai.github.io/langgraph/concepts/langgraph_studio/), a visual debugging IDE, to build, run, and debug the agent.

![Graph view in LangGraph studio UI](./static/studio_ui.png)

## Overview

The AI agent is implemented in `src/agent/graph.py` and consists of a graph with three nodes:

1. **Input Node**: Receives business data as a Python dictionary or JSON object, validating that it contains the required fields for today’s and yesterday’s data (e.g., sales, costs, customers).
2. **Processing Node**: Calculates key metrics such as profit (sales - costs), customer acquisition cost (CAC = costs / customers), and percentage changes in sales and costs compared to the previous day.
3. **Recommendation Node**: Analyzes the calculated metrics and generates actionable recommendations, such as reducing costs if profit is negative or increasing the marketing budget if sales grew significantly.

The agent outputs a dictionary or JSON object containing the profit/loss status, any alerts or warnings, and decision-making recommendations. Example output:

```json
{
  "profit_status": "Profit: $200.00",
  "alerts": [],
  "recommendations": [
    "Consider increasing advertising budget due to 11.11% sales growth"
  ]
}
```

## Getting Started

### Prerequisites

- Python 3.8+
- Git

### Setup Instructions

1. Clone the repository:
    
    ```bash
    git clone https://github.com/itzreqle/langgraph-business-agent.git
    ```
    
2. Navigate to the project directory:
    
    ```bash
    cd langgraph-business-agent
    ```
    
3. Create a virtual environment:
    
    ```bash
    python3 -m venv langgraph-env
    ```
    
4. Activate the virtual environment:
    
    ```bash
    source langgraph-env/bin/activate  # On Windows: langgraph-env\Scripts\activate
    ```
    
5. Install dependencies, including the [LangGraph CLI](https://langchain-ai.github.io/langgraph/concepts/langgraph_cli/):
    
    ```bash
    pip install -e . "langgraph-cli[inmem]"
    ```
    
6. (Optional) Create a `.env` file for secrets, such as a LangSmith API key for tracing:
    
    ```bash
    cp .env.example .env
    ```
    
    Edit `.env` to include:
    
    ```text
    LANGSMITH_API_KEY=lsv2...
    ```
    

### Running the Agent

- Run the agent directly:
    
    ```bash
    python src/agent/graph.py
    ```
    
- Or start the LangGraph Server for development and debugging:
    
    ```bash
    langgraph dev
    ```
    

For more details on using LangGraph Server, see the [LangGraph Server tutorial](https://langchain-ai.github.io/langgraph/tutorials/langgraph-platform/local-server/).

## Graph Structure

The graph, defined in `src/agent/graph.py`, consists of three nodes:

- **Input Node**: Ensures the input data is valid and structured correctly.
- **Processing Node**: Performs calculations like profit, CAC, and percentage changes in performance metrics.
- **Recommendation Node**: Uses predefined conditions to generate advice, such as warnings for high CAC or suggestions for budget adjustments.

You can visualize and debug this graph in LangGraph Studio, where local changes are hot-reloaded automatically.

## Testing

The project includes unit and integration tests to validate the agent’s functionality. Run them with:

- Unit tests:
    
    ```bash
    python -m unittest tests/unit_tests/test_graph.py
    ```
    
- Integration tests:
    
    ```bash
    python -m unittest tests/integration_tests/test_graph.py
    ```
    

All tests should pass, confirming the agent works as expected.

## How to Customize

1. **Modify Configurable Parameters**: Update the `Configuration` class in `src/agent/graph.py` to expose new parameters (e.g., custom thresholds for recommendations). See [Lang -][https://langchain-ai.github.io/langgraph/concepts/low_level/?h=configuration#configuration](https://langchain-ai.github.io/langgraph/concepts/low_level/?h=configuration#configuration)) for details.
2. **Extend the Graph**: Edit `src/agent/graph.py` to add nodes, edges, or adjust the logic. For example, add a node for trend analysis or tweak recommendation conditions.

For advanced examples, refer to the [LangGraph documentation](https://langchain-ai.github.io/langgraph/).

## Development with LangGraph Studio

- Edit past states and rerun the app from any point to debug specific nodes.
- Local changes are applied via hot reload.
- Start a new thread with the `+` button in LangGraph Studio to clear history.

Integrate with [LangSmith](https://smith.langchain.com/) for detailed tracing and collaboration.