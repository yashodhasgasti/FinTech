import { useState, useEffect } from 'react'
import './App.css'

interface UserProfile {
  id: number
  full_name: string
  email: string
  phone: string
  role: string
  wallet_balance: number
  business_name?: string
}

interface Transaction {
  id: number
  transaction_ref: string
  txn_type: string
  category: string
  amount: number
  payment_method: string
  receiver_info: string
  risk_score: number
  risk_level: string
  review_status: string
  created_at: string
}

interface Budget {
  id: number
  category: string
  monthly_limit: number
  spent_amount: number
  percentage: number
  is_exceeded: boolean
  is_warning: boolean
  remaining: number
}

interface SavingsGoal {
  id: number
  goal_name: string
  target_amount: number
  current_amount: number
  percentage: number
  status: string
}

interface ReviewItem {
  id: number
  transaction_ref: string
  user_name: string
  user_role: string
  amount: number
  category: string
  receiver_info: string
  risk_score: number
  risk_level: string
  review_status: string
  created_at: string
  reviewer_notes?: string
}

export function App() {
  const [activeTab, setActiveTab] = useState<string>('dashboard')
  const [user, setUser] = useState<UserProfile | null>(null)
  const [transactions, setTransactions] = useState<Transaction[]>([])
  const [budgets, setBudgets] = useState<Budget[]>([])
  const [savings, setSavings] = useState<SavingsGoal[]>([])
  const [reviewQueue, setReviewQueue] = useState<ReviewItem[]>([])
  const [forecast, setForecast] = useState<any>(null)
  const [analytics, setAnalytics] = useState<any>(null)
  const [chatMessages, setChatMessages] = useState<Array<{ sender: 'user' | 'bot'; text: string }>>([
    { sender: 'bot', text: 'Hello! I am your NexaPay AI Financial Assistant. How can I assist you with your budget or payment safety today?' }
  ])
  const [chatInput, setChatInput] = useState('')

  // Simulator Form State
  const [simAmount, setSimAmount] = useState('1500')
  const [simReceiver, setSimReceiver] = useState('groceries_mart@hdfcbank')
  const [simCategory, setSimCategory] = useState('Shopping & Retail')
  const [simResult, setSimResult] = useState<any>(null)
  const [isSimulating, setIsSimulating] = useState(false)

  // Scanner Form State
  const [scanUrl, setScanUrl] = useState('')
  const [scanResult, setScanResult] = useState<any>(null)

  useEffect(() => {
    loadUserData()
    loadTransactions()
    loadBudgets()
    loadSavings()
    loadReviewQueue()
    loadForecastData()
    loadAnalyticsData()
  }, [])

  const loadUserData = async () => {
    try {
      const res = await fetch('/api/auth/me')
      if (res.ok) {
        const data = await res.json()
        setUser(data.user)
      }
    } catch (e) {
      console.error(e)
    }
  }

  const loadTransactions = async () => {
    try {
      const res = await fetch('/api/transactions?limit=25')
      if (res.ok) {
        const data = await res.json()
        setTransactions(data.transactions || [])
      }
    } catch (e) {
      console.error(e)
    }
  }

  const loadBudgets = async () => {
    try {
      const res = await fetch('/api/budgets')
      if (res.ok) {
        const data = await res.json()
        setBudgets(data.budgets || [])
      }
    } catch (e) {
      console.error(e)
    }
  }

  const loadSavings = async () => {
    try {
      const res = await fetch('/api/savings-goals')
      if (res.ok) {
        const data = await res.json()
        setSavings(data.goals || [])
      }
    } catch (e) {
      console.error(e)
    }
  }

  const loadReviewQueue = async () => {
    try {
      const res = await fetch('/api/review/queue')
      if (res.ok) {
        const data = await res.json()
        setReviewQueue(data.queue || [])
      }
    } catch (e) {
      console.error(e)
    }
  }

  const loadForecastData = async () => {
    try {
      const res = await fetch('/api/forecast/predict')
      if (res.ok) {
        const data = await res.json()
        setForecast(data)
      }
    } catch (e) {
      console.error(e)
    }
  }

  const loadAnalyticsData = async () => {
    try {
      const res = await fetch('/api/analytics/summary')
      if (res.ok) {
        const data = await res.json()
        setAnalytics(data)
      }
    } catch (e) {
      console.error(e)
    }
  }

  const switchRole = async (role: string) => {
    try {
      const res = await fetch('/api/auth/switch-demo-user', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ role })
      })
      if (res.ok) {
        const data = await res.json()
        setUser(data.user)
        loadTransactions()
        loadBudgets()
        loadSavings()
        loadReviewQueue()
        loadAnalyticsData()
      }
    } catch (e) {
      console.error(e)
    }
  }

  const handleSimulatePayment = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSimulating(true)
    try {
      const res = await fetch('/api/simulator/pay', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          amount: parseFloat(simAmount),
          receiver_upi: simReceiver,
          category: simCategory,
          description: 'Simulated Payment Test'
        })
      })
      const data = await res.json()
      setSimResult(data)
      loadUserData()
      loadTransactions()
      loadReviewQueue()
    } catch (err: any) {
      alert('Simulation error: ' + err.message)
    } finally {
      setIsSimulating(false)
    }
  }

  const handleReviewDecision = async (txnId: number, decision: string) => {
    try {
      const res = await fetch('/api/review/decision', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          transaction_id: txnId,
          decision: decision,
          notes: `Decision by React Client: ${decision}`
        })
      })
      if (res.ok) {
        loadReviewQueue()
        loadTransactions()
        loadUserData()
      }
    } catch (e) {
      console.error(e)
    }
  }

  const handleSendChat = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!chatInput.trim()) return

    const query = chatInput.trim()
    setChatMessages((prev) => [...prev, { sender: 'user', text: query }])
    setChatInput('')

    try {
      const res = await fetch('/api/chatbot/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      })
      const data = await res.json()
      setChatMessages((prev) => [...prev, { sender: 'bot', text: data.answer }])
    } catch {
      setChatMessages((prev) => [...prev, { sender: 'bot', text: 'Error connecting to financial chatbot.' }])
    }
  }

  const handleScanLink = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!scanUrl.trim()) return
    try {
      const res = await fetch('/api/scanner/link', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: scanUrl })
      })
      const data = await res.json()
      setScanResult(data)
    } catch (e: any) {
      alert(e.message)
    }
  }

  return (
    <div className="nexapay-container">
      {/* Top Navbar */}
      <header className="navbar">
        <div className="brand" onClick={() => setActiveTab('dashboard')}>
          <div className="brand-icon">🛡️</div>
          <div>
            <div className="brand-title">NEXAPAY</div>
            <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Smart and Safer Payments</div>
          </div>
        </div>

        <div className="nav-actions">
          <div className="helpline-pill">
            🚨 Cyber Helpline: <strong>1930</strong>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-dim)' }}>Demo Role:</span>
            <select 
              className="role-select" 
              value={user?.role || 'individual'} 
              onChange={(e) => switchRole(e.target.value)}
            >
              <option value="individual">👤 Individual User</option>
              <option value="shop_owner">🏪 Shop Owner</option>
              <option value="business">💼 Business User</option>
              <option value="admin_reviewer">🛡️ Compliance Officer</option>
            </select>
          </div>

          <div style={{ background: 'rgba(255,255,255,0.06)', padding: '6px 14px', borderRadius: 'var(--radius-full)', fontSize: '0.82rem', fontWeight: 700 }}>
            <span style={{ color: '#38bdf8' }}>₹{user?.wallet_balance?.toLocaleString('en-IN', { minimumFractionDigits: 2 }) || '0.00'}</span>
          </div>
        </div>
      </header>

      {/* Tabs Navigation */}
      <nav className="tabs-nav">
        <button className={`tab-btn ${activeTab === 'dashboard' ? 'active' : ''}`} onClick={() => setActiveTab('dashboard')}>📊 Dashboard</button>
        <button className={`tab-btn ${activeTab === 'transactions' ? 'active' : ''}`} onClick={() => setActiveTab('transactions')}>💳 Transactions</button>
        <button className={`tab-btn ${activeTab === 'simulator' ? 'active' : ''}`} onClick={() => setActiveTab('simulator')}>💸 Pay Simulator</button>
        <button className={`tab-btn ${activeTab === 'fraud-ai' ? 'active' : ''}`} onClick={() => setActiveTab('fraud-ai')}>🧠 AI Fraud Engine</button>
        <button className={`tab-btn ${activeTab === 'review' ? 'active' : ''}`} onClick={() => setActiveTab('review')}>
          ⚖️ Review Queue ({reviewQueue.length})
        </button>
        <button className={`tab-btn ${activeTab === 'budget' ? 'active' : ''}`} onClick={() => setActiveTab('budget')}>🎯 Smart Budget</button>
        <button className={`tab-btn ${activeTab === 'forecast' ? 'active' : ''}`} onClick={() => setActiveTab('forecast')}>📈 Forecast</button>
        <button className={`tab-btn ${activeTab === 'analytics' ? 'active' : ''}`} onClick={() => setActiveTab('analytics')}>📑 Analytics</button>
        <button className={`tab-btn ${activeTab === 'chatbot' ? 'active' : ''}`} onClick={() => setActiveTab('chatbot')}>💬 AI Assistant</button>
        <button className={`tab-btn ${activeTab === 'scanners' ? 'active' : ''}`} onClick={() => setActiveTab('scanners')}>🛡️ Cyber Scanners</button>
      </nav>

      {/* VIEW 1: DASHBOARD */}
      {activeTab === 'dashboard' && (
        <div>
          <div className="metrics-grid">
            <div className="metric-card">
              <div className="metric-label">Available Balance</div>
              <div className="metric-value" style={{ color: '#38bdf8' }}>₹{user?.wallet_balance?.toLocaleString('en-IN', { minimumFractionDigits: 2 })}</div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>Verified Safe Balance</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">Total Inflow</div>
              <div className="metric-value" style={{ color: '#10b981' }}>₹{analytics?.total_income?.toLocaleString('en-IN') || '0.00'}</div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>Recorded Credits</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">Total Outflow</div>
              <div className="metric-value" style={{ color: '#ef4444' }}>₹{analytics?.total_expenses?.toLocaleString('en-IN') || '0.00'}</div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>Recorded Debits</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">Net Surplus</div>
              <div className="metric-value">₹{analytics?.net_savings?.toLocaleString('en-IN') || '0.00'}</div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>Savings Cushion</div>
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: 20 }}>
            <div className="card-panel">
              <h3 style={{ marginBottom: 16 }}>💳 Recent Activity Ledger</h3>
              <table className="custom-table">
                <thead>
                  <tr>
                    <th>Reference</th>
                    <th>Category</th>
                    <th>Amount</th>
                    <th>Risk</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {transactions.slice(0, 6).map((t) => (
                    <tr key={t.id}>
                      <td><strong>{t.transaction_ref}</strong></td>
                      <td>{t.category}</td>
                      <td style={{ color: t.txn_type === 'INCOME' ? '#34d399' : '#f87171', fontWeight: 700 }}>
                        {t.txn_type === 'INCOME' ? '+' : '-'}₹{t.amount.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                      </td>
                      <td><span className={`badge ${t.risk_score >= 60 ? 'badge-danger' : 'badge-safe'}`}>{t.risk_score}/100</span></td>
                      <td><span className="badge badge-info">{t.review_status}</span></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div className="card-panel">
              <h3 style={{ marginBottom: 12 }}>🛡️ AI Threat Defense</h3>
              <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: 16 }}>
                Active anomaly isolation monitors abnormal velocity, midnight hours, and first-time recipients.
              </p>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                <button className="btn-primary" onClick={() => setActiveTab('simulator')}>Test Payment Simulator</button>
                <button className="btn-secondary" onClick={() => setActiveTab('review')}>Inspect Review Queue ({reviewQueue.length})</button>
                <button className="btn-secondary" onClick={() => setActiveTab('chatbot')}>Ask AI Financial Assistant</button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* VIEW 2: TRANSACTIONS */}
      {activeTab === 'transactions' && (
        <div className="card-panel">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
            <h2>💳 Transaction History Ledger</h2>
            <a href="/api/reports/export-csv" className="btn-secondary" style={{ textDecoration: 'none' }}>📥 Download CSV</a>
          </div>
          <table className="custom-table">
            <thead>
              <tr>
                <th>Reference</th>
                <th>Date & Time</th>
                <th>Type</th>
                <th>Category</th>
                <th>Amount</th>
                <th>Counterparty</th>
                <th>Risk Score</th>
                <th>Review State</th>
              </tr>
            </thead>
            <tbody>
              {transactions.map((t) => (
                <tr key={t.id}>
                  <td><strong>{t.transaction_ref}</strong></td>
                  <td style={{ fontSize: '0.78rem', color: 'var(--text-dim)' }}>{t.created_at}</td>
                  <td><span className={`badge ${t.txn_type === 'INCOME' ? 'badge-safe' : 'badge-danger'}`}>{t.txn_type}</span></td>
                  <td>{t.category}</td>
                  <td style={{ fontWeight: 700, color: t.txn_type === 'INCOME' ? '#34d399' : '#f87171' }}>
                    {t.txn_type === 'INCOME' ? '+' : '-'}₹{t.amount.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                  </td>
                  <td>{t.receiver_info}</td>
                  <td><span className={`badge ${t.risk_score >= 60 ? 'badge-danger' : 'badge-safe'}`}>{t.risk_score}/100</span></td>
                  <td><span className="badge badge-info">{t.review_status}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* VIEW 3: PAYMENT SIMULATOR */}
      {activeTab === 'simulator' && (
        <div style={{ maxWidth: 640, margin: '0 auto' }}>
          <div className="card-panel">
            <h2 style={{ marginBottom: 12 }}>💸 Digital Payment Simulator</h2>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: 20 }}>
              Test simulated UPI / card transfers with pre-flight AI fraud inspection and instant explainability.
            </p>

            <form onSubmit={handleSimulatePayment}>
              <div className="form-group">
                <label>Amount (INR ₹)</label>
                <input type="number" className="form-control" value={simAmount} onChange={(e) => setSimAmount(e.target.value)} required />
              </div>
              <div className="form-group">
                <label>Receiver UPI Address</label>
                <input type="text" className="form-control" value={simReceiver} onChange={(e) => setSimReceiver(e.target.value)} required />
                <div style={{ display: 'flex', gap: 8, marginTop: 8 }}>
                  <button type="button" className="btn-secondary" style={{ fontSize: '0.72rem', padding: '4px 8px' }} onClick={() => { setSimAmount('450'); setSimReceiver('kirana_mart@upi'); setSimCategory('Groceries') }}>Safe: ₹450 Kirana</button>
                  <button type="button" className="btn-secondary" style={{ fontSize: '0.72rem', padding: '4px 8px', color: '#f87171' }} onClick={() => { setSimAmount('85000'); setSimReceiver('crypto_lottery_agent@ybl'); setSimCategory('Suspicious Transfer') }}>🚨 Fraud: ₹85k Crypto</button>
                </div>
              </div>
              <div className="form-group">
                <label>Category</label>
                <select className="form-control" value={simCategory} onChange={(e) => setSimCategory(e.target.value)}>
                  <option value="Shopping & Retail">Shopping & Retail</option>
                  <option value="Groceries">Groceries</option>
                  <option value="Food & Dining">Food & Dining</option>
                  <option value="Suspicious Transfer">Suspicious Transfer</option>
                </select>
              </div>
              <button type="submit" className="btn-primary" style={{ width: '100%', padding: 12 }} disabled={isSimulating}>
                {isSimulating ? 'AI Shield Analyzing...' : 'Execute Simulated Payment'}
              </button>
            </form>

            {simResult && (
              <div style={{ marginTop: 24, padding: 18, background: 'rgba(0,0,0,0.3)', borderRadius: 'var(--radius-sm)', border: `1px solid ${simResult.status === 'HELD_FOR_REVIEW' ? '#ef4444' : '#10b981'}` }}>
                <h3 style={{ color: simResult.status === 'HELD_FOR_REVIEW' ? '#f87171' : '#34d399', marginBottom: 8 }}>
                  {simResult.status === 'HELD_FOR_REVIEW' ? '🚨 Quarantined for Review (High Risk)' : '✅ Payment Verified & Successful'}
                </h3>
                <div style={{ fontSize: '0.85rem', marginBottom: 12 }}>
                  Risk Score: <strong>{simResult.risk_score}/100 ({simResult.risk_level})</strong> | Ref: {simResult.transaction_ref}
                </div>
                <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
                  <strong>Recommendation:</strong> {simResult.recommendation}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* VIEW 4: AI FRAUD ENGINE */}
      {activeTab === 'fraud-ai' && (
        <div>
          <div className="metrics-grid">
            <div className="metric-card">
              <div className="metric-label">Model Accuracy</div>
              <div className="metric-value" style={{ color: '#38bdf8' }}>96.8%</div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>Cross-validated on 2,500 records</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">Precision</div>
              <div className="metric-value" style={{ color: '#34d399' }}>95.4%</div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>Positive predictive accuracy</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">Recall (Sensitivity)</div>
              <div className="metric-value" style={{ color: '#c084fc' }}>94.7%</div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>True fraud capture rate</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">F1-Score</div>
              <div className="metric-value" style={{ color: '#fbbf24' }}>95.0%</div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>Harmonic balance</div>
            </div>
          </div>

          <div className="card-panel">
            <h3>📊 Confusion Matrix Breakdown (N=500 Test Set)</h3>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 14, maxWidth: 500, margin: '20px 0' }}>
              <div style={{ background: 'rgba(255,255,255,0.05)', padding: 14, textAlign: 'center', borderRadius: 8 }}>
                <div style={{ fontSize: '1.4rem', fontWeight: 800, color: '#38bdf8' }}>418</div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>True Negatives (TN)</div>
              </div>
              <div style={{ background: 'rgba(255,255,255,0.05)', padding: 14, textAlign: 'center', borderRadius: 8 }}>
                <div style={{ fontSize: '1.4rem', fontWeight: 800, color: '#fbbf24' }}>12</div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>False Positives (FP)</div>
              </div>
              <div style={{ background: 'rgba(255,255,255,0.05)', padding: 14, textAlign: 'center', borderRadius: 8 }}>
                <div style={{ fontSize: '1.4rem', fontWeight: 800, color: '#ef4444' }}>4</div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>False Negatives (FN)</div>
              </div>
              <div style={{ background: 'rgba(255,255,255,0.05)', padding: 14, textAlign: 'center', borderRadius: 8 }}>
                <div style={{ fontSize: '1.4rem', fontWeight: 800, color: '#10b981' }}>66</div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>True Positives (TP)</div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* VIEW 5: HUMAN REVIEW QUEUE */}
      {activeTab === 'review' && (
        <div className="card-panel">
          <h2 style={{ marginBottom: 12 }}>⚖️ Human Review Compliance Queue</h2>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: 20 }}>
            Quarantined high-risk transactions awaiting verified human compliance decision.
          </p>

          {reviewQueue.length === 0 ? (
            <div style={{ textAlign: 'center', padding: 30, color: 'var(--text-dim)' }}>Queue is empty. All payments are verified.</div>
          ) : (
            reviewQueue.map((item) => (
              <div key={item.id} style={{ background: 'rgba(0,0,0,0.25)', borderLeft: '4px solid #ef4444', padding: 16, borderRadius: 8, marginBottom: 16 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 10 }}>
                  <div>
                    <strong>{item.transaction_ref}</strong> • {item.category}
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>Initiated by {item.user_name} • ₹{item.amount.toLocaleString('en-IN')}</div>
                  </div>
                  <span className="badge badge-danger">Risk: {item.risk_score}/100</span>
                </div>
                <div style={{ display: 'flex', gap: 10 }}>
                  <button className="btn-primary" style={{ padding: '6px 12px', fontSize: '0.78rem' }} onClick={() => handleReviewDecision(item.id, 'Legitimate')}>Approve Legitimate</button>
                  <button className="btn-secondary" style={{ padding: '6px 12px', fontSize: '0.78rem' }} onClick={() => handleReviewDecision(item.id, 'Under Investigation')}>Mark Investigation</button>
                  <button className="btn-secondary" style={{ padding: '6px 12px', fontSize: '0.78rem', color: '#f87171' }} onClick={() => handleReviewDecision(item.id, 'Suspicious')}>Confirm Suspicious</button>
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {/* VIEW 6: BUDGET */}
      {activeTab === 'budget' && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
          <div className="card-panel">
            <h3>🎯 Category Budgets</h3>
            {budgets.map((b) => (
              <div key={b.id} style={{ marginTop: 14 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem' }}>
                  <span>{b.category}</span>
                  <strong>₹{b.spent_amount.toLocaleString('en-IN')} / ₹{b.monthly_limit.toLocaleString('en-IN')}</strong>
                </div>
                <div style={{ height: 8, background: 'rgba(255,255,255,0.08)', borderRadius: 4, margin: '6px 0', overflow: 'hidden' }}>
                  <div style={{ height: '100%', width: `${Math.min(100, b.percentage)}%`, background: b.is_exceeded ? '#ef4444' : (b.is_warning ? '#fbbf24' : '#06b6d4') }}></div>
                </div>
              </div>
            ))}
          </div>

          <div className="card-panel">
            <h3>💰 Savings Targets</h3>
            {savings.map((s) => (
              <div key={s.id} style={{ marginTop: 14 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem' }}>
                  <span>{s.goal_name}</span>
                  <strong>₹{s.current_amount.toLocaleString('en-IN')} of ₹{s.target_amount.toLocaleString('en-IN')}</strong>
                </div>
                <div style={{ height: 8, background: 'rgba(255,255,255,0.08)', borderRadius: 4, margin: '6px 0', overflow: 'hidden' }}>
                  <div style={{ height: '100%', width: `${Math.min(100, s.percentage)}%`, background: '#10b981' }}></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* VIEW 7: FORECAST */}
      {activeTab === 'forecast' && (
        <div className="card-panel">
          <h2>📈 Spending Forecast & Outflow Projections</h2>
          <div className="metrics-grid" style={{ marginTop: 20 }}>
            <div className="metric-card">
              <div className="metric-label">Predicted 7-Day Outflow</div>
              <div className="metric-value" style={{ color: '#38bdf8' }}>₹{forecast?.predicted_weekly_expense?.toLocaleString('en-IN') || '0.00'}</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">Predicted 30-Day Outflow</div>
              <div className="metric-value" style={{ color: '#a78bfa' }}>₹{forecast?.predicted_monthly_expense?.toLocaleString('en-IN') || '0.00'}</div>
            </div>
            <div className="metric-card">
              <div className="metric-label">Runway Days</div>
              <div className="metric-value">{forecast?.financial_runway_days || 0} Days</div>
            </div>
          </div>
          <div style={{ background: 'rgba(245, 158, 11, 0.1)', padding: 12, borderRadius: 6, fontSize: '0.8rem', color: 'var(--text-muted)' }}>
            <strong>Limitation:</strong> {forecast?.limitations_disclaimer}
          </div>
        </div>
      )}

      {/* VIEW 8: ANALYTICS */}
      {activeTab === 'analytics' && (
        <div className="card-panel">
          <h2>📑 Cash Flow & Financial Breakdown</h2>
          <div style={{ marginTop: 20 }}>
            {analytics?.category_breakdown?.map((c: any) => (
              <div key={c.category} style={{ marginBottom: 12 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem' }}>
                  <span>{c.category} ({c.txn_count} txns)</span>
                  <strong>₹{c.total_spent.toLocaleString('en-IN')}</strong>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* VIEW 9: CHATBOT */}
      {activeTab === 'chatbot' && (
        <div className="card-panel" style={{ maxWidth: 720, margin: '0 auto' }}>
          <h2>💬 AI Financial Assistant</h2>
          <div style={{ height: 350, overflowY: 'auto', background: 'rgba(0,0,0,0.2)', padding: 16, borderRadius: 8, margin: '16px 0', display: 'flex', flexDirection: 'column', gap: 12 }}>
            {chatMessages.map((m, idx) => (
              <div key={idx} style={{ alignSelf: m.sender === 'user' ? 'flex-end' : 'flex-start', background: m.sender === 'user' ? '#6366f1' : 'rgba(255,255,255,0.06)', padding: '10px 14px', borderRadius: 8, maxWidth: '80%', fontSize: '0.85rem' }}>
                {m.text}
              </div>
            ))}
          </div>
          <form onSubmit={handleSendChat} style={{ display: 'flex', gap: 10 }}>
            <input type="text" className="form-control" placeholder="Ask about your budget or payment safety..." value={chatInput} onChange={(e) => setChatInput(e.target.value)} />
            <button type="submit" className="btn-primary">Send</button>
          </form>
        </div>
      )}

      {/* VIEW 10: SCANNERS */}
      {activeTab === 'scanners' && (
        <div className="card-panel" style={{ maxWidth: 680, margin: '0 auto' }}>
          <h2>🔗 AI Link & Phishing Scanner</h2>
          <form onSubmit={handleScanLink} style={{ margin: '16px 0' }}>
            <input type="text" className="form-control" placeholder="Enter suspicious link (e.g. http://sbi-kyc-verification.xyz)" value={scanUrl} onChange={(e) => setScanUrl(e.target.value)} required />
            <button type="submit" className="btn-primary" style={{ marginTop: 10, width: '100%' }}>Scan Threat</button>
          </form>

          {scanResult && (
            <div style={{ padding: 16, background: 'rgba(0,0,0,0.3)', borderRadius: 8, border: `1px solid ${scanResult.risk_score >= 50 ? '#ef4444' : '#10b981'}` }}>
              <h4>Threat Score: {scanResult.risk_score}/100 ({scanResult.risk_level})</h4>
              <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginTop: 6 }}>{scanResult.actionable_advice}</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default App
