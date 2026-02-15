# Deterministic Pipeline Skeleton (v1 Trial)

A minimal, clean pipeline structure demonstrating:

• Explicit inputs and parameters  
• Deterministic hashing (inputs + config)  
• Pure processing functions (no I/O)  
• Provenance recording (`provenance.json`)  
• Clear separation of concerns and fail-fast behavior  

## Project structure

• `run.py` — thin orchestration entrypoint (arg parsing + wiring)  
• `pipeline/input_layer.py` — load/validate/hash inputs + config  
• `pipeline/processing_layer.py` — pure processing functions only (no I/O)  
• `pipeline/provenance_layer.py` — provenance metadata generation  
• `pipeline/output_layer.py` — writes artifacts and `provenance.json`  
• `examples/` — sample inputs and config  

## Prerequisites

Before running the pipeline, ensure the following:

• Python 3.9+ installed  
• Access to a shell or terminal  
• No external Python packages required (standard library only)   

To verify your Python version:

```
python3 --version
```

Expected output:

```
Python 3.x.x
```

The pipeline has been designed to:

• Avoid third-party dependencies  
• Run in isolated virtual environments  
• Produce deterministic behavior across supported Python versions  

## Virtual environment setup

From the project root:

```bash
python3 -m venv .venv
```

Activate:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

Dependencies:

• This project uses only the Python standard library (no installs required).  
• Optional: upgrade pip

```bash
python -m pip install --upgrade pip
```

## Run examples

### Uppercase Transformation

```bash
python run.py \
  --inputs examples/input1.txt \
  --config examples/config_upper.json \
  --version v1.0.0 \
  --out out_upper
```

Behavior:

• All text converted to uppercase  
• Deterministic output bytes  
• Provenance records transform=upper  

### Lowercase Transformation

```bash
python run.py \
  --inputs examples/input1.txt \
  --config examples/config_lower.json \
  --version v1.0.0 \
  --out out_lower
```

Behavior:

• All text converted to lowercase  
• Same input + different config ⇒ different artifact  
• Different config hash recorded in provenance  

### No-Op Transformation

```bash
python run.py \
  --inputs examples/input1.txt \
  --config examples/config_noop.json \
  --version v1.0.0 \
  --out out_noop
```

Behavior:

• Output identical to input bytes  
• Still fully hashed and recorded  
• Demonstrates structural determinism independent of transformation  

### Outputs:

• `out/artifacts/input1.txt.processed`  
• `out/provenance.json`  

### Multiple input files:

```bash
python run.py \
  --inputs examples/input1.txt examples/input2.txt \
  --config examples/config_upper.json \
  --version v1.0.0 \
  --out out_multi
```

Note: the pipeline accepts one or more file paths. Use distinct files in real runs.

### Missing Input File

```bash
python run.py \
  --inputs examples/does_not_exist.txt \
  --config examples/config_upper.json \
  --version v1.0.0 \
  --out out_invalid
```

Expected behavior:

• Exit with non-zero status  
• Print explicit error:  

```
PIPELINE ERROR: Input file does not exist: ...
```

## Determinism guarantees

The processed artifact bytes are deterministic given identical:

• input file bytes  
• config content  
• pipeline version  
• processing code  

Determinism is enforced by:

• SHA256 over raw input bytes (input layer)  
• Canonical JSON hashing of config (sorted keys, stable separators)  
• Pure processing functions (no filesystem, no time, no globals)  
• No hidden defaults (config requires explicit keys)  
• No randomness (a `seed` parameter is still required explicitly and recorded)  

`provenance.json` includes timestamp/environment metadata for auditability; those fields are expected to differ across runs and do not affect artifact determinism.

## Where scale / infrastructure would go later (not implemented)

This structure leaves clear extension points without changing processing purity:

• Orchestration: replace `run.py` with a queue/worker runner  
• Input/output: swap local filesystem for object storage  
• Provenance: add git commit SHA, container image digest, run IDs, dataset identifiers  

## AI / LLM-assisted coding constraints

LLMs can accelerate implementation inside strict boundaries:

• Human-defined invariants: layer separation, determinism rules, parameter schema, provenance schema  
• LLM-allowed work: boilerplate inside a single layer, helper functions with direct tests  
• Mandatory human review: anything that changes determinism, parameters/defaults, or provenance semantics  

## Unit Tests

The processing layer is independently testable and contains no I/O or orchestration dependencies.

A minimal test file is provided:

```
tests/test_processing.py
```

It validates:

• Processing logic is callable without run.py  
• Deterministic behavior (identical inputs + parameters ⇒ identical outputs)  
• No hidden state or side effects  

Running Tests

From the project root:

```
python -m unittest discover -s tests
```

No external testing framework is required.
Tests use Python’s built-in unittest module.