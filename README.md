# Language Learning Agent

An AI-powered language learning assistant that generates vocabulary words, translates them, and automatically creates Anki flashcard decks — all through a conversational interface.

## What It Does

- Fetches random words in a target language (Spanish, German, French, etc.)
- Supports difficulty levels: `beginners`, `intermediates`, `advanced`
- Translates words using a local or cloud LLM
- Automatically creates Anki decks and flashcards via MCP (Model Context Protocol)
- Supports two LLM backends: **Gemini** (cloud) and **Ollama/qwen3** (local)

## Tech Stack

- [LangGraph](https://github.com/langchain-ai/langgraph) — agent graph orchestration
- [LangChain](https://github.com/langchain-ai/langchain) — LLM abstractions
- [Ollama](https://ollama.com) — local LLM inference (qwen3:4b)
- [Gemini](https://ai.google.dev) — Google cloud LLM
- [MCP (Model Context Protocol)](https://modelcontextprotocol.io) — Anki integration via clanki
- [Clanki](https://github.com/your-username/clanki) — MCP server for Anki

## Project Structure
```
PythonProject/
├── main.py                  # Entry point, agent graph
├── agent/
│   └── tools.py             # LangChain tools (word fetch, translate)
├── clanki/                  # MCP server for Anki (Node.js)
│   ├── build/
│   │   └── index.js
│   └── package.json
├── words/                   # Word list JSON files per language
├── .env                     # API keys (not committed)
├── requirements.txt
└── README.md
```

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/your-username/language-learning-agent
cd language-learning-agent
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Install and build Clanki (Anki MCP server)
```bash
cd clanki
npm install
npm run build
cd ..
```

### 4. Set up environment variables
Create a `.env` file:
```
google_api_key=your_gemini_api_key_here
```

### 5. Install Ollama (for local LLM)
Download from https://ollama.com and pull the model:
```bash
ollama pull qwen3:4b
```

### 6. Make sure Anki is running
Anki must be open on your desktop for the MCP server to connect.

## Usage

Run with Ollama (local, free):
```bash
python main.py
```

Run with Gemini (cloud):
```python
# Change last line in main.py
asyncio.run(main('gemini'))
```

### Example prompts
```
Get 20 random words in Spanish.
Get 10 hard words in German.
Get 15 easy words in English and translate them to Spanish.
Get 5 advanced German words, translate to English and add to Anki deck called German::Advanced
```

## Requirements

- Python 3.12+
- Node.js 18+ (for clanki)
- Anki desktop app
- Ollama (for local mode)
```

---

**`requirements.txt`**
```
langchain
langchain-google-genai
langchain-ollama
langchain-mcp-adapters
langgraph
python-dotenv
typing-extensions
attrs
ollama
```

---

**`.env.example`**
```
google_api_key=your_gemini_api_key_here# Language Learning Agent

An AI-powered language learning assistant that generates vocabulary words, translates them, and automatically creates Anki flashcard decks — all through a conversational interface.

## What It Does

- Fetches random words in a target language (Spanish, German, French, etc.)
- Supports difficulty levels: `beginners`, `intermediates`, `advanced`
- Translates words using a local or cloud LLM
- Automatically creates Anki decks and flashcards via MCP (Model Context Protocol)
- Supports two LLM backends: **Gemini** (cloud) and **Ollama/qwen3** (local)

## Tech Stack

- [LangGraph](https://github.com/langchain-ai/langgraph) — agent graph orchestration
- [LangChain](https://github.com/langchain-ai/langchain) — LLM abstractions
- [Ollama](https://ollama.com) — local LLM inference (qwen3:4b)
- [Gemini](https://ai.google.dev) — Google cloud LLM
- [MCP (Model Context Protocol)](https://modelcontextprotocol.io) — Anki integration via clanki
- [Clanki](https://github.com/your-username/clanki) — MCP server for Anki

## Project Structure
```
PythonProject/
├── main.py                  # Entry point, agent graph
├── agent/
│   └── tools.py             # LangChain tools (word fetch, translate)
├── clanki/                  # MCP server for Anki (Node.js)
│   ├── build/
│   │   └── index.js
│   └── package.json
├── words/                   # Word list JSON files per language
├── .env                     # API keys (not committed)
├── requirements.txt
└── README.md
```

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/your-username/language-learning-agent
cd language-learning-agent
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Install and build Clanki (Anki MCP server)
```bash
cd clanki
npm install
npm run build
cd ..
```

### 4. Set up environment variables
Create a `.env` file:
```
google_api_key=your_gemini_api_key_here
```

### 5. Install Ollama (for local LLM)
Download from https://ollama.com and pull the model:
```bash
ollama pull qwen3:4b
```

### 6. Make sure Anki is running
Anki must be open on your desktop for the MCP server to connect.

## Usage

Run with Ollama (local, free):
```bash
python main.py
```

Run with Gemini (cloud):
```python
# Change last line in main.py
asyncio.run(main('gemini'))
```

### Example prompts
```
Get 20 random words in Spanish.
Get 10 hard words in German.
Get 15 easy words in English and translate them to Spanish.
Get 5 advanced German words, translate to English and add to Anki deck called German::Advanced
```

## Requirements

- Python 3.12+
- Node.js 18+ (for clanki)
- Anki desktop app
- Ollama (for local mode)
```

---

**`requirements.txt`**
```
langchain
langchain-google-genai
langchain-ollama
langchain-mcp-adapters
langgraph
python-dotenv
typing-extensions
attrs
ollama
```

---

**`.env.example`**
```
google_api_key=your_gemini_api_key_here