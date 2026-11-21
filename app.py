"""
NEXAPAY Main Application & Flask API Server
Tagline: 'Smart and Safer Payments'
Comprehensive AI-Powered FinTech Platform integrating:
1. Multi-role Authentication & RBAC (Individual, Shop Owner, Business, Admin/Reviewer)
2. Real-Time AI/ML Fraud Detection (Isolation Forest + Random Forest + XAI)
3. Transaction Management & Payment Simulator
4. Human Review Compliance Queue & Audit Trail
5. Smart Budget Planner & Savings Goals
6. Spending Forecasting & Financial Analytics
7. AI Financial Assistant (Chatbot)
8. Multi-Vector Security Scanners (Link, OTP, SMS, QR)
9. Notification Center & Downloadable Financial / 1930 Dossier Reports
"""

import os
import json
import io
import csv
from datetime import datetime
from flask import (
    Flask, render_template, request, jsonify, 
    session, redirect, url_for, make_response
)

import database
from engines.link_scanner import LinkScannerEngine
from engines.otp_detector import OTPScamDetectorEngine
from engines.message_scanner import MessageScannerEngine
from engines.qr_scanner import QRScannerEngine
from engines.anomaly_detector import AnomalyDetectionEngine
from engines.ml_fraud_engine import MLFraudEngine
from engines.forecasting_engine import SpendingForecastingEngine
from engines.financial_chatbot import FinancialChatbotEngine

app = Flask(__name__)
app.config["SECRET_KEY"] = "nexapay-hackathon-production-secret-key-2026"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB max upload

# Initialize database on startup
database.init_db()

# Cached baseline synthetic stream for anomaly analytics
SYNTHETIC_TX_CACHE = AnomalyDetectionEngine.generate_synthetic_stream(25)


# =====================================================================
# AUTHENTICATION & SESSION HELPERS
# =====================================================================

def get_current_user():
    """Returns the current authenticated user dict or a default demo user (Individual User 1)."""
    user_id = session.get("user_id", 1)
    user = database.get_user_by_id(user_id)
    if not user:
        # Fallback to demo individual
        user = database.get_user_by_id(1)
        if user:
            session["user_id"] = user["id"]
            session["role"] = user["role"]
    return user


# =====================================================================
# CORE PAGE ROUTES
# =====================================================================

@app.route("/")
def index():
    """Renders the NEXAPAY unified FinTech platform."""
    user = get_current_user()
    metrics = database.get_dashboard_metrics()
    recent_scans = database.get_recent_scans(6)
    return render_template(
        "index.html", 
        current_user=user, 
        metrics=metrics, 
        recent_scans=recent_scans
    )


# =====================================================================
# AUTHENTICATION APIS
# =====================================================================

