"""
output_layer.py

Output boundary of the pipeline.

Responsibilities:
• Write processed artifacts to disk
• Write human-readable provenance.json
• Ensure explicit and visible write behavior

Architectural Constraints:
• May perform file I/O
• Must not perform processing logic
• Must not compute hashes
• Must not mutate provenance structure

If any write fails, the run must fail explicitly.
No partial success marking.
"""


import json
from pathlib import Path
from typing import Dict

from .utils import canonical_json_dumps
from .processing_layer import ProcessedArtifact
from .provenance_layer import Provenance


def write_outputs(*, out_dir: str, processed: ProcessedArtifact, provenance: Provenance) -> Dict[str, str]:
    out_path = Path(out_dir).resolve()
    out_path.mkdir(parents=True, exist_ok=True)

    artifacts_dir = out_path / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    written = {}

    for input_path, content in sorted(processed.items.items()):
        name = Path(input_path).name
        out_file = artifacts_dir / f"{name}.processed"
        out_file.write_bytes(content)
        written[input_path] = str(out_file)

    prov_file = out_path / "provenance.json"
    prov_file.write_text(
        json.dumps(provenance.data, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    written["provenance"] = str(prov_file)

    return written
