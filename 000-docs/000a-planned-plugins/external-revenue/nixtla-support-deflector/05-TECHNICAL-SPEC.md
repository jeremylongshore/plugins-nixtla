# Support Deflector - Technical Specification

**Plugin:** nixtla-support-deflector
**Version:** 0.1.0
**Last Updated:** 2025-12-15

---

## Technology Stack

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Runtime | Python 3.10+ | Nixtla ecosystem compatibility |
| MCP Server | FastAPI + MCP SDK | Standard plugin architecture |
| Vector Store | ChromaDB | Local-first, easy setup |
| Embeddings | OpenAI ada-002 | Cost-effective, high quality |
| LLM | Claude/GPT-4 | Response generation |
| Database | SQLite | Metadata storage |

---

## API Specification

### MCP Tools

#### 1. `ingest_tickets`
```json
{
  "name": "ingest_tickets",
  "description": "Import tickets from configured sources",
  "inputSchema": {
    "type": "object",
    "properties": {
      "source": {
        "type": "string",
        "enum": ["github", "intercom", "email", "all"]
      },
      "since": {
        "type": "string",
        "description": "ISO datetime to fetch tickets from"
      },
      "limit": {
        "type": "integer",
        "default": 100
      }
    }
  }
}
```

#### 2. `draft_response`
```json
{
  "name": "draft_response",
  "description": "Generate response draft for a ticket",
  "inputSchema": {
    "type": "object",
    "properties": {
      "ticket_id": {
        "type": "string",
        "description": "Ticket identifier (e.g., github:1234)"
      },
      "include_sources": {
        "type": "boolean",
        "default": true
      }
    },
    "required": ["ticket_id"]
  }
}
```

#### 3. `categorize_ticket`
```json
{
  "name": "categorize_ticket",
  "description": "Classify ticket type and priority",
  "inputSchema": {
    "type": "object",
    "properties": {
      "ticket_id": {
        "type": "string"
      }
    },
    "required": ["ticket_id"]
  }
}
```

#### 4. `get_patterns`
```json
{
  "name": "get_patterns",
  "description": "Retrieve recurring issue patterns",
  "inputSchema": {
    "type": "object",
    "properties": {
      "days": {
        "type": "integer",
        "default": 14
      },
      "min_occurrences": {
        "type": "integer",
        "default": 3
      }
    }
  }
}
```

#### 5. `generate_digest`
```json
{
  "name": "generate_digest",
  "description": "Create weekly summary report",
  "inputSchema": {
    "type": "object",
    "properties": {
      "period": {
        "type": "string",
        "enum": ["daily", "weekly", "monthly"],
        "default": "weekly"
      },
      "format": {
        "type": "string",
        "enum": ["text", "json", "markdown"],
        "default": "markdown"
      }
    }
  }
}
```

---

## Data Models

### Ticket Schema
```python
@dataclass
class Ticket:
    id: str                    # Unique identifier
    source: str                # github, intercom, email
    external_id: str           # Source-specific ID
    title: str
    body: str
    author: str
    created_at: datetime
    status: str                # open, resolved, escalated
    category: Optional[str]    # faq, bug, feature, doc_gap
    confidence: Optional[float]
    embedding: Optional[List[float]]
```

### Response Draft Schema
```python
@dataclass
class ResponseDraft:
    ticket_id: str
    content: str
    confidence: float          # 0.0 - 1.0
    sources: List[str]         # Documentation URLs used
    similar_tickets: List[str] # Related resolved tickets
    auto_resolve: bool         # True if confidence > 0.9
```

---

## Configuration

```yaml
# config.yaml
sources:
  github:
    enabled: true
    repo: "nixtla/nixtla"
    labels: ["question", "help wanted"]
  intercom:
    enabled: false
    workspace_id: ""
  email:
    enabled: false
    imap_server: ""
    inbox: "support"

rag:
  embedding_model: "text-embedding-ada-002"
  chunk_size: 1000
  chunk_overlap: 200
  similarity_threshold: 0.75

auto_resolve:
  enabled: true
  confidence_threshold: 0.9
  require_approval: true

notifications:
  slack_webhook: ""
  notify_on_escalation: true
```

---

## Performance Requirements

| Metric | Target |
|--------|--------|
| Draft generation | <5 seconds |
| Ticket ingestion | 100 tickets/minute |
| Pattern analysis | Real-time |
| Vector search | <100ms |

---

## Security Considerations

- API tokens stored in `.env` file (never committed)
- No customer PII in logs
- Audit trail for all auto-responses
- Rate limiting on MCP endpoints
- Input sanitization for all ticket content

---

## Dependencies

```txt
# requirements.txt
fastapi>=0.100.0
uvicorn>=0.23.0
chromadb>=0.4.0
openai>=1.0.0
anthropic>=0.5.0
pygithub>=2.0.0
pydantic>=2.0.0
python-dotenv>=1.0.0
```

---

## Directory Structure

```
nixtla-support-deflector/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   └── support-deflector.md
├── scripts/
│   ├── mcp_server.py
│   ├── ingestion.py
│   ├── rag_engine.py
│   ├── pattern_analyzer.py
│   └── digest_generator.py
├── data/
│   ├── tickets.db          # SQLite metadata
│   └── chroma/             # Vector store
├── config.yaml
├── requirements.txt
└── README.md
```
