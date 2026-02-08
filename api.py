"""
Simple FastAPI server for sentiment analysis - Windows compatible
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from integrate import TradingSentimentSystem
import uvicorn
from datetime import datetime

app = FastAPI(title="BVMT Sentiment API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

system = TradingSentimentSystem()


@app.get("/")
def root():
    return {
        "service": "BVMT Stock Sentiment Analysis API",
        "version": "1.0",
        "endpoints": {
            "/health": "Check API health",
            "/sentiment/{symbol}": "Get sentiment for stock",
            "/sentiment/all": "Get sentiment for all stocks",
            "/stocks": "List available stocks"
        }
    }


@app.get("/health")
def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get("/sentiment/{symbol}")
def get_sentiment(symbol: str):
    result = system.analyze_stock_sentiment(symbol.upper(), max_articles=3)
    return result


@app.get("/sentiment/all")
def get_all_sentiments():
    stocks = ["ATB", "TUNTEL", "BH", "STB", "AB", "ADWYA", "AMS", "UIB"]
    results = system.analyze_multiple_stocks(stocks, max_articles_per_stock=2)
    return {
        "timestamp": datetime.now().isoformat(),
        "stocks_analyzed": len(stocks),
        "results": results
    }


@app.get("/stocks")
def list_stocks():
    return {
        "tunisian_stocks": system.scraper.stock_symbols,
        "count": len(system.scraper.stock_symbols)
    }


if __name__ == "__main__":
    print("Starting BVMT Sentiment API on http://localhost:8001")
    print("API Docs: http://localhost:8001/docs")
    # Use import string so reload=True works (no warning); Windows-compatible
    uvicorn.run("api:app", host="0.0.0.0", port=8001, reload=True)
