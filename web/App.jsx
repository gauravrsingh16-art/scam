import React, { useState, useEffect } from 'react';
import { Sidebar } from './components/Sidebar';
import { Topbar } from './components/Topbar';
import { DashboardView } from './views/DashboardView';
import { MessageDetectionView } from './views/MessageDetectionView';
import { EmailAnalysisView } from './views/EmailAnalysisView';
import { BulkDetectionView } from './views/BulkDetectionView';
import { ModelPerformanceView } from './views/ModelPerformanceView';
import { DatasetManagementView } from './views/DatasetManagementView';
import { ClassificationHistoryView } from './views/ClassificationHistoryView';
import { ProjectInfoView } from './views/ProjectInfoView';
import { SettingsView } from './views/SettingsView';
import { checkHealth } from './api';

export function App() {
  const [currentView, setCurrentView] = useState('dashboard');
  const [apiHealth, setApiHealth] = useState(null);

  useEffect(() => {
    const fetchHealthStatus = async () => {
      try {
        const health = await checkHealth();
        setApiHealth(health);
      } catch (err) {
        setApiHealth({ status: 'offline', error: err.message });
      }
    };

    fetchHealthStatus();
    const interval = setInterval(fetchHealthStatus, 30000); // 30s heartbeat
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="app-container">
      {/* Fixed Sidebar */}
      <Sidebar
        currentView={currentView}
        onSelectView={setCurrentView}
        apiHealth={apiHealth}
      />

      {/* Main Content Layout */}
      <div className="main-layout">
        <Topbar
          currentView={currentView}
          apiHealth={apiHealth}
        />

        {/* View Router */}
        {currentView === 'dashboard' && <DashboardView onNavigate={setCurrentView} />}
        {currentView === 'message-detection' && <MessageDetectionView />}
        {currentView === 'email-analysis' && <EmailAnalysisView />}
        {currentView === 'bulk-detection' && <BulkDetectionView />}
        {currentView === 'model-performance' && <ModelPerformanceView />}
        {currentView === 'dataset-management' && <DatasetManagementView />}
        {currentView === 'classification-history' && <ClassificationHistoryView />}
        {currentView === 'project-info' && <ProjectInfoView />}
        {currentView === 'settings' && <SettingsView apiHealth={apiHealth} />}
      </div>
    </div>
  );
}

export default App;
