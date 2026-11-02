import React from 'react';
import {
  Info,
  GitBranch,
  ShieldCheck,
  Cpu,
  Layers,
  Database,
  Terminal,
  ExternalLink,
  Code2
} from 'lucide-react';

export function ProjectInfoView() {
  return (
    <div className="page-workspace">
      {/* Header Banner */}
      <div className="welcome-banner">
        <div>
          <h2 className="welcome-title">
            Project <span className="welcome-gradient">Intelligence & Architecture</span> ℹ
          </h2>
          <p className="welcome-subtitle">
            Academic engineering mini-project specification, ML pipeline design, and system benchmarks
          </p>
        </div>
        <a
          href="https://github.com/gauravrsingh16-art/scam"
          target="_blank"
          rel="noopener noreferrer"
          className="btn btn-secondary"
          style={{ textDecoration: 'none' }}
        >
          <GitBranch size={14} />
          GitHub Repository
          <ExternalLink size={12} />
        </a>
      </div>

      {/* Overview Card */}
      <div className="saas-card">
        <div className="card-title-row">
          <div>
            <div className="card-title">Executive Summary</div>
            <div className="card-subtitle">AI-Powered Email/SMS Spam Detection System</div>
          </div>
          <span className="badge-pill badge-purple">Production-Quality AIML</span>
        </div>

        <p style={{ color: '#B9B1C8', fontSize: '0.9rem', lineHeight: '1.7', marginBottom: '16px' }}>
          <strong>SPAM INTELLIGENCE</strong> is an enterprise-grade cybersecurity application engineered to intercept, classify, and explain spam, fraudulent lures, and phishing payloads in SMS messages and email transmissions. Built on Scikit-Learn’s Multinomial Naive Bayes and custom NLP lexical feature extractors, the system achieves a verified <strong>98.39% test accuracy</strong> and <strong>94.59% precision</strong> while operating within serverless response constraints.
        </p>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '14px', marginTop: '16px' }}>
          <div style={{ background: '#100C1B', border: '1px solid #3A2B55', padding: '16px', borderRadius: '8px' }}>
            <div style={{ color: '#8E82A5', fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase' }}>
              Repository
            </div>
            <div style={{ color: '#FFFFFF', fontWeight: 700, fontSize: '0.92rem', marginTop: '4px' }}>
              gauravrsingh16-art/scam
            </div>
            <div style={{ color: '#C084FC', fontSize: '0.75rem', marginTop: '2px' }}>Branch: main</div>
          </div>

          <div style={{ background: '#100C1B', border: '1px solid #3A2B55', padding: '16px', borderRadius: '8px' }}>
            <div style={{ color: '#8E82A5', fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase' }}>
              Core ML Classifier
            </div>
            <div style={{ color: '#FFFFFF', fontWeight: 700, fontSize: '0.92rem', marginTop: '4px' }}>
              Multinomial Naive Bayes
            </div>
            <div style={{ color: '#16D98B', fontSize: '0.75rem', marginTop: '2px' }}>Laplace α = 0.1</div>
          </div>

          <div style={{ background: '#100C1B', border: '1px solid #3A2B55', padding: '16px', borderRadius: '8px' }}>
            <div style={{ color: '#8E82A5', fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase' }}>
              Vectorization Engine
            </div>
            <div style={{ color: '#FFFFFF', fontWeight: 700, fontSize: '0.92rem', marginTop: '4px' }}>
              TF-IDF (1k Features)
            </div>
            <div style={{ color: '#60A5FA', fontSize: '0.75rem', marginTop: '2px' }}>Sublinear TF Scaling</div>
          </div>

          <div style={{ background: '#100C1B', border: '1px solid #3A2B55', padding: '16px', borderRadius: '8px' }}>
            <div style={{ color: '#8E82A5', fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase' }}>
              Deployment Target
            </div>
            <div style={{ color: '#FFFFFF', fontWeight: 700, fontSize: '0.92rem', marginTop: '4px' }}>
              Vercel Serverless + Streamlit Cloud
            </div>
            <div style={{ color: '#F59E0B', fontSize: '0.75rem', marginTop: '2px' }}>Hybrid Dual-Architecture</div>
          </div>
        </div>
      </div>

      {/* System Architecture Grid */}
      <div className="saas-card">
        <div className="card-title-row">
          <div>
            <div className="card-title">End-to-End System Architecture</div>
            <div className="card-subtitle">Dual-runtime deployment architecture supporting both Vercel Serverless and Streamlit Cloud</div>
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '18px', marginTop: '14px' }}>
          <div style={{ background: '#100C1B', border: '1px solid #3A2B55', padding: '18px', borderRadius: '10px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '10px' }}>
              <Code2 size={20} color="#8B35F6" />
              <div style={{ fontWeight: 700, color: '#FFFFFF', fontSize: '0.95rem' }}>1. Frontend Layer</div>
            </div>
            <p style={{ color: '#B9B1C8', fontSize: '0.82rem', lineHeight: '1.6' }}>
              React 18 SPA built with Vite. Features a cybersecurity SaaS design system with dark purple accents, live telemetry gauges, batch upload processors, and modular operational dashboards.
            </p>
          </div>

          <div style={{ background: '#100C1B', border: '1px solid #3A2B55', padding: '18px', borderRadius: '10px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '10px' }}>
              <Cpu size={20} color="#A855F7" />
              <div style={{ fontWeight: 700, color: '#FFFFFF', fontSize: '0.95rem' }}>2. API & Serverless Layer</div>
            </div>
            <p style={{ color: '#B9B1C8', fontSize: '0.82rem', lineHeight: '1.6' }}>
              FastAPI ASGI serverless application located at <code style={{ color: '#C084FC' }}>api/index.py</code>. Exposes REST endpoints for real-time inference, email threat audits, batch CSV classification, and telemetry retrieval.
            </p>
          </div>

          <div style={{ background: '#100C1B', border: '1px solid #3A2B55', padding: '18px', borderRadius: '10px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '10px' }}>
              <Layers size={20} color="#16D98B" />
              <div style={{ fontWeight: 700, color: '#FFFFFF', fontSize: '0.95rem' }}>3. Machine Learning Core</div>
            </div>
            <p style={{ color: '#B9B1C8', fontSize: '0.82rem', lineHeight: '1.6' }}>
              Multinomial Naive Bayes model paired with TF-IDF vectorizer and regex heuristic analyzer. Reused directly by both FastAPI serverless functions and the existing Streamlit dashboard (<code style={{ color: '#16D98B' }}>app.py</code>).
            </p>
          </div>

          <div style={{ background: '#100C1B', border: '1px solid #3A2B55', padding: '18px', borderRadius: '10px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '10px' }}>
              <Database size={20} color="#60A5FA" />
              <div style={{ fontWeight: 700, color: '#FFFFFF', fontSize: '0.95rem' }}>4. Telemetry & Storage</div>
            </div>
            <p style={{ color: '#B9B1C8', fontSize: '0.82rem', lineHeight: '1.6' }}>
              Embedded SQLite audit database with privacy-preserving text sanitization. In serverless environments, safely falls back to writable temporary storage with seed replication.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
