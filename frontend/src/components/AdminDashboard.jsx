import React, { useState, useEffect } from 'react';

const AdminDashboard = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [metrics, setMetrics] = useState({
    marketPerformance: {},
    agentPerformance: {},
    leadConversion: {},
    propertyAnalytics: {},
    financialMetrics: {}
  });

  useEffect(() => {
    // Fetch dashboard metrics
    fetchDashboardMetrics();
  }, []);

  const fetchDashboardMetrics = async () => {
    try {
      const response = await fetch('/api/admin/dashboard-metrics');
      const data = await response.json();
      setMetrics(data);
    } catch (error) {
      console.error('Error fetching dashboard metrics:', error);
    }
  };

  const MarketPerformanceCard = () => (
    <div className="card">
      <div className="card-header">
        <h3 className="text-lg font-semibold text-text-primary">📈 Market Performance</h3>
        <p className="text-sm text-text-secondary">Dubai Real Estate Trends</p>
      </div>
      <div className="card-body">
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <div className="metric-card">
            <div className="text-2xl font-bold text-primary-500">AED 2,450</div>
            <div className="text-sm text-text-secondary">Avg Price/sqft</div>
            <div className="text-xs text-success-500">+5.2%</div>
          </div>
          <div className="metric-card">
            <div className="text-2xl font-bold text-primary-500">45 days</div>
            <div className="text-sm text-text-secondary">Avg Days on Market</div>
            <div className="text-xs text-success-500">-12%</div>
          </div>
          <div className="metric-card">
            <div className="text-2xl font-bold text-primary-500">1,247</div>
            <div className="text-sm text-text-secondary">Active Listings</div>
            <div className="text-xs text-success-500">+8.3%</div>
          </div>
          <div className="metric-card">
            <div className="text-2xl font-bold text-primary-500">AED 125.6M</div>
            <div className="text-sm text-text-secondary">Total Market Value</div>
            <div className="text-xs text-success-500">+15.7%</div>
          </div>
        </div>
        <div className="bg-surface rounded-lg p-4 text-center">
          <span className="text-text-secondary">📊 Price Trends by Neighborhood</span>
        </div>
      </div>
    </div>
  );

  const AgentPerformanceCard = () => (
    <div className="card">
      <div className="card-header">
        <h3 className="text-lg font-semibold text-text-primary">👥 Agent Performance</h3>
        <p className="text-sm text-text-secondary">Top Performers This Month</p>
      </div>
      <div className="card-body">
        <div className="space-y-4">
          {[
            { name: 'Jane Smith', sales: 12, commission: 'AED 45,000', satisfaction: 4.8 },
            { name: 'Emily White', sales: 9, commission: 'AED 32,000', satisfaction: 4.6 },
            { name: 'Michael Brown', sales: 7, commission: 'AED 28,000', satisfaction: 4.7 },
            { name: 'Sarah Green', sales: 6, commission: 'AED 24,000', satisfaction: 4.5 }
          ].map((agent, index) => (
            <div key={index} className="flex items-center justify-between p-4 bg-surface rounded-lg border border-border">
              <div className="flex items-center gap-4">
                <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-primary-300 rounded-full flex items-center justify-center text-white font-bold">
                  {agent.name.charAt(0)}
                </div>
                <div>
                  <div className="font-medium text-text-primary">{agent.name}</div>
                  <div className="text-sm text-text-secondary">
                    <span>{agent.sales} sales</span>
                    <span className="ml-2">⭐ {agent.satisfaction}</span>
                  </div>
                </div>
              </div>
              <div className="text-right">
                <div className="font-semibold text-primary-500">{agent.commission}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const LeadConversionCard = () => (
    <div className="card">
      <div className="card-header">
        <h3 className="text-lg font-semibold text-text-primary">🎯 Lead Conversion</h3>
        <p className="text-sm text-text-secondary">Conversion Pipeline</p>
      </div>
      <div className="card-body">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="text-center p-4 bg-surface rounded-lg border border-border">
            <div className="text-3xl font-bold text-primary-500">1,247</div>
            <div className="text-sm text-text-secondary">Total Leads</div>
            <div className="text-xs text-success-500">+12% this month</div>
          </div>
          <div className="text-center p-4 bg-surface rounded-lg border border-border">
            <div className="text-3xl font-bold text-warning-500">342</div>
            <div className="text-sm text-text-secondary">Qualified Leads</div>
            <div className="text-xs text-warning-500">27.4% conversion</div>
          </div>
          <div className="text-center p-4 bg-surface rounded-lg border border-border">
            <div className="text-3xl font-bold text-success-500">89</div>
            <div className="text-sm text-text-secondary">Closed Deals</div>
            <div className="text-xs text-success-500">26% success rate</div>
          </div>
        </div>
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-sm text-text-secondary">Lead Response Time</span>
            <span className="text-sm font-medium text-text-primary">2.3 hours</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div className="bg-success-500 h-2 rounded-full" style={{ width: '85%' }}></div>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm text-text-secondary">Follow-up Rate</span>
            <span className="text-sm font-medium text-text-primary">94%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div className="bg-primary-500 h-2 rounded-full" style={{ width: '94%' }}></div>
          </div>
        </div>
      </div>
    </div>
  );

  const PropertyAnalyticsCard = () => (
    <div className="card">
      <div className="card-header">
        <h3 className="text-lg font-semibold text-text-primary">🏠 Property Analytics</h3>
        <p className="text-sm text-text-secondary">Property Performance Metrics</p>
      </div>
      <div className="card-body">
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <div className="text-center">
            <div className="text-2xl font-bold text-primary-500">2,847</div>
            <div className="text-sm text-text-secondary">Total Views</div>
            <div className="text-xs text-success-500">+18%</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-primary-500">156</div>
            <div className="text-sm text-text-secondary">Inquiries</div>
            <div className="text-xs text-success-500">+23%</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-primary-500">89</div>
            <div className="text-sm text-text-secondary">Favorites</div>
            <div className="text-xs text-success-500">+15%</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-primary-500">5.8</div>
            <div className="text-sm text-text-secondary">Avg Rating</div>
            <div className="text-xs text-success-500">+0.3</div>
          </div>
        </div>
        <div className="space-y-4">
          <div className="flex items-center justify-between p-3 bg-surface rounded-lg">
            <span className="text-sm text-text-secondary">Most Viewed Property</span>
            <span className="text-sm font-medium text-text-primary">Marina Heights #1204</span>
          </div>
          <div className="flex items-center justify-between p-3 bg-surface rounded-lg">
            <span className="text-sm text-text-secondary">Highest Inquiry Rate</span>
            <span className="text-sm font-medium text-text-primary">Downtown Views</span>
          </div>
          <div className="flex items-center justify-between p-3 bg-surface rounded-lg">
            <span className="text-sm text-text-secondary">Best Rated</span>
            <span className="text-sm font-medium text-text-primary">Palm Jumeirah Villa</span>
          </div>
        </div>
      </div>
    </div>
  );

  const FinancialMetricsCard = () => (
    <div className="card">
      <div className="card-header">
        <h3 className="text-lg font-semibold text-text-primary">💰 Financial Metrics</h3>
        <p className="text-sm text-text-secondary">Revenue & Commission Tracking</p>
      </div>
      <div className="card-body">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <div className="space-y-4">
            <div className="text-center p-4 bg-surface rounded-lg border border-border">
              <div className="text-3xl font-bold text-success-500">AED 2.4M</div>
              <div className="text-sm text-text-secondary">Total Revenue</div>
              <div className="text-xs text-success-500">+18.5% vs last month</div>
            </div>
            <div className="text-center p-4 bg-surface rounded-lg border border-border">
              <div className="text-3xl font-bold text-primary-500">AED 180K</div>
              <div className="text-sm text-text-secondary">Commission Earned</div>
              <div className="text-xs text-primary-500">7.5% of revenue</div>
            </div>
          </div>
          <div className="space-y-4">
            <div className="text-center p-4 bg-surface rounded-lg border border-border">
              <div className="text-3xl font-bold text-warning-500">AED 45K</div>
              <div className="text-sm text-text-secondary">Avg Deal Value</div>
              <div className="text-xs text-warning-500">+12% increase</div>
            </div>
            <div className="text-center p-4 bg-surface rounded-lg border border-border">
              <div className="text-3xl font-bold text-error-500">6.2%</div>
              <div className="text-sm text-text-secondary">ROI per Property</div>
              <div className="text-xs text-error-500">Above market avg</div>
            </div>
          </div>
        </div>
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-sm text-text-secondary">Commission Split</span>
            <span className="text-sm font-medium text-text-primary">70/30 (Agent/Company)</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div className="bg-primary-500 h-2 rounded-full" style={{ width: '70%' }}></div>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm text-text-secondary">Payment Processing</span>
            <span className="text-sm font-medium text-text-primary">98% on time</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div className="bg-success-500 h-2 rounded-full" style={{ width: '98%' }}></div>
          </div>
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
              📊
            </div>
            <div>
              <h1 className="text-2xl font-bold text-primary-500">Admin Dashboard</h1>
              <p className="text-sm text-text-secondary">
                Real Estate Performance Analytics
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
            { id: 'overview', label: 'Overview', icon: '📊' },
            { id: 'market', label: 'Market', icon: '📈' },
            { id: 'agents', label: 'Agents', icon: '👥' },
            { id: 'leads', label: 'Leads', icon: '🎯' },
            { id: 'properties', label: 'Properties', icon: '🏠' },
            { id: 'finance', label: 'Finance', icon: '💰' }
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

        {/* Dashboard Content */}
        <div className="space-y-6">
          {activeTab === 'overview' && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <MarketPerformanceCard />
              <AgentPerformanceCard />
              <LeadConversionCard />
              <PropertyAnalyticsCard />
            </div>
          )}
          
          {activeTab === 'market' && <MarketPerformanceCard />}
          {activeTab === 'agents' && <AgentPerformanceCard />}
          {activeTab === 'leads' && <LeadConversionCard />}
          {activeTab === 'properties' && <PropertyAnalyticsCard />}
          {activeTab === 'finance' && <FinancialMetricsCard />}
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