@app.route("/api/auth/register", methods=["POST"])
def auth_register():
    """Registers a new user account with selected role."""
    data = request.get_json(silent=True) or {}
    name = data.get("full_name", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()
    role = data.get("role", "individual").strip()
    phone = data.get("phone", "").strip()
    business_name = data.get("business_name", "").strip()

    if not name or not email or not password:
        return jsonify({"success": False, "error": "Name, email, and password are required."}), 400

    if len(password) < 6:
        return jsonify({"success": False, "error": "Password must be at least 6 characters long."}), 400

    success, msg, user = database.register_user(name, email, password, role, phone, business_name)
    if success and user:
        session["user_id"] = user["id"]
        session["role"] = user["role"]
        return jsonify({"success": True, "message": msg, "user": user})
    return jsonify({"success": False, "error": msg}), 400


@app.route("/api/auth/login", methods=["POST"])
def auth_login():
    """Authenticates a user and starts session."""
    data = request.get_json(silent=True) or {}
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    if not email or not password:
        return jsonify({"success": False, "error": "Email and password are required."}), 400

    success, msg, user = database.authenticate_user(email, password)
    if success and user:
        session["user_id"] = user["id"]
        session["role"] = user["role"]
        return jsonify({"success": True, "message": msg, "user": user})
    return jsonify({"success": False, "error": msg}), 401


@app.route("/api/auth/logout", methods=["POST"])
def auth_logout():
    """Clears current user session."""
    session.clear()
    return jsonify({"success": True, "message": "Logged out successfully."})


@app.route("/api/auth/me", methods=["GET"])
def auth_me():
    """Returns current active user details and live wallet balance."""
    user = get_current_user()
    if not user:
        return jsonify({"authenticated": False}), 401
    
    analytics = database.get_financial_analytics(user["id"], user["role"])
    return jsonify({
        "authenticated": True,
        "user": user,
        "analytics_summary": {
            "wallet_balance": user["wallet_balance"],
            "total_income": analytics["total_income"],
            "total_expenses": analytics["total_expenses"],
            "net_savings": analytics["net_savings"],
            "flagged_transactions": analytics["flagged_transactions"]
        }
    })


@app.route("/api/auth/switch-demo-user", methods=["POST"])
def auth_switch_demo():
    """Quickly switches active user between the 4 demo roles for live evaluation."""
    data = request.get_json(silent=True) or {}
    target_role = data.get("role", "individual")

    role_email_map = {
        "individual": "individual@nexapay.local",
        "shop_owner": "shop@nexapay.local",
        "business": "business@nexapay.local",
        "admin_reviewer": "admin@nexapay.local"
    }

    email = role_email_map.get(target_role, "individual@nexapay.local")
    users = database.get_all_users_list()
    target_user = next((u for u in users if u["email"] == email), None)

    if target_user:
        session["user_id"] = target_user["id"]
        session["role"] = target_user["role"]
        return jsonify({"success": True, "user": target_user, "message": f"Switched to {target_role} profile."})
    return jsonify({"success": False, "error": "Role user not found."}), 404


@app.route("/api/auth/update-profile", methods=["POST"])
def auth_update_profile():
    """Updates user profile settings."""
    user = get_current_user()
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    full_name = data.get("full_name", user["full_name"])
    phone = data.get("phone", user["phone"])
    business_name = data.get("business_name", user["business_name"])
    language_pref = data.get("language_pref", user["language_pref"])

    database.update_user_profile(user["id"], full_name, phone, business_name, language_pref)
    updated_user = database.get_user_by_id(user["id"])
    return jsonify({"success": True, "user": updated_user, "message": "Profile updated successfully."})


@app.route("/api/auth/change-password", methods=["POST"])
def auth_change_password():
    """Changes user password."""
    user = get_current_user()
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    curr_pwd = data.get("current_password", "")
    new_pwd = data.get("new_password", "")

    if len(new_pwd) < 6:
        return jsonify({"success": False, "error": "New password must be at least 6 characters."}), 400

    success, msg = database.change_user_password(user["id"], curr_pwd, new_pwd)
    return jsonify({"success": success, "message" if success else "error": msg}), (200 if success else 400)


# =====================================================================
# TRANSACTION MANAGEMENT APIS
# =====================================================================

@app.route("/api/transactions", methods=["GET"])
def get_transactions():
    """Retrieves paginated transactions filtered by category, type, and review status."""
    user = get_current_user()
    search = request.args.get("search", "")
    category = request.args.get("category", "")
    txn_type = request.args.get("txn_type", "")
    review_status = request.args.get("review_status", "")
    limit = int(request.args.get("limit", 50))
    offset = int(request.args.get("offset", 0))

    txns, total = database.get_user_transactions(
        user_id=user["id"],
        role=user["role"],
        search=search,
        category=category,
        txn_type=txn_type,
        review_status=review_status,
        limit=limit,
        offset=offset
    )
    return jsonify({"transactions": txns, "total": total, "limit": limit, "offset": offset})


@app.route("/api/transactions", methods=["POST"])
def create_transaction():
    """Manually records a transaction with real-time AI ML risk scoring."""
    user = get_current_user()
    data = request.get_json(silent=True) or {}

    txn_type = data.get("txn_type", "EXPENSE").upper()
    category = data.get("category", "General")
    amount = float(data.get("amount", 0.0))
    receiver = data.get("receiver_info", "Merchant")
    desc = data.get("description", "")
    method = data.get("payment_method", "UPI")

    if amount <= 0:
        return jsonify({"error": "Transaction amount must be greater than zero."}), 400

    # Fetch user history for ML baseline evaluation
    user_txns, _ = database.get_user_transactions(user["id"], user["role"], limit=20)
    
    # Run AI/ML Fraud Evaluation
    eval_res = MLFraudEngine.evaluate_transaction({
        "amount": amount,
        "category": category,
        "receiver_info": receiver,
        "hour": datetime.now().hour
    }, user_txns)

    review_status = "Pending Review" if eval_res["requires_human_review"] else "Legitimate"

    created = database.create_transaction(
        user_id=user["id"],
        txn_type=txn_type,
        category=category,
        amount=amount,
        receiver_info=receiver,
        description=desc,
        payment_method=method,
        sender_info=user["full_name"],
        is_flagged=eval_res["is_flagged"],
        risk_score=eval_res["risk_score"],
        risk_level=eval_res["risk_level"],
        review_status=review_status,
        ai_reasons=eval_res["attributions"]
    )

    return jsonify({
        "success": True,
        "transaction": created,
        "evaluation": eval_res,
        "message": "Transaction recorded." if not eval_res["is_flagged"] else "Transaction flagged by AI Security Shield for human review."
    })


@app.route("/api/transactions/<int:txn_id>", methods=["DELETE"])
def delete_transaction(txn_id: int):
    """Deletes a transaction."""
    user = get_current_user()
    success = database.delete_transaction(txn_id, user["id"], user["role"])
    if success:
        return jsonify({"success": True, "message": "Transaction removed."})
    return jsonify({"success": False, "error": "Transaction not found or unauthorized."}), 404


# =====================================================================
# PAYMENT SIMULATOR APIS
# =====================================================================

@app.route("/api/simulator/pay", methods=["POST"])
def simulate_payment():
    """
    Simulates a digital payment transaction with pre-flight AI fraud analysis.
    Executes transaction, updates balances, and handles quarantine if flagged.
    """
    user = get_current_user()
    data = request.get_json(silent=True) or {}

    amount = float(data.get("amount", 0.0))
    receiver_upi = data.get("receiver_upi", "").strip()
    category = data.get("category", "Shopping & Retail")
    description = data.get("description", "Simulated Payment")
    payment_method = data.get("payment_method", "UPI")

    if amount <= 0:
        return jsonify({"success": False, "error": "Payment amount must be greater than ₹0."}), 400

    if not receiver_upi:
        return jsonify({"success": False, "error": "Receiver UPI ID / Account is required."}), 400

    # Fetch user history
    user_txns, _ = database.get_user_transactions(user["id"], user["role"], limit=20)

    # Evaluate transaction through AI/ML Engine
    hour = datetime.now().hour
    eval_res = MLFraudEngine.evaluate_transaction({
        "amount": amount,
        "category": category,
        "receiver_info": receiver_upi,
        "hour": hour
    }, user_txns)

    is_flagged = 1 if (eval_res["requires_human_review"] or eval_res["risk_score"] >= 60.0 or eval_res["risk_level"] in ["HIGH_RISK", "CRITICAL"]) else 0
    review_status = "Pending Review" if is_flagged else "Legitimate"

    # Create transaction
    txn = database.create_transaction(
        user_id=user["id"],
        txn_type="EXPENSE",
        category=category,
        amount=amount,
        receiver_info=receiver_upi,
        description=description,
        payment_method=payment_method,
        sender_info=user["full_name"],
        is_flagged=is_flagged,
        risk_score=eval_res["risk_score"],
        risk_level=eval_res["risk_level"],
        review_status=review_status,
        ai_reasons=eval_res["attributions"]
    )

    updated_user = database.get_user_by_id(user["id"])

    response_data = {
        "success": True,
        "transaction_ref": txn["transaction_ref"],
        "transaction_id": txn["id"],
        "amount": amount,
        "receiver": receiver_upi,
        "status": "HELD_FOR_REVIEW" if is_flagged else "SUCCESSFUL",
        "review_status": review_status,
        "risk_score": eval_res["risk_score"],
        "risk_level": eval_res["risk_level"],
        "attributions": eval_res["attributions"],
        "recommendation": eval_res["recommended_action"],
        "ml_breakdown": eval_res["ml_breakdown"],
        "updated_wallet_balance": updated_user["wallet_balance"]
    }

    return jsonify(response_data)


# =====================================================================
# AI/ML FRAUD DETECTION & BENCHMARKS APIS
# =====================================================================

@app.route("/api/fraud/evaluate", methods=["POST"])
def evaluate_custom_fraud():
    """Runs AI/ML fraud evaluation on any arbitrary transaction parameters."""
    user = get_current_user()
    data = request.get_json(silent=True) or {}
    user_txns, _ = database.get_user_transactions(user["id"], user["role"], limit=20)
    result = MLFraudEngine.evaluate_transaction(data, user_txns)
    return jsonify(result)


@app.route("/api/fraud/model-metrics", methods=["GET"])
def get_model_metrics():
    """Returns AI/ML model performance evaluation metrics (Accuracy, Precision, Recall, F1, Matrix)."""
    metrics = MLFraudEngine.get_model_evaluation_metrics()
    return jsonify(metrics)


# =====================================================================
# HUMAN REVIEW WORKFLOW APIS
# =====================================================================

@app.route("/api/review/queue", methods=["GET"])
def get_compliance_review_queue():
    """Returns all flagged transactions awaiting human compliance officer review."""
    queue = database.get_review_queue(limit=50)
    return jsonify({"queue": queue, "total_pending": len(queue)})


@app.route("/api/review/decision", methods=["POST"])
def submit_review_decision():
    """Submits a human reviewer's compliance decision on a flagged transaction."""
    user = get_current_user()
    data = request.get_json(silent=True) or {}

    txn_id = int(data.get("transaction_id", 0))
    decision = data.get("decision", "")
    notes = data.get("notes", "Reviewed and verified by compliance officer.")

    if not txn_id or not decision:
        return jsonify({"success": False, "error": "Transaction ID and decision are required."}), 400

    success, msg = database.submit_review_decision(
        transaction_id=txn_id,
        reviewer_id=user["id"],
        new_status=decision,
        reviewer_notes=notes
    )

    return jsonify({"success": success, "message" if success else "error": msg}), (200 if success else 400)


@app.route("/api/review/audit-logs", methods=["GET"])
def get_review_audit_logs():
    """Retrieves full audit log history of reviewer compliance decisions."""
    logs = database.get_review_audit_logs(limit=50)
    return jsonify({"logs": logs})


# =====================================================================
# SMART BUDGET PLANNER & SAVINGS GOALS APIS
# =====================================================================

@app.route("/api/budgets", methods=["GET"])
def get_budgets():
    """Fetches user monthly budgets with real-time expenditure calculations."""
    user = get_current_user()
    budgets = database.get_user_budgets(user["id"])
    return jsonify({"budgets": budgets})


@app.route("/api/budgets", methods=["POST"])
def set_budget():
    """Creates or updates a category budget allocation."""
    user = get_current_user()
    data = request.get_json(silent=True) or {}

    category = data.get("category", "")
    limit_amt = float(data.get("monthly_limit", 0.0))
    alert_thresh = float(data.get("alert_threshold", 80.0))

    if not category or limit_amt <= 0:
        return jsonify({"success": False, "error": "Valid category and budget limit are required."}), 400

    database.set_user_budget(user["id"], category, limit_amt, alert_thresh)
    return jsonify({"success": True, "message": f"Budget set for {category} at ₹{limit_amt:,.2f}."})


@app.route("/api/budgets/<int:budget_id>", methods=["DELETE"])
def delete_budget(budget_id: int):
    """Deletes a budget allocation."""
    user = get_current_user()
    success = database.delete_user_budget(budget_id, user["id"])
    return jsonify({"success": success})


@app.route("/api/savings-goals", methods=["GET"])
def get_savings():
    """Retrieves all savings goals and progress."""
    user = get_current_user()
    goals = database.get_savings_goals(user["id"])
    return jsonify({"goals": goals})


@app.route("/api/savings-goals", methods=["POST"])
def create_savings_goal():
    """Creates a new savings goal."""
    user = get_current_user()
    data = request.get_json(silent=True) or {}

    name = data.get("goal_name", "").strip()
    target = float(data.get("target_amount", 0.0))
    current = float(data.get("current_amount", 0.0))
    target_date = data.get("target_date", "")
    category = data.get("category", "General")

    if not name or target <= 0:
        return jsonify({"success": False, "error": "Goal name and target amount are required."}), 400

    goal_id = database.create_savings_goal(user["id"], name, target, current, target_date, category)
    return jsonify({"success": True, "goal_id": goal_id, "message": "Savings goal created!"})


@app.route("/api/savings-goals/<int:goal_id>/deposit", methods=["POST"])
def deposit_savings_goal(goal_id: int):
    """Adds funds to a savings goal."""
    user = get_current_user()
    data = request.get_json(silent=True) or {}
    amount = float(data.get("amount", 0.0))

    if amount <= 0:
        return jsonify({"success": False, "error": "Deposit amount must be greater than zero."}), 400

    success = database.update_savings_goal_progress(goal_id, user["id"], amount)
    return jsonify({"success": success, "message": "Savings goal progress updated!"})


# =====================================================================
# FINANCIAL ANALYTICS & SPENDING FORECAST APIS
# =====================================================================

@app.route("/api/analytics/summary", methods=["GET"])
def get_analytics_summary():
    """Returns comprehensive financial metrics, trends, and category breakdowns."""
    user = get_current_user()
    analytics = database.get_financial_analytics(user["id"], user["role"])
    return jsonify(analytics)


@app.route("/api/forecast/predict", methods=["GET"])
def get_spending_forecast():
    """Generates weekly and monthly predictive spending forecasts."""
    user = get_current_user()
    user_txns, _ = database.get_user_transactions(user["id"], user["role"], limit=100)
    forecast = SpendingForecastingEngine.generate_forecast(user_txns, user["wallet_balance"])
    return jsonify(forecast)


# =====================================================================
# NOTIFICATION SERVICES APIS
# =====================================================================

@app.route("/api/notifications", methods=["GET"])
def get_notifications():
    """Fetches user notifications."""
    user = get_current_user()
    notifs = database.get_user_notifications(user["id"], limit=30)
    unread_count = sum(1 for n in notifs if n["is_read"] == 0)
    return jsonify({"notifications": notifs, "unread_count": unread_count})


@app.route("/api/notifications/<int:notif_id>/read", methods=["POST"])
def mark_notif_read(notif_id: int):
    """Marks a single notification as read."""
    user = get_current_user()
    database.mark_notification_read(notif_id, user["id"])
    return jsonify({"success": True})


@app.route("/api/notifications/read-all", methods=["POST"])
def mark_all_notifs_read():
    """Marks all user notifications as read."""
    user = get_current_user()
    database.mark_all_notifications_read(user["id"])
    return jsonify({"success": True})


# =====================================================================
# AI FINANCIAL ASSISTANT (CHATBOT) API
# =====================================================================

@app.route("/api/chatbot/query", methods=["POST"])
def chatbot_query():
    """Contextual conversational response grounded in user's actual financial records."""
    user = get_current_user()
    data = request.get_json(silent=True) or {}
    query = data.get("query", "").strip()

    if not query:
        return jsonify({"answer": "Please ask a question regarding your finances or payment security."}), 400

    financial_summary = database.get_financial_analytics(user["id"], user["role"])
    result = FinancialChatbotEngine.process_query(query, user, financial_summary)
    return jsonify(result)


# =====================================================================
# ADMIN OPERATIONS APIS
# =====================================================================

@app.route("/api/admin/users", methods=["GET"])
def admin_get_users():
    """Admin view of all registered users."""
    user = get_current_user()
    users = database.get_all_users_list()
    return jsonify({"users": users})


@app.route("/api/admin/system-stats", methods=["GET"])
def admin_get_stats():
    """System-wide administrative health and security statistics."""
    stats = database.get_admin_system_stats()
    return jsonify(stats)


# =====================================================================
# REPORT GENERATION & DOWNLOADS
# =====================================================================

@app.route("/api/reports/export-csv", methods=["GET"])
def export_transactions_csv():
    """Exports user transactions as a downloadable CSV spreadsheet."""
    user = get_current_user()
    txns, _ = database.get_user_transactions(user["id"], user["role"], limit=500)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Transaction Reference", "Date & Time", "Type", "Category", 
        "Amount (INR)", "Payment Method", "Counterparty", "Risk Score", 
        "Risk Level", "Review Status", "Description"
    ])

    for t in txns:
        writer.writerow([
            t["transaction_ref"],
            t["created_at"],
            t["txn_type"],
            t["category"],
            f"{t['amount']:.2f}",
            t["payment_method"],
            t["receiver_info"],
            t["risk_score"],
            t["risk_level"],
            t["review_status"],
            t["description"]
        ])

    csv_data = output.getvalue()
    response = make_response(csv_data)
    response.headers["Content-Disposition"] = f"attachment; filename=NexaPay_Transactions_{datetime.now().strftime('%Y%m%d')}.csv"
    response.headers["Content-Type"] = "text/csv; charset=utf-8"
    return response


