"""
File Security Utilities for Dubai Real Estate RAG System

This module provides secure file upload validation, disk space monitoring,
and strict cleanup of temporary files to prevent security vulnerabilities
and resource exhaustion attacks.
"""

import os
import shutil
import tempfile
import hashlib
import mimetypes
from pathlib import Path
from typing import Optional, Tuple, List, Dict, Any
from fastapi import HTTPException, UploadFile
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Security configuration
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
MAX_TOTAL_UPLOAD_SIZE = 500 * 1024 * 1024  # 500MB
MIN_DISK_SPACE_MB = 1000  # 1GB minimum free space
ALLOWED_EXTENSIONS = {
    '.pdf', '.docx', '.doc', '.txt', '.csv', '.xlsx', '.xls',
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'
}
ALLOWED_MIME_TYPES = {
    'application/pdf',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/msword',
    'text/plain',
    'text/csv',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.ms-excel',
    'image/jpeg',
    'image/png',
    'image/gif',
    'image/bmp',
    'image/tiff'
}

# Dangerous file extensions to block
BLOCKED_EXTENSIONS = {
    '.exe', '.bat', '.cmd', '.com', '.pif', '.scr', '.vbs', '.js',
    '.jar', '.war', '.ear', '.class', '.php', '.asp', '.aspx',
    '.jsp', '.py', '.pl', '.sh', '.bash', '.ps1', '.psm1'
}

class FileSecurityError(Exception):
    """Custom exception for file security violations"""
    pass

