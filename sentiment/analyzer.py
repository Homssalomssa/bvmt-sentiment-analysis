"""
Sentiment Analyzer for Tunisian Stock Market News - Windows Compatible
Supports French, Arabic, English. Includes explainability and context-aware scoring.
"""

import re
import sys
import io
from typing import Dict, List, Tuple, Any


def _windows_utf8_stdout():
    if sys.platform == "win32":
        try:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
        except (AttributeError, OSError):
            pass


def _is_arabic_char(c: str) -> bool:
    """Check if character is in Arabic Unicode blocks (Windows compatible)."""
    code = ord(c)
    return (
        0x0600 <= code <= 0x06FF
        or 0x0750 <= code <= 0x077F
        or 0x08A0 <= code <= 0x08FF
        or 0xFB50 <= code <= 0xFDFF
        or 0xFE70 <= code <= 0xFEFF
    )


def get_sentiment_intensity(score: float) -> str:
    """Return human-readable intensity level for a sentiment score."""
    if score > 0.8:
        return "Very strong"
    elif score > 0.6:
        return "Strong"
    elif score > 0.3:
        return "Moderate"
    elif score > 0.1:
        return "Slight"
    elif score >= -0.1:
        return "Neutral"
    elif score >= -0.3:
        return "Slight"
    elif score >= -0.6:
        return "Moderate"
    elif score >= -0.8:
        return "Strong"
    else:
        return "Very strong"


