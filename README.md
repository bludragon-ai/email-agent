# 📧 Email Agent

AI-powered email management agent that triages, categorizes, summarizes, and drafts replies to your emails using LLMs.

![Python](https://img.shields.io/badge/python-3.11+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![LangChain](https://img.shields.io/badge/langchain-0.3-orange)

## ✨ Features

- **Auto-categorization** — Classifies emails as urgent, client, routine, newsletter, or spam
- **Priority scoring** — 5-level priority ranking (critical → minimal)
- **Thread summarization** — Condenses multi-message threads into key points
- **Smart reply drafting** — Generates contextual replies with tone selection (professional, friendly, formal, concise, apologetic)
- **Pluggable providers** — Local JSON demo store included; Gmail/IMAP interface ready to implement
- **Multi-LLM support** — Anthropic Claude (default) or OpenAI GPT via environment config

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│                 Streamlit UI                     │
│         (Inbox · Detail · Compose)               │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│               EmailAgent                         │
│    (orchestrates providers + AI chains)           │
└───────┬──────────────────────┬──────────────────┘
        │                      │
┌───────▼───────┐    ┌────────▼────────────────┐
│   Provider    │    │     LangChain Chains     │
│  (pluggable)  │    │  ┌─────────────────────┐ │
│               │    │  │ Triage / Categorize  │ │
│ • Local JSON  │    │  │ Reply Drafting       │ │
│ • Gmail*      │    │  │ Thread Summarization │ │
│ • IMAP*       │    │  └─────────────────────┘ │
└───────────────┘    └────────┬────────────────┘
                              │
                   ┌──────────▼──────────┐
                   │    LLM Provider     │
                   │  Anthropic / OpenAI │
                   └─────────────────────┘

* = planned
```

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/bludragon-ai/email-agent.git
cd email-agent

# Install
make dev

# Configure
cp .env.example .env
# Edit .env with your API key

# Run
make run
```

Open [http://localhost:8501](http://localhost:8501)

### Docker

```bash
cp .env.example .env
# Edit .env
make docker-up
```

## ⚙️ Configuration

| Variable | Default | Description |
|---|---|---|
| `LLM_PROVIDER` | `anthropic` | `anthropic` or `openai` |
| `ANTHROPIC_API_KEY` | — | Anthropic API key |
| `ANTHROPIC_MODEL` | `claude-sonnet-4-20250514` | Anthropic model name |
| `OPENAI_API_KEY` | — | OpenAI API key |
| `OPENAI_MODEL` | `gpt-4o-mini` | OpenAI model name |
| `LLM_TEMPERATURE` | `0.2` | LLM temperature |

## 📁 Project Structure

```
email-agent/
├── src/
│   ├── agents/          # EmailAgent orchestrator
│   ├── chains/          # LangChain chains (triage, reply, summarize)
│   ├── models/          # Pydantic domain models
│   ├── providers/       # Pluggable email backends
│   ├── ui/              # Streamlit application
│   └── utils/           # Configuration & helpers
├── tests/               # Unit tests
├── data/                # Sample email data
├── Dockerfile
├── docker-compose.yml
├── Makefile
└── pyproject.toml
```

## 🧪 Testing

```bash
make test
```

## 🔌 Adding a New Email Provider

Implement `src/providers/base.EmailProvider`:

```python
class GmailProvider(EmailProvider):
    def list_emails(self, limit=50, offset=0) -> list[Email]: ...
    def get_email(self, email_id: str) -> Optional[Email]: ...
    def get_thread(self, thread_id: str) -> list[Email]: ...
    def mark_read(self, email_id: str) -> None: ...
    def send_email(self, to, subject, body) -> Email: ...
```

## 📄 License

MIT
