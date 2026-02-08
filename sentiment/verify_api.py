#!/usr/bin/env python3
"""
Test script - Run this to verify API is working
"""

import time
import requests
import json
import subprocess
import sys
from threading import Thread

def run_server():
    """Run API server"""
    subprocess.run([
        sys.executable, "-m", "uvicorn", 
        "api:app", 
        "--host", "127.0.0.1", 
        "--port", "8000",
        "--log-level", "error"
    ])

def test_api():
    """Test all endpoints"""
    base = "http://localhost:8000"
    
    # Wait for server
    print("Waiting for server...")
    for i in range(15):
        try:
            requests.get(f"{base}/", timeout=1)
            print("✓ Server ready\n")
            break
        except:
            time.sleep(1)
    else:
        print("✗ Server didn't start")
        return False
    
    tests = [
        ("GET", "/", "Root"),
        ("GET", "/sentiment/ATB", "ATB sentiment"),
        ("GET", "/sentiment/STB", "STB sentiment"),
        ("GET", "/sentiment/all", "All stocks (shows first 5)"),
        ("GET", "/articles", "Articles (shows first 1)"),
        ("GET", "/stats", "Statistics"),
    ]
    
    print("=" * 70)
    print("API ENDPOINT TESTS")
    print("=" * 70 + "\n")
    
    passed = 0
    for method, endpoint, desc in tests:
        url = f"{base}{endpoint}"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✓ {method:4} {endpoint:20} {desc}")
                
                # Show sample data
                if endpoint == "/sentiment/ATB":
                    print(f"  → Score: {data['score']}, Label: {data['label']}")
                elif endpoint == "/sentiment/all":
                    print(f"  → {data['count']} stocks total")
                    if data['data']:
                        print(f"  → Top: {data['data'][0]['symbol']} ({data['data'][0]['mentions']} mentions)")
                elif endpoint == "/articles":
                    print(f"  → {data['count']} articles found")
                elif endpoint == "/stats":
                    print(f"  → {data['mentioned']} mentioned, {data['neutral']} neutral")
                
                passed += 1
            else:
                print(f"✗ {method:4} {endpoint:20} Status: {response.status_code}")
        except Exception as e:
            print(f"✗ {method:4} {endpoint:20} Error: {str(e)[:50]}")
    
    print("\n" + "=" * 70)
    print(f"Results: {passed}/{len(tests)} tests passed")
    print("=" * 70 + "\n")
    
    return passed == len(tests)

if __name__ == "__main__":
    print("\n" + "█" * 70)
    print("█ BVMT SENTIMENT ANALYSIS API - TEST SUITE")
    print("█" * 70 + "\n")
    
    # Start server in background
    print("Starting API server...")
    server_thread = Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Run tests
    success = test_api()
    
    if success:
        print("✅ API IS READY FOR PRODUCTION\n")
        print("To start the server for your stock predictor:")
        print("  python -m uvicorn api:app --host 127.0.0.1 --port 8000\n")
        print("Then call:")
        print("  GET http://localhost:8000/sentiment/{symbol}  - Get one stock")
        print("  GET http://localhost:8000/sentiment/all       - Get all stocks")
        print("  GET http://localhost:8000/articles            - Get articles")
        sys.exit(0)
    else:
        print("❌ Some tests failed")
        sys.exit(1)