@app.route("/api/reports/statement", methods=["GET"])
def export_statement():
    """Generates a clean HTML/printable summary statement for the user."""
    user = get_current_user()
    analytics = database.get_financial_analytics(user["id"], user["role"])
    txns, _ = database.get_user_transactions(user["id"], user["role"], limit=20)
    
    return render_template(
        "statement.html",
        user=user,
        analytics=analytics,
        transactions=txns,
        generated_date=datetime.now().strftime("%d %B %Y, %I:%M %p")
    )


# =====================================================================
# PRESERVED CYBERSECURITY SCANNER APIS
# =====================================================================

@app.route("/api/scanner/link", methods=["POST"])
def scan_link():
    """Evaluates suspicious URLs for phishing, spoofing and rogue domains."""
    data = request.get_json(silent=True) or {}
    url = data.get("url", "").strip()
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400

    result = LinkScannerEngine.scan_url(url)
    database.log_scan_event(
        scan_type="LINK",
        input_preview=url,
        risk_score=result["risk_score"],
        risk_level=result["risk_level"],
        explanations=result["attributions"]
    )
    return jsonify(result)


@app.route("/api/scanner/otp", methods=["POST"])
def scan_otp():
    """Identifies credential harvesting and OTP/PIN extortion patterns."""
    data = request.get_json(silent=True) or {}
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "Text parameter is required"}), 400

    result = OTPScamDetectorEngine.scan_message(text)
    database.log_scan_event(
        scan_type="OTP",
        input_preview=text,
        risk_score=result["risk_score"],
        risk_level=result["risk_level"],
        explanations=result["attributions"]
    )
    return jsonify(result)


