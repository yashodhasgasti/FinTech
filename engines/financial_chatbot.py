"""
NEXAPAY AI Financial Assistant & Conversational Intelligence Engine
Provides context-aware, privacy-preserving guidance on:
- Personalized budget utilization & overspending alerts (using user's real DB records)
- Smart savings strategies & the 50/30/20 budgeting rule
- Payment security, UPI PIN safeguards, and National Cybercrime Helpline 1930 procedures
- Small business and retail shopkeeper cash-flow tips
"""

from typing import Dict, Any, List
import re


class FinancialChatbotEngine:
    """
    Intelligent FinTech Assistant powered by domain knowledge and real-time database context.
    """

    @classmethod
    def process_query(
        cls, 
        query: str, 
        user_profile: Dict[str, Any], 
        financial_summary: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Parses user intent and crafts a contextual, educational, and actionable response.
        """
        q = query.strip().lower()
        role = user_profile.get("role", "individual")
        user_name = user_profile.get("full_name", "User").split()[0]
        wallet_balance = float(user_profile.get("wallet_balance", 0.0))
        
        income = float(financial_summary.get("total_income", 0.0))
        expenses = float(financial_summary.get("total_expenses", 0.0))
        net_savings = float(financial_summary.get("net_savings", 0.0))
        flagged_count = int(financial_summary.get("flagged_transactions", 0))
        category_breakdown = financial_summary.get("category_breakdown", [])

        top_cat = category_breakdown[0]["category"] if category_breakdown else "General Expenses"
        top_cat_amt = category_breakdown[0]["total_spent"] if category_breakdown else 0.0

        # INTENT 1: Current Spending / Expense Inquiries
        if any(w in q for w in ["spend", "expense", "spent", "kharcha", "how much did i spend"]):
            reply = (
                f"Hello {user_name}! According to your live NexaPay financial records:\n\n"
                f"• **Total Recorded Outflow:** ₹{expenses:,.2f}\n"
                f"• **Total Recorded Inflow:** ₹{income:,.2f}\n"
                f"• **Top Spending Category:** {top_cat} (₹{top_cat_amt:,.2f})\n"
                f"• **Current Available Balance:** ₹{wallet_balance:,.2f}\n\n"
            )
            if expenses > income and income > 0:
                reply += "⚠️ *Alert:* Your outflows currently exceed your recorded inflows. I recommend reviewing non-essential discretionary items."
            else:
                reply += "💡 *Tip:* You are maintaining a positive net cash flow! Consider moving 20% of your remaining surplus into your Emergency Fund savings goal."
            return {"answer": reply, "topic": "EXPENSES"}

        # INTENT 2: Budgeting & Overspending
        if any(w in q for w in ["budget", "overspend", "saving rule", "50/30/20", "limit"]):
            reply = (
                f"Here is a smart budgeting strategy tailored for your **{role.replace('_', ' ').title()}** profile:\n\n"
                f"1. **The 50/30/20 Guideline:**\n"
                f"   - **50% Needs:** Housing, utilities, food essentials, and supplier costs.\n"
                f"   - **30% Discretionary:** Dining, leisure, gadgets, and lifestyle.\n"
                f"   - **20% Savings & Debt Cushion:** Emergency reserve and liquid savings.\n\n"
                f"2. **Your Current NexaPay Status:**\n"
                f"   - Your highest expenditure is currently in **{top_cat}**.\n"
                f"   - To prevent overspending, set an alert threshold of 80% under the **Smart Budget Planner** tab so you receive prompt alerts before exceeding your allocation."
            )
            return {"answer": reply, "topic": "BUDGET"}

        # INTENT 3: Fraud Prevention & Payment Security
        if any(w in q for w in ["fraud", "scam", "upi pin", "phishing", "fake link", "1930", "safety", "secure", "stolen", "hack"]):
            reply = (
                f"🛡️ **NexaPay Critical Financial Safety Protocol:**\n\n"
                f"1. **The Golden Rule of UPI:**\n"
                f"   - **You NEVER enter your UPI PIN to RECEIVE money.**\n"
                f"   - Any person asking you to scan a QR code or enter your PIN to claim cashback, a lottery, or a refund is attempting fraud.\n\n"
                f"2. **Immediate Action if Targeted:**\n"
                f"   - Dial National Cybercrime Helpline **1930** immediately within the golden hour.\n"
                f"   - Generate a formal incident dossier in the **Incident Dossier** tab of NexaPay to register with **cybercrime.gov.in**.\n"
                f"   - Block your UPI VPA and contact your banking institution.\n\n"
                f"3. **Active Defense:** NexaPay's AI Shield has already flagged {flagged_count} suspicious transaction(s) for compliance review on this account."
            )
            return {"answer": reply, "topic": "SECURITY"}

        # INTENT 4: Shop Owner & Small Business Specific Cash Flow
        if any(w in q for w in ["shop", "business", "store", "counter sales", "merchant", "customer", "qr scan", "inventory"]):
            reply = (
                f"📊 **Financial Strategies for Merchants & Business Users:**\n\n"
                f"• **Soundbox & SMS Verification:** Always confirm customer payment alerts via soundbox audio or official bank SMS—never trust screenshots presented by the customer.\n"
                f"• **Working Capital Runway:** NexaPay calculates your active cash runway. Maintain at least 45 to 60 days of operating expenses in reserve for inventory restock.\n"
                f"• **Counter-Payment Anomaly Shield:** If a customer initiates a sudden refund request citing a duplicate payment, do not transfer funds immediately. Direct them through the formal bank dispute channel."
            )
            return {"answer": reply, "topic": "BUSINESS"}

        # INTENT 5: Savings Goals & Wealth Guidance
        if any(w in q for w in ["save", "saving", "invest", "target", "emergency fund", "wealth"]):
            reply = (
                f"💰 **Maximizing Your Savings with NexaPay:**\n\n"
                f"• **Current Net Surplus:** ₹{net_savings:,.2f}\n"
                f"• **Target Milestone:** Establish an emergency fund equal to 3-6 months of essential expenses before investing in high-volatility assets.\n"
                f"• **Micro-Savings Technique:** Round up routine expenses to the nearest ₹100 and deposit the spare change directly into your active Savings Goals.\n"
                f"• Visit the **Smart Budget Planner** tab to create dedicated goals with milestone tracking."
            )
            return {"answer": reply, "topic": "SAVINGS"}

        # DEFAULT / GENERAL FINANCIAL LITERACY
        reply = (
            f"Hello {user_name}! I am your NexaPay AI Financial Assistant.\n\n"
            f"I can assist you with:\n"
            f"• Tracking and explaining your current income, expenses, and cash flow\n"
            f"• Creating category budgets and overspending prevention rules\n"
            f"• Explaining AI fraud alerts and how to avoid UPI payment traps\n"
            f"• Cybercrime reporting via **1930** and filing formal incident dossiers\n"
            f"• Cash-flow advice for shopkeepers, retail merchants, and businesses\n\n"
            f"What financial topic or question would you like to explore today?"
        )
        return {"answer": reply, "topic": "GENERAL"}
