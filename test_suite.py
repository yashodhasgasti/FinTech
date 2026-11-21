"""
NEXAPAY Comprehensive Automated Test Suite
Executes complete verification across:
1. Security Scanners (Link, OTP, SMS, QR)
2. Explainable AI & Anomaly Detection
3. Pure-NumPy Machine Learning Fraud Engine & Model Evaluation Metrics
4. Multi-Role Authentication, RBAC, and Profile Management
5. Transaction CRUD & Pre-Flight Payment Simulator
6. Human Compliance Review Queue & Audit Trail
7. Smart Budget Planner & Savings Goals
8. Spending Forecasting Engine & Trend Analysis
9. AI Financial Assistant Contextual Q&A
10. Notification Management & Report Generation (CSV & Statement)
"""

import unittest
import json
import os
from werkzeug.security import check_password_hash
from engines.link_scanner import LinkScannerEngine
from engines.otp_detector import OTPScamDetectorEngine
from engines.message_scanner import MessageScannerEngine
from engines.qr_scanner import QRScannerEngine
from engines.anomaly_detector import AnomalyDetectionEngine
from engines.explainability import ExplainabilityEngine
from engines.ml_fraud_engine import MLFraudEngine
from engines.feature_extractor import RealTimeFeatureExtractor
from engines.forecasting_engine import SpendingForecastingEngine
from engines.financial_chatbot import FinancialChatbotEngine
from app import app, USER_RATE_TIMESTAMPS, RATE_LIMIT_LOCK, check_user_rate_limit
import database


class NexaPayComprehensiveTestSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        database.init_db()
        app.config["TESTING"] = True
        cls.client = app.test_client()

    # -------------------------------------------------------------
    # 1. AI LINK SCANNER TESTS (PRESERVED)
    # -------------------------------------------------------------
    def test_01_link_scanner_phishing(self):
        res = LinkScannerEngine.scan_url("http://sbi-kyc-verification-login.xyz")
        self.assertGreaterEqual(res["risk_score"], 60.0)
        self.assertIn(res["risk_level"], ["HIGH_RISK", "CRITICAL"])
        print("✓ Test 01 Passed: Link Scanner flagged phishing URL with score:", res["risk_score"])

    def test_02_link_scanner_legit(self):
        res = LinkScannerEngine.scan_url("https://onlinesbi.sbi")
        self.assertLessEqual(res["risk_score"], 25.0)
        self.assertEqual(res["risk_level"], "SAFE")
        print("✓ Test 02 Passed: Link Scanner verified genuine domain.")

    def test_03_link_scanner_raw_ip(self):
        res = LinkScannerEngine.scan_url("http://192.168.1.100/login")
        self.assertGreaterEqual(res["risk_score"], 40.0)
        print("✓ Test 03 Passed: Link Scanner flagged raw IP server.")

    # -------------------------------------------------------------
    # 2. OTP SCAM DETECTOR TESTS (PRESERVED)
    # -------------------------------------------------------------
    def test_04_otp_detector_urgency(self):
        text = "Urgent: Your electricity power will be disconnected today. Share your OTP 492019 to verify payment."
        res = OTPScamDetectorEngine.scan_message(text)
        self.assertGreaterEqual(res["risk_score"], 70.0)
        self.assertEqual(res["risk_level"], "CRITICAL")
        print("✓ Test 04 Passed: OTP Detector flagged urgent OTP extortion.")

    def test_05_otp_detector_reverse_upi(self):
        text = "To receive Rs 5000 cashback into your bank account, please enter your UPI PIN right now."
        res = OTPScamDetectorEngine.scan_message(text)
        self.assertGreaterEqual(res["risk_score"], 50.0)
        print("✓ Test 05 Passed: OTP Detector flagged reverse UPI PIN scam.")

    def test_06_otp_detector_normal(self):
        text = "Your appointment with Dr. Sharma is confirmed for tomorrow at 4 PM."
        res = OTPScamDetectorEngine.scan_message(text)
        self.assertLessEqual(res["risk_score"], 25.0)
        print("✓ Test 06 Passed: OTP Detector passed normal message.")

    # -------------------------------------------------------------
    # 3. SMS & WHATSAPP MESSAGE SCANNER TESTS (PRESERVED)
    # -------------------------------------------------------------
    def test_07_msg_scanner_job_scam(self):
        msg = "Part time work from home earn 5000 daily by liking YouTube videos. Join Telegram t.me/fast_income"
        res = MessageScannerEngine.scan_message(msg)
        self.assertGreaterEqual(res["risk_score"], 60.0)
        print("✓ Test 07 Passed: Message Scanner flagged job scam.")

    def test_08_msg_scanner_lottery(self):
        msg = "Congratulations! Your mobile number has won Rs 25,00,000 in KBC Lucky Draw 2026."
        res = MessageScannerEngine.scan_message(msg)
        self.assertGreaterEqual(res["risk_score"], 35.0)
        print("✓ Test 08 Passed: Message Scanner flagged lottery scam.")

    # -------------------------------------------------------------
    # 4. QR CODE SAFETY SCANNER TESTS (PRESERVED)
    # -------------------------------------------------------------
    def test_09_qr_scanner_spoofed_vpa(self):
        payload = "upi://pay?pa=scammer99@oksbi&pn=ElectricityOffice&am=5000&cu=INR"
        res = QRScannerEngine.inspect_payload(payload)
        self.assertGreaterEqual(res["risk_score"], 70.0)
        print("✓ Test 09 Passed: QR Scanner detected payee impersonation.")

    def test_10_qr_scanner_genuine_merchant(self):
        payload = "upi://pay?pa=retail.store@hdfcbank&pn=Retail_Store&cu=INR"
        res = QRScannerEngine.inspect_payload(payload)
        self.assertLessEqual(res["risk_score"], 25.0)
        print("✓ Test 10 Passed: QR Scanner verified merchant QR.")

    # -------------------------------------------------------------
    # 5. AI ANOMALY & ML FRAUD ENGINE TESTS
    # -------------------------------------------------------------
    def test_11_ml_fraud_engine_critical_outlier(self):
        tx = {"amount": 95000.0, "category": "Suspicious Transfer", "receiver_info": "crypto_cashout@ybl", "hour": 2}
        history = [{"amount": 1200.0, "receiver_info": "local_shop@upi"} for _ in range(5)]
        eval_res = MLFraudEngine.evaluate_transaction(tx, history)
        self.assertGreaterEqual(eval_res["risk_score"], 70.0)
        self.assertEqual(eval_res["risk_level"], "CRITICAL")
        self.assertTrue(eval_res["requires_human_review"])
        self.assertTrue(len(eval_res["attributions"]) >= 3)
        print("✓ Test 11 Passed: ML Fraud Engine flagged critical outlier with score:", eval_res["risk_score"])

    def test_12_ml_fraud_engine_normal_transaction(self):
        tx = {"amount": 450.0, "category": "Groceries", "receiver_info": "daily_mart@upi", "hour": 14}
        history = [{"amount": 500.0, "receiver_info": "daily_mart@upi"} for _ in range(5)]
        eval_res = MLFraudEngine.evaluate_transaction(tx, history)
        self.assertLessEqual(eval_res["risk_score"], 30.0)
        self.assertEqual(eval_res["risk_level"], "SAFE")
        self.assertFalse(eval_res["requires_human_review"])
        print("✓ Test 12 Passed: ML Fraud Engine approved safe routine transaction.")

    def test_13_ml_model_evaluation_metrics(self):
        metrics = MLFraudEngine.get_model_evaluation_metrics()
        self.assertGreaterEqual(metrics["accuracy"], 95.0)
        self.assertGreaterEqual(metrics["precision"], 94.0)
        self.assertGreaterEqual(metrics["recall"], 94.0)
        self.assertGreaterEqual(metrics["f1_score"], 94.0)
        self.assertIn("true_positives", metrics["confusion_matrix"])
        print("✓ Test 13 Passed: ML Evaluation Metrics validated (Accuracy:", metrics["accuracy"], "%)")

    # -------------------------------------------------------------
    # 6. AUTHENTICATION & ROLE MANAGEMENT APIS
    # -------------------------------------------------------------
    def test_14_auth_register_and_login(self):
        email = "testuser_suite@nexapay.local"
        reg_payload = {
            "full_name": "Test Suite Candidate",
            "email": email,
            "password": "password123",
            "role": "shop_owner",
            "business_name": "Candidate Mart"
        }
        res = self.client.post("/api/auth/register", json=reg_payload)
        self.assertIn(res.status_code, [200, 400]) # 200 or already registered

        # Login
        login_res = self.client.post("/api/auth/login", json={"email": email, "password": "password123"})
        self.assertEqual(login_res.status_code, 200)
        data = login_res.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["user"]["role"], "shop_owner")
        print("✓ Test 14 Passed: User registration & role authentication successful.")

    def test_15_auth_switch_demo_user(self):
        res = self.client.post("/api/auth/switch-demo-user", json={"role": "admin_reviewer"})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["user"]["role"], "admin_reviewer")
        print("✓ Test 15 Passed: Demo user role switch to admin_reviewer successful.")

    # -------------------------------------------------------------
    # 7. TRANSACTION MANAGEMENT & PAYMENT SIMULATOR
    # -------------------------------------------------------------
    def test_16_transaction_creation_and_listing(self):
        txn_payload = {
            "txn_type": "EXPENSE",
            "category": "Food & Dining",
            "amount": 820.0,
            "receiver_info": "Restaurant Plaza",
            "payment_method": "UPI",
            "description": "Team lunch"
        }
        res = self.client.post("/api/transactions", json=txn_payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["transaction"]["category"], "Food & Dining")

        # List transactions
        list_res = self.client.get("/api/transactions")
        self.assertEqual(list_res.status_code, 200)
        self.assertGreaterEqual(len(list_res.get_json()["transactions"]), 1)
        print("✓ Test 16 Passed: Transaction created and verified in transaction list.")

    def test_17_payment_simulator_high_risk_quarantine(self):
        sim_payload = {
            "amount": 99000.0,
            "receiver_upi": "unknown_crypto_agent@ybl",
            "category": "Suspicious Transfer",
            "description": "Urgent lottery fee transfer"
        }
        res = self.client.post("/api/simulator/pay", json=sim_payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "HELD_FOR_REVIEW")
        self.assertEqual(data["review_status"], "Pending Review")
        self.assertGreaterEqual(data["risk_score"], 60.0)
        self.assertIn(data["risk_level"], ["HIGH_RISK", "CRITICAL"])
        print("✓ Test 17 Passed: Simulator flagged high-risk transfer and routed to Human Review Queue.")

    # -------------------------------------------------------------
    # 8. HUMAN REVIEW QUEUE & AUDIT LOGS
    # -------------------------------------------------------------
    def test_18_review_queue_and_decision(self):
        # Fetch queue
        queue_res = self.client.get("/api/review/queue")
        self.assertEqual(queue_res.status_code, 200)
        queue = queue_res.get_json()["queue"]
        self.assertGreaterEqual(len(queue), 1)
        txn_id = queue[0]["id"]

        # Submit compliance decision
        dec_payload = {
            "transaction_id": txn_id,
            "decision": "Under Investigation",
            "notes": "Verified by Automated Compliance Bot. Escalated for KYC check."
        }
        dec_res = self.client.post("/api/review/decision", json=dec_payload)
        self.assertEqual(dec_res.status_code, 200)
        self.assertTrue(dec_res.get_json()["success"])

        # Check Audit Log
        audit_res = self.client.get("/api/review/audit-logs")
        self.assertEqual(audit_res.status_code, 200)
        logs = audit_res.get_json()["logs"]
        self.assertGreaterEqual(len(logs), 1)
        print("✓ Test 18 Passed: Compliance review decision and audit trail verified.")

    # -------------------------------------------------------------
    # 9. SMART BUDGET PLANNER & SAVINGS GOALS
    # -------------------------------------------------------------
    def test_19_budget_management(self):
        b_payload = {
            "category": "Entertainment",
            "monthly_limit": 5000.0,
            "alert_threshold": 80.0
        }
        res = self.client.post("/api/budgets", json=b_payload)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.get_json()["success"])

        budgets_res = self.client.get("/api/budgets")
        self.assertEqual(budgets_res.status_code, 200)
        b_list = budgets_res.get_json()["budgets"]
        self.assertTrue(any(b["category"] == "Entertainment" for b in b_list))
        print("✓ Test 19 Passed: Category budget successfully created & tracked.")

    def test_20_savings_goals(self):
        goal_payload = {
            "goal_name": "Emergency Health Fund",
            "target_amount": 50000.0,
            "current_amount": 15000.0,
            "target_date": "2026-12-31",
            "category": "Health Reserve"
        }
        res = self.client.post("/api/savings-goals", json=goal_payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        goal_id = data["goal_id"]

        # Deposit to goal
        dep_res = self.client.post(f"/api/savings-goals/{goal_id}/deposit", json={"amount": 5000.0})
        self.assertEqual(dep_res.status_code, 200)
        print("✓ Test 20 Passed: Savings goal created and deposit processed.")

    # -------------------------------------------------------------
    # 10. SPENDING FORECASTING & ANALYTICS
    # -------------------------------------------------------------
    def test_21_spending_forecasting(self):
        res = self.client.get("/api/forecast/predict")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("predicted_weekly_expense", data)
        self.assertIn("predicted_monthly_expense", data)
        self.assertIn("trend", data)
        self.assertIn("actual_vs_predicted", data)
        self.assertIn("limitations_disclaimer", data)
        print("✓ Test 21 Passed: Spending forecast generated with weekly/monthly estimates and limitations.")

    # -------------------------------------------------------------
    # 11. AI FINANCIAL ASSISTANT (CHATBOT)
    # -------------------------------------------------------------
    def test_22_ai_financial_chatbot(self):
        res = self.client.post("/api/chatbot/query", json={"query": "How much did I spend this month?"})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("answer", data)
        self.assertEqual(data["topic"], "EXPENSES")

        sec_res = self.client.post("/api/chatbot/query", json={"query": "What is the golden rule of UPI PIN?"})
        self.assertEqual(sec_res.status_code, 200)
        sec_data = sec_res.get_json()
        self.assertIn("1930", sec_data["answer"])
        print("✓ Test 22 Passed: AI Financial Chatbot returned context-grounded financial advice.")

    # -------------------------------------------------------------
    # 12. NOTIFICATIONS & REPORTS
    # -------------------------------------------------------------
    def test_23_notifications_and_read_status(self):
        res = self.client.get("/api/notifications")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("notifications", data)

        # Mark all read
        read_res = self.client.post("/api/notifications/read-all")
        self.assertEqual(read_res.status_code, 200)
        print("✓ Test 23 Passed: Notification center fetched and read status toggled.")

    def test_24_reports_csv_and_statement(self):
        csv_res = self.client.get("/api/reports/export-csv")
        self.assertEqual(csv_res.status_code, 200)
        self.assertEqual(csv_res.headers["Content-Type"], "text/csv; charset=utf-8")

        stmt_res = self.client.get("/api/reports/statement")
        self.assertEqual(stmt_res.status_code, 200)
        self.assertIn(b"NEXAPAY", stmt_res.data)
        print("✓ Test 24 Passed: CSV export and printable statement generation succeeded.")

    def test_25_admin_operations_stats(self):
        stats_res = self.client.get("/api/admin/system-stats")
        self.assertEqual(stats_res.status_code, 200)
        stats = stats_res.get_json()
        self.assertGreaterEqual(stats["total_users"], 4)
        self.assertGreaterEqual(stats["total_transactions"], 1)

        users_res = self.client.get("/api/admin/users")
        self.assertEqual(users_res.status_code, 200)
        print("✓ Test 25 Passed: Admin system metrics and registered users list retrieved.")

    # -------------------------------------------------------------
    # 13. REAL-TIME FEATURE EXTRACTION & COLD-START VALIDATION
    # -------------------------------------------------------------
    def test_26_realtime_feature_extractor(self):
        tx = {
            "amount": 1500.0,
            "receiver_info": "reliance_fresh@okaxis",
            "category": "Groceries",
            "device_info": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "hour": 15
        }
        features = RealTimeFeatureExtractor.extract_features(user_id=1, transaction=tx)
        required_features = [
            "tx_count_1m", "tx_count_5m", "tx_count_10m", "tx_count_1h",
            "avg_amount", "std_amount", "max_recent_amount", "z_score",
            "amount_ratio", "seconds_since_last_txn", "is_new_recipient",
            "is_frequent_recipient", "is_unusual_hour", "rapid_repeat_detected",
            "unusual_device"
        ]
        for f in required_features:
            self.assertIn(f, features, f"Missing feature {f}")
        self.assertIsInstance(features["avg_amount"], (int, float))
        self.assertIsInstance(features["is_new_recipient"], bool)
        print("✓ Test 26 Passed: Real-time feature extractor calculated all 15 operational features from database history.")

    def test_27_cold_start_new_user(self):
        # User ID 99999 has no prior transactions
        new_uid = 99999
        tx = {"amount": 250.0, "receiver_info": "tea_stall@upi", "category": "Food", "hour": 14}
        features = RealTimeFeatureExtractor.extract_features(user_id=new_uid, transaction=tx)
        self.assertEqual(features["tx_count_1m"], 0)
        self.assertEqual(features["tx_count_1h"], 0)
        self.assertTrue(features["is_new_recipient"])
        self.assertIn(features["seconds_since_last_txn"], [999999, 999999.0])
        self.assertEqual(features["avg_amount"], 0.0)
        
        # Test ML evaluation handles cold start gracefully
        eval_res = MLFraudEngine.evaluate_transaction(tx, user_id=new_uid)
        self.assertIn("risk_score", eval_res)
        self.assertIn("attributions", eval_res)
        print("✓ Test 27 Passed: Cold-start new user safely handled with genuine feature fallbacks.")

    # -------------------------------------------------------------
    # 14. THREE-TIER RISK ACTIONS (LOW, MEDIUM, HIGH)
    # -------------------------------------------------------------
    def test_28_three_tier_low_risk_execution(self):
        with RATE_LIMIT_LOCK:
            USER_RATE_TIMESTAMPS.clear()
        payload = {
            "amount": 220.0,
            "receiver_upi": "groceries_mart@hdfcbank",
            "category": "Groceries",
            "description": "Daily essentials purchase",
            "hour": 14
        }
        res = self.client.post("/api/simulator/pay", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "SUCCESSFUL")
        self.assertFalse(data["verification_required"])
        self.assertLess(data["risk_score"], 30.0)
        self.assertIn(data["decision"], ["ALLOW", "APPROVED"])
        print("✓ Test 28 Passed: Low-risk transaction (<30) instantly approved and settled.")

    def test_29_three_tier_medium_risk_step_up_challenge(self):
        with RATE_LIMIT_LOCK:
            USER_RATE_TIMESTAMPS.clear()
        # Medium risk scenario: ₹28,000 for item from a new payee
        payload = {
            "amount": 28000.0,
            "receiver_upi": "luxury_boutique_suite@icici",
            "category": "Electronics",
            "description": "Gadget purchase",
            "hour": 14
        }
        res = self.client.post("/api/simulator/pay", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "REQUIRE_VERIFICATION")
        self.assertTrue(data["verification_required"])
        self.assertGreaterEqual(data["risk_score"], 30.0)
        self.assertLess(data["risk_score"], 70.0)
        self.assertEqual(data["risk_level"], "MEDIUM")
        challenge = data.get("verification_challenge")
        self.assertIsNotNone(challenge)
        txn_id = challenge["transaction_id"]
        hint_code = challenge.get("code_hint", "123456")

        # Confirm step-up challenge code
        verify_res = self.client.post("/api/simulator/verify-challenge", json={
            "transaction_id": txn_id,
            "verification_code": hint_code
        })
        self.assertEqual(verify_res.status_code, 200)
        v_data = verify_res.get_json()
        self.assertTrue(v_data["success"])
        print("✓ Test 29 Passed: Medium-risk transaction (30-69) prompted step-up 2FA and cleared upon verification.")

    def test_30_three_tier_high_risk_held_for_review(self):
        with RATE_LIMIT_LOCK:
            USER_RATE_TIMESTAMPS.clear()
        payload = {
            "amount": 99999.0,
            "receiver_upi": "anonymous_crypto_wallet@binance",
            "category": "Suspicious Transfer",
            "description": "Urgent offshore crypto fund transfer"
        }
        res = self.client.post("/api/simulator/pay", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "HELD_FOR_REVIEW")
        self.assertGreaterEqual(data["risk_score"], 70.0)
        self.assertIn(data["risk_level"], ["HIGH_RISK", "CRITICAL"])
        self.assertIn(data["decision"], ["HOLD", "HELD_FOR_REVIEW", "BLOCKED"])
        self.assertGreaterEqual(len(data.get("risk_reasons", [])), 1)
        print("✓ Test 30 Passed: High-risk transaction (>=70) held for review without releasing funds.")

    # -------------------------------------------------------------
    # 15. DUPLICATE TRANSACTION & RATE LIMIT PREVENTION
    # -------------------------------------------------------------
    def test_31_duplicate_transaction_prevention(self):
        with RATE_LIMIT_LOCK:
            USER_RATE_TIMESTAMPS.clear()
        unique_amt = 4321.75
        payload = {
            "amount": unique_amt,
            "receiver_upi": "unique_merchant_suite@okhdfc",
            "category": "Shopping",
            "description": "First attempt"
        }
        res1 = self.client.post("/api/simulator/pay", json=payload)
        self.assertEqual(res1.status_code, 200)
        
        # Immediate duplicate submission within 10-second window
        res2 = self.client.post("/api/simulator/pay", json=payload)
        self.assertEqual(res2.status_code, 409)
        d2 = res2.get_json()
        self.assertFalse(d2["success"])
        self.assertIn("Duplicate transaction detected", d2["error"])
        print("✓ Test 31 Passed: Duplicate transaction prevention blocked identical second submission (HTTP 409).")

    def test_32_rate_limiter_enforcement(self):
        test_uid = 77777
        with RATE_LIMIT_LOCK:
            USER_RATE_TIMESTAMPS[test_uid] = []
        
        # Fire 15 valid requests
        for i in range(15):
            allowed = check_user_rate_limit(test_uid, max_per_minute=15)
            self.assertTrue(allowed, f"Request {i+1} should be allowed")
        
        # 16th request must be rejected
        blocked = check_user_rate_limit(test_uid, max_per_minute=15)
        self.assertFalse(blocked, "16th request must be rate-limited")
        
        # Clean up
        with RATE_LIMIT_LOCK:
            USER_RATE_TIMESTAMPS.pop(test_uid, None)
        print("✓ Test 32 Passed: Sliding-window rate limiter blocked user after 15 tx/min.")

    # -------------------------------------------------------------
    # 16. CONFIGURABLE THRESHOLDS, LIVE TELEMETRY & SSE STREAM
    # -------------------------------------------------------------
    def test_33_configurable_thresholds_api(self):
        # Read current thresholds
        get_res = self.client.get("/api/fraud/thresholds")
        self.assertEqual(get_res.status_code, 200)
        t_data = get_res.get_json()["thresholds"]
        self.assertIn("low_max", t_data)
        self.assertIn("high_min", t_data)

        # Switch to admin reviewer
        self.client.post("/api/auth/switch-demo-user", json={"role": "admin_reviewer"})

        # Update thresholds
        post_res = self.client.post("/api/fraud/thresholds", json={
            "low_max": 25.0,
            "high_min": 75.0,
            "auto_block_high_risk": True
        })
        self.assertEqual(post_res.status_code, 200)
        self.assertTrue(post_res.get_json()["success"])
        
        # Verify persistence
        verify_res = self.client.get("/api/fraud/thresholds")
        v_data = verify_res.get_json()["thresholds"]
        self.assertEqual(v_data["low_max"], 25.0)
        self.assertEqual(v_data["high_min"], 75.0)
        self.assertTrue(v_data["auto_block_high_risk"])

        # Restore default thresholds
        self.client.post("/api/fraud/thresholds", json={
            "low_max": 30.0,
            "high_min": 70.0,
            "auto_block_high_risk": False
        })
        print("✓ Test 33 Passed: Configurable risk thresholds read, updated, and persisted.")

    def test_34_sse_live_alert_stream_handshake(self):
        res = self.client.get("/api/stream/alerts", buffered=False)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.headers["Content-Type"].startswith("text/event-stream"))
        first_frame = next(res.response)
        self.assertIn(b"CONNECTED", first_frame)
        res.close()
        print("✓ Test 34 Passed: Server-Sent Events (SSE) live stream handshake verified.")

    def test_35_human_reviewer_investigation_and_feedback(self):
        # 1. Fetch queue to obtain a quarantined transaction
        queue_res = self.client.get("/api/review/queue")
        self.assertEqual(queue_res.status_code, 200)
        queue = queue_res.get_json()["queue"]
        self.assertGreaterEqual(len(queue), 1)
        txn_id = queue[0]["id"]

        # 2. Inspect transaction details with real-time features
        detail_res = self.client.get(f"/api/transactions/{txn_id}")
        self.assertEqual(detail_res.status_code, 200)
        detail = detail_res.get_json()["transaction"]
        self.assertIn("features_json", detail)
        self.assertIn("rule_risk_score", detail)
        self.assertIn("ml_anomaly_score", detail)
        self.assertIn("ml_fraud_prob", detail)

        # 3. Submit reviewer decision with notes
        rev_payload = {
            "transaction_id": txn_id,
            "decision": "Confirmed Suspicious",
            "notes": "Verified fraudulent anomaly signature. Confirmed by Compliance Officer."
        }
        dec_res = self.client.post("/api/review/decision", json=rev_payload)
        self.assertEqual(dec_res.status_code, 200)
        self.assertTrue(dec_res.get_json()["success"])

        # 4. Verify fraud_feedback audit entry for model improvement
        conn = database.get_db_connection()
        row = conn.execute("SELECT * FROM fraud_feedback WHERE transaction_id = ? ORDER BY id DESC LIMIT 1", (txn_id,)).fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row["ground_truth_label"], 1)
        self.assertIn(row["reviewer_decision"], ["Confirmed Suspicious", "Suspicious"])
        conn.close()
        print("✓ Test 35 Passed: Human reviewer investigation, audit log, and feedback loop verified.")

    def test_36_fraud_live_stats_telemetry(self):
        res = self.client.get("/api/fraud/live-stats")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("total_evaluated", data)
        self.assertIn("low_risk_count", data)
        self.assertIn("medium_risk_count", data)
        self.assertIn("high_risk_count", data)
        self.assertIn("thresholds", data)
        print("✓ Test 36 Passed: Real-time fraud telemetry and distribution metrics verified.")

    # -------------------------------------------------------------
    # 17. AUTHENTICATION & LOGIN WORKFLOW TESTS
    # -------------------------------------------------------------
    def test_37_unauthenticated_dashboard_redirect(self):
        anon_client = app.test_client()
        res = anon_client.get("/")
        self.assertEqual(res.status_code, 302)
        self.assertIn("/login", res.headers.get("Location", ""))
        print("✓ Test 37 Passed: Unauthenticated dashboard request safely redirects to /login.")

    def test_38_unauthenticated_protected_apis_401(self):
        anon_client = app.test_client()
        res_tx = anon_client.get("/api/transactions")
        self.assertEqual(res_tx.status_code, 401)
        res_bg = anon_client.get("/api/budgets")
        self.assertEqual(res_bg.status_code, 401)
        res_sg = anon_client.get("/api/savings-goals")
        self.assertEqual(res_sg.status_code, 401)
        print("✓ Test 38 Passed: Unauthenticated API access correctly rejected with HTTP 401.")

    def test_39_login_page_renders(self):
        anon_client = app.test_client()
        res = anon_client.get("/login")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Welcome Back to NexaPay", res.data)
        self.assertIn(b"Secure access to your smarter financial experience", res.data)
        print("✓ Test 39 Passed: Professional login page renders with branding and security badges.")

    def test_40_valid_login_form_post(self):
        auth_client = app.test_client()
        login_res = auth_client.post("/login", data={
            "identifier": "individual@nexapay.local",
            "password": "demo123",
            "remember_me": "1"
        }, follow_redirects=False)
        self.assertEqual(login_res.status_code, 302)
        self.assertEqual(login_res.headers.get("Location"), "/")
        
        # Follow redirect to dashboard
        dash_res = auth_client.get("/")
        self.assertEqual(dash_res.status_code, 200)
        self.assertIn(b"Aditya Verma", dash_res.data)
        print("✓ Test 40 Passed: Valid credential login sets session and redirects to dashboard.")

    def test_41_invalid_email_or_username(self):
        res = self.client.post("/login", data={
            "identifier": "nonexistent_ghost_999@nexapay.local",
            "password": "some_random_password"
        })
        self.assertEqual(res.status_code, 401)
        self.assertIn(b"Invalid email or password", res.data)
        print("✓ Test 41 Passed: Unknown email/username login returns 401 with generic safe error.")

    def test_42_incorrect_password(self):
        res = self.client.post("/login", data={
            "identifier": "individual@nexapay.local",
            "password": "definitely_wrong_password_456"
        })
        self.assertEqual(res.status_code, 401)
        self.assertIn(b"Invalid email or password", res.data)
        print("✓ Test 42 Passed: Incorrect password attempt rejected with 401.")

    def test_43_empty_form_submission(self):
        res = self.client.post("/login", data={"identifier": "", "password": ""})
        self.assertEqual(res.status_code, 400)
        self.assertIn(b"required", res.data)
        print("✓ Test 43 Passed: Empty login form submission rejected with 400.")

    def test_44_registration_successful_and_duplicate_prevention(self):
        unique_email = f"candidate_{os.getpid()}_{hash(app)}@nexapay.local"
        reg_payload = {
            "full_name": "Ramesh Patel",
            "email": unique_email,
            "phone": "+91 98765 11111",
            "role": "shop_owner",
            "password": "SecurePassword#2026",
            "confirm_password": "SecurePassword#2026"
        }
        reg_res = self.client.post("/register", data=reg_payload, follow_redirects=False)
        self.assertEqual(reg_res.status_code, 302)
        
        # Attempt duplicate registration with exact same email
        dup_res = self.client.post("/register", data=reg_payload)
        self.assertEqual(dup_res.status_code, 400)
        self.assertIn(b"already exists", dup_res.data)
        print("✓ Test 44 Passed: User registration succeeded and duplicate email was blocked.")

    def test_45_registration_admin_role_forbidden(self):
        hacker_email = f"fake_admin_{os.getpid()}@nexapay.local"
        reg_payload = {
            "full_name": "Infiltrator",
            "email": hacker_email,
            "role": "admin_reviewer",
            "password": "Password123",
            "confirm_password": "Password123"
        }
        self.client.post("/register", data=reg_payload)
        
        # Inspect created user in SQLite
        conn = database.get_db_connection()
        row = conn.execute("SELECT role FROM users WHERE email = ?", (hacker_email,)).fetchone()
        self.assertIsNotNone(row)
        self.assertNotEqual(row["role"], "admin_reviewer", "Self-registering as admin must be strictly prevented")
        self.assertEqual(row["role"], "individual")
        conn.close()
        print("✓ Test 45 Passed: Self-registration as administrator prevented; demoted to individual.")

    def test_46_password_hashing_werkzeug_verification(self):
        conn = database.get_db_connection()
        row = conn.execute("SELECT password_hash FROM users WHERE email LIKE 'candidate_%' ORDER BY id DESC LIMIT 1").fetchone()
        self.assertIsNotNone(row)
        stored_hash = row["password_hash"]
        self.assertTrue(
            stored_hash.startswith("pbkdf2:sha256:") or stored_hash.startswith("scrypt:"),
            f"Expected Werkzeug password hash format, got {stored_hash}"
        )
        self.assertTrue(check_password_hash(stored_hash, "SecurePassword#2026"))
        self.assertFalse(check_password_hash(stored_hash, "PlaintextLeaked"))
        conn.close()
        print("✓ Test 46 Passed: Werkzeug PBKDF2 password hashing validated; plaintext never stored.")

    def test_47_forgot_and_reset_password_workflow(self):
        # 1. Request forgot password
        forgot_res = self.client.post("/forgot-password", data={"email": "individual@nexapay.local"})
        self.assertEqual(forgot_res.status_code, 200)
        self.assertIn(b"reset instructions have been generated", forgot_res.data)

        # 2. Generate and verify token directly
        ok, msg, raw_token = database.create_password_reset_token("individual@nexapay.local")
        self.assertTrue(ok)
        self.assertIsNotNone(raw_token)

        # 3. Apply password reset
        new_pwd = "ResetTempPass#2026"
        reset_ok, reset_msg = database.reset_password_with_token(raw_token, new_pwd)
        self.assertTrue(reset_ok)

        # 4. Authenticate with new password
        auth_ok, auth_msg, u = database.authenticate_user("individual@nexapay.local", new_pwd)
        self.assertTrue(auth_ok)
        self.assertEqual(u["full_name"], "Aditya Verma")

        # 5. Restore demo123 password
        database.reset_password_with_token(
            database.create_password_reset_token("individual@nexapay.local")[2], 
            "demo123"
        )
        print("✓ Test 47 Passed: Secure one-time token password reset workflow validated.")

    def test_48_logout_invalidates_session(self):
        test_client = app.test_client()
        # Log in first
        test_client.post("/login", data={"identifier": "individual@nexapay.local", "password": "demo123"})
        # Confirm access to dashboard
        dash_res = test_client.get("/")
        self.assertEqual(dash_res.status_code, 200)

        # Log out
        logout_res = test_client.get("/logout")
        self.assertEqual(logout_res.status_code, 302)
        self.assertEqual(logout_res.headers.get("Location"), "/login")
        self.assertIn("no-store", logout_res.headers.get("Cache-Control", ""))

        # Subsequent attempt to access dashboard must be redirected
        post_logout_res = test_client.get("/")
        self.assertEqual(post_logout_res.status_code, 302)
        self.assertIn("/login", post_logout_res.headers.get("Location", ""))
        print("✓ Test 48 Passed: Logout invalidates session and prevents back-navigation cache exposure.")


if __name__ == "__main__":
    unittest.main()
