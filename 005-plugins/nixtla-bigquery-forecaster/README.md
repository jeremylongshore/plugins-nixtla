# Nixtla BigQuery Forecaster

> **What it is**: Run Nixtla statsforecast models on BigQuery data via Cloud Functions
> **Why it exists**: Showcase what's possible with Claude Code plugins + Nixtla + Google Cloud
> **Who it's for**: Anyone who wants to forecast BigQuery time series data

---

## 2-Minute Demo

Uses **PUBLIC** Chicago taxi data (200M+ rows). Zero setup on your end.

### Step 1: Deploy
GitHub Actions handles everything. Just push to main.

### Step 2: Test
```bash
curl -X POST "https://YOUR-FUNCTION-URL" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "bigquery-public-data",
    "dataset": "chicago_taxi_trips",
    "table": "taxi_trips",
    "timestamp_col": "trip_start_timestamp",
    "value_col": "trip_total",
    "group_by": "payment_type",
    "horizon": 7,
    "limit": 1000,
    "source_project": "bigquery-public-data"
  }'
```

### Step 3: Get Results
- Forecasts for next 7 days
- AutoETS + AutoTheta models (official Nixtla statsforecast)
- Payment types: Cash, Credit Card, Mobile, etc.

Example output:
```json
{
  "status": "success",
  "metadata": {
    "rows_read": 210,
    "unique_series": 7,
    "forecast_points_generated": 49
  },
  "forecasts": [
    {
      "unique_id": "Cash",
      "ds": "2023-02-01",
      "AutoETS": 69918.06,
      "AutoTheta": 56865.52
    }
  ]
}
```

---

## What This Shows

✅ **Nixtla OSS works great on massive datasets** (we tested with 100K+ rows)
✅ **Serverless deployment is easy** (Cloud Functions auto-scale)
✅ **Real-world data, real-world use case** (not toy examples)

---

## Ideas for Max

Could this become:
- Customer demo for "Nixtla + BigQuery"?
- Internal tool for testing statsforecast at scale?
- Template for building Nixtla integrations?
- Proof point for Google Cloud partnerships?

**We don't know. Just sharing what we built.**

---

## Technical Details

**Models Used:**
- AutoETS (Exponential smoothing)
- AutoTheta (Theta method)
- SeasonalNaive (baseline)
- Optional: TimeGPT (if API key provided)

**Libraries:**
```
statsforecast==2.0.3      # Official Nixtla OSS
nixtla==0.7.1             # TimeGPT client
google-cloud-bigquery     # BigQuery connector
```

**Infrastructure:**
- Cloud Functions (Gen2, Python 3.12)
- BigQuery API
- GitHub Actions deployment
- Workload Identity Federation (keyless auth)

**Cost:**
- ~$0.01 per forecast run
- Free tier covers moderate usage

---

## Try It

1. **Setup**: See `GCP-SETUP-COMPLETE.md` for deployment instructions
2. **Test Locally**:
   ```bash
   cd plugins/nixtla-bigquery-forecaster
   source .venv/bin/activate
   python test_local.py
   ```
3. **Deploy**: Push to main branch (GitHub Actions deploys automatically)

---

## Files

```
plugins/nixtla-bigquery-forecaster/
├── src/
│   ├── main.py                  # Cloud Function entry point
│   ├── bigquery_connector.py    # BigQuery data reader/writer
│   └── forecaster.py            # Nixtla statsforecast wrapper
├── 000-docs/
│   ├── 001-DR-REFR-google-timeseries-insights-api.md
│   ├── 002-DR-QREF-max-quick-start-guide.md
│   └── 003-AT-ARCH-plugin-architecture.md
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

---

## What We Learned

Building this plugin validated:
- Nixtla statsforecast handles 100K+ rows easily
- BigQuery public datasets are great for demos
- Cloud Functions deployment is straightforward
- AutoETS and AutoTheta are production-ready

---

**Built with**: Nixtla statsforecast, Google Cloud, Claude Code
**Time to build**: 48 hours
**Status**: Working demo, tested with real data
