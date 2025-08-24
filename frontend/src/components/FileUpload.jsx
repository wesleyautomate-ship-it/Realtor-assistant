import React, { useState, useRef, useCallback } from 'react';
import axios from 'axios';
import './FileUpload.css';

const FileUpload = ({ onFileUploaded, role = 'client' }) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const fileInputRef = useRef(null);

  // Supported file types
  const supportedTypes = [
    'application/pdf',
    'text/csv',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/json',
    'text/plain',
    'image/jpeg',
    'image/png',
    'image/gif'
  ];

  // File size limit (10MB)
  const maxFileSize = 10 * 1024 * 1024;

  const validateFile = (file) => {
    const errors = [];

    // Check file type
    if (!supportedTypes.includes(file.type)) {
      errors.push(`File type ${file.type} is not supported`);
    }

    // Check file size
    if (file.size > maxFileSize) {
      errors.push(`File size ${(file.size / 1024 / 1024).toFixed(2)}MB exceeds limit of 10MB`);
    }

    return errors;
  };

  const uploadFile = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('role', role);

    try {
      setUploading(true);
      setError(null);
      setUploadProgress(0);

      const response = await axios.post('http://localhost:8001/upload-file', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          setUploadProgress(progress);
        },
      });

      // Backend returns FileUploadResponse directly, no success field
      setSuccess(`File "${file.name}" uploaded successfully!`);
      setUploadedFiles(prev => [...prev, {
        name: file.name,
        size: file.size,
        type: file.type,
        uploadedAt: new Date().toISOString(),
        id: response.data.file_id || Date.now()
      }]);
      
      // Call parent callback if provided
      if (onFileUploaded) {
        onFileUploaded(response.data);
      }
    } catch (err) {
      setError(err.response?.data?.detail || err.response?.data?.message || err.message || 'Upload failed');
    } finally {
      setUploading(false);
      setUploadProgress(0);
    }
  };

  const handleFileSelect = useCallback((files) => {
    const fileArray = Array.from(files);
    
    fileArray.forEach(file => {
      const validationErrors = validateFile(file);
      
      if (validationErrors.length > 0) {
        setError(`Validation failed for ${file.name}: ${validationErrors.join(', ')}`);
        return;
      }

      uploadFile(file);
    });
  }, [role]);

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
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFileSelect(files);
    }
  }, [handleFileSelect]);

  const handleFileInputChange = (e) => {
    const files = e.target.files;
    if (files.length > 0) {
      handleFileSelect(files);
    }
  };

  const handleBrowseClick = () => {
    fileInputRef.current?.click();
  };

  const removeFile = (fileId) => {
    setUploadedFiles(prev => prev.filter(file => file.id !== fileId));
  };

  const clearMessages = () => {
    setError(null);
    setSuccess(null);
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getFileIcon = (fileType) => {
    if (fileType.includes('pdf')) return '📄';
    if (fileType.includes('csv') || fileType.includes('excel')) return '📊';
    if (fileType.includes('json')) return '📋';
    if (fileType.includes('image')) return '🖼️';
    if (fileType.includes('text')) return '📝';
    return '📎';
  };

  return (
    <div className="file-upload-container">
      <div className="file-upload-header">
        <h3>📁 File Upload</h3>
        <p>Upload documents, property data, or images for analysis</p>
      </div>

      {/* Error and Success Messages */}
      {error && (
        <div className="upload-message error" onClick={clearMessages}>
          <span>❌ {error}</span>
          <button className="close-btn">×</button>
        </div>
      )}
      
      {success && (
        <div className="upload-message success" onClick={clearMessages}>
          <span>✅ {success}</span>
          <button className="close-btn">×</button>
        </div>
      )}

      {/* Upload Area */}
      <div 
        className={`upload-area ${isDragOver ? 'drag-over' : ''} ${uploading ? 'uploading' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        {uploading ? (
          <div className="upload-progress">
            <div className="progress-bar">
              <div 
                className="progress-fill" 
                style={{ width: `${uploadProgress}%` }}
              ></div>
            </div>
            <p>Uploading... {uploadProgress}%</p>
          </div>
        ) : (
          <>
            <div className="upload-icon">📤</div>
            <h4>Drag & Drop Files Here</h4>
            <p>or</p>
            <button 
              className="browse-btn"
              onClick={handleBrowseClick}
              disabled={uploading}
            >
              Browse Files
            </button>
            <div className="file-info">
              <p><strong>Supported formats:</strong> PDF, CSV, Excel, JSON, Images</p>
              <p><strong>Maximum size:</strong> 10MB per file</p>
            </div>
          </>
        )}
      </div>

      {/* Hidden file input */}
      <input
        ref={fileInputRef}
        type="file"
        multiple
        accept={supportedTypes.join(',')}
        onChange={handleFileInputChange}
        style={{ display: 'none' }}
      />

      {/* Uploaded Files List */}
      {uploadedFiles.length > 0 && (
        <div className="uploaded-files">
          <h4>📋 Uploaded Files</h4>
          <div className="files-list">
            {uploadedFiles.map((file) => (
              <div key={file.id} className="file-item">
                <div className="file-info">
                  <span className="file-icon">{getFileIcon(file.type)}</span>
                  <div className="file-details">
                    <span className="file-name">{file.name}</span>
                    <span className="file-size">{formatFileSize(file.size)}</span>
                    <span className="file-date">
                      {new Date(file.uploadedAt).toLocaleString()}
                    </span>
                  </div>
                </div>
                <button 
                  className="remove-btn"
                  onClick={() => removeFile(file.id)}
                  title="Remove file"
                >
                  🗑️
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Role-based Information */}
      <div className="role-info">
        <h4>👤 Current Role: {role.charAt(0).toUpperCase() + role.slice(1)}</h4>
        <div className="role-capabilities">
          {role === 'client' && (
            <p>You can upload property documents and images for analysis.</p>
          )}
          {role === 'agent' && (
            <p>You can upload property data, client documents, and market reports.</p>
          )}
          {role === 'listing_agent' && (
            <p>You have full access to upload all types of documents and data.</p>
          )}
          {role === 'manager' && (
            <p>You have complete access to upload and manage all system files.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default FileUpload;
