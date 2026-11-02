import React from 'react';
import { NAV_ITEMS } from './Sidebar';
import { Shield, Sparkles, Cpu, GitBranch } from 'lucide-react';

export function Topbar({ currentView, apiHealth }) {
  const currentNav = NAV_ITEMS.find((item) => item.id === currentView) || { label: 'Dashboard' };
  const isHealthy = apiHealth?.status === 'healthy';

  return (
    <header className="topbar">
      <div className="topbar-left">
        <h1 className="topbar-page-title">{currentNav.label}</h1>
        <span className="badge-pill badge-purple">
          <Cpu size={12} />
          v2.0 Serverless
        </span>
      </div>

      <div className="topbar-right">
        <a
          href="https://github.com/gauravrsingh16-art/scam"
          target="_blank"
          rel="noopener noreferrer"
          className="badge-pill badge-purple"
          style={{ textDecoration: 'none', cursor: 'pointer' }}
        >
          <GitBranch size={12} />
          main / scam
        </a>

        <div className={`badge-pill ${isHealthy ? 'badge-green' : 'badge-red'}`}>
          <Shield size={12} />
          {isHealthy ? 'AI Engine Online' : 'Connecting...'}
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', paddingLeft: '8px', borderLeft: '1px solid #3A2B55' }}>
          <div style={{ width: '32px', height: '32px', borderRadius: '50%', background: 'linear-gradient(135deg, #8B35F6, #EC4899)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 700, fontSize: '0.8rem' }}>
            SI
          </div>
        </div>
      </div>
    </header>
  );
}
