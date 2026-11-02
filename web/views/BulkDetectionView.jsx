import React, { useState } from 'react';
import { bulkPredict } from '../api';
import {
  Upload,
  Files,
  FileSpreadsheet,
  Download,
  AlertTriangle,
  CheckCircle,
  Filter,
  Layers,
  ShieldAlert,
  ShieldCheck,
  Search
} from 'lucide-react';

const SAMPLE_CSV_CONTENT = `text
"Congratulations! You won a guaranteed £1000 cash prize. Call 09061701461 to claim your award immediately."
"Hi Sarah, are we still having lunch at the cafeteria at 12:30?"
"URGENT! Your mobile number has been selected for a free holiday trip. Reply CLAIM to 87077."
"Can you please review the attached slide deck before our client demo at 3pm?"
"WINNER! As a valued subscriber you have been awarded a £500 gift voucher. Dial 08715203677 to collect."
"I'll be home in about 20 minutes, please keep dinner warm for me."
"Final warning: Your account has been suspended due to overdue billing. Click http://suspend-auth.xyz/verify."
"Hey dad, did you manage to get the groceries for this evening?"
"Free message: Thanks for opting in! You get 500 bonus points. Text STOP to cancel."
"The conference call was moved to Friday morning due to scheduling conflicts."`;

