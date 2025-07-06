"""Unit tests for the LangGraph agent's configuration and functionality."""

import unittest
from agent.graph import run_agent

class TestConfiguration(unittest.TestCase):
    def test_run_agent_configuration(self):
        """Test the agent's run_agent function with sample input."""
        input_data = {
            "today": {"sales": 1000, "costs": 800, "customers": 50},
            "yesterday": {"sales": 900, "costs": 750, "customers": 45}
        }
        result = run_agent(input_data)
        self.assertEqual(result["profit_status"], "Profit: $200.00")
        self.assertIn("Consider increasing advertising budget due to 11.11% sales growth", result["recommendations"])

if __name__ == "__main__":
    unittest.main()