import React, { useState, useEffect } from 'react';
import { fetchSettings, updateSettings } from '../api';
import {
  Settings,
  Shield,
  Eye,
  Database,
  RefreshCw,
  CheckCircle2,
  AlertTriangle,
  HardDrive,
  Cpu
} from 'lucide-react';

export function SettingsView({ apiHealth }) {
  const [historyEnabled, setHistoryEnabled] = useState(true);
  const [storePreviews, setStorePreviews] = useState(false);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saveMessage, setSaveMessage] = useState(null);
  const [error, setError] = useState(null);

  const loadSettingsData = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetchSettings();
      setHistoryEnabled(res.history_enabled);
      setStorePreviews(res.store_previews);
    } catch (err) {
      setError(err.message || 'Failed loading settings.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSettingsData();
  }, []);

  const handleSave = async () => {
    setSaving(true);
    setSaveMessage(null);
    try {
      const res = await updateSettings({
        history_enabled: historyEnabled,
        store_previews: storePreviews
      });
      setHistoryEnabled(res.history_enabled);
      setStorePreviews(res.store_previews);
      setSaveMessage('Privacy preferences saved successfully.');
      setTimeout(() => setSaveMessage(null), 3000);
    } catch (err) {
      setError(err.message || 'Failed saving settings.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="page-workspace">
      {/* Header Banner */}
      <div className="welcome-banner">
        <div>
          <h2 className="welcome-title">
            System <span className="welcome-gradient">Settings & Privacy</span> ⚙
          </h2>
          <p className="welcome-subtitle">
            Configure privacy controls, audit logging preferences, and system parameters
          </p>
        </div>
        <button
          className="btn btn-primary"
          onClick={handleSave}
          disabled={saving || loading}
          style={{ minWidth: '160px' }}
        >
          {saving ? <span className="spinner" /> : <CheckCircle2 size={14} />}
          {saving ? 'Saving...' : 'Save Changes'}
        </button>
      </div>

      {saveMessage && (
        <div style={{ padding: '14px 18px', background: 'rgba(22, 217, 139, 0.15)', border: '1px solid rgba(22, 217, 139, 0.35)', borderRadius: '8px', color: '#16D98B', marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '10px' }}>
          <CheckCircle2 size={18} />
          <span>{saveMessage}</span>
        </div>
      )}

      {error && (
        <div style={{ padding: '14px 18px', background: 'rgba(255, 83, 107, 0.15)', border: '1px solid rgba(255, 83, 107, 0.3)', borderRadius: '8px', color: '#FF8A9B', marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '10px' }}>
          <AlertTriangle size={18} />
          <span>{error}</span>
        </div>
      )}

      {/* Privacy Settings Card */}
      <div className="saas-card">
        <div className="card-title-row">
          <div>
            <div className="card-title">Privacy & Classification History</div>
            <div className="card-subtitle">Granular data retention and privacy controls</div>
          </div>
          <span className="badge-pill badge-purple">Privacy First</span>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '18px', marginTop: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '14px 18px', background: '#100C1B', border: '1px solid #3A2B55', borderRadius: '8px' }}>
            <div>
              <div style={{ fontWeight: 600, color: '#FFFFFF', fontSize: '0.9rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Database size={16} color="#8B35F6" />
                Audit Trail Logging
              </div>
              <div style={{ fontSize: '0.78rem', color: '#B9B1C8', marginTop: '2px' }}>
                Log incoming classification verdicts, timestamps, and confidence scores into SQLite.
              </div>
            </div>
            <label style={{ position: 'relative', display: 'inline-block', width: '44px', height: '24px' }}>
              <input
                type="checkbox"
                checked={historyEnabled}
                onChange={(e) => setHistoryEnabled(e.target.checked)}
                style={{ width: '100%', height: '100%', cursor: 'pointer', accentColor: '#8B35F6' }}
              />
            </label>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '14px 18px', background: '#100C1B', border: '1px solid #3A2B55', borderRadius: '8px' }}>
            <div>
              <div style={{ fontWeight: 600, color: '#FFFFFF', fontSize: '0.9rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Eye size={16} color="#A855F7" />
                Store Sanitized Message Previews
              </div>
              <div style={{ fontSize: '0.78rem', color: '#B9B1C8', marginTop: '2px' }}>
                When enabled, saves a truncated 60-character preview in history. When disabled, zero message content is retained.
              </div>
            </div>
            <label style={{ position: 'relative', display: 'inline-block', width: '44px', height: '24px' }}>
              <input
                type="checkbox"
                checked={storePreviews}
                onChange={(e) => setStorePreviews(e.target.checked)}
                style={{ width: '100%', height: '100%', cursor: 'pointer', accentColor: '#8B35F6' }}
              />
            </label>
          </div>
        </div>
      </div>

      {/* System Telemetry & Paths */}
      <div className="saas-card">
        <div className="card-title-row">
          <div>
            <div className="card-title">Serverless Runtime Telemetry</div>
            <div className="card-subtitle">Active environment and model artifact verification</div>
          </div>
          <span className="badge-pill badge-green">Healthy</span>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginTop: '14px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 14px', background: '#100C1B', borderRadius: '6px', border: '1px solid #3A2B55' }}>
            <span style={{ color: '#B9B1C8', fontSize: '0.85rem' }}>Service Name</span>
            <span style={{ color: '#FFFFFF', fontWeight: 600, fontSize: '0.85rem' }}>
              {apiHealth?.service || 'Spam Intelligence AI Defense Engine'}
            </span>
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 14px', background: '#100C1B', borderRadius: '6px', border: '1px solid #3A2B55' }}>
            <span style={{ color: '#B9B1C8', fontSize: '0.85rem' }}>Model Status</span>
            <span style={{ color: apiHealth?.model_loaded ? '#16D98B' : '#FF536B', fontWeight: 600, fontSize: '0.85rem' }}>
              {apiHealth?.model_loaded ? '✓ Model Loaded (models/spam_model.pkl)' : '✗ Not Loaded'}
            </span>
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 14px', background: '#100C1B', borderRadius: '6px', border: '1px solid #3A2B55' }}>
            <span style={{ color: '#B9B1C8', fontSize: '0.85rem' }}>Vectorizer Pipeline</span>
            <span style={{ color: apiHealth?.vectorizer_path_exists ? '#16D98B' : '#FF536B', fontWeight: 600, fontSize: '0.85rem' }}>
              {apiHealth?.vectorizer_path_exists ? '✓ Serialized TF-IDF (models/vectorizer.pkl)' : '✗ Missing'}
            </span>
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 14px', background: '#100C1B', borderRadius: '6px', border: '1px solid #3A2B55' }}>
            <span style={{ color: '#B9B1C8', fontSize: '0.85rem' }}>Database File Location</span>
            <span style={{ color: '#C084FC', fontFamily: 'monospace', fontSize: '0.8rem' }}>
              {apiHealth?.database_path || 'data/classification_history.db'}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