@app.route("/api/scanner/message", methods=["POST"])
def scan_message():
    """Analyzes text messages for fraud patterns (electricity, jobs, lottery, etc.)."""
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"error": "Message parameter is required"}), 400

    result = MessageScannerEngine.scan_message(message)
    database.log_scan_event(
        scan_type="MESSAGE",
        input_preview=message,
        risk_score=result["risk_score"],
        risk_level=result["risk_level"],
        explanations=result["attributions"]
    )
    return jsonify(result)


@app.route("/api/scanner/qr", methods=["POST"])
def scan_qr():
    """Decodes QR codes and inspects UPI payloads."""
    raw_payload = None

    if "file" in request.files:
        file = request.files["file"]
        if file.filename:
            file_bytes = file.read()
            raw_payload = QRScannerEngine.decode_qr_bytes(file_bytes)
            if not raw_payload:
                return jsonify({
                    "error": "Could not decode any QR code from the uploaded image.",
                    "risk_score": 0.0,
                    "risk_level": "UNKNOWN"
                }), 400

    if not raw_payload:
        data = request.get_json(silent=True) or {}
        raw_payload = data.get("payload", "").strip()

    if not raw_payload:
        return jsonify({"error": "Either an image file or a raw payload string is required"}), 400

    result = QRScannerEngine.inspect_payload(raw_payload)
    database.log_scan_event(
        scan_type="QR",
        input_preview=raw_payload,
        risk_score=result.get("risk_score", 0.0),
        risk_level=result.get("risk_level", "SAFE"),
        explanations=result.get("attributions", [])
    )
    return jsonify(result)


