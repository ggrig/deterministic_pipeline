"""
input_layer.py

Input boundary of the pipeline.

Responsibilities:
• Validate input file paths
• Load and validate configuration
• Enforce explicit parameter schema (no hidden defaults)
• Compute deterministic SHA256 hashes for:
    - Raw input files
    - Canonicalized config

Architectural Constraints:
• May perform I/O (file reads)
• Must not perform processing transformations
• Must not write outputs
• Must fail fast on invalid input

This layer establishes deterministic input identity.
"""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

from .errors import ConfigError, InputValidationError
from .utils import sha256_file, sha256_json


@dataclass(frozen=True)
class LoadedInputs:
    input_paths: List[Path]
    input_hashes: Dict[str, str]
    config: Dict[str, Any]
    config_hash: str
    pipeline_version: str


def _validate_paths(paths: List[Path]) -> None:
    if not paths:
        raise InputValidationError("No input files provided.")
    for p in paths:
        if not p.exists():
            raise InputValidationError(f"Input file does not exist: {p}")
        if not p.is_file():
            raise InputValidationError(f"Input path is not a file: {p}")


def _load_config(config_path: Path) -> Dict[str, Any]:
    if not config_path.exists():
        raise ConfigError(f"Config file does not exist: {config_path}")
    if not config_path.is_file():
        raise ConfigError(f"Config path is not a file: {config_path}")

    try:
        raw = config_path.read_text(encoding="utf-8")
        cfg = json.loads(raw)
    except Exception as e:
        raise ConfigError(f"Failed to parse config as JSON: {e}") from e

    if not isinstance(cfg, dict):
        raise ConfigError("Config must be a JSON object.")

    required_keys = ["transform", "seed"]
    missing = [k for k in required_keys if k not in cfg]
    if missing:
        raise ConfigError(f"Missing required config keys: {missing}")

    if cfg["transform"] not in ("upper", "lower", "noop"):
        raise ConfigError('config.transform must be "upper", "lower", or "noop"')

    if not isinstance(cfg["seed"], int):
        raise ConfigError("config.seed must be an integer")

    return cfg


def load_validate_hash(input_files: List[str], config_file: str, pipeline_version: str) -> LoadedInputs:
    if not pipeline_version.strip():
        raise InputValidationError("pipeline_version must be non-empty")

    paths = [Path(p).resolve() for p in input_files]
    _validate_paths(paths)

    cfg_path = Path(config_file).resolve()
    cfg = _load_config(cfg_path)

    input_hashes = {str(p): sha256_file(p) for p in paths}
    config_hash = sha256_json(cfg)

    return LoadedInputs(
        input_paths=paths,
        input_hashes=input_hashes,
        config=cfg,
        config_hash=config_hash,
        pipeline_version=pipeline_version.strip(),
    )
