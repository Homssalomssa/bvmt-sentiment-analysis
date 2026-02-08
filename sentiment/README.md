# BVMT Sentiment Analysis Module

**Tunisian Stock Exchange (BVMT) – News Sentiment Analysis for IHEC-CODELAB 2.0 Hackathon**

---

## Project Context

This folder contains the **Sentiment Analysis** module for a BVMT trading assistant built during the **IHEC-CODELAB 2.0 Hackathon**. It analyzes French, Arabic, and English financial news to produce sentiment scores and explanations for Tunisian listed stocks.

| Role        | Responsibility           |
|------------|---------------------------|
| **Person 3** (this repo) | Sentiment analysis, news scraping, API |
| Person 1   | Trading dashboard / frontend |
| Person 2   | Portfolio / decision agent |
| Person 4   | Price forecasting / other modules |

---

## Quick Setup (Windows)

### 1. Prerequisites

- **Python 3.8+** – [python.org](https://www.python.org/downloads/)
- **Git** – [git-scm.com](https://git-scm.com/)

### 2. Clone & setup

```cmd
git clone https://github.com/Homssalomssa/bvmt-sentiment-analysis.git
cd bvmt-sentiment-analysis\sentiment
setup.bat
```

Or manually (from the `sentiment` folder):

```cmd
cd sentiment
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run

From the **sentiment** folder:

| Action        | Command / script      |
|---------------|------------------------|
| Test analyzer & scraper | `test_system.bat` or `python analyzer.py` then `python scraper.py` |
| Full analysis + JSON export | `run_system.bat` or `python integrate.py` |
| Start API server | `quick_start.bat` → option 4, or `python api.py` |

---

## API Documentation

**Base URL (local):** `http://localhost:8001`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Service info and list of endpoints |
| GET | `/health` | Health check |
| GET | `/stocks` | List of supported Tunisian stock symbols |
| GET | `/sentiment/{symbol}` | Sentiment for one stock (e.g. ATB, TUNTEL, BH) |
| GET | `/sentiment/all` | Sentiment for all configured stocks |

With the API running: **Swagger UI** at [http://localhost:8001/docs](http://localhost:8001/docs)

---

## Project Structure (this folder)

```
sentiment/
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
└── team_integration.md   # Team integration instructions
```

Generated at runtime (not in repo): `venv/`, `stock_sentiment_results.json`, `__pycache__/`.

---

## Team Integration

- **Person 1 (Frontend):** GET `http://localhost:8001/sentiment/{symbol}` or `/sentiment/all` – use `overall_score`, `sentiment`, `overall_explanation`.
- **Person 2 (Decision agent):** Same endpoints; use `overall_score`, `confidence`, `explanation_detail.recommendation`.
- **Person 4:** Same API; combine with your module.

See **team_integration.md** in this folder for details.

---

Developed for **IHEC-CODELAB 2.0 Hackathon**.
