# AI Agent Tools

A Python toolkit for AI agents featuring Retrieval-Augmented Generation (RAG) with LangChain, Chroma vector store, HuggingFace embeddings, OpenAI LLM, and SerpAPI search integration. Includes environment-based API key management.

## Architecture Overview

This project is structured in four layers:

### 1. Data Layer
Where facts live. This can include Chroma DB, CSVs, or external APIs.

### 2. Retrieval Layer
The librarian (RAG logic) that finds information for the model using vector search and retrieval techniques.

### 3. Model Layer
The LLM (e.g., OpenAI GPT-4, Claude) that interprets and reasons over the retrieved information.

### 4. Orchestration Layer
LangChain Agents decide which tool, model, or data source to use for the current job.

---

**Benefits of Layered Design:**
- Swap models (OpenAI → Anthropic) without breaking retrieval.
- Upgrade your data store without touching your model code.
- Test each layer independently for robust development.

## Step-by-Step Architecture

**Step 1: Data ingestion**
- Fetch data from PubMed, ClinicalTrials.gov, OpenFDA via their APIs.
- Store structured results in SQLite / Postgres.

**Step 2: LangChain agent**
- Use langchain_experimental agent tools to query your database or APIs.
- Wrap queries in structured prompts to avoid hallucinations (critical in medical context).

**Step 3: Logging & tracking**
- Use langsmith for experiment logs, queries, and outputs.
- Keep a query-response history for auditability.

**Step 4: Optional fine-tuning / embeddings**
- Generate vector embeddings for research papers or drug info.
- Use langchain-text-splitters to break long documents into chunks.

## Features
- RAG pipeline with LangChain, Chroma, HuggingFace, and OpenAI.
- SerpAPI search tool integration.
- Environment-based API key management via `.env`.

## Getting Started
1. Clone the repo and set up a Python environment.
2. Add your API keys to `.env`.
3. Use the provided tools to build and extend your AI agent workflows.

## Changelog
See `CHANGELOG.md` for details on updates and new features.
