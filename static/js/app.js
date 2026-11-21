/**
 * NEXAPAY — Interactive Client Engine
 * Connects all 15 FinTech pages, real-time AI/ML fraud detection, 
 * payment simulator, human review queue, budget tracking, spending forecasting,
 * conversational financial chatbot, and multi-vector security scanners.
 */

// Global Application State
const state = {
  currentUser: null,
  activeTab: "panel-dashboard",
  language: "en",
  unreadCount: 0,
  transactions: [],
  budgets: [],
  savingsGoals: [],
  reviewQueue: [],
  notifications: []
};

// Multi-Language Localization Dictionary (English, Hindi, Tamil, Telugu, Bengali)
const i18n = {
  en: {
    tagline: "Smart and Safer Payments",
    helpline: "Cyber Fraud Helpline: 1930",
    balance: "Wallet Balance",
    inflow: "Total Income",
    outflow: "Total Expenses",
    netSavings: "Net Cash Flow",
    quickPay: "Simulate Payment",
    addTxn: "Add Transaction",
    fraudAlerts: "AI Fraud Shield",
    reviewQueue: "Compliance Review Queue",
    budgetTitle: "Smart Budget Allocation",
    forecastTitle: "7-Day & 30-Day Spending Forecast"
  },
  hi: {
    tagline: "स्मार्ट और सुरक्षित डिजिटल भुगतान",
    helpline: "साइबर फ्रॉड हेल्पलाइन: 1930",
    balance: "उपलब्ध बैलेंस",
    inflow: "कुल आमदनी",
    outflow: "कुल खर्च",
    netSavings: "शुद्ध बचत",
    quickPay: "भुगतान सिम्युलेटर",
    addTxn: "नया लेनदेन जोड़ें",
    fraudAlerts: "एआई फ्रॉड शील्ड",
    reviewQueue: "समीक्षा कतार",
    budgetTitle: "स्मार्ट मासिक बजट",
    forecastTitle: "व्यय पूर्वानुमान"
  },
  ta: {
    tagline: "ஸ்மார்ட் மற்றும் பாதுகாப்பான கட்டணங்கள்",
    helpline: "சைபர் மோசடி உதவி எண்: 1930",
    balance: "மீதமுள்ள இருப்பு",
    inflow: "மொத்த வருமானம்",
    outflow: "மொத்த செலவுகள்",
    netSavings: "சேமிப்பு",
    quickPay: "பணம் செலுத்துதல் உருவகப்படுத்துதல்",
    addTxn: "பரிவர்த்தனை சேர்",
    fraudAlerts: "மோசடி கண்டறிதல்",
    reviewQueue: "மதிப்பாய்வு வரிசை",
    budgetTitle: "ஸ்மார்ட் பட்ஜெட்",
    forecastTitle: "செலவு கணிப்பு"
  },
  te: {
    tagline: "స్మార్ట్ మరియు సురక్షిత డిజిటల్ చెల్లింపులు",
    helpline: "సైబర్ ఫ్రాడ్ హెల్ప్‌లైన్: 1930",
    balance: "వాలెట్ బ్యాలెన్స్",
    inflow: "మొత్తం ఆదాయం",
    outflow: "మొత్తం ఖర్చులు",
    netSavings: "నికర పొదుపు",
    quickPay: "చెల్లింపు సిమ్యులేటర్",
    addTxn: "లావాదేవీని జోడించండి",
    fraudAlerts: "మోసం హెచ్చరికలు",
    reviewQueue: "సమీక్ష క్యూ",
    budgetTitle: "స్మార్ట్ బడ్జెట్",
    forecastTitle: "ఖర్చుల అంచనా"
  },
  bn: {
    tagline: "স্মার্ট ও নিরাপদ ডিজিটাল পেমেন্ট প্ল্যাটফর্ম",
    helpline: "সাইবার জালিয়াতি হেল্পলাইন: ১৯৩০",
    balance: "ওয়ালেট ব্যালেন্স",
    inflow: "মোট আয়",
    outflow: "মোট ব্যয়",
    netSavings: "সঞ্চয়",
    quickPay: "পেমেন্ট সিমুলেটর",
    addTxn: "নতুন লেনদেন যোগ করুন",
    fraudAlerts: "এআই ফ্রড অ্যালার্ট",
    reviewQueue: "রিভিউ কিউ",
    budgetTitle: "স্মার্ট বাজেট",
    forecastTitle: "ব্যয় পূর্বাভাস"
  }
};

document.addEventListener("DOMContentLoaded", async () => {
  setupTabs();
  setupLanguageSelector();
  setupModals();
  await loadCurrentUser();
  setupTransactionForm();
  setupPaymentSimulator();
  setupChatbot();
  setupCustomFraudCalculator();
  setupSampleButtons();
  setupScanForms();
  loadAcademyModules();
  setupIncidentReportForm();
  initAlertStream();
  loadFraudLiveStats();
  loadThresholds();
});

// =====================================================================
// AUTHENTICATION & DEMO SWITCHER
// =====================================================================

async function loadCurrentUser() {
  try {
    const res = await fetch("/api/auth/me");
    if (res.ok) {
      const data = await res.json();
      state.currentUser = data.user;
      renderUserPill(data.user);
      renderDashboardSummary(data.analytics_summary);
    }
  } catch (err) {
    console.error("Auth fetch error:", err);
  }
  // Load core data for active view
  loadTransactions();
  loadBudgets();
  loadSavingsGoals();
  loadNotifications();
  loadModelMetrics();
  loadReviewQueue();
}

function renderUserPill(user) {
  const nameEl = document.getElementById("nav-user-name");
  const roleEl = document.getElementById("nav-user-role");
  const avatarEl = document.getElementById("nav-user-avatar");
  const balanceEl = document.getElementById("nav-user-balance");

  if (nameEl) nameEl.textContent = user.full_name;
  if (avatarEl) avatarEl.textContent = user.full_name.charAt(0).toUpperCase();
  if (roleEl) {
    roleEl.textContent = user.role.replace("_", " ");
    roleEl.className = `user-role-tag role-${user.role}`;
  }
  if (balanceEl) {
    balanceEl.textContent = `₹${user.wallet_balance.toLocaleString('en-IN', { minimumFractionDigits: 2 })}`;
  }

  // Populate profile settings fields
  const pName = document.getElementById("profile-full-name");
  const pEmail = document.getElementById("profile-email");
  const pPhone = document.getElementById("profile-phone");
  const pBiz = document.getElementById("profile-business-name");
  const pRole = document.getElementById("profile-role-display");

  if (pName) pName.value = user.full_name;
  if (pEmail) pEmail.value = user.email;
  if (pPhone) pPhone.value = user.phone || "";
  if (pBiz) pBiz.value = user.business_name || "";
  if (pRole) pRole.textContent = user.role.replace("_", " ").toUpperCase();
}

async function switchDemoRole(role) {
  try {
    const res = await fetch("/api/auth/switch-demo-user", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ role })
    });
    const data = await res.json();
    if (data.success) {
      state.currentUser = data.user;
      await loadCurrentUser();
      showToast(`Switched to ${role.replace("_", " ").toUpperCase()} profile!`);
      // Return to dashboard
      switchTab("panel-dashboard");
    }
  } catch (err) {
    alert("Role switch failed: " + err.message);
  }
}

// =====================================================================
// TAB NAVIGATION SYSTEM
// =====================================================================

function setupTabs() {
  const tabs = document.querySelectorAll(".tab-btn");
  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      tabs.forEach(t => t.classList.remove("active"));
      tab.classList.add("active");

      const targetId = tab.dataset.target;
      state.activeTab = targetId;

      document.querySelectorAll(".view-panel").forEach(panel => {
        panel.classList.remove("active");
      });

      const targetPanel = document.getElementById(targetId);
      if (targetPanel) {
        targetPanel.classList.add("active");
        onTabActivated(targetId);
      }
    });
  });
}

function switchTab(tabId) {
  const btn = document.querySelector(`.tab-btn[data-target="${tabId}"]`);
  if (btn) btn.click();
}

function onTabActivated(tabId) {
  if (tabId === "panel-dashboard") {
    loadCurrentUser();
  } else if (tabId === "panel-transactions") {
    loadTransactions();
  } else if (tabId === "panel-review") {
    loadReviewQueue();
    loadReviewAuditLogs();
  } else if (tabId === "panel-budget") {
    loadBudgets();
    loadSavingsGoals();
  } else if (tabId === "panel-analytics") {
    loadAnalytics();
  } else if (tabId === "panel-forecast") {
    loadForecast();
  } else if (tabId === "panel-fraud-ai") {
    loadModelMetrics();
  } else if (tabId === "panel-admin") {
    loadAdminStats();
    loadAdminUsers();
  } else if (tabId === "panel-notifications") {
    loadNotifications();
  }
}

// =====================================================================
// DASHBOARD METRICS LOADER
// =====================================================================

function renderDashboardSummary(summary) {
  if (!summary) return;
  const balEl = document.getElementById("dash-balance");
  const inEl = document.getElementById("dash-income");
  const outEl = document.getElementById("dash-expense");
  const savEl = document.getElementById("dash-savings");
  const flagEl = document.getElementById("dash-flagged-count");

  if (balEl) balEl.textContent = `₹${Number(summary.wallet_balance).toLocaleString('en-IN', { minimumFractionDigits: 2 })}`;
  if (inEl) inEl.textContent = `₹${Number(summary.total_income).toLocaleString('en-IN', { minimumFractionDigits: 2 })}`;
  if (outEl) outEl.textContent = `₹${Number(summary.total_expenses).toLocaleString('en-IN', { minimumFractionDigits: 2 })}`;
  if (savEl) savEl.textContent = `₹${Number(summary.net_savings).toLocaleString('en-IN', { minimumFractionDigits: 2 })}`;
  if (flagEl) flagEl.textContent = summary.flagged_transactions;
}

// =====================================================================
// TRANSACTIONS MANAGEMENT
// =====================================================================

async function loadTransactions() {
  const searchInput = document.getElementById("txn-search");
  const catSelect = document.getElementById("txn-filter-category");
  const typeSelect = document.getElementById("txn-filter-type");
  const riskSelect = document.getElementById("txn-filter-risk");
  const statusSelect = document.getElementById("txn-filter-status");
  const dateFrom = document.getElementById("txn-filter-date-from");
  const dateTo = document.getElementById("txn-filter-date-to");

  const search = searchInput ? searchInput.value.trim() : "";
  const cat = catSelect ? catSelect.value : "";
  const type = typeSelect ? typeSelect.value : "";
  const risk = riskSelect ? riskSelect.value : "";
  const status = statusSelect ? statusSelect.value : "";
  const dFrom = dateFrom ? dateFrom.value : "";
  const dTo = dateTo ? dateTo.value : "";

  const url = `/api/transactions?search=${encodeURIComponent(search)}&category=${encodeURIComponent(cat)}&txn_type=${encodeURIComponent(type)}&risk_level=${encodeURIComponent(risk)}&review_status=${encodeURIComponent(status)}&date_from=${encodeURIComponent(dFrom)}&date_to=${encodeURIComponent(dTo)}&limit=100`;

  try {
    const res = await fetch(url);
    const data = await res.json();
    state.transactions = data.transactions || [];
    renderTransactionsTable(state.transactions);
    renderRecentDashboardTransactions(state.transactions.slice(0, 5));
  } catch (err) {
    console.error("Error loading transactions:", err);
  }
}

