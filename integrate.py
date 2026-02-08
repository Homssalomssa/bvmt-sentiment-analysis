"""
Integration script for Windows - Combines analyzer and scraper
"""

import sys
import io

from analyzer import SentimentAnalyzer
from scraper import NewsScraper
from datetime import datetime
import json


class TradingSentimentSystem:
    """Main system that combines sentiment analyzer and news scraper"""

    def __init__(self):
        self.analyzer = SentimentAnalyzer()
        self.scraper = NewsScraper()
        print("Trading Sentiment System initialized (Windows Compatible)")

    def analyze_stock_sentiment(self, symbol, max_articles=5):
        """Analyze sentiment for a specific stock"""
        print(f"\n{'='*60}")
        print(f"ANALYZING: {symbol}")
        print(f"{'='*60}")

        print("Fetching news articles...")
        articles = self.scraper.get_articles_for_stock(symbol, max_articles)

        if not articles:
            print(f"No articles found for {symbol}")
            return self._create_empty_result(symbol)

        print(f"Found {len(articles)} articles")
        print("Analyzing sentiment...")
        analyzed_articles = []
        sentiment_scores = []

        for i, article in enumerate(articles, 1):
            print(f"\n  Article {i}: {article['title'][:50]}...")

            sentiment = self.analyzer.analyze_sentiment(
                article["content"],
                symbol
            )

            article_result = {
                "id": article["id"],
                "title": article["title"],
                "source": article["source"],
                "language": article["language"],
                "published_date": article["published_date"],
                "sentiment_score": sentiment["score"],
                "sentiment_label": sentiment["label"],
                "confidence": sentiment["confidence"],
                "analysis_method": sentiment["method"],
                "positive_keywords": sentiment.get("positive_keywords", 0),
                "negative_keywords": sentiment.get("negative_keywords", 0),
                "explanation": sentiment.get("explanation"),
                "explanation_detail": sentiment.get("explanation_detail"),
            }

            analyzed_articles.append(article_result)
            sentiment_scores.append(sentiment["score"])

            print(f"    Sentiment: {sentiment['label'].upper()} (score: {sentiment['score']:.2f})")
            print(f"    Confidence: {sentiment['confidence']:.2f}")

        overall_score = sum(sentiment_scores) / len(sentiment_scores)

        if overall_score > 0.3:
            overall_label = "POSITIVE"
            emoji = "[+]"
        elif overall_score < -0.3:
            overall_label = "NEGATIVE"
            emoji = "[-]"
        else:
            overall_label = "NEUTRAL"
            emoji = "[=]"

        avg_confidence = sum(a["confidence"] for a in analyzed_articles) / len(analyzed_articles)

        sentiment_counts = {
            "positive": sum(1 for a in analyzed_articles if a["sentiment_label"] == "positive"),
            "negative": sum(1 for a in analyzed_articles if a["sentiment_label"] == "negative"),
            "neutral": sum(1 for a in analyzed_articles if a["sentiment_label"] == "neutral")
        }

        print(f"\n{'='*60}")
        print(f"SUMMARY FOR {symbol}")
        print(f"{'='*60}")
        print(f"{emoji} Overall Sentiment: {overall_label}")
        print(f"Overall Score: {overall_score:.2f}")
        print(f"Confidence: {avg_confidence:.2f}")
        print(f"Articles Analyzed: {len(analyzed_articles)}")
        print(f"Positive Articles: {sentiment_counts['positive']}")
        print(f"Negative Articles: {sentiment_counts['negative']}")
        print(f"Neutral Articles: {sentiment_counts['neutral']}")

        # Overall explanation for API/UI
        overall_explanation = (
            f"Overall {overall_label.lower()} sentiment from {len(analyzed_articles)} articles. "
            f"Distribution: {sentiment_counts['positive']} positive, {sentiment_counts['negative']} negative, {sentiment_counts['neutral']} neutral. "
        )
        if analyzed_articles and analyzed_articles[0].get("explanation"):
            overall_explanation += f"Example: {analyzed_articles[0]['explanation']}"

        result = {
            "symbol": symbol,
            "overall_score": round(overall_score, 3),
            "sentiment": overall_label.lower(),
            "sentiment_emoji": emoji,
            "confidence": round(avg_confidence, 3),
            "articles_analyzed": len(analyzed_articles),
            "sentiment_distribution": sentiment_counts,
            "overall_explanation": overall_explanation,
            "analysis_timestamp": datetime.now().isoformat(),
            "articles": analyzed_articles
        }

        return result

    def analyze_multiple_stocks(self, stocks, max_articles_per_stock=3):
        """Analyze sentiment for multiple stocks"""
        print(f"\n{'='*60}")
        print("MULTI-STOCK ANALYSIS")
        print(f"{'='*60}")

        results = {}

        for stock in stocks:
            print(f"\nAnalyzing {stock}...")
            result = self.analyze_stock_sentiment(stock, max_articles_per_stock)
            results[stock] = result

        print(f"\n{'='*60}")
        print("STOCK COMPARISON")
        print(f"{'='*60}")

        print(f"\n{'Stock':<10} {'Sentiment':<12} {'Score':<8} {'Confidence':<12} {'Articles':<10}")
        print("-" * 50)

        for stock, result in results.items():
            print(f"{stock:<10} {result['sentiment'].upper():<12} {result['overall_score']:<8.2f} "
                  f"{result['confidence']:<12.2f} {result['articles_analyzed']:<10}")

        if results:
            best_stock = max(results.items(), key=lambda x: x[1]["overall_score"])
            worst_stock = min(results.items(), key=lambda x: x[1]["overall_score"])
            print(f"\nBEST PERFORMING: {best_stock[0]} ({best_stock[1]['overall_score']:.2f})")
            print(f"WORST PERFORMING: {worst_stock[0]} ({worst_stock[1]['overall_score']:.2f})")

        return results

    def export_results(self, results, filename="sentiment_results.json"):
        """Export results to JSON file"""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\nResults exported to {filename}")

    def _create_empty_result(self, symbol):
        """Create empty result when no articles found"""
        return {
            "symbol": symbol,
            "overall_score": 0.0,
            "sentiment": "neutral",
            "sentiment_emoji": "[=]",
            "confidence": 0.0,
            "articles_analyzed": 0,
            "sentiment_distribution": {"positive": 0, "negative": 0, "neutral": 0},
            "analysis_timestamp": datetime.now().isoformat(),
            "articles": []
        }


