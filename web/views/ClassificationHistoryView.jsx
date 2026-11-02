import React, { useState, useEffect } from 'react';
import { fetchHistory, deleteHistoryRecord, clearAllHistory } from '../api';
import {
  History,
  Trash2,
  Search,
  Filter,
  Download,
  RefreshCw,
  AlertTriangle,
  CheckCircle,
  FileText
} from 'lucide-react';

export function ClassificationHistoryView() {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('ALL');
  const [messageType, setMessageType] = useState('ALL');

  const loadHistory = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetchHistory({ search, category, messageType, limit: 200 });
      setRecords(res.records || []);
    } catch (err) {
      setError(err.message || 'Failed loading classification audit history.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadHistory();
  }, [category, messageType]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    loadHistory();
  };

  const handleDelete = async (id) => {
    if (!window.confirm(`Delete classification record #${id}?`)) return;
    try {
      await deleteHistoryRecord(id);
      setRecords((prev) => prev.filter((r) => r.id !== id));
    } catch (err) {
      alert(`Error deleting record: ${err.message}`);
    }
  };

  const handleClearAll = async () => {
    if (!window.confirm('Are you sure you want to purge all classification audit history records? This cannot be undone.')) return;
    try {
      await clearAllHistory();
      setRecords([]);
    } catch (err) {
      alert(`Error clearing history: ${err.message}`);
    }
  };

  const exportHistoryCSV = () => {
    if (records.length === 0) return;
    const header = ['ID', 'Timestamp', 'Message Type', 'Prediction', 'Confidence', 'Character Count', 'Vectorizer', 'Preview'];
    const rows = records.map((r) => [
      r.id,
      `"${r.timestamp}"`,
      `"${r.message_type}"`,
      `"${r.prediction}"`,
      r.confidence,
      r.char_count,
      `"${r.vectorizer_used}"`,
      `"${(r.text_preview || '').replace(/"/g, '""')}"`
    ]);
    const csvContent = [header.join(','), ...rows.map((row) => row.join(','))].join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `spam_intelligence_history_${Date.now()}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="page-workspace">
      {/* Header Banner */}
      <div className="welcome-banner">
        <div>
          <h2 className="welcome-title">
            Classification <span className="welcome-gradient">Audit History</span> 📜
          </h2>
          <p className="welcome-subtitle">
            Immutable SQLite audit trail with granular privacy sanitization and compliance tracking
          </p>
        </div>
        <div style={{ display: 'flex', gap: '10px' }}>
          <button className="btn btn-secondary" onClick={exportHistoryCSV} disabled={records.length === 0}>
            <Download size={14} />
            Export Audit CSV
          </button>
          <button className="btn btn-danger" onClick={handleClearAll} disabled={records.length === 0}>
            <Trash2 size={14} />
            Purge History
          </button>
        </div>
      </div>

      {error && (
        <div style={{ padding: '14px 18px', background: 'rgba(255, 83, 107, 0.15)', border: '1px solid rgba(255, 83, 107, 0.3)', borderRadius: '8px', color: '#FF8A9B', marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '10px' }}>
          <AlertTriangle size={18} />
          <span>{error}</span>
        </div>
      )}

      {/* Filter and Search Bar */}
      <div className="saas-card" style={{ padding: '16px 20px', marginBottom: '20px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '14px' }}>
          <form onSubmit={handleSearchSubmit} style={{ display: 'flex', gap: '8px', flex: 1, minWidth: '260px' }}>
            <div style={{ position: 'relative', width: '100%' }}>
              <Search size={14} style={{ position: 'absolute', left: '12px', top: '12px', color: '#8E82A5' }} />
              <input
                type="text"
                className="text-input"
                style={{ paddingLeft: '34px' }}
                placeholder="Search audit records by preview text or ID..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>
            <button type="submit" className="btn btn-secondary">
              Search
            </button>
          </form>

          <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <span style={{ fontSize: '0.75rem', color: '#B9B1C8', textTransform: 'uppercase' }}>Verdict:</span>
              <select
                className="select-input"
                style={{ width: 'auto', padding: '8px 12px', fontSize: '0.8rem' }}
                value={category}
                onChange={(e) => setCategory(e.target.value)}
              >
                <option value="ALL">All Verdicts</option>
                <option value="SPAM">Spam Only</option>
                <option value="HAM">Not Spam Only</option>
              </select>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <span style={{ fontSize: '0.75rem', color: '#B9B1C8', textTransform: 'uppercase' }}>Channel:</span>
              <select
                className="select-input"
                style={{ width: 'auto', padding: '8px 12px', fontSize: '0.8rem' }}
                value={messageType}
                onChange={(e) => setMessageType(e.target.value)}
              >
                <option value="ALL">All Channels</option>
                <option value="SMS">SMS</option>
                <option value="Email">Email</option>
                <option value="Bulk">Bulk</option>
              </select>
            </div>

            <button className="btn btn-secondary" onClick={loadHistory} disabled={loading}>
              <RefreshCw size={14} className={loading ? 'spinner' : ''} />
            </button>
          </div>
        </div>
      </div>

      {/* History Table */}
      <div className="saas-card">
        <div className="card-title-row">
          <div>
            <div className="card-title">Audit Log Entries ({records.length} records)</div>
            <div className="card-subtitle">Showing latest records from SQLite database</div>
          </div>
        </div>

        {records.length > 0 ? (
          <div className="data-table-container">
            <table className="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Timestamp</th>
                  <th>Channel</th>
                  <th>Verdict</th>
                  <th>Confidence</th>
                  <th>Chars</th>
                  <th>Preview Snippet</th>
                  <th style={{ textAlign: 'right' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {records.map((r) => {
                  const isSpam = r.prediction === 'SPAM';
                  return (
                    <tr key={r.id}>
                      <td style={{ fontFamily: 'monospace', color: '#8E82A5' }}>#{r.id}</td>
                      <td style={{ color: '#B9B1C8', whiteSpace: 'nowrap' }}>{r.timestamp}</td>
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
                      <td style={{ color: '#8E82A5' }}>{r.char_count}</td>
                      <td style={{ color: '#B9B1C8', maxWidth: '320px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                        {r.text_preview || <span style={{ color: '#64748B', fontStyle: 'italic' }}>— [preview disabled] —</span>}
                      </td>
                      <td style={{ textAlign: 'right' }}>
                        <button
                          onClick={() => handleDelete(r.id)}
                          style={{ background: 'transparent', border: 'none', color: '#FF536B', cursor: 'pointer', padding: '4px' }}
                          title="Delete Record"
                        >
                          <Trash2 size={15} />
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        ) : (
          <div style={{ textAlign: 'center', padding: '40px 16px', color: '#8E82A5' }}>
            <History size={36} style={{ marginBottom: '10px', opacity: 0.4 }} />
            <p>No classification records found matching the active filters.</p>
          </div>
        )}
      </div>
    </div>
  );
}