function renderTransactionsTable(transactions) {
  const tbody = document.getElementById("transactions-tbody");
  if (!tbody) return;

  if (transactions.length === 0) {
    tbody.innerHTML = `<tr><td colspan="9" style="text-align: center; color: var(--text-dim); padding: 30px;">No transactions recorded matching criteria.</td></tr>`;
    return;
  }

  tbody.innerHTML = transactions.map(t => {
    const isIncome = t.txn_type === "INCOME";
    const amountClass = isIncome ? "badge-income" : "badge-expense";
    const amountPrefix = isIncome ? "+₹" : "-₹";
    const riskBadgeClass = getRiskBadgeClass(t.risk_level);
    const statusBadgeClass = getStatusBadgeClass(t.review_status);

    return `
      <tr>
        <td><strong>${escapeHtml(t.transaction_ref)}</strong></td>
        <td style="color: var(--text-dim); font-size: 0.8rem;">${escapeHtml(t.created_at)}</td>
        <td><span class="badge ${amountClass}">${t.txn_type}</span></td>
        <td>${escapeHtml(t.category)}</td>
        <td><strong style="color: ${isIncome ? '#34d399' : '#f87171'}">${amountPrefix}${Number(t.amount).toLocaleString('en-IN', { minimumFractionDigits: 2 })}</strong></td>
        <td>${escapeHtml(t.receiver_info || t.sender_info || "N/A")}</td>
        <td><span class="badge ${riskBadgeClass}">${t.risk_score}/100</span></td>
        <td><span class="badge ${statusBadgeClass}">${escapeHtml(t.review_status)}</span></td>
        <td style="white-space: nowrap;">
          <button class="btn-secondary" style="font-size: 0.72rem; padding: 3px 8px; margin-right: 4px;" onclick="openTxnDetailsModal(${t.id})">🔬 Inspect</button>
          <button class="btn-danger" style="font-size: 0.72rem; padding: 3px 8px;" onclick="deleteTxn(${t.id})">Delete</button>
        </td>
      </tr>
    `;
  }).join("");
}

function renderRecentDashboardTransactions(transactions) {
  const container = document.getElementById("dash-recent-txns");
  if (!container) return;

  if (transactions.length === 0) {
    container.innerHTML = `<div style="color: var(--text-dim); padding: 16px; text-align: center;">No recent transactions.</div>`;
    return;
  }

  container.innerHTML = transactions.map(t => {
    const isIncome = t.txn_type === "INCOME";
    return `
      <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid var(--border-color);">
        <div>
          <div style="font-weight: 600; font-size: 0.9rem;">${escapeHtml(t.receiver_info || t.category)}</div>
          <div style="font-size: 0.75rem; color: var(--text-dim);">${escapeHtml(t.created_at)} • ${t.payment_method}</div>
        </div>
        <div style="text-align: right;">
          <div style="font-weight: 700; color: ${isIncome ? '#34d399' : '#f87171'}">
            ${isIncome ? '+' : '-'}₹${Number(t.amount).toLocaleString('en-IN', { minimumFractionDigits: 2 })}
          </div>
          <span class="badge ${getRiskBadgeClass(t.risk_level)}" style="font-size: 0.65rem; padding: 1px 6px;">Risk: ${t.risk_score}</span>
        </div>
      </div>
    `;
  }).join("");
}

async function deleteTxn(id) {
  if (!confirm("Are you sure you want to delete this transaction record?")) return;
  try {
    const res = await fetch(`/api/transactions/${id}`, { method: "DELETE" });
    const data = await res.json();
    if (data.success) {
      showToast("Transaction removed.");
      loadTransactions();
      loadCurrentUser();
    }
  } catch (err) {
    alert("Delete failed: " + err.message);
  }
}

function setupTransactionForm() {
  const form = document.getElementById("form-add-transaction");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const type = document.getElementById("txn-add-type").value;
    const cat = document.getElementById("txn-add-category").value;
    const amt = parseFloat(document.getElementById("txn-add-amount").value);
    const receiver = document.getElementById("txn-add-receiver").value.trim();
    const desc = document.getElementById("txn-add-desc").value.trim();
    const method = document.getElementById("txn-add-method").value;

    if (!amt || amt <= 0 || !receiver) {
      alert("Please enter a valid amount and recipient/source name.");
      return;
    }

    try {
      const res = await fetch("/api/transactions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          txn_type: type,
          category: cat,
          amount: amt,
          receiver_info: receiver,
          description: desc,
          payment_method: method
        })
      });
      const data = await res.json();
      if (data.success) {
        showToast(data.message);
        closeModal("modal-add-txn");
        form.reset();
        await loadCurrentUser();
        loadTransactions();
      } else {
        alert("Transaction error: " + (data.error || "Failed to add."));
      }
    } catch (err) {
      alert("Error: " + err.message);
    }
  });
}

// =====================================================================
// PAYMENT SIMULATOR & PRE-FLIGHT AI FRAUD ANALYSIS
// =====================================================================

function setupPaymentSimulator() {
  const form = document.getElementById("form-payment-simulator");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const amt = parseFloat(document.getElementById("sim-amount").value);
    const receiver = document.getElementById("sim-receiver-upi").value.trim();
    const cat = document.getElementById("sim-category").value;
    const desc = document.getElementById("sim-desc").value.trim();
    const method = document.getElementById("sim-method").value;

    if (!amt || amt <= 0 || !receiver) {
      alert("Please provide amount and receiver UPI ID.");
      return;
    }

    const submitBtn = document.getElementById("btn-sim-pay");
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.textContent = "AI Shield Analyzing Threat...";
    }

    try {
      const res = await fetch("/api/simulator/pay", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          amount: amt,
          receiver_upi: receiver,
          category: cat,
          description: desc,
          payment_method: method
        })
      });

      const data = await res.json();
      if (!res.ok || data.success === false) {
        showToast("⚠️ " + (data.error || "Payment execution declined."));
        return;
      }

      if (data.status === "REQUIRE_VERIFICATION" || data.verification_required) {
        openVerificationChallengeModal(data);
      } else {
        renderSimulatorResultModal(data);
      }

      await loadCurrentUser();
      loadTransactions();
      loadReviewQueue();
      loadFraudLiveStats();
    } catch (err) {
      alert("Simulation failed: " + err.message);
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = "Execute Simulated Payment";
      }
    }
  });
}

function openVerificationChallengeModal(data) {
  const content = document.getElementById("challenge-content");
  if (!content) return;

  const challenge = data.verification_challenge || {};
  const codeHint = challenge.code_hint || "123456";

  content.innerHTML = `
    <div style="text-align: center; margin-bottom: 16px;">
      <div style="font-size: 2.2rem; margin-bottom: 6px;">⚠️🔐</div>
      <h4 style="color: #f59e0b; font-weight: 800; font-size: 1.15rem;">Medium Fraud Risk Warning (Score: ${data.risk_score}/100)</h4>
      <p style="font-size: 0.82rem; color: var(--text-muted); margin-top: 4px;">
        Transfer of <strong>₹${Number(data.amount).toLocaleString('en-IN', {minimumFractionDigits: 2})}</strong> to <strong>${escapeHtml(data.receiver)}</strong> flagged for behavioral variance. Secondary confirmation required.
      </p>
    </div>

    <div style="background: rgba(245, 158, 11, 0.08); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 8px; padding: 12px; margin-bottom: 16px; font-size: 0.82rem;">
      <strong style="color: #f59e0b; display: block; margin-bottom: 4px;">Flagged Indicators:</strong>
      ${(data.attributions || []).map(a => `• <strong>${escapeHtml(a.factor)}:</strong> ${escapeHtml(a.detail)}`).join("<br>")}
    </div>

    <div style="background: rgba(0,0,0,0.3); border: 1px dashed var(--accent-cyan); border-radius: 8px; padding: 12px; text-align: center; margin-bottom: 16px;">
      <span style="font-size: 0.72rem; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.5px;">Step-Up Security Challenge Code:</span>
      <div style="font-size: 1.6rem; font-weight: 800; letter-spacing: 4px; color: #38bdf8; margin: 4px 0;">${escapeHtml(codeHint)}</div>
      <span style="font-size: 0.72rem; color: var(--text-muted);">(Issued to account holder for payment authorization)</span>
    </div>

    <form onsubmit="submitVerificationChallenge(event, ${data.transaction_id})">
      <div class="form-group">
        <label>Enter 6-Digit Confirmation PIN</label>
        <input type="text" id="challenge-pin-input" class="form-control" placeholder="Enter confirmation code" value="${escapeHtml(codeHint)}" required style="text-align: center; font-size: 1.25rem; letter-spacing: 3px; font-weight: 700;">
      </div>
      <div style="display: flex; justify-content: flex-end; gap: 10px; margin-top: 18px;">
        <button type="button" class="btn-secondary" onclick="closeModal('modal-verify-challenge')">Cancel Transfer</button>
        <button type="submit" class="btn-primary" id="btn-submit-challenge">Confirm & Authorize</button>
      </div>
    </form>
  `;

  openModal("modal-verify-challenge");
}

async function submitVerificationChallenge(e, txnId) {
  e.preventDefault();
  const pinInput = document.getElementById("challenge-pin-input");
  const pin = pinInput ? pinInput.value.trim() : "";
  const btn = document.getElementById("btn-submit-challenge");
  if (btn) btn.disabled = true;

  try {
    const res = await fetch("/api/simulator/verify-challenge", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ transaction_id: txnId, verification_code: pin })
    });
    const d = await res.json();
    if (d.success) {
      showToast("✅ " + d.message);
      closeModal("modal-verify-challenge");
      await loadCurrentUser();
      loadTransactions();
      loadReviewQueue();
      loadFraudLiveStats();
    } else {
      alert("Verification failed: " + (d.error || "Invalid confirmation code"));
    }
  } catch (err) {
    alert("Verification request failed: " + err.message);
  } finally {
    if (btn) btn.disabled = false;
  }
}

