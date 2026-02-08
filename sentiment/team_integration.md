# Team Integration Guide – BVMT Sentiment Module

Quick instructions for **Persons 1, 2, and 4** to integrate with the Sentiment Analysis module (Person 3).

---

## 1. Getting the code

```cmd
git clone https://github.com/Homssalomssa/bvmt-sentiment-analysis.git
cd bvmt-sentiment-analysis
```

Then run **setup.bat** (or `python -m venv venv` and `pip install -r requirements.txt`).

---

## 2. Running the API

From the repo folder:

```cmd
venv\Scripts\activate
python api.py
```

- API base URL: **http://localhost:8001**
- Docs: **http://localhost:8001/docs**

Keep this terminal open while others use the API.

---

## 3. Endpoints you need

| Your role   | Use this |
|------------|----------|
| Person 1 (Frontend) | `GET /sentiment/{symbol}` and `GET /sentiment/all` for scores and explanations |
| Person 2 (Decision agent) | Same; use `overall_score`, `confidence`, `overall_explanation`, `explanation_detail.recommendation` |
| Person 4 (Forecasting) | Same; use scores and explanations as features or filters |

---

## 4. Response shape (summary)

- **`symbol`** – Stock ticker (e.g. ATB, TUNTEL, BH).
- **`overall_score`** – Number from -1 (negative) to 1 (positive).
- **`sentiment`** – `"positive"` | `"negative"` | `"neutral"`.
- **`confidence`** – 0–1.
- **`overall_explanation`** – Short text summary.
- **`articles`** – List of analyzed articles; each has `sentiment_score`, `sentiment_label`, `explanation`, `explanation_detail` (with `intensity`, `key_findings`, `recommendation`).

---

## 5. Example: fetch sentiment in your app

**JavaScript (fetch):**

```javascript
const res = await fetch('http://localhost:8001/sentiment/ATB');
const data = await res.json();
console.log(data.sentiment, data.overall_score, data.overall_explanation);
```

**Python (requests):**

```python
import requests
r = requests.get('http://localhost:8001/sentiment/ATB')
data = r.json()
print(data['sentiment'], data['overall_score'], data['overall_explanation'])
```

---

## 6. Testing the API from your machine

1. Start the API in the sentiment repo: `python api.py`.
2. In another terminal (or from your app): run `python test_frontend_integration.py` from the sentiment repo, or call the same URLs from your frontend/backend.

---

## 7. Troubleshooting

| Issue | What to do |
|-------|------------|
| Connection refused | Start the API in this repo: `python api.py`. |
| Module not found | Activate venv and install deps: `venv\Scripts\activate` then `pip install -r requirements.txt`. |
| Port 8001 in use | Change port in `api.py`: `uvicorn.run(..., port=8002)`. |

For more detail, see **README.md** in the same repo.
