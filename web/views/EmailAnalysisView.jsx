import React, { useState } from 'react';
import { analyzeEmail } from '../api';
import {
  Mail,
  ShieldAlert,
  ShieldCheck,
  AlertTriangle,
  Sparkles,
  RefreshCw,
  AtSign,
  FileText,
  CheckCircle,
  Copy,
  Check
} from 'lucide-react';

const EMAIL_SAMPLES = {
  phishing: {
    subject: 'Urgent: Your PayPal Account Has Been Suspended',
    sender: 'security-service@paypal-verification-center.xyz',
    body: 'Dear Valued Customer,\n\nWe detected unauthorized login attempts to your bank account from an unrecognized IP address. To prevent permanent suspension, please verify your credentials and billing details immediately by logging in at http://192.168.1.10/verify-account.\n\nFailure to act within 24 hours will result in permanent account termination.\n\nSincerely,\nPayPal Fraud Prevention Team'
  },
  legitimate: {
    subject: 'Quarterly Security Engineering Sync — Q4 Roadmap',
    sender: 'alex.chen@acme-corp.internal',
    body: 'Team,\n\nPlease find attached the agenda for our upcoming quarterly sprint planning. We will review model performance, SQLite database indexing, and Vercel serverless deployment metrics.\n\nMeeting link is in your corporate calendar invite.\n\nBest,\nAlex'
  }
};