function renderSimulatorResultModal(result) {
  const modal = document.getElementById("modal-sim-result");
  const content = document.getElementById("sim-result-content");
  if (!modal || !content) return;

  const isQuarantine = result.status === "HELD_FOR_REVIEW";
  const statusColor = isQuarantine ? "var(--color-danger)" : "var(--color-safe)";
  const statusTitle = isQuarantine ? "🚨 TRANSACTION QUARANTINED (HIGH FRAUD RISK)" : "✅ PAYMENT SUCCESSFUL (SAFE & VERIFIED)";

  content.innerHTML = `
    <div style="text-align: center; margin-bottom: 20px;">
      <div style="font-size: 2.5rem; margin-bottom: 8px;">${isQuarantine ? '🛡️⚠️' : '💳✨'}</div>
      <h3 style="color: ${statusColor}; font-weight: 800; font-size: 1.25rem;">${statusTitle}</h3>
      <p style="color: var(--text-muted); font-size: 0.85rem; margin-top: 4px;">Ref ID: <strong>${escapeHtml(result.transaction_ref)}</strong></p>
    </div>

    <div style="background: rgba(0,0,0,0.25); border: 1px solid var(--border-color); border-radius: var(--radius-sm); padding: 14px; margin-bottom: 18px;">
      <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
        <span style="color: var(--text-dim); font-size: 0.82rem;">Amount Transferred</span>
        <strong style="color: #38bdf8; font-size: 1.1rem;">₹${Number(result.amount).toLocaleString('en-IN', { minimumFractionDigits: 2 })}</strong>
      </div>
      <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
        <span style="color: var(--text-dim); font-size: 0.82rem;">Counterparty</span>
        <strong>${escapeHtml(result.receiver)}</strong>
      </div>
      <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
        <span style="color: var(--text-dim); font-size: 0.82rem;">AI Risk Score</span>
        <span class="badge ${getRiskBadgeClass(result.risk_level)}">${result.risk_score} / 100 (${result.risk_level})</span>
      </div>
      <div style="display: flex; justify-content: space-between;">
        <span style="color: var(--text-dim); font-size: 0.82rem;">Compliance State</span>
        <span class="badge ${getStatusBadgeClass(result.review_status)}">${result.review_status}</span>
      </div>
    </div>

    <h4 style="font-size: 0.88rem; color: var(--text-main); margin-bottom: 8px;">Explainable AI Threat Attribution:</h4>
    <div style="margin-bottom: 16px;">
      ${(result.attributions || []).map(a => `
        <div class="attribution-item">
          <div class="attribution-header">
            <span>${escapeHtml(a.factor)}</span>
            <span style="color: var(--color-danger)">+${a.impact} pts</span>
          </div>
          <div class="attribution-bar-bg">
            <div class="attribution-bar-fill" style="width: ${Math.min(100, a.impact * 2)}%"></div>
          </div>
          <div class="attribution-desc">${escapeHtml(a.detail)}</div>
        </div>
      `).join("")}
    </div>

    <div style="background: rgba(6, 182, 212, 0.08); border-left: 3px solid var(--accent-cyan); padding: 10px 14px; border-radius: 4px; font-size: 0.82rem; margin-bottom: 20px;">
      <strong>Action Required:</strong> ${escapeHtml(result.recommendation)}
    </div>

    <div style="display: flex; justify-content: flex-end; gap: 10px;">
      ${isQuarantine ? `<button class="btn-primary" onclick="closeModal('modal-sim-result'); switchTab('panel-review');">View in Human Review Queue</button>` : ''}
      <button class="btn-secondary" onclick="closeModal('modal-sim-result');">Dismiss</button>
    </div>
  `;

  openModal("modal-sim-result");
}

// =====================================================================
// HUMAN REVIEW WORKFLOW & AUDIT TRAIL
// =====================================================================

async function loadReviewQueue() {
  try {
    const res = await fetch("/api/review/queue");
    const data = await res.json();
    state.reviewQueue = data.queue || [];
    renderReviewQueue(state.reviewQueue);

    const badge = document.getElementById("review-pending-badge");
    if (badge) badge.textContent = `${state.reviewQueue.length} Pending`;
  } catch (err) {
    console.error("Error loading review queue:", err);
  }
}

function renderReviewQueue(queue) {
  const container = document.getElementById("review-queue-container");
  if (!container) return;

  if (queue.length === 0) {
    container.innerHTML = `
      <div style="text-align: center; padding: 40px; color: var(--text-dim); background: rgba(0,0,0,0.15); border-radius: var(--radius-md);">
        <div style="font-size: 2.2rem; margin-bottom: 8px;">🛡️✅</div>
        <h4>Human Review Queue is Clear</h4>
        <p style="font-size: 0.85rem;">All transactions comply with safe risk parameters. No pending compliance alerts.</p>
      </div>
    `;
    return;
  }

  container.innerHTML = queue.map(t => {
    let aiFactors = [];
    try {
      aiFactors = typeof t.ai_reasons === "string" ? JSON.parse(t.ai_reasons || "[]") : (t.ai_reasons || []);
    } catch (e) {
      aiFactors = [];
    }

    return `
      <div class="review-item-card ${t.risk_level === 'CRITICAL' ? 'critical' : ''}">
        <div class="review-card-top">
          <div>
            <div style="font-size: 1rem; font-weight: 700; color: var(--text-main);">
              ${escapeHtml(t.transaction_ref)} • ${escapeHtml(t.category)}
            </div>
            <div style="font-size: 0.78rem; color: var(--text-dim); margin-top: 2px;">
              Initiated by: <strong>${escapeHtml(t.user_name || "User")}</strong> (${escapeHtml(t.user_role || "User")}) • ${escapeHtml(t.created_at)}
            </div>
          </div>
          <div>
            <span class="badge ${getRiskBadgeClass(t.risk_level)}">Risk: ${t.risk_score}/100 (${t.risk_level})</span>
            <span class="badge ${getStatusBadgeClass(t.review_status)}" style="margin-left: 6px;">${escapeHtml(t.review_status)}</span>
          </div>
        </div>

        <div class="review-details-grid">
          <div><span style="color: var(--text-dim)">Amount:</span><br><strong style="color: #f87171; font-size: 1rem;">₹${Number(t.amount).toLocaleString('en-IN', { minimumFractionDigits: 2 })}</strong></div>
          <div><span style="color: var(--text-dim)">Recipient:</span><br><strong>${escapeHtml(t.receiver_info || "Unknown")}</strong></div>
          <div><span style="color: var(--text-dim)">Payment Mode:</span><br><strong>${escapeHtml(t.payment_method)}</strong></div>
          <div><span style="color: var(--text-dim)">Flag Reason:</span><br><strong>${escapeHtml(t.description || "High Anomaly Score")}</strong></div>
        </div>

        <div style="display: flex; gap: 14px; font-size: 0.74rem; color: var(--text-dim); background: rgba(0,0,0,0.15); padding: 6px 10px; border-radius: 4px; margin-bottom: 8px;">
          <span>Rules: <strong style="color: #38bdf8;">${t.rule_risk_score !== undefined ? t.rule_risk_score : 'N/A'}</strong></span>
          <span>IsoForest: <strong style="color: #c084fc;">${t.ml_anomaly_score !== undefined ? t.ml_anomaly_score + '%' : 'N/A'}</strong></span>
          <span>RandomForest: <strong style="color: #fbbf24;">${t.ml_fraud_prob !== undefined ? t.ml_fraud_prob + '%' : 'N/A'}</strong></span>
          <span>Decision: <strong style="color: #f87171;">${escapeHtml(t.decision || t.review_status)}</strong></span>
          ${t.device_info ? `<span>Device: <strong style="color: var(--text-muted);">${escapeHtml(t.device_info.slice(0, 20))}...</strong></span>` : ''}
        </div>

        ${aiFactors.length > 0 ? `
          <div style="background: rgba(0,0,0,0.2); padding: 10px 14px; border-radius: var(--radius-sm); margin-bottom: 12px; font-size: 0.8rem;">
            <strong style="color: var(--accent-cyan); display: block; margin-bottom: 4px;">Explainable AI Analysis:</strong>
            ${aiFactors.map(f => `• <strong>${escapeHtml(f.factor || f.feature)}:</strong> ${escapeHtml(f.detail || f.desc)}`).join("<br>")}
          </div>
        ` : ''}

        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
          <input type="text" id="reviewer-note-${t.id}" placeholder="Enter compliance officer investigation notes..." class="form-control" style="flex: 1; min-width: 240px; padding: 7px 12px; font-size: 0.82rem;" value="${escapeHtml(t.reviewer_notes || '')}">
          
          <div class="review-actions" style="display: flex; gap: 6px; flex-wrap: wrap;">
            <button class="btn-secondary" style="font-size: 0.78rem; padding: 6px 10px;" onclick="openTxnDetailsModal(${t.id})">🔬 Inspect Features</button>
            <button class="btn-success" onclick="submitDecision(${t.id}, 'Legitimate')">Approve as Legitimate</button>
            <button class="btn-warning" onclick="submitDecision(${t.id}, 'Under Investigation')">Mark Investigation</button>
            <button class="btn-danger" onclick="submitDecision(${t.id}, 'Suspicious')">Confirm Suspicious</button>
            <button class="btn-danger" style="background: #991b1b;" onclick="submitDecision(${t.id}, 'Blocked')">🚫 Block</button>
          </div>
        </div>
      </div>
    `;
  }).join("");
}

async function submitDecision(txnId, decision) {
  const noteInput = document.getElementById(`reviewer-note-${txnId}`);
  const notes = noteInput ? noteInput.value.trim() : "";

  try {
    const res = await fetch("/api/review/decision", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        transaction_id: txnId,
        decision: decision,
        notes: notes || `Compliance officer marked as ${decision}.`
      })
    });
    const data = await res.json();
    if (data.success) {
      showToast(data.message);
      await loadCurrentUser();
      loadReviewQueue();
      loadReviewAuditLogs();
      loadTransactions();
    } else {
      alert("Decision error: " + data.error);
    }
  } catch (err) {
    alert("Error submitting decision: " + err.message);
  }
}

async function loadReviewAuditLogs() {
  const container = document.getElementById("review-audit-tbody");
  if (!container) return;

  try {
    const res = await fetch("/api/review/audit-logs");
    const data = await res.json();
    const logs = data.logs || [];

    if (logs.length === 0) {
      container.innerHTML = `<tr><td colspan="6" style="text-align: center; color: var(--text-dim); padding: 20px;">No audit events recorded yet.</td></tr>`;
      return;
    }

    container.innerHTML = logs.map(l => `
      <tr>
        <td style="color: var(--text-dim); font-size: 0.8rem;">${escapeHtml(l.created_at)}</td>
        <td><strong>${escapeHtml(l.transaction_ref)}</strong></td>
        <td>${escapeHtml(l.reviewer_name)}</td>
        <td><span class="badge ${getStatusBadgeClass(l.previous_status)}">${l.previous_status}</span></td>
        <td><span class="badge ${getStatusBadgeClass(l.new_status)}">${l.new_status}</span></td>
        <td style="font-size: 0.82rem; color: var(--text-muted);">${escapeHtml(l.reviewer_notes || 'N/A')}</td>
      </tr>
    `).join("");
  } catch (err) {
    console.error("Error loading audit logs:", err);
  }
}

