"""
utils.py

Shared deterministic utilities.

Responsibilities:
• Provide SHA256 hashing helpers
• Provide canonical JSON serialization for stable hashing

Architectural Constraints:
• Must remain deterministic
• No side effects
• No I/O beyond file hashing helpers
• No business logic

Canonical JSON encoding is used strictly for hashing stability.
Human-readable JSON formatting is handled elsewhere.
"""

import hashlib
import json
from pathlib import Path
from typing import Any


def sha256_bytes(data: bytes) -> str:
    h = hashlib.sha256()
    h.update(data)
    return h.hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_json_dumps(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_json(obj: Any) -> str:
    return sha256_bytes(canonical_json_dumps(obj).encode("utf-8"))
