"""
NEXAPAY Module 4: QR Code Safety Scanner
Decodes QR codes using OpenCV and inspects UPI payment payloads (upi://pay) 
for merchant spoofing, reverse-payment traps, and suspicious destination VPAs.
"""

import os
import re
from urllib.parse import parse_qs, urlparse
from typing import Dict, Any, List, Optional
import cv2
import numpy as np
from engines.explainability import ExplainabilityEngine
from engines.link_scanner import LinkScannerEngine


class QRScannerEngine:
    # Recognized legitimate merchant handles/banks
    OFFICIAL_MERCHANT_DOMAINS = [
        "okaxis", "okhdfcbank", "okicici", "oksbi", "paytm", 
        "ybl", "ibl", "barodampay", "federal", "airtel"
    ]

    # Sensitive brand names often spoofed on fake QR stickers
    SPOOFED_BRANDS = [
        "electricity", "bescom", "tneb", "torrent", "bses",
        "gas", "indane", "hpcl", "bharatgas", "jalboard",
        "traffic", "police", "challan", "amazon", "flipkart", "refund"
    ]

    @classmethod
    def decode_qr_image(cls, image_path: str) -> Optional[str]:
        """Decodes QR code from an image file using OpenCV's QRCodeDetector."""
        if not os.path.exists(image_path):
            return None
        
        try:
            img = cv2.imread(image_path)
            if img is None:
                return None
            detector = cv2.QRCodeDetector()
            data, _, _ = detector.detectAndDecode(img)
            return data if data else None
        except Exception:
            return None

    @classmethod
    def decode_qr_bytes(cls, img_bytes: bytes) -> Optional[str]:
        """Decodes QR code from raw image bytes (e.g., uploaded multipart file)."""
        try:
            nparr = np.frombuffer(img_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if img is None:
                return None
            detector = cv2.QRCodeDetector()
            data, _, _ = detector.detectAndDecode(img)
            return data if data else None
        except Exception:
            return None

    @classmethod
    def inspect_payload(cls, raw_payload: str) -> Dict[str, Any]:
        """
        Inspects decoded QR payload. Can be a UPI deep link, a Web URL, or plain text.
        """
        if not raw_payload or not isinstance(raw_payload, str):
            return {
                "risk_score": 0.0,
                "risk_level": "SAFE",
                "summary": "No QR payload detected or empty code."
            }

        raw_payload = raw_payload.strip()

        # Check if it is a UPI URI
        if raw_payload.lower().startswith("upi://pay"):
            return cls._inspect_upi_uri(raw_payload)

        # Check if it is a standard Web URL
        if raw_payload.startswith(("http://", "https://", "www.")):
            url_res = LinkScannerEngine.scan_url(raw_payload)
            url_res["qr_type"] = "WEB_URL"
            url_res["raw_payload"] = raw_payload
            return url_res

        # Plain text QR
        return {
            "qr_type": "PLAIN_TEXT",
            "raw_payload": raw_payload,
            "risk_score": 5.0,
            "risk_level": "SAFE",
            "badge_color": "#10B981",
            "summary": "Standard text QR code with no payment or web link actions.",
            "recommendation": "Safe to view. No automated payment or browser redirect found.",
            "attributions": []
        }

    @classmethod
    def _inspect_upi_uri(cls, upi_uri: str) -> Dict[str, Any]:
        """Analyzes a UPI deep link for fraudulent payee indicators and reverse payment traps."""
        parsed = urlparse(upi_uri)
        query_params = parse_qs(parsed.query)

        vpa = query_params.get("pa", [""])[0]
        payee_name = query_params.get("pn", [""])[0]
        amount = query_params.get("am", [""])[0]
        note = query_params.get("tn", [""])[0]
        currency = query_params.get("cu", ["INR"])[0]

        feature_impacts: List[Dict[str, Any]] = []

        # 1. Missing or invalid VPA
        if not vpa or "@" not in vpa:
            feature_impacts.append({
                "feature": "Invalid VPA Format",
                "impact": 35.0,
                "desc": "The UPI string lacks a valid Virtual Payment Address (VPA) recipient.",
                "category": "Validation"
            })
        else:
            vpa_user, vpa_handle = vpa.split("@", 1) if "@" in vpa else (vpa, "")
            
            # 2. Check for Merchant Name Spoofing:
            # If the Payee Name claims to be a brand, utility or government office,
            # but the VPA appears to be a personal/individual handle.
            name_lower = payee_name.lower()
            is_claiming_institution = any(brand in name_lower for brand in cls.SPOOFED_BRANDS)
            
            if is_claiming_institution:
                # Scrutinize the VPA username
                digits_in_vpa = len(re.findall(r"\d", vpa_user))
                if digits_in_vpa >= 4 or any(c in vpa_user for c in ["scam", "cash", "loot", "win"]):
                    feature_impacts.append({
                        "feature": "Merchant Identity Spoofing",
                        "impact": 50.0,
                        "desc": f"Payee name claims to be '{payee_name}', but payment points to suspicious personal VPA '{vpa}'.",
                        "category": "Fraud"
                    })

        # 3. Preset Payment Amount Trap
        if amount:
            try:
                amt_val = float(amount)
                if amt_val > 0:
                    feature_impacts.append({
                        "feature": f"Hardcoded Debit Amount (INR {amt_val:,.2f})",
                        "impact": 30.0,
                        "desc": f"Scanning this QR will automatically request to DEBIT INR {amt_val:,.2f} from your bank account! Scammers frequently claim this QR is to receive a refund.",
                        "category": "Financial Risk"
                    })
            except ValueError:
                pass

        # 4. Deceptive transaction note
        note_lower = note.lower()
        if any(term in note_lower for term in ["refund", "cashback", "lottery", "bonus", "reward"]):
            feature_impacts.append({
                "feature": "Deceptive Note Labeling",
                "impact": 25.0,
                "desc": f"Transaction note is labeled '{note}' to fool the user into thinking money is incoming.",
                "category": "Social Engineering"
            })

        base_risk = 5.0
        xai_result = ExplainabilityEngine.calculate_attributions(base_risk, feature_impacts)

        if xai_result["risk_level"] in ["HIGH_RISK", "CRITICAL"]:
            recommendation = (
                "DANGER: DO NOT SCAN OR APPROVE PAYMENT! "
                "This QR code triggers a DEBIT from your account to an unverified or mismatched recipient. "
                "You NEVER need to scan a QR code or enter a PIN to receive funds."
            )
        elif xai_result["risk_level"] == "CAUTION":
            recommendation = (
                f"Verify the recipient carefully. The QR will transfer funds to '{vpa}' ({payee_name or 'Unknown'})."
            )
        else:
            recommendation = (
                f"Standard UPI payment request to {vpa}. Confirm the amount and merchant name on your UPI app screen before entering PIN."
            )

        return {
            "qr_type": "UPI_PAYMENT",
            "raw_payload": upi_uri,
            "vpa": vpa,
            "payee_name": payee_name,
            "amount": amount,
            "currency": currency,
            "note": note,
            "risk_score": xai_result["risk_score"],
            "risk_level": xai_result["risk_level"],
            "badge_color": xai_result["badge_color"],
            "summary": xai_result["summary"],
            "recommendation": recommendation,
            "attributions": xai_result["attributions"]
        }