// =====================================================================
// REAL-TIME FEATURE INSPECTION & EXPLAINABLE AI TELEMETRY MODAL
// =====================================================================

function openTxnDetailsModal(txnId) {
  let txn = state.transactions.find(t => t.id === txnId) || state.reviewQueue.find(t => t.id === txnId);
  if (!txn) {
    fetch(`/api/transactions?search=&limit=100`)
      .then(res => res.json())
      .then(data => {
        txn = (data.transactions || []).find(t => t.id === txnId);
        if (txn) renderTxnDetailsModal(txn);
        else alert("Transaction details not found.");
      })
      .catch(e => alert(e.message));
    return;
  }
  renderTxnDetailsModal(txn);
}

function renderTxnDetailsModal(txn) {
  const content = document.getElementById("txn-details-content");
  if (!content) return;

  let feats = {};
  try {
    feats = typeof txn.features_json === "string" ? JSON.parse(txn.features_json || "{}") : (txn.features_json || {});
  } catch (e) {
    feats = {};
  }

  let attributions = [];
  try {
    attributions = typeof txn.ai_reasons === "string" ? JSON.parse(txn.ai_reasons || "[]") : (txn.ai_reasons || []);
  } catch (e) {
    attributions = [];
  }

  const riskBadgeClass = getRiskBadgeClass(txn.risk_level);
  const statusBadgeClass = getStatusBadgeClass(txn.review_status);

  content.innerHTML = `
    <div style="background: rgba(0,0,0,0.25); border: 1px solid var(--border-color); border-radius: var(--radius-sm); padding: 14px; margin-bottom: 16px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <span style="font-size: 1.1rem; font-weight: 800; color: #38bdf8;">${escapeHtml(txn.transaction_ref)}</span>
        <div>
          <span class="badge ${riskBadgeClass}">Risk: ${txn.risk_score} / 100 (${txn.risk_level})</span>
          <span class="badge ${statusBadgeClass}" style="margin-left: 6px;">${escapeHtml(txn.review_status)}</span>
        </div>
      </div>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 8px; font-size: 0.82rem; color: var(--text-muted);">
        <div><strong>Amount:</strong> ₹${Number(txn.amount).toLocaleString('en-IN', {minimumFractionDigits: 2})}</div>
        <div><strong>Payee:</strong> ${escapeHtml(txn.receiver_info || 'N/A')}</div>
        <div><strong>Category:</strong> ${escapeHtml(txn.category)}</div>
        <div><strong>Payment Method:</strong> ${escapeHtml(txn.payment_method)}</div>
        <div><strong>Initiated:</strong> ${escapeHtml(txn.created_at)}</div>
        <div><strong>Decision:</strong> <span style="color: #38bdf8;">${escapeHtml(txn.decision || 'N/A')}</span></div>
        <div><strong>Device / UA:</strong> ${escapeHtml((txn.device_info || 'Web Client').slice(0, 30))}</div>
        <div><strong>Location:</strong> ${escapeHtml(txn.location || 'Terminal')}</div>
      </div>
    </div>

    <h4 style="font-size: 0.9rem; color: var(--text-main); margin-bottom: 8px; display: flex; align-items: center; gap: 6px;">
      <span>🧠</span> Multi-Model ML & Anomaly Scoring Breakdown:
    </h4>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 10px; margin-bottom: 16px;">
      <div class="feature-pill" style="border-left: 3px solid #38bdf8;">
        <div class="feature-pill-label">Deterministic Rules</div>
        <div class="feature-pill-val" style="color: #38bdf8;">${txn.rule_risk_score !== undefined ? txn.rule_risk_score : (feats.rule_score || 0)} pts</div>
        <div style="font-size: 0.7rem; color: var(--text-dim);">Weight: 40%</div>
      </div>
      <div class="feature-pill" style="border-left: 3px solid #c084fc;">
        <div class="feature-pill-label">Isolation Forest Anomaly</div>
        <div class="feature-pill-val" style="color: #c084fc;">${txn.ml_anomaly_score !== undefined ? txn.ml_anomaly_score + '%' : 'N/A'}</div>
        <div style="font-size: 0.7rem; color: var(--text-dim);">Weight: 30% (Pure NumPy)</div>
      </div>
      <div class="feature-pill" style="border-left: 3px solid #fbbf24;">
        <div class="feature-pill-label">Random Forest Fraud Prob</div>
        <div class="feature-pill-val" style="color: #fbbf24;">${txn.ml_fraud_prob !== undefined ? txn.ml_fraud_prob + '%' : 'N/A'}</div>
        <div style="font-size: 0.7rem; color: var(--text-dim);">Weight: 30% (Ensemble)</div>
      </div>
      <div class="feature-pill" style="border-left: 3px solid #f87171;">
        <div class="feature-pill-label">Combined Risk Score</div>
        <div class="feature-pill-val" style="color: #f87171;">${txn.risk_score} / 100</div>
        <div style="font-size: 0.7rem; color: var(--text-dim);">Calibrated Final Index</div>
      </div>
    </div>

    <h4 style="font-size: 0.9rem; color: var(--text-main); margin-bottom: 8px; display: flex; align-items: center; gap: 6px;">
      <span>📊</span> Real-Time Extracted Transaction Features (Database Ground Truth):
    </h4>
    <div class="feature-inspection-grid">
      <div class="feature-pill">
        <div class="feature-pill-label">Velocity (1 Minute)</div>
        <div class="feature-pill-val">${feats.tx_count_1m !== undefined ? feats.tx_count_1m : 0} txns</div>
      </div>
      <div class="feature-pill">
        <div class="feature-pill-label">Velocity (5 Minutes)</div>
        <div class="feature-pill-val">${feats.tx_count_5m !== undefined ? feats.tx_count_5m : 0} txns</div>
      </div>
      <div class="feature-pill">
        <div class="feature-pill-label">Velocity (10 Minutes)</div>
        <div class="feature-pill-val">${feats.tx_count_10m !== undefined ? feats.tx_count_10m : 0} txns</div>
      </div>
      <div class="feature-pill">
        <div class="feature-pill-label">Velocity (1 Hour)</div>
        <div class="feature-pill-val">${feats.tx_count_1h !== undefined ? feats.tx_count_1h : 0} txns</div>
      </div>
      <div class="feature-pill">
        <div class="feature-pill-label">User Avg Spend Baseline</div>
        <div class="feature-pill-val">₹${feats.avg_amount !== undefined ? Number(feats.avg_amount).toLocaleString('en-IN') : 'N/A'}</div>
      </div>
      <div class="feature-pill">
        <div class="feature-pill-label">Spending Deviation (Z-Score)</div>
        <div class="feature-pill-val">${feats.z_score !== undefined ? (feats.z_score > 0 ? '+' : '') + feats.z_score + 'σ' : '0.0σ'}</div>
      </div>
      <div class="feature-pill">
        <div class="feature-pill-label">Time Since Prior Txn</div>
        <div class="feature-pill-val">${feats.seconds_since_last_txn !== null && feats.seconds_since_last_txn !== undefined ? feats.seconds_since_last_txn + 's' : 'N/A (First Txn)'}</div>
      </div>
      <div class="feature-pill">
        <div class="feature-pill-label">First-Time Payee</div>
        <div class="feature-pill-val" style="color: ${feats.is_new_recipient ? '#f59e0b' : '#10b981'}">${feats.is_new_recipient ? 'Yes (New)' : 'No (Known)'}</div>
      </div>
      <div class="feature-pill">
        <div class="feature-pill-label">Frequently Used Payee</div>
        <div class="feature-pill-val" style="color: ${feats.is_frequent_recipient ? '#10b981' : 'var(--text-main)'}">${feats.is_frequent_recipient ? 'Yes (Trusted)' : 'No'}</div>
      </div>
      <div class="feature-pill">
        <div class="feature-pill-label">Odd Hours (1 AM - 5 AM)</div>
        <div class="feature-pill-val" style="color: ${feats.is_odd_hour ? '#ef4444' : '#10b981'}">${feats.is_odd_hour ? 'Flagged (Odd Hr)' : 'Normal (Daytime)'}</div>
      </div>
      <div class="feature-pill">
        <div class="feature-pill-label">Rapid Repeat Pattern</div>
        <div class="feature-pill-val" style="color: ${feats.rapid_repeat_detected ? '#ef4444' : '#10b981'}">${feats.rapid_repeat_detected ? '🚨 DETECTED' : 'None'}</div>
      </div>
      <div class="feature-pill">
        <div class="feature-pill-label">Unusual Device / Session</div>
        <div class="feature-pill-val" style="color: ${feats.unusual_device ? '#f59e0b' : '#10b981'}">${feats.unusual_device ? 'Flagged (Unseen)' : 'Recognized'}</div>
      </div>
    </div>

    <h4 style="font-size: 0.9rem; color: var(--text-main); margin: 16px 0 8px; display: flex; align-items: center; gap: 6px;">
      <span>🔍</span> Explainable AI Attributions:
    </h4>
    <div>
      ${attributions.length > 0 ? attributions.map(a => `
        <div class="attribution-item">
          <div class="attribution-header">
            <span><strong>${escapeHtml(a.factor || a.feature || 'Risk Factor')}</strong> (${escapeHtml(a.category || 'General')})</span>
            <span style="color: var(--color-danger)">+${a.impact || 0} pts</span>
          </div>
          <div class="attribution-bar-bg">
            <div class="attribution-bar-fill" style="width: ${Math.min(100, (a.impact || 5) * 2)}%"></div>
          </div>
          <div class="attribution-desc">${escapeHtml(a.detail || a.desc || '')}</div>
        </div>
      `).join("") : '<div style="color: var(--text-dim); font-size: 0.85rem;">Conforms to standard behavioral baseline. Zero threats triggered.</div>'}
    </div>

    <div style="display: flex; justify-content: flex-end; margin-top: 18px;">
      <button class="btn-secondary" onclick="closeModal('modal-txn-details')">Close Inspection</button>
    </div>
  `;

  openModal("modal-txn-details");
}

// =====================================================================
// REAL-TIME SERVER-SENT EVENTS (SSE) STREAM & ALERT DISPATCHER
// =====================================================================

function initAlertStream() {
  if (state.eventSource) {
    try { state.eventSource.close(); } catch (e) {}
  }

  try {
    state.eventSource = new EventSource("/api/stream/alerts");

    state.eventSource.onopen = () => {
      const dot = document.getElementById("sse-pulse-dot");
      const text = document.getElementById("sse-status-text");
      if (dot) dot.className = "live-pulse-dot online";
      if (text) {
        text.textContent = "Live Shield Active";
        text.style.color = "#10b981";
      }
    };

    state.eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        handleIncomingSSEEvent(data);
      } catch (err) {
        console.error("SSE parse error:", err);
      }
    };

    state.eventSource.onerror = () => {
      const dot = document.getElementById("sse-pulse-dot");
      const text = document.getElementById("sse-status-text");
      if (dot) dot.className = "live-pulse-dot";
      if (text) {
        text.textContent = "Reconnecting...";
        text.style.color = "#f59e0b";
      }
    };
  } catch (err) {
    console.error("Failed to initialize SSE EventSource:", err);
  }
}

