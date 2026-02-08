# test_frontend_integration.py
import requests
import json
import sys
import io

# Windows: ensure stdout accepts Unicode (emoji, etc.)
if sys.platform == "win32":
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass

BASE_URL = "http://localhost:8001"

# Test API endpoints
print("Testing API endpoints for frontend integration...")

try:
    # 1. Health check
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    response.raise_for_status()
    print(f"✅ Health Check: {response.json()}")

    # 2. Get sentiment for ATB
    response = requests.get(f"{BASE_URL}/sentiment/ATB", timeout=30)
    response.raise_for_status()
    data = response.json()
    print(f"\n✅ ATB Sentiment: {data['sentiment'].upper()} ({data['overall_score']:.2f})")
    print(f"   Articles analyzed: {data['articles_analyzed']}")

    # 3. Get all sentiments
    response = requests.get(f"{BASE_URL}/sentiment/all", timeout=60)
    response.raise_for_status()
    data = response.json()
    print(f"\n✅ All Stocks Analyzed: {len(data['results'])} stocks")

    # Print summary table
    print("\n📊 SENTIMENT SUMMARY:")
    print("-" * 50)
    for stock, sentiment in data["results"].items():
        emoji = "📈" if sentiment["sentiment"] == "positive" else "📉" if sentiment["sentiment"] == "negative" else "📊"
        print(f"{emoji} {stock:<8} {sentiment['sentiment'].upper():<10} Score: {sentiment['overall_score']:.2f}")

    print("\nFrontend integration test passed.")

except requests.exceptions.ConnectionError:
    print("\nError: Could not connect to API at", BASE_URL)
    print("Start the API first: run quick_start.bat -> option 4, or: python api.py")
    sys.exit(1)
except requests.exceptions.Timeout:
    print("\nError: Request timed out. API may be busy.")
    sys.exit(1)
except Exception as e:
    print(f"\nError: {e}")
    sys.exit(1)
