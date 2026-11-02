/**
 * Spam Intelligence API Client SDK
 * Communicates with FastAPI serverless endpoints for real-time ML inference and analytics.
 */

const API_BASE = import.meta.env?.VITE_API_BASE_URL || '';

export async function checkHealth() {
  const res = await fetch(`${API_BASE}/api/health`);
  if (!res.ok) throw new Error(`Health check failed: ${res.statusText}`);
  return res.json();
}

export async function fetchDashboardStats() {
  const res = await fetch(`${API_BASE}/api/dashboard-stats`);
  if (!res.ok) throw new Error(`Failed to load dashboard stats: ${res.statusText}`);
  return res.json();
}

export async function predictMessage(text, messageType = 'SMS', logToDb = true) {
  const res = await fetch(`${API_BASE}/api/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      text,
      message_type: messageType,
      log_to_db: logToDb
    })
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || `Prediction failed: ${res.statusText}`);
  }
  return res.json();
}

export async function analyzeEmail({ subject, sender, body, logToDb = true }) {
  const res = await fetch(`${API_BASE}/api/email-analysis`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      subject: subject || '',
      sender: sender || '',
      body: body || '',
      log_to_db: logToDb
    })
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || `Email analysis failed: ${res.statusText}`);
  }
  return res.json();
}

export async function bulkPredict(file, textColumn = '', logToDb = false) {
  const formData = new FormData();
  formData.append('file', file);
  if (textColumn) formData.append('text_column', textColumn);
  formData.append('log_to_db', logToDb ? 'true' : 'false');

  const res = await fetch(`${API_BASE}/api/bulk-predict`, {
    method: 'POST',
    body: formData
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || `Bulk classification failed: ${res.statusText}`);
  }
  return res.json();
}

export async function fetchModelMetrics() {
  const res = await fetch(`${API_BASE}/api/model-metrics`);
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || `Failed to fetch model metrics: ${res.statusText}`);
  }
  return res.json();
}

export async function fetchHistory({ search = '', category = 'ALL', messageType = 'ALL', limit = 100 } = {}) {
  const params = new URLSearchParams();
  if (search) params.append('search', search);
  if (category && category !== 'ALL') params.append('category', category);
  if (messageType && messageType !== 'ALL') params.append('message_type', messageType);
  params.append('limit', limit.toString());

  const res = await fetch(`${API_BASE}/api/history?${params.toString()}`);
  if (!res.ok) throw new Error(`Failed to load history: ${res.statusText}`);
  return res.json();
}

export async function deleteHistoryRecord(recordId) {
  const res = await fetch(`${API_BASE}/api/history/delete`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ record_id: Number(recordId) })
  });
  if (!res.ok) throw new Error(`Failed to delete record: ${res.statusText}`);
  return res.json();
}

export async function clearAllHistory() {
  const res = await fetch(`${API_BASE}/api/history/clear`, {
    method: 'POST'
  });
  if (!res.ok) throw new Error(`Failed to clear history: ${res.statusText}`);
  return res.json();
}

export async function fetchDatasetInfo() {
  const res = await fetch(`${API_BASE}/api/dataset-info`);
  if (!res.ok) throw new Error(`Failed to load dataset info: ${res.statusText}`);
  return res.json();
}

export async function fetchSettings() {
  const res = await fetch(`${API_BASE}/api/settings`);
  if (!res.ok) throw new Error(`Failed to load settings: ${res.statusText}`);
  return res.json();
}

export async function updateSettings(settings) {
  const res = await fetch(`${API_BASE}/api/settings`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(settings)
  });
  if (!res.ok) throw new Error(`Failed to update settings: ${res.statusText}`);
  return res.json();
}
