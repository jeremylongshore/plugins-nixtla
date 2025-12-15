# Embedded Forecast Widget - Product Requirements Document

**Plugin:** nixtla-embedded-forecast-widget
**Version:** 0.1.0
**Status:** Planned
**Last Updated:** 2025-12-15

---

## Overview

A white-label React/JavaScript widget that SaaS companies embed in their applications. Users upload data or connect to sources, and the widget handles visualization, forecasting (via TimeGPT), and result display. Nixtla earns revenue share on every forecast.

---

## Problem Statement

SaaS companies want to add forecasting features to their products but lack ML expertise. Building forecasting from scratch takes 6-12 months. These companies would pay for a drop-in solution, but Nixtla's current offering requires significant integration effort.

---

## Goals

1. Drop-in React component: `npm install nixtla-forecast-widget`
2. Data connectors for CSV upload, REST API, database connections
3. Interactive visualization with confidence intervals
4. White-label styling with CSS theming
5. Built-in usage metering for revenue share calculations

## Non-Goals

- Replace full Nixtla API for power users
- Support non-JavaScript frameworks (Phase 1)
- On-premise deployment (Phase 1)

---

## Target Users

| User | Need |
|------|------|
| SaaS developers | Easy integration |
| Product managers | Quick feature addition |
| End users | Simple forecasting interface |
| Partners | Revenue opportunity |

---

## Functional Requirements

### FR-1: Drop-In Component
- npm package: `nixtla-forecast-widget`
- React component: `<ForecastWidget />`
- Vanilla JS version for non-React apps
- TypeScript support with full types

### FR-2: Data Connectors
- CSV file upload with drag-and-drop
- REST API connector (configurable endpoint)
- Database connectors (PostgreSQL, MySQL)
- Sample data for demos

### FR-3: Interactive Visualization
- Time series chart with Chart.js or D3
- Confidence interval bands
- Zoom and pan controls
- Download chart as PNG/SVG

### FR-4: White-Label Styling
- CSS theming system
- Remove/customize Nixtla branding
- Match host application design
- Dark/light mode support

### FR-5: Usage Metering
- Track forecasts per widget instance
- Report usage to Nixtla backend
- Partner dashboard for usage stats
- Billing integration

### FR-6: Configuration API
```jsx
<ForecastWidget
  apiKey="partner-key"
  theme="dark"
  dataSource="csv"
  horizon={14}
  confidenceLevels={[80, 95]}
  showBranding={false}
  onForecast={(result) => handleResult(result)}
/>
```

---

## Non-Functional Requirements

### NFR-1: Performance
- Widget load time: <2 seconds
- Forecast generation: <5 seconds
- Bundle size: <50KB gzipped

### NFR-2: Security
- API keys never exposed to browser
- Backend proxy for all API calls
- CORS configuration for partners

### NFR-3: Compatibility
- React 16.8+ (hooks support)
- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile responsive

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Partner integrations (Y1) | 20+ |
| End-user forecasts/month | 1M+ |
| Widget revenue share | 30% of TimeGPT revenue |
| Partner satisfaction | 4.5/5 |

---

## Pricing Model

| Tier | Price | Features |
|------|-------|----------|
| Free | 1,000 forecasts/month | Nixtla branding required |
| Growth | $0.01/forecast | White-label available |
| Enterprise | Volume discounts | Custom SLA, support |

Revenue share: Partners can mark up and resell, Nixtla gets base rate.

---

## Scope

### In Scope
- React widget component
- Vanilla JS wrapper
- CSV and API data sources
- Chart visualization
- White-label theming
- Usage metering

### Out of Scope (Phase 1)
- Vue/Angular native components
- On-premise deployment
- Offline mode
- Custom model training

---

## Technical Approach

- **React Component**: TypeScript, tree-shakeable, <50KB gzipped
- **Backend Proxy**: API gateway handles auth, metering, rate limiting
- **SDK Generation**: Also provide vanilla JS version for non-React apps

---

## Estimated Effort

10-12 weeks for production-ready widget with documentation and partner onboarding.

---

## Revenue Impact

Direct and scalable. Partner distribution multiplies Nixtla's reach.
- Y1: $50-100K
- Y2: $200-500K (as partner network grows)
