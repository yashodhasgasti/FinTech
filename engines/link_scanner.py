"""
NEXAPAY Module 1: AI Link Scanner
Analyzes URLs for phishing, brand impersonation, deceptive TLDs, typosquatting, 
and credential-harvesting patterns with Explainable AI risk scoring.
"""

import math
import re
from urllib.parse import urlparse
from typing import Dict, Any, List
from engines.explainability import ExplainabilityEngine


class LinkScannerEngine:
    # High-risk financial brand names targeted by phishing campaigns
    TARGET_BRANDS = [
        "sbi", "hdfc", "icici", "axis", "pnb", "bob", "kotak",
        "paytm", "phonepe", "gpay", "googlepay", "bhim", "cred",
        "rbi", "incometax", "aadhaar", "uidai", "nsdl", "epfo",
        "paypal", "amazonpay", "bharatpe"
    ]
    
    # Suspicious keywords frequently observed in financial lures
    SUSPICIOUS_KEYWORDS = [
        "kyc", "update", "verify", "secure", "login", "signin",
        "banking", "reward", "cashback", "lottery", "claim", "bonus",
        "refund", "unblock", "suspended", "urgent", "pan", "aadhar",
        "electricity", "bill-pay", "support-desk"
    ]
    
    # Frequently abused free or low-reputation top-level domains
    HIGH_RISK_TLDS = {
        ".xyz", ".top", ".tk", ".ml", ".ga", ".cf", ".gq",
        ".buzz", ".club", ".work", ".loan", ".click", ".link",
        ".icu", ".rest", ".monster", ".fit"
    }

    @staticmethod
    def _calculate_entropy(text: str) -> float:
        """Computes Shannon entropy of string to identify algorithmically generated domains."""
        if not text:
            return 0.0
        entropy = 0.0
        length = len(text)
        freq = {}
        for char in text:
            freq[char] = freq.get(char, 0) + 1
        for count in freq.values():
            p = count / length
            entropy -= p * math.log2(p)
        return round(entropy, 3)

    @classmethod
    def scan_url(cls, url: str) -> Dict[str, Any]:
        """
        Thoroughly analyzes a URL and returns safety risk evaluation with Explainable AI attribution.
        """
        if not url or not isinstance(url, str):
            return {
                "risk_score": 0.0,
                "risk_level": "SAFE",
                "summary": "Empty or invalid URL provided."
            }

        url = url.strip()
        # Ensure scheme for proper urlparse
        parsed_url = url if url.startswith(("http://", "https://")) else "http://" + url
        try:
            parsed = urlparse(parsed_url)
        except Exception:
            return {
                "risk_score": 85.0,
                "risk_level": "HIGH_RISK",
                "summary": "Malformed URL syntax detected."
            }

        netloc = parsed.netloc.lower()
        path = parsed.path.lower()
        query = parsed.query.lower()
        full_path = f"{netloc}{path}?{query}"

        feature_impacts: List[Dict[str, Any]] = []

        # 1. Non-SSL / Insecure HTTP check
        if parsed.scheme == "http":
            feature_impacts.append({
                "feature": "Insecure Protocol (HTTP)",
                "impact": 15.0,
                "desc": "The link does not use encrypted HTTPS, making transmitted data vulnerable to interception.",
                "category": "Security"
            })

        # 2. Raw IP address used instead of domain
        ip_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?::[0-9]+)?$"
        if re.match(ip_pattern, netloc):
            feature_impacts.append({
                "feature": "Direct IP Host",
                "impact": 35.0,
                "desc": f"Link uses a raw numeric IP address ({netloc}) instead of a registered domain name, typical of rogue phishing servers.",
                "category": "Network"
            })

        # 3. High-risk or abused TLD
        matched_tld = next((tld for tld in cls.HIGH_RISK_TLDS if netloc.endswith(tld)), None)
        if matched_tld:
            feature_impacts.append({
                "feature": f"High-Risk TLD ({matched_tld})",
                "impact": 25.0,
                "desc": f"The domain uses '{matched_tld}', which has an unusually high prevalence in phishing and scam campaigns.",
                "category": "Reputation"
            })

        # 4. Brand Impersonation / Typosquatting in Domain
        found_brands = [b for b in cls.TARGET_BRANDS if b in netloc]
        if found_brands:
            # Check if it is the genuine official domain (e.g. sbi.co.in, onlinesbi.sbi, hdfcbank.com)
            legit_domains = [
                "sbi.co.in", "onlinesbi.sbi", "hdfcbank.com", "icicibank.com", 
                "axisbank.com", "paytm.com", "phonepe.com", "rbi.org.in"
            ]
            is_legit = any(netloc == ld or netloc.endswith("." + ld) for ld in legit_domains)
            
            if not is_legit:
                feature_impacts.append({
                    "feature": "Financial Brand Spoofing",
                    "impact": 40.0,
                    "desc": f"Domain contains brand keyword '{found_brands[0].upper()}' on an unauthorized host name.",
                    "category": "Fraud"
                })

        # 5. Suspicious action/urgency keywords in URL path or query
        found_keywords = [kw for kw in cls.SUSPICIOUS_KEYWORDS if kw in full_path]
        if found_keywords:
            impact_score = min(30.0, len(found_keywords) * 12.0)
            feature_impacts.append({
                "feature": "Phishing Keywords Detected",
                "impact": impact_score,
                "desc": f"URL contains keywords commonly used in lures: {', '.join(found_keywords[:4])}.",
                "category": "Heuristics"
            })

        # 6. Excessive subdomains or hyphens (URL Obfuscation)
        subdomain_parts = netloc.split(".")
        if len(subdomain_parts) > 3:
            feature_impacts.append({
                "feature": "Excessive Subdomains",
                "impact": 15.0,
                "desc": f"Contains {len(subdomain_parts)} domain segments designed to mislead mobile users about the actual destination.",
                "category": "Obfuscation"
            })
            
        hyphen_count = netloc.count("-")
        if hyphen_count >= 2:
            feature_impacts.append({
                "feature": "Multiple Domain Hyphens",
                "impact": 12.0,
                "desc": f"Host has {hyphen_count} hyphens, a technique frequently used to create mimic lookalike URLs.",
                "category": "Obfuscation"
            })

        # 7. Domain character entropy check (DGA - Domain Generation Algorithm)
        entropy = cls._calculate_entropy(netloc.split(".")[0])
        if entropy > 3.6 and len(netloc.split(".")[0]) > 8:
            feature_impacts.append({
                "feature": "High Domain Randomness (DGA)",
                "impact": 20.0,
                "desc": f"High character entropy ({entropy}) indicates algorithmically generated random letters typical of botnets.",
                "category": "AI Heuristics"
            })

        # 8. Suspicious Characters (@ in URL used to trick browsers)
        if "@" in url:
            feature_impacts.append({
                "feature": "URL Credential Embedded (@)",
                "impact": 35.0,
                "desc": "URL uses '@' symbol to mask the real destination server from human inspection.",
                "category": "Obfuscation"
            })

        # Base clean baseline risk
        base_risk = 5.0
        xai_result = ExplainabilityEngine.calculate_attributions(base_risk, feature_impacts)

        # Generate recommendation
        if xai_result["risk_level"] in ["HIGH_RISK", "CRITICAL"]:
            recommendation = (
                "DO NOT OPEN THIS LINK. It exhibits strong patterns of credential theft, "
                "banking impersonation, or malware distribution. Report it immediately."
            )
        elif xai_result["risk_level"] == "CAUTION":
            recommendation = (
                "PROCEED WITH CAUTION. Do not enter passwords, PINs, or banking details. "
                "Verify the domain directly on the organization's official website."
            )
        else:
            recommendation = (
                "The link appears safe based on structural analysis. "
                "Always confirm HTTPS security before entering any sensitive details."
            )

        return {
            "target": url,
            "domain": netloc,
            "risk_score": xai_result["risk_score"],
            "risk_level": xai_result["risk_level"],
            "badge_color": xai_result["badge_color"],
            "summary": xai_result["summary"],
            "recommendation": recommendation,
            "attributions": xai_result["attributions"],
            "entropy": entropy
        }
