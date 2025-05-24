# Sentimint: AI-Powered Financial Insight Agent 🚀📈

This repository (`agentai-fin-app`) is the main backend API for **Sentimint**, an AI-driven financial analysis system that:
- Fetches real-time financial data
- Gathers relevant news articles
- Generates investment recommendations
- Verifies and justifies those recommendations using LLMs
- Supports frontend UI via REST API (and optionally WebSocket)

---

## 🧠 Architecture Overview

```
Frontend (React / Orchids UI)
      │
      ▼
Backend: Flask API (agentai-fin-app)
      ├── Financial Data: [finscraper submodule]
      ├── News Analysis: [finscraper + LLM]
      ├── Insight Generation: [agent.py]
      └── Recommendation Verifier: [testing_bot.py]
```

---

## 📁 Repository Structure

```bash
agentai-fin-app/
│
├── app.py                       # Flask app entrypoint
├── static/nasdaq-listed-symbols.csv  # Company name ↔ ticker mapping
│
├── Agentmodules/                # Submodule: Core agent + verification logic
│   ├── agent.py                 # LLM-based stock insight generator
│   ├── testing_bot.py           # Verifier agent with heuristics + multi-source analysis
│
├── finscraper/                 # Submodule: Stock + news data fetcher
│   └── scraper_tool/
│       ├── fetcher.py          # Uses Yahoo Finance (yfinance)
│       ├── news_fetcher.py     # Pulls financial news
│       └── tool.py             # LangChain wrappers
│
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## 🛠 Features

### ✅ Stock Insight Agent (agent.py)
- Uses OpenAI GPT model
- Ingests financial metrics + news
- Outputs: Buy/Sell recommendation, justification, confidence %

### ✅ Verifier Agent (testing_bot.py)
- Fetches fresh news
- Applies heuristic rules (e.g., P/E > 100)
- Validates LLM recommendation
- Returns final verdict and extracted support

### ✅ RESTful Flask API (app.py)
- `/financials`: Returns ticker + news + parsed data
- `/insight`: Generates LLM insight
- `/verify`: Verifies and justifies recommendation

---

## 🧪 Example Workflow

```bash
curl -X POST http://localhost:5050/insight \
     -H "Content-Type: application/json" \
     -d '{"query": "Apple"}'
```

→ Returns JSON with:
- financials
- recommendation
- justification
- supporting news
- verdict

---

## 🧰 Setup

### 1. Clone with submodules
```bash
git clone --recurse-submodules https://github.com/ForgottenLight4415/agentai-fin-app.git
```

### 2. Install dependencies
```bash
cd agentai-fin-app
pip install -r requirements.txt
```

### 3. Add your OpenAI key
```bash
echo "OPENAI_API_KEY=sk-..." > .env
```

### 4. Run the backend
```bash
python app.py
```

---

## 🌐 Frontend

The frontend UI (`sentimint-landing`) connects via REST and supports:
- Visualized flow of agent analysis
- Loading animations per stage
- Interactive exploration of financial + news data

---

## 👥 Contributors

- [@ForgottenLight4415](https://github.com/ForgottenLight4415)
- [@RohanChavan0701](https://github.com/RohanChavan0701)
- [atharvasalunke](https://github.com/atharvasalunke)
- [hitanshi2599](https://github.com/hitanshi2599)

---

