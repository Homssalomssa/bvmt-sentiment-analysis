"""
News Scraper for Tunisian Financial News - Windows Compatible
Mock data generator for demo
"""

import random
import sys
import io
from datetime import datetime, timedelta
from typing import List, Dict

def _windows_utf8_stdout():
    if sys.platform == "win32":
        try:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
        except (AttributeError, OSError):
            pass


class NewsScraper:
    def __init__(self):
        """Initialize with Tunisian stock symbols and company names"""
        self.stock_symbols = [
            "ATB", "TUNTEL", "BH", "STB", "AB",
            "ADWYA", "AMS", "CELL", "SIPHAT", "UIB"
        ]

        self.company_data = {
            "ATB": {
                "fr": "Arab Tunisian Bank",
                "ar": "البنك العربي التونسي",
                "sector": "bancaire"
            },
            "TUNTEL": {
                "fr": "Tunisie Telecom",
                "ar": "تونسيّة للإتصالات",
                "sector": "télécommunications"
            },
            "BH": {
                "fr": "Banque de l'Habitat",
                "ar": "البنك العقاري",
                "sector": "bancaire"
            },
            "STB": {
                "fr": "Société Tunisienne de Banque",
                "ar": "البنك التونسي",
                "sector": "bancaire"
            },
            "AB": {
                "fr": "Amen Bank",
                "ar": "بنك آمن",
                "sector": "bancaire"
            },
            "ADWYA": {
                "fr": "Adwya Assurances",
                "ar": "أضواء للتأمين",
                "sector": "assurances"
            },
            "AMS": {
                "fr": "Assurances Maghrébines",
                "ar": "التأمينات المغاربية",
                "sector": "assurances"
            },
            "CELL": {
                "fr": "Cellulose",
                "ar": "السللوز",
                "sector": "industrie"
            },
            "SIPHAT": {
                "fr": "Société Industrielle Pharmaceutique",
                "ar": "الصناعات الدوائية",
                "sector": "pharmaceutique"
            },
            "UIB": {
                "fr": "Union Internationale de Banques",
                "ar": "الاتحاد الدولي للبنوك",
                "sector": "bancaire"
            }
        }

        self.sources = {
            "kapitalis": {
                "name": "Kapitalis",
                "url": "https://kapitalis.com",
                "language": "fr"
            },
            "ilboursa": {
                "name": "IlBoursa",
                "url": "https://ilboursa.com",
                "language": "ar"
            },
            "tunisienumerique": {
                "name": "Tunisie Numérique",
                "url": "https://tunisienumerique.com",
                "language": "fr"
            }
        }

    def _generate_random_date(self, days_back=7):
        """Generate random date within last N days"""
        now = datetime.now()
        random_days = random.randint(0, days_back)
        random_hours = random.randint(0, 23)
        random_minutes = random.randint(0, 59)
        return now - timedelta(days=random_days, hours=random_hours, minutes=random_minutes)

    def _generate_french_article(self, symbol):
        """Generate French article for a stock"""
        templates = [
            (
                f"{self.company_data[symbol]['fr']} annonce des résultats exceptionnels pour le trimestre",
                ["excellent", "positif", "croissance", "profit", "réussite", "record"],
                0.8
            ),
            (
                f"{self.company_data[symbol]['fr']} fait face à des défis dans le secteur {self.company_data[symbol]['sector']}",
                ["défis", "difficultés", "ralentissement", "problème", "crise", "risque"],
                -0.6
            ),
            (
                f"Nouveau contrat pour {self.company_data[symbol]['fr']} avec un partenaire international",
                ["contrat", "partenariat", "accord", "collaboration", "opportunité", "développement"],
                0.7
            ),
            (
                f"{self.company_data[symbol]['fr']} maintient une position stable malgré le contexte économique",
                ["stable", "maintien", "résilient", "équilibre", "pérennité", "durable"],
                0.1
            ),
            (
                f"Baisse des ventes pour {self.company_data[symbol]['fr']} au dernier trimestre",
                ["baisse", "réduction", "déclin", "chute", "perte", "ralentissement"],
                -0.5
            )
        ]

        title_template, keywords, base_score = random.choice(templates)

        content = f"{title_template}. "
        content += f"La société a démontré une performance remarquable dans un environnement complexe. "
        content += f"Les analystes suivent avec attention l'évolution de {self.company_data[symbol]['fr']}. "
        content += f"Le secteur {self.company_data[symbol]['sector']} connaît des transformations importantes. "
        content += f"Les investisseurs anticipent des développements futurs pour l'entreprise."

        return {
            "title": title_template,
            "content": content,
            "keywords": keywords,
            "base_score": base_score
        }

    def _generate_arabic_article(self, symbol):
        """Generate Arabic article for a stock"""
        templates = [
            (
                f"{self.company_data[symbol]['ar']} تعلن عن نتائج استثنائية للربع",
                ["ممتاز", "إيجابي", "نمو", "ربح", "نجاح", "قياسي"],
                0.8
            ),
            (
                f"{self.company_data[symbol]['ar']} تواجه تحديات في قطاع {self.company_data[symbol]['sector']}",
                ["تحديات", "صعوبات", "تباطؤ", "مشكلة", "أزمة", "خطر"],
                -0.6
            ),
            (
                f"عقد جديد لـ {self.company_data[symbol]['ar']} مع شريك دولي",
                ["عقد", "شراكة", "اتفاق", "تعاون", "فرصة", "تطوير"],
                0.7
            ),
            (
                f"{self.company_data[symbol]['ar']} تحافظ على وضع مستقر رغم الظروف الاقتصادية",
                ["مستقر", "ثبات", "مرونة", "توازن", "استدامة", "دائم"],
                0.1
            ),
            (
                f"انخفاض مبيعات {self.company_data[symbol]['ar']} في الربع الأخير",
                ["انخفاض", "تراجع", "هبوط", "خسارة", "عجز", "تباطؤ"],
                -0.5
            )
        ]

        title_template, keywords, base_score = random.choice(templates)

        content = f"{title_template}. "
        content += f"أظهرت الشركة أداءً ملحوظاً في بيئة معقدة. "
        content += f"يتبع المحللون بتأنّ تطورات {self.company_data[symbol]['ar']}. "
        content += f"يشهد قطاع {self.company_data[symbol]['sector']} تحولات كبيرة. "
        content += f"يتوقع المستثمرون تطورات مستقبلية للشركة."

        return {
            "title": title_template,
            "content": content,
            "keywords": keywords,
            "base_score": base_score
        }

    def scrape_news(self, source="all", max_articles=10):
        """Scrape news articles (mock implementation)"""
        print(f"Scraping news from {source} (mock mode)...")

        articles = []
        sources_to_scrape = []

        if source == "all":
            sources_to_scrape = ["kapitalis", "ilboursa"]
        elif source in self.sources:
            sources_to_scrape = [source]
        else:
            sources_to_scrape = ["kapitalis"]

        for source_key in sources_to_scrape:
            source_info = self.sources[source_key]
            language = source_info["language"]
            num_articles = random.randint(2, min(4, max_articles))

            for i in range(num_articles):
                symbol = random.choice(self.stock_symbols)

                if language == "fr":
                    article_data = self._generate_french_article(symbol)
                else:
                    article_data = self._generate_arabic_article(symbol)

                article = {
                    "id": f"{source_key}_{i}_{datetime.now().timestamp()}",
                    "title": article_data["title"],
                    "content": article_data["content"],
                    "source": source_info["name"],
                    "source_url": source_info["url"],
                    "published_date": self._generate_random_date().isoformat(),
                    "scraped_date": datetime.now().isoformat(),
                    "language": language,
                    "mentioned_stocks": [symbol],
                    "keywords": article_data["keywords"],
                    "base_sentiment_score": article_data["base_score"]
                }
                articles.append(article)

        print(f"Generated {len(articles)} mock articles")
        return articles

    def get_articles_for_stock(self, symbol, max_articles=5):
        """Get articles for a specific stock"""
        all_articles = self.scrape_news("all", max_articles * 3)
        symbol_articles = []
        for article in all_articles:
            if symbol.upper() in [s.upper() for s in article["mentioned_stocks"]]:
                symbol_articles.append(article)
            if len(symbol_articles) >= max_articles:
                break
        return symbol_articles

    def extract_stock_symbols(self, text):
        """Extract stock symbols from text"""
        mentioned = []
        text_lower = text.lower()
        for symbol in self.stock_symbols:
            if symbol.lower() in text_lower:
                mentioned.append(symbol)
        for symbol, data in self.company_data.items():
            fr_name_lower = data["fr"].lower()
            if fr_name_lower in text_lower and symbol not in mentioned:
                mentioned.append(symbol)
            if data["ar"] in text and symbol not in mentioned:
                mentioned.append(symbol)
        return list(set(mentioned))