def main():
    """Main function to run the system"""
    print("=" * 60)
    print("TUNISIAN STOCK SENTIMENT ANALYSIS SYSTEM")
    print("=" * 60)
    print("Version: Windows Compatible 1.0")
    print("Focus: Tunisian Stock Exchange (BVMT)")
    print("=" * 60)

    system = TradingSentimentSystem()

    print("\n1. TEST INDIVIDUAL STOCK")
    print("-" * 40)
    atb_result = system.analyze_stock_sentiment("ATB", max_articles=3)

    print("\n\n2. TEST MULTIPLE STOCKS")
    print("-" * 40)
    stocks_to_analyze = ["ATB", "TUNTEL", "BH", "STB"]
    all_results = system.analyze_multiple_stocks(stocks_to_analyze, max_articles_per_stock=2)

    print("\n\n3. EXPORT RESULTS")
    print("-" * 40)
    system.export_results(all_results, "stock_sentiment_results.json")

    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE!")
    print("=" * 60)
    print("\nReady for integration with:")
    print("   - Trading Dashboard (Frontend)")
    print("   - Portfolio Manager (Decision Agent)")
    print("   - Price Forecasting System")
    print("\nFiles created:")
    print("   - analyzer.py - Sentiment analysis")
    print("   - scraper.py - News scraping (mock)")
    print("   - integrate.py - Integration system")
    print("   - stock_sentiment_results.json - Results")

    return all_results


if __name__ == "__main__":
    if sys.platform == "win32":
        try:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
        except (AttributeError, OSError):
            pass
    try:
        results = main()
    except Exception as e:
        print(f"\nError: {e}")
        raise