export function BulkDetectionView() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [textCol, setTextCol] = useState('');
  const [logToDb, setLogToDb] = useState(false);
  const [loading, setLoading] = useState(false);
  const [bulkResult, setBulkResult] = useState(null);
  const [error, setError] = useState(null);
  const [filterType, setFilterType] = useState('ALL');
  const [searchQuery, setSearchQuery] = useState('');

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
      setError(null);
    }
  };

  const handleProcessBulk = async () => {
    if (!selectedFile) {
      setError('Please select or upload a CSV/TSV file first.');
      return;
    }
    setError(null);
    setLoading(true);
    try {
      const response = await bulkPredict(selectedFile, textCol, logToDb);
      setBulkResult(response);
    } catch (err) {
      setError(err.message || 'Bulk classification failed.');
    } finally {
      setLoading(false);
    }
  };

  const loadSampleCSV = () => {
    const blob = new Blob([SAMPLE_CSV_CONTENT], { type: 'text/csv' });
    const file = new File([blob], 'sample_bulk_messages.csv', { type: 'text/csv' });
    setSelectedFile(file);
    setError(null);
  };

  const downloadSampleTemplate = () => {
    const blob = new Blob([SAMPLE_CSV_CONTENT], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'spam_detection_sample_template.csv';
    a.click();
    URL.revokeObjectURL(url);
  };

  const downloadResultsCSV = () => {
    if (!bulkResult || !bulkResult.rows || bulkResult.rows.length === 0) return;
    const columns = bulkResult.columns || Object.keys(bulkResult.rows[0]);
    const header = columns.join(',');
    const rows = bulkResult.rows.map((row) =>
      columns.map((c) => `"${String(row[c] || '').replace(/"/g, '""')}"`).join(',')
    );
    const csvContent = [header, ...rows].join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `classified_${bulkResult.filename || 'bulk_results.csv'}`;
    a.click();
    URL.revokeObjectURL(url);
  };

  // Filter rows
  const filteredRows = (bulkResult?.rows || []).filter((row) => {
    const matchesFilter =
      filterType === 'ALL' ||
      (filterType === 'SPAM' && row.Prediction === 'SPAM') ||
      (filterType === 'HAM' && row.Prediction === 'NOT SPAM');

    const matchesSearch =
      !searchQuery ||
      Object.values(row).some((val) =>
        String(val).toLowerCase().includes(searchQuery.toLowerCase())
      );

    return matchesFilter && matchesSearch;
  });

  return (
    <div className="page-workspace">
      {/* Header Banner */}
      <div className="welcome-banner">
        <div>
          <h2 className="welcome-title">
            Bulk <span className="welcome-gradient">Threat Ingestion</span> 📂
          </h2>
          <p className="welcome-subtitle">
            Vectorized high-throughput batch classification for CSV / TSV message archives
          </p>
        </div>
        <div style={{ display: 'flex', gap: '10px' }}>
          <button className="btn btn-secondary" onClick={downloadSampleTemplate}>
            <Download size={14} />
            Download Sample CSV
          </button>
          <button className="btn btn-secondary" onClick={loadSampleCSV}>
            <FileSpreadsheet size={14} />
            Load Built-In Sample
          </button>
        </div>
      </div>

      {/* Upload Box */}
      <div className="saas-card">
        <div style={{ border: '2px dashed #3A2B55', borderRadius: '10px', padding: '32px 20px', textAlign: 'center', background: 'rgba(16, 11, 29, 0.4)', transition: 'border-color 0.2s', marginBottom: '20px' }}>
          <Upload size={38} color="#8B35F6" style={{ marginBottom: '12px' }} />
          <div style={{ fontSize: '1rem', fontWeight: 700, color: '#FFFFFF', marginBottom: '4px' }}>
            {selectedFile ? selectedFile.name : 'Choose a CSV or TSV file to classify'}
          </div>
          <div style={{ fontSize: '0.8rem', color: '#B9B1C8', marginBottom: '16px' }}>
            Supports standard UTF-8 files with message columns (e.g. text, message, content, sms)
          </div>

          <label className="btn btn-secondary" style={{ cursor: 'pointer' }}>
            <span>Browse Computer</span>
            <input
              type="file"
              accept=".csv,.tsv,.txt"
              onChange={handleFileChange}
              style={{ display: 'none' }}
            />
          </label>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '16px', marginBottom: '16px' }}>
          <div>
            <label className="input-label">Text Column Name (Optional - Auto-Detected)</label>
            <input
              type="text"
              className="text-input"
              placeholder="e.g. text, message, content (Leave blank for auto)"
              value={textCol}
              onChange={(e) => setTextCol(e.target.value)}
            />
          </div>

          <div style={{ display: 'flex', alignItems: 'center' }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', color: '#B9B1C8', fontSize: '0.82rem' }}>
              <input
                type="checkbox"
                checked={logToDb}
                onChange={(e) => setLogToDb(e.target.checked)}
                style={{ accentColor: '#8B35F6' }}
              />
              Log all batch items to SQLite history
            </label>
          </div>
        </div>

        {error && (
          <div style={{ padding: '12px 16px', background: 'rgba(255, 83, 107, 0.15)', border: '1px solid rgba(255, 83, 107, 0.3)', borderRadius: '8px', color: '#FF8A9B', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <AlertTriangle size={16} />
            <span>{error}</span>
          </div>
        )}

        <button
          className="btn btn-primary"
          onClick={handleProcessBulk}
          disabled={loading || !selectedFile}
          style={{ minWidth: '200px' }}
        >
          {loading ? <span className="spinner" /> : <Layers size={16} />}
          {loading ? 'Executing Vectorized Inference...' : 'Process Batch Ingestion'}
        </button>
      </div>

      {/* Batch Summary & Table */}
      {bulkResult && (
        <div className="saas-card">
          <div className="card-title-row">
            <div>
              <div className="card-title">Batch Processing Summary: {bulkResult.filename}</div>
              <div className="card-subtitle">Processed using column: "{bulkResult.text_column}"</div>
            </div>
            <button className="btn btn-primary" onClick={downloadResultsCSV}>
              <Download size={14} />
              Export Classified CSV
            </button>
          </div>

          {/* KPI Summary Cards */}
          <div className="kpi-grid" style={{ marginBottom: '20px' }}>
            <div className="kpi-card" style={{ padding: '16px' }}>
              <div className="kpi-header">
                <span className="kpi-label">Total Processed</span>
                <Files size={16} color="#A855F7" />
              </div>
              <div className="kpi-value" style={{ fontSize: '1.6rem' }}>
                {bulkResult.summary.total}
              </div>
            </div>

            <div className="kpi-card" style={{ padding: '16px' }}>
              <div className="kpi-header">
                <span className="kpi-label">Spam Intercepted</span>
                <ShieldAlert size={16} color="#FF536B" />
              </div>
              <div className="kpi-value" style={{ fontSize: '1.6rem', color: '#FF536B' }}>
                {bulkResult.summary.spam_count}
              </div>
              <div className="kpi-subtext">{bulkResult.summary.spam_rate}% threat rate</div>
            </div>

            <div className="kpi-card" style={{ padding: '16px' }}>
              <div className="kpi-header">
                <span className="kpi-label">Legitimate Clean</span>
                <ShieldCheck size={16} color="#16D98B" />
              </div>
              <div className="kpi-value" style={{ fontSize: '1.6rem', color: '#16D98B' }}>
                {bulkResult.summary.ham_count}
              </div>
              <div className="kpi-subtext">
                {(100 - bulkResult.summary.spam_rate).toFixed(1)}% clean traffic
              </div>
            </div>

            <div className="kpi-card" style={{ padding: '16px' }}>
              <div className="kpi-header">
                <span className="kpi-label">Avg Confidence</span>
                <Layers size={16} color="#C084FC" />
              </div>
              <div className="kpi-value" style={{ fontSize: '1.6rem' }}>
                {bulkResult.summary.avg_confidence}%
              </div>
              <div className="kpi-subtext">Vectorized batch speed</div>
            </div>
          </div>

          {/* Filter Bar */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '12px', marginBottom: '16px', flexWrap: 'wrap' }}>
            <div style={{ display: 'flex', gap: '8px' }}>
              {['ALL', 'SPAM', 'HAM'].map((t) => (
                <button
                  key={t}
                  className={`btn ${filterType === t ? 'btn-primary' : 'btn-secondary'}`}
                  style={{ padding: '6px 12px', fontSize: '0.78rem' }}
                  onClick={() => setFilterType(t)}
                >
                  {t}
                </button>
              ))}
            </div>

            <div style={{ position: 'relative', minWidth: '220px' }}>
              <Search size={14} style={{ position: 'absolute', left: '10px', top: '10px', color: '#8E82A5' }} />
              <input
                type="text"
                className="text-input"
                style={{ paddingLeft: '32px', paddingTop: '6px', paddingBottom: '6px', fontSize: '0.8rem' }}
                placeholder="Search rows..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
          </div>

          {/* Table */}
          <div className="data-table-container">
            <table className="data-table">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Verdict</th>
                  <th>Confidence</th>
                  <th>Spam Prob</th>
                  <th>Message Preview</th>
                </tr>
              </thead>
              <tbody>
                {filteredRows.map((row, idx) => {
                  const isSpam = row.Prediction === 'SPAM';
                  const textVal = row[bulkResult.text_column] || Object.values(row)[0] || '';
                  return (
                    <tr key={idx}>
                      <td style={{ color: '#8E82A5', fontFamily: 'monospace' }}>{idx + 1}</td>
                      <td>
                        <span className={`badge-pill ${isSpam ? 'badge-red' : 'badge-green'}`} style={{ padding: '2px 8px', fontSize: '0.72rem' }}>
                          {isSpam ? '● SPAM' : '● NOT SPAM'}
                        </span>
                      </td>
                      <td style={{ fontWeight: 600, color: '#FFFFFF' }}>
                        {(Number(row.Confidence) * 100).toFixed(1)}%
                      </td>
                      <td style={{ color: '#FF8A9B' }}>
                        {(Number(row.Spam_Probability || 0) * 100).toFixed(1)}%
                      </td>
                      <td style={{ color: '#B9B1C8', maxWidth: '400px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                        {String(textVal)}
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
