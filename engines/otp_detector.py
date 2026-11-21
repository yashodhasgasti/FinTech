"""
NEXAPAY Module 2: OTP Scam Detector
Identifies social engineering messages and calls designed to harvest OTPs, 
UPI PINs, CVVs, and banking credentials.
"""

import re
from typing import Dict, Any, List
from engines.explainability import ExplainabilityEngine


class OTPScamDetectorEngine:
    # High-risk patterns requesting OTP or PIN
    OTP_PATTERNS = [
        (r"\b(share|send|tell|provide|forward|give)\s+(me\s+)?(your\s+)?(the\s+)?(otp|one[- ]time[- ]password|pin|code|6[- ]digit|4[- ]digit)\b", 
         "Direct OTP Request", 55.0, "Directly demands sharing a confidential one-time password (OTP)."),
        
        (r"\b(enter|type|submit)\s+(your\s+)?(upi\s+)?pin\b.*?\b(receive|get|claim|collect|accept|credit|cashback|refund)\b|\b(receive|get|claim|collect|accept|credit|cashback|refund)\b.*?\b(enter|type|submit)\s+(your\s+)?(upi\s+)?pin\b", 
         "UPI PIN Reverse-Credit Trap", 55.0, "Claims you need to enter your UPI PIN to RECEIVE money. (Golden Rule: UPI PIN is ONLY entered when SENDING money, never receiving!)."),
        
        (r"\b(cvv|card\s*number|expiry\s*date|atm\s*pin)\b", 
         "Debit/Credit Card Data Extraction", 45.0, "Solicits payment card CVV or ATM PIN."),
        
        (r"\b(urgent|immediately|within\s+\d+\s*(hours?|mins?)|blocked\s+today|deactivate|disconnected|power[- ]cut)\b", 
         "Artificial Panic / Urgency Trigger", 30.0, "Fabricates imminent penalty or disconnection to short-circuit critical rational thinking."),
        
        (r"\b(install|download)\s+(anydesk|teamviewer|quicksupport|rustdesk|screen\s*share|apk)\b", 
         "Remote Screen Mirroring Attack", 50.0, "Instructs target to install remote access tools that allow scammers to view incoming SMS OTPs directly."),
        
        (r"\b(bank\s*manager|rbi\s*officer|cyber\s*cell|customs\s*officer|customer\s*care\s*executive|sbi\s*helpdesk|electricity\s*officer)\b", 
         "Authority Impersonation", 35.0, "Impersonates bank, utility, or law enforcement personnel to command trust.")
    ]

    @classmethod
    def scan_message(cls, text: str) -> Dict[str, Any]:
        """
        Evaluates input text for credential and OTP theft patterns.
        """
        if not text or not isinstance(text, str):
            return {
                "risk_score": 0.0,
                "risk_level": "SAFE",
                "summary": "No text provided for analysis."
            }

        text_lower = text.lower()
        feature_impacts: List[Dict[str, Any]] = []
        triggered_rules = []

        for pattern, feature_name, impact, desc in cls.OTP_PATTERNS:
            match = re.search(pattern, text_lower, re.DOTALL)
            if match:
                matched_snippet = match.group(0)[:60]
                feature_impacts.append({
                    "feature": feature_name,
                    "impact": impact,
                    "desc": f"{desc} [Matched: '{matched_snippet}']",
                    "category": "Credential Extraction"
                })
                triggered_rules.append(feature_name)

        # Baseline risk
        base_risk = 5.0
        xai_result = ExplainabilityEngine.calculate_attributions(base_risk, feature_impacts)

        # Generate action recommendation
        if xai_result["risk_level"] in ["HIGH_RISK", "CRITICAL"]:
            recommendation = (
                "CRITICAL WARNING: NEVER SHARE YOUR OTP OR UPI PIN! "
                "Banks and payment providers will NEVER ask for your OTP over phone, SMS, or chat. "
                "Entering a UPI PIN will DEDUCT funds from your account, never add funds."
            )
        elif xai_result["risk_level"] == "CAUTION":
            recommendation = (
                "Be vigilant. The message contains elements of urgency or payment terms. "
                "Verify directly through your official mobile banking application."
            )
        else:
            recommendation = (
                "No active OTP or PIN extraction patterns detected in this text. "
                "Maintain regular security hygiene and never forward authentication codes."
            )

        return {
            "input_text": text,
            "risk_score": xai_result["risk_score"],
            "risk_level": xai_result["risk_level"],
            "badge_color": xai_result["badge_color"],
            "summary": xai_result["summary"],
            "recommendation": recommendation,
            "attributions": xai_result["attributions"],
            "detected_tactics": triggered_rules
        }
