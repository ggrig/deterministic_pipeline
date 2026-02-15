"""
run.py

Thin orchestration entrypoint for the deterministic pipeline.

Responsibilities:
• Parse CLI arguments
• Invoke input, processing, provenance, and output layers
• Own all I/O side effects (file reads/writes)
• Fail fast with explicit exit codes

Architectural Constraints:
• No business logic
• No processing logic
• No hashing logic
• No provenance logic

This file wires layers together but must not contain domain behavior.
Processing remains independently callable without this module.
"""


import argparse
import sys
from pathlib import Path

from pipeline.errors import PipelineError
from pipeline.input_layer import load_validate_hash
from pipeline.processing_layer import process
from pipeline.provenance_layer import build_provenance
from pipeline.output_layer import write_outputs


def _read_inputs(paths):
    return {str(p): Path(p).read_bytes() for p in paths}


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", nargs="+", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)

    try:
        loaded = load_validate_hash(args.inputs, args.config, args.version)

        raw_inputs = _read_inputs(loaded.input_paths)

        processed = process(raw_inputs, parameters=loaded.config)

        provenance = build_provenance(
            input_hashes=loaded.input_hashes,
            config_hash=loaded.config_hash,
            pipeline_version=loaded.pipeline_version,
            parameters=loaded.config,
        )

        write_outputs(out_dir=args.out, processed=processed, provenance=provenance)

        print("Run successful.")
        return 0

    except PipelineError as e:
        print(f"PIPELINE ERROR: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"UNEXPECTED ERROR: {e}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
