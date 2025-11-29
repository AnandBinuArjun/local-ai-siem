# 🛡️ Local AI SIEM + Autonomous SOC Assistant

> **A fully local, privacy-first Security Information and Event Management (SIEM) system powered by local LLMs.**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Status](https://img.shields.io/badge/status-Alpha-orange.svg)

**Goal:** A "mini-Splunk" with an AI brain that runs entirely on your workstation. It ingests logs, detects threats using Sigma-style rules, and uses a local Large Language Model (LLM) to summarize incidents and answer investigation questions—without sending a single byte to the cloud.

---

## 📖 Table of Contents

- [Architecture](#-architecture)
- [Key Features](#-key-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [Directory Structure](#-directory-structure)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)

---

## 🏗️ Architecture

The system is designed as a modular pipeline, separating ingestion, storage, detection, and AI analysis.

### High-Level Data Flow

```mermaid
graph TD
    subgraph Sources
        OS[OS Logs]
        App[App Logs]
        Net[Network Logs]
    end

    subgraph "Ingestion & Normalization"
        C[Collectors] -->|Raw JSON| N[Normalizer]
        N -->|Event Object| Router{Router}
    end

    subgraph Storage
        Router -->|Insert| SQL[(SQLite/Postgres)]
        Router -->|Embed| Vec[(ChromaDB Vector Store)]
    end

    subgraph "Detection & AI"
        SQL -->|Stream| Detect[Detection Engine]
        Detect -->|Alerts| Correlate[Correlation Engine]
        Correlate -->|Incidents| LLM[Local LLM (Ollama)]
        LLM -->|Enrichment| SQL
    end

    subgraph Interface
        User((User)) <-->|REST API| API[FastAPI Server]
        API <-->|Search| Vec
        API <-->|Query| SQL
        API <-->|Chat| LLM
    end

    Sources --> C
```

### Component Breakdown

1. **Ingestion Layer**: Python-based collectors (e.g., `aisiem.ingest.windows`) that tail logs from OS and apps.
2. **Normalization**: Converts messy raw logs into a canonical `Event` schema (Timestamp, Host, Source, Category, Severity).
3. **Storage**:
    - **Relational**: SQLite for structured event storage and rapid filtering.
    - **Vector**: ChromaDB for semantic search (e.g., "Find similar attacks").
4. **Detection**: Evaluates rules against incoming events to generate `Detections`.
5. **Correlation**: Groups related detections into `Incidents` based on entities (User, IP) and time.
6. **AI Layer**:
    - **Embeddings**: `sentence-transformers` converts logs to vectors.
    - **LLM**: Connects to a local Ollama instance (Llama 3, Mistral) for incident summarization and "SOC Chat".

---

## ✨ Key Features

- **🔍 Universal Ingestion**: Modular collectors for Windows Event Logs, Linux `journald`, and text files.
- **🧠 Semantic Search**: Search logs by *meaning*, not just keywords (e.g., "Show me failed logins" finds Event ID 4625).
- **🤖 AI SOC Assistant**: Chat with your logs. Ask "What did user Alice do today?" and get a summarized answer.
- **🚨 Automated Correlation**: Links isolated alerts into full incident narratives.
- **🔒 100% Local**: No data leaves your machine. Perfect for sensitive environments or homelabs.

---

## ⚙️ Installation

### Prerequisites

- **Python 3.10+**
- **Ollama** (for the AI features)
  - Download from [ollama.com](https://ollama.com)
  - Run `ollama run llama3` (or your preferred model)

### Setup

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/local-ai-siem.git
    cd local-ai-siem
    ```

2. **Install dependencies**:

    ```bash
    # Windows
    setup_env.bat
    
    # Linux/Mac
    pip install -r requirements.txt
    ```

---

## 🚀 Usage

### 1. Start Ingestion

This starts the background worker that collects logs, normalizes them, and indexes them into the DB and Vector Store.

```bash
# Windows
run_ingestion.bat

# Manual
python -m aisiem.main
```

### 2. Start the API Server

This launches the REST API and the Chat interface backend.

```bash
# Windows
run_api.bat

# Manual
uvicorn aisiem.api.server:app --reload
```

### 3. Chat with your SIEM

Send a POST request to `http://localhost:8000/chat`:

```json
{
  "query": "Show me any suspicious PowerShell activity from the last 24 hours"
}
```

---

## 📂 Directory Structure

```text
aisiem/
├── ingest/             # 📥 Data Collectors
│   ├── windows.py      # Windows Event Log collector
│   └── linux.py        # (Planned) Journald collector
├── normalize/          # 🔄 Parsers & Schema
│   ├── router.py       # Directs logs to correct parser
│   └── windows_parsers.py
├── storage/            # 💾 Database & Models
│   ├── db.py           # SQLAlchemy setup
│   └── models.py       # Pydantic schemas (Event, Incident)
├── detect/             # 🕵️ Detection Logic
│   ├── rules_engine.py # Sigma-style rule evaluator
│   └── correlation.py  # Incident grouping logic
├── ai/                 # 🧠 AI & ML Components
│   ├── embedder.py     # SentenceTransformers wrapper
│   ├── vector_index.py # ChromaDB interface
│   └── incident_summarizer.py # LLM client
├── api/                # 🌐 REST API
│   └── routes/         # Endpoint definitions
└── ui/                 # 🖥️ Frontend (CLI/Web)
```

---

## 🗺️ Roadmap

### Phase 1: Core Foundation (✅ Completed)

- [x] Project skeleton & architecture
- [x] SQLite & SQLAlchemy integration
- [x] Basic Windows Event Log ingestion
- [x] Normalization pipeline

### Phase 2: The "Brain" (✅ Completed)

- [x] Vector Database integration (ChromaDB)
- [x] Local Embedding generation
- [x] Basic Correlation Engine
- [x] LLM Integration (Ollama)
- [x] Chat API Endpoint

### Phase 3: Detection & UI (🚧 In Progress)

- [ ] Sigma Rule parser & engine
- [ ] Web Dashboard (React/Next.js)
- [ ] Real-time WebSocket alerts
- [ ] Linux & macOS collectors

### Phase 4: Advanced Features

- [ ] Automated Response (Active Defense)
- [ ] Multi-node support (Forwarders)
- [ ] Fine-tuned LoRA for Security Analysis

---

## 🤝 Contributing

Contributions are welcome! Please read `CONTRIBUTING.md` for details on our code of conduct and the process for submitting pull requests.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
