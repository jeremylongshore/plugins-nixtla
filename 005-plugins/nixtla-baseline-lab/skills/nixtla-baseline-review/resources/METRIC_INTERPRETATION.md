# Metric Interpretation Guide

## sMAPE (Symmetric Mean Absolute Percentage Error)

**Definition**: sMAPE measures the percentage error between forecasts and actual values, symmetrically treating over-predictions and under-predictions.

**Range**: 0% (perfect) to 200% (worst)

**Interpretation Scale**:
- **Excellent**: < 10% - Very accurate forecasts
- **Good**: 10-15% - Reliable for most business decisions
- **Acceptable**: 15-20% - Usable but requires caution
- **Poor**: > 20% - May not be suitable for critical decisions

**Practical Example**:
If you're forecasting daily sales of 100 units and get sMAPE of 12.3%, your forecast will typically be within ±12 units of the true value.

**M4 Benchmark Context**:
- M4-Daily: Anything under 15% is considered good performance
- M4-Monthly: Under 12% is typically good
- M4-Hourly: Under 8% is excellent (hourly data is often more volatile)

## MASE (Mean Absolute Scaled Error)

**Definition**: MASE measures forecast accuracy relative to a seasonal naive baseline (repeating the seasonal pattern from the training data).

**Interpretation**:
- **< 1.0**: Better than seasonal naive baseline
- **= 1.0**: Same as seasonal naive
- **> 1.0**: Worse than seasonal naive

**Practical Examples**:
- MASE of 0.85 = Model is 15% better than naive seasonal forecast
- MASE of 0.50 = Model is 50% better than naive seasonal forecast
- MASE of 1.20 = Model is 20% worse than naive seasonal forecast

**Season Length Context**:
MASE depends on the season_length parameter:
- Daily data with weekly pattern: season_length=7
- Monthly data with yearly pattern: season_length=12
- Hourly data with daily pattern: season_length=24

**When to Use MASE vs sMAPE**:
- **MASE**: Better for comparing models across different datasets or scales
- **sMAPE**: More interpretable for business stakeholders (percentage error)
- **Both**: Use both for comprehensive evaluation

## Model Performance Characteristics

### SeasonalNaive
- **How it works**: Repeats the seasonal pattern from training data
- **Strengths**: Simple, robust, no parameters to tune
- **Good for**: Stable series with clear seasonality
- **Limitations**: Cannot handle trends or pattern changes
- **Expected MASE**: Exactly 1.0 by definition (it's the baseline)

### AutoETS (Exponential Smoothing)
- **How it works**: State space exponential smoothing with automatic model selection
- **Strengths**: Handles trend + seasonality, robust to outliers
- **Good for**: Series with strong seasonal patterns and gradual trends
- **Limitations**: Can struggle with sudden shifts or long-term trends
- **Typical MASE**: 0.80-0.95 on M4-Daily

### AutoTheta
- **How it works**: Theta method with automatic parameter optimization
- **Strengths**: Excellent on M4 benchmarks, handles trends well
- **Good for**: Diverse patterns, especially with trends
- **Limitations**: Less interpretable than ETS
- **Typical MASE**: 0.75-0.90 on M4-Daily (often the winner)

## Summary Statistics Interpretation

### Mean vs Median
- **Mean**: Average performance across all series
- **Median**: Middle value (less affected by outliers)
- **When to prefer median**: When you have a few series with very high errors

### Standard Deviation
- **Low std dev (< 5% for sMAPE)**: Consistent performance across series
- **High std dev (> 10% for sMAPE)**: Model struggles on some series
- **Interpretation**: Lower is better - indicates robust performance

### Win Rate (Series Won)
- **Definition**: Count of series where a model has the lowest error
- **Interpretation**: Higher is better, but check margin of victory
- **Caveat**: A model that wins 60% of series by 0.1% isn't necessarily better than one that wins 40% by 5%

## Pattern Analysis Tips

### Identifying Model Strengths
- **Sort by MASE**: Find series where each model excels
- **Look for patterns**: Do certain models win on high/low seasonality?
- **Check failure cases**: Where do ALL models struggle? (sMAPE > 30%)

### Production Model Selection
1. **Default**: Use the model with lowest mean sMAPE AND lowest std dev
2. **Ensemble**: If models are close, consider averaging their forecasts
3. **Routing**: Use different models for different series types (requires analysis)

### Red Flags
- **All models > 20% sMAPE**: Data quality issue or high inherent uncertainty
- **MASE > 1.5 for sophisticated models**: Check data preprocessing
- **High std dev (> 15%)**: Model may be overfitting or data is heterogeneous
