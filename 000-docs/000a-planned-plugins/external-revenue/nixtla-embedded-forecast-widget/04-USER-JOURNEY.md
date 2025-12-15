# Embedded Forecast Widget - User Journey

**Plugin:** nixtla-embedded-forecast-widget
**Version:** 0.1.0
**Last Updated:** 2025-12-15

---

## Persona: SaaS Developer

**Name:** David
**Role:** Full-stack Developer at a B2B SaaS company
**Pain Point:** Product team wants forecasting feature, but building ML is outside expertise

---

## Journey Map

### Stage 1: Discovery
**Trigger:** Product manager asks for demand forecasting in the analytics dashboard

**Actions:**
- David researches forecasting options
- Finds: build from scratch (6+ months), hire ML team ($$$), or use API
- Discovers Nixtla widget: drop-in component

**Outcome:** Decides to try the widget

---

### Stage 2: Quick Start
**Trigger:** David evaluates the widget

**Actions:**
```bash
# Install the widget
npm install @nixtla/forecast-widget

# Add to React component
```

```jsx
import { ForecastWidget } from '@nixtla/forecast-widget';

function AnalyticsDashboard() {
  return (
    <div className="dashboard">
      <h2>Demand Forecast</h2>
      <ForecastWidget
        apiKey="demo-key"
        dataSource="csv"
        horizon={30}
        theme="light"
      />
    </div>
  );
}
```

**Outcome:** Working prototype in 30 minutes

---

### Stage 3: Integration
**Trigger:** David integrates with company's data

**Actions:**
```jsx
import { ForecastWidget } from '@nixtla/forecast-widget';

function CustomerDashboard({ customerId }) {
  const handleForecast = (result) => {
    // Save to customer's dashboard
    saveToDatabase(customerId, result);
    showNotification('Forecast generated!');
  };

  return (
    <ForecastWidget
      apiKey={process.env.NIXTLA_PARTNER_KEY}
      dataSource="api"
      apiEndpoint={`/api/customers/${customerId}/sales-data`}
      horizon={90}
      confidenceLevels={[80, 95]}
      theme={{
        primary: '#4F46E5',  // Company brand color
        fontFamily: 'Inter, sans-serif',
      }}
      showBranding={false}  // White-label
      onForecast={handleForecast}
      onError={(err) => logError(err)}
    />
  );
}
```

**Outcome:** Branded widget integrated with company data

---

### Stage 4: Customization
**Trigger:** Design team wants widget to match brand

**Actions:**
```jsx
const brandTheme = {
  primary: '#4F46E5',
  secondary: '#10B981',
  background: '#FFFFFF',
  surface: '#F9FAFB',
  text: '#111827',
  textSecondary: '#6B7280',
  lineColor: '#4F46E5',
  confidenceBandColor: 'rgba(79, 70, 229, 0.2)',
  fontFamily: 'Inter, sans-serif',
  borderRadius: '8px',
};

<ForecastWidget
  apiKey={apiKey}
  theme={brandTheme}
  showBranding={false}
  className="custom-forecast-widget"
/>
```

**CSS Override:**
```css
.custom-forecast-widget {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border: 1px solid #E5E7EB;
}

.custom-forecast-widget .chart-container {
  min-height: 400px;
}
```

**Outcome:** Widget looks native to the application

---

### Stage 5: Production Launch
**Trigger:** Feature goes live to customers

**Actions:**
1. Upgrade to Growth tier ($0.01/forecast)
2. Enable white-label mode
3. Set up usage monitoring
4. Configure billing alerts

**Dashboard View:**
```
Partner Dashboard: Acme Analytics
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This Month:
- Forecasts: 45,234
- Revenue: $452.34
- Active end users: 1,247

Usage Trend: ↑ 23% vs last month

API Keys:
- Production: pk_live_xxxx (Active)
- Staging: pk_test_xxxx (Active)
```

**Outcome:** Feature live, Nixtla earning revenue share

---

### Stage 6: End User Experience
**Trigger:** Customer uses the forecasting feature

**End User View:**
```
┌─────────────────────────────────────────────────┐
│  Sales Forecast                            ⚙️   │
├─────────────────────────────────────────────────┤
│                                                 │
│    📈 [Interactive Chart]                       │
│    - Historical data (solid line)              │
│    - Forecast (dashed line)                    │
│    - 80% confidence band (light shading)       │
│    - 95% confidence band (lighter shading)     │
│                                                 │
├─────────────────────────────────────────────────┤
│  Forecast Horizon: [14 days ▼]                 │
│  Confidence Level: [80% ▼] [95% ▼]             │
│                                                 │
│  [Generate Forecast]  [Download CSV]           │
└─────────────────────────────────────────────────┘
```

**Outcome:** End users get forecasting without knowing Nixtla exists

---

## Success Scenario

- Integration time: 6 months → 2 days
- Development cost: $50K+ → $500/month
- Feature quality: ML-grade forecasting
- David: Hero to the product team
- Nixtla: Passive revenue from every forecast
