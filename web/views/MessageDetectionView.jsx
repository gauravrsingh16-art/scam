import React, { useState } from 'react';
import { predictMessage } from '../api';
import {
  ShieldAlert,
  ShieldCheck,
  Sparkles,
  RefreshCw,
  AlertTriangle,
  ExternalLink,
  CheckCircle,
  Copy,
  Check
} from 'lucide-react';

const SAMPLES = {
  spam_lottery: 'URGENT: You have won a £1,000 cash prize or a holiday voucher! Claim immediately by calling 09050000321 or click http://prize-winner.xyz/claim. Limited time!',
  spam_bank: 'Security Alert: Your bank account has been temporarily locked due to unauthorized login attempts. Verify your identity now at https://secure-auth-update.click or services will be suspended.',
  ham_meeting: 'Hi Alex, are we still meeting tomorrow at 1:00 PM for the project architecture review? Let me know if that time still works.',
  ham_package: 'Your package with tracking number 9400100000000000000000 is scheduled for delivery today by 5:00 PM. No signature required.'
};

export function MessageDetectionView() {
  const [inputText, setInputText] = useState('');
  const [logToDb, setLogToDb] = useState(true);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [copied, setCopied] = useState(false);

  const handleClassify = async () => {
    if (!inputText.trim()) {
      setError('Please enter or paste a message to analyze.');
      return;
    }
    setError(null);
    setLoading(true);
    try {
      const response = await predictMessage(inputText, 'SMS', logToDb);
      setResult(response.data);
    } catch (err) {
      setError(err.message || 'Classification request failed.');
    } finally {
      setLoading(false);
    }
  };

  const loadSample = (key) => {
    setInputText(SAMPLES[key] || '');
    setResult(null);
    setError(null);
  };

  const copyResult = () => {
    if (!result) return;
    const text = `Spam Intelligence Verdict: ${result.label} (${(result.confidence * 100).toFixed(1)}% confidence)\nText: "${inputText}"`;
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const charCount = inputText.length;
  const wordCount = inputText.trim() ? inputText.trim().split(/\s+/).length : 0;

  return (
    <div className="page-workspace">
      {/* Header Banner */}
      <div className="welcome-banner">
        <div>
          <h2 className="welcome-title">
            Message <span className="welcome-gradient">Threat Detection</span> 💬
          </h2>
          <p className="welcome-subtitle">
            Real-time inference using Multinomial Naive Bayes & Lexical Threat Heuristics
          </p>
        </div>
      </div>

      {/* Main Input Form */}
      <div className="saas-card">
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '14px' }}>
          <span style={{ fontSize: '0.85rem', fontWeight: 700, color: '#FFFFFF', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
            Quick Test Scenarios
          </span>
          <span style={{ fontSize: '0.75rem', color: '#B9B1C8' }}>Select to prefill payload</span>
        </div>

        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginBottom: '20px' }}>
          <button className="btn btn-secondary" onClick={() => loadSample('spam_lottery')}>
            🎰 Lottery Cash Prize (Spam)
          </button>
          <button className="btn btn-secondary" onClick={() => loadSample('spam_bank')}>
            🚨 Bank Account Locked (Phishing)
          </button>
          <button className="btn btn-secondary" onClick={() => loadSample('ham_meeting')}>
            💼 Team Meeting (Ham)
          </button>
          <button className="btn btn-secondary" onClick={() => loadSample('ham_package')}>
            📦 Delivery Notification (Ham)
          </button>
        </div>

        <label className="input-label">Message Payload (SMS or Chat Text)</label>
        <textarea
          className="text-area"
          rows={5}
          placeholder="Type or paste incoming SMS / message text here to evaluate for spam, fraud, or phishing triggers..."
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
        />

        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '8px', marginBottom: '18px', fontSize: '0.78rem', color: '#8E82A5' }}>
          <span>{charCount} characters • {wordCount} words</span>
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
            onClick={handleClassify}
            disabled={loading || !inputText.trim()}
            style={{ minWidth: '180px' }}
          >
            {loading ? <span className="spinner" /> : <Sparkles size={16} />}
            {loading ? 'Executing ML Inference...' : 'Classify Message'}
          </button>

          <button
            className="btn btn-secondary"
            onClick={() => { setInputText(''); setResult(null); setError(null); }}
            disabled={loading || (!inputText && !result)}
          >
            Clear Fields
          </button>
        </div>
      </div>

      {/* Inference Result Card */}
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

          {/* Explainability & Heuristics Section */}
          <div style={{ marginTop: '24px', paddingTop: '20px', borderTop: '1px solid rgba(58, 43, 85, 0.6)' }}>
            <div style={{ fontSize: '0.95rem', fontWeight: 700, color: '#FFFFFF', marginBottom: '12px' }}>
              Lexical Analysis & Threat Indicators
            </div>

            {result.heuristics?.has_indicators ? (
              <div style={{ marginBottom: '16px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '10px' }}>
                  <span className="badge-pill badge-red">
                    Threat Score: {result.heuristics.threat_score}/100
                  </span>
                  <span style={{ fontSize: '0.8rem', color: '#B9B1C8' }}>
                    Detected suspicious patterns in text
                  </span>
                </div>

                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
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
              </div>
            ) : (
              <div style={{ padding: '12px', background: 'rgba(22, 217, 139, 0.08)', border: '1px solid rgba(22, 217, 139, 0.25)', borderRadius: '6px', color: '#16D98B', fontSize: '0.85rem', marginBottom: '16px' }}>
                ✓ No high-risk coercion, prize, or link-shortener heuristic patterns detected.
              </div>
            )}

            {/* Recommendations */}
            {result.heuristics?.recommendations?.length > 0 && (
              <div style={{ background: '#100C1B', border: '1px solid #3A2B55', padding: '16px', borderRadius: '8px', marginTop: '14px' }}>
                <div style={{ fontSize: '0.82rem', fontWeight: 700, color: '#FFFFFF', marginBottom: '8px', textTransform: 'uppercase' }}>
                  Cybersecurity Defense Advisory
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