export function EmailAnalysisView() {
  const [subject, setSubject] = useState('');
  const [sender, setSender] = useState('');
  const [body, setBody] = useState('');
  const [logToDb, setLogToDb] = useState(true);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [copied, setCopied] = useState(false);

  const handleAnalyze = async () => {
    if (!subject.trim() && !body.trim()) {
      setError('Please provide at least an Email Subject Line or Email Body.');
      return;
    }
    setError(null);
    setLoading(true);
    try {
      const response = await analyzeEmail({ subject, sender, body, logToDb });
      setResult(response.data);
    } catch (err) {
      setError(err.message || 'Email analysis failed.');
    } finally {
      setLoading(false);
    }
  };

  const loadSample = (type) => {
    const sample = EMAIL_SAMPLES[type];
    if (sample) {
      setSubject(sample.subject);
      setSender(sample.sender);
      setBody(sample.body);
      setResult(null);
      setError(null);
    }
  };

  const copyResult = () => {
    if (!result) return;
    const text = `Email Threat Analysis Verdict: ${result.label} (${(result.confidence * 100).toFixed(1)}%)\nSubject: ${subject}\nSender: ${sender}`;
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="page-workspace">
      {/* Header Banner */}
      <div className="welcome-banner">
        <div>
          <h2 className="welcome-title">
            Email Threat <span className="welcome-gradient">Analysis</span> ✉
          </h2>
          <p className="welcome-subtitle">
            Multi-field lexical evaluation of Email Subject, Sender Domain, and Body payload
          </p>
        </div>
      </div>

      {/* Main Form */}
      <div className="saas-card">
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '14px' }}>
          <span style={{ fontSize: '0.85rem', fontWeight: 700, color: '#FFFFFF', textTransform: 'uppercase' }}>
            Quick Test Scenarios
          </span>
          <span style={{ fontSize: '0.75rem', color: '#B9B1C8' }}>Select to prefill email headers</span>
        </div>

        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginBottom: '20px' }}>
          <button className="btn btn-secondary" onClick={() => loadSample('phishing')}>
            🎣 Phishing Account Alert (Spam)
          </button>
          <button className="btn btn-secondary" onClick={() => loadSample('legitimate')}>
            💼 Legitimate Meeting Notice (Ham)
          </button>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px', marginBottom: '16px' }}>
          <div>
            <label className="input-label">Email Subject Line</label>
            <input
              type="text"
              className="text-input"
              placeholder="e.g. Urgent: Account Verification Required"
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
            />
          </div>

          <div>
            <label className="input-label">Sender Address / Display (Optional)</label>
            <input
              type="text"
              className="text-input"
              placeholder="e.g. security-alert@verify-portal.xyz"
              value={sender}
              onChange={(e) => setSender(e.target.value)}
            />
          </div>
        </div>

        <div style={{ marginBottom: '16px' }}>
          <label className="input-label">Email Body Content</label>
          <textarea
            className="text-area"
            rows={6}
            placeholder="Paste full email body text here..."
            value={body}
            onChange={(e) => setBody(e.target.value)}
          />
        </div>

        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '18px', fontSize: '0.78rem', color: '#8E82A5' }}>
          <span>{body.length} body characters</span>
          <label style={{ display: 'flex', alignItems: 'center', gap: '6px', cursor: 'pointer', color: '#B9B1C8' }}>
            <input
              type="checkbox"
              checked={logToDb}
              onChange={(e) => setLogToDb(e.target.checked)}
              style={{ accentColor: '#8B35F6' }}
            />
            Log classification to SQLite history
          </label>
        </div>

        {error && (
          <div style={{ padding: '12px 16px', background: 'rgba(255, 83, 107, 0.15)', border: '1px solid rgba(255, 83, 107, 0.3)', borderRadius: '8px', color: '#FF8A9B', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <AlertTriangle size={16} />
            <span>{error}</span>
          </div>
        )}

        <div style={{ display: 'flex', gap: '12px' }}>
          <button
            className="btn btn-primary"
            onClick={handleAnalyze}
            disabled={loading || (!subject.trim() && !body.trim())}
            style={{ minWidth: '180px' }}
          >
            {loading ? <span className="spinner" /> : <Sparkles size={16} />}
            {loading ? 'Analyzing Email Payload...' : 'Analyze Email'}
          </button>

          <button
            className="btn btn-secondary"
            onClick={() => { setSubject(''); setSender(''); setBody(''); setResult(null); setError(null); }}
            disabled={loading || (!subject && !sender && !body && !result)}
          >
            Reset Fields
          </button>
        </div>
      </div>

      {/* Result Card */}
      {result && (
        <div className={`result-card ${result.is_spam ? 'result-spam' : 'result-ham'}`}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '12px' }}>
            <div>
              <div className={`result-badge ${result.is_spam ? 'badge-spam-lg' : 'badge-ham-lg'}`}>
                {result.is_spam ? <ShieldAlert size={24} /> : <ShieldCheck size={24} />}
                {result.label}
              </div>
              <div style={{ fontSize: '0.9rem', color: '#FFFFFF', fontWeight: 600 }}>
                Confidence Score: {(result.confidence * 100).toFixed(2)}%
              </div>
            </div>

            <button className="btn btn-secondary" onClick={copyResult}>
              {copied ? <Check size={14} color="#16D98B" /> : <Copy size={14} />}
              {copied ? 'Copied' : 'Copy Verdict'}
            </button>
          </div>

          {/* Sender Domain Analysis Card */}
          {result.heuristics?.sender_spoof_flags?.length > 0 && (
            <div style={{ marginTop: '16px', padding: '14px', background: 'rgba(255, 83, 107, 0.15)', border: '1px solid rgba(255, 83, 107, 0.35)', borderRadius: '8px' }}>
              <div style={{ fontSize: '0.82rem', fontWeight: 700, color: '#FF536B', textTransform: 'uppercase', marginBottom: '6px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                <AlertTriangle size={16} />
                Sender Header Spoofing Flags
              </div>
              <ul style={{ paddingLeft: '20px', color: '#FF8A9B', fontSize: '0.82rem' }}>
                {result.heuristics.sender_spoof_flags.map((flag, idx) => (
                  <li key={idx}>{flag}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Probability Bars */}
          <div style={{ marginTop: '20px', display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '16px' }}>
            <div style={{ background: '#100C1B', padding: '14px', borderRadius: '8px', border: '1px solid #3A2B55' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', marginBottom: '6px' }}>
                <span style={{ color: '#FF8A9B', fontWeight: 600 }}>Spam Probability</span>
                <span style={{ color: '#FFFFFF', fontWeight: 700 }}>{(result.spam_probability * 100).toFixed(2)}%</span>
              </div>
              <div className="progress-bar-bg">
                <div
                  className="progress-bar-fill"
                  style={{ width: `${result.spam_probability * 100}%`, background: '#FF536B' }}
                />
              </div>
            </div>

            <div style={{ background: '#100C1B', padding: '14px', borderRadius: '8px', border: '1px solid #3A2B55' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', marginBottom: '6px' }}>
                <span style={{ color: '#16D98B', fontWeight: 600 }}>Legitimate (Ham) Probability</span>
                <span style={{ color: '#FFFFFF', fontWeight: 700 }}>{(result.ham_probability * 100).toFixed(2)}%</span>
              </div>
              <div className="progress-bar-bg">
                <div
                  className="progress-bar-fill"
                  style={{ width: `${result.ham_probability * 100}%`, background: '#16D98B' }}
                />
              </div>
            </div>
          </div>

          {/* Lexical Details */}
          <div style={{ marginTop: '24px', paddingTop: '20px', borderTop: '1px solid rgba(58, 43, 85, 0.6)' }}>
            <div style={{ fontSize: '0.95rem', fontWeight: 700, color: '#FFFFFF', marginBottom: '12px' }}>
              Email Threat Breakdown & Advisory
            </div>

            {result.heuristics?.has_indicators ? (
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginBottom: '16px' }}>
                {Object.entries(result.heuristics.detected_triggers || {}).map(([category, items]) => (
                  <div key={category} style={{ background: '#100C1B', border: '1px solid #3A2B55', padding: '10px 14px', borderRadius: '6px' }}>
                    <div style={{ fontSize: '0.72rem', color: '#C084FC', fontWeight: 700, textTransform: 'uppercase', marginBottom: '4px' }}>
                      {category}
                    </div>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px' }}>
                      {items.map((token, idx) => (
                        <span key={idx} className="heuristic-pill">
                          {token}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div style={{ padding: '12px', background: 'rgba(22, 217, 139, 0.08)', border: '1px solid rgba(22, 217, 139, 0.25)', borderRadius: '6px', color: '#16D98B', fontSize: '0.85rem', marginBottom: '16px' }}>
                ✓ Clean lexical profile. No known malicious patterns or suspicious TLDs identified.
              </div>
            )}

            {/* Recommendations */}
            {result.heuristics?.recommendations?.length > 0 && (
              <div style={{ background: '#100C1B', border: '1px solid #3A2B55', padding: '16px', borderRadius: '8px' }}>
                <div style={{ fontSize: '0.82rem', fontWeight: 700, color: '#FFFFFF', marginBottom: '8px', textTransform: 'uppercase' }}>
                  Enterprise Mail Hygiene Recommendations
                </div>
                <ul style={{ paddingLeft: '20px', color: '#B9B1C8', fontSize: '0.82rem', lineHeight: '1.6' }}>
                  {result.heuristics.recommendations.map((rec, idx) => (
                    <li key={idx}>{rec}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
