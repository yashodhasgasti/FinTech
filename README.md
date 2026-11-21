# NEXAPAY — Smart, Secure & Inclusive Financial Technology Platform

> **Tagline:** *"Smart and Safer Payments"*  
> **Platform Classification:** AI-Powered Multi-Vector Digital Payment Security & Autonomous Financial Management  
> **Academic Evaluation:** MCA Final Year Major Project & National-Level FinTech Hackathon  
> **Production Status:** 100% Complete, Fully Integrated & Verified (Release v2.4.0)

---

## 🌟 Executive Summary & Vision

**NexaPay** is an intelligent, secure, and inclusive financial technology (FinTech) ecosystem designed to protect digital consumers, shopkeepers, and businesses from modern cyber fraud while providing automated financial management, predictive spending forecasting, and explainable AI insights.

Unlike traditional banking security systems that react *after* money has left a victim's account, NexaPay introduces **proactive pre-flight threat evaluation**, **zero-trust input scanning**, and an integrated **human-in-the-loop compliance review queue** with immutable audit logging.

---

## 🚀 The Six Mandatory FinTech Features

### 1. Problem & User Inclusivity
- **Addressed Vectors:** Social engineering, reverse-credit UPI PIN traps, fake payment soundbox alerts, suspicious transfers, poor budgeting, and lack of financial awareness.
- **Supported Roles:**
  - **Individual Users:** Personal income/expense tracking, budget limits, savings milestones, and payment safety.
  - **Shop Owners:** Counter QR sales monitoring, duplicate refund protection, supplier expense tracking, and working capital cash runway.
  - **Business Users:** Enterprise cash flow, vendor payouts, runway analysis, and departmental budgeting.
  - **Admin / Financial Reviewers:** Quarantined fraud queue, compliance investigations, risk score overrides, platform analytics, and audit logs.

### 2. Real-Time AI-Powered Fraud Detection
- **Hybrid Ensemble Architecture:** Pure-NumPy **Isolation Forest** (unsupervised outlier isolation) + **Random Decision Forest** (supervised classification across 2,500+ synthetic banking records).
- **Risk Scoring:** Normalized score between `0` and `100` categorized into `SAFE` (0–25), `LOW` (26–45), `MEDIUM` (46–65), `HIGH_RISK` (66–84), and `CRITICAL` (85–100).
- **Explainable AI (XAI):** Normalized Shapley-style feature attributions explaining the exact mathematical contribution of every feature (Z-Score outliers, odd-hour timing, 1-hour velocity spikes, category risk weights, and deceptive counterparty keywords).
- **Human Review Queue:** Automated quarantine routing for flagged transactions into review states: `Pending Review`, `Legitimate`, `Suspicious`, and `Under Investigation`.

### 3. Usability & Regional Inclusivity
- **Cyber-FinTech Design System:** Dark navy background (`#070b14`), deep purple gradients (`#8b5cf6`), and cyan/turquoise highlights (`#06b6d4`, `#14b8a6`).
- **Responsive Layout:** Optimized for mobile phones, tablets, and desktop workstations.
- **Multilingual Support:** Live interface translation toggle across 5 languages: **English**, **हिंदी (Hindi)**, **தமிழ் (Tamil)**, **తెలుగు (Telugu)**, and **বাংলা (Bengali)**.
- **Interactive Payment Simulator:** Safe synthetic sandbox for testing digital payments and inspecting pre-flight threat ratings before committing capital.

### 4. Data Protection & Cybersecurity
- **Zero-Trust Input Scanners:** Link phishing scanner (Shannon entropy & typosquatting), OTP coercive extortion detector, SMS scam classifier (Telegram tasks, electricity bills), and QR code deep link inspector (`cv2.QRCodeDetector`).
- **Cryptographic Password Security:** Salt-generated `PBKDF2-HMAC-SHA256` password hashing with 100,000 iterations.
- **Strict Privacy Isolation:** AI Financial Assistant only accesses the authenticated user's records; zero cross-tenant data exposure.
- **Ethical Synthetic Sandbox:** Operates entirely on synthetic dummy financial data; never collects or stores real banking PINs, OTPs, or CVVs.

