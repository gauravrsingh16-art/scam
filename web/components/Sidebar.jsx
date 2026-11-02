import React from 'react';
import {
  LayoutDashboard,
  MessageSquare,
  Mail,
  Files,
  Activity,
  Database,
  History,
  Info,
  Settings,
  ShieldCheck,
  ShieldAlert
} from 'lucide-react';

export const NAV_ITEMS = [
  { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { id: 'message-detection', label: 'Message Detection', icon: MessageSquare },
  { id: 'email-analysis', label: 'Email Analysis', icon: Mail },
  { id: 'bulk-detection', label: 'Bulk Detection', icon: Files },
  { id: 'model-performance', label: 'Model Performance', icon: Activity },
  { id: 'dataset-management', label: 'Dataset Management', icon: Database },
  { id: 'classification-history', label: 'Classification History', icon: History },
  { id: 'project-info', label: 'Project Information', icon: Info },
  { id: 'settings', label: 'Settings', icon: Settings },
];

export function Sidebar({ currentView, onSelectView, apiHealth }) {
  const isHealthy = apiHealth?.status === 'healthy';

  return (
    <aside className="sidebar">
      {/* Brand */}
      <div className="sidebar-brand">
        <div className="brand-icon">
          <ShieldAlert size={22} color="#FFFFFF" />
        </div>
        <div>
          <div className="brand-title">SPAM INTEL</div>
          <div className="brand-subtitle">AI DEFENSE ENGINE</div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="sidebar-nav">
        <div className="nav-section-title">Operations</div>
        {NAV_ITEMS.slice(0, 4).map((item) => {
          const Icon = item.icon;
          const isActive = currentView === item.id;
          return (
            <button
              key={item.id}
              className={`nav-item ${isActive ? 'active' : ''}`}
              onClick={() => onSelectView(item.id)}
            >
              <span className="nav-item-icon">
                <Icon size={18} />
              </span>
              <span>{item.label}</span>
            </button>
          );
        })}

        <div className="nav-section-title" style={{ marginTop: '12px' }}>Intelligence & Data</div>
        {NAV_ITEMS.slice(4, 7).map((item) => {
          const Icon = item.icon;
          const isActive = currentView === item.id;
          return (
            <button
              key={item.id}
              className={`nav-item ${isActive ? 'active' : ''}`}
              onClick={() => onSelectView(item.id)}
            >
              <span className="nav-item-icon">
                <Icon size={18} />
              </span>
              <span>{item.label}</span>
            </button>
          );
        })}

        <div className="nav-section-title" style={{ marginTop: '12px' }}>System</div>
        {NAV_ITEMS.slice(7).map((item) => {
          const Icon = item.icon;
          const isActive = currentView === item.id;
          return (
            <button
              key={item.id}
              className={`nav-item ${isActive ? 'active' : ''}`}
              onClick={() => onSelectView(item.id)}
            >
              <span className="nav-item-icon">
                <Icon size={18} />
              </span>
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>

      {/* Footer Status */}
      <div className="sidebar-footer">
        <div className="model-status-card">
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '6px' }}>
            <span style={{ fontSize: '0.72rem', fontWeight: 600, color: '#B9B1C8', textTransform: 'uppercase' }}>
              ML ENGINE STATUS
            </span>
            <div className="status-dot-pulse" style={{ backgroundColor: isHealthy ? '#16D98B' : '#FF536B' }} />
          </div>
          <div style={{ fontSize: '0.82rem', fontWeight: 700, color: '#FFFFFF', display: 'flex', alignItems: 'center', gap: '6px' }}>
            <ShieldCheck size={16} color={isHealthy ? '#16D98B' : '#FF536B'} />
            {isHealthy ? 'MultinomialNB Active' : 'Offline / Loading'}
          </div>
          <div style={{ fontSize: '0.7rem', color: '#8E82A5', marginTop: '2px' }}>
            TF-IDF (5,000 features)
          </div>
        </div>
      </div>
    </aside>
  );
}