@app.route("/api/dashboard/stats", methods=["GET"])
def get_stats():
    """Returns current security health metrics and recent scan history."""
    metrics = database.get_dashboard_metrics()
    recent = database.get_recent_scans(10)
    return jsonify({"metrics": metrics, "recent_scans": recent})


@app.route("/api/academy/modules", methods=["GET"])
def get_academy_modules():
    """Returns the 10 educational modules and interactive quizzes."""
    json_path = os.path.join(app.root_path, "static", "data", "academy_modules.json")
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            modules = json.load(f)
        return jsonify(modules)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/academy/submit", methods=["POST"])
def submit_quiz():
    """Records quiz score and updates badge progress."""
    data = request.get_json(silent=True) or {}
    module_id = int(data.get("module_id", 0))
    score = int(data.get("score", 0))
    if module_id > 0:
        database.record_academy_progress(module_id, score)
        return jsonify({"success": True, "message": f"Module {module_id} completed with score {score}!"})
    return jsonify({"error": "Invalid module ID"}), 400


@app.route("/api/fraud/analytics", methods=["GET"])
def get_fraud_analytics():
    """Returns synthetic transaction stream and predictive anomaly risk summary."""
    anomalies = [
        AnomalyDetectionEngine.analyze_transaction(tx, SYNTHETIC_TX_CACHE)
        for tx in SYNTHETIC_TX_CACHE
    ]
    anomalous_count = sum(1 for a in anomalies if a["is_anomalous"])
    
    return jsonify({
        "transactions": SYNTHETIC_TX_CACHE,
        "anomalies": anomalies,
        "summary": {
            "total_transactions": len(SYNTHETIC_TX_CACHE),
            "anomalous_detected": anomalous_count,
            "anomaly_rate": round((anomalous_count / len(SYNTHETIC_TX_CACHE)) * 100, 1),
            "baseline_avg_amount": 1850.00
        }
    })


@app.route("/api/fraud/analyze-txn", methods=["POST"])
def analyze_single_transaction():
    """Evaluates a single custom transaction for anomalies."""
    data = request.get_json(silent=True) or {}
    res = AnomalyDetectionEngine.analyze_transaction(data, SYNTHETIC_TX_CACHE)
    return jsonify(res)


@app.route("/api/reports/generate", methods=["POST"])
def generate_report():
    """Generates an official Cybercrime incident complaint dossier (1930)."""
    data = request.get_json(silent=True) or {}
    report_num = database.save_fraud_report(data)
    
    response = {
        "report_number": report_num,
        "status": "GENERATED",
        "instructions": "Present this formal dossier when lodging an FIR or calling 1930 / cybercrime.gov.in.",
        "data": {
            "report_number": report_num,
            "fraud_type": data.get("fraud_type", "DIGITAL_PAYMENT_FRAUD"),
            "suspected_entity": data.get("suspected_entity", "Unknown"),
            "financial_loss": float(data.get("financial_loss", 0.0)),
            "description": data.get("description", ""),
            "helpline": "1930",
            "portal": "https://cybercrime.gov.in"
        }
    }
    return jsonify(response)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
