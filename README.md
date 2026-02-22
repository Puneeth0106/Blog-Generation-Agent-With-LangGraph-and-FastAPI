# Blog Agent — AI-Powered Blog Generation System

**Multi-Language Content Automation** | **LangGraph Orchestration + FastAPI + OpenAI**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.128-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![LangGraph](https://img.shields.io/badge/LangGraph-1.0-FF6B35?style=flat)](https://langchain-ai.github.io/langgraph/)
[![LangChain](https://img.shields.io/badge/LangChain-1.2-1C3C3C?style=flat)](https://langchain.com)
[![Deployed on Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-000000?style=flat&logo=vercel&logoColor=white)](https://vercel.com)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

An end-to-end autonomous content generation system that takes a topic and produces a fully structured, SEO-optimised blog post — translated into any of **6 languages** — through a **4-node LangGraph state machine**, served via a **FastAPI REST API** with a live web frontend deployed on **Vercel**.

**Live Demo →** [blog-agent on Vercel](https://blog-agent-gdo1g8xjf-puneeth0106s-projects.vercel.app/)

---

## What It Does — In Numbers

| Metric | Value |
|---|---|
| Minimum blog length | **500+ words** per generation |
| Languages supported | **6** (English, Spanish, French, German, Telugu, Swahili) |
| LangGraph nodes in pipeline | **4** (title → content → router → translation) |
| Graph execution modes | **2** (topic-only / language-aware) |
| API endpoints | **2** (`GET /` frontend, `POST /blogs`) |
| LLM providers supported | **2** (OpenAI GPT-4o-mini, Groq Llama 3.3-70B) |
| Lines of application code | **< 250** across the entire `src/` package |

---

## Architecture

### System Data Flow

```
Client Request  →  POST /blogs  { topic, language? }
                        │
                   app.py selects graph mode
                   based on presence of "language"
                        │
            ┌───────────┴────────────┐
            │                        │
      Topic Mode               Language Mode
  (3-node graph)             (4-node graph)
            │                        │
            └───────────┬────────────┘
                        │
              ┌─────────▼──────────┐
              │  title_creation    │  LLM generates SEO-optimised
              │  _node             │  markdown title from topic
              └─────────┬──────────┘
                        │
              ┌─────────▼──────────┐
              │  content_generation│  LLM writes 500+ word
              │  _node             │  structured markdown blog
              └─────────┬──────────┘
                        │
              ┌─────────▼──────────┐   (Language Mode only)
              │  language_router   │  Conditional edge — routes
              │  _node             │  to correct translation node
              └──┬──┬──┬──┬──┬───┘   or exits if English
                 │  │  │  │  │
              ES FR DE TE SW END
                 │  │  │  │  │
              ┌──▼──▼──▼──▼──▼──┐
              │  translation     │  Translates content preserving
              │  _node(language) │  tone, structure & markdown
              └─────────┬────────┘
                        │
              ┌─────────▼──────────┐
              │  JSON Response     │  { data: { topic, blog:
              │                    │    { title, content } } }
              └────────────────────┘
```

### Two Graph Modes

```
Topic Graph:     START → title_creation → content_generation → END

Language Graph:  START → title_creation → content_generation
                              → language_router ──┬── spanish_node ──┐
                                                  ├── french_node   ──┤
                                                  ├── german_node   ──┤→ END
                                                  ├── telugu_node   ──┤
                                                  ├── swahili_node  ──┘
                                                  └── END (if english)
```

### Shared State Shape

```python
Blogstate = {
    "topic":            str,   # user input
    "blog":             Blog,  # { title: str, content: str }
    "language_content": str,   # target language (optional)
}
```

State flows immutably through every node — each node receives the full state and returns only the fields it modifies.

---

## Key Engineering Decisions

### 1. LangGraph for Stateful Orchestration
Rather than chaining LLM calls imperatively, the pipeline is modelled as a **directed acyclic graph**. LangGraph manages state transitions, conditional routing, and execution order. This makes the pipeline easy to extend (adding a new language is 3 lines: new node, new edge, new router branch) and trivial to debug in LangGraph Studio.

### 2. Two Separate Graphs, Not One Fat Graph
A simpler design would be a single graph with an optional translation branch. Instead, two distinct graphs are compiled at request time based on whether a `language` field is present. This keeps graph complexity low and avoids dead nodes for the majority of requests.

### 3. LLM Abstraction Layer
The `LLM` class in `src/llms/llm.py` exposes `openaillm()` and `groqllm()` factory methods. Swapping the underlying model requires **zero changes** to any node or graph — only the factory call in `app.py` changes.

### 4. Pydantic State Validation
The `Blog` model is a Pydantic `BaseModel`. Every node that writes to `blog` produces a validated, type-safe object. Invalid LLM outputs fail fast at the state boundary rather than causing silent downstream errors.

---

## Tech Stack

### AI / ML
| Library | Version | Role |
|---|---|---|
| LangGraph | 1.0.7 | State machine graph orchestration |
| LangChain | 1.2.7 | LLM interface & prompt management |
| OpenAI GPT-4o-mini | — | Primary content generation model |
| Groq Llama 3.3-70B | — | Alternative LLM provider |
| LangSmith | 0.6.4 | Tracing & observability (optional) |

### Backend
| Library | Version | Role |
|---|---|---|
| FastAPI | 0.128 | Async REST API framework |
| Pydantic | 2.12 | Data validation & state typing |
| Uvicorn | 0.40 | ASGI server |
| python-dotenv | 1.2 | Environment configuration |

### Frontend & Deployment
| Tool | Role |
|---|---|
| Vanilla JS + Tailwind CSS | Responsive single-page frontend |
| Marked.js | Markdown → HTML rendering |
| highlight.js | Code block syntax highlighting |
| Vercel | Serverless deployment (Python 3.12 runtime) |

---

## Project Structure

```
Blog-Agent/
├── app.py                      # FastAPI entrypoint — graph selection, route handlers
├── frontend/
│   └── index.html              # Single-page frontend (Tailwind + Marked.js)
├── src/
│   ├── graphs/
│   │   └── graph_builder.py    # Graph_builder class — compiles both graph modes
│   ├── llms/
│   │   └── llm.py              # LLM factory — OpenAI & Groq providers
│   ├── nodes/
│   │   └── blog_node.py        # All 4 node functions + 5 translation nodes
│   └── states/
│       └── blogstate.py        # Blogstate TypedDict + Blog Pydantic model
├── langgraph.json              # LangGraph Studio config → points at graph_builder:graph
├── pyproject.toml              # Dependencies (uv lockfile)
├── vercel.json                 # Vercel build config
└── .python-version             # Pins Python 3.12 for Vercel runtime
```

---

## Local Setup

### Prerequisites
- Python 3.12+
- OpenAI API key (or Groq API key)

### 1. Clone & install

```bash
git clone https://github.com/Puneeth0106/Blog-Agent.git
cd Blog-Agent
pip install -e .
```

### 2. Configure environment

```bash
# .env
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini

# Optional — Groq alternative
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama-3.3-70b-versatile

# Optional — LangSmith tracing
LANGCHAIN_API_KEY=your_key_here
LANGCHAIN_PROJECT=blog-agent
LANGCHAIN_TRACING_V2=true
```

### 3. Start the server

```bash
python3 app.py
# → http://localhost:8000
```

### 4. (Optional) LangGraph Studio

```bash
langgraph up
# Visual graph debugger at http://localhost:8123
```

---

## API Reference

### `POST /blogs`

Generate a blog post from a topic, with optional translation.

**Request body**

```json
{ "topic": "The Future of Quantum Computing", "language": "spanish" }
```

`language` is optional. Omit it for English output. Supported values: `english`, `spanish`, `french`, `german`, `telugu`, `swahili`.

**Response**

```json
{
  "data": {
    "topic": "The Future of Quantum Computing",
    "blog": {
      "title": "# El Futuro de la Computación Cuántica",
      "content": "## Introducción\n\nLa computación cuántica..."
    },
    "language_content": "spanish"
  }
}
```

**Examples**

```bash
# English
curl -X POST http://localhost:8000/blogs \
  -H "Content-Type: application/json" \
  -d '{"topic": "The Future of Quantum Computing"}'

# Spanish
curl -X POST http://localhost:8000/blogs \
  -H "Content-Type: application/json" \
  -d '{"topic": "The Future of Quantum Computing", "language": "spanish"}'
```

---

## Adding a New Language

3 steps, ~10 lines of code:

1. **`src/nodes/blog_node.py`** — add a translation node method following the existing pattern
2. **`src/graphs/graph_builder.py`** — register the node and its edge in `build_language_graph()`
3. **`src/nodes/blog_node.py`** — add a routing branch in `language_router_node()`

---

## Highlights for Reviewers

- **Agentic pipeline design** — multi-step LLM workflow with stateful graph orchestration, not a single prompt call
- **Conditional graph routing** — dynamic execution paths determined at runtime based on input, not hardcoded branches
- **Dual-provider LLM abstraction** — production-ready pattern for model-agnostic AI systems
- **Type-safe state machine** — Pydantic validation at every state boundary prevents silent failures
- **Full-stack deployment** — Python serverless backend + static frontend, both served from a single Vercel project
- **Extensible by design** — new language in 3 files, new LLM provider in 1 file, new node in 2 files

---

## Contact

**GitHub**: [Puneeth0106](https://github.com/Puneeth0106)
**LinkedIn**: [Your LinkedIn Profile]
**Email**: [Your Email]
