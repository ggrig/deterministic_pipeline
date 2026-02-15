"""
provenance_layer.py

Provenance metadata generation layer.

Responsibilities:
• Construct structured provenance metadata
• Record:
    - Input hashes
    - Config hash
    - Pipeline version
    - Explicit parameters
    - Execution environment metadata
    - Timestamp (audit-only)

Architectural Constraints:
• Must not influence processing output
• Timestamp is for auditability only
• Determinism of artifacts must not depend on provenance

This layer documents execution without affecting results.
"""

import platform
import sys
import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict


@dataclass(frozen=True)
class Provenance:
    data: Dict[str, Any]


def _compute_run_id(
    *,
    input_hashes: Dict[str, str],
    config_hash: str,
    pipeline_version: str,
) -> str:
    """
    Deterministic run identifier derived from:
    • Input file hashes
    • Config hash
    • Pipeline version

    Does NOT include timestamp or environment.
    """
    h = hashlib.sha256()

    # Stable ordering
    for path in sorted(input_hashes.keys()):
        h.update(path.encode("utf-8"))
        h.update(input_hashes[path].encode("utf-8"))

    h.update(config_hash.encode("utf-8"))
    h.update(pipeline_version.encode("utf-8"))

    return h.hexdigest()


def build_provenance(
    *,
    input_hashes: Dict[str, str],
    config_hash: str,
    pipeline_version: str,
    parameters: Dict[str, Any],
) -> Provenance:

    ts = datetime.now(timezone.utc).isoformat()

    env = {
        "python_version": sys.version.split()[0],
        "platform": platform.platform(),
        "implementation": platform.python_implementation(),
    }

    run_id = _compute_run_id(
        input_hashes=input_hashes,
        config_hash=config_hash,
        pipeline_version=pipeline_version,
    )

    prov = {
        "run_id": run_id,
        "pipeline_version": pipeline_version,
        "timestamp_utc": ts,
        "inputs": [
            {"path": p, "sha256": h}
            for p, h in sorted(input_hashes.items())
        ],
        "config_sha256": config_hash,
        "parameters": parameters,
        "execution_environment": env,
        "deterministic_scope": "inputs + config + pipeline_version",
    }

    return Provenance(data=prov)