class SentimentAnalyzer:
    def __init__(self):
        """Initialize keyword-based sentiment analyzer (fast, no ML dependencies)"""
        print("Using keyword-based sentiment analyzer (fast for Windows)")

        # French keywords
        self.fr_positive = [
            "bon", "excellent", "positif", "hausse", "croissance",
            "profit", "réussite", "fort", "solide", "augmentation",
            "bénéfice", "dividende", "record", "meilleur", "performance", "performances",
            "progress", "avancée", "succès", "rentable", "gain",
            "supérieur", "excédent", "solde positif", "boni", "excédentaire"
        ]
        self.fr_positive_strong = [
            "excellent", "exceptionnel", "exceptionnels", "record", "records",
            "profit", "profits", "croissance", "succès", "réussite"
        ]

        self.fr_negative = [
            "mauvais", "négatif", "baisse", "perte", "échec",
            "problème", "crise", "faible", "déclin", "chute",
            "déficit", "ralentissement", "risque", "avertissement",
            "difficulté", "challenge", "dette", "perte", "échec",
            "inférieur", "déficitaire", "solde négatif", "mali", "dégressif"
        ]

        # Arabic keywords
        self.ar_positive = [
            "جيد", "ممتاز", "إيجابي", "ارتفاع", "نمو", "ربح", "نجاح",
            "قوي", "متين", "زيادة", "مكسب", "أداء", "قياسي", "توزيع",
            "أفضل", "تقدم", "تطور", "فوز", "مربح", "ربحية",
            "متفوق", "فائض", "رصيد إيجابي", "مكسب", "فائضي"
        ]

        self.ar_negative = [
            "سيء", "سلبي", "انخفاض", "خسارة", "فشل", "مشكلة", "أزمة",
            "ضعيف", "تراجع", "سقوط", "عجز", "تباطؤ", "خطر", "تحذير",
            "صعوبة", "تحدي", "دين", "خسائر", "إخفاق",
            "أدنى", "عاجز", "رصيد سلبي", "خسارة", "منخفض"
        ]

        # English keywords
        self.en_positive = [
            "good", "excellent", "positive", "rise", "growth", "profit",
            "success", "strong", "solid", "increase", "gain", "dividend",
            "record", "improvement", "advance", "achievement", "profitable",
            "superior", "surplus", "positive balance", "bonus", "excess"
        ]

        self.en_negative = [
            "bad", "negative", "fall", "loss", "failure", "problem",
            "crisis", "weak", "decline", "drop", "deficit", "slowdown",
            "risk", "warning", "difficulty", "challenge", "debt", "loss",
            "inferior", "deficit", "negative balance", "loss", "deficient"
        ]

        # Neutral words (do not count as positive or negative)
        self.neutral_words = [
            "stable", "stables", "stabilité", "مستقر", "maintain", "maintenir",
            "maintien", "mixed", "mixte", "مختلط", "significatif", "changement",
            "equal", "équilibré", "balance", "maintained", "maintenue", "stability",
            "maintained", "overall", "résultats", "results", "context"
        ]

        # Context modifiers: phrases that negate or soften nearby sentiment
        self.context_modifiers = [
            "pas de", "pas d'", "sans", "aucun", "aucune", "لا يوجد", "no ", "not ",
            "ni ", "ne ", "n'", "jamais", "never"
        ]

        # Words that are positive only when NOT in neutral context (e.g. "performances stables")
        self.positive_neutral_context_words = ["performance", "performances", "أداء"]

        # Company-specific keywords
        self.company_keywords = {
            "ATB": {
                "positive": ["banque", "bank", "finance", "crédit", "prêt", "dépôt"],
                "negative": ["faillite", "bankruptcy", "défaut", "dette", "crise bancaire"]
            },
            "TUNTEL": {
                "positive": ["télécom", "telecom", "mobile", "data", "internet", "5g"],
                "negative": ["concurrence", "competition", "satellite", "fibre", "interruption"]
            },
            "BH": {
                "positive": ["immobilier", "real estate", "property", "logement", "construction"],
                "negative": ["bulle", "bubble", "marché immobilier", "property crash", "vacant"]
            }
        }

    def detect_language_simple(self, text: str) -> str:
        """Simple language detection for Windows compatibility"""
        if not text:
            return "unknown"
        sample = text[:200]
        if any(_is_arabic_char(c) for c in sample):
            return "ar"
        french_chars = set("éèêëàâäôöûüçÉÈÊËÀÂÄÔÖÛÜÇ")
        if any(c in french_chars for c in sample):
            return "fr"
        return "en"

    def clean_text(self, text: str) -> str:
        """Clean text for analysis"""
        if not text:
            return ""
        text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)
        text = re.sub(r"<.*?>", "", text)
        text = re.sub(r"[^\w\s\u0600-\u06FF\u00C0-\u017F.,!?;:\'-]", " ", text)
        text = " ".join(text.split())
        return text

    def _get_keywords_with_language(self) -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]]]:
        """Return (positive_list, negative_list) where each item is (word, lang)."""
        pos = [(w, "fr") for w in self.fr_positive] + [(w, "fr") for w in self.fr_positive_strong]
        pos = list(dict.fromkeys(pos))  # dedupe
        pos += [(w, "ar") for w in self.ar_positive]
        pos += [(w, "en") for w in self.en_positive]
        neg = [(w, "fr") for w in self.fr_negative]
        neg += [(w, "ar") for w in self.ar_negative]
        neg += [(w, "en") for w in self.en_negative]
        return pos, neg

    def _has_neutral_context_for_performance(self, text_lower: str) -> bool:
        """True if text suggests neutral context (e.g. 'performances stables', 'stable performance')."""
        neutral_indicators = ["stable", "stables", "stabilité", "maintain", "maintien", "pas de changement", "no change", "mixed", "مستقر"]
        return any(n in text_lower for n in neutral_indicators)

    def _apply_context_dampening(self, text_lower: str, positive_count: int, negative_count: int) -> Tuple[int, int]:
        """Reduce counts when negation/context modifiers present."""
        has_modifier = any(m in text_lower for m in self.context_modifiers)
        if not has_modifier:
            return positive_count, negative_count
        # Dampen both so we don't over-penalize; pull toward neutral
        return int(positive_count * 0.7), int(negative_count * 0.7)

    def _build_explanation(
        self,
        positive_found: List[Tuple[str, str, int]],
        negative_found: List[Tuple[str, str, int]],
        neutral_found: List[str],
        normalized_score: float,
        label: str,
        total: int,
        stock_symbol: str = None,
    ) -> Tuple[str, Dict[str, Any]]:
        """Build rich explanation with intensity, key_findings, recommendation."""
        pos_words = [w for w, _, _ in positive_found]
        neg_words = [w for w, _, _ in negative_found]
        pos_count = sum(w for _, _, w in positive_found)
        neg_count = sum(w for _, _, w in negative_found)
        intensity = get_sentiment_intensity(normalized_score)

        # Top terms (by count, then unique)
        def top_terms(items: List[Tuple[str, str, int]], n: int = 5) -> List[str]:
            seen: Dict[str, int] = {}
            for w, _, weight in items:
                seen[w] = seen.get(w, 0) + weight
            sorted_terms = sorted(seen.items(), key=lambda x: -x[1])
            return [t[0] for t in sorted_terms[:n]]

        top_pos = top_terms(positive_found, 5)
        top_neg = top_terms(negative_found, 5)
        top_neutral = list(dict.fromkeys(neutral_found))[:5]

        # Key findings (rich sentences)
        key_findings: List[str] = []
        if pos_count > 0:
            mentions = []
            for w in sorted(set(pos_words))[:5]:
                c = sum(weight for ww, _, weight in positive_found if ww == w)
                if c > 1:
                    mentions.append(f"'{w}' ({c} mentions)")
                else:
                    mentions.append(f"'{w}'")
            key_findings.append("Key positive indicators: " + ", ".join(mentions))
        if neg_count > 0:
            key_findings.append("Negative terms present: " + ", ".join(f"'{w}'" for w in sorted(set(neg_words))[:5]))
        else:
            if label == "positive":
                key_findings.append("No concerning negative terms detected.")
        if neutral_found and (pos_count or neg_count):
            key_findings.append("Neutral/context terms: " + ", ".join(sorted(set(neutral_found))[:4]))

        # Summary sentence
        if total == 0:
            summary = "Neutral sentiment. No strong sentiment keywords found; context suggests stable or mixed outlook."
        elif label == "positive":
            summary = f"{intensity} positive sentiment ({normalized_score:.2f}). Key positive indicators: {', '.join(top_pos[:4])}. " + ("No negative terms detected." if neg_count == 0 else f"Some negative terms ({', '.join(top_neg[:2])}) present.")
        elif label == "negative":
            summary = f"{intensity} negative sentiment ({normalized_score:.2f}). Key negative indicators: {', '.join(top_neg[:4])}. " + ("No positive terms." if pos_count == 0 else f"Some positive terms ({', '.join(top_pos[:2])}) also present.")
        else:
            summary = f"Neutral sentiment ({normalized_score:.2f}). Balanced positive and negative terms. Context suggests stable or mixed performance."

        # Recommendation
        if label == "positive" and normalized_score > 0.5:
            recommendation = "Overall positive outlook for investment consideration."
        elif label == "negative" and normalized_score < -0.5:
            recommendation = "Caution advised; negative indicators present."
        else:
            recommendation = "Mixed or neutral outlook; monitor for further developments."

        # Legacy simple explanation string (backward compatible)
        simple_explanation = summary

        # Detailed breakdown for API (keep existing structure + add new)
        impact_per_hit = 1.0 / total if total else 0
        positive_keywords: List[Dict[str, Any]] = []
        seen_pos: Dict[str, int] = {}
        for word, lang, weight in positive_found:
            key = f"{word}:{lang}"
            if key not in seen_pos:
                seen_pos[key] = len(positive_keywords)
                positive_keywords.append({"word": word, "language": lang, "count": 0, "impact": 0.0})
            positive_keywords[seen_pos[key]]["count"] += weight
        for item in positive_keywords:
            item["impact"] = round(item["count"] * impact_per_hit, 3)

        negative_keywords: List[Dict[str, Any]] = []
        seen_neg: Dict[str, int] = {}
        for word, lang, weight in negative_found:
            key = f"{word}:{lang}"
            if key not in seen_neg:
                seen_neg[key] = len(negative_keywords)
                negative_keywords.append({"word": word, "language": lang, "count": 0, "impact": 0.0})
            negative_keywords[seen_neg[key]]["count"] += weight
        for item in negative_keywords:
            item["impact"] = round(-item["count"] * impact_per_hit, 3)

        lang_pos: Dict[str, int] = {}
        lang_neg: Dict[str, int] = {}
        for _, lang, w in positive_found:
            lang_pos[lang] = lang_pos.get(lang, 0) + w
        for _, lang, w in negative_found:
            lang_neg[lang] = lang_neg.get(lang, 0) + w
        language_analysis: Dict[str, Dict[str, Any]] = {}
        for lang in set(list(lang_pos.keys()) + list(lang_neg.keys())):
            p = lang_pos.get(lang, 0)
            n = lang_neg.get(lang, 0)
            tot = p + n
            lang_score = (p - n) / tot if tot else 0.0
            language_analysis[lang] = {
                "score": round(lang_score, 3),
                "keywords_found": p + n,
                "positive_hits": p,
                "negative_hits": n,
            }

        sector_insights = ""
        if stock_symbol and stock_symbol in self.company_keywords:
            company_data = self.company_keywords[stock_symbol]
            found_sector_pos = [w for w, _, _ in positive_found if w in company_data["positive"]]
            found_sector_neg = [w for w, _, _ in negative_found if w in company_data["negative"]]
            if found_sector_pos or found_sector_neg:
                sector_insights = f"Company-specific keywords for {stock_symbol} contributed: "
                parts = []
                if found_sector_pos:
                    parts.append(f"positive ({', '.join(found_sector_pos)})")
                if found_sector_neg:
                    parts.append(f"negative ({', '.join(found_sector_neg)})")
                sector_insights += "; ".join(parts) + "."

        explanation_detail = {
            "summary": summary,
            "intensity": intensity,
            "key_findings": key_findings,
            "keyword_breakdown": {
                "positive_keywords": positive_keywords,
                "negative_keywords": negative_keywords,
                "positive": {"count": pos_count, "top_terms": top_pos},
                "negative": {"count": neg_count, "top_terms": top_neg},
                "neutral": {"count": len(neutral_found), "top_terms": top_neutral},
            },
            "language_analysis": language_analysis,
            "sector_insights": sector_insights or None,
            "recommendation": recommendation,
        }
        return simple_explanation, explanation_detail

    def analyze_sentiment(self, text: str, stock_symbol: str = None) -> Dict:
        """Analyze sentiment with context awareness; returns score, label, explanation (backward compatible)."""
        cleaned_text = self.clean_text(text)
        if len(cleaned_text) < 10:
            return {
                "score": 0.0,
                "label": "neutral",
                "confidence": 0.0,
                "explanation": "Text too short to analyze.",
                "explanation_detail": None,
                "positive_keywords": 0,
                "negative_keywords": 0,
                "method": "keyword_based",
            }

        text_lower = cleaned_text.lower()
        pos_list, neg_list = self._get_keywords_with_language()
        has_neutral_context = self._has_neutral_context_for_performance(text_lower)

        # Neutral words found (track only, don't add to score)
        neutral_found: List[str] = []
        for w in self.neutral_words:
            if w in text_lower:
                neutral_found.append(w)

        positive_found: List[Tuple[str, str, int]] = []
        negative_found: List[Tuple[str, str, int]] = []

        for word, lang in pos_list:
            # Skip "performance(s)" when text has stable/neutral context
            if word in self.positive_neutral_context_words and has_neutral_context:
                continue
            if word in text_lower:
                n = min(text_lower.count(word), 3)
                positive_found.append((word, lang, n))

        for word, lang in neg_list:
            if word in text_lower:
                n = min(text_lower.count(word), 3)
                negative_found.append((word, lang, n))

        if stock_symbol and stock_symbol in self.company_keywords:
            company_data = self.company_keywords[stock_symbol]
            for word in company_data["positive"]:
                # In neutral context (e.g. "secteur immobilier", "performances stables"), don't count sector terms as positive
                if has_neutral_context:
                    continue
                if word in text_lower:
                    n = min(text_lower.count(word), 3)
                    positive_found.append((word, "company", n * 2))
            for word in company_data["negative"]:
                if word in text_lower:
                    n = min(text_lower.count(word), 3)
                    negative_found.append((word, "company", n * 2))

        positive_count = sum(w for _, _, w in positive_found)
        negative_count = sum(w for _, _, w in negative_found)

        # Context dampening (negation phrases)
        positive_count, negative_count = self._apply_context_dampening(text_lower, positive_count, negative_count)
        total = positive_count + negative_count

        if total == 0:
            summary = "Neutral sentiment. No strong sentiment keywords found; context suggests stable or mixed outlook."
            empty_detail = {
                "summary": summary,
                "intensity": "Neutral",
                "key_findings": ["No sentiment keywords detected; neutral/stable context."],
                "keyword_breakdown": {
                    "positive_keywords": [],
                    "negative_keywords": [],
                    "positive": {"count": 0, "top_terms": []},
                    "negative": {"count": 0, "top_terms": []},
                    "neutral": {"count": len(neutral_found), "top_terms": neutral_found[:5]},
                },
                "language_analysis": {},
                "sector_insights": None,
                "recommendation": "Mixed or neutral outlook; monitor for further developments.",
            }
            return {
                "score": 0.0,
                "label": "neutral",
                "confidence": 0.5,
                "explanation": summary,
                "explanation_detail": empty_detail,
                "positive_keywords": 0,
                "negative_keywords": 0,
                "method": "keyword_based",
            }

        score = (positive_count - negative_count) / total
        normalized_score = max(-1.0, min(1.0, score))

        # Score softening: avoid perfect 1.0 / -1.0
        if abs(normalized_score) > 0.8:
            normalized_score *= 0.9
        # Slight pull toward neutral for very few keywords
        if total < 3:
            normalized_score *= 0.85

        if normalized_score > 0.3:
            label = "positive"
            confidence = min(0.95, 0.5 + abs(normalized_score) * 0.5)
        elif normalized_score < -0.3:
            label = "negative"
            confidence = min(0.95, 0.5 + abs(normalized_score) * 0.5)
        else:
            label = "neutral"
            confidence = 0.5

        explanation, explanation_detail = self._build_explanation(
            positive_found, negative_found, neutral_found,
            normalized_score, label, total, stock_symbol
        )

        return {
            "score": round(normalized_score, 3),
            "label": label,
            "confidence": round(confidence, 3),
            "explanation": explanation,
            "explanation_detail": explanation_detail,
            "positive_keywords": positive_count,
            "negative_keywords": negative_count,
            "method": "keyword_based",
        }