function handleIncomingSSEEvent(data) {
  if (data.type === "CONNECTED") {
    return;
  }

  if (data.type === "FRAUD_ALERT") {
    // 1. Show live animated toast alert banner
    showLiveAlertToast(data);

    // 2. Increment notification bell counter
    state.unreadCount = (state.unreadCount || 0) + 1;
    const notifBadge = document.getElementById("nav-notif-count");
    if (notifBadge) {
      notifBadge.style.display = "flex";
      notifBadge.textContent = state.unreadCount;
    }

    // 3. Update dashboard counters and review queue
    loadFraudLiveStats();
    loadReviewQueue();
    loadTransactions();

    // 4. Append to Live Activity Stream
    appendLiveActivity({
      type: "ALERT",
      amount: data.amount,
      receiver: data.receiver,
      risk_score: data.risk_score,
      risk_level: data.risk_level,
      status: data.review_status || "Pending Review",
      timestamp: data.timestamp || "Just now"
    });
  } else if (data.type === "TRANSACTION_ACTIVITY" || data.type === "TRANSACTION_VERIFIED") {
    appendLiveActivity({
      type: "TXN",
      amount: data.amount,
      receiver: data.receiver,
      risk_score: data.risk_score || 10,
      risk_level: data.risk_level || "SAFE",
      status: data.status || "SUCCESSFUL",
      timestamp: data.timestamp || "Just now"
    });
    loadFraudLiveStats();
    loadTransactions();
  } else if (data.type === "REVIEW_DECISION") {
    showToast(`⚖️ Transaction review updated to '${data.new_status}' by ${data.reviewer_name || 'Compliance'}`);
    loadReviewQueue();
    loadReviewAuditLogs();
    loadFraudLiveStats();
    loadTransactions();
    loadCurrentUser();
  }
}

function showLiveAlertToast(alert) {
  const container = document.getElementById("live-alert-toast-container");
  if (!container) return;

  const isCritical = alert.risk_level === "CRITICAL" || alert.risk_score >= 80;
  const isMedium = alert.risk_level === "MEDIUM" || (alert.risk_score >= 30 && alert.risk_score < 70);
  const toastClass = isCritical ? "" : (isMedium ? "toast-medium" : "toast-safe");

  const toast = document.createElement("div");
  toast.className = `live-alert-toast ${toastClass}`;

  const topReason = (alert.reasons && alert.reasons.length > 0) ? (alert.reasons[0].factor || alert.reasons[0].detail) : "Suspicious transaction parameters flagged";

  toast.innerHTML = `
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px;">
      <div style="display: flex; align-items: center; gap: 8px;">
        <span class="live-pulse-dot"></span>
        <strong style="color: ${isCritical ? '#ef4444' : '#f59e0b'}; font-size: 0.95rem;">
          ${isCritical ? '🚨 CRITICAL FRAUD ALERT' : '⚠️ SUSPICIOUS TRANSACTION FLAGGED'}
        </strong>
      </div>
      <button style="background: transparent; border: none; color: var(--text-dim); cursor: pointer; font-size: 1rem;" onclick="this.closest('.live-alert-toast').remove()">✕</button>
    </div>
    <div style="font-size: 0.82rem; margin-bottom: 6px;">
      Payment of <strong style="color: #38bdf8;">₹${Number(alert.amount || 0).toLocaleString('en-IN', {minimumFractionDigits: 2})}</strong> to <strong>${escapeHtml(alert.receiver || 'Unknown')}</strong>
    </div>
    <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 8px;">
      ${escapeHtml(topReason)}
    </div>
    <div style="display: flex; justify-content: space-between; align-items: center;">
      <span class="badge ${getRiskBadgeClass(alert.risk_level)}" style="font-size: 0.7rem; padding: 2px 8px;">Risk Score: ${alert.risk_score}/100</span>
      <button class="btn-primary" style="font-size: 0.75rem; padding: 3px 10px;" onclick="switchTab('panel-review'); this.closest('.live-alert-toast').remove();">Investigate</button>
    </div>
  `;

  container.prepend(toast);

  // Auto-dismiss after 7 seconds
  setTimeout(() => {
    if (toast.parentNode) {
      toast.style.opacity = "0";
      toast.style.transform = "translateX(110%)";
      setTimeout(() => toast.remove(), 400);
    }
  }, 7000);
}

function appendLiveActivity(evt) {
  const container = document.getElementById("dash-live-activity-stream");
  if (!container) return;

  if (container.children.length === 1 && container.children[0].textContent.includes("Listening")) {
    container.innerHTML = "";
  }

  const isAlert = evt.type === "ALERT";
  const item = document.createElement("div");
  item.className = "live-activity-item";
  item.innerHTML = `
    <div>
      <div style="font-weight: 600; color: ${isAlert ? '#f87171' : 'var(--text-main)'};">
        ${isAlert ? '🚨' : '💳'} ₹${Number(evt.amount || 0).toLocaleString('en-IN', {minimumFractionDigits: 2})} → ${escapeHtml(evt.receiver || 'Merchant')}
      </div>
      <div style="font-size: 0.72rem; color: var(--text-dim);">${escapeHtml(evt.timestamp)} • Status: <strong>${escapeHtml(evt.status)}</strong></div>
    </div>
    <span class="badge ${getRiskBadgeClass(evt.risk_level)}" style="font-size: 0.68rem; padding: 2px 6px;">Risk: ${evt.risk_score}</span>
  `;

  container.prepend(item);

  while (container.children.length > 15) {
    container.removeChild(container.lastChild);
  }
}

// =====================================================================
// FRAUD TELEMETRY & CONFIGURABLE THRESHOLDS MANAGEMENT
// =====================================================================

async function loadFraudLiveStats() {
  try {
    const res = await fetch("/api/fraud/live-stats");
    if (!res.ok) return;
    const stats = await res.json();

    const evalEl = document.getElementById("dash-evaluated-count");
    const lowEl = document.getElementById("dash-low-risk-count");
    const medEl = document.getElementById("dash-medium-risk-count");
    const highEl = document.getElementById("dash-high-risk-count");
    const pendEl = document.getElementById("dash-pending-count");

    if (evalEl) evalEl.textContent = stats.total_evaluated || 0;
    if (lowEl) lowEl.textContent = stats.low_risk_count || 0;
    if (medEl) medEl.textContent = stats.medium_risk_count || 0;
    if (highEl) highEl.textContent = stats.high_risk_count || 0;
    if (pendEl) pendEl.textContent = stats.pending_reviews || 0;

    const total = Math.max(1, stats.total_evaluated || 1);
    const pctLow = Math.round(((stats.low_risk_count || 0) / total) * 100);
    const pctMed = Math.round(((stats.medium_risk_count || 0) / total) * 100);
    const pctHigh = Math.round(((stats.high_risk_count || 0) / total) * 100);

    const barLow = document.getElementById("bar-dist-low");
    const barMed = document.getElementById("bar-dist-med");
    const barHigh = document.getElementById("bar-dist-high");

    if (barLow) barLow.style.width = `${Math.max(5, pctLow)}%`;
    if (barMed) barMed.style.width = `${Math.max(3, pctMed)}%`;
    if (barHigh) barHigh.style.width = `${Math.max(3, pctHigh)}%`;

    const txtLow = document.getElementById("pct-dist-low");
    const txtMed = document.getElementById("pct-dist-med");
    const txtHigh = document.getElementById("pct-dist-high");

    if (txtLow) txtLow.textContent = `${pctLow}% (${stats.low_risk_count || 0})`;
    if (txtMed) txtMed.textContent = `${pctMed}% (${stats.medium_risk_count || 0})`;
    if (txtHigh) txtHigh.textContent = `${pctHigh}% (${stats.high_risk_count || 0})`;

    renderRecentFraudAlerts(stats.recent_alerts || []);
  } catch (err) {
    console.error("Error loading fraud live stats:", err);
  }
}

function renderRecentFraudAlerts(alerts) {
  const container = document.getElementById("dash-recent-fraud-alerts");
  if (!container) return;

  if (alerts.length === 0) {
    container.innerHTML = `<div style="text-align: center; color: var(--text-dim); padding: 14px; font-size: 0.82rem;">No suspicious transactions detected. Shield is active.</div>`;
    return;
  }

  container.innerHTML = alerts.slice(0, 4).map(a => `
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 10px; background: rgba(0,0,0,0.18); border-left: 3px solid #ef4444; border-radius: 4px; margin-bottom: 6px; font-size: 0.82rem;">
      <div>
        <div style="font-weight: 700; color: #f87171;">₹${Number(a.amount).toLocaleString('en-IN', {minimumFractionDigits: 2})} → ${escapeHtml(a.receiver_info || 'Unknown')}</div>
        <div style="font-size: 0.72rem; color: var(--text-dim);">${escapeHtml(a.created_at)} • ${escapeHtml(a.review_status)}</div>
      </div>
      <button class="btn-secondary" style="font-size: 0.7rem; padding: 2px 8px;" onclick="openTxnDetailsModal(${a.id})">Inspect</button>
    </div>
  `).join("");
}

async function loadThresholds() {
  try {
    const res = await fetch("/api/fraud/thresholds");
    if (!res.ok) return;
    const data = await res.json();
    state.thresholds = data.thresholds || {};

    const lowMax = state.thresholds.low_max || 29;
    const highMin = state.thresholds.high_min || 70;
    const autoBlock = state.thresholds.auto_block_high_risk || false;

    const inLow = document.getElementById("thresh-low-max");
    const inHigh = document.getElementById("thresh-high-min");
    const inBlock = document.getElementById("thresh-auto-block");

    if (inLow) inLow.value = lowMax;
    if (inHigh) inHigh.value = highMin;
    if (inBlock) inBlock.checked = autoBlock;

    const pLow = document.getElementById("policy-low-max");
    const pMed = document.getElementById("policy-med-range");
    const pHigh = document.getElementById("policy-high-min");

    if (pLow) pLow.textContent = `0 – ${lowMax} pts`;
    if (pMed) pMed.textContent = `${Number(lowMax) + 1} – ${Number(highMin) - 1} pts`;
    if (pHigh) pHigh.textContent = `${highMin} – 100 pts`;
  } catch (err) {
    console.error("Error loading thresholds:", err);
  }
}