class FileSecurityManager:
    """Manages secure file operations and validation"""
    
    def __init__(self, upload_dir: str, temp_dir: str = None):
        self.upload_dir = Path(upload_dir)
        self.temp_dir = Path(temp_dir) if temp_dir else Path(tempfile.gettempdir()) / "rag_uploads"
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        # Track uploads for cleanup
        self.upload_sessions: Dict[str, Dict[str, Any]] = {}
        
    def validate_file_upload(self, file: UploadFile, user_id: int) -> Tuple[bool, str]:
        """
        Comprehensive file upload validation
        
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        try:
            # 1. Check file size
            if not self._validate_file_size(file):
                return False, f"File size exceeds maximum limit of {MAX_FILE_SIZE / (1024*1024):.1f}MB"
            
            # 2. Check file extension
            if not self._validate_file_extension(file):
                return False, "File type not allowed"
            
            # 3. Check MIME type
            if not self._validate_mime_type(file):
                return False, "File MIME type not allowed"
            
            # 4. Check for dangerous content
            if not self._validate_file_content(file):
                return False, "File contains potentially dangerous content"
            
            # 5. Check disk space
            if not self._check_disk_space(file.size or 0):
                return False, "Insufficient disk space"
            
            # 6. Check upload limits
            if not self._check_upload_limits(user_id, file.size or 0):
                return False, "Upload limit exceeded"
            
            return True, "File validation passed"
            
        except Exception as e:
            logger.error(f"File validation error: {e}")
            return False, f"File validation failed: {str(e)}"
    
    def _validate_file_size(self, file: UploadFile) -> bool:
        """Validate file size against maximum limit"""
        if file.size is None:
            return False
        
        return file.size <= MAX_FILE_SIZE
    
    def _validate_file_extension(self, file: UploadFile) -> bool:
        """Validate file extension"""
        if not file.filename:
            return False
        
        file_ext = Path(file.filename).suffix.lower()
        
        # Check blocked extensions
        if file_ext in BLOCKED_EXTENSIONS:
            logger.warning(f"Blocked file extension attempted: {file_ext}")
            return False
        
        # Check allowed extensions
        return file_ext in ALLOWED_EXTENSIONS
    
    def _validate_mime_type(self, file: UploadFile) -> bool:
        """Validate MIME type"""
        if not file.content_type:
            return False
        
        return file.content_type in ALLOWED_MIME_TYPES
    
    def _validate_file_content(self, file: UploadFile) -> bool:
        """Validate file content for dangerous patterns"""
        try:
            # Read first 1KB to check for dangerous patterns
            content = file.file.read(1024)
            file.file.seek(0)  # Reset file pointer
            
            # Check for executable patterns
            dangerous_patterns = [
                b'MZ',  # Windows executable
                b'\x7fELF',  # Linux executable
                b'#!/',  # Shell script
                b'<?php',  # PHP script
                b'<script',  # JavaScript
                b'<html',  # HTML with potential scripts
            ]
            
            for pattern in dangerous_patterns:
                if pattern in content:
                    logger.warning(f"Dangerous content pattern detected: {pattern}")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Content validation error: {e}")
            return False
    
    def _check_disk_space(self, file_size: int) -> bool:
        """Check available disk space"""
        try:
            statvfs = os.statvfs(self.upload_dir)
            free_space = statvfs.f_frsize * statvfs.f_bavail
            required_space = file_size + (MIN_DISK_SPACE_MB * 1024 * 1024)
            
            return free_space >= required_space
            
        except Exception as e:
            logger.error(f"Disk space check error: {e}")
            return False
    
    def _check_upload_limits(self, user_id: int, file_size: int) -> bool:
        """Check user upload limits"""
        try:
            # Get user's total upload size in the last 24 hours
            user_session_key = f"user_{user_id}"
            if user_session_key in self.upload_sessions:
                session_data = self.upload_sessions[user_session_key]
                if datetime.now() - session_data['start_time'] < timedelta(hours=24):
                    total_size = session_data['total_size'] + file_size
                    if total_size > MAX_TOTAL_UPLOAD_SIZE:
                        return False
                    session_data['total_size'] = total_size
                else:
                    # Reset session after 24 hours
                    self.upload_sessions[user_session_key] = {
                        'start_time': datetime.now(),
                        'total_size': file_size
                    }
            else:
                # Create new session
                self.upload_sessions[user_session_key] = {
                    'start_time': datetime.now(),
                    'total_size': file_size
                }
            
            return True
            
        except Exception as e:
            logger.error(f"Upload limit check error: {e}")
            return False
    
    def create_secure_temp_file(self, file: UploadFile, user_id: int) -> Path:
        """Create a secure temporary file with proper permissions"""
        try:
            # Generate secure filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_hash = hashlib.md5(f"{file.filename}_{timestamp}".encode()).hexdigest()[:8]
            safe_filename = f"upload_{user_id}_{timestamp}_{file_hash}{Path(file.filename).suffix}"
            
            temp_file_path = self.temp_dir / safe_filename
            
            # Create temporary file with restricted permissions
            with open(temp_file_path, 'wb') as temp_file:
                shutil.copyfileobj(file.file, temp_file)
            
            # Set restrictive permissions (owner read/write only)
            os.chmod(temp_file_path, 0o600)
            
            logger.info(f"Created secure temp file: {temp_file_path}")
            return temp_file_path
            
        except Exception as e:
            logger.error(f"Error creating secure temp file: {e}")
            raise FileSecurityError(f"Failed to create secure temporary file: {str(e)}")
    
    def move_to_upload_dir(self, temp_file: Path, original_filename: str, user_id: int) -> Path:
        """Move temporary file to upload directory with secure naming"""
        try:
            # Generate secure final filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_hash = hashlib.md5(f"{original_filename}_{timestamp}".encode()).hexdigest()[:12]
            safe_filename = f"file_{user_id}_{timestamp}_{file_hash}{Path(original_filename).suffix}"
            
            final_path = self.upload_dir / safe_filename
            
            # Move file
            shutil.move(str(temp_file), str(final_path))
            
            # Set appropriate permissions
            os.chmod(final_path, 0o644)
            
            logger.info(f"Moved file to upload directory: {final_path}")
            return final_path
            
        except Exception as e:
            logger.error(f"Error moving file to upload directory: {e}")
            # Clean up temp file if move fails
            self.cleanup_temp_file(temp_file)
            raise FileSecurityError(f"Failed to move file to upload directory: {str(e)}")
    
    def cleanup_temp_file(self, temp_file: Path) -> bool:
        """Safely cleanup temporary file"""
        try:
            if temp_file.exists():
                temp_file.unlink()
                logger.info(f"Cleaned up temp file: {temp_file}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error cleaning up temp file {temp_file}: {e}")
            return False
    
    def cleanup_old_temp_files(self, max_age_hours: int = 24) -> int:
        """Clean up old temporary files"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
            cleaned_count = 0
            
            for temp_file in self.temp_dir.glob("*"):
                if temp_file.is_file():
                    file_age = datetime.fromtimestamp(temp_file.stat().st_mtime)
                    if file_age < cutoff_time:
                        self.cleanup_temp_file(temp_file)
                        cleaned_count += 1
            
            logger.info(f"Cleaned up {cleaned_count} old temporary files")
            return cleaned_count
            
        except Exception as e:
            logger.error(f"Error cleaning up old temp files: {e}")
            return 0
    
    def get_disk_usage_stats(self) -> Dict[str, Any]:
        """Get disk usage statistics"""
        try:
            statvfs = os.statvfs(self.upload_dir)
            total_space = statvfs.f_frsize * statvfs.f_blocks
            free_space = statvfs.f_frsize * statvfs.f_bavail
            used_space = total_space - free_space
            
            return {
                "total_space_mb": total_space / (1024 * 1024),
                "used_space_mb": used_space / (1024 * 1024),
                "free_space_mb": free_space / (1024 * 1024),
                "usage_percentage": (used_space / total_space) * 100,
                "upload_dir": str(self.upload_dir),
                "temp_dir": str(self.temp_dir)
            }
        except Exception as e:
            logger.error(f"Error getting disk usage stats: {e}")
            return {"error": str(e)}
    
    def validate_file_integrity(self, file_path: Path) -> bool:
        """Validate file integrity after upload"""
        try:
            if not file_path.exists():
                return False
            
            # Check file size is reasonable
            file_size = file_path.stat().st_size
            if file_size == 0 or file_size > MAX_FILE_SIZE:
                return False
            
            # Check file permissions
            file_mode = file_path.stat().st_mode
            if file_mode & 0o777 != 0o644:  # Should be 644
                logger.warning(f"File has incorrect permissions: {oct(file_mode)}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"File integrity check error: {e}")
            return False

# Global instance
file_security_manager = FileSecurityManager(
    upload_dir=os.getenv('UPLOAD_DIR', './uploads'),
    temp_dir=os.getenv('TEMP_UPLOAD_DIR', './temp_uploads')
)
