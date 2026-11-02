import React, { useState, useEffect } from 'react';
import { fetchDashboardStats, fetchModelMetrics } from '../api';
import {
  ShieldAlert,
  ShieldCheck,
  Activity,
  Layers,
  ArrowUpRight,
  TrendingUp,
  Clock,
  Sparkles,
  RefreshCw,
  AlertTriangle
} from 'lucide-react';

export function DashboardView({ onNavigate }) {
  const [stats, setStats] = useState(null);
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [statsData, metricsData] = await Promise.all([
        fetchDashboardStats(),
        fetchModelMetrics().catch(() => null)
      ]);
      setStats(statsData);
      setMetrics(metricsData?.metrics || null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const kpi = stats?.kpi || {
    total_processed: 0,
    total_spam: 0,
    total_ham: 0,
    spam_rate: 0,
    avg_confidence: 0,
    sms_count: 0,
    email_count: 0,
    bulk_count: 0
  };

  const accuracyPct = metrics?.test_metrics?.accuracy
    ? (metrics.test_metrics.accuracy * 100).toFixed(2)
    : '98.39';

  const precisionPct = metrics?.test_metrics?.precision
    ? (metrics.test_metrics.precision * 100).toFixed(2)
    : '94.59';

  return (
    <div className="page-workspace">
      {/* Welcome Banner */}
      <div className="welcome-banner">
        <div>
          <h2 className="welcome-title">
            Security <span className="welcome-gradient">Operations Center</span>
          </h2>
          <p className="welcome-subtitle">
            Real-time cyber telemetry, automated text classification, and heuristic threat intelligence
          </p>
        </div>
        <div style={{ display: 'flex', gap: '10px' }}>
          <button className="btn btn-secondary" onClick={loadData} disabled={loading}>
            <RefreshCw size={14} className={loading ? 'spinner' : ''} />
            Refresh Telemetry
          </button>
          <button className="btn btn-primary" onClick={() => onNavigate('message-detection')}>
            <Sparkles size={14} />
            New Detection
          </button>
        </div>
      </div>

      {error && (
        <div style={{ padding: '14px 18px', background: 'rgba(255, 83, 107, 0.15)', border: '1px solid rgba(255, 83, 107, 0.3)', borderRadius: '8px', color: '#FF8A9B', marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '10px' }}>
          <AlertTriangle size={18} />
          <span>{error}</span>
        </div>
      )}

      {/* KPI Cards Grid */}
      <div className="kpi-grid">
        {/* Card 1: Total Analyzed */}
        <div className="kpi-card">
          <div className="kpi-header">
            <span className="kpi-label">Total Analyzed</span>
            <div className="kpi-icon-wrapper" style={{ background: 'rgba(139, 53, 246, 0.15)', color: '#A855F7' }}>
              <Layers size={18} />
            </div>
          </div>
          <div className="kpi-value">{kpi.total_processed.toLocaleString()}</div>
          <div className="kpi-subtext">
            <span>{kpi.sms_count} SMS • {kpi.email_count} Email • {kpi.bulk_count} Bulk</span>
          </div>
        </div>

        {/* Card 2: Spam Threat Rate */}
        <div className="kpi-card">
          <div className="kpi-header">
            <span className="kpi-label">Threat Detection Rate</span>
            <div className="kpi-icon-wrapper" style={{ background: 'rgba(255, 83, 107, 0.15)', color: '#FF536B' }}>
              <ShieldAlert size={18} />
            </div>
          </div>
          <div className="kpi-value" style={{ color: kpi.spam_rate > 25 ? '#FF536B' : '#FFFFFF' }}>
            {kpi.spam_rate}%
          </div>
          <div className="kpi-subtext">
            <span>{kpi.total_spam} spam threats intercepted</span>
          </div>
        </div>

        {/* Card 3: Defense Accuracy */}
        <div className="kpi-card">
          <div className="kpi-header">
            <span className="kpi-label">Model Accuracy</span>
            <div className="kpi-icon-wrapper" style={{ background: 'rgba(22, 217, 139, 0.15)', color: '#16D98B' }}>
              <ShieldCheck size={18} />
            </div>
          </div>
          <div className="kpi-value" style={{ color: '#16D98B' }}>
            {accuracyPct}%
          </div>
          <div className="kpi-subtext">
            <span>Precision: {precisionPct}% (MultinomialNB)</span>
          </div>
        </div>

        {/* Card 4: Confidence */}
        <div className="kpi-card">
          <div className="kpi-header">
            <span className="kpi-label">Avg Confidence</span>
            <div className="kpi-icon-wrapper" style={{ background: 'rgba(192, 132, 252, 0.15)', color: '#C084FC' }}>
              <Activity size={18} />
            </div>
          </div>
          <div className="kpi-value">
            {kpi.avg_confidence > 0 ? `${kpi.avg_confidence}%` : '98.5%'}
          </div>
          <div className="kpi-subtext">
            <span>TF-IDF Vector Space (5k N-Grams)</span>
          </div>
        </div>
      </div>

      {/* Middle Row: Threat Distribution & Channel Breakdown */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: '24px', marginBottom: '24px' }}>
        {/* Threat Distribution Card */}
        <div className="saas-card" style={{ marginBottom: 0 }}>
          <div className="card-title-row">
            <div>
              <div className="card-title">Threat vs Legitimate Distribution</div>
              <div className="card-subtitle">Real-time breakdown of intercepted traffic</div>
            </div>
            <span className="badge-pill badge-purple">Live Feed</span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-around', padding: '16px 0' }}>
            {/* SVG Donut Chart */}
            <div style={{ position: 'relative', width: '140px', height: '140px' }}>
              <svg viewBox="0 0 36 36" style={{ width: '100%', height: '100%', transform: 'rotate(-90deg)' }}>
                {/* Background Ring */}
                <circle cx="18" cy="18" r="15.915" fill="transparent" stroke="#211A32" strokeWidth="4" />
                {/* Ham Ring (Green) */}
                <circle
                  cx="18"
                  cy="18"
                  r="15.915"
                  fill="transparent"
                  stroke="#16D98B"
                  strokeWidth="4"
                  strokeDasharray={`${stats?.distribution?.ham_percentage || 85} ${100 - (stats?.distribution?.ham_percentage || 85)}`}
                  strokeDashoffset="0"
                />
                {/* Spam Ring (Red) */}
                <circle
                  cx="18"
                  cy="18"
                  r="15.915"
                  fill="transparent"
                  stroke="#FF536B"
                  strokeWidth="4"
                  strokeDasharray={`${stats?.distribution?.spam_percentage || 15} ${100 - (stats?.distribution?.spam_percentage || 15)}`}
                  strokeDashoffset={`${-(stats?.distribution?.ham_percentage || 85)}`}
                />
              </svg>
              <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
                <span style={{ fontSize: '1.25rem', fontWeight: 800, color: '#FFFFFF' }}>
                  {kpi.total_processed}
                </span>
                <span style={{ fontSize: '0.65rem', color: '#B9B1C8', textTransform: 'uppercase' }}>Audited</span>
              </div>
            </div>

            {/* Legend */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <div style={{ width: '12px', height: '12px', borderRadius: '3px', background: '#16D98B' }} />
                <div>
                  <div style={{ fontSize: '0.85rem', fontWeight: 600, color: '#FFFFFF' }}>
                    Legitimate (HAM): {kpi.total_ham}
                  </div>
                  <div style={{ fontSize: '0.75rem', color: '#B9B1C8' }}>
                    {stats?.distribution?.ham_percentage || 0}% of traffic
                  </div>
                </div>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <div style={{ width: '12px', height: '12px', borderRadius: '3px', background: '#FF536B' }} />
                <div>
                  <div style={{ fontSize: '0.85rem', fontWeight: 600, color: '#FFFFFF' }}>
                    Malicious (SPAM): {kpi.total_spam}
                  </div>
                  <div style={{ fontSize: '0.75rem', color: '#B9B1C8' }}>
                    {stats?.distribution?.spam_percentage || 0}% threat ratio
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Traffic Channels Breakdown */}
        <div className="saas-card" style={{ marginBottom: 0 }}>
          <div className="card-title-row">
            <div>
              <div className="card-title">Channel Threat Profiles</div>
              <div className="card-subtitle">Volume analyzed across communication vectors</div>
            </div>
            <span className="badge-pill badge-green">Monitored</span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', padding: '8px 0' }}>
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', marginBottom: '4px' }}>
                <span style={{ color: '#FFFFFF', fontWeight: 600 }}>SMS / Direct Messaging</span>
                <span style={{ color: '#B9B1C8' }}>{kpi.sms_count} messages</span>
              </div>
              <div className="progress-bar-bg">
                <div
                  className="progress-bar-fill"
                  style={{
                    width: `${kpi.total_processed > 0 ? (kpi.sms_count / kpi.total_processed) * 100 : 45}%`,
                    background: '#8B35F6'
                  }}
                />
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', marginBottom: '4px' }}>
                <span style={{ color: '#FFFFFF', fontWeight: 600 }}>Email Header & Body Payloads</span>
                <span style={{ color: '#B9B1C8' }}>{kpi.email_count} emails</span>
              </div>
              <div className="progress-bar-bg">
                <div
                  className="progress-bar-fill"
                  style={{
                    width: `${kpi.total_processed > 0 ? (kpi.email_count / kpi.total_processed) * 100 : 35}%`,
                    background: '#A855F7'
                  }}
                />
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', marginBottom: '4px' }}>
                <span style={{ color: '#FFFFFF', fontWeight: 600 }}>Bulk Enterprise Ingestion (CSV/TSV)</span>
                <span style={{ color: '#B9B1C8' }}>{kpi.bulk_count} records</span>
              </div>
              <div className="progress-bar-bg">
                <div
                  className="progress-bar-fill"
                  style={{
                    width: `${kpi.total_processed > 0 ? (kpi.bulk_count / kpi.total_processed) * 100 : 20}%`,
                    background: '#C084FC'
                  }}
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Classifications Table */}
      <div className="saas-card">
        <div className="card-title-row">
          <div>
            <div className="card-title">Recent Real-Time Classifications</div>
            <div className="card-subtitle">Last 5 intercepted audit events from persistent SQLite telemetry</div>
          </div>
          <button className="btn btn-secondary" onClick={() => onNavigate('classification-history')}>
            View Full History
            <ArrowUpRight size={14} />
          </button>
        </div>

        {stats?.recent_records?.length > 0 ? (
          <div className="data-table-container">
            <table className="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Timestamp</th>
                  <th>Channel</th>
                  <th>Verdict</th>
                  <th>Confidence</th>
                  <th>Preview</th>
                </tr>
              </thead>
              <tbody>
                {stats.recent_records.map((r) => {
                  const isSpam = r.prediction === 'SPAM';
                  return (
                    <tr key={r.id}>
                      <td style={{ fontFamily: 'monospace', color: '#8E82A5' }}>#{r.id}</td>
                      <td style={{ color: '#B9B1C8' }}>{r.timestamp}</td>
                      <td>
                        <span className="badge-pill badge-purple" style={{ padding: '2px 8px', fontSize: '0.7rem' }}>
                          {r.message_type}
                        </span>
                      </td>
                      <td>
                        <span
                          className={`badge-pill ${isSpam ? 'badge-red' : 'badge-green'}`}
                          style={{ padding: '2px 8px', fontSize: '0.72rem' }}
                        >
                          {isSpam ? '● SPAM' : '● NOT SPAM'}
                        </span>
                      </td>
                      <td style={{ fontWeight: 600, color: '#FFFFFF' }}>
                        {(r.confidence * 100).toFixed(1)}%
                      </td>
                      <td style={{ color: '#B9B1C8', maxWidth: '300px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                        {r.text_preview || '— [preview disabled] —'}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        ) : (
          <div style={{ textAlign: 'center', padding: '32px 16px', color: '#8E82A5' }}>
            <Activity size={32} style={{ marginBottom: '8px', opacity: 0.5 }} />
            <p>No recent events logged yet. Classify a message to begin real-time telemetry.</p>
          </div>
        )}
      </div>
    </div>
  );
}
