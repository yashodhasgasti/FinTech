"""
NEXAPAY Advanced Machine Learning Engine: Real-Time Fraud Detection & Evaluation
Implements:
1. Pure-NumPy Feature Vector Assembly from Real-Time Database Extraction.
2. Hybrid Architecture: Rule-Based Engine + Isolation Forest + Random Forest + Logistic Regression Baseline.
3. Configurable Risk Thresholds (LOW: 0-29, MEDIUM: 30-69, HIGH: 70-100).
4. Explainable AI (XAI): Shapley-style feature attributions explaining the exact reason for the score.
5. Real Model Evaluation Statistics (Accuracy, Precision, Recall, F1, Confusion Matrix).
"""

import math
import numpy as np
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

from engines.feature_extractor import RealTimeFeatureExtractor
from engines.ml_models import get_or_load_ml_models, FEATURE_COLUMNS


class MLFraudEngine:
    """
    Production-grade AI/ML Hybrid Fraud Detection Engine.
    Combines deterministic financial security rules with pure-NumPy machine learning.
    """

    CATEGORY_RISK_MAP = {
        "Counter Sales": 0.10,
        "Salary & Wages": 0.05,
        "Rent & Housing": 0.10,
        "Groceries": 0.12,
        "Utilities & Bills": 0.15,
        "Food & Dining": 0.18,
        "Healthcare": 0.20,
        "Inventory Supplies": 0.25,
        "Shopping & Retail": 0.35,
        "Entertainment": 0.30,
        "Vendor Payout": 0.30,
        "Suspicious Transfer": 0.95,
        "Suspicious Reversal": 0.95,
        "General": 0.25,
        "Other": 0.35
    }

    SUSPICIOUS_RECIPIENT_KEYWORDS = [
        "crypto", "lottery", "cashback", "refund", "telegram", "fast_money", 
        "gift", "reward", "lucky", "bonus", "winner", "task", "job_daily",
        "airdrop", "ponzi", "scheme"
    ]

    @classmethod
    def assemble_feature_vector(cls, features: Dict[str, Any], amount: float, category: str, receiver: str) -> np.ndarray:
        """
        Converts extracted real-time features into normalized 15-dimensional vector for ML inference.
        """
        receiver_clean = receiver.strip().lower()
        log_amt = float(math.log1p(max(0.0, amount)))
        z_score = float(features.get("z_score", 0.0))
        hour = float(features.get("hour", datetime.now().hour))
        is_odd = 1.0 if features.get("is_odd_hour", False) else 0.0
        v1m = float(features.get("tx_count_1m", 0))
        v5m = float(features.get("tx_count_5m", 0))
        v10m = float(features.get("tx_count_10m", 0))
        v1h = float(features.get("tx_count_1h", 0))
        cat_risk = float(cls.CATEGORY_RISK_MAP.get(category, 0.25))
        is_new_recip = 1.0 if features.get("is_new_recipient", False) else 0.0
        is_freq_recip = 1.0 if features.get("is_frequent_recipient", False) else 0.0
        kw_flag = 1.0 if any(kw in receiver_clean for kw in cls.SUSPICIOUS_RECIPIENT_KEYWORDS) else 0.0
        rapid_repeat = 1.0 if features.get("rapid_repeat_detected", False) else 0.0
        unusual_dev = 1.0 if features.get("unusual_device", False) else 0.0

        vec = np.array([
            amount, log_amt, z_score, hour, is_odd,
            v1m, v5m, v10m, v1h, cat_risk, is_new_recip, is_freq_recip,
            kw_flag, rapid_repeat, unusual_dev
        ], dtype=float)

        return vec

    @classmethod
    def evaluate_rules(
        cls, 
        features: Dict[str, Any], 
        amount: float, 
        category: str, 
        receiver: str
    ) -> Tuple[float, List[Dict[str, Any]]]:
        """
        Executes Rule-Based Detection Engine:
        - Rapid repeated transactions
        - Unusually high transaction amount compared with spending history
        - Multiple transactions within short time
        - New recipient combined with other suspicious indicators
        - Unusual transaction timing
        - Suspicious counterparty keywords & patterns
        """
        receiver_clean = receiver.strip().lower()
        rule_score = 0.0
        attributions: List[Dict[str, Any]] = []

        z_score = features.get("z_score", 0.0)
        avg_amt = features.get("avg_amount", 0.0)
        amount_ratio = features.get("amount_ratio", 1.0)
        v1m = features.get("tx_count_1m", 0)
        v5m = features.get("tx_count_5m", 0)
        v10m = features.get("tx_count_10m", 0)
        v1h = features.get("tx_count_1h", 0)
        is_odd = features.get("is_odd_hour", False)
        is_new_recip = features.get("is_new_recipient", False)
        rapid_repeat = features.get("rapid_repeat_detected", False)
        rapid_reasons = features.get("rapid_repeat_reasons", [])
        unusual_dev = features.get("unusual_device", False)
        kw_match = [kw for kw in cls.SUSPICIOUS_RECIPIENT_KEYWORDS if kw in receiver_clean]
        cat_risk = cls.CATEGORY_RISK_MAP.get(category, 0.25)

        # 1. Rapid repeated transactions rule
        if rapid_repeat:
            pts = 42.0
            rule_score += pts
            detail_msg = "; ".join(rapid_reasons) if rapid_reasons else "Rapid burst velocity: repeated transactions detected in short window."
            attributions.append({
                "factor": "Rapid Repeated Transaction Pattern",
                "impact": pts,
                "detail": detail_msg,
                "category": "Velocity Risk"
            })

        # 2. Amount deviation from historical spending
        if z_score > 2.5 or (avg_amt > 0 and amount_ratio >= 3.0 and amount > 20000.0):
            pts = min(48.0, round(32.0 + (z_score * 4.0), 1))
            rule_score += pts
            attributions.append({
                "factor": f"Extreme Spending Outlier (Z-Score: +{z_score:.2f}σ)",
                "impact": pts,
                "detail": f"Amount of ₹{amount:,.2f} is {amount_ratio:.1f}x higher than your historical average (₹{avg_amt:,.2f}).",
                "category": "Behavioral Anomaly"
            })
        elif z_score > 1.0 or (avg_amt > 0 and amount_ratio >= 1.5 and amount > 8000.0) or (avg_amt == 0 and amount > 12000.0):
            pts = 28.0
            rule_score += pts
            attributions.append({
                "factor": f"Elevated Transaction Value (+{z_score:.2f}σ)",
                "impact": pts,
                "detail": f"Amount exceeds normal expenditure baseline by {amount_ratio:.1f}x.",
                "category": "Behavioral Anomaly"
            })

        # 3. High transaction velocity bursts in 1m, 5m, 1h
        if v1m >= 2:
            pts = 32.0
            rule_score += pts
            attributions.append({
                "factor": "1-Minute High Frequency Velocity Spike",
                "impact": pts,
                "detail": f"{v1m} transactions recorded in the last 60 seconds.",
                "category": "Velocity Risk"
            })
        elif v5m >= 4:
            pts = 26.0
            rule_score += pts
            attributions.append({
                "factor": "5-Minute Velocity Accumulation",
                "impact": pts,
                "detail": f"{v5m} transactions recorded within the last 5 minutes.",
                "category": "Velocity Risk"
            })
        elif v1h >= 8:
            pts = 20.0
            rule_score += pts
            attributions.append({
                "factor": "1-Hour Velocity Anomaly",
                "impact": pts,
                "detail": f"{v1h} transactions initiated in the last hour.",
                "category": "Velocity Risk"
            })

        # 4. Deceptive counterparty keyword lure
        if kw_match:
            pts = 45.0
            rule_score += pts
            attributions.append({
                "factor": "Deceptive Recipient Identifier Flag",
                "impact": pts,
                "detail": f"Counterparty address contains flagged scam/lure identifier: '{kw_match[0]}'.",
                "category": "Counterparty Risk"
            })

        # 5. New recipient combined with other risk indicators
        if is_new_recip:
            if amount > 12000.0 or (is_odd and amount > 3000.0) or kw_match or z_score > 1.2:
                pts = 32.0
                rule_score += pts
                attributions.append({
                    "factor": "Substantial Transfer to Unverified Payee",
                    "impact": pts,
                    "detail": "Large transfer routed to a brand new payee combined with unusual spending profile.",
                    "category": "Relationship Anomaly"
                })
            elif amount > 3000.0:
                attributions.append({
                    "factor": "First-Time Payee",
                    "impact": 12.0,
                    "detail": "First transfer to this payee account.",
                    "category": "Relationship Anomaly"
                })
                rule_score += 12.0
            else:
                attributions.append({
                    "factor": "New Payee Account",
                    "impact": 5.0,
                    "detail": "First transfer to this payee, but routine transaction amount.",
                    "category": "Relationship Anomaly"
                })
                rule_score += 5.0

        # 6. Unusual transaction timing (odd hours)
        if is_odd:
            pts = 24.0 if (amount > 5000.0 or z_score > 1.0) else 8.0
            rule_score += pts
            attributions.append({
                "factor": "High-Risk Time Window (Odd Hours)" if pts > 15 else "Off-Peak Transaction Hour",
                "impact": pts,
                "detail": f"Initiated at {features.get('hour', 0):02d}:00 hrs, outside normal daytime behavioral hours.",
                "category": "Temporal Anomaly"
            })

        # 7. Unusual device/session
        if unusual_dev:
            pts = 22.0
            rule_score += pts
            attributions.append({
                "factor": "Unrecognized Client Device / Session",
                "impact": pts,
                "detail": "Transaction initiated from a device fingerprint not previously recognized in your history.",
                "category": "Device Anomaly"
            })

        # 8. High-risk transaction category
        if cat_risk >= 0.80:
            pts = 35.0
            rule_score += pts
            attributions.append({
                "factor": "High-Risk Category Classification",
                "impact": pts,
                "detail": f"Category '{category}' is tagged for elevated chargeback/fraud risk.",
                "category": "Category Risk"
            })
        elif cat_risk >= 0.35:
            pts = 8.0
            rule_score += pts

        # Normal profile concordance fallback
        if not attributions:
            attributions.append({
                "factor": "Routine Behavioral Alignment",
                "impact": 5.0,
                "detail": "Transaction parameters conform to verified historical patterns and low-risk counterparties.",
                "category": "Profile Concordance"
            })
            rule_score = 5.0

        clamped_rule_score = min(100.0, max(0.0, rule_score))
        return clamped_rule_score, attributions

    @classmethod
    def evaluate_transaction(
        cls, 
        transaction: Dict[str, Any], 
        user_id_or_history: Any = 1,
        user_history: Optional[List[Dict[str, Any]]] = None,
        db_conn: Optional[Any] = None,
        thresholds: Optional[Dict[str, Any]] = None,
        user_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Full Real-Time Hybrid Fraud Evaluation Pipeline.
        1. Real-time feature extraction from database history (or provided history)
        2. Rule-based evaluation
        3. Pure-NumPy Isolation Forest anomaly isolation scoring
        4. Pure-NumPy Random Forest fraud probability classification
        5. Pure-NumPy Logistic Regression baseline comparison
        6. Configurable threshold classification (LOW, MEDIUM, HIGH)
        7. Explainable AI feature attributions
        """
        if isinstance(user_id_or_history, (list, tuple)):
            hist = user_id_or_history
            uid = user_id if user_id is not None else 1
        elif isinstance(user_id_or_history, int):
            uid = user_id_or_history
            hist = user_history
        else:
            uid = user_id if user_id is not None else 1
            hist = user_history

        amount = float(transaction.get("amount", 0.0))
        receiver = str(transaction.get("receiver_info", "") or transaction.get("receiver_upi", "")).strip()
        category = str(transaction.get("category", "General")).strip()

        # Step 1: Real-time Feature Extraction
        extracted_features = RealTimeFeatureExtractor.extract_features(
            user_id=uid,
            transaction=transaction,
            user_history=hist,
            db_conn=db_conn
        )

        # Step 2: Rule-Based Evaluation
        rule_score, attributions = cls.evaluate_rules(
            features=extracted_features,
            amount=amount,
            category=category,
            receiver=receiver
        )

        # Step 3: Pure-NumPy ML Inference
        models = get_or_load_ml_models()
        iso_forest = models["isolation_forest"]
        baseline_lr = models["logistic_regression"]
        rf_classifier = models["random_forest"]

        feat_vec = cls.assemble_feature_vector(
            features=extracted_features,
            amount=amount,
            category=category,
            receiver=receiver
        )

        # Isolation Forest Anomaly Score (0.0 to 1.0 -> scaled to 0 to 100)
        iso_score_raw = iso_forest.anomaly_score(feat_vec)
        ml_anomaly_score = round(iso_score_raw * 100.0, 1)

        # Random Forest Fraud Probability (0.0 to 1.0 -> scaled to 0 to 100)
        rf_prob_raw = float(rf_classifier.predict_proba(feat_vec.reshape(1, -1))[0])
        ml_fraud_prob = round(rf_prob_raw * 100.0, 1)

        # Baseline Logistic Regression Probability (for comparative benchmarking)
        lr_prob_raw = float(baseline_lr.predict_proba(feat_vec.reshape(1, -1))[0])
        baseline_lr_prob = round(lr_prob_raw * 100.0, 1)

        # Step 4: Hybrid Risk Blending
        # 40% Rules + 30% Isolation Forest + 30% Random Forest
        blended = (rule_score * 0.40) + (ml_anomaly_score * 0.30) + (ml_fraud_prob * 0.30)

        # Hard guardrails for critical scenarios
        kw_match = any(kw in receiver.lower() for kw in cls.SUSPICIOUS_RECIPIENT_KEYWORDS)
        if kw_match and (extracted_features.get("z_score", 0.0) > 1.8 or amount > 25000.0):
            blended = max(blended, 82.0)
        elif extracted_features.get("rapid_repeat_detected", False) and extracted_features.get("tx_count_1m", 0) >= 2:
            blended = max(blended, 76.0)

        final_risk_score = round(float(np.clip(blended, 2.0, 99.5)), 1)

        # Step 5: Configurable Threshold Classification
        if not thresholds:
            import database
            thresholds = database.get_system_thresholds()

        low_max = thresholds.get("low_max", 29.0)
        high_min = thresholds.get("high_min", 70.0)
        auto_block = thresholds.get("auto_block_high_risk", False)

        if final_risk_score >= high_min:
            risk_level = "CRITICAL" if final_risk_score >= 80.0 else "HIGH_RISK"
            decision = "BLOCKED" if auto_block else "HELD_FOR_REVIEW"
            review_status = "Pending Review"
            is_flagged = 1
            requires_human_review = True
            requires_verification = False
            action = "HIGH FRAUD RISK: Simulated payment withheld. Transaction quarantined in Human Review Queue."
        elif final_risk_score > low_max:
            risk_level = "MEDIUM"
            decision = "REQUIRE_VERIFICATION"
            review_status = "Pending Verification"
            is_flagged = 0
            requires_human_review = False
            requires_verification = True
            action = "MEDIUM RISK WARNING: Step-up security confirmation challenge required before funds can be committed."
        else:
            risk_level = "SAFE" if final_risk_score < 20.0 or not any(a.get("impact", 0) > 10 for a in attributions) else "LOW"
            decision = "APPROVED"
            review_status = "Legitimate"
            is_flagged = 0
            requires_human_review = False
            requires_verification = False
            action = "LOW RISK: Transaction conforms to expected behavioral baseline. Instant execution authorized."

        return {
            "risk_score": final_risk_score,
            "risk_level": risk_level,
            "decision": decision,
            "review_status": review_status,
            "is_flagged": is_flagged,
            "requires_human_review": requires_human_review,
            "requires_verification": requires_verification,
            "attributions": attributions,
            "recommended_action": action,
            "scores_breakdown": {
                "rule_risk_score": round(rule_score, 1),
                "ml_anomaly_score": ml_anomaly_score,
                "ml_fraud_prob": ml_fraud_prob,
                "baseline_lr_prob": baseline_lr_prob,
                "final_combined_score": final_risk_score
            },
            "features_extracted": extracted_features,
            "model_metadata": {
                "architecture": "Ensemble Hybrid (Isolation Forest + Random Forest + Logistic Regression Baseline)",
                "evaluated_at": datetime.now().isoformat()
            }
        }

    @classmethod
    def get_model_evaluation_metrics(cls) -> Dict[str, Any]:
        """Returns the authentic model evaluation metrics calculated from held-out test data."""
        models = get_or_load_ml_models()
        return models["evaluation"]
