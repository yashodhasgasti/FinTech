"""
NEXAPAY Module 3: SMS & WhatsApp Message Scanner
Identifies and categorizes modern digital scams (Utility power cut, Work-From-Home traps, 
KBC lotteries, KYC suspension, Digital Arrest, and Courier fraud).
"""

import re
from typing import Dict, Any, List
from engines.explainability import ExplainabilityEngine
from engines.link_scanner import LinkScannerEngine


class MessageScannerEngine:
    # Scam taxonomies with distinctive heuristic signatures
    SCAM_TAXONOMY = {
        "PART_TIME_JOB": {
            "name": "Part-Time Task / Telegram Job Scam",
            "regex": r"\b(part[- ]time|work\s+from\s+home|earn\s+\d+|daily\s+income|youtube\s+like|hotel\s+rating|t\.me/|telegram)\b",
            "keywords": ["part-time", "daily", "salary", "youtube", "task", "telegram", "earn", "bonus"],
            "advice": "Legitimate employers never pay via Telegram for liking videos or rating products. This is a Ponzi-style task scam."
        },
        "ELECTRICITY_UTILITY": {
            "name": "Electricity / Utility Disconnection Scam",
            "regex": r"\b(electricity|power|power-cut|light)\s+(will\s+be\s+)?(disconnected|cut|suspended)\s+(tonight|at\s+\d+|today)\b",
            "keywords": ["electricity", "power", "disconnected", "bill", "officer", "eb office", "meter"],
            "advice": "Power departments never send unofficial SMS threatening disconnection tonight or giving personal mobile numbers. Pay bills solely through official utility portals."
        },
        "KYC_SUSPENSION": {
            "name": "Bank KYC / Account Suspension Scam",
            "regex": r"\b(kyc|pan|aadhaar|account\s+blocked|dormant|deactivated|update\s+kyc)\b",
            "keywords": ["kyc", "pan", "deactivated", "unblock", "suspended", "banking", "sbi", "hdfc"],
            "advice": "Banks NEVER send SMS links to complete KYC. KYC verification must be done via your official netbanking portal or bank branch."
        },
        "LOTTERY_PRIZE": {
            "name": "Lottery / KBC / Prize Winner Scam",
            "regex": r"\b(congratulations|lucky\s+draw|kbc|won|winner|25\s*lakh|cash\s*prize)\b",
            "keywords": ["congratulations", "lucky", "prize", "won", "reward", "lottery"],
            "advice": "You cannot win a lottery you never entered. Never pay 'processing fees' or 'GST' to claim bogus lottery winnings."
        },
        "DIGITAL_ARREST": {
            "name": "Digital Arrest / Fake Law Enforcement Scam",
            "regex": r"\b(cbi|trai|police|customs|digital\s*arrest|narcotics|arrest\s*warrant|money\s*laundering)\b",
            "keywords": ["cbi", "police", "customs", "arrest", "narcotics", "court", "warrant"],
            "advice": "Indian law enforcement agencies NEVER place individuals under 'digital arrest' or demand money via video calls. Disconnect immediately."
        },
        "PARCEL_COURIER": {
            "name": "Parcel / Courier Delivery Scam",
            "regex": r"\b(india\s*post|fedex|dhl|parcel|package|delivery\s+failed|incomplete\s+address)\b",
            "keywords": ["parcel", "delivery", "post", "address", "package", "consignment"],
            "advice": "Postal services do not ask for card details to re-schedule deliveries. Check the tracking number on the official carrier website."
        }
    }

    @classmethod
    def scan_message(cls, text: str) -> Dict[str, Any]:
        """
        Parses an SMS, WhatsApp, or chat message for fraud classification, embedded links, 
        phone numbers, and security risks.
        """
        if not text or not isinstance(text, str):
            return {
                "risk_score": 0.0,
                "risk_level": "SAFE",
                "summary": "No message content provided."
            }

        text_lower = text.lower()
        feature_impacts: List[Dict[str, Any]] = []
        detected_categories: List[Dict[str, str]] = []

        # 1. Identify scam categories based on regex and keyword frequency
        for category_id, info in cls.SCAM_TAXONOMY.items():
            matched_regex = bool(re.search(info["regex"], text_lower))
            keyword_matches = [kw for kw in info["keywords"] if kw in text_lower]
            
            if matched_regex or len(keyword_matches) >= 2:
                impact = 50.0 if matched_regex else 30.0
                feature_impacts.append({
                    "feature": f"Scam Signature: {info['name']}",
                    "impact": impact,
                    "desc": f"Matches characteristic syntax and vocabulary of {info['name']}.",
                    "category": "Scam Pattern"
                })
                detected_categories.append({
                    "id": category_id,
                    "name": info["name"],
                    "advice": info["advice"]
                })

        # 2. Check for Telegram or unverified communication redirection
        if "t.me/" in text_lower or "telegram" in text_lower:
            feature_impacts.append({
                "feature": "Telegram Group Redirection",
                "impact": 25.0,
                "desc": "Redirects users to unregulated encrypted messaging groups commonly used to evade law enforcement tracing.",
                "category": "Channel Risk"
            })

        # 3. Extract embedded URLs and scan them with LinkScannerEngine
        url_matches = re.findall(r"https?://[^\s]+|www\.[^\s]+|[a-zA-Z0-9-]+\.(?:xyz|top|buzz|click|tk|link)[^\s]*", text)
        for url in url_matches:
            scan_res = LinkScannerEngine.scan_url(url)
            if scan_res["risk_score"] > 50.0:
                feature_impacts.append({
                    "feature": f"Malicious Embedded Link ({scan_res['domain']})",
                    "impact": 35.0,
                    "desc": f"Contains link with {scan_res['risk_level']} risk level: {scan_res['summary']}",
                    "category": "Malicious URL"
                })

        # 4. Extract unverified contact numbers (e.g., "call officer at 9876543210")
        phone_matches = re.findall(r"(?:\+91[-\s]?)?[6-9]\d{9}", text)
        if phone_matches and detected_categories:
            feature_impacts.append({
                "feature": "Unofficial Contact Number in Alert",
                "impact": 20.0,
                "desc": f"Directs target to call personal mobile number ({phone_matches[0]}) rather than institutional helplines.",
                "category": "Social Engineering"
            })

        # 5. Urgency words
        urgency_words = ["immediate", "today", "tonight", "within 24 hours", "urgent", "last warning"]
        found_urgency = [w for w in urgency_words if w in text_lower]
        if found_urgency:
            feature_impacts.append({
                "feature": "Urgency & Coercion Pressure",
                "impact": 18.0,
                "desc": f"Employs pressure tactic words: '{', '.join(found_urgency)}' to bypass victim skepticism.",
                "category": "Psychological Manipulation"
            })

        # Baseline
        base_risk = 5.0
        xai_result = ExplainabilityEngine.calculate_attributions(base_risk, feature_impacts)

        # Best specific advice
        primary_advice = (
            detected_categories[0]["advice"] 
            if detected_categories 
            else ("Stay vigilant. Never forward suspicious messages or click unverified links.")
        )

        return {
            "message": text,
            "risk_score": xai_result["risk_score"],
            "risk_level": xai_result["risk_level"],
            "badge_color": xai_result["badge_color"],
            "summary": xai_result["summary"],
            "primary_category": detected_categories[0]["name"] if detected_categories else "General Message",
            "all_detected_scams": detected_categories,
            "embedded_urls": url_matches,
            "embedded_phones": phone_matches,
            "attributions": xai_result["attributions"],
            "recommended_action": primary_advice
        }