def test_analyzer_windows():
    """Test the sentiment analyzer on Windows"""
    print("=" * 60)
    print("TESTING SENTIMENT ANALYZER (Windows Compatible)")
    print("=" * 60)

    analyzer = SentimentAnalyzer()

    test_cases = [
        {
            "text": "ATB annonce des résultats exceptionnels avec une croissance de 25% et des profits records. C'est une excellente performance pour la banque.",
            "stock": "ATB",
            "expected": "positive",
            "score_range": (0.5, 1.0),
        },
        {
            "text": "تونسيّة للإتصالات تواجه أزمة مالية كبيرة قد تؤدي إلى خسائر فادحة للمساهمين. هذا وضع سلبي للشركة.",
            "stock": "TUNTEL",
            "expected": "negative",
            "score_range": (-1.0, -0.5),
        },
        {
            "text": "BH présente des performances stables dans le secteur immobilier. Pas de changement significatif.",
            "stock": "BH",
            "expected": "neutral",
            "score_range": (-0.2, 0.2),
        },
        {
            "text": "The market shows mixed results with some gains and some losses. Overall stability maintained.",
            "stock": None,
            "expected": "neutral",
            "score_range": (-0.2, 0.2),
        },
    ]

    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}:")
        print(f"Text: {test['text'][:70]}...")
        lang = analyzer.detect_language_simple(test["text"])
        print(f"Detected language: {lang}")
        sentiment = analyzer.analyze_sentiment(test["text"], test["stock"])
        print(f"Sentiment: {sentiment['label'].upper()} (score: {sentiment['score']:.2f})")
        print(f"Intensity: {sentiment.get('explanation_detail', {}).get('intensity', 'N/A')}")
        print(f"Confidence: {sentiment['confidence']:.2f}")
        print(f"Explanation: {sentiment.get('explanation', 'N/A')}")
        print(f"Method: {sentiment['method']}")
        label_ok = sentiment["label"] == test["expected"]
        lo, hi = test.get("score_range", (-1.0, 1.0))
        score_ok = lo <= sentiment["score"] <= hi
        if label_ok and score_ok:
            print("PASS")
        else:
            if not label_ok:
                print(f"Expected label: {test['expected'].upper()}")
            if not score_ok:
                print(f"Expected score in [{lo}, {hi}]")
        print("-" * 50)


if __name__ == "__main__":
    _windows_utf8_stdout()
    test_analyzer_windows()
