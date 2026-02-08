# API QUICK REFERENCE

## Start
```bash
python -m uvicorn api:app --host 127.0.0.1 --port 8000
```

## Endpoints

### Get One Stock
```
GET http://localhost:8000/sentiment/ATB
```
Returns: `{symbol, score, label, mentions, company}`

### Get All Stocks  
```
GET http://localhost:8000/sentiment/all
```
Returns: `{count, data: [{symbol, score, label, mentions}, ...]}`

### Get Articles
```
GET http://localhost:8000/articles
```
Returns: `{count, articles: [{title, source, mentions, date}, ...]}`

### Get Stats
```
GET http://localhost:8000/stats
```
Returns: `{total_companies, mentioned, neutral, articles, cached_at}`

### Refresh Cache
```
POST http://localhost:8000/refresh
```
Returns: `{status, timestamp}`

## Sentiment Scores

- **-1.0 to -0.1**: Negative
- **-0.1 to 0.1**: Neutral
- **0.1 to 1.0**: Positive

## Integration (Python)

```python
import requests

# One stock
r = requests.get("http://localhost:8000/sentiment/ATB")
score = r.json()['score']

# All stocks
r = requests.get("http://localhost:8000/sentiment/all")
all_stocks = r.json()['data']
```

## Status: ✅ READY FOR PRODUCTION