async function handleThresholdsSubmit(e) {
  e.preventDefault();
  const lowMax = parseFloat(document.getElementById("thresh-low-max").value);
  const highMin = parseFloat(document.getElementById("thresh-high-min").value);
  const autoBlock = document.getElementById("thresh-auto-block").checked;

  if (lowMax >= highMin) {
    alert("Low risk threshold must be strictly less than high risk threshold.");
    return;
  }

  try {
    const res = await fetch("/api/fraud/thresholds", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ low_max: lowMax, high_min: highMin, auto_block_high_risk: autoBlock })
    });
    const data = await res.json();
    if (data.success) {
      showToast("✅ " + data.message);
      closeModal("modal-thresholds");
      loadThresholds();
      loadFraudLiveStats();
    } else {
      alert("Error saving policy: " + data.error);
    }
  } catch (err) {
    alert("Request failed: " + err.message);
  }
}

// =====================================================================
// SMART BUDGET PLANNER & SAVINGS GOALS
// =====================================================================

async function loadBudgets() {
  try {
    const res = await fetch("/api/budgets");
    const data = await res.json();
    state.budgets = data.budgets || [];
    renderBudgets(state.budgets);
  } catch (err) {
    console.error("Error loading budgets:", err);
  }
}

function renderBudgets(budgets) {
  const container = document.getElementById("budgets-list-container");
  if (!container) return;

  if (budgets.length === 0) {
    container.innerHTML = `<div style="color: var(--text-dim); padding: 20px; text-align: center;">No budget limits configured yet. Click "Set Category Budget" to add one!</div>`;
    return;
  }

  container.innerHTML = budgets.map(b => {
    let fillClass = "";
    if (b.is_exceeded) fillClass = "exceeded";
    else if (b.is_warning) fillClass = "warning";

    return `
      <div class="budget-progress-box card-panel" style="margin-bottom: 14px; padding: 16px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
          <div>
            <strong style="font-size: 0.95rem;">${escapeHtml(b.category)}</strong>
            <span style="font-size: 0.75rem; color: var(--text-dim); margin-left: 8px;">Threshold: ${b.alert_threshold}%</span>
          </div>
          <div style="text-align: right;">
            <strong style="color: ${b.is_exceeded ? '#ef4444' : '#38bdf8'}">₹${Number(b.spent_amount).toLocaleString('en-IN', { minimumFractionDigits: 2 })}</strong> / 
            <span style="color: var(--text-dim)">₹${Number(b.monthly_limit).toLocaleString('en-IN', { minimumFractionDigits: 2 })}</span>
            <button onclick="deleteBudget(${b.id})" style="background: transparent; border: none; color: var(--color-danger); cursor: pointer; margin-left: 10px; font-size: 0.9rem;" title="Delete Budget">🗑️</button>
          </div>
        </div>

        <div class="budget-bar-bg">
          <div class="budget-bar-fill ${fillClass}" style="width: ${Math.min(100, b.percentage)}%"></div>
        </div>

        <div style="display: flex; justify-content: space-between; font-size: 0.78rem; color: var(--text-dim);">
          <span>${b.percentage}% Utilized</span>
          <span>${b.is_exceeded ? '🚨 Overspent by ₹' + Math.abs(b.monthly_limit - b.spent_amount).toFixed(2) : 'Remaining: ₹' + b.remaining.toFixed(2)}</span>
        </div>
      </div>
    `;
  }).join("");
}

async function deleteBudget(id) {
  if (!confirm("Remove this budget target?")) return;
  try {
    const res = await fetch(`/api/budgets/${id}`, { method: "DELETE" });
    const data = await res.json();
    if (data.success) {
      showToast("Budget removed.");
      loadBudgets();
    }
  } catch (err) {
    alert("Delete failed: " + err.message);
  }
}

async function loadSavingsGoals() {
  try {
    const res = await fetch("/api/savings-goals");
    const data = await res.json();
    state.savingsGoals = data.goals || [];
    renderSavingsGoals(state.savingsGoals);
  } catch (err) {
    console.error("Error loading savings goals:", err);
  }
}

function renderSavingsGoals(goals) {
  const container = document.getElementById("savings-goals-container");
  if (!container) return;

  if (goals.length === 0) {
    container.innerHTML = `<div style="color: var(--text-dim); padding: 20px; text-align: center;">No active savings targets. Create your first goal to begin!</div>`;
    return;
  }

  container.innerHTML = goals.map(g => `
    <div class="card-panel" style="padding: 18px; margin-bottom: 14px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <div>
          <strong style="font-size: 1rem; color: #38bdf8;">${escapeHtml(g.goal_name)}</strong>
          <div style="font-size: 0.75rem; color: var(--text-dim);">Target Date: ${escapeHtml(g.target_date || 'Ongoing')} • ${escapeHtml(g.category)}</div>
        </div>
        <div>
          <span class="badge ${g.status === 'REACHED' ? 'badge-risk-safe' : 'badge-status-investigation'}">${g.status}</span>
        </div>
      </div>

      <div class="budget-bar-bg" style="height: 10px;">
        <div class="budget-bar-fill" style="width: ${Math.min(100, g.percentage)}%; background: linear-gradient(90deg, #10b981, #06b6d4);"></div>
      </div>

      <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.8rem; margin-top: 8px;">
        <span><strong>₹${Number(g.current_amount).toLocaleString('en-IN')}</strong> of ₹${Number(g.target_amount).toLocaleString('en-IN')} (${g.percentage}%)</span>
        <button class="btn-primary" style="padding: 4px 12px; font-size: 0.75rem;" onclick="promptDepositGoal(${g.id}, '${escapeHtml(g.goal_name)}')">+ Deposit</button>
      </div>
    </div>
  `).join("");
}

