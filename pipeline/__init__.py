"""
pipeline package

Contains clearly separated layers of the deterministic pipeline:

• input_layer
• processing_layer
• provenance_layer
• output_layer
• utils
• errors

Architectural Principle:
Layer responsibilities must remain isolated.
Cross-layer coupling is prohibited.
"""

__all__ = [
    "input_layer",
    "processing_layer",
    "provenance_layer",
    "output_layer",
    "utils",
    "errors",
]
