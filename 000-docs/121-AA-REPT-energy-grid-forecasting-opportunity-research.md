# 121-AA-REPT: Energy Grid Forecasting Opportunity Research

**Date**: 2026-01-03 21:35 CST
**Author**: Jeremy Longshore
**Status**: Research Complete - Pending Review

---

## Executive Summary

- Investigated combining US power transmission infrastructure visualization with Nixtla forecasting
- **Finding**: Nixtla already has extensive energy forecasting tutorials and a production customer (GridStor)
- **Opportunity**: The geo-visualization overlay (forecasts on transmission maps) does NOT exist
- Potential plugin concept: Real-time grid forecasting dashboard with congestion prediction
- Next step: Decide whether to prototype or deprioritize

---

## Scope

### What Was Investigated

- GitHub Gist: [US Electric Power Transmission Lines visualization](https://gist.github.com/walkerke/a214c8aabec0e87ac8044085254eef19) (R/maplibre)
- Nixtla's existing energy forecasting capabilities
- Public grid data sources (EIA, ERCOT, PJM, CAISO)
- Market opportunity / whitespace

### What Was NOT Investigated

- Actual implementation feasibility
- Licensing/data usage restrictions
- Competitive landscape (other energy forecasting tools)

---

## Research Findings

### 1. Source Visualization (Walker's Gist)

An R script creating interactive map of US electrical transmission infrastructure:
- **Data source**: HIFLD (Homeland Infrastructure Foundation-Level Data) via ArcGIS REST API
- **Features**: 700k+ miles of transmission lines, color-coded by voltage (100kV to 735kV+)
- **Tech**: maplibre for interactive rendering, dynamic line widths, glowing effects
- **Purpose**: 30-day mapping challenge entry (Day 26: Transport)

### 2. Nixtla's Existing Energy Forecasting

**Already well-covered territory:**

| Resource | Description | Link |
|----------|-------------|------|
| Electricity Load Forecast | PJM hourly data with MSTL model | [Tutorial](https://nixtlaverse.nixtla.io/statsforecast/docs/tutorials/electricityloadforecasting.html) |
| Electricity Peak Forecasting | ERCOT (Texas) peak detection | [Notebook](https://github.com/Nixtla/statsforecast/blob/main/nbs/docs/tutorials/ElectricityPeakForecasting.ipynb) |
| Energy Demand (TimeGPT) | PJM 5-region forecasting | [Use Case](https://www.nixtla.io/docs/use_cases/forecasting_energy_demand) |

**Production Customer: GridStor**
- Portland-based battery energy storage company
- **Problem**: $20k/month AWS costs, 25%+ forecast error with ARIMA
- **Solution**: TimeGPT for electricity price forecasting
- **Results**: Seconds instead of hours, significantly improved accuracy
- **Use case**: Optimize when to store vs sell energy
- [Case Study](https://www.nixtla.io/success-stories/gridstor)

**Performance Benchmarks (from Nixtla docs)**:
- TimeGPT vs N-HiTS: 90% faster, 7.8% better MAE
- statsforecast MSTL vs Prophet: 26% more accurate, 2x faster
- statsforecast SeasonalNaive vs NeuralProphet: 20% more accurate, 366x faster

### 3. Public Data Sources Identified

| Source | Data Available | Granularity | API |
|--------|----------------|-------------|-----|
| EIA Open Data | Regional demand, generation by fuel | Hourly | Yes (free) |
| ERCOT | Real-time LMP, load, wind/solar | 5-min to hourly | Yes (free) |
| PJM | Nodal prices, congestion, demand | 5-min to hourly | Yes (free) |
| CAISO | California grid data, OASIS | Hourly | Yes (free) |
| NOAA | Weather (demand driver) | Hourly | Yes (free) |

### 4. The Whitespace (What Doesn't Exist)

Nixtla's tutorials output **dataframes and CSVs**. There is no:

1. **Geo-visualization layer** - Forecasts overlaid on transmission infrastructure
2. **Congestion prediction** - Which transmission corridors will bottleneck
3. **Interactive dashboard** - Real-time updates with forecast confidence intervals
4. **Multi-region comparison** - Side-by-side regional forecasts on map

**This is the potential plugin opportunity.**

---

## Potential Plugin Concept

### Name: `nixtla-grid-forecaster` or `nixtla-energy-dashboard`

### Features (Hypothetical)

1. **Data Ingestion**
   - Pull real-time ERCOT/PJM/CAISO data via public APIs
   - Historical data for training window

2. **Forecasting Engine**
   - TimeGPT for primary forecasts (fast, accurate)
   - statsforecast MSTL as baseline comparison
   - 24-72 hour horizons with confidence intervals

3. **Visualization**
   - Transmission line map (from HIFLD data)
   - Color-coded forecast overlays (predicted load by region)
   - Congestion hotspot indicators
   - Anomaly detection alerts

4. **Outputs**
   - Interactive web dashboard
   - Slack/email alerts for anomalies
   - CSV exports for downstream analysis

### Technical Stack (If Built)

- **Backend**: Python (Nixtla SDK, pandas, requests)
- **Visualization**: Plotly/Dash or Observable/D3.js
- **Map**: maplibre-gl or Deck.gl
- **Data**: ERCOT API (Texas - isolated grid, good starting point)

---

## Risks / Unknowns

| Risk | Mitigation |
|------|------------|
| Already exists elsewhere | Competitive research needed |
| Data API rate limits | May need caching layer |
| Visualization complexity | Start with static maps, add interactivity later |
| Scope creep | MVP = one region (ERCOT) + one forecast type (load) |
| Business value unclear | Target audience: energy traders, grid operators, researchers |

---

## Options

### Option A: Prototype (2-3 days)

Build minimal working demo:
1. ERCOT hourly load data (last 30 days)
2. TimeGPT 48-hour forecast
3. Static map with regional overlays
4. Jupyter notebook deliverable

**Pros**: Tangible output, validates feasibility
**Cons**: Time investment, may not lead anywhere

### Option B: Document & Deprioritize

Create detailed PRD, add to backlog, revisit when:
- Client interest emerges
- Nixtla partnership opportunity
- Energy sector outreach

**Pros**: Zero time investment now
**Cons**: Loses momentum, idea may go stale

### Option C: Pitch to Nixtla

Share concept with Nixtla team as potential:
- Case study collaboration
- Featured community project
- Co-marketing opportunity

**Pros**: External validation, potential support
**Cons**: Gives away idea, depends on their interest

---

## Next Actions

1. [ ] **DECISION NEEDED**: Which option (A/B/C)?
2. [ ] If Option A: Create beads task for prototype sprint
3. [ ] If Option B: Create PRD in `000-docs/000a-planned-plugins/`
4. [ ] If Option C: Draft outreach email to Nixtla team

---

## References

- [Walker's Transmission Lines Gist](https://gist.github.com/walkerke/a214c8aabec0e87ac8044085254eef19)
- [HIFLD Electric Power Transmission Lines](https://hifld-geoplatform.opendata.arcgis.com/datasets/electric-power-transmission-lines)
- [Nixtla Energy Demand Tutorial](https://www.nixtla.io/docs/use_cases/forecasting_energy_demand)
- [Nixtla ERCOT Peak Forecasting](https://github.com/Nixtla/statsforecast/blob/main/nbs/docs/tutorials/ElectricityPeakForecasting.ipynb)
- [GridStor Case Study](https://www.nixtla.io/success-stories/gridstor)
- [ERCOT Data API](http://www.ercot.com/gridinfo)
- [EIA Open Data](https://www.eia.gov/opendata/)

---

intent solutions io — confidential IP
Contact: jeremy@intentsolutions.io
