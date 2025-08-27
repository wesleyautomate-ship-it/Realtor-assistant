import React, { useState, useCallback, useRef } from 'react';

const AdminDataManagement = () => {
  const [activeTab, setActiveTab] = useState('upload');
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [uploadProgress, setUploadProgress] = useState({});
  const [validationResults, setValidationResults] = useState({});
  const [processingStatus, setProcessingStatus] = useState('idle');
  const [dataQuality, setDataQuality] = useState({});
  const [versionHistory, setVersionHistory] = useState([]);
  const [databaseHealth, setDatabaseHealth] = useState({});
  const [storageAnalytics, setStorageAnalytics] = useState({});
  const [dataLineage, setDataLineage] = useState([]);
  
  const fileInputRef = useRef(null);
  const dropZoneRef = useRef(null);

  // Drag and drop handlers
  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    dropZoneRef.current?.classList.add('drag-over');
  }, []);

  const handleDragLeave = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    dropZoneRef.current?.classList.remove('drag-over');
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    dropZoneRef.current?.classList.remove('drag-over');
    
    const files = Array.from(e.dataTransfer.files);
    handleFiles(files);
  }, []);

  const handleFileSelect = useCallback((e) => {
    const files = Array.from(e.target.files);
    handleFiles(files);
  }, []);

  const handleFiles = async (files) => {
    const newFiles = files.map(file => ({
      id: Date.now() + Math.random(),
      file,
      name: file.name,
      size: file.size,
      type: file.type,
      status: 'pending',
      progress: 0,
      validation: null,
      quality: null
    }));

    setUploadedFiles(prev => [...prev, ...newFiles]);
    
    // Process each file
    for (const fileObj of newFiles) {
      await processFile(fileObj);
    }
  };

  const processFile = async (fileObj) => {
    try {
      // Update status to processing
      setUploadedFiles(prev => 
        prev.map(f => f.id === fileObj.id ? { ...f, status: 'processing' } : f)
      );

      // Simulate file upload with progress
      for (let progress = 0; progress <= 100; progress += 10) {
        setUploadProgress(prev => ({ ...prev, [fileObj.id]: progress }));
        await new Promise(resolve => setTimeout(resolve, 100));
      }

      // Validate file
      const validation = await validateFile(fileObj);
      setValidationResults(prev => ({ ...prev, [fileObj.id]: validation }));

      // Check data quality
      const quality = await checkDataQuality(fileObj);
      setDataQuality(prev => ({ ...prev, [fileObj.id]: quality }));

      // Update status to completed
      setUploadedFiles(prev => 
        prev.map(f => f.id === fileObj.id ? { 
          ...f, 
          status: validation.isValid ? 'completed' : 'error',
          validation,
          quality
        } : f)
      );

    } catch (error) {
      console.error('Error processing file:', error);
      setUploadedFiles(prev => 
        prev.map(f => f.id === fileObj.id ? { ...f, status: 'error' } : f)
      );
    }
  };

  const validateFile = async (fileObj) => {
    // Simulate validation
    await new Promise(resolve => setTimeout(resolve, 500));
    
    return {
      isValid: Math.random() > 0.2, // 80% success rate
      errors: Math.random() > 0.8 ? ['Invalid format', 'Missing required fields'] : [],
      warnings: Math.random() > 0.6 ? ['Data quality issues detected'] : [],
      score: Math.floor(Math.random() * 40) + 60 // 60-100 score
    };
  };

  const checkDataQuality = async (fileObj) => {
    // Simulate data quality check
    await new Promise(resolve => setTimeout(resolve, 300));
    
    return {
      completeness: Math.floor(Math.random() * 30) + 70,
      accuracy: Math.floor(Math.random() * 25) + 75,
      consistency: Math.floor(Math.random() * 20) + 80,
      timeliness: Math.floor(Math.random() * 15) + 85,
      overall: Math.floor(Math.random() * 20) + 80
    };
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return 'text-success-500';
      case 'processing': return 'text-warning-500';
      case 'error': return 'text-error-500';
      default: return 'text-text-secondary';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed': return '✅';
      case 'processing': return '⏳';
      case 'error': return '❌';
      default: return '⏸️';
    }
  };

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
              <h1 className="text-2xl font-bold text-primary-500">Data Management</h1>
              <p className="text-sm text-text-secondary">
                Advanced data upload, validation, and management
              </p>
            </div>
          </div>
          
          <div className="flex items-center gap-4">
            <span className="text-sm text-text-secondary">
              {uploadedFiles.length} files processed
            </span>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="p-6">
        <div className="flex space-x-1 bg-surface rounded-lg p-1 mb-6">
          {[
            { id: 'upload', label: 'Upload', icon: '📁' },
            { id: 'validation', label: 'Validation', icon: '✅' },
            { id: 'quality', label: 'Quality', icon: '📊' },
            { id: 'database', label: 'Database', icon: '🗄️' },
            { id: 'lineage', label: 'Lineage', icon: '🔄' }
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
          {/* Upload Tab */}
          {activeTab === 'upload' && (
            <div className="space-y-6">
              <div className="card">
                <div className="card-header">
                  <h3 className="text-lg font-semibold text-text-primary">📁 File Upload</h3>
                  <p className="text-sm text-text-secondary">Drag & drop files for processing</p>
                </div>
                <div className="card-body">
                  <div
                    ref={dropZoneRef}
                    className="upload-zone"
                    onDragOver={handleDragOver}
                    onDragLeave={handleDragLeave}
                    onDrop={handleDrop}
                    onClick={() => fileInputRef.current?.click()}
                  >
                    <div className="text-center">
                      <div className="w-16 h-16 bg-gradient-to-br from-primary-500 to-primary-300 rounded-full flex items-center justify-center text-3xl mx-auto mb-4">
                        📁
                      </div>
                      <h3 className="text-xl font-semibold text-text-primary mb-2">
                        Drop files here or click to browse
                      </h3>
                      <p className="text-text-secondary mb-4">
                        Support for CSV, Excel, JSON, and other data formats
                      </p>
                      <p className="text-sm text-text-tertiary">
                        Max file size: 50MB
                      </p>
                    </div>
                    
                    <input
                      ref={fileInputRef}
                      type="file"
                      multiple
                      onChange={handleFileSelect}
                      className="hidden"
                      accept=".csv,.xlsx,.xls,.json,.txt,.pdf"
                    />
                  </div>
                </div>
              </div>

              {/* File List */}
              {uploadedFiles.length > 0 && (
                <div className="card">
                  <div className="card-header">
                    <h3 className="text-lg font-semibold text-text-primary">📋 Uploaded Files</h3>
                  </div>
                  <div className="card-body">
                    <div className="space-y-4">
                      {uploadedFiles.map(file => (
                        <div key={file.id} className="flex items-center justify-between p-4 bg-surface rounded-lg border border-border">
                          <div className="flex items-center gap-4">
                            <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-primary-300 rounded-lg flex items-center justify-center text-xl">
                              📄
                            </div>
                            <div>
                              <h4 className="font-medium text-text-primary">{file.name}</h4>
                              <p className="text-sm text-text-secondary">
                                {formatFileSize(file.size)} • {file.type}
                              </p>
                            </div>
                          </div>
                          
                          <div className="flex items-center gap-4">
                            <div className="text-right">
                              <div className={`flex items-center gap-2 ${getStatusColor(file.status)}`}>
                                <span>{getStatusIcon(file.status)}</span>
                                <span className="text-sm font-medium capitalize">{file.status}</span>
                              </div>
                              {uploadProgress[file.id] !== undefined && (
                                <div className="text-xs text-text-secondary">
                                  {uploadProgress[file.id]}% complete
                                </div>
                              )}
                            </div>
                            
                            {uploadProgress[file.id] !== undefined && (
                              <div className="w-24 bg-gray-200 rounded-full h-2">
                                <div
                                  className="bg-gradient-to-r from-primary-500 to-primary-300 h-2 rounded-full transition-all duration-300"
                                  style={{ width: `${uploadProgress[file.id]}%` }}
                                ></div>
                              </div>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Validation Tab */}
          {activeTab === 'validation' && (
            <div className="card">
              <div className="card-header">
                <h3 className="text-lg font-semibold text-text-primary">✅ Data Validation</h3>
                <p className="text-sm text-text-secondary">Validation results and error analysis</p>
              </div>
              <div className="card-body">
                <div className="space-y-4">
                  {Object.entries(validationResults).map(([fileId, validation]) => {
                    const file = uploadedFiles.find(f => f.id === fileId);
                    if (!file) return null;
                    
                    return (
                      <div key={fileId} className="p-4 bg-surface rounded-lg border border-border">
                        <div className="flex items-center justify-between mb-4">
                          <h4 className="font-medium text-text-primary">{file.name}</h4>
                          <span className={`badge ${validation.isValid ? 'badge-success' : 'badge-error'}`}>
                            {validation.isValid ? 'Valid' : 'Invalid'}
                          </span>
                        </div>
                        
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                          <div className="text-center">
                            <div className="text-2xl font-bold text-primary-500">{validation.score}%</div>
                            <div className="text-sm text-text-secondary">Validation Score</div>
                          </div>
                          <div className="text-center">
                            <div className="text-2xl font-bold text-error-500">{validation.errors.length}</div>
                            <div className="text-sm text-text-secondary">Errors</div>
                          </div>
                          <div className="text-center">
                            <div className="text-2xl font-bold text-warning-500">{validation.warnings.length}</div>
                            <div className="text-sm text-text-secondary">Warnings</div>
                          </div>
                        </div>
                        
                        {validation.errors.length > 0 && (
                          <div className="mt-4">
                            <h5 className="font-medium text-error-500 mb-2">Errors:</h5>
                            <ul className="space-y-1">
                              {validation.errors.map((error, index) => (
                                <li key={index} className="text-sm text-text-secondary flex items-center gap-2">
                                  <span className="text-error-500">•</span>
                                  {error}
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                        
                        {validation.warnings.length > 0 && (
                          <div className="mt-4">
                            <h5 className="font-medium text-warning-500 mb-2">Warnings:</h5>
                            <ul className="space-y-1">
                              {validation.warnings.map((warning, index) => (
                                <li key={index} className="text-sm text-text-secondary flex items-center gap-2">
                                  <span className="text-warning-500">⚠</span>
                                  {warning}
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          )}

          {/* Quality Tab */}
          {activeTab === 'quality' && (
            <div className="card">
              <div className="card-header">
                <h3 className="text-lg font-semibold text-text-primary">📊 Data Quality</h3>
                <p className="text-sm text-text-secondary">Quality metrics and scoring</p>
              </div>
              <div className="card-body">
                <div className="space-y-4">
                  {Object.entries(dataQuality).map(([fileId, quality]) => {
                    const file = uploadedFiles.find(f => f.id === fileId);
                    if (!file) return null;
                    
                    return (
                      <div key={fileId} className="p-4 bg-surface rounded-lg border border-border">
                        <div className="flex items-center justify-between mb-4">
                          <h4 className="font-medium text-text-primary">{file.name}</h4>
                          <span className={`badge ${quality.overall >= 80 ? 'badge-success' : quality.overall >= 60 ? 'badge-warning' : 'badge-error'}`}>
                            {quality.overall}% Quality Score
                          </span>
                        </div>
                        
                        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                          <div className="text-center">
                            <div className="text-lg font-bold text-primary-500">{quality.completeness}%</div>
                            <div className="text-xs text-text-secondary">Completeness</div>
                          </div>
                          <div className="text-center">
                            <div className="text-lg font-bold text-primary-500">{quality.accuracy}%</div>
                            <div className="text-xs text-text-secondary">Accuracy</div>
                          </div>
                          <div className="text-center">
                            <div className="text-lg font-bold text-primary-500">{quality.consistency}%</div>
                            <div className="text-xs text-text-secondary">Consistency</div>
                          </div>
                          <div className="text-center">
                            <div className="text-lg font-bold text-primary-500">{quality.timeliness}%</div>
                            <div className="text-xs text-text-secondary">Timeliness</div>
                          </div>
                          <div className="text-center">
                            <div className="text-lg font-bold text-primary-500">{quality.overall}%</div>
                            <div className="text-xs text-text-secondary">Overall</div>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          )}

          {/* Database Tab */}
          {activeTab === 'database' && (
            <div className="space-y-6">
              <div className="card">
                <div className="card-header">
                  <h3 className="text-lg font-semibold text-text-primary">🗄️ Database Health</h3>
                  <p className="text-sm text-text-secondary">System status and performance</p>
                </div>
                <div className="card-body">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="text-center p-4 bg-surface rounded-lg border border-border">
                      <div className="text-3xl font-bold text-success-500">99.9%</div>
                      <div className="text-sm text-text-secondary">Uptime</div>
                    </div>
                    <div className="text-center p-4 bg-surface rounded-lg border border-border">
                      <div className="text-3xl font-bold text-primary-500">2.3ms</div>
                      <div className="text-sm text-text-secondary">Avg Response Time</div>
                    </div>
                    <div className="text-center p-4 bg-surface rounded-lg border border-border">
                      <div className="text-3xl font-bold text-warning-500">1,247</div>
                      <div className="text-sm text-text-secondary">Active Connections</div>
                    </div>
                  </div>
                </div>
              </div>

              <div className="card">
                <div className="card-header">
                  <h3 className="text-lg font-semibold text-text-primary">💾 Storage Analytics</h3>
                  <p className="text-sm text-text-secondary">Storage usage and optimization</p>
                </div>
                <div className="card-body">
                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-text-secondary">Database Size</span>
                      <span className="text-sm font-medium text-text-primary">2.4 GB</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div className="bg-primary-500 h-2 rounded-full" style={{ width: '65%' }}></div>
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-text-secondary">Index Size</span>
                      <span className="text-sm font-medium text-text-primary">450 MB</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div className="bg-success-500 h-2 rounded-full" style={{ width: '25%' }}></div>
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-text-secondary">Backup Size</span>
                      <span className="text-sm font-medium text-text-primary">1.8 GB</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div className="bg-warning-500 h-2 rounded-full" style={{ width: '45%' }}></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Lineage Tab */}
          {activeTab === 'lineage' && (
            <div className="card">
              <div className="card-header">
                <h3 className="text-lg font-semibold text-text-primary">🔄 Data Lineage</h3>
                <p className="text-sm text-text-secondary">Data flow and transformation tracking</p>
              </div>
              <div className="card-body">
                <div className="space-y-4">
                  {[
                    { id: 1, source: 'property_data.csv', transformation: 'Data Cleaning', target: 'properties_table', timestamp: '2024-01-15 10:30' },
                    { id: 2, source: 'market_data.xlsx', transformation: 'Aggregation', target: 'market_analytics', timestamp: '2024-01-15 09:15' },
                    { id: 3, source: 'client_data.json', transformation: 'Validation', target: 'clients_table', timestamp: '2024-01-15 08:45' }
                  ].map(item => (
                    <div key={item.id} className="flex items-center gap-4 p-4 bg-surface rounded-lg border border-border">
                      <div className="w-8 h-8 bg-gradient-to-br from-primary-500 to-primary-300 rounded-full flex items-center justify-center text-white text-sm font-bold">
                        {item.id}
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center gap-2 text-sm">
                          <span className="text-text-secondary">{item.source}</span>
                          <span className="text-primary-500">→</span>
                          <span className="text-warning-500">{item.transformation}</span>
                          <span className="text-primary-500">→</span>
                          <span className="text-text-primary">{item.target}</span>
                        </div>
                        <div className="text-xs text-text-tertiary mt-1">
                          {item.timestamp}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AdminDataManagement;
