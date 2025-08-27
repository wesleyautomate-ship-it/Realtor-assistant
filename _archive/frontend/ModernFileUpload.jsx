import React, { useState, useRef, useCallback } from 'react';

const ModernFileUpload = ({ onFileUpload, selectedRole }) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState({});
  const fileInputRef = useRef(null);

  const supportedFormats = ['PDF', 'CSV', 'Excel', 'JSON', 'Images'];
  const maxFileSize = 10; // MB

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
        alert(`Unsupported file format: ${file.name}`);
      }
      if (!isValidSize) {
        alert(`File too large: ${file.name} (max ${maxFileSize}MB)`);
      }
      
      return isValidFormat && isValidSize;
    });

    if (validFiles.length === 0) return;

    setUploading(true);
    
    // Simulate upload progress for each file
    const newProgress = {};
    validFiles.forEach(file => {
      newProgress[file.name] = 0;
    });
    setUploadProgress(newProgress);

    // Simulate upload process
    for (const file of validFiles) {
      for (let progress = 0; progress <= 100; progress += 10) {
        await new Promise(resolve => setTimeout(resolve, 100));
        setUploadProgress(prev => ({
          ...prev,
          [file.name]: progress
        }));
      }
    }

    // Add files to uploaded list
    const newFiles = validFiles.map(file => ({
      id: Date.now() + Math.random(),
      name: file.name,
      size: file.size,
      type: file.type,
      uploadedAt: new Date(),
      status: 'completed'
    }));

    setUploadedFiles(prev => [...prev, ...newFiles]);
    setUploading(false);
    setUploadProgress({});

    // Call the parent upload handler
    if (onFileUpload) {
      onFileUpload(validFiles);
    }
  };

  const removeFile = (fileId) => {
    setUploadedFiles(prev => prev.filter(file => file.id !== fileId));
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getFileIcon = (fileName, fileType) => {
    const extension = fileName.split('.').pop()?.toLowerCase();
    
    if (fileType.includes('pdf')) return '📄';
    if (fileType.includes('csv') || extension === 'csv') return '📊';
    if (fileType.includes('excel') || extension === 'xlsx' || extension === 'xls') return '📈';
    if (fileType.includes('json') || extension === 'json') return '⚙️';
    if (fileType.includes('image')) return '🖼️';
    
    return '📁';
  };

  const getRoleDescription = (role) => {
    const descriptions = {
      client: 'Upload property preferences, requirements, or documents for analysis',
      agent: 'Upload property data, client documents, and market reports',
      employee: 'Upload company documents, policies, and internal reports',
      admin: 'Upload system configurations, user data, and administrative documents'
    };
    return descriptions[role] || descriptions.client;
  };

  return (
    <div className="modern-upload-container">
      {/* Header */}
      <div className="upload-header">
        <div className="header-content">
          <div className="header-title">
            <div className="title-icon">📁</div>
            <div className="title-text">
              <h1 className="page-title">File Upload</h1>
              <p className="page-subtitle">Upload documents, property data, or images for analysis</p>
            </div>
          </div>
        </div>
      </div>

      {/* Upload Area */}
      <div className="upload-section">
        <div className="upload-content">
          {/* Drag & Drop Zone */}
          <div
            className={`upload-zone ${isDragOver ? 'drag-over' : ''} ${uploading ? 'uploading' : ''}`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
          >
            <div className="upload-zone-content">
              <div className="upload-icon">
                <span className="icon-symbol">☁️</span>
              </div>
              
              <h3 className="upload-title">
                {uploading ? 'Uploading Files...' : 'Drag & Drop Files Here'}
              </h3>
              
              <p className="upload-description">
                {uploading 
                  ? 'Please wait while your files are being processed'
                  : 'or click to browse files from your computer'
                }
              </p>
              
              {!uploading && (
                <button className="btn btn-primary btn-lg browse-btn">
                  <span className="btn-icon">📂</span>
                  Browse Files
                </button>
              )}
            </div>
            
            {/* Hidden file input */}
            <input
              ref={fileInputRef}
              type="file"
              multiple
              accept=".pdf,.csv,.xlsx,.xls,.json,.jpg,.jpeg,.png,.gif"
              onChange={handleFileSelect}
              style={{ display: 'none' }}
            />
          </div>

          {/* File Format Info */}
          <div className="upload-info">
            <div className="info-section">
              <h4 className="info-title">Supported Formats</h4>
              <div className="format-tags">
                {supportedFormats.map(format => (
                  <span key={format} className="format-tag">{format}</span>
                ))}
              </div>
            </div>
            
            <div className="info-section">
              <h4 className="info-title">File Size Limit</h4>
              <p className="info-text">Maximum {maxFileSize}MB per file</p>
            </div>
          </div>

          {/* Upload Progress */}
          {Object.keys(uploadProgress).length > 0 && (
            <div className="upload-progress">
              <h4 className="progress-title">Uploading Files</h4>
              {Object.entries(uploadProgress).map(([fileName, progress]) => (
                <div key={fileName} className="progress-item">
                  <div className="progress-info">
                    <span className="progress-filename">{fileName}</span>
                    <span className="progress-percentage">{progress}%</span>
                  </div>
                  <div className="progress-bar">
                    <div 
                      className="progress-fill"
                      style={{ width: `${progress}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Uploaded Files */}
          {uploadedFiles.length > 0 && (
            <div className="uploaded-files">
              <div className="files-header">
                <h4 className="files-title">Uploaded Files</h4>
                <span className="files-count">{uploadedFiles.length} files</span>
              </div>
              
              <div className="files-list">
                {uploadedFiles.map(file => (
                  <div key={file.id} className="file-item">
                    <div className="file-info">
                      <div className="file-icon">
                        <span className="icon">{getFileIcon(file.name, file.type)}</span>
                      </div>
                      
                      <div className="file-details">
                        <div className="file-name">{file.name}</div>
                        <div className="file-meta">
                          <span className="file-size">{formatFileSize(file.size)}</span>
                          <span className="file-date">
                            {file.uploadedAt.toLocaleDateString()}
                          </span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="file-actions">
                      <span className={`status-badge badge-${file.status}`}>
                        {file.status}
                      </span>
                      <button
                        className="btn btn-ghost btn-sm remove-btn"
                        onClick={() => removeFile(file.id)}
                        title="Remove file"
                      >
                        <span className="btn-icon">🗑️</span>
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Role Information */}
      <div className="role-info">
        <div className="role-content">
          <div className="role-header">
            <span className="role-icon">👤</span>
            <span className="role-label">Current Role: {selectedRole.charAt(0).toUpperCase() + selectedRole.slice(1)}</span>
          </div>
          <p className="role-description">{getRoleDescription(selectedRole)}</p>
        </div>
      </div>
    </div>
  );
};

export default ModernFileUpload;
