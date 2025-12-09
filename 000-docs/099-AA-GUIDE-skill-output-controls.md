# Skill Output Controls Guide

**Created**: 2025-12-09
**Purpose**: Explains where skill outputs go and how users control them

---

## Output Control Methods

### Method 1: CLI Flags (Most Common)

**User controls output location via `--output` flag:**

```bash
# Example: Generate config
python scripts/generate_config.py \
    --data data/sales.csv \
    --target revenue \
    --horizon 30 \
    --freq D \
    --output /path/user/chooses/config.yml  ← USER CONTROLS THIS

# Example: Generate pipeline
python scripts/generate_pipeline.py \
    --config config.yml \
    --platform airflow \
    --output /home/user/pipelines/  ← USER CONTROLS THIS
```

**Where it goes**: Wherever the user specifies in `--output`

---

### Method 2: Console Output (Screen)

**Some scripts print to stdout (screen):**

```bash
# Prints to screen
python scripts/detect_environment.py

# Output appears on screen:
✓ statsforecast: 1.6.0
✓ mlforecast: 0.10.0
✓ nixtla: 0.5.1
```

**Where it goes**:
- **Screen (stdout)** by default
- **User can redirect**: `python script.py > output.txt`
- **User can pipe**: `python script.py | grep "error"`

---

### Method 3: Optional File Output

**Scripts with `--output` flag for optional file saving:**

```bash
# Without --output: prints to screen
python scripts/detect_environment.py --json

# With --output: saves to file
python scripts/detect_environment.py --json --output env.json
```

**Where it goes**: User chooses screen OR file

---

## Default Output Locations (When User Doesn't Specify)

### SKILL 1: nixtla-experiment-architect

```bash
# Default structure created in current directory:
./forecasting/
├── config.yml                 ← generate_config.py
├── experiments.py             ← scaffold_experiment.py
└── results/                   ← Created when experiments.py runs
    ├── metrics_summary.csv
    └── forecasts.csv
```

**User controls**:
- `--output forecasting/config.yml` → Can change to any path
- Current working directory determines where `forecasting/` appears

---

### SKILL 2: nixtla-prod-pipeline-generator

```bash
# User MUST specify --output:
python scripts/generate_pipeline.py \
    --output pipelines/  ← Required, user chooses

# Creates:
./pipelines/
├── forecast_dag.py
├── monitoring.py
├── README.md
└── requirements.txt
```

**User controls**: Required `--output` flag

---

### SKILL 3: nixtla-schema-mapper

```bash
# Default: Creates in current directory
./
├── mapping.json              ← analyze_schema.py
├── transform.py              ← generate_transform.py
├── NIXTLA_SCHEMA_CONTRACT.md ← create_contract.py

# User can override:
python scripts/analyze_schema.py --output /path/to/mapping.json
```

**User controls**: Optional `--output` overrides current directory

---

### SKILL 4: nixtla-timegpt-finetune-lab

```bash
# Default: Creates finetuning/ in current directory
./finetuning/
├── train.csv
├── val.csv
├── config.yml
├── artifacts/
│   └── job_metadata.json
└── comparison.csv

# User can override:
python scripts/prepare_finetune_data.py --output-dir /my/path/
```

**User controls**: `--output-dir` flag changes base directory

---

## How Users Redirect Output

### Redirect to File

```bash
# Capture screen output
python scripts/detect_environment.py > environment.txt

# Capture errors too
python scripts/generate_config.py 2>&1 > all_output.txt
```

### Pipe to Other Tools

```bash
# Search output
python scripts/detect_environment.py | grep "nixtla"

# Process with jq
python scripts/detect_environment.py --json | jq '.libraries'

# Count lines
python scripts/analyze_schema.py | wc -l
```

### Suppress Output

```bash
# Silent execution
python scripts/generate_config.py > /dev/null 2>&1

# Only show errors
python scripts/generate_config.py > /dev/null
```

---

## Output Type Reference

| Script | Default Output | User Control | Can Redirect? |
|--------|---------------|--------------|---------------|
| `generate_config.py` | File (--output required) | ✅ Required flag | N/A (writes file) |
| `scaffold_experiment.py` | File (--output required) | ✅ Required flag | N/A (writes file) |
| `validate_experiment.py` | Screen (stdout) | ❌ None | ✅ Yes |
| `generate_pipeline.py` | Directory (--output required) | ✅ Required flag | N/A (writes files) |
| `add_monitoring.py` | Modifies file in-place | ✅ --pipeline flag | N/A (modifies file) |
| `analyze_schema.py` | File (--output optional) | ✅ Optional flag | ✅ Yes (if no --output) |
| `generate_transform.py` | File (--output required) | ✅ Required flag | N/A (writes file) |
| `create_contract.py` | File (--output required) | ✅ Required flag | N/A (writes file) |
| `prepare_finetune_data.py` | Directory (--output-dir) | ✅ Optional flag | N/A (writes files) |
| `submit_finetune.py` | Directory (--output-dir) | ✅ Optional flag | ✅ Yes (also screen) |
| `monitor_finetune.py` | Screen (stdout) | ❌ None | ✅ Yes |
| `compare_finetuned.py` | Files + Screen | ✅ Config-based | ✅ Yes (screen part) |
| `evaluate.py` | File (--output required) | ✅ Required flag | N/A (writes file) |
| `detect_environment.py` | Screen (stdout) | ✅ Optional --output | ✅ Yes |

---

## Complete Example: User Controls Everything

```bash
# User chooses all paths
cd /home/user/my-project

# Step 1: Config goes where user wants
python /path/to/skills/scripts/generate_config.py \
    --data ./data/sales.csv \
    --output /tmp/experiment/config.yml  ← User's choice

# Step 2: Validation prints to screen (user can redirect)
python /path/to/skills/scripts/validate_experiment.py \
    --config /tmp/experiment/config.yml > validation.log  ← User's redirect

# Step 3: Experiment script goes where user wants
python /path/to/skills/scripts/scaffold_experiment.py \
    --config /tmp/experiment/config.yml \
    --output $HOME/experiments/run1.py  ← User's choice

# Step 4: Results go in forecasting/results/ by default
# BUT user can edit run1.py to change output paths
python $HOME/experiments/run1.py
```

---

## Key Principles

1. **User is in control**: Every file output has `--output` flag
2. **Current directory matters**: Relative paths start from `pwd`
3. **Screen output is flexible**: Users can redirect/pipe/suppress
4. **No surprises**: Scripts create directories as needed, don't fail silently
5. **Predictable**: Same command always produces same output structure

---

**Updated**: 2025-12-09
