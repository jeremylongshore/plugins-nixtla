# Embedded Forecast Widget - Technical Specification

**Plugin:** nixtla-embedded-forecast-widget
**Version:** 0.1.0
**Last Updated:** 2025-12-15

---

## Technology Stack

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Frontend | React 18 + TypeScript | Industry standard |
| Charts | D3.js or Recharts | Flexibility + SSR |
| Styling | CSS-in-JS (Emotion) | Theming support |
| Build | Rollup | Tree-shaking, small bundle |
| Backend | Cloud Run (Python) | Scalable proxy |
| Dashboard | Next.js | Fast partner portal |

---

## Widget API

### React Component

```typescript
import { ForecastWidget } from '@nixtla/forecast-widget';

// Basic usage
<ForecastWidget apiKey="pk_xxx" />

// Full configuration
<ForecastWidget
  apiKey="pk_xxx"
  dataSource="api"
  apiEndpoint="/api/sales-data"
  initialData={historicalData}
  horizon={30}
  frequency="D"
  confidenceLevels={[80, 95]}
  theme={customTheme}
  showBranding={false}
  showControls={true}
  showDownload={true}
  chartType="area"
  showConfidenceBands={true}
  enableZoom={true}
  onForecast={handleForecast}
  onError={handleError}
  onDataLoad={handleDataLoad}
  className="my-widget"
  style={{ height: 400 }}
/>
```

### Vanilla JavaScript

```html
<div id="forecast-widget"></div>
<script src="https://unpkg.com/@nixtla/forecast-widget"></script>
<script>
  NixtlaWidget.create('#forecast-widget', {
    apiKey: 'pk_xxx',
    horizon: 30,
    theme: 'dark'
  });
</script>
```

---

## TypeScript Definitions

```typescript
// Data types
interface TimeSeriesData {
  timestamps: string[];
  values: number[];
  metadata?: Record<string, any>;
}

interface ForecastResult {
  timestamps: string[];
  forecast: number[];
  confidence: {
    level: number;
    lower: number[];
    upper: number[];
  }[];
  metadata: {
    model: string;
    horizon: number;
    frequency: string;
    executionTime: number;
  };
}

// Events
interface WidgetEvents {
  onForecast: (result: ForecastResult) => void;
  onError: (error: WidgetError) => void;
  onDataLoad: (data: TimeSeriesData) => void;
  onThemeChange: (theme: ThemeConfig) => void;
}

// Error types
interface WidgetError {
  code: string;
  message: string;
  details?: Record<string, any>;
}
```

---

## Backend Proxy API

### Endpoint: POST /api/forecast

```json
// Request
{
  "partner_key": "pk_xxx",
  "data": {
    "timestamps": ["2024-01-01", "2024-01-02", ...],
    "values": [100, 105, ...]
  },
  "horizon": 30,
  "frequency": "D",
  "confidence_levels": [80, 95]
}

// Response
{
  "forecast": {
    "timestamps": ["2024-02-01", ...],
    "values": [110, 112, ...],
    "confidence": [
      {
        "level": 80,
        "lower": [105, 107, ...],
        "upper": [115, 117, ...]
      }
    ]
  },
  "usage": {
    "forecasts_used": 1,
    "remaining": 999
  }
}
```

### Authentication

```
Headers:
  X-Partner-Key: pk_xxx
  X-Widget-Version: 1.0.0
  X-Origin: https://partner-app.com
```

---

## Metering System

```python
# Usage tracking
class UsageTracker:
    def record_forecast(
        self,
        partner_id: str,
        widget_instance: str,
        data_points: int,
        horizon: int,
        timestamp: datetime
    ):
        """Record a forecast for billing."""
        self.db.insert({
            "partner_id": partner_id,
            "widget_instance": widget_instance,
            "data_points": data_points,
            "horizon": horizon,
            "timestamp": timestamp,
            "billed": False
        })

    def get_usage_summary(
        self,
        partner_id: str,
        start_date: date,
        end_date: date
    ) -> UsageSummary:
        """Get usage summary for billing period."""
        return self.db.aggregate(
            partner_id=partner_id,
            start=start_date,
            end=end_date
        )
```

---

## Bundle Optimization

```javascript
// rollup.config.js
export default {
  input: 'src/index.tsx',
  output: [
    { file: 'dist/widget.esm.js', format: 'esm' },
    { file: 'dist/widget.cjs.js', format: 'cjs' },
    { file: 'dist/widget.umd.js', format: 'umd', name: 'NixtlaWidget' }
  ],
  plugins: [
    typescript(),
    terser(),
    visualizer({ filename: 'bundle-stats.html' })
  ],
  external: ['react', 'react-dom']  // Peer dependencies
};
```

Target: <50KB gzipped (excluding peer deps)

---

## Performance Requirements

| Metric | Target |
|--------|--------|
| Bundle size | <50KB gzipped |
| Initial render | <500ms |
| Forecast request | <3s (p95) |
| Chart render | <100ms |

---

## Dependencies

```json
{
  "peerDependencies": {
    "react": ">=16.8.0",
    "react-dom": ">=16.8.0"
  },
  "dependencies": {
    "d3": "^7.8.0",
    "@emotion/react": "^11.11.0",
    "@emotion/styled": "^11.11.0"
  },
  "devDependencies": {
    "typescript": "^5.0.0",
    "rollup": "^4.0.0",
    "@types/react": "^18.0.0"
  }
}
```

---

## Directory Structure

```
nixtla-forecast-widget/
├── packages/
│   ├── widget/                 # React component
│   │   ├── src/
│   │   │   ├── components/
│   │   │   ├── hooks/
│   │   │   ├── themes/
│   │   │   └── index.tsx
│   │   ├── package.json
│   │   └── rollup.config.js
│   └── vanilla/               # Vanilla JS wrapper
├── backend/
│   ├── proxy/                 # API gateway
│   ├── metering/              # Usage tracking
│   └── dashboard/             # Partner portal
├── docs/
│   ├── getting-started.md
│   ├── api-reference.md
│   └── theming-guide.md
└── examples/
    ├── react-app/
    └── vanilla-html/
```
