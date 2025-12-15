# Embedded Forecast Widget - Architecture

**Plugin:** nixtla-embedded-forecast-widget
**Version:** 0.1.0
**Last Updated:** 2025-12-15

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  PARTNER APPLICATION                                        │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  <ForecastWidget apiKey="..." theme="dark" />       │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  WIDGET COMPONENT (React/JS)                                │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │ Data         │  │ Chart        │  │ Controls        │   │
│  │ Uploader     │  │ Renderer     │  │ Panel           │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │ Theme        │  │ State        │  │ API             │   │
│  │ Provider     │  │ Manager      │  │ Client          │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
         │
         ▼ (HTTPS)
┌─────────────────────────────────────────────────────────────┐
│  WIDGET BACKEND (API Gateway)                               │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │ Auth         │  │ Rate         │  │ Usage           │   │
│  │ Middleware   │  │ Limiter      │  │ Metering        │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  NIXTLA SERVICES                                            │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │ TimeGPT      │  │ Billing      │  │ Partner         │   │
│  │ API          │  │ Service      │  │ Dashboard       │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Breakdown

### 1. Widget Frontend
- **Data Uploader**: CSV upload, drag-and-drop, API connector
- **Chart Renderer**: D3.js or Chart.js visualization
- **Controls Panel**: Horizon, confidence, settings
- **Theme Provider**: CSS-in-JS theming
- **State Manager**: React context for widget state
- **API Client**: Fetch wrapper with auth headers

### 2. Widget Backend
- **Auth Middleware**: Validate partner API keys
- **Rate Limiter**: Prevent abuse
- **Usage Metering**: Track forecasts per partner
- **Proxy**: Forward requests to TimeGPT

### 3. Partner Dashboard
- **Usage Stats**: Forecasts, revenue, trends
- **API Key Management**: Create, rotate keys
- **Billing**: View invoices, payment methods
- **Configuration**: Branding, default settings

---

## Widget Props API

```typescript
interface ForecastWidgetProps {
  // Required
  apiKey: string;

  // Data source
  dataSource?: 'csv' | 'api' | 'demo';
  apiEndpoint?: string;
  initialData?: TimeSeriesData;

  // Forecast settings
  horizon?: number;
  frequency?: 'H' | 'D' | 'W' | 'M';
  confidenceLevels?: number[];

  // Display
  theme?: 'light' | 'dark' | 'auto' | ThemeConfig;
  showBranding?: boolean;
  showControls?: boolean;
  showDownload?: boolean;

  // Chart
  chartType?: 'line' | 'area';
  showConfidenceBands?: boolean;
  enableZoom?: boolean;

  // Callbacks
  onForecast?: (result: ForecastResult) => void;
  onError?: (error: Error) => void;
  onDataLoad?: (data: TimeSeriesData) => void;

  // Styling
  className?: string;
  style?: React.CSSProperties;
}
```

---

## Theme Configuration

```typescript
interface ThemeConfig {
  // Colors
  primary: string;
  secondary: string;
  background: string;
  surface: string;
  text: string;
  textSecondary: string;

  // Chart colors
  lineColor: string;
  confidenceBandColor: string;
  gridColor: string;

  // Typography
  fontFamily: string;
  fontSize: {
    small: string;
    medium: string;
    large: string;
  };

  // Spacing
  borderRadius: string;
  padding: string;

  // Branding
  logo?: string;
  poweredBy?: boolean;
}
```

---

## Data Flow

1. **Initialize**: Widget loads with partner API key
2. **Upload**: User uploads CSV or connects API
3. **Validate**: Widget validates data format
4. **Request**: Widget sends data to backend proxy
5. **Auth**: Backend validates partner key
6. **Forecast**: Backend calls TimeGPT API
7. **Meter**: Backend records usage
8. **Respond**: Forecast returned to widget
9. **Render**: Widget displays chart

---

## Security Model

```
Partner App → Widget → Backend Proxy → TimeGPT

1. Partner API key (never exposed to end users)
2. Backend validates key, checks rate limits
3. Backend proxies to TimeGPT with Nixtla credentials
4. Usage metered for billing
```

- Partner keys: Scoped to widget only
- End user: No access to API keys
- Data: Processed in transit, not stored
- CORS: Configured per partner domain

---

## Bundle Structure

```
dist/
├── nixtla-forecast-widget.esm.js    # ES modules
├── nixtla-forecast-widget.cjs.js    # CommonJS
├── nixtla-forecast-widget.umd.js    # UMD (browser)
├── nixtla-forecast-widget.css       # Styles
├── types/
│   └── index.d.ts                   # TypeScript definitions
└── README.md
```

---

## Deployment Model

- **npm package**: Published to npm registry
- **CDN**: Also available via unpkg/jsdelivr
- **Backend**: Cloud Run or Lambda
- **Dashboard**: Hosted web app
