import React, { useState, useEffect } from 'react';
import { fetchDatasetInfo } from '../api';
import {
  Database,
  FileSpreadsheet,
  Layers,
  Sparkles,
  RefreshCw,
  AlertTriangle,
  CheckCircle2
} from 'lucide-react';

export function DatasetManagementView() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadDataset = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetchDatasetInfo();
      setData(res);
    } catch (err) {
      setError(err.message || 'Failed loading dataset info.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDataset();
  }, []);

  const total = data?.total_rows || 5572;
  const hamCount = data?.ham_count || 4825;
  const spamCount = data?.spam_count || 747;
  const spamPct = data?.spam_percentage || 13.4;
  const hamPct = data?.ham_percentage || 86.6;

  return (
    <div className="page-workspace">
      {/* Header Banner */}
      <div className="welcome-banner">
        <div>
          <h2 className="welcome-title">
            Dataset <span className="welcome-gradient">Management & Corpus</span> 🗄
          </h2>
          <p className="welcome-subtitle">
            Ground-truth training corpus distribution and text preprocessing telemetry
          </p>
        </div>
        <button className="btn btn-secondary" onClick={loadDataset} disabled={loading}>
          <RefreshCw size={14} className={loading ? 'spinner' : ''} />
          Refresh Corpus Data
        </button>
      </div>

      {error && (
        <div style={{ padding: '14px 18px', background: 'rgba(255, 83, 107, 0.15)', border: '1px solid rgba(255, 83, 107, 0.3)', borderRadius: '8px', color: '#FF8A9B', marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '10px' }}>
          <AlertTriangle size={18} />
          <span>{error}</span>
        </div>
      )}

      {/* Dataset Statistics Grid */}
      <div className="kpi-grid">
        <div className="kpi-card">
          <div className="kpi-header">
            <span className="kpi-label">Total Corpus Rows</span>
            <div className="kpi-icon-wrapper" style={{ background: 'rgba(139, 53, 246, 0.15)', color: '#A855F7' }}>
              <Database size={18} />
            </div>
          </div>
          <div className="kpi-value">{total.toLocaleString()}</div>
          <div className="kpi-subtext">Source: SMS Spam Collection Dataset</div>
        </div>

        <div className="kpi-card">
          <div className="kpi-header">
            <span className="kpi-label">Legitimate (Ham)</span>
            <div className="kpi-icon-wrapper" style={{ background: 'rgba(22, 217, 139, 0.15)', color: '#16D98B' }}>
              <CheckCircle2 size={18} />
            </div>
          </div>
          <div className="kpi-value" style={{ color: '#16D98B' }}>
            {hamCount.toLocaleString()}
          </div>
          <div className="kpi-subtext">{hamPct}% of corpus</div>
        </div>

        <div className="kpi-card">
          <div className="kpi-header">
            <span className="kpi-label">Malicious (Spam)</span>
            <div className="kpi-icon-wrapper" style={{ background: 'rgba(255, 83, 107, 0.15)', color: '#FF536B' }}>
              <AlertTriangle size={18} />
            </div>
          </div>
          <div className="kpi-value" style={{ color: '#FF536B' }}>
            {spamCount.toLocaleString()}
          </div>
          <div className="kpi-subtext">{spamPct}% class imbalance</div>
        </div>

        <div className="kpi-card">
          <div className="kpi-header">
            <span className="kpi-label">Dataset File</span>
            <div className="kpi-icon-wrapper" style={{ background: 'rgba(192, 132, 252, 0.15)', color: '#C084FC' }}>
              <FileSpreadsheet size={18} />
            </div>
          </div>
          <div className="kpi-value" style={{ fontSize: '1.25rem', marginTop: '6px' }}>
            {data?.filename || 'cleaned_dataset.csv'}
          </div>
          <div className="kpi-subtext">Preprocessed and validated</div>
        </div>
      </div>

      {/* Preprocessing Pipeline Information */}
      <div className="saas-card">
        <div className="card-title-row">
          <div>
            <div className="card-title">NLP Preprocessing Pipeline Architecture</div>
            <div className="card-subtitle">Deterministic transformation applied identically during training and inference</div>
          </div>
          <span className="badge-pill badge-purple">Zero Data Leakage</span>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '14px', marginTop: '12px' }}>
          <div style={{ background: '#100C1B', border: '1px solid #3A2B55', padding: '14px', borderRadius: '8px' }}>
            <div style={{ color: '#C084FC', fontWeight: 700, fontSize: '0.82rem', marginBottom: '4px' }}>
              1. Case Normalization
            </div>
            <div style={{ color: '#B9B1C8', fontSize: '0.78rem' }}>
              Lowercases all characters while computing the uppercase ratio as a separate heuristic feature.
            </div>
          </div>

          <div style={{ background: '#100C1B', border: '1px solid #3A2B55', padding: '14px', borderRadius: '8px' }}>
            <div style={{ color: '#C084FC', fontWeight: 700, fontSize: '0.82rem', marginBottom: '4px' }}>
              2. URL Masking
            </div>
            <div style={{ color: '#B9B1C8', fontSize: '0.78rem' }}>
              Replaces links with canonical token <code style={{ color: '#16D98B' }}>url_link</code> to preserve phishing signal.
            </div>
          </div>

          <div style={{ background: '#100C1B', border: '1px solid #3A2B55', padding: '14px', borderRadius: '8px' }}>
            <div style={{ color: '#C084FC', fontWeight: 700, fontSize: '0.82rem', marginBottom: '4px' }}>
              3. Currency Normalization
            </div>
            <div style={{ color: '#B9B1C8', fontSize: '0.78rem' }}>
              Transforms £, $, € symbols into unified <code style={{ color: '#16D98B' }}>currency_symbol</code> tokens.
            </div>
          </div>

          <div style={{ background: '#100C1B', border: '1px solid #3A2B55', padding: '14px', borderRadius: '8px' }}>
            <div style={{ color: '#C084FC', fontWeight: 700, fontSize: '0.82rem', marginBottom: '4px' }}>
              4. TF-IDF Vectorization
            </div>
            <div style={{ color: '#B9B1C8', fontSize: '0.78rem' }}>
              Constructs 1,000 sublinear TF-IDF features with unigram & bigram vocabulary extraction.
            </div>
          </div>
        </div>
      </div>

      {/* Dataset Sample Table */}
      {data?.sample_rows?.length > 0 && (
        <div className="saas-card">
          <div className="card-title-row">
            <div>
              <div className="card-title">Corpus Data Inspection (Sample Rows)</div>
              <div className="card-subtitle">Exemplar rows from the active training collection</div>
            </div>
          </div>

          <div className="data-table-container">
            <table className="data-table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Ground Truth Label</th>
                  <th>Raw Message Content</th>
                </tr>
              </thead>
              <tbody>
                {data.sample_rows.map((row, idx) => {
                  const label = String(row.label || row.v1 || '').toUpperCase();
                  const isSpam = label === 'SPAM' || label === '1';
                  const text = row.text || row.message || row.v2 || Object.values(row)[1] || '';
                  return (
                    <tr key={idx}>
                      <td style={{ color: '#8E82A5', fontFamily: 'monospace' }}>{idx + 1}</td>
                      <td>
                        <span className={`badge-pill ${isSpam ? 'badge-red' : 'badge-green'}`} style={{ padding: '2px 8px', fontSize: '0.72rem' }}>
                          {isSpam ? '● SPAM' : '● HAM'}
                        </span>
                      </td>
                      <td style={{ color: '#B9B1C8', maxWidth: '500px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                        {String(text)}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
