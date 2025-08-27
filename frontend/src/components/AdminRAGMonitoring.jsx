import React, { useState, useEffect } from 'react';

const AdminRAGMonitoring = () => {
  const [activeTab, setActiveTab] = useState('performance');
  const [ragMetrics, setRagMetrics] = useState({
    querySuccess: {},
    responseTime: {},
    contextAccuracy: {},
    userSatisfaction: {},
    knowledgeCoverage: {},
    modelPerformance: {},
    trainingInsights: {}
  });

  useEffect(() => {
    fetchRAGMetrics();
  }, []);

  const fetchRAGMetrics = async () => {
    try {
      const response = await fetch('/api/admin/rag-metrics');
      const data = await response.json();
      setRagMetrics(data);
    } catch (error) {
      console.error('Error fetching RAG metrics:', error);
    }
  };

  const RAGPerformanceCard = () => (
    <div className="card">
      <div className="card-header">
        <h3 className="text-lg font-semibold text-text-primary">🚀 RAG Performance Overview</h3>
        <p className="text-sm text-text-secondary">Real-time AI System Metrics</p>
      </div>
      <div className="card-body">
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <div className="metric-card">
            <div className="text-2xl font-bold text-success-500">98.5%</div>
            <div className="text-sm text-text-secondary">Query Success Rate</div>
            <div className="text-xs text-success-500">+2.1%</div>
          </div>
          <div className="metric-card">
            <div className="text-2xl font-bold text-primary-500">1.2s</div>
            <div className="text-sm text-text-secondary">Avg Response Time</div>
            <div className="text-xs text-warning-500">+0.3s</div>
          </div>
          <div className="metric-card">
            <div className="text-2xl font-bold text-success-500">94.2%</div>
            <div className="text-sm text-text-secondary">Context Accuracy</div>
            <div className="text-xs text-success-500">+1.8%</div>
          </div>
          <div className="metric-card">
            <div className="text-2xl font-bold text-primary-500">4.6/5</div>
            <div className="text-sm text-text-secondary">User Satisfaction</div>
            <div className="text-xs text-success-500">+0.2</div>
          </div>
        </div>
        <div className="bg-surface rounded-lg p-4 text-center">
          <span className="text-text-secondary">📊 Response Time Trends (Last 24 Hours)</span>
        </div>
      </div>
    </div>
  );

  const QueryAnalyticsCard = () => (
    <div className="card">
      <div className="card-header">
        <h3 className="text-lg font-semibold text-text-primary">🔍 Query Analytics</h3>
        <p className="text-sm text-text-secondary">Query Success Rates by Category</p>
      </div>
      <div className="card-body">
        <div className="space-y-4">
          {[
            { category: 'Property Search', success: 99.2, volume: 1250, avgTime: 0.8 },
            { category: 'Market Analysis', success: 97.8, volume: 890, avgTime: 1.5 },
            { category: 'Price Estimation', success: 96.5, volume: 650, avgTime: 2.1 },
            { category: 'Legal Questions', success: 94.2, volume: 320, avgTime: 1.8 },
            { category: 'General Inquiries', success: 98.9, volume: 2100, avgTime: 0.6 }
          ].map((item, index) => (
            <div key={index} className="flex items-center justify-between p-4 bg-surface rounded-lg border border-border">
              <div className="flex-1">
                <div className="font-medium text-text-primary">{item.category}</div>
                <div className="text-sm text-text-secondary">
                  <span>{item.volume} queries</span>
                  <span className="ml-2">•</span>
                  <span className="ml-2">{item.avgTime}s avg</span>
                </div>
              </div>
              <div className="flex items-center gap-4">
                <div className="w-32 bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-gradient-to-r from-success-500 to-success-400 h-2 rounded-full"
                    style={{ width: `${item.success}%` }}
                  ></div>
                </div>
                <span className="text-sm font-medium text-text-primary">{item.success}%</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const ModelPerformanceCard = () => (
    <div className="card">
      <div className="card-header">
        <h3 className="text-lg font-semibold text-text-primary">🤖 Model Performance</h3>
        <p className="text-sm text-text-secondary">Gemini AI Usage & Performance</p>
      </div>
      <div className="card-body">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="text-center p-4 bg-surface rounded-lg border border-border">
            <div className="text-3xl font-bold text-primary-500">2.4M</div>
            <div className="text-sm text-text-secondary">Tokens Used</div>
            <div className="text-xs text-success-500">+15% this month</div>
          </div>
          <div className="text-center p-4 bg-surface rounded-lg border border-border">
            <div className="text-3xl font-bold text-warning-500">$1,247</div>
            <div className="text-sm text-text-secondary">API Costs</div>
            <div className="text-xs text-warning-500">+8% vs last month</div>
          </div>
          <div className="text-center p-4 bg-surface rounded-lg border border-border">
            <div className="text-3xl font-bold text-success-500">99.8%</div>
            <div className="text-sm text-text-secondary">Uptime</div>
            <div className="text-xs text-success-500">Excellent</div>
          </div>
        </div>
        
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-sm text-text-secondary">Rate Limit Usage</span>
            <span className="text-sm font-medium text-text-primary">65%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div className="bg-warning-500 h-2 rounded-full" style={{ width: '65%' }}></div>
          </div>
          
          <div className="flex items-center justify-between">
            <span className="text-sm text-text-secondary">Error Rate</span>
            <span className="text-sm font-medium text-text-primary">0.2%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div className="bg-success-500 h-2 rounded-full" style={{ width: '0.2%' }}></div>
          </div>
        </div>
      </div>
    </div>
  );

  const KnowledgeGapCard = () => (
    <div className="card">
      <div className="card-header">
        <h3 className="text-lg font-semibold text-text-primary">🧠 Knowledge Gap Analysis</h3>
        <p className="text-sm text-text-secondary">Unanswered questions and knowledge gaps</p>
      </div>
      <div className="card-body">
        <div className="space-y-4">
          {[
            { question: 'What are the latest regulations for off-plan purchases?', frequency: 45, category: 'Legal' },
            { question: 'How do I calculate ROI for rental properties?', frequency: 32, category: 'Financial' },
            { question: 'What are the best areas for short-term rentals?', frequency: 28, category: 'Market' },
            { question: 'How to verify property title deeds?', frequency: 22, category: 'Legal' },
            { question: 'What are the tax implications for foreign investors?', frequency: 18, category: 'Financial' }
          ].map((item, index) => (
            <div key={index} className="p-4 bg-surface rounded-lg border border-border">
              <div className="flex items-start justify-between mb-2">
                <h4 className="font-medium text-text-primary">{item.question}</h4>
                <span className="badge badge-warning">{item.category}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-text-secondary">
                  Asked {item.frequency} times this month
                </span>
                <button className="btn btn-primary btn-sm">
                  Add to Knowledge Base
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const UserFeedbackCard = () => (
    <div className="card">
      <div className="card-header">
        <h3 className="text-lg font-semibold text-text-primary">💬 User Feedback</h3>
        <p className="text-sm text-text-secondary">Recent user feedback and satisfaction</p>
      </div>
      <div className="card-body">
        <div className="space-y-4">
          {[
            { rating: 5, comment: 'Excellent property recommendations!', user: 'John D.', date: '2 hours ago' },
            { rating: 4, comment: 'Very helpful market analysis, but could be faster', user: 'Sarah M.', date: '4 hours ago' },
            { rating: 5, comment: 'Accurate price estimates and detailed property info', user: 'Mike R.', date: '6 hours ago' },
            { rating: 3, comment: 'Good information but needs more recent data', user: 'Lisa K.', date: '1 day ago' },
            { rating: 5, comment: 'Amazing AI assistant, very responsive and helpful', user: 'David L.', date: '1 day ago' }
          ].map((feedback, index) => (
            <div key={index} className="p-4 bg-surface rounded-lg border border-border">
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-center gap-2">
                  <div className="flex">
                    {[...Array(5)].map((_, i) => (
                      <span key={i} className={`text-lg ${i < feedback.rating ? 'text-warning-500' : 'text-gray-300'}`}>
                        ⭐
                      </span>
                    ))}
                  </div>
                  <span className="text-sm text-text-secondary">by {feedback.user}</span>
                </div>
                <span className="text-xs text-text-tertiary">{feedback.date}</span>
              </div>
              <p className="text-sm text-text-primary">{feedback.comment}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  return (
    <div className="admin-container">
      {/* Header */}
      <div className="admin-header">
        <div className="flex items-center justify-between w-full p-6">
          <div className="flex items-center">
            <div className="w-12 h-12 bg-gradient-to-br from-primary-500 to-primary-300 rounded-full flex items-center justify-center text-2xl font-bold text-secondary-50 mr-4 shadow-lg">
              🤖
            </div>
            <div>
              <h1 className="text-2xl font-bold text-primary-500">RAG System Monitoring</h1>
              <p className="text-sm text-text-secondary">
                AI performance, knowledge gaps, and user feedback
              </p>
            </div>
          </div>
          
          <div className="flex items-center gap-4">
            <span className="text-sm text-text-secondary">
              Last updated: {new Date().toLocaleString()}
            </span>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="p-6">
        <div className="flex space-x-1 bg-surface rounded-lg p-1 mb-6">
          {[
            { id: 'performance', label: 'Performance', icon: '🚀' },
            { id: 'queries', label: 'Queries', icon: '🔍' },
            { id: 'model', label: 'Model', icon: '🤖' },
            { id: 'gaps', label: 'Knowledge Gaps', icon: '🧠' },
            { id: 'feedback', label: 'Feedback', icon: '💬' }
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-all ${
                activeTab === tab.id
                  ? 'bg-primary-500 text-secondary-50'
                  : 'text-text-secondary hover:text-text-primary hover:bg-surface-elevated'
              }`}
            >
              <span>{tab.icon}</span>
              {tab.label}
            </button>
          ))}
        </div>

        {/* Content */}
        <div className="space-y-6">
          {activeTab === 'performance' && <RAGPerformanceCard />}
          {activeTab === 'queries' && <QueryAnalyticsCard />}
          {activeTab === 'model' && <ModelPerformanceCard />}
          {activeTab === 'gaps' && <KnowledgeGapCard />}
          {activeTab === 'feedback' && <UserFeedbackCard />}
        </div>
      </div>
    </div>
  );
};

export default AdminRAGMonitoring;
