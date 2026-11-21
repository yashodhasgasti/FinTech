"""
NEXAPAY Advanced AI: Transaction Anomaly Detection & Predictive Financial Analytics
Evaluates synthetic transaction streams for anomalous velocity, outlier amounts, 
odd-hour activity, and predictive risk scoring using statistical ML algorithms.
"""

from typing import List, Dict, Any
import numpy as np


class AnomalyDetectionEngine:
    @staticmethod
    def analyze_transaction(
        transaction: Dict[str, Any], 
        history: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calculates anomaly scores for a candidate transaction against historical user baseline.
        """
        amount = float(transaction.get("amount", 0.0))
        hour = int(transaction.get("hour", 14))
        recipient = transaction.get("receiver_upi", "")

        feature_impacts = []
        
        # 1. Historical baseline statistical analysis
        if history and len(history) >= 5:
            past_amounts = np.array([float(tx.get("amount", 0.0)) for tx in history])
            mean_amt = np.mean(past_amounts)
            std_amt = np.std(past_amounts) or 1.0
            
            # Z-Score Calculation
            z_score = (amount - mean_amt) / std_amt
            
            if z_score > 3.0:
                feature_impacts.append({
                    "feature": f"Extreme Amount Outlier (Z-Score: {z_score:.2f})",
                    "impact": min(50.0, z_score * 12.0),
                    "desc": f"Transaction amount (INR {amount:,.2f}) is {z_score:.1f} standard deviations above historical mean (INR {mean_amt:,.2f}).",
                    "category": "Behavioral Anomaly"
                })
            elif z_score > 2.0:
                feature_impacts.append({
                    "feature": f"Moderate Amount Spike (Z-Score: {z_score:.2f})",
                    "impact": 20.0,
                    "desc": f"Amount is significantly higher than your typical average spend.",
                    "category": "Behavioral Anomaly"
                })
        else:
            # Cold start baseline heuristic
            if amount > 50000.0:
                feature_impacts.append({
                    "feature": "High Value New Transaction",
                    "impact": 35.0,
                    "desc": f"Large initial transaction value (INR {amount:,.2f}) requires multi-factor step-up verification.",
                    "category": "High Risk Threshold"
                })

        # 2. Unusual timing (Midnight / Early Morning 1 AM - 5 AM)
        if 1 <= hour <= 5:
            feature_impacts.append({
                "feature": "High-Risk Time Window (Odd Hours)",
                "impact": 22.0,
                "desc": f"Initiated at {hour}:00 hrs, outside normal daytime behavioral patterns.",
                "category": "Temporal Anomaly"
            })

        # 3. New / Unseen VPA check
        if history:
            seen_vpas = {tx.get("receiver_upi") for tx in history}
            if recipient and recipient not in seen_vpas and amount > 10000.0:
                feature_impacts.append({
                    "feature": "High-Value Transfer to First-Time Recipient",
                    "impact": 25.0,
                    "desc": f"Recipient '{recipient}' has no prior transaction history in your profile.",
                    "category": "Relationship Anomaly"
                })

        # Calculate final risk score
        raw_score = sum(f["impact"] for f in feature_impacts)
        clamped_score = min(100.0, raw_score)
        
        is_anomalous = clamped_score >= 50.0

        return {
            "transaction_ref": transaction.get("transaction_ref", "TXN-DEMO"),
            "amount": amount,
            "receiver_upi": recipient,
            "is_anomalous": is_anomalous,
            "anomaly_score": round(clamped_score, 1),
            "risk_level": "CRITICAL" if clamped_score >= 80 else ("HIGH" if clamped_score >= 50 else "NORMAL"),
            "risk_factors": feature_impacts,
            "recommendation": (
                "FRAUD SUSPECT: Trigger secondary biometric or 2FA step-up confirmation before authorizing release of funds." 
                if is_anomalous else "Transaction conforms to expected baseline behavior."
            )
        }

    @staticmethod
    def generate_synthetic_stream(count: int = 20) -> List[Dict[str, Any]]:
        """Generates realistic synthetic financial transactions for live hackathon demonstration."""
        import random
        from datetime import datetime, timedelta

        categories = ["Groceries", "Utility Bill", "Electronics", "P2P Transfer", "Food & Dining", "Travel"]
        vpas = ["merchant@upi", "supermarket@okaxis", "friend@oksbi", "electric@bescom", "unknown_user992@ybl"]
        
        txns = []
        now = datetime.now()
        
        for i in range(count):
            is_fraud_injection = (i % 6 == 0 and i > 0)
            
            if is_fraud_injection:
                amt = round(random.uniform(45000.0, 98000.0), 2)
                hour = random.choice([2, 3, 4])
                vpa = "scammer_mule_account@ybl"
                cat = "P2P Transfer"
            else:
                amt = round(random.uniform(150.0, 2500.0), 2)
                hour = random.choice([10, 12, 14, 16, 18, 20])
                vpa = random.choice(vpas)
                cat = random.choice(categories)

            tx_time = now - timedelta(hours=count - i)
            txns.append({
                "transaction_ref": f"TXN-NEXA-{1000 + i}",
                "amount": amt,
                "receiver_upi": vpa,
                "category": cat,
                "hour": hour,
                "timestamp": tx_time.strftime("%Y-%m-%d %H:%M:%S"),
                "is_synthetic": True
            })
            
        return txns