def test_scraper_windows():
    """Test the news scraper on Windows"""
    print("=" * 60)
    print("TESTING NEWS SCRAPER (Windows Compatible)")
    print("=" * 60)

    scraper = NewsScraper()

    print("\n1. French articles from Kapitalis:")
    fr_articles = scraper.scrape_news("kapitalis", 2)
    for i, article in enumerate(fr_articles, 1):
        print(f"  Article {i}: {article['title'][:60]}...")
        print(f"    Stocks: {article['mentioned_stocks']}")
        print(f"    Language: {article['language']}")
        print()

    print("\n2. Arabic articles from IlBoursa:")
    ar_articles = scraper.scrape_news("ilboursa", 2)
    for i, article in enumerate(ar_articles, 1):
        print(f"  Article {i}: {article['title'][:60]}...")
        print(f"    Stocks: {article['mentioned_stocks']}")
        print(f"    Language: {article['language']}")
        print()

    print("\n3. Articles for ATB:")
    atb_articles = scraper.get_articles_for_stock("ATB", 3)
    for i, article in enumerate(atb_articles, 1):
        print(f"  Article {i}: {article['title'][:70]}...")
        print(f"    Source: {article['source']}")
        base = article["base_sentiment_score"]
        sentiment_str = "Positive" if base > 0 else "Negative" if base < 0 else "Neutral"
        print(f"    Base Sentiment: {sentiment_str}")
        print()


if __name__ == "__main__":
    _windows_utf8_stdout()
    test_scraper_windows()
