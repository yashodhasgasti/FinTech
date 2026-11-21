"""
NEXAPAY Real-Time Feature Extraction Engine
Extracts 13 real-time behavioral and transactional features using actual database records and timestamps.
Handles missing historical data safely for new users (cold start).
Zero placeholder values, zero hardcoded transaction counts.
"""

import sqlite3
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple


class RealTimeFeatureExtractor:
    """
    Extracts features for fraud risk evaluation directly from database history.
    """

    @staticmethod
    def _parse_timestamp(ts_val: Any) -> Optional[datetime]:
        """Safely parses timestamp string or object into datetime."""
        if not ts_val:
            return None
        if isinstance(ts_val, datetime):
            return ts_val
        ts_str = str(ts_val).strip()
        for fmt in (
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%d"
        ):
            try:
                return datetime.strptime(ts_str, fmt)
            except ValueError:
                continue
        return None

    @classmethod
    def extract_features(
        cls,
        user_id: int = 1,
        transaction: Optional[Dict[str, Any]] = None,
        user_history: Optional[List[Dict[str, Any]]] = None,
        db_conn: Optional[sqlite3.Connection] = None,
        submission_time: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Calculates all 13 required features using real transaction history for user_id:
        1. Number of transactions in the last 1 minute
        2. Number of transactions in the last 5 minutes
        3. Number of transactions in the last 10 minutes
        4. Number of transactions in the last 1 hour
        5. Average transaction amount
        6. Maximum recent transaction amount
        7. Deviation from the user's normal spending pattern (Z-Score & amount ratio)
        8. Time since the previous transaction (in seconds)
        9. First-time recipient detection
        10. Frequently used recipient detection
        11. Unusual transaction time detection
        12. Rapid repeated transaction detection
        13. Unusual device/session detection
        """
        if transaction is None:
            transaction = {}

        now = submission_time or datetime.now()
        amount = float(transaction.get("amount", 0.0))
        receiver = str(transaction.get("receiver_info", "") or transaction.get("receiver_upi", "")).strip().lower()
        device = str(transaction.get("device_info", "") or transaction.get("session_id", "")).strip()
        category = str(transaction.get("category", "General")).strip()
        hour = int(transaction.get("hour", now.hour))

        history: List[Dict[str, Any]] = []

        if user_history is not None:
            # Use provided history list (e.g. for unit tests or synthetic evaluation)
            for idx, r in enumerate(user_history):
                dt = cls._parse_timestamp(r.get("created_at") or r.get("timestamp")) or (now - timedelta(days=idx+1))
                history.append({
                    "id": r.get("id", idx + 1),
                    "amount": float(r.get("amount", 0.0)),
                    "receiver_info": str(r.get("receiver_info", "") or r.get("receiver_upi", "")).strip().lower(),
                    "txn_type": r.get("txn_type", "EXPENSE"),
                    "category": r.get("category", "General"),
                    "payment_method": r.get("payment_method", "UPI"),
                    "device_info": str(r.get("device_info", "")).strip(),
                    "created_at_dt": dt,
                    "created_at_str": str(dt),
                    "review_status": r.get("review_status", "Legitimate")
                })
        else:
            # Query actual SQLite database records
            close_conn_on_finish = False
            if db_conn is None:
                import database
                db_conn = database.get_db_connection()
                close_conn_on_finish = True

            cursor = db_conn.cursor()
            cursor.execute("""
            SELECT id, amount, receiver_info, txn_type, category, payment_method, 
                   device_info, created_at, review_status
            FROM transactions
            WHERE user_id = ?
            ORDER BY created_at DESC, id DESC
            """, (user_id,))
            raw_rows = cursor.fetchall()

            for r in raw_rows:
                dt = cls._parse_timestamp(r["created_at"])
                if dt:
                    history.append({
                        "id": r["id"],
                        "amount": float(r["amount"]),
                        "receiver_info": str(r["receiver_info"] or "").strip().lower(),
                        "txn_type": r["txn_type"],
                        "category": r["category"],
                        "payment_method": r["payment_method"],
                        "device_info": str(r["device_info"] or "").strip(),
                        "created_at_dt": dt,
                        "created_at_str": str(r["created_at"]),
                        "review_status": r["review_status"]
                    })

            if close_conn_on_finish:
                db_conn.close()

        # -------------------------------------------------------------
        # 1. Transaction Velocity Features (1m, 5m, 10m, 1h)
        # -------------------------------------------------------------
        count_1m = 0
        count_5m = 0
        count_10m = 0
        count_1h = 0
        seconds_since_last: Optional[float] = None

        if history:
            # Time since the immediate previous transaction
            diff_last = (now - history[0]["created_at_dt"]).total_seconds()
            seconds_since_last = max(0.0, diff_last)

            for h in history:
                sec_diff = (now - h["created_at_dt"]).total_seconds()
                # Consider only transactions in the past (sec_diff >= 0)
                if sec_diff >= 0:
                    if sec_diff <= 60:
                        count_1m += 1
                    if sec_diff <= 300:
                        count_5m += 1
                    if sec_diff <= 600:
                        count_10m += 1
                    if sec_diff <= 3600:
                        count_1h += 1

        # -------------------------------------------------------------
        # 2. Historical Amount Baselines & Spending Deviations
        # -------------------------------------------------------------
        amounts_history = [h["amount"] for h in history]
        is_new_user = len(amounts_history) == 0

        if len(amounts_history) >= 3:
            avg_amount = float(np.mean(amounts_history))
            std_amount = float(np.std(amounts_history))
            std_safe = std_amount if std_amount > 1.0 else 1.0
            z_score = float((amount - avg_amount) / std_safe)
            max_recent_amount = float(np.max(amounts_history[:30]))
            amount_ratio = float(amount / avg_amount) if avg_amount > 0 else 1.0
        elif len(amounts_history) > 0:
            avg_amount = float(np.mean(amounts_history))
            std_amount = 0.0
            z_score = float((amount - avg_amount) / (avg_amount * 0.5 or 1000.0))
            max_recent_amount = float(np.max(amounts_history))
            amount_ratio = float(amount / avg_amount) if avg_amount > 0 else 1.0
        else:
            # Cold-start for new user: safe defaults without fabricating past transactions
            avg_amount = 0.0
            std_amount = 0.0
            z_score = 0.0 if amount < 10000.0 else float((amount - 5000.0) / 5000.0)
            max_recent_amount = 0.0
            amount_ratio = 1.0

        # -------------------------------------------------------------
        # 3. Recipient Familiarity & Frequency
        # -------------------------------------------------------------
        recipient_counts: Dict[str, int] = {}
        for h in history:
            rec = h["receiver_info"]
            if rec:
                recipient_counts[rec] = recipient_counts.get(rec, 0) + 1

        is_new_recipient = (receiver not in recipient_counts) if receiver else False
        is_frequent_recipient = (recipient_counts.get(receiver, 0) >= 3) if receiver else False
        recipient_prior_tx_count = recipient_counts.get(receiver, 0) if receiver else 0

        # -------------------------------------------------------------
        # 4. Unusual Transaction Timing
        # -------------------------------------------------------------
        # Standard odd hours: 1 AM to 5 AM (01:00 - 05:59)
        is_odd_hour = (1 <= hour <= 5)
        is_unusual_hour = is_odd_hour

        # Personal profile check: if user has history, check typical transaction hours
        if len(history) >= 5:
            hist_hours = [h["created_at_dt"].hour for h in history]
            hour_counts = {hr: hist_hours.count(hr) for hr in range(24)}
            if hour_counts.get(hour, 0) > 0:
                is_unusual_hour = False
            elif is_odd_hour:
                is_unusual_hour = True
            else:
                is_unusual_hour = False

        # -------------------------------------------------------------
        # 5. Rapid Repeated Transaction Detection
        # -------------------------------------------------------------
        rapid_repeat_detected = False
        rapid_repeat_reasons = []

        if history:
            # Check if any transaction to identical recipient within 5 mins (300s)
            recent_same_recipient = [
                h for h in history[:10]
                if h["receiver_info"] == receiver and 0 <= (now - h["created_at_dt"]).total_seconds() <= 300
            ]
            if len(recent_same_recipient) >= 1:
                rapid_repeat_detected = True
                rapid_repeat_reasons.append(f"{len(recent_same_recipient)} previous transaction(s) to same recipient within 5 minutes.")

            # Check if identical amount to same recipient within 10 mins (600s)
            recent_identical = [
                h for h in history[:10]
                if h["receiver_info"] == receiver and abs(h["amount"] - amount) < 0.01 and 0 <= (now - h["created_at_dt"]).total_seconds() <= 600
            ]
            if len(recent_identical) >= 1:
                rapid_repeat_detected = True
                rapid_repeat_reasons.append(f"Identical transfer amount of ₹{amount:,.2f} sent to '{receiver}' within 10 minutes.")

            # Velocity burst trigger
            if count_1m >= 2:
                rapid_repeat_detected = True
                rapid_repeat_reasons.append(f"Rapid burst velocity: {count_1m} transactions recorded in the last 60 seconds.")
            elif count_5m >= 4:
                rapid_repeat_detected = True
                rapid_repeat_reasons.append(f"High velocity frequency: {count_5m} transactions recorded in the last 5 minutes.")

        # -------------------------------------------------------------
        # 6. Unusual Device / Session Detection
        # -------------------------------------------------------------
        known_devices = {h["device_info"] for h in history if h.get("device_info")}
        unusual_device = False

        if device and known_devices:
            # If user has established device history and current device is not recognized
            if device not in known_devices:
                unusual_device = True

        # Compile full feature dict
        features = {
            "tx_count_1m": int(count_1m),
            "tx_count_5m": int(count_5m),
            "tx_count_10m": int(count_10m),
            "tx_count_1h": int(count_1h),
            "avg_amount": round(float(avg_amount), 2),
            "std_amount": round(float(std_amount), 2),
            "max_recent_amount": round(float(max_recent_amount), 2),
            "z_score": round(float(z_score), 2),
            "amount_ratio": round(float(amount_ratio), 2),
            "seconds_since_last_txn": round(float(seconds_since_last), 1) if seconds_since_last is not None else 999999.0,
            "is_new_recipient": bool(is_new_recipient),
            "is_frequent_recipient": bool(is_frequent_recipient),
            "recipient_prior_tx_count": int(recipient_prior_tx_count),
            "hour": int(hour),
            "is_odd_hour": bool(is_odd_hour),
            "is_unusual_hour": bool(is_unusual_hour),
            "rapid_repeat_detected": bool(rapid_repeat_detected),
            "rapid_repeat_reasons": rapid_repeat_reasons,
            "unusual_device": bool(unusual_device),
            "device_info": device,
            "is_new_user": bool(is_new_user),
            "history_count": len(history),
            "evaluated_at": now.strftime("%Y-%m-%d %H:%M:%S")
        }

        return features
