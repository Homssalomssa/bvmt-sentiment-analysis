# BVMT Sentiment Analysis Module

**Tunisian Stock Exchange (BVMT) – News Sentiment Analysis for IHEC-CODELAB 2.0 Hackathon**

---

## Project Context

This repository contains the **Sentiment Analysis** module for a BVMT trading assistant built during the **IHEC-CODELAB 2.0 Hackathon**. It analyzes French, Arabic, and English financial news to produce sentiment scores and explanations for Tunisian listed stocks.

| Role        | Responsibility           |
|------------|---------------------------|
| **Person 3** (this repo) | Sentiment analysis, news scraping, API |
| Person 1   | Trading dashboard / frontend |
| Person 2   | Portfolio / decision agent |
| Person 4   | Price forecasting / other modules |

---

## Features

- **Multilingual**: French, Arabic, English keyword-based sentiment
- **Explainability**: Per-article and overall explanations with intensity, key findings, and recommendations
- **Context-aware**: Neutral phrases (e.g. “performances stables”) and negation handling
- **Windows-ready**: Batch scripts, no GPU; runs on Python 3.8+
- **REST API**: FastAPI server for frontend and other modules

---

## Quick Setup (Windows)

### 1. Prerequisites

- **Python 3.8+** – [python.org](https://www.python.org/downloads/)
- **Git** (for cloning/updates) – [git-scm.com](https://git-scm.com/)

### 2. Clone & setup

```cmd
git clone https://github.com/Homssalomssa/bvmt-sentiment-analysis.git
cd bvmt-sentiment-analysis
setup.bat
```

Or manually:

```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run

| Action        | Command / script      |
|---------------|------------------------|
| Test analyzer & scraper | `test_system.bat` or `python analyzer.py` then `python scraper.py` |
| Full analysis + JSON export | `run_system.bat` or `python integrate.py` |
| Start API server | `quick_start.bat` → option 4, or `python api.py` |

---

## API Documentation

**Base URL (local):** `http://localhost:8001`

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Service info and list of endpoints |
| GET | `/health` | Health check |
| GET | `/stocks` | List of supported Tunisian stock symbols |
| GET | `/sentiment/{symbol}` | Sentiment for one stock (e.g. ATB, TUNTEL, BH) |
| GET | `/sentiment/all` | Sentiment for all configured stocks |

### Examples

**Health check**

```bash
curl http://localhost:8001/health
```

**Sentiment for one stock (ATB)**

```bash
curl http://localhost:8001/sentiment/ATB
```

**All stocks**

```bash
curl http://localhost:8001/sentiment/all
```

### Sample response: `/sentiment/ATB`

```json
{
  "symbol": "ATB",
  "overall_score": 0.72,
  "sentiment": "positive",
  "confidence": 0.85,
  "overall_explanation": "Overall positive sentiment from 3 articles. Distribution: 2 positive, 0 negative, 1 neutral. Example: Strong positive sentiment (0.90). Key positive indicators: excellent, profit, record.",
  "articles_analyzed": 3,
  "articles": [
    {
      "title": "...",
      "sentiment_score": 0.9,
      "sentiment_label": "positive",
      "explanation": "Very strong positive sentiment (0.90). Key positive indicators: excellent, profit, record. No negative terms detected.",
      "explanation_detail": {
        "intensity": "Very strong",
        "key_findings": ["Key positive indicators: 'excellent', 'profit', 'record'", "No concerning negative terms detected."],
        "recommendation": "Overall positive outlook for investment consideration."
      }
    }
  ]
}
```

### Interactive docs

With the API running:

- **Swagger UI:** [http://localhost:8001/docs](http://localhost:8001/docs)
- **ReDoc:** [http://localhost:8001/redoc](http://localhost:8001/redoc)

---

## Team Integration Guide

### For Person 1 (Frontend / Dashboard)

- Call **GET** `http://localhost:8001/sentiment/{symbol}` or `/sentiment/all` to get scores and explanations.
- Use `overall_score` (-1 to 1), `sentiment` (positive/negative/neutral), and `overall_explanation` for UI.
- Per-article: `articles[].sentiment_label`, `articles[].explanation`, `articles[].explanation_detail.intensity` and `key_findings`.

### For Person 2 (Portfolio / Decision Agent)

- Use `overall_score` and `confidence` for logic; use `explanation_detail.recommendation` and `key_findings` for reasoning or logs.
- Run the API on a fixed port (e.g. 8001) or get the URL from the team.

### For Person 4 (Forecasting / Other)

- Same API; combine sentiment with your outputs (e.g. use score as a feature or for filtering).

### Running the API

1. In this repo: `python api.py` (or `quick_start.bat` → 4).
2. API runs at **http://localhost:8001**.
3. Frontend/other services: use this base URL in your config.

---

## Running Tests

```cmd
venv\Scripts\activate
python analyzer.py
python scraper.py
python integrate.py
```

Or use **test_system.bat** to run analyzer, scraper, and integration in sequence.

**Frontend integration test (API must be running):**

```cmd
python test_frontend_integration.py
```

---

## Project Structure

```
bvmt-sentiment-analysis/
├── analyzer.py          # Sentiment analyzer (FR/AR/EN, explainability)
├── scraper.py            # Mock Tunisian financial news scraper
├── integrate.py          # Orchestration: scraper + analyzer + export
├── api.py                # FastAPI server
├── requirements.txt      # Python dependencies
├── setup.bat             # First-time setup (venv + pip install)
├── test_system.bat       # Run analyzer + scraper + integrate tests
├── run_system.bat        # Full analysis and JSON export
├── quick_start.bat       # Menu: setup / test / run / API
├── test_frontend_integration.py  # API client test
├── README.md             # This file
├── team_integration.md   # Team integration instructions
└── .gitignore
```

Generated at runtime (not in repo): `venv/`, `stock_sentiment_results.json`, `__pycache__/`.

---

## Supported stocks (examples)

ATB, TUNTEL, BH, STB, AB, ADWYA, AMS, CELL, SIPHAT, UIB (configurable in code).

---

## License & Hackathon

Developed for **IHEC-CODELAB 2.0 Hackathon**. Use and adapt for your team’s BVMT trading assistant.