async function promptDepositGoal(goalId, name) {
  const amtStr = prompt(`Enter deposit amount for "${name}":`, "1000");
  if (!amtStr) return;
  const amt = parseFloat(amtStr);
  if (isNaN(amt) || amt <= 0) return alert("Please enter a valid amount.");

  try {
    const res = await fetch(`/api/savings-goals/${goalId}/deposit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ amount: amt })
    });
    const data = await res.json();
    if (data.success) {
      showToast("Deposit recorded!");
      loadSavingsGoals();
    }
  } catch (err) {
    alert("Deposit failed: " + err.message);
  }
}

// =====================================================================
// FINANCIAL ANALYTICS & SPENDING FORECAST
// =====================================================================

async function loadAnalytics() {
  try {
    const res = await fetch("/api/analytics/summary");
    const data = await res.json();

    const inEl = document.getElementById("analytics-inflow");
    const outEl = document.getElementById("analytics-outflow");
    const netEl = document.getElementById("analytics-net");
    const savRateEl = document.getElementById("analytics-rate");

    if (inEl) inEl.textContent = `₹${data.total_income.toLocaleString('en-IN')}`;
    if (outEl) outEl.textContent = `₹${data.total_expenses.toLocaleString('en-IN')}`;
    if (netEl) netEl.textContent = `₹${data.net_savings.toLocaleString('en-IN')}`;
    if (savRateEl) savRateEl.textContent = `${data.savings_rate}%`;

    renderCategoryDonut(data.category_breakdown);
    renderMonthlyTrendChart(data.monthly_trends);
  } catch (err) {
    console.error("Error loading analytics:", err);
  }
}

function renderCategoryDonut(breakdown) {
  const container = document.getElementById("analytics-category-bars");
  if (!container) return;

  if (!breakdown || breakdown.length === 0) {
    container.innerHTML = `<div style="color: var(--text-dim); padding: 20px; text-align: center;">No expenditure records found.</div>`;
    return;
  }

  const maxVal = Math.max(...breakdown.map(b => b.total_spent));

  container.innerHTML = breakdown.map(b => {
    const pct = maxVal > 0 ? (b.total_spent / maxVal) * 100 : 0;
    return `
      <div style="margin-bottom: 12px;">
        <div style="display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 4px;">
          <span>${escapeHtml(b.category)} (${b.txn_count} txns)</span>
          <strong style="color: #38bdf8;">₹${Number(b.total_spent).toLocaleString('en-IN', { minimumFractionDigits: 2 })}</strong>
        </div>
        <div class="budget-bar-bg" style="height: 8px;">
          <div class="budget-bar-fill" style="width: ${pct}%; background: linear-gradient(90deg, #6366f1, #06b6d4);"></div>
        </div>
      </div>
    `;
  }).join("");
}

function renderMonthlyTrendChart(trends) {
  const container = document.getElementById("analytics-trend-chart");
  if (!container) return;

  if (!trends || trends.length === 0) {
    container.innerHTML = `<div style="color: var(--text-dim); padding: 30px; text-align: center;">Accumulating monthly timeline records...</div>`;
    return;
  }

  const maxAmt = Math.max(...trends.map(t => Math.max(t.income, t.expense)), 1000);

  container.innerHTML = `
    <div style="display: flex; align-items: flex-end; justify-content: space-around; height: 180px; padding-top: 20px; border-bottom: 1px solid var(--border-color);">
      ${trends.map(t => {
        const inHeight = Math.max(8, (t.income / maxAmt) * 140);
        const outHeight = Math.max(8, (t.expense / maxAmt) * 140);
        return `
          <div style="text-align: center; width: 60px;">
            <div style="display: flex; justify-content: center; gap: 4px; align-items: flex-end; height: 140px;">
              <div style="width: 14px; height: ${inHeight}px; background: #10b981; border-radius: 3px 3px 0 0;" title="Income: ₹${t.income}"></div>
              <div style="width: 14px; height: ${outHeight}px; background: #ef4444; border-radius: 3px 3px 0 0;" title="Expense: ₹${t.expense}"></div>
            </div>
            <div style="font-size: 0.72rem; color: var(--text-dim); margin-top: 8px;">${escapeHtml(t.month_key)}</div>
          </div>
        `;
      }).join("")}
    </div>
    <div style="display: flex; justify-content: center; gap: 20px; margin-top: 10px; font-size: 0.78rem;">
      <span style="color: #10b981;">■ Inflows (Income)</span>
      <span style="color: #ef4444;">■ Outflows (Expenses)</span>
    </div>
  `;
}

async function loadForecast() {
  try {
    const res = await fetch("/api/forecast/predict");
    const data = await res.json();

    const wkEl = document.getElementById("forecast-weekly");
    const moEl = document.getElementById("forecast-monthly");
    const trendEl = document.getElementById("forecast-trend-tag");
    const runwayEl = document.getElementById("forecast-runway");
    const adviceEl = document.getElementById("forecast-advice");
    const disclaimerEl = document.getElementById("forecast-disclaimer");

    if (wkEl) wkEl.textContent = `₹${Number(data.predicted_weekly_expense).toLocaleString('en-IN', { minimumFractionDigits: 2 })}`;
    if (moEl) moEl.textContent = `₹${Number(data.predicted_monthly_expense).toLocaleString('en-IN', { minimumFractionDigits: 2 })}`;
    if (runwayEl) runwayEl.textContent = `${data.financial_runway_days} Days`;
    if (adviceEl) adviceEl.textContent = data.trend.advice;
    if (disclaimerEl) disclaimerEl.textContent = data.limitations_disclaimer;

    if (trendEl) {
      trendEl.textContent = data.trend.label;
      trendEl.className = `badge ${data.trend.status === 'INCREASING' ? 'badge-risk-critical' : (data.trend.status === 'DECREASING' ? 'badge-risk-safe' : 'badge-status-pending')}`;
    }

    renderActualVsPredictedChart(data.actual_vs_predicted);
  } catch (err) {
    console.error("Error loading forecast:", err);
  }
}

function renderActualVsPredictedChart(points) {
  const container = document.getElementById("forecast-comparison-chart");
  if (!container || !points) return;

  container.innerHTML = points.map(p => `
    <div style="background: rgba(0,0,0,0.2); border: 1px solid var(--border-color); border-radius: var(--radius-sm); padding: 12px 16px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;">
      <div>
        <strong style="font-size: 0.9rem;">${escapeHtml(p.period)}</strong>
        <div style="font-size: 0.75rem; color: var(--text-dim);">
          ${p.actual !== null ? `Actual: ₹${p.actual.toLocaleString('en-IN')} • Predicted: ₹${p.predicted.toLocaleString('en-IN')}` : `Forecast Model: ₹${p.predicted.toLocaleString('en-IN')}`}
        </div>
      </div>
      <div>
        ${p.variance_pct !== null ? `
          <span class="badge ${Math.abs(p.variance_pct) < 5 ? 'badge-risk-safe' : 'badge-risk-medium'}">Variance: ${p.variance_pct > 0 ? '+' : ''}${p.variance_pct}%</span>
        ` : `<span class="badge badge-status-investigation">Projections Active</span>`}
      </div>
    </div>
  `).join("");
}

// =====================================================================
// AI FRAUD DETECTION DASHBOARD & MODEL BENCHMARKS
// =====================================================================

async function loadModelMetrics() {
  try {
    const res = await fetch("/api/fraud/model-metrics");
    const m = await res.json();

    const accEl = document.getElementById("metric-accuracy");
    const precEl = document.getElementById("metric-precision");
    const recEl = document.getElementById("metric-recall");
    const f1El = document.getElementById("metric-f1");

    if (accEl) accEl.textContent = `${m.accuracy}%`;
    if (precEl) precEl.textContent = `${m.precision}%`;
    if (recEl) recEl.textContent = `${m.recall}%`;
    if (f1El) f1El.textContent = `${m.f1_score}%`;

    const tnEl = document.getElementById("matrix-tn");
    const fpEl = document.getElementById("matrix-fp");
    const fnEl = document.getElementById("matrix-fn");
    const tpEl = document.getElementById("matrix-tp");

    if (tnEl) tnEl.textContent = m.confusion_matrix.true_negatives;
    if (fpEl) fpEl.textContent = m.confusion_matrix.false_positives;
    if (fnEl) fnEl.textContent = m.confusion_matrix.false_negatives;
    if (tpEl) tpEl.textContent = m.confusion_matrix.true_positives;
  } catch (err) {
    console.error("Error loading model metrics:", err);
  }
}

function setupCustomFraudCalculator() {
  const form = document.getElementById("form-fraud-calculator");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const amt = parseFloat(document.getElementById("calc-amount").value);
    const cat = document.getElementById("calc-category").value;
    const receiver = document.getElementById("calc-receiver").value.trim();
    const hour = parseInt(document.getElementById("calc-hour").value) || 14;

    try {
      const res = await fetch("/api/fraud/evaluate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          amount: amt,
          category: cat,
          receiver_info: receiver,
          hour: hour
        })
      });
      const data = await res.json();
      renderCustomFraudResult(data);
    } catch (err) {
      alert("Evaluation failed: " + err.message);
    }
  });
}

function renderCustomFraudResult(result) {
  const container = document.getElementById("calc-result-box");
  if (!container) return;

  container.style.display = "block";
  container.innerHTML = `
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
      <div>
        <span class="badge ${getRiskBadgeClass(result.risk_level)}" style="font-size: 0.9rem;">Risk Score: ${result.risk_score} / 100 (${result.risk_level})</span>
      </div>
      <div>
        <span class="badge ${result.requires_human_review ? 'badge-status-pending' : 'badge-status-legit'}">
          ${result.requires_human_review ? 'Requires Human Review' : 'Auto-Approved'}
        </span>
      </div>
    </div>

    <div style="margin-bottom: 12px;">
      ${(result.attributions || []).map(a => `
        <div class="attribution-item">
          <div class="attribution-header">
            <span>${escapeHtml(a.factor)}</span>
            <span style="color: var(--color-danger)">+${a.impact} pts</span>
          </div>
          <div class="attribution-bar-bg">
            <div class="attribution-bar-fill" style="width: ${Math.min(100, a.impact * 2)}%"></div>
          </div>
          <div class="attribution-desc">${escapeHtml(a.detail)}</div>
        </div>
      `).join("")}
    </div>

    <div style="font-size: 0.8rem; background: rgba(0,0,0,0.25); padding: 8px 12px; border-radius: 4px; color: var(--text-dim);">
      Isolation Forest Anomaly Score: <strong>${result.ml_breakdown.isolation_forest_anomaly_score}%</strong> | 
      Random Forest Probability: <strong>${result.ml_breakdown.random_forest_fraud_prob}%</strong> | 
      Z-Score: <strong>${result.ml_breakdown.z_score}σ</strong>
    </div>
  `;
}

// =====================================================================
// AI FINANCIAL ASSISTANT (CHATBOT)
// =====================================================================

function setupChatbot() {
  const form = document.getElementById("form-chatbot");
  const input = document.getElementById("chatbot-input");
  if (!form || !input) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const query = input.value.trim();
    if (!query) return;

    appendChatMessage("user", query);
    input.value = "";

    try {
      const res = await fetch("/api/chatbot/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query })
      });
      const data = await res.json();
      appendChatMessage("bot", data.answer);
    } catch (err) {
      appendChatMessage("bot", "I apologize, but I could not connect to the advisory model. Please try again.");
    }
  });

  // Setup prompt chips
  document.querySelectorAll(".chat-chip").forEach(chip => {
    chip.addEventListener("click", () => {
      input.value = chip.dataset.prompt;
      form.dispatchEvent(new Event("submit"));
    });
  });
}

function appendChatMessage(sender, text) {
  const container = document.getElementById("chatbot-messages");
  if (!container) return;

  const bubble = document.createElement("div");
  bubble.className = `chat-bubble ${sender}`;

  // Simple Markdown parser for bold and line breaks
  const formatted = text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/\n/g, '<br>');

  bubble.innerHTML = formatted;
  container.appendChild(bubble);
  container.scrollTop = container.scrollHeight;
}

// =====================================================================
// NOTIFICATION CENTER
// =====================================================================

async function loadNotifications() {
  try {
    const res = await fetch("/api/notifications");
    const data = await res.json();
    state.notifications = data.notifications || [];
    state.unreadCount = data.unread_count || 0;

    const badge = document.getElementById("nav-notif-count");
    if (badge) {
      badge.textContent = state.unreadCount;
      badge.style.display = state.unreadCount > 0 ? "flex" : "none";
    }

    renderNotifications(state.notifications);
  } catch (err) {
    console.error("Error loading notifications:", err);
  }
}

function renderNotifications(notifs) {
  const container = document.getElementById("notifications-list-container");
  if (!container) return;

  if (notifs.length === 0) {
    container.innerHTML = `<div style="color: var(--text-dim); padding: 30px; text-align: center;">No notifications in your inbox.</div>`;
    return;
  }

  container.innerHTML = notifs.map(n => `
    <div class="card-panel" style="padding: 16px; margin-bottom: 12px; border-left: 4px solid ${n.is_read ? 'var(--border-color)' : 'var(--accent-cyan)'}; opacity: ${n.is_read ? '0.75' : '1'}">
      <div style="display: flex; justify-content: space-between; align-items: flex-start;">
        <div>
          <strong style="font-size: 0.95rem; color: ${n.notification_type === 'FRAUD_ALERT' ? '#f87171' : 'var(--text-main)'}">${escapeHtml(n.title)}</strong>
          <div style="font-size: 0.85rem; color: var(--text-muted); margin: 4px 0;">${escapeHtml(n.message)}</div>
          <div style="font-size: 0.72rem; color: var(--text-dim);">${escapeHtml(n.created_at)} • Type: ${n.notification_type}</div>
        </div>
        ${!n.is_read ? `<button class="btn-secondary" style="padding: 4px 10px; font-size: 0.72rem;" onclick="markSingleNotifRead(${n.id})">Mark Read</button>` : ''}
      </div>
    </div>
  `).join("");
}

async function markSingleNotifRead(id) {
  try {
    await fetch(`/api/notifications/${id}/read`, { method: "POST" });
    loadNotifications();
  } catch (err) {
    console.error(err);
  }
}

async function markAllNotificationsRead() {
  try {
    await fetch("/api/notifications/read-all", { method: "POST" });
    showToast("All notifications marked as read.");
    loadNotifications();
  } catch (err) {
    console.error(err);
  }
}

// =====================================================================
// ADMIN OPERATIONS DASHBOARD
// =====================================================================

async function loadAdminStats() {
  try {
    const res = await fetch("/api/admin/system-stats");
    const data = await res.json();

    const uEl = document.getElementById("admin-total-users");
    const tEl = document.getElementById("admin-total-txns");
    const vEl = document.getElementById("admin-total-volume");
    const fEl = document.getElementById("admin-flagged-count");

    if (uEl) uEl.textContent = data.total_users;
    if (tEl) tEl.textContent = data.total_transactions;
    if (vEl) vEl.textContent = `₹${data.total_volume.toLocaleString('en-IN')}`;
    if (fEl) fEl.textContent = data.flagged_transactions;
  } catch (err) {
    console.error("Error loading admin stats:", err);
  }
}

async function loadAdminUsers() {
  const container = document.getElementById("admin-users-tbody");
  if (!container) return;

  try {
    const res = await fetch("/api/admin/users");
    const data = await res.json();
    const users = data.users || [];

    container.innerHTML = users.map(u => `
      <tr>
        <td><strong>#${u.id}</strong></td>
        <td>${escapeHtml(u.full_name)}</td>
        <td>${escapeHtml(u.email)}</td>
        <td><span class="badge role-${u.role}">${u.role}</span></td>
        <td>₹${Number(u.wallet_balance).toLocaleString('en-IN', { minimumFractionDigits: 2 })}</td>
        <td>${u.transaction_count}</td>
        <td><span class="badge badge-risk-safe">${u.status}</span></td>
      </tr>
    `).join("");
  } catch (err) {
    console.error("Error loading admin users:", err);
  }
}

// =====================================================================
// PRESERVED CYBERSECURITY SCANNER CLIENT LOGIC
// =====================================================================

function setupScanForms() {
  // 1. Link Scanner
  const linkForm = document.getElementById("form-scan-link");
  if (linkForm) {
    linkForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const url = document.getElementById("input-link").value.trim();
      if (!url) return;
      setLoading("btn-scan-link", true);
      try {
        const res = await fetch("/api/scanner/link", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ url })
        });
        const data = await res.json();
        renderScanResult("result-link", data);
      } catch (err) {
        alert("Scan failed: " + err.message);
      } finally {
        setLoading("btn-scan-link", false);
      }
    });
  }

  // 2. OTP Scam Detector
  const otpForm = document.getElementById("form-scan-otp");
  if (otpForm) {
    otpForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const text = document.getElementById("input-otp").value.trim();
      if (!text) return;
      setLoading("btn-scan-otp", true);
      try {
        const res = await fetch("/api/scanner/otp", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text })
        });
        const data = await res.json();
        renderScanResult("result-otp", data);
      } catch (err) {
        alert("Scan failed: " + err.message);
      } finally {
        setLoading("btn-scan-otp", false);
      }
    });
  }

  // 3. Message Scanner
  const msgForm = document.getElementById("form-scan-msg");
  if (msgForm) {
    msgForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const message = document.getElementById("input-msg").value.trim();
      if (!message) return;
      setLoading("btn-scan-msg", true);
      try {
        const res = await fetch("/api/scanner/message", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message })
        });
        const data = await res.json();
        renderScanResult("result-msg", data);
      } catch (err) {
        alert("Scan failed: " + err.message);
      } finally {
        setLoading("btn-scan-msg", false);
      }
    });
  }

  // 4. QR Scanner
  const qrForm = document.getElementById("form-scan-qr");
  if (qrForm) {
    qrForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const payload = document.getElementById("input-qr-payload").value.trim();
      const fileInput = document.getElementById("input-qr-file");

      const formData = new FormData();
      if (fileInput && fileInput.files[0]) {
        formData.append("file", fileInput.files[0]);
      } else if (payload) {
        formData.append("payload", payload);
      } else {
        alert("Please provide a QR image file or paste a UPI string.");
        return;
      }

      setLoading("btn-scan-qr", true);
      try {
        let res;
        if (fileInput && fileInput.files[0]) {
          res = await fetch("/api/scanner/qr", { method: "POST", body: formData });
        } else {
          res = await fetch("/api/scanner/qr", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ payload })
          });
        }
        const data = await res.json();
        renderScanResult("result-qr", data);
      } catch (err) {
        alert("QR inspection failed: " + err.message);
      } finally {
        setLoading("btn-scan-qr", false);
      }
    });
  }
}

function renderScanResult(containerId, data) {
  const container = document.getElementById(containerId);
  if (!container) return;

  container.style.display = "block";
  const badgeClass = getRiskBadgeClass(data.risk_level);

  container.innerHTML = `
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
      <span class="badge ${badgeClass}" style="font-size: 0.95rem;">Threat Score: ${data.risk_score}/100 (${data.risk_level})</span>
      <span style="font-size: 0.8rem; color: var(--text-dim);">${data.analysis_time_ms || 12}ms analysis</span>
    </div>

    ${data.warning_title ? `<h4 style="color: #f87171; margin-bottom: 6px;">${escapeHtml(data.warning_title)}</h4>` : ''}
    <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 14px;">${escapeHtml(data.actionable_advice || data.recommendation || '')}</p>

    <h5 style="font-size: 0.82rem; color: var(--text-dim); text-transform: uppercase; margin-bottom: 8px;">Explainable AI Attribution Breakdown:</h5>
    ${(data.attributions || []).map(a => `
      <div class="attribution-item">
        <div class="attribution-header">
          <span>${escapeHtml(a.factor || a.feature)}</span>
          <span style="color: var(--color-danger)">+${a.impact || a.score || 0} pts</span>
        </div>
        <div class="attribution-bar-bg">
          <div class="attribution-bar-fill" style="width: ${Math.min(100, (a.impact || a.score || 10) * 2)}%"></div>
        </div>
        <div class="attribution-desc">${escapeHtml(a.detail || a.desc || '')}</div>
      </div>
    `).join("")}
  `;
}

function setupSampleButtons() {
  document.querySelectorAll(".pill-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const inputId = btn.dataset.input;
      const sample = btn.dataset.sample;
      const el = document.getElementById(inputId);
      if (el) {
        el.value = sample;
        el.focus();
      }
    });
  });
}

async function loadAcademyModules() {
  const container = document.getElementById("academy-modules-container");
  if (!container) return;

  try {
    const res = await fetch("/api/academy/modules");
    const modules = await res.json();

    container.innerHTML = modules.map(m => `
      <div class="card-panel" style="margin-bottom: 16px; padding: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px;">
          <div>
            <span class="badge badge-risk-safe" style="margin-bottom: 6px;">Module #${m.id}</span>
            <h4 style="font-size: 1.1rem; color: #38bdf8;">${escapeHtml(m.title)}</h4>
          </div>
          <span style="font-size: 1.8rem;">${m.badge_icon || '🎓'}</span>
        </div>
        <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 12px;">${escapeHtml(m.summary)}</p>
        <div style="background: rgba(0,0,0,0.25); border-left: 3px solid var(--accent-cyan); padding: 10px 14px; border-radius: 4px; font-size: 0.8rem; margin-bottom: 14px;">
          <strong>Security Golden Rule:</strong> ${escapeHtml(m.golden_rule)}
        </div>
        <button class="btn-secondary" style="font-size: 0.8rem; padding: 6px 14px;" onclick="startQuizModal(${m.id}, '${escapeHtml(m.title)}')">Take Knowledge Check Quiz</button>
      </div>
    `).join("");
  } catch (err) {
    console.error("Error loading academy:", err);
  }
}

function startQuizModal(moduleId, title) {
  const ans = confirm(`Question for ${title}:\n\nTrue or False: A shopkeeper or customer must enter their UPI PIN to RECEIVE incoming cashback or refunds?`);
  if (!ans) {
    submitQuizScore(moduleId, 100);
    alert("🎉 Correct! You never enter your UPI PIN to receive money. Badge unlocked!");
  } else {
    alert("❌ Incorrect. The Golden Rule of UPI is: UPI PIN is ONLY entered when SENDING money, NEVER for receiving money!");
  }
}

async function submitQuizScore(moduleId, score) {
  try {
    await fetch("/api/academy/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ module_id: moduleId, score: score })
    });
  } catch (e) {
    console.error(e);
  }
}

function setupIncidentReportForm() {
  const form = document.getElementById("form-incident-report");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const ftype = document.getElementById("report-fraud-type").value;
    const entity = document.getElementById("report-entity").value.trim();
    const loss = parseFloat(document.getElementById("report-loss").value) || 0;
    const desc = document.getElementById("report-desc").value.trim();

    try {
      const res = await fetch("/api/reports/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          fraud_type: ftype,
          suspected_entity: entity,
          financial_loss: loss,
          description: desc
        })
      });
      const data = await res.json();
      renderIncidentReportResult(data);
    } catch (err) {
      alert("Report generation failed: " + err.message);
    }
  });
}

function renderIncidentReportResult(data) {
  const container = document.getElementById("incident-report-result");
  if (!container) return;

  container.style.display = "block";
  container.innerHTML = `
    <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid var(--color-safe); border-radius: var(--radius-sm); padding: 18px; margin-top: 18px;">
      <h4 style="color: #34d399; margin-bottom: 8px;">✅ Official Incident Complaint Dossier Generated</h4>
      <p style="font-size: 0.85rem; margin-bottom: 10px;">Unique Cybercrime Filing Reference: <strong style="color: #38bdf8;">${escapeHtml(data.report_number)}</strong></p>
      <div style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.6; margin-bottom: 14px;">
        ${escapeHtml(data.instructions)} Call National Cybercrime Helpline <strong>1930</strong> or present this dossier reference at <strong>cybercrime.gov.in</strong>.
      </div>
      <button class="btn-primary" onclick="window.print()">Print Dossier Filing Sheet</button>
    </div>
  `;
}

// =====================================================================
// UTILITY HELPERS & MODALS
// =====================================================================

function setupLanguageSelector() {
  const sel = document.getElementById("nav-lang-selector");
  if (!sel) return;

  sel.addEventListener("change", (e) => {
    const lang = e.target.value;
    state.language = lang;
    applyLanguage(lang);
  });
}

function applyLanguage(lang) {
  const dict = i18n[lang] || i18n.en;
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.dataset.i18n;
    if (dict[key]) {
      el.textContent = dict[key];
    }
  });
  showToast(`Language set to ${lang.toUpperCase()}`);
}

function setupModals() {
  document.querySelectorAll(".modal-overlay").forEach(overlay => {
    overlay.addEventListener("click", (e) => {
      if (e.target === overlay) {
        overlay.classList.remove("active");
      }
    });
  });
}

function openModal(modalId) {
  const m = document.getElementById(modalId);
  if (m) m.classList.add("active");
}

function closeModal(modalId) {
  const m = document.getElementById(modalId);
  if (m) m.classList.remove("active");
}

function setLoading(btnId, isLoading) {
  const btn = document.getElementById(btnId);
  if (!btn) return;
  btn.disabled = isLoading;
  btn.style.opacity = isLoading ? "0.6" : "1";
}

function getRiskBadgeClass(level) {
  switch (level) {
    case "SAFE": return "badge-risk-safe";
    case "LOW": return "badge-risk-low";
    case "MEDIUM": return "badge-risk-medium";
    case "HIGH_RISK": case "HIGH": return "badge-risk-high";
    case "CRITICAL": return "badge-risk-critical";
    default: return "badge-status-investigation";
  }
}

function getStatusBadgeClass(status) {
  switch (status) {
    case "Legitimate": return "badge-status-legit";
    case "Pending Review": return "badge-status-pending";
    case "Suspicious": return "badge-status-suspicious";
    case "Under Investigation": return "badge-status-investigation";
    default: return "badge-status-legit";
  }
}

function showToast(msg) {
  let toast = document.getElementById("app-toast");
  if (!toast) {
    toast = document.createElement("div");
    toast.id = "app-toast";
    toast.style.position = "fixed";
    toast.style.bottom = "24px";
    toast.style.right = "24px";
    toast.style.background = "linear-gradient(135deg, #1e1b4b, #0f172a)";
    toast.style.border = "1px solid var(--accent-cyan)";
    toast.style.color = "#f8fafc";
    toast.style.padding = "12px 20px";
    toast.style.borderRadius = "8px";
    toast.style.boxShadow = "0 10px 25px rgba(0,0,0,0.5)";
    toast.style.zIndex = "9999";
    toast.style.fontSize = "0.88rem";
    toast.style.fontWeight = "600";
    toast.style.transition = "all 0.3s ease";
    document.body.appendChild(toast);
  }
  toast.textContent = msg;
  toast.style.opacity = "1";
  toast.style.transform = "translateY(0)";
  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateY(10px)";
  }, 3200);
}

function escapeHtml(str) {
  if (typeof str !== "string") return str || "";
  return str.replace(/[&<>"']/g, (m) => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;'
  })[m]);
}
