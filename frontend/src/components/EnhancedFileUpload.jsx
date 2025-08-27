import React, { useState, useRef, useCallback, useEffect } from 'react';

const EnhancedFileUpload = ({ onFileUpload, selectedRole, onAnalysisComplete }) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState({});
  const [analyzing, setAnalyzing] = useState(false);
  const [analysisResults, setAnalysisResults] = useState({});
  const [previewData, setPreviewData] = useState({});
  const [selectedFile, setSelectedFile] = useState(null);
  const [notifications, setNotifications] = useState([]);
  const fileInputRef = useRef(null);

  const supportedFormats = ['PDF', 'CSV', 'Excel', 'JSON', 'Images', 'Word', 'Text'];
  const maxFileSize = 10; // MB

  // Helper function to add notifications
  const addNotification = (message, type = 'info') => {
    const id = Date.now();
    setNotifications(prev => [...prev, { id, message, type }]);
    
    // Auto-remove notification after 5 seconds
    setTimeout(() => {
      setNotifications(prev => prev.filter(n => n.id !== id));
    }, 5000);
  };

  // Helper function to remove notification
  const removeNotification = (id) => {
    setNotifications(prev => prev.filter(n => n.id !== id));
  };

  // AI Analysis Types
  const analysisTypes = {
    'image': ['Property Analysis', 'Quality Assessment', 'Location Detection', 'Value Estimation'],
    'pdf': ['Document Analysis', 'Content Extraction', 'Legal Review', 'Property Details'],
    'csv': ['Data Analysis', 'Market Trends', 'Property Comparison', 'Statistical Insights'],
    'excel': ['Spreadsheet Analysis', 'Financial Data', 'Market Reports', 'Investment Analysis'],
    'word': ['Document Review', 'Contract Analysis', 'Legal Compliance', 'Content Summary'],
    'text': ['Text Analysis', 'Sentiment Analysis', 'Key Information', 'Summary Generation']
  };

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    setIsDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e) => {
    e.preventDefault();
    setIsDragOver(false);
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setIsDragOver(false);
    
    const files = Array.from(e.dataTransfer.files);
    handleFiles(files);
  }, []);

  const handleFileSelect = useCallback((e) => {
    const files = Array.from(e.target.files);
    handleFiles(files);
  }, []);

  const handleFiles = async (files) => {
    const validFiles = files.filter(file => {
      const isValidFormat = supportedFormats.some(format => 
        file.type.includes(format.toLowerCase()) || 
        file.name.toLowerCase().endsWith(format.toLowerCase())
      );
      
      const isValidSize = file.size <= maxFileSize * 1024 * 1024;
      
      if (!isValidFormat) {
        addNotification(`Unsupported file format: ${file.name}`, 'error');
      }
      if (!isValidSize) {
        addNotification(`File too large: ${file.name} (max ${maxFileSize}MB)`, 'error');
      }
      
      return isValidFormat && isValidSize;
    });

    if (validFiles.length === 0) return;

    setUploading(true);
    
    // Initialize upload progress for each file
    const newProgress = {};
    validFiles.forEach(file => {
      newProgress[file.name] = 0;
    });
    setUploadProgress(newProgress);

    const uploadedFiles = [];

    // Simulate file upload with progress
    for (const file of validFiles) {
      try {
        // Simulate upload progress
        for (let i = 0; i <= 100; i += 10) {
          await new Promise(resolve => setTimeout(resolve, 100));
          setUploadProgress(prev => ({
            ...prev,
            [file.name]: i
          }));
        }

        const uploadedFile = {
          id: Date.now() + Math.random(),
          name: file.name,
          size: file.size,
          type: file.type,
          uploadedAt: new Date().toISOString(),
          status: 'uploaded',
          progress: 100
        };

        uploadedFiles.push(uploadedFile);
        addNotification(`Successfully uploaded: ${file.name}`, 'success');

      } catch (error) {
        addNotification(`Failed to upload: ${file.name}`, 'error');
      }
    }

    setUploadedFiles(prev => [...prev, ...uploadedFiles]);
    setUploading(false);
    setUploadProgress({});

    // Call the parent component's onFileUpload callback
    if (onFileUpload) {
      onFileUpload(uploadedFiles);
    }
  };

  const handleAnalyzeFile = async (file) => {
    setAnalyzing(true);
    setSelectedFile(file);

    try {
      // Simulate AI analysis
      await new Promise(resolve => setTimeout(resolve, 2000));

      const analysisResult = {
        fileId: file.id,
        analysisType: 'Property Analysis',
        insights: [
          'Property value estimated at AED 2.5M',
          'Market trend analysis shows 15% appreciation',
          'Location score: 8.5/10',
          'Investment potential: High'
        ],
        recommendations: [
          'Consider this property for investment',
          'Market timing is favorable',
          'Location has good growth potential'
        ],
        confidence: 0.85
      };

      setAnalysisResults(prev => ({
        ...prev,
        [file.id]: analysisResult
      }));

      addNotification(`Analysis completed for: ${file.name}`, 'success');

      if (onAnalysisComplete) {
        onAnalysisComplete(analysisResult);
      }

    } catch (error) {
      addNotification(`Analysis failed for: ${file.name}`, 'error');
    } finally {
      setAnalyzing(false);
    }
  };

  const handlePreviewFile = (file) => {
    setSelectedFile(file);
    
    // Simulate file preview data
    const preview = {
      content: `Sample content from ${file.name}...`,
      metadata: {
        size: file.size,
        type: file.type,
        uploadedAt: file.uploadedAt
      }
    };
    
    setPreviewData(prev => ({
      ...prev,
      [file.id]: preview
    }));
  };

  const removeFile = (fileId) => {
    setUploadedFiles(prev => prev.filter(f => f.id !== fileId));
    setAnalysisResults(prev => {
      const newResults = { ...prev };
      delete newResults[fileId];
      return newResults;
    });
    setPreviewData(prev => {
      const newPreview = { ...prev };
      delete newPreview[fileId];
      return newPreview;
    });
    
    if (selectedFile && selectedFile.id === fileId) {
      setSelectedFile(null);
    }
  };

  const getFileIcon = (fileName) => {
    const extension = fileName.split('.').pop()?.toLowerCase();
    const icons = {
      pdf: '📄',
      csv: '📊',
      xlsx: '📈',
      xls: '📈',
      doc: '📝',
      docx: '📝',
      txt: '📄',
      jpg: '🖼️',
      jpeg: '🖼️',
      png: '🖼️',
      json: '⚙️'
    };
    return icons[extension] || '📁';
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="upload-container">
      {/* Header */}
      <div className="upload-header">
        <div className="flex items-center justify-between w-full p-6">
          <div className="flex items-center">
            <div className="w-12 h-12 bg-gradient-to-br from-primary-500 to-primary-300 rounded-full flex items-center justify-center text-2xl font-bold text-secondary-50 mr-4 shadow-lg">
              📁
            </div>
            <div>
              <h1 className="text-2xl font-bold text-primary-500">Enhanced File Upload</h1>
              <p className="text-sm text-text-secondary">
                Upload and analyze real estate documents with AI
              </p>
            </div>
          </div>
          
          <div className="flex items-center gap-4">
            <span className="text-sm text-text-secondary">
              {uploadedFiles.length} files uploaded
            </span>
          </div>
        </div>
      </div>

      {/* Notifications */}
      {notifications.length > 0 && (
        <div className="fixed top-4 right-4 z-50 space-y-2">
          {notifications.map(notification => (
            <div
              key={notification.id}
              className={`p-4 rounded-lg shadow-lg max-w-sm ${
                notification.type === 'success' ? 'bg-success-100 text-success-800' :
                notification.type === 'error' ? 'bg-error-100 text-error-800' :
                'bg-primary-100 text-primary-800'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="text-sm">{notification.message}</span>
                <button
                  onClick={() => removeNotification(notification.id)}
                  className="ml-2 text-lg hover:opacity-70"
                >
                  ×
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="p-6 space-y-6">
        {/* Upload Zone */}
        <div className="card">
          <div className="card-header">
            <h3 className="text-lg font-semibold text-text-primary">Upload Files</h3>
          </div>
          <div className="card-body">
            <div
              className={`upload-zone ${isDragOver ? 'drag-over' : ''} ${uploading ? 'uploading' : ''}`}
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
                  {uploading ? 'Uploading...' : 'Drop files here or click to browse'}
                </h3>
                <p className="text-text-secondary mb-4">
                  Support for PDF, CSV, Excel, Word, Images, and more
                </p>
                <p className="text-sm text-text-tertiary">
                  Max file size: {maxFileSize}MB
                </p>
              </div>
              
              <input
                ref={fileInputRef}
                type="file"
                multiple
                onChange={handleFileSelect}
                className="hidden"
                accept=".pdf,.csv,.xlsx,.xls,.doc,.docx,.txt,.jpg,.jpeg,.png,.json"
              />
            </div>
          </div>
        </div>

        {/* Upload Progress */}
        {Object.keys(uploadProgress).length > 0 && (
          <div className="card">
            <div className="card-header">
              <h3 className="text-lg font-semibold text-text-primary">Upload Progress</h3>
            </div>
            <div className="card-body">
              {Object.entries(uploadProgress).map(([fileName, progress]) => (
                <div key={fileName} className="mb-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-text-secondary">{fileName}</span>
                    <span className="text-sm text-text-secondary">{progress}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-gradient-to-r from-primary-500 to-primary-300 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${progress}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Uploaded Files */}
        {uploadedFiles.length > 0 && (
          <div className="card">
            <div className="card-header">
              <h3 className="text-lg font-semibold text-text-primary">Uploaded Files</h3>
            </div>
            <div className="card-body">
              <div className="space-y-4">
                {uploadedFiles.map(file => (
                  <div key={file.id} className="flex items-center justify-between p-4 bg-surface rounded-lg border border-border">
                    <div className="flex items-center gap-4">
                      <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-primary-300 rounded-lg flex items-center justify-center text-xl">
                        {getFileIcon(file.name)}
                      </div>
                      <div>
                        <h4 className="font-medium text-text-primary">{file.name}</h4>
                        <p className="text-sm text-text-secondary">
                          {formatFileSize(file.size)} • {new Date(file.uploadedAt).toLocaleDateString()}
                        </p>
                      </div>
                    </div>
                    
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => handlePreviewFile(file)}
                        className="btn btn-secondary btn-sm"
                      >
                        👁️ Preview
                      </button>
                      <button
                        onClick={() => handleAnalyzeFile(file)}
                        disabled={analyzing}
                        className="btn btn-primary btn-sm"
                      >
                        {analyzing && selectedFile?.id === file.id ? (
                          <span className="flex items-center gap-2">
                            <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin"></div>
                            Analyzing...
                          </span>
                        ) : (
                          '🤖 Analyze'
                        )}
                      </button>
                      <button
                        onClick={() => removeFile(file.id)}
                        className="btn btn-ghost btn-sm text-error-500 hover:text-error-600"
                      >
                        🗑️
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Analysis Results */}
        {Object.keys(analysisResults).length > 0 && (
          <div className="card">
            <div className="card-header">
              <h3 className="text-lg font-semibold text-text-primary">AI Analysis Results</h3>
            </div>
            <div className="card-body">
              <div className="space-y-6">
                {Object.values(analysisResults).map(result => (
                  <div key={result.fileId} className="p-4 bg-surface rounded-lg border border-border">
                    <div className="flex items-center justify-between mb-4">
                      <h4 className="font-semibold text-text-primary">{result.analysisType}</h4>
                      <span className="badge badge-primary">
                        Confidence: {(result.confidence * 100).toFixed(0)}%
                      </span>
                    </div>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <h5 className="font-medium text-text-primary mb-2">Key Insights</h5>
                        <ul className="space-y-1">
                          {result.insights.map((insight, index) => (
                            <li key={index} className="text-sm text-text-secondary flex items-center gap-2">
                              <span className="text-primary-500">•</span>
                              {insight}
                            </li>
                          ))}
                        </ul>
                      </div>
                      
                      <div>
                        <h5 className="font-medium text-text-primary mb-2">Recommendations</h5>
                        <ul className="space-y-1">
                          {result.recommendations.map((rec, index) => (
                            <li key={index} className="text-sm text-text-secondary flex items-center gap-2">
                              <span className="text-success-500">✓</span>
                              {rec}
                            </li>
                          ))}
                        </ul>
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
  );
};

export default EnhancedFileUpload;