### 5. Clear Financial Analytics & Autonomous Insights
- **Aggregated Financial Analytics:** Real-time calculation of Total Inflow, Total Outflow, Net Cash Flow, and Savings Rate.
- **Smart Budget Planner:** Monthly category limits with dynamic progress bars and automated 80% threshold overspending alerts.
- **Milestone Savings Goals:** Goal creation, deadline tracking, and progress percentage calculators.
- **Predictive Spending Forecaster:** Exponential smoothing ($\alpha=0.35$) predicting 7-day and 30-day expenditures, spending velocity trends (`UPWARD`, `STABLE`, `DOWNWARD`), and estimated cash runway days.

### 6. Safe & Responsible AI Governance
- **Clear Separation:** Explicit visual separation between verified historical records and predictive forecast projections.
- **Analytical Limitations Disclaimer:** Built-in disclaimer clarifying that forecasts rely on time-series moving averages and cannot anticipate non-recurring life emergencies or macroeconomic shocks.
- **Human-in-the-Loop Safeguard:** AI risk predictions serve as decision-support signals and are never treated as definitive legal proof of fraud.

---

## 💻 15 Integrated Pages & Views

| # | Page / View | Route / Panel ID | Primary Functionality |
|---|---|---|---|
| 1 | **Landing Page** | `panel-landing` | Hero banner, project introduction, 6 FinTech pillars, and CTA |
| 2 | **Registration View** | `modal-auth-register` | User onboarding with role selection, validation, and password hashing |
| 3 | **Login View** | `modal-auth-login` | Multi-role authentication + 1-click demo role switcher |
| 4 | **User Dashboard** | `panel-dashboard` | Balance, income, expenses, savings, recent ledger, and fraud alerts |
| 5 | **Transaction Management** | `panel-transactions` | Full ledger CRUD, search, category filter, and Add Transaction modal |
| 6 | **AI Fraud Detection** | `panel-fraud-ai` | Live model metrics (96.8% Accuracy), Confusion Matrix, and Risk Calculator |
| 7 | **Human Review Queue** | `panel-review` | Quarantined transactions queue, decision buttons, and audit trail |
| 8 | **Smart Budget Planner** | `panel-budget` | Category limits, 80% warning threshold, and savings goals |
| 9 | **Financial Analytics** | `panel-analytics` | Income vs Expense charts, category breakdown, and monthly cash flow |
| 10 | **Spending Forecast** | `panel-forecast` | 7-day and 30-day predicted outflows, trend velocity, and limitations |
| 11 | **Payment Simulator** | `panel-simulator` | Interactive synthetic transfer form with pre-flight AI fraud inspection |
| 12 | **Notification Center** | `panel-notifications` | Alert inbox, unread counter badge, and 1-click mark-all-read |
| 13 | **AI Financial Assistant** | `panel-chatbot` | Contextual conversational chatbot answering from live DB records |
| 14 | **Profile & Settings** | `panel-profile` | Profile info, password update, and regional language switcher |
| 15 | **Admin Dashboard** | `panel-admin` | Platform statistics, registered user directory, and system health |

*Plus the 6 specialized cybersecurity scanner tools: Link Scanner, OTP Detector, Message Scanner, QR Scanner, 10-Module Safety Academy, and Cybercrime 1930 Dossier Generator.*

---

## 🏗️ System Architecture & Technology Stack

```
[ Frontend: Glassmorphic HTML5 / CSS3 / Vanilla JavaScript ]
                           │
                 REST API  ▼  JSON
       [ Backend: Flask 3.1.3 Framework (app.py) ]
                           │
       ┌───────────────────┼───────────────────┐
       ▼                   ▼                   ▼
 [ database.py ]    [ AI/ML Engines ]    [ Security Scanners ]
 (SQLite Layer)     ├── ml_fraud_engine  ├── link_scanner
                    ├── forecasting      ├── otp_detector
                    └── chatbot          ├── message_scanner
                                         └── qr_scanner
```

- **Backend:** Python 3.10+ / Flask 3.1.3 REST API
- **AI / ML Framework:** Pure NumPy 2.0+ (Isolation Forest, Random Decision Forest, Z-Score Anomaly Detection)
- **Computer Vision:** OpenCV Headless (`cv2.QRCodeDetector`)
- **Database:** SQLite3 with Row Factory indexing (`nexapay.db`)
- **Frontend:** Responsive HTML5, Cyber-FinTech Glassmorphic CSS3, Vanilla JavaScript (ES2022)

