# AI-Powered Blog Generation Agent

**Automated Content Creation System** | **Multi-Language Blog Generation with LangGraph & LLM Orchestration**

An intelligent blog generation agent that leverages state-of-the-art LLMs and LangGraph orchestration to automatically create SEO-optimized blog content in multiple languages. Architected with FastAPI for high-performance API endpoints and designed for scalable content production workflows.

---

## Key Features

- **Intelligent Blog Generation**: Automatically creates catchy titles and comprehensive blog content (500+ words) using GPT-4o-mini
- **Multi-Language Translation**: Supports 6 languages (English, Spanish, French, German, Telugu, Swahili) with context-aware translations
- **Graph-Based Orchestration**: Leveraged LangGraph for sophisticated state management and conditional routing between content generation stages
- **RESTful API Architecture**: FastAPI-powered endpoints with hot-reload capability for seamless integration
- **SEO-Optimized Content**: Implements SEO best practices for title and content generation with plagiarism-free output
- **Modular Design Pattern**: Cleanly separated concerns with dedicated nodes, states, and LLM abstractions for maintainability
- **Flexible LLM Support**: Configurable support for OpenAI and Groq models with environment-based configuration

---

## Tech Stack

### **Languages**
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)

### **AI Frameworks & LLMs**
- **LangChain** (v0.3.25) - LLM application framework
- **LangGraph** (v0.4.8) - State machine orchestration for multi-step workflows
- **OpenAI GPT-4o-mini** - Primary content generation model
- **ChatGroq** (Llama 3.3 70B) - Alternative LLM provider support

### **Web Framework**
- **FastAPI** (v0.115+) - High-performance async API framework
- **Uvicorn** - ASGI server with auto-reload

### **Development Tools**
- **Pydantic** - Data validation and settings management
- **python-dotenv** - Environment variable management
- **LangGraph CLI** - Development and debugging tooling

---

## Architecture & System Design

### **High-Level Data Flow**

```
┌─────────────────┐
│   API Request   │ (Topic + Optional Language)
│   (FastAPI)     │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│       Graph Builder (LangGraph)         │
│  ┌─────────────────────────────────┐   │
│  │  Router Logic                    │   │
│  │  (Topic-only vs Language Mode)   │   │
│  └──────────┬──────────────────────┘   │
│             │                            │
│             ▼                            │
│  ┌──────────────────────┐               │
│  │  Title Creation Node │               │
│  │  (SEO-Optimized)     │               │
│  └──────────┬───────────┘               │
│             │                            │
│             ▼                            │
│  ┌──────────────────────┐               │
│  │ Content Generation   │               │
│  │ Node (500+ words)    │               │
│  └──────────┬───────────┘               │
│             │                            │
│             ▼                            │
│  ┌──────────────────────┐               │
│  │  Language Router     │◄──(if language specified)
│  │  (Conditional Logic) │               │
│  └──────────┬───────────┘               │
│             │                            │
│    ┌────────┴────────┐                  │
│    ▼                 ▼                  │
│  [Translation Nodes (5 languages)]      │
│    │                 │                  │
│    └────────┬────────┘                  │
│             │                            │
└─────────────┼────────────────────────────┘
              │
              ▼
      ┌───────────────┐
      │ JSON Response │ (Title + Content)
      └───────────────┘
```

### **Core Components**

1. **State Management** (`Blogstate`): TypedDict-based state container tracking topic, generated blog, and language preferences
2. **Graph Builder**: Dynamically constructs execution graphs with conditional routing based on use case
3. **Blog Nodes**: Specialized processing units for title creation, content generation, and translation
4. **LLM Abstraction Layer**: Unified interface supporting multiple LLM providers (OpenAI, Groq)

---

## Installation & Setup

### **Prerequisites**
- Python 3.11 or higher
- OpenAI API Key (or Groq API Key)

### **1. Clone the Repository**
```bash
git clone https://github.com/yourusername/Blog-Agent.git
cd Blog-Agent
```

### **2. Create Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **3. Install Dependencies**
```bash
pip install -e .
```

### **4. Configure Environment Variables**
Create a `.env` file in the project root:
```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Groq Configuration
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

### **5. Run the Application**
```bash
python3 app.py
```
The API will be available at `http://localhost:8000`

---

## Usage Examples

### **Generate Blog (English Only)**
```bash
curl -X POST http://localhost:8000/blogs \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "The Future of Artificial Intelligence"
  }'
```

### **Generate Blog with Translation**
```bash
curl -X POST http://localhost:8000/blogs \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Sustainable Energy Solutions",
    "language": "spanish"
  }'
```

**Supported Languages**: `english`, `spanish`, `french`, `german`, `telugu`, `swahili`

---

## Key Achievements

- **Automated Multi-Step Workflow**: Orchestrated a 3-stage content generation pipeline reducing manual effort by 100%
- **Scalable Graph Architecture**: Implemented conditional routing with LangGraph, enabling dynamic execution paths based on user input
- **Multi-LLM Support**: Architected flexible LLM abstraction supporting both OpenAI and Groq providers with zero code changes
- **Production-Ready API**: Deployed FastAPI endpoints with async support and hot-reload capability for rapid iteration
- **Context-Aware Translation**: Engineered translation nodes that preserve tone and cultural nuances across 5 languages
- **Type-Safe State Management**: Leveraged Pydantic models ensuring data integrity throughout the execution graph

---

## Project Structure

```
Blog-Agent/
├── app.py                      # FastAPI application entry point
├── main.py                     # CLI entry point
├── pyproject.toml              # Project dependencies and metadata
├── langgraph.json             # LangGraph configuration
├── .env                        # Environment variables (not in repo)
└── src/
    ├── graphs/
    │   └── graph_builder.py   # Graph orchestration logic
    ├── llms/
    │   └── llm.py             # LLM provider abstractions
    ├── nodes/
    │   └── blog_node.py       # Content generation nodes
    └── states/
        └── blogstate.py       # State type definitions
```

---

## Future Enhancements

- [ ] Add support for custom content length parameters
- [ ] Implement caching layer for repeated topics
- [ ] Integrate vector database for RAG-based content enrichment
- [ ] Add streaming responses for real-time content generation
- [ ] Implement A/B testing for multiple title/content variants
- [ ] Deploy with container orchestration (Docker + Kubernetes)

---

## Contact

**Portfolio**: [Your Portfolio URL]  
**LinkedIn**: [Your LinkedIn Profile]  
**Email**: [Your Email]

---

<div align="center">

**Star this repo if you find it useful!**

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/Python-3.11%2B-brightgreen)
![LangGraph](https://img.shields.io/badge/LangGraph-0.4.8-orange)

</div>
