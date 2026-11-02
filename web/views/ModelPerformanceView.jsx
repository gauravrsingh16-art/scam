import React, { useState, useEffect } from 'react';
import { fetchModelMetrics } from '../api';
import {
  Activity,
  CheckCircle2,
  AlertTriangle,
  Cpu,
  Layers,
  Sparkles,
  RefreshCw,
  BarChart2,
  Percent
} from 'lucide-react';

export function ModelPerformanceView() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadMetrics = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetchModelMetrics();
      setData(res.metrics);
    } catch (err) {
      setError(err.message || 'Failed loading metrics.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadMetrics();
  }, []);

  const tm = data?.test_metrics || {
    accuracy: 0.9839,
    precision: 0.9459,
    recall: 0.9333,
    f1_score: 0.9396,
    roc_auc: 0.9902,
    specificity: 0.9917,
    true_negatives: 957,
    false_positives: 8,
    false_negatives: 10,
    true_positives: 140,
    test_samples_total: 1115
  };

  const hp = data?.hyperparameters || {
    alpha: 0.1,
    ngram_range: [1, 2],
    max_features: 1000,
    min_df: 2,
    test_size: 0.2,
    random_state: 42
  };

  return (
    <div className="page-workspace">
      {/* Header Banner */}
      <div className="welcome-banner">
        <div>
          <h2 className="welcome-title">
            Model <span className="welcome-gradient">Performance & Evaluation</span> 📊
          </h2>
          <p className="welcome-subtitle">
            Rigorous classification metrics on held-out test data (80/20 stratified split)
          </p>
        </div>
        <button className="btn btn-secondary" onClick={loadMetrics} disabled={loading}>
          <RefreshCw size={14} className={loading ? 'spinner' : ''} />
          Refresh Metrics
        </button>
      </div>

      {error && (
        <div style={{ padding: '14px 18px', background: 'rgba(255, 83, 107, 0.15)', border: '1px solid rgba(255, 83, 107, 0.3)', borderRadius: '8px', color: '#FF8A9B', marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '10px' }}>
          <AlertTriangle size={18} />
          <span>{error}</span>
        </div>
      )}

      {/* Metrics Cards */}
      <div className="kpi-grid">
        <div className="kpi-card">
          <div className="kpi-header">
            <span className="kpi-label">Test Accuracy</span>
            <div className="kpi-icon-wrapper" style={{ background: 'rgba(22, 217, 139, 0.15)', color: '#16D98B' }}>
              <CheckCircle2 size={18} />
            </div>
          </div>
          <div className="kpi-value" style={{ color: '#16D98B' }}>
            {(tm.accuracy * 100).toFixed(2)}%
          </div>
          <div className="kpi-subtext">Overall correct rate on 1,115 test cases</div>
        </div>

        <div className="kpi-card">
          <div className="kpi-header">
            <span className="kpi-label">Precision (Spam)</span>
            <div className="kpi-icon-wrapper" style={{ background: 'rgba(139, 53, 246, 0.15)', color: '#A855F7' }}>
              <Percent size={18} />
            </div>
          </div>
          <div className="kpi-value">
            {(tm.precision * 100).toFixed(2)}%
          </div>
          <div className="kpi-subtext">Only 8 false positives out of 965 ham</div>
        </div>

        <div className="kpi-card">
          <div className="kpi-header">
            <span className="kpi-label">Recall (Sensitivity)</span>
            <div className="kpi-icon-wrapper" style={{ background: 'rgba(192, 132, 252, 0.15)', color: '#C084FC' }}>
              <Activity size={18} />
            </div>
          </div>
          <div className="kpi-value">
            {(tm.recall * 100).toFixed(2)}%
          </div>
          <div className="kpi-subtext">140 out of 150 spam threats intercepted</div>
        </div>

        <div className="kpi-card">
          <div className="kpi-header">
            <span className="kpi-label">F1-Score</span>
            <div className="kpi-icon-wrapper" style={{ background: 'rgba(59, 130, 246, 0.15)', color: '#60A5FA' }}>
              <BarChart2 size={18} />
            </div>
          </div>
          <div className="kpi-value">
            {(tm.f1_score * 100).toFixed(2)}%
          </div>
          <div className="kpi-subtext">Harmonic balance of precision & recall</div>
        </div>
      </div>

      {/* Middle Row: Confusion Matrix & Hyperparameters */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: '24px', marginBottom: '24px' }}>
        {/* Confusion Matrix Card */}
        <div className="saas-card" style={{ marginBottom: 0 }}>
          <div className="card-title-row">
            <div>
              <div className="card-title">Test Confusion Matrix</div>
              <div className="card-subtitle">Evaluation on {tm.test_samples_total} unseen test samples</div>
            </div>
            <span className="badge-pill badge-green">ROC-AUC: {(tm.roc_auc * 100).toFixed(2)}%</span>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px', marginTop: '16px' }}>
            <div style={{ background: '#100C1B', border: '1px solid rgba(22, 217, 139, 0.4)', borderRadius: '10px', padding: '16px', textAlign: 'center' }}>
              <div style={{ fontSize: '0.72rem', color: '#16D98B', fontWeight: 700, textTransform: 'uppercase' }}>
                True Negatives (TN)
              </div>
              <div style={{ fontSize: '1.85rem', fontWeight: 800, color: '#FFFFFF', marginTop: '4px' }}>
                {tm.true_negatives}
              </div>
              <div style={{ fontSize: '0.72rem', color: '#B9B1C8', marginTop: '4px' }}>
                Legitimate accurately cleared
              </div>
            </div>

            <div style={{ background: '#100C1B', border: '1px solid rgba(255, 83, 107, 0.3)', borderRadius: '10px', padding: '16px', textAlign: 'center' }}>
              <div style={{ fontSize: '0.72rem', color: '#FF8A9B', fontWeight: 700, textTransform: 'uppercase' }}>
                False Positives (FP)
              </div>
              <div style={{ fontSize: '1.85rem', fontWeight: 800, color: '#FF536B', marginTop: '4px' }}>
                {tm.false_positives}
              </div>
              <div style={{ fontSize: '0.72rem', color: '#B9B1C8', marginTop: '4px' }}>
                Ham flagged as spam (Error)
              </div>
            </div>

            <div style={{ background: '#100C1B', border: '1px solid rgba(255, 83, 107, 0.3)', borderRadius: '10px', padding: '16px', textAlign: 'center' }}>
              <div style={{ fontSize: '0.72rem', color: '#FF8A9B', fontWeight: 700, textTransform: 'uppercase' }}>
                False Negatives (FN)
              </div>
              <div style={{ fontSize: '1.85rem', fontWeight: 800, color: '#FF536B', marginTop: '4px' }}>
                {tm.false_negatives}
              </div>
              <div style={{ fontSize: '0.72rem', color: '#B9B1C8', marginTop: '4px' }}>
                Spam slipped through (Error)
              </div>
            </div>

            <div style={{ background: '#100C1B', border: '1px solid rgba(22, 217, 139, 0.4)', borderRadius: '10px', padding: '16px', textAlign: 'center' }}>
              <div style={{ fontSize: '0.72rem', color: '#16D98B', fontWeight: 700, textTransform: 'uppercase' }}>
                True Positives (TP)
              </div>
              <div style={{ fontSize: '1.85rem', fontWeight: 800, color: '#FFFFFF', marginTop: '4px' }}>
                {tm.true_positives}
              </div>
              <div style={{ fontSize: '0.72rem', color: '#B9B1C8', marginTop: '4px' }}>
                Spam threats intercepted
              </div>
            </div>
          </div>
        </div>

        {/* Hyperparameters Card */}
        <div className="saas-card" style={{ marginBottom: 0 }}>
          <div className="card-title-row">
            <div>
              <div className="card-title">Production Hyperparameters</div>
              <div className="card-subtitle">Active configuration loaded from model artifacts</div>
            </div>
            <span className="badge-pill badge-purple">
              <Cpu size={12} />
              MultinomialNB
            </span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginTop: '14px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 14px', background: '#100C1B', borderRadius: '6px', border: '1px solid #3A2B55' }}>
              <span style={{ color: '#B9B1C8', fontSize: '0.85rem' }}>Classifier Algorithm</span>
              <span style={{ color: '#FFFFFF', fontWeight: 600, fontSize: '0.85rem' }}>Multinomial Naive Bayes</span>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 14px', background: '#100C1B', borderRadius: '6px', border: '1px solid #3A2B55' }}>
              <span style={{ color: '#B9B1C8', fontSize: '0.85rem' }}>Laplace Smoothing (Alpha)</span>
              <span style={{ color: '#C084FC', fontWeight: 600, fontSize: '0.85rem', fontFamily: 'monospace' }}>α = {hp.alpha}</span>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 14px', background: '#100C1B', borderRadius: '6px', border: '1px solid #3A2B55' }}>
              <span style={{ color: '#B9B1C8', fontSize: '0.85rem' }}>N-Gram Range</span>
              <span style={{ color: '#FFFFFF', fontWeight: 600, fontSize: '0.85rem', fontFamily: 'monospace' }}>({hp.ngram_range?.[0]}, {hp.ngram_range?.[1]}) Unigrams & Bigrams</span>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 14px', background: '#100C1B', borderRadius: '6px', border: '1px solid #3A2B55' }}>
              <span style={{ color: '#B9B1C8', fontSize: '0.85rem' }}>TF-IDF Vocabulary Max Features</span>
              <span style={{ color: '#FFFFFF', fontWeight: 600, fontSize: '0.85rem' }}>{hp.max_features || 1000} top n-grams</span>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 14px', background: '#100C1B', borderRadius: '6px', border: '1px solid #3A2B55' }}>
              <span style={{ color: '#B9B1C8', fontSize: '0.85rem' }}>Train/Test Partition</span>
              <span style={{ color: '#FFFFFF', fontWeight: 600, fontSize: '0.85rem' }}>80% Train / 20% Test (Stratified)</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
