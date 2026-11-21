"""
NEXAPAY Database Layer (SQLite)
Manages Users, Roles, Transactions, Budgets, Savings Goals, Fraud Detection,
Human Review Queue, Notifications, Audit Logs, Spending Forecasts, Scan Logs,
and Academy Progress.
"""

import sqlite3
import json
import os
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple

DB_PATH = os.path.join(os.path.dirname(__file__), "nexapay.db")


def get_db_connection():
    """Returns a SQLite connection with row factory enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def hash_password(password: str, salt: Optional[str] = None) -> Tuple[str, str]:
    """Hashes password with PBKDF2-HMAC-SHA256 and unique salt."""
    if not salt:
        salt = secrets.token_hex(16)
    pwd_hash = hashlib.pbkdf2_hmac(
        "sha256", 
        password.encode("utf-8"), 
        salt.encode("utf-8"), 
        100000
    ).hex()
    return pwd_hash, salt


def verify_password(stored_hash: str, salt: str, password_attempt: str) -> bool:
    """Verifies a password attempt against stored PBKDF2 hash."""
    calc_hash, _ = hash_password(password_attempt, salt)
    return secrets.compare_digest(stored_hash, calc_hash)


def init_db():
    """Initializes all database tables and seeds demo accounts if empty."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT,
        password_hash TEXT NOT NULL,
        salt TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'individual', 
        business_name TEXT,
        language_pref TEXT DEFAULT 'en',
        wallet_balance REAL DEFAULT 25000.0,
        status TEXT DEFAULT 'ACTIVE',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 2. Transactions Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        transaction_ref TEXT UNIQUE NOT NULL,
        txn_type TEXT NOT NULL, 
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        payment_method TEXT DEFAULT 'UPI',
        sender_info TEXT,
        receiver_info TEXT,
        description TEXT,
        is_flagged INTEGER DEFAULT 0,
        risk_score REAL DEFAULT 5.0,
        risk_level TEXT DEFAULT 'SAFE',
        review_status TEXT DEFAULT 'Legitimate', 
        reviewer_notes TEXT,
        ai_reasons TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    # 3. Budgets Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS budgets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        category TEXT NOT NULL,
        monthly_limit REAL NOT NULL,
        month INTEGER NOT NULL,
        year INTEGER NOT NULL,
        alert_threshold REAL DEFAULT 80.0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, category, month, year),
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    # 4. Savings Goals Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS savings_goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        goal_name TEXT NOT NULL,
        target_amount REAL NOT NULL,
        current_amount REAL DEFAULT 0.0,
        target_date TEXT,
        category TEXT DEFAULT 'General',
        status TEXT DEFAULT 'IN_PROGRESS',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    # 5. Notifications Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        message TEXT NOT NULL,
        notification_type TEXT NOT NULL,
        is_read INTEGER DEFAULT 0,
        metadata TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    # 6. Human Review & Audit Logs Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS review_audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        transaction_id INTEGER NOT NULL,
        reviewer_id INTEGER NOT NULL,
        reviewer_name TEXT NOT NULL,
        previous_status TEXT NOT NULL,
        new_status TEXT NOT NULL,
        reviewer_notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (transaction_id) REFERENCES transactions (id),
        FOREIGN KEY (reviewer_id) REFERENCES users (id)
    )
    """)

    # 7. Spending Forecasts Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS spending_forecasts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        period_type TEXT NOT NULL, 
        predicted_amount REAL NOT NULL,
        confidence_score REAL DEFAULT 88.0,
        insights_json TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    # 8. Scan Logs Table (Preserved from existing)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scan_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER DEFAULT 1,
        scan_type TEXT NOT NULL,
        input_preview TEXT NOT NULL,
        risk_score REAL NOT NULL,
        risk_level TEXT NOT NULL,
        explanations TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 9. Fraud Reports Table (Preserved from existing)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fraud_reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        report_number TEXT UNIQUE NOT NULL,
        user_id INTEGER DEFAULT 1,
        fraud_type TEXT NOT NULL,
        suspected_entity TEXT NOT NULL,
        financial_loss REAL DEFAULT 0.0,
        description TEXT NOT NULL,
        status TEXT DEFAULT 'FILED',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 10. Academy Progress Table (Preserved from existing)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS academy_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER DEFAULT 1,
        module_id INTEGER NOT NULL,
        score INTEGER NOT NULL,
        completed INTEGER DEFAULT 1,
        completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, module_id)
    )
    """)

    # 11. Synthetic Transactions Table (Preserved from existing)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS synthetic_transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        transaction_ref TEXT UNIQUE NOT NULL,
        amount REAL NOT NULL,
        receiver_upi TEXT NOT NULL,
        category TEXT NOT NULL,
        is_anomalous INTEGER DEFAULT 0,
        anomaly_score REAL DEFAULT 0.0,
        timestamp TEXT NOT NULL
    )
    """)

    conn.commit()

    # Seed Default Users & Demo Data if users table is empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        seed_demo_data(cursor)
        conn.commit()

    conn.close()


def seed_demo_data(cursor):
    """Populates realistic seed data for all 4 roles and starter transactions."""
    now = datetime.now()
    
    # 4 Seed Roles
    demo_users = [
        {
            "name": "Aditya Verma",
            "email": "individual@nexapay.local",
            "phone": "+91 98765 43210",
            "role": "individual",
            "business": None,
            "balance": 42500.0
        },
        {
            "name": "Rajesh Kumar",
            "email": "shop@nexapay.local",
            "phone": "+91 98123 45678",
            "role": "shop_owner",
            "business": "Kumar General Kirana & Superstore",
            "balance": 185600.0
        },
        {
            "name": "Priya Sharma",
            "email": "business@nexapay.local",
            "phone": "+91 99234 56789",
            "role": "business",
            "business": "NexaTech Enterprise Solutions Pvt Ltd",
            "balance": 840000.0
        },
        {
            "name": "Vikram Singh",
            "email": "admin@nexapay.local",
            "phone": "+91 99887 76655",
            "role": "admin_reviewer",
            "business": "NexaPay Financial Intelligence Unit",
            "balance": 50000.0
        }
    ]

    for u in demo_users:
        pwd_hash, salt = hash_password("demo123")
        cursor.execute("""
        INSERT INTO users (full_name, email, phone, password_hash, salt, role, business_name, wallet_balance)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (u["name"], u["email"], u["phone"], pwd_hash, salt, u["role"], u["business"], u["balance"]))

    # Seed Sample Transactions for Individual (User ID 1)
    individual_txns = [
        ("TXN-IND-101", "INCOME", "Salary & Wages", 65000.0, "NetBanking", "Apex Software Corp", "Aditya Verma", "Monthly Salary Credit", 0, 5.0, "SAFE", "Legitimate", None, "[]", (now - timedelta(days=20)).strftime("%Y-%m-%d 10:15:00")),
        ("TXN-IND-102", "EXPENSE", "Rent & Housing", 18000.0, "UPI", "Aditya Verma", "Landlord Ramesh", "Monthly Apartment Rent", 0, 8.0, "SAFE", "Legitimate", None, "[]", (now - timedelta(days=19)).strftime("%Y-%m-%d 11:30:00")),
        ("TXN-IND-103", "EXPENSE", "Groceries", 4200.0, "UPI", "Aditya Verma", "NatureBasket UPI", "Weekly organic groceries", 0, 10.0, "SAFE", "Legitimate", None, "[]", (now - timedelta(days=15)).strftime("%Y-%m-%d 18:45:00")),
        ("TXN-IND-104", "EXPENSE", "Utilities & Bills", 2450.0, "UPI", "Aditya Verma", "Tata Power DDL", "Electricity Bill Payment", 0, 6.0, "SAFE", "Legitimate", None, "[]", (now - timedelta(days=12)).strftime("%Y-%m-%d 14:20:00")),
        ("TXN-IND-105", "EXPENSE", "Food & Dining", 1320.0, "Card", "Aditya Verma", "Zomato Online", "Weekend family dinner", 0, 12.0, "SAFE", "Legitimate", None, "[]", (now - timedelta(days=8)).strftime("%Y-%m-%d 20:15:00")),
        ("TXN-IND-106", "EXPENSE", "Shopping & Retail", 8500.0, "UPI", "Aditya Verma", "Amazon India Pay", "New monitor and headphones", 0, 15.0, "SAFE", "Legitimate", None, "[]", (now - timedelta(days=5)).strftime("%Y-%m-%d 16:10:00")),
        ("TXN-IND-107", "EXPENSE", "Suspicious Transfer", 78000.0, "UPI", "Aditya Verma", "unknown_crypto_agent@ybl", "Urgent investment lottery deposit", 1, 92.5, "CRITICAL", "Pending Review", None, json.dumps([{"factor": "Extreme Amount Spike", "score": 45, "detail": "Amount is 9.4x higher than standard median spend"}, {"factor": "Odd Hours", "score": 25, "detail": "Initiated at 02:45 AM"}, {"factor": "Unseen High-Risk Recipient", "score": 22.5, "detail": "Recipient identifier flagged for high velocity churn"}]), (now - timedelta(days=1)).strftime("%Y-%m-%d 02:45:00")),
        ("TXN-IND-108", "EXPENSE", "Healthcare", 1850.0, "UPI", "Aditya Verma", "Apollo Pharmacy", "Prescription medicines", 0, 5.0, "SAFE", "Legitimate", None, "[]", now.strftime("%Y-%m-%d 09:30:00"))
    ]

    for tx in individual_txns:
        cursor.execute("""
        INSERT INTO transactions (user_id, transaction_ref, txn_type, category, amount, payment_method, sender_info, receiver_info, description, is_flagged, risk_score, risk_level, review_status, reviewer_notes, ai_reasons, created_at)
        VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, tx)

    # Seed Sample Transactions for Shop Owner (User ID 2)
    shop_txns = [
        ("TXN-SHP-201", "INCOME", "Counter Sales", 24800.0, "UPI", "Retail Customers", "Kumar General Store", "Daily Morning QR Collections", 0, 5.0, "SAFE", "Legitimate", None, "[]", (now - timedelta(days=3)).strftime("%Y-%m-%d 13:00:00")),
        ("TXN-SHP-202", "INCOME", "Counter Sales", 31200.0, "UPI", "Retail Customers", "Kumar General Store", "Evening Rush QR Collections", 0, 5.0, "SAFE", "Legitimate", None, "[]", (now - timedelta(days=2)).strftime("%Y-%m-%d 21:30:00")),
        ("TXN-SHP-203", "EXPENSE", "Inventory Supplies", 45000.0, "NetBanking", "Kumar General Store", "FMCG Wholesale Distributor", "Weekly Grocery & Dairy Restock", 0, 10.0, "SAFE", "Legitimate", None, "[]", (now - timedelta(days=2)).strftime("%Y-%m-%d 11:00:00")),
        ("TXN-SHP-204", "EXPENSE", "Utilities & Bills", 6200.0, "UPI", "Kumar General Store", "Commercial Electric Board", "Store Air Conditioning Bill", 0, 8.0, "SAFE", "Legitimate", None, "[]", (now - timedelta(days=1)).strftime("%Y-%m-%d 15:40:00")),
        ("TXN-SHP-205", "EXPENSE", "Suspicious Reversal", 49999.0, "UPI", "Kumar General Store", "fast_refund_agent@paytm", "Claimed duplicate UPI QR payment refund", 1, 86.0, "CRITICAL", "Pending Review", None, json.dumps([{"factor": "Immediate Large Refund Request", "score": 40, "detail": "Reversal requested without matching inbound credit"}, {"factor": "Social Engineering Pattern", "score": 46, "detail": "Customer demanded quick PIN entry on shop soundbox"}]), (now - timedelta(hours=6)).strftime("%Y-%m-%d 17:15:00"))
    ]

    for tx in shop_txns:
        cursor.execute("""
        INSERT INTO transactions (user_id, transaction_ref, txn_type, category, amount, payment_method, sender_info, receiver_info, description, is_flagged, risk_score, risk_level, review_status, reviewer_notes, ai_reasons, created_at)
        VALUES (2, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, tx)

    # Seed Budgets for Individual (User ID 1)
    current_month = now.month
    current_year = now.year
    seed_budgets = [
        (1, "Food & Dining", 6000.0, current_month, current_year),
        (1, "Groceries", 12000.0, current_month, current_year),
        (1, "Shopping & Retail", 10000.0, current_month, current_year),
        (1, "Utilities & Bills", 5000.0, current_month, current_year),
        (1, "Healthcare", 4000.0, current_month, current_year),
        (2, "Inventory Supplies", 150000.0, current_month, current_year),
        (2, "Utilities & Bills", 15000.0, current_month, current_year)
    ]

    for b in seed_budgets:
        cursor.execute("""
        INSERT INTO budgets (user_id, category, monthly_limit, month, year)
        VALUES (?, ?, ?, ?, ?)
        """, b)

    # Seed Savings Goals
    seed_goals = [
        (1, "Emergency Fund (6 Months)", 100000.0, 45000.0, (now + timedelta(days=180)).strftime("%Y-%m-%d"), "Safety Reserve"),
        (1, "MacBook Pro Upgrade", 150000.0, 60000.0, (now + timedelta(days=120)).strftime("%Y-%m-%d"), "Gadgets"),
        (2, "Store Cold Storage Unit", 200000.0, 110000.0, (now + timedelta(days=90)).strftime("%Y-%m-%d"), "Business Expansion")
    ]

    for g in seed_goals:
        cursor.execute("""
        INSERT INTO savings_goals (user_id, goal_name, target_amount, current_amount, target_date, category)
        VALUES (?, ?, ?, ?, ?, ?)
        """, g)

    # Seed Starter Notifications
    seed_notifs = [
        (1, "High-Risk Transaction Flagged", "A payment of ₹78,000 to unknown_crypto_agent@ybl was quarantined for security review.", "FRAUD_ALERT", 0, json.dumps({"txn_ref": "TXN-IND-107", "risk_score": 92.5})),
        (1, "Monthly Budget Alert", "You have utilized 85% of your Shopping & Retail monthly budget allocation.", "BUDGET_WARNING", 0, None),
        (1, "Financial Safety Shield Active", "Your account is protected by real-time AI anomaly detection and zero-trust safeguards.", "SYSTEM", 1, None),
        (2, "Suspicious Payment Alert", "A reverse refund request of ₹49,999 has been held for reviewer verification.", "FRAUD_ALERT", 0, json.dumps({"txn_ref": "TXN-SHP-205", "risk_score": 86.0})),
        (4, "New Flagged Transactions in Review Queue", "2 high-risk transactions require your human compliance review decision.", "REVIEW_UPDATE", 0, None)
    ]

    for n in seed_notifs:
        cursor.execute("""
        INSERT INTO notifications (user_id, title, message, notification_type, is_read, metadata)
        VALUES (?, ?, ?, ?, ?, ?)
        """, n)


# =====================================================================
# USER & AUTHENTICATION FUNCTIONS
# =====================================================================

def register_user(full_name: str, email: str, password: str, role: str = "individual", phone: str = "", business_name: str = "") -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """Registers a new user with secure password hashing."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    clean_email = email.strip().lower()
    cursor.execute("SELECT id FROM users WHERE email = ?", (clean_email,))
    if cursor.fetchone():
        conn.close()
        return False, "An account with this email address already exists.", None

    pwd_hash, salt = hash_password(password)
    valid_roles = ["individual", "shop_owner", "business", "admin_reviewer"]
    assigned_role = role if role in valid_roles else "individual"

    initial_balance = 25000.0 if assigned_role == "individual" else (100000.0 if assigned_role == "shop_owner" else 500000.0)

    try:
        cursor.execute("""
        INSERT INTO users (full_name, email, phone, password_hash, salt, role, business_name, wallet_balance)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (full_name.strip(), clean_email, phone.strip(), pwd_hash, salt, assigned_role, business_name.strip(), initial_balance))
        new_id = cursor.lastrowid
        conn.commit()

        # Create welcome notification
        cursor.execute("""
        INSERT INTO notifications (user_id, title, message, notification_type)
        VALUES (?, 'Welcome to NexaPay!', 'Your secure AI-powered FinTech account is active. Explore smart budgeting and fraud defense.', 'SYSTEM')
        """, (new_id,))
        conn.commit()

        user_data = get_user_by_id(new_id)
        conn.close()
        return True, "Registration successful!", user_data
    except Exception as e:
        conn.close()
        return False, f"Registration failed: {str(e)}", None


