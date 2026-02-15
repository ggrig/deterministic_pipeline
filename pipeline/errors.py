"""
errors.py

Centralized exception definitions for the pipeline.

Responsibilities:
• Define explicit error types for:
    - Input validation failures
    - Config validation failures
    - Pipeline-level failures

Architectural Constraints:
• No logic
• No side effects
• Used to enforce fail-fast behavior

All user-facing failures should be explicit and typed.
"""

class PipelineError(Exception):
    """Base exception for pipeline failures."""


class InputValidationError(PipelineError):
    """Raised when inputs are missing/invalid."""


class ConfigError(PipelineError):
    """Raised when config is missing/invalid."""
