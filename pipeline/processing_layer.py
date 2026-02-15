"""
processing_layer.py

Pure deterministic processing layer.

Responsibilities:
• Transform raw input bytes using explicit parameters
• Contain only pure functions
• Be independently callable without orchestration

Architectural Constraints:
• No file I/O
• No timestamps
• No environment inspection
• No global state
• No hidden defaults
• No implicit randomness

Function signature defines full behavior:
(raw_inputs, parameters) -> processed artifacts

This module must remain environment-agnostic and deterministic.
"""


from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class ProcessedArtifact:
    items: Dict[str, bytes]


def _transform_bytes(data: bytes, transform: str) -> bytes:
    if transform == "noop":
        return data
    text = data.decode("utf-8", errors="strict")
    if transform == "upper":
        return text.upper().encode("utf-8")
    if transform == "lower":
        return text.lower().encode("utf-8")
    raise ValueError(f"Unsupported transform: {transform}")


def process(raw_inputs: Dict[str, bytes], *, parameters: Dict[str, object]) -> ProcessedArtifact:
    if "transform" not in parameters:
        raise ValueError("Missing parameter: transform")
    if "seed" not in parameters:
        raise ValueError("Missing parameter: seed")

    transform = parameters["transform"]

    processed = {
        path: _transform_bytes(data, transform)
        for path, data in raw_inputs.items()
    }
    return ProcessedArtifact(items=processed)
