# TimeGPT Showdown Guide

## Overview

The **TimeGPT showdown** is an optional comparison feature that evaluates Nixtla's hosted foundation model (TimeGPT) against open-source statsforecast baselines on a small sample of series.

## When TimeGPT Comparison is Available

**Files to check**:
- `timegpt_showdown_M4_Daily_h{horizon}.txt` - Detailed showdown summary report
- `timegpt_status` field in tool response JSON

**Activation**:
- User must enable: `include_timegpt=true` when running baselines
- Requires: `NIXTLA_TIMEGPT_API_KEY` environment variable
- Requires: `nixtla` SDK installed (`pip install nixtla`)

## How to Interpret TimeGPT Results

### When timegpt_status.success == True

**What to do**:
1. Read the showdown file using Read or Bash tool
2. Note the comparison scope (typically 3-5 series for cost/time constraints)
3. Compare TimeGPT to the best statsforecast model (AutoETS, AutoTheta, SeasonalNaive)
4. Use metrics from `timegpt_status`: avg_smape, avg_mase, comparison deltas

**Response template**:
```markdown
## TimeGPT Comparison (Limited Sample)

Tested on {N} series (subset for cost/time constraints):
- **TimeGPT avg sMAPE**: {X.XX}%
- **Best baseline avg sMAPE**: {Y.YY}% ({ModelName})
- **Winner on this subset**: {WINNER}
- **Delta**: TimeGPT is {Z.Z}% {better/worse} than best baseline

⚠️ **Important**: This is an illustrative comparison on a small sample, not a full benchmark.
TimeGPT performance may vary significantly on the complete dataset.

**Key Insights**:
- {Insight about relative performance}
- {Insight about where TimeGPT excels or struggles}
- {Recommendation about when to consider TimeGPT}
```

### When timegpt_status.success == False

**Reasons** (from `timegpt_status.reason`):
- `missing_api_key`: NIXTLA_TIMEGPT_API_KEY environment variable not set
- `sdk_not_installed`: nixtla SDK not installed (pip install nixtla)
- `api_error`: TimeGPT API call failed (network, auth, or service issue)
- `disabled`: TimeGPT not requested (include_timegpt=False)

**Response template**:
```markdown
TimeGPT comparison was not run.

**Reason**: {timegpt_status.reason}

**To enable TimeGPT showdown**:
1. Install nixtla SDK: `pip install nixtla`
2. Set API key: `export NIXTLA_TIMEGPT_API_KEY=your_key_here`
3. Run baselines with: `include_timegpt=true`

For now, the analysis focuses on statsforecast baselines (SeasonalNaive, AutoETS, AutoTheta).
```

## Important Reminders

### Scope and Limitations
- **Small sample size**: Typically 3-5 series (not comprehensive benchmark)
- **Cost constraint**: TimeGPT is a paid API, so testing is limited
- **Directional insights**: Results are indicative, not conclusive
- **Series selection**: Usually the first N series from the dataset

### Language to Use
- **Good**: "indicative", "illustrative", "limited comparison", "on this subset"
- **Avoid**: "conclusive", "comprehensive", "proven", "always better"

### When to Emphasize TimeGPT
- User explicitly asks about TimeGPT performance
- TimeGPT shows significant performance difference (> 5% sMAPE delta)
- User is evaluating TimeGPT for production use

### When NOT to Mention TimeGPT
- TimeGPT was not run (timegpt_status.success == False)
- User only asks about baseline comparisons
- Showdown results are similar (< 2% sMAPE delta)

## Example User Prompts

**"How did TimeGPT perform compared to AutoETS?"**
- Check timegpt_status first
- If success, compare metrics and note sample size
- If failure, explain why and how to enable

**"Why was TimeGPT skipped?"**
- Check timegpt_status.reason
- Explain the specific reason (API key, SDK, disabled)
- Provide instructions to enable if user wants it

**"What would I need to enable TimeGPT showdown?"**
- List prerequisites: API key, SDK installation
- Show example command: `include_timegpt=true`
- Note that it's optional and has no impact on default behavior

**"Is TimeGPT better than the baselines on this dataset?"**
- If showdown exists, provide careful comparison
- Emphasize limited series count
- Avoid overgeneralizing from small sample

## Technical Details

### What TimeGPT Is
- **Official**: Nixtla's hosted foundation model for time series forecasting
- **Access**: Requires API key (paid service)
- **Not statsforecast**: Separate product from the open-source statsforecast library
- **Use case**: Zero-shot forecasting without training, good for diverse patterns

### What the Showdown Tests
- **Same series**: Uses identical train/test split as baselines
- **Same horizon**: Forecasts same number of steps ahead
- **Same metrics**: sMAPE and MASE for direct comparison
- **Limited series**: Typically 3-5 series to control API costs

### Response JSON Structure
```json
{
  "timegpt_status": {
    "success": true,
    "avg_smape": 10.23,
    "avg_mase": 0.85,
    "series_evaluated": 3,
    "reason": null
  },
  "timegpt_per_series": [
    {"series_id": "D1", "smape": 9.5, "mase": 0.82},
    {"series_id": "D2", "smape": 11.0, "mase": 0.88}
  ]
}
```

## Production Guidance

### When to Recommend TimeGPT
- User needs zero-shot forecasting (no training)
- User has diverse patterns across many series
- User wants to test state-of-the-art foundation model
- Results show TimeGPT significantly outperforms baselines (> 10% improvement)

### When to Recommend Baselines
- User wants full control and transparency
- User needs offline/on-premise deployment
- User has stable patterns where baselines perform well
- Cost is a primary concern (statsforecast is free)

### Hybrid Approach
- Use baselines for most series (cheap, fast, transparent)
- Route difficult series to TimeGPT (detected via high baseline errors)
- Ensemble: Average TimeGPT and best baseline for robustness

## Never Fabricate TimeGPT Data

**Critical rule**: If timegpt_status doesn't exist or success == False, DO NOT:
- Invent TimeGPT metrics
- Speculate about what TimeGPT "would probably" achieve
- Compare to TimeGPT without actual results

**Instead**:
- Focus analysis on statsforecast baselines
- Explain how to enable TimeGPT if user asks
- Be honest: "TimeGPT comparison not available for this run"
