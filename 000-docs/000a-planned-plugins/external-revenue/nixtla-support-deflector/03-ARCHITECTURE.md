# Support Deflector - Architecture

**Plugin:** nixtla-support-deflector
**Version:** 0.1.0
**Last Updated:** 2025-12-15

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  TICKET SOURCES                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │ GitHub       │  │ Intercom     │  │ Email           │   │
│  │ Issues API   │  │ Webhooks     │  │ IMAP Parser     │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│  INGESTION LAYER                                            │
│  - Normalize ticket format                                  │
│  - Extract metadata (user, timestamp, category)             │
│  - Queue for processing                                     │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  RAG ENGINE                                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Vector Store (ChromaDB)                             │   │
│  │  - Nixtla documentation embeddings                   │   │
│  │  - Historical ticket embeddings                      │   │
│  │  - Resolution patterns                               │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  LLM Processing                                      │   │
│  │  - Response generation                               │   │
│  │  - Categorization                                    │   │
│  │  - Pattern extraction                                │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  MCP SERVER (5 tools)                                       │
│  ┌────────────┐ ┌────────────┐ ┌────────────────────────┐  │
│  │ ingest_    │ │ draft_     │ │ categorize_ticket      │  │
│  │ tickets    │ │ response   │ │                        │  │
│  └────────────┘ └────────────┘ └────────────────────────┘  │
│  ┌────────────┐ ┌────────────────────────────────────────┐ │
│  │ get_       │ │ generate_digest                        │ │
│  │ patterns   │ │                                        │ │
│  └────────────┘ └────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  OUTPUT LAYER                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │ Draft        │  │ Weekly       │  │ Slack           │   │
│  │ Responses    │  │ Digests      │  │ Notifications   │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Breakdown

### 1. Ticket Ingestion Service
- **GitHub Connector**: Poll GitHub Issues API, filter by labels
- **Intercom Connector**: Webhook receiver for new conversations
- **Email Connector**: IMAP polling for support inbox
- **Normalizer**: Convert all sources to unified ticket schema

### 2. RAG Engine
- **Document Loader**: Ingest Nixtla docs (statsforecast, nixtla, mlforecast)
- **Embedding Service**: Generate embeddings via OpenAI/Cohere
- **Vector Store**: ChromaDB for similarity search
- **Response Generator**: LLM-powered draft creation

### 3. Pattern Analyzer
- **Clustering**: Group similar tickets
- **Categorizer**: Classify as FAQ/Bug/Feature/Doc Gap
- **Trend Detector**: Identify emerging patterns

### 4. MCP Server
- FastAPI-based MCP server
- 5 exposed tools for Claude Code integration
- JSON-RPC protocol

---

## Data Flow

1. **Ingest**: Tickets arrive from GitHub/Intercom/Email
2. **Normalize**: Convert to standard schema
3. **Embed**: Generate vector embedding for ticket
4. **Search**: Find similar docs and resolved tickets
5. **Draft**: Generate response using context
6. **Route**: Auto-resolve or escalate based on confidence
7. **Learn**: Store resolution for future pattern matching

---

## Integration Points

| System | Integration Type | Purpose |
|--------|------------------|---------|
| GitHub Issues | REST API | Ticket source |
| Intercom | Webhooks | Ticket source |
| Email | IMAP | Ticket source |
| ChromaDB | Local/Cloud | Vector storage |
| OpenAI/Anthropic | API | LLM processing |
| Slack | Webhooks | Notifications |

---

## Deployment Model

- **Local Development**: Docker Compose with ChromaDB
- **Production**: Cloud Run + managed vector DB
- **Data**: SQLite for metadata, ChromaDB for embeddings
