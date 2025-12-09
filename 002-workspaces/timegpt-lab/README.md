# TimeGPT Lab

Experiments with Nixtla's TimeGPT (API usage, forecasting, anomaly detection, prompts). Prototyping workflows before 005-plugins/skills or production use. This workspace is the home base for TimeGPT engineers to design, validate, and refine TimeGPT-specific workflows.

## Structure

- **skills/** - TimeGPT-specific Claude Skills (prototypes for `nixtla-timegpt-*` family)
- **scripts/** - Python scripts for TimeGPT API experimentation (forecasting, anomaly detection, prompt engineering)
- **data/** - Sample datasets, API response caches, TimeGPT experiment data
- **reports/** - Generated markdown/HTML reports from TimeGPT experiments
- **docs/** - Internal guides, best practices, API usage patterns

## Example Future Flows

1. **Design and run TimeGPT experiments** on internal/sample time series
2. **Prototype new TimeGPT features** (e.g., anomaly detection with custom thresholds)
3. **Validate TimeGPT prompts** before packaging into skills-pack or plugins
4. **Benchmark TimeGPT** against StatsForecast baselines for specific domains
5. **Create golden datasets** for TimeGPT smoke tests and CI integration

## Cross-Lab Comparison

Compare TimeGPT results against StatsForecast baselines using the aggregator script:

```bash
# 1. Run TimeGPT experiments (this lab)
cd 002-workspaces/timegpt-lab
export NIXTLA_TIMEGPT_API_KEY='your_key_here'
python scripts/run_experiment.py

# 2. (Optional) Run StatsForecast baselines
cd ../statsforecast-lab
python scripts/run_statsforecast_baseline.py

# 3. Generate comparison report
cd /home/jeremy/000-projects/nixtla
python 004-scripts/compare_timegpt_vs_statsforecast.py
```

**Outputs**:
- CSV: `004-scripts/compare_outputs/timegpt_vs_statsforecast_metrics.csv`
- Report: `000-docs/091-RA-REPT-timegpt-vs-statsforecast-baseline.md`

The aggregator handles missing StatsForecast results gracefully (generates TimeGPT-only report with PENDING status). Re-run after StatsForecast baseline is generated to get full comparison.

## Environment Setup

```bash
export NIXTLA_TIMEGPT_API_KEY="your-api-key-here"
pip install nixtla utilsforecast
```

## Promotion Path

When a TimeGPT workflow is stable and validated:
- **Skills**: Promote to `003-skills/.claude/skills/nixtla-timegpt-*`
- **Scripts**: Integrate into `005-plugins/nixtla-timegpt-*/` (future MCP server)
- **Docs**: Extract best practices to `000-docs/` with proper NNN-CC-ABCD naming
