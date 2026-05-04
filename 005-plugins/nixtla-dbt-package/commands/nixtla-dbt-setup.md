---
name: nixtla-dbt-setup
description: Set up Nixtla dbt package in your dbt project
---

# nixtla-dbt-setup

Set up the Nixtla dbt package for TimeGPT forecasting.

## Instructions

1. Add to packages.yml:
   ```yaml
   packages:
     - git: "https://github.com/jeremylongshore/plugins-nixtla.git"
       subdirectory: "005-plugins/nixtla-dbt-package"
   ```

2. Run `dbt deps` to install

3. Set environment variables:
   - `NIXTLA_API_KEY` - Your TimeGPT API key
   - `NIXTLA_ENVIRONMENT` - dev/staging/prod

4. Use macros in your models:
   - `{{ nixtla_forecast(table, horizon) }}`
   - `{{ nixtla_anomaly_detect(table) }}`
