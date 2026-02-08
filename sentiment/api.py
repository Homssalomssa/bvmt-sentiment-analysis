#!/usr/bin/env python3
"""
Simple working API - Scrape → Analyze → Serve
No complexity, just working endpoints
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json
from datetime import datetime

app = FastAPI(title="BVMT Sentiment", version="2.0")

# Global cache - populated on first request
_data_cache = None


def _get_data():
    """Get or create cached data"""
    global _data_cache
    
    if _data_cache is not None:
        return _data_cache
    
    # Import here to avoid issues on module load
    from scraper_new import SmartNewsScraper
    from analyzer import SentimentAnalyzer
    
    print("Loading scraper and analyzer...")
    scraper = SmartNewsScraper()
    analyzer = SentimentAnalyzer()
    
    print("Fetching articles...")
    articles = scraper.get_articles_last_week()
    
    # Build sentiment dict
    sentiments = {}
    
    # Process mentioned companies
    for article in articles:
        text = f"{article['title']} {article['content']}"
        result = analyzer.analyze_sentiment(text)
        
        for company in article['mentioned_companies']:
            if company not in sentiments:
                sentiments[company] = {'scores': [], 'count': 0}
            sentiments[company]['scores'].append(result['score'])
            sentiments[company]['count'] += 1
    
    # Add unmentioned as neutral
    for symbol in scraper.stock_symbols:
        if symbol not in sentiments:
            sentiments[symbol] = {'scores': [0.0], 'count': 0}
    
    # Cache it
    _data_cache = {
        'sentiments': sentiments,
        'articles': articles,
        'companies': scraper.stock_symbols,
        'company_info': scraper.company_data,
        'timestamp': datetime.now().isoformat()
    }
    
    return _data_cache


@app.get("/")
def root():
    """Root endpoint - API is alive"""
    return {"service": "BVMT Sentiment Analysis", "version": "2.0"}


@app.get("/sentiment/{symbol}")
def sentiment(symbol: str):
    """Get sentiment for ONE stock"""
    data = _get_data()
    symbol = symbol.upper()
    
    if symbol not in data['companies']:
        return JSONResponse({"error": f"Unknown symbol: {symbol}"}, status_code=404)
    
    sent = data['sentiments'].get(symbol, {'scores': [0.0], 'count': 0})
    scores = sent['scores']
    avg_score = sum(scores) / len(scores) if scores else 0.0
    
    return {
        "symbol": symbol,
        "score": round(avg_score, 3),
        "label": "positive" if avg_score > 0.1 else "negative" if avg_score < -0.1 else "neutral",
        "mentions": sent['count'],
        "company": data['company_info'].get(symbol, {}).get('fr', symbol)
    }


@app.get("/sentiment/all")
def sentiment_all():
    """Get ALL stocks sentiment"""
    data = _get_data()
    
    results = []
    for symbol in data['companies']:
        sent = data['sentiments'].get(symbol, {'scores': [0.0], 'count': 0})
        scores = sent['scores']
        avg = sum(scores) / len(scores) if scores else 0.0
        
        results.append({
            "symbol": symbol,
            "score": round(avg, 3),
            "label": "positive" if avg > 0.1 else "negative" if avg < -0.1 else "neutral",
            "mentions": sent['count']
        })
    
    # Sort by mentions descending
    results.sort(key=lambda x: x['mentions'], reverse=True)
    
    return {
        "count": len(results),
        "data": results
    }


@app.get("/articles")
def articles():
    """Get all articles with mentions"""
    data = _get_data()
    
    return {
        "count": len(data['articles']),
        "articles": [
            {
                "title": a['title'],
                "source": a['source'],
                "mentions": a['mentioned_companies'],
                "date": a['date'].isoformat() if hasattr(a['date'], 'isoformat') else str(a['date'])
            }
            for a in data['articles']
        ]
    }


@app.get("/stats")
def stats():
    """Get statistics"""
    data = _get_data()
    
    mentioned_count = sum(1 for s in data['sentiments'].values() if s['count'] > 0)
    
    return {
        "total_companies": len(data['companies']),
        "mentioned": mentioned_count,
        "neutral": len(data['companies']) - mentioned_count,
        "articles": len(data['articles']),
        "cached_at": data['timestamp']
    }


@app.post("/refresh")
def refresh():
    """Force refresh cache"""
    global _data_cache
    _data_cache = None
    data = _get_data()
    return {"status": "refreshed", "timestamp": data['timestamp']}
