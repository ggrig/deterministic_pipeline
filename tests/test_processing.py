"""
test_processing.py

Minimal tests validating:
• Processing layer independence
• Deterministic behavior
• No hidden state
"""

import unittest
from pipeline.processing_layer import process


class TestProcessingLayer(unittest.TestCase):

    def test_uppercase_transformation(self):
        raw_inputs = {
            "file.txt": b"hello world"
        }

        params = {
            "transform": "upper",
            "seed": 123
        }

        result = process(raw_inputs, parameters=params)

        self.assertEqual(result.items["file.txt"], b"HELLO WORLD")

    def test_deterministic_output(self):
        raw_inputs = {
            "file.txt": b"hello world"
        }

        params = {
            "transform": "upper",
            "seed": 123
        }

        result1 = process(raw_inputs, parameters=params)
        result2 = process(raw_inputs, parameters=params)

        self.assertEqual(result1.items, result2.items)


if __name__ == "__main__":
    unittest.main()
