"""Unit tests for the LangGraph agent's graph functionality."""

import unittest
from agent.graph import run_agent

class TestBusinessAgent(unittest.TestCase):
    def test_profit_and_sales_growth(self):
        """Test profit calculation and sales growth recommendation."""
        input_data = {
            "today": {"sales": 1000, "costs": 800, "customers": 50},
            "yesterday": {"sales": 900, "costs": 750, "customers": 45}
        }
        result = run_agent(input_data)
        self.assertEqual(result["profit_status"], "Profit: $200.00")
        self.assertEqual(len(result["alerts"]), 0)
        self.assertIn("Consider increasing advertising budget due to 11.11% sales growth", result["recommendations"])

    def test_loss_scenario(self):
        """Test loss scenario and cost reduction recommendation."""
        input_data = {
            "today": {"sales": 700, "costs": 800, "customers": 50},
            "yesterday": {"sales": 900, "costs": 750, "customers": 45}
        }
        result = run_agent(input_data)
        self.assertEqual(result["profit_status"], "Loss: $100.00")
        self.assertEqual(len(result["alerts"]), 0)
        self.assertIn("Reduce costs to improve profitability", result["recommendations"])

    def test_cac_increase(self):
        """Test CAC increase detection and marketing review recommendation."""
        input_data = {
            "today": {"sales": 1000, "costs": 800, "customers": 40},
            "yesterday": {"sales": 900, "costs": 750, "customers": 50}
        }
        result = run_agent(input_data)
        self.assertEqual(result["profit_status"], "Profit: $200.00")
        self.assertIn("CAC increased by 33.33%, which is significant.", result["alerts"])
        self.assertIn("Review marketing campaigns for efficiency", result["recommendations"])
        self.assertIn("Consider increasing advertising budget due to 11.11% sales growth", result["recommendations"])

    def test_invalid_input(self):
        """Test handling of invalid input data."""
        input_data = {}
        with self.assertRaises(ValueError):
            run_agent(input_data)

if __name__ == "__main__":
    unittest.main()