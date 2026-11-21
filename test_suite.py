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
from engines.link_scanner import LinkScannerEngine
from engines.otp_detector import OTPScamDetectorEngine
from engines.message_scanner import MessageScannerEngine
from engines.qr_scanner import QRScannerEngine
from engines.anomaly_detector import AnomalyDetectionEngine
from engines.explainability import ExplainabilityEngine
from engines.ml_fraud_engine import MLFraudEngine
from engines.forecasting_engine import SpendingForecastingEngine
from engines.financial_chatbot import FinancialChatbotEngine
from app import app
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


if __name__ == "__main__":
    unittest.main()