def authenticate_user(email: str, password_attempt: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """Authenticates user credentials."""
    conn = get_db_connection()
    cursor = conn.cursor()
    clean_email = email.strip().lower()

    cursor.execute("SELECT * FROM users WHERE email = ?", (clean_email,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return False, "Invalid email or password.", None

    if not verify_password(user["password_hash"], user["salt"], password_attempt):
        return False, "Invalid email or password.", None

    user_dict = dict(user)
    user_dict.pop("password_hash", None)
    user_dict.pop("salt", None)
    return True, "Authentication successful.", user_dict


def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """Fetches user profile by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, full_name, email, phone, role, business_name, language_pref, wallet_balance, status, created_at FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def update_user_profile(user_id: int, full_name: str, phone: str, business_name: str, language_pref: str) -> bool:
    """Updates user personal details."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE users 
    SET full_name = ?, phone = ?, business_name = ?, language_pref = ?
    WHERE id = ?
    """, (full_name.strip(), phone.strip(), business_name.strip(), language_pref, user_id))
    conn.commit()
    conn.close()
    return True


def change_user_password(user_id: int, current_pwd: str, new_pwd: str) -> Tuple[bool, str]:
    """Updates user password after verifying existing password."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash, salt FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return False, "User not found."

    if not verify_password(row["password_hash"], row["salt"], current_pwd):
        conn.close()
        return False, "Incorrect current password."

    new_hash, new_salt = hash_password(new_pwd)
    cursor.execute("UPDATE users SET password_hash = ?, salt = ? WHERE id = ?", (new_hash, new_salt, user_id))
    conn.commit()
    conn.close()
    return True, "Password updated successfully."


# =====================================================================
# TRANSACTION MANAGEMENT
# =====================================================================

def create_transaction(
    user_id: int, 
    txn_type: str, 
    category: str, 
    amount: float, 
    receiver_info: str, 
    description: str = "",
    payment_method: str = "UPI",
    sender_info: str = "",
    is_flagged: int = 0,
    risk_score: float = 5.0,
    risk_level: str = "SAFE",
    review_status: str = "Legitimate",
    ai_reasons: Any = None
) -> Dict[str, Any]:
    """Records a new transaction and adjusts user wallet balance."""
    conn = get_db_connection()
    cursor = conn.cursor()

    ref = f"TXN-{datetime.now().strftime('%Y%m%d%H%M%S')}-{secrets.token_hex(2).upper()}"
    reasons_str = json.dumps(ai_reasons) if ai_reasons and not isinstance(ai_reasons, str) else (ai_reasons or "[]")

    cursor.execute("""
    INSERT INTO transactions (
        user_id, transaction_ref, txn_type, category, amount, payment_method, 
        sender_info, receiver_info, description, is_flagged, risk_score, 
        risk_level, review_status, ai_reasons
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id, ref, txn_type.upper(), category, amount, payment_method,
        sender_info, receiver_info, description, is_flagged, risk_score,
        risk_level, review_status, reasons_str
    ))
    new_txn_id = cursor.lastrowid

    # Update wallet balance if transaction is legitimate or safe (do not deduct if pending high risk review)
    if review_status != "Pending Review":
        if txn_type.upper() == "EXPENSE":
            cursor.execute("UPDATE users SET wallet_balance = wallet_balance - ? WHERE id = ?", (amount, user_id))
        elif txn_type.upper() == "INCOME":
            cursor.execute("UPDATE users SET wallet_balance = wallet_balance + ? WHERE id = ?", (amount, user_id))

    # Trigger Fraud Notification if flagged
    if is_flagged or risk_level in ["HIGH_RISK", "CRITICAL"]:
        cursor.execute("""
        INSERT INTO notifications (user_id, title, message, notification_type, metadata)
        VALUES (?, 'High-Risk Payment Flagged', ?, 'FRAUD_ALERT', ?)
        """, (
            user_id, 
            f"Payment of ₹{amount:,.2f} to {receiver_info} triggered AI risk score {risk_score}/100 and has been sent for reviewer verification.",
            json.dumps({"txn_id": new_txn_id, "txn_ref": ref, "risk_score": risk_score, "risk_level": risk_level})
        ))

    conn.commit()
    
    cursor.execute("SELECT * FROM transactions WHERE id = ?", (new_txn_id,))
    row = dict(cursor.fetchone())
    conn.close()
    return row


def get_user_transactions(
    user_id: int, 
    role: str = "individual",
    search: str = "", 
    category: str = "", 
    txn_type: str = "", 
    review_status: str = "",
    limit: int = 50,
    offset: int = 0
) -> Tuple[List[Dict[str, Any]], int]:
    """Fetches filtered transactions. Admin can view all users' transactions."""
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT t.*, u.full_name as user_name FROM transactions t JOIN users u ON t.user_id = u.id WHERE 1=1"
    params = []

    if role != "admin_reviewer":
        query += " AND t.user_id = ?"
        params.append(user_id)

    if search:
        query += " AND (t.transaction_ref LIKE ? OR t.receiver_info LIKE ? OR t.description LIKE ?)"
        s = f"%{search}%"
        params.extend([s, s, s])

    if category:
        query += " AND t.category = ?"
        params.append(category)

    if txn_type:
        query += " AND t.txn_type = ?"
        params.append(txn_type.upper())

    if review_status:
        query += " AND t.review_status = ?"
        params.append(review_status)

    count_query = query.replace("SELECT t.*, u.full_name as user_name", "SELECT COUNT(*)")
    cursor.execute(count_query, params)
    total_count = cursor.fetchone()[0]

    query += " ORDER BY t.id DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    cursor.execute(query, params)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows, total_count


def delete_transaction(txn_id: int, user_id: int, role: str) -> bool:
    """Deletes transaction if permitted."""
    conn = get_db_connection()
    cursor = conn.cursor()
    if role == "admin_reviewer":
        cursor.execute("DELETE FROM transactions WHERE id = ?", (txn_id,))
    else:
        cursor.execute("DELETE FROM transactions WHERE id = ? AND user_id = ?", (txn_id, user_id))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted


# =====================================================================
# HUMAN REVIEW WORKFLOW & AUDIT TRAIL
# =====================================================================

def get_review_queue(limit: int = 50) -> List[Dict[str, Any]]:
    """Retrieves all transactions pending or undergoing human review."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT t.*, u.full_name as user_name, u.email as user_email, u.role as user_role
    FROM transactions t
    JOIN users u ON t.user_id = u.id
    WHERE t.is_flagged = 1 OR t.review_status IN ('Pending Review', 'Under Investigation', 'Suspicious')
    ORDER BY t.risk_score DESC, t.id DESC
    LIMIT ?
    """, (limit,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def submit_review_decision(
    transaction_id: int, 
    reviewer_id: int, 
    new_status: str, 
    reviewer_notes: str
) -> Tuple[bool, str]:
    """Processes a human reviewer's compliance decision on a flagged transaction."""
    valid_statuses = ["Legitimate", "Suspicious", "Under Investigation", "Pending Review"]
    if new_status not in valid_statuses:
        return False, "Invalid review status."

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions WHERE id = ?", (transaction_id,))
    txn = cursor.fetchone()
    if not txn:
        conn.close()
        return False, "Transaction not found."

    prev_status = txn["review_status"]
    user_id = txn["user_id"]
    amount = txn["amount"]
    txn_type = txn["txn_type"]

    cursor.execute("SELECT full_name FROM users WHERE id = ?", (reviewer_id,))
    rev = cursor.fetchone()
    reviewer_name = rev["full_name"] if rev else "Authorized Reviewer"

    # Update transaction review state
    unflag = 1 if new_status in ["Suspicious", "Under Investigation", "Pending Review"] else 0
    cursor.execute("""
    UPDATE transactions 
    SET review_status = ?, reviewer_notes = ?, is_flagged = ?
    WHERE id = ?
    """, (new_status, reviewer_notes, unflag, transaction_id))

    # Log to audit trail
    cursor.execute("""
    INSERT INTO review_audit_logs (transaction_id, reviewer_id, reviewer_name, previous_status, new_status, reviewer_notes)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (transaction_id, reviewer_id, reviewer_name, prev_status, new_status, reviewer_notes))

    # If transitioned from Pending to Legitimate, debit/credit the wallet now
    if prev_status == "Pending Review" and new_status == "Legitimate":
        if txn_type == "EXPENSE":
            cursor.execute("UPDATE users SET wallet_balance = wallet_balance - ? WHERE id = ?", (amount, user_id))
        elif txn_type == "INCOME":
            cursor.execute("UPDATE users SET wallet_balance = wallet_balance + ? WHERE id = ?", (amount, user_id))

    # Send Notification to User
    cursor.execute("""
    INSERT INTO notifications (user_id, title, message, notification_type)
    VALUES (?, 'Transaction Review Status Updated', ?, 'REVIEW_UPDATE')
    """, (
        user_id, 
        f"Your transaction {txn['transaction_ref']} for ₹{amount:,.2f} has been marked as '{new_status}' by the compliance team. Notes: {reviewer_notes}"
    ))

    conn.commit()
    conn.close()
    return True, f"Transaction successfully updated to '{new_status}'."


def get_review_audit_logs(limit: int = 50) -> List[Dict[str, Any]]:
    """Fetches recent audit log history."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT a.*, t.transaction_ref, t.amount, t.category 
    FROM review_audit_logs a
    JOIN transactions t ON a.transaction_id = t.id
    ORDER BY a.id DESC LIMIT ?
    """, (limit,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


# =====================================================================
# BUDGET MANAGEMENT & OVERSPENDING DETECTION
# =====================================================================

def get_user_budgets(user_id: int) -> List[Dict[str, Any]]:
    """Calculates real-time monthly budget vs actual expenditure for the current month."""
    now = datetime.now()
    month = now.month
    year = now.year

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM budgets 
    WHERE user_id = ? AND month = ? AND year = ?
    ORDER BY monthly_limit DESC
    """, (user_id, month, year))
    budgets = [dict(r) for r in cursor.fetchall()]

    # If no budgets set for current month, copy defaults or return empty
    for b in budgets:
        # Sum actual expenses in this category for this month
        cursor.execute("""
        SELECT COALESCE(SUM(amount), 0.0) FROM transactions 
        WHERE user_id = ? AND category = ? AND txn_type = 'EXPENSE'
        AND strftime('%m', created_at) = ? AND strftime('%Y', created_at) = ?
        """, (user_id, b["category"], f"{month:02d}", str(year)))
        spent = cursor.fetchone()[0]
        b["spent_amount"] = spent
        b["remaining"] = max(0.0, b["monthly_limit"] - spent)
        b["percentage"] = round((spent / b["monthly_limit"]) * 100.0, 1) if b["monthly_limit"] > 0 else 0.0
        b["is_exceeded"] = spent > b["monthly_limit"]
        b["is_warning"] = spent >= (b["monthly_limit"] * (b["alert_threshold"] / 100.0))

    conn.close()
    return budgets


def set_user_budget(user_id: int, category: str, monthly_limit: float, alert_threshold: float = 80.0) -> bool:
    """Creates or updates a monthly category budget."""
    now = datetime.now()
    month = now.month
    year = now.year

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO budgets (user_id, category, monthly_limit, month, year, alert_threshold)
    VALUES (?, ?, ?, ?, ?, ?)
    ON CONFLICT(user_id, category, month, year) DO UPDATE SET 
        monthly_limit = excluded.monthly_limit,
        alert_threshold = excluded.alert_threshold
    """, (user_id, category, monthly_limit, month, year, alert_threshold))
    conn.commit()
    conn.close()
    return True


def delete_user_budget(budget_id: int, user_id: int) -> bool:
    """Removes a budget entry."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM budgets WHERE id = ? AND user_id = ?", (budget_id, user_id))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted


# =====================================================================
# SAVINGS GOALS
# =====================================================================

def get_savings_goals(user_id: int) -> List[Dict[str, Any]]:
    """Returns savings goals with calculated progress percentages."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM savings_goals WHERE user_id = ? ORDER BY id DESC", (user_id,))
    goals = [dict(r) for r in cursor.fetchall()]
    for g in goals:
        g["percentage"] = round((g["current_amount"] / g["target_amount"]) * 100.0, 1) if g["target_amount"] > 0 else 0.0
        g["remaining"] = max(0.0, g["target_amount"] - g["current_amount"])
    conn.close()
    return goals


def create_savings_goal(user_id: int, goal_name: str, target_amount: float, current_amount: float, target_date: str, category: str = "General") -> int:
    """Adds a new savings goal."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO savings_goals (user_id, goal_name, target_amount, current_amount, target_date, category)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, goal_name, target_amount, current_amount, target_date, category))
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id


def update_savings_goal_progress(goal_id: int, user_id: int, add_amount: float) -> bool:
    """Deposits funds into a savings goal."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE savings_goals 
    SET current_amount = current_amount + ?,
        status = CASE WHEN (current_amount + ?) >= target_amount THEN 'REACHED' ELSE status END
    WHERE id = ? AND user_id = ?
    """, (add_amount, add_amount, goal_id, user_id))
    updated = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return updated


# =====================================================================
# NOTIFICATION SERVICES
# =====================================================================

def get_user_notifications(user_id: int, limit: int = 30) -> List[Dict[str, Any]]:
    """Fetches user notifications."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM notifications 
    WHERE user_id = ? 
    ORDER BY is_read ASC, id DESC LIMIT ?
    """, (user_id, limit))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


def mark_notification_read(notif_id: int, user_id: int) -> bool:
    """Marks a single notification as read."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE notifications SET is_read = 1 WHERE id = ? AND user_id = ?", (notif_id, user_id))
    updated = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return updated


def mark_all_notifications_read(user_id: int) -> bool:
    """Marks all user notifications as read."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE notifications SET is_read = 1 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
    return True


# =====================================================================
# FINANCIAL ANALYTICS & INSIGHTS ENGINE
# =====================================================================

def get_financial_analytics(user_id: int, role: str = "individual") -> Dict[str, Any]:
    """Computes comprehensive financial analytics from actual database records."""
    conn = get_db_connection()
    cursor = conn.cursor()

    uid_clause = "WHERE 1=1" if role == "admin_reviewer" else f"WHERE user_id = {user_id}"

    # 1. Total Inflow / Income
    cursor.execute(f"SELECT COALESCE(SUM(amount), 0.0) FROM transactions {uid_clause} AND txn_type = 'INCOME'")
    total_income = cursor.fetchone()[0]

    # 2. Total Outflow / Expenses
    cursor.execute(f"SELECT COALESCE(SUM(amount), 0.0) FROM transactions {uid_clause} AND txn_type = 'EXPENSE'")
    total_expenses = cursor.fetchone()[0]

    # 3. Net Savings / Cash Flow
    net_savings = total_income - total_expenses
    savings_rate = round((net_savings / total_income * 100.0), 1) if total_income > 0 else 0.0

    # 4. Category-wise Expenditure Breakdown
    cursor.execute(f"""
    SELECT category, COALESCE(SUM(amount), 0.0) as total_spent, COUNT(*) as txn_count
    FROM transactions 
    {uid_clause} AND txn_type = 'EXPENSE'
    GROUP BY category 
    ORDER BY total_spent DESC
    """)
    category_breakdown = [dict(r) for r in cursor.fetchall()]

    # 5. Monthly Cash Flow Trends (Last 6 Months)
    cursor.execute(f"""
    SELECT 
        strftime('%Y-%m', created_at) as month_key,
        COALESCE(SUM(CASE WHEN txn_type = 'INCOME' THEN amount ELSE 0 END), 0.0) as income,
        COALESCE(SUM(CASE WHEN txn_type = 'EXPENSE' THEN amount ELSE 0 END), 0.0) as expense
    FROM transactions
    {uid_clause}
    GROUP BY month_key
    ORDER BY month_key ASC
    LIMIT 6
    """)
    monthly_trends = [dict(r) for r in cursor.fetchall()]

    # 6. Flagged & High Risk Statistics
    cursor.execute(f"SELECT COUNT(*) FROM transactions {uid_clause} AND is_flagged = 1")
    flagged_count = cursor.fetchone()[0]

    cursor.execute(f"SELECT COUNT(*) FROM transactions {uid_clause}")
    total_txns = cursor.fetchone()[0]

    conn.close()

    return {
        "total_income": round(total_income, 2),
        "total_expenses": round(total_expenses, 2),
        "net_savings": round(net_savings, 2),
        "savings_rate": savings_rate,
        "total_transactions": total_txns,
        "flagged_transactions": flagged_count,
        "fraud_rate": round((flagged_count / total_txns * 100.0), 1) if total_txns > 0 else 0.0,
        "category_breakdown": category_breakdown,
        "monthly_trends": monthly_trends
    }


# =====================================================================
# ADMIN OPERATIONS & SYSTEM STATS
# =====================================================================

def get_admin_system_stats() -> Dict[str, Any]:
    """Retrieves full platform statistics for the Admin / Reviewer Dashboard."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM transactions")
    total_transactions = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(amount), 0.0) FROM transactions")
    total_volume = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM transactions WHERE is_flagged = 1")
    flagged_transactions = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM transactions WHERE review_status = 'Pending Review'")
    pending_reviews = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scan_logs")
    total_scans = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scan_logs WHERE risk_level IN ('HIGH_RISK', 'CRITICAL')")
    threats_blocked = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM fraud_reports")
    reports_filed = cursor.fetchone()[0]

    conn.close()

    return {
        "total_users": total_users,
        "total_transactions": total_transactions,
        "total_volume": round(total_volume, 2),
        "flagged_transactions": flagged_transactions,
        "pending_reviews": pending_reviews,
        "total_scans": total_scans,
        "threats_blocked": threats_blocked,
        "reports_filed": reports_filed,
        "platform_safety_score": 98.4
    }


def get_all_users_list() -> List[Dict[str, Any]]:
    """Returns all registered users for administration."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT u.id, u.full_name, u.email, u.phone, u.role, u.business_name, 
           u.wallet_balance, u.status, u.created_at,
           COUNT(t.id) as transaction_count
    FROM users u
    LEFT JOIN transactions t ON u.id = t.user_id
    GROUP BY u.id
    ORDER BY u.id ASC
    """)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows


# =====================================================================
# PRESERVED ORIGINAL SCAN LOG & ACADEMY HELPERS
# =====================================================================

def log_scan_event(scan_type: str, input_preview: str, risk_score: float, risk_level: str, explanations: Any) -> int:
    """Records an anonymized scan result into database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    clean_preview = (input_preview[:120] + "...") if len(input_preview) > 120 else input_preview
    exp_json = json.dumps(explanations) if not isinstance(explanations, str) else explanations

    cursor.execute("""
    INSERT INTO scan_logs (scan_type, input_preview, risk_score, risk_level, explanations)
    VALUES (?, ?, ?, ?, ?)
    """, (scan_type, clean_preview, risk_score, risk_level, exp_json))
    
    inserted_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return inserted_id


def get_recent_scans(limit: int = 10) -> List[Dict[str, Any]]:
    """Retrieves recent scan events."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, scan_type, input_preview, risk_score, risk_level, created_at 
    FROM scan_logs ORDER BY id DESC LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_dashboard_metrics() -> Dict[str, Any]:
    """Computes real-time statistics for the dashboard."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM scan_logs")
    total_scans = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scan_logs WHERE risk_level IN ('HIGH_RISK', 'CRITICAL')")
    threats_blocked = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM fraud_reports")
    reports_filed = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT module_id) FROM academy_progress WHERE completed = 1")
    academy_completed = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM transactions WHERE is_flagged = 1")
    flagged_txns = cursor.fetchone()[0]

    conn.close()
    return {
        "total_scans": total_scans,
        "threats_blocked": threats_blocked,
        "reports_filed": reports_filed,
        "academy_completed": academy_completed,
        "flagged_transactions": flagged_txns,
        "safety_index": round(100.0 - (min(50, threats_blocked + flagged_txns) * 0.8), 1)
    }


def save_fraud_report(report_data: Dict[str, Any]) -> str:
    """Creates a new Cybercrime incident report and returns unique reference code."""
    import random
    report_num = f"NEXA-CR-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO fraud_reports (report_number, fraud_type, suspected_entity, financial_loss, description)
    VALUES (?, ?, ?, ?, ?)
    """, (
        report_num,
        report_data.get("fraud_type", "OTHER"),
        report_data.get("suspected_entity", "Unknown"),
        float(report_data.get("financial_loss", 0.0)),
        report_data.get("description", "")
    ))
    conn.commit()
    conn.close()
    return report_num


def record_academy_progress(module_id: int, score: int) -> bool:
    """Updates quiz score for an educational module."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO academy_progress (user_id, module_id, score, completed)
    VALUES (1, ?, ?, 1)
    ON CONFLICT(user_id, module_id) DO UPDATE SET score = MAX(score, excluded.score), completed = 1
    """, (module_id, score))
    conn.commit()
    conn.close()
    return True