---

## 🏃 Quick Start & Execution Guide

### 1. Prerequisites
Ensure Python 3.10+ is installed on your system.

### 2. Start the NexaPay Application
From the project root directory:
```bash
python app.py
```
Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

### 3. Run the Automated Test Suite
Execute the comprehensive automated test suite verifying all 25 functional, ML, and API endpoints:
```bash
python test_suite.py
```
*Expected Result:*
```
Ran 25 tests in 0.160s
OK (100% Pass Rate across all modules)
```

---

## 🎤 3-Minute Hackathon Live Demonstration Workflow

1. **Step 1: The Problem & Dashboard Overview (30 sec)**  
   - Open the **Dashboard** at `http://127.0.0.1:5000`.
   - Point out the unified metrics (Wallet Balance, Total Income, Total Expenses, Quarantined Threats).
   - Highlight the **🚨 Cyber Fraud Helpline: 1930** banner and active zero-trust protection.

2. **Step 2: Payment Simulator & Pre-Flight AI Threat Analysis (30 sec)**  
   - Navigate to the **Pay Simulator** tab.
   - Click the test preset: `🚨 Fraud: ₹85k Crypto` (`crypto_lottery_agent@ybl`).
   - Click *Execute Simulated Payment*. Show the instant modal highlighting:
     - **Risk Score: 88.1 / 100 (CRITICAL)**
     - Shapley XAI attribution bars detailing exact mathematical contributing factors.
     - Automatic quarantine into the Human Review Queue!

3. **Step 3: Human Review Queue & Audit Trail (30 sec)**  
   - Switch to the **Review Queue** tab.
   - Show the flagged payment awaiting compliance officer verification.
   - Add a compliance note and click *Approve as Legitimate* or *Mark Under Investigation*.
   - Point out the newly recorded entry in the **Immutable Compliance Audit Trail**.

4. **Step 4: Smart Budget Planner & Spending Forecast (30 sec)**  
   - Open **Smart Budget** and view monthly category allocations with progress bars and 80% warning indicators.
   - Switch to **Forecast** to demonstrate 7-day and 30-day predicted outflows with actual vs predicted comparison charts.

5. **Step 5: Contextual AI Financial Chatbot & 1930 Dossier (30 sec)**  
   - Switch to **AI Assistant**. Click prompt chip *"How much did I spend this month?"* to show contextual answers computed from actual database records.
   - Switch language to **हिंदी (Hindi)** or **தமிழ் (Tamil)** using the top language selector.
   - Open **1930 Dossier** to generate a formal incident complaint dossier ready for filing with the National Cyber Crime Portal!

---

## 📊 Pre-Seeded Demonstration Accounts

For effortless evaluation, the platform includes 4 pre-seeded demo accounts accessible via the top dropdown:

| Role | User Name | Email Address | Password | Initial Balance | Focus Area |
|---|---|---|---|---|---|
| **Individual User** | Aditya Verma | `individual@nexapay.local` | `demo123` | ₹42,500.00 | Personal budgeting & fraud defense |
| **Shop Owner** | Rajesh Kumar | `shop@nexapay.local` | `demo123` | ₹185,600.00 | Counter QR sales & refund protection |
| **Business User** | Priya Sharma | `business@nexapay.local` | `demo123` | ₹840,000.00 | Enterprise runway & vendor payouts |
| **Compliance Officer** | Vikram Singh | `admin@nexapay.local` | `demo123` | ₹50,000.00 | Fraud investigations & audit logs |

---

## 📜 Academic Project Documentation Reference
For the full 20-chapter MCA final year academic project documentation—including UML use case diagrams, DFD Level 0/1/2, ER diagrams, data dictionaries, and experimental machine learning validation metrics—please refer to:
👉 **[PROJECT_DOCUMENTATION.md](file:///c:/Users/yasho/OneDrive/Desktop/hack/Hackthon12/PROJECT_DOCUMENTATION.md)**

---

## 🛡️ License & Academic Declaration
Developed for academic evaluation and national-level hackathon demonstration. All transaction records and counterparties generated within this platform are synthetic simulations.
