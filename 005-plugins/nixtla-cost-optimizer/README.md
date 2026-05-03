# Nixtla Cost Optimizer

Real cost optimization for Nixtla TimeGPT customers. Feed it your API call records, get back ranked optimization recommendations with USD savings estimates, simulate batching impact, generate a hybrid TimeGPT + statsforecast routing strategy, and export the whole thing as a markdown/JSON/CSV report.

**Version**: 1.0.0 · **Status**: Working · **API key needed**: None (pure local computation on call records)

---

## 30-second pitch

Nixtla customers see a TimeGPT bill they want to cut. This plugin reads their actual call records, detects the four biggest cost drivers (small batches, redundant calls, single-series calls, short-horizon calls), and returns concrete, ranked, USD-quantified recommendations they can hand to their data team — including a routing function (real Python code) for hybrid TimeGPT + statsforecast deployment.

---

## Quick start

```bash
cd 005-plugins/nixtla-cost-optimizer
pip install -r scripts/requirements.txt

# In Claude Code:
# "Analyze my TimeGPT API usage from this list of calls and recommend optimizations."
# Claude calls analyze_usage → recommend_optimizations → simulate_batching →
# generate_hybrid_strategy → export_report.
```

Inputs: a list of API call records. Each record may carry:

```json
{
  "series_count": 12,
  "horizon": 30,
  "freq": "D",
  "model": "timegpt-1",
  "input_hash": "sha-of-input-payload",
  "series_ids": ["sales_north", "sales_south"]
}
```

---

## What you get back

`analyze_usage` returns:

```json
{
  "total_calls": 1500,
  "total_series": 18420,
  "avg_series_per_call": 12.28,
  "estimated_monthly_cost_usd": 1.842,
  "cost_per_1k_series": 0.10,
  "opportunities": [
    {"type": "batching",            "description": "...", "potential_savings_pct": 35},
    {"type": "caching",             "description": "...", "potential_savings_pct": 12},
    {"type": "hybrid_short_horizon","description": "...", "potential_savings_pct": 8}
  ],
  "n_opportunities": 3
}
```

`recommend_optimizations` consumes that and returns:

```json
{
  "recommendations": [
    {
      "id": "rec_001",
      "category": "batching",
      "title": "Aggregate small calls into batches",
      "description": "...",
      "estimated_savings_pct": 35,
      "estimated_savings_usd_per_month": 0.65,
      "implementation_effort": "medium",
      "implementation_steps": ["...", "..."],
      "validation_criteria": ["...", "..."]
    }
  ],
  "total_estimated_savings_pct": 55,
  "total_estimated_savings_usd_per_month": 1.01,
  "current_monthly_cost_usd": 1.84
}
```

Sorted by USD savings descending. Capped at 95% total to avoid the compound-savings illusion.

`simulate_batching` projects post-batching call counts and overhead-driven savings. `generate_hybrid_strategy` returns real Python code for a `route_forecast(metadata) -> "timegpt" | "statsforecast"` decision function plus a JSON config of the routing rules. `export_report` composes everything into markdown / JSON / CSV.

---

## Detection heuristics

| Pattern | Trigger | Recommendation |
|---|---|---|
| **Batching** | >30% of calls have <10 series | Aggregate in 60-second windows up to 100 series/call |
| **Caching** | >5% of payload signatures repeat | Hash (input, horizon, freq, model); store with TTL |
| **Single-series** | >40% of calls forecast a single series | Group by (freq, horizon), use multi-series endpoint |
| **Short-horizon hybrid** | >20% of calls have horizon ≤ 3 | Route those to statsforecast (free, faster) |

Payload signature is `sha256(input_hash, series_ids, horizon, freq, model)`'s first 16 hex chars — captures whether two calls would compute the same result.

---

## Hybrid strategy decision logic

The generated `route_forecast` function uses these rules in order:

1. `horizon >= 14` → TimeGPT (long horizons benefit most from foundation models)
2. `has_exog == True` → TimeGPT (exogenous variables)
3. `history_length < 100 OR sparse_history == True` → TimeGPT (statsforecast struggles)
4. Otherwise → statsforecast (faster, deterministic, free)

Thresholds tune based on the `usage_profile` you pass in:
- `accuracy_critical: True` → lowers `timegpt_horizon_threshold` (more goes to TimeGPT)
- `latency_sla_seconds < 1.0` → raises threshold (real-time SLA pushes more to statsforecast)

---

## Tests

```bash
cd 005-plugins/nixtla-cost-optimizer
PYTHONPATH=scripts pytest tests/ --cov=cost_optimizer_mcp -v
```

30 tests covering payload signatures, usage analysis (with synthetic fixtures triggering each pattern), recommendations sorting + savings math + 95%-cap, batching simulation, hybrid strategy thresholds (accuracy-critical lowers, real-time SLA raises), report generation in all three formats (markdown / json / csv), and async MCP dispatch.

---

## License

MIT — Jeremy Longshore.
