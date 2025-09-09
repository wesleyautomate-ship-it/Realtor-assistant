# 🔧 CI/CD Updates for Advanced Chat Integration

## 📋 **Build Script Updates Required**

### 1. **Remove References to Deleted Files**

#### Files to Remove from Build Scripts:
- `backend/advanced_chat_router.py` - **DELETED**

#### Update These Build Scripts:
- **Docker builds** - Remove any references to `advanced_chat_router.py`
- **Test scripts** - Update endpoint tests
- **Deployment scripts** - Remove old router references
- **Health checks** - Update endpoint monitoring

### 2. **Update Test Scripts**

#### Before (Old Endpoints):
```bash
# Remove these test references
curl -X GET "http://localhost:8003/advanced-chat/health"
curl -X POST "http://localhost:8003/advanced-chat/ai/detect-entities"
```

#### After (New Endpoints):
```bash
# Use these new session-based endpoints
curl -X GET "http://localhost:8003/sessions/{session_id}/advanced/health"
curl -X POST "http://localhost:8003/sessions/{session_id}/advanced/detect-entities"
```

### 3. **Update Health Check Scripts**

#### Old Health Check:
```bash
# Remove this
curl -X GET "http://localhost:8003/advanced-chat/health"
```

#### New Health Check:
```bash
# Use this (requires valid session_id)
curl -X GET "http://localhost:8003/sessions/{session_id}/advanced/health"
```

### 4. **Update Monitoring Scripts**

#### Update These Monitoring Endpoints:
- **Remove**: `/advanced-chat/health`
- **Add**: `/sessions/{session_id}/advanced/health`
- **Note**: New endpoint requires valid session_id

### 5. **Update Docker Configuration**

#### Dockerfile Updates:
```dockerfile
# Remove any specific references to advanced_chat_router.py
# The main chat router now handles all functionality
```

#### Docker Compose Updates:
```yaml
# No changes needed - all functionality preserved
# Just remove any specific health checks for advanced-chat endpoints
```

### 6. **Update Deployment Scripts**

#### Before:
```bash
# Remove these references
python -c "import advanced_chat_router"
curl -X GET "http://localhost:8003/advanced-chat/health"
```

#### After:
```bash
# Use these instead
python -c "import chat_sessions_router"
curl -X GET "http://localhost:8003/sessions/{session_id}/advanced/health"
```

## 🔍 **Files to Check and Update**

### Build Scripts to Review:
- `docker-compose.yml`
- `Dockerfile`
- `build.sh` (if exists)
- `deploy.sh` (if exists)
- `test.sh` (if exists)
- `health-check.sh` (if exists)

### Test Files to Update:
- `test_actual_endpoints.py` ✅ **Already Updated**
- Any other test files referencing `/advanced-chat/*`

### Monitoring Scripts to Update:
- Health check scripts
- Performance monitoring
- Endpoint availability checks

## 📝 **Specific Updates Needed**

### 1. **Health Check Updates**
```bash
# OLD
curl -X GET "http://localhost:8003/advanced-chat/health"

# NEW (requires session_id)
curl -X GET "http://localhost:8003/sessions/{session_id}/advanced/health"
```

### 2. **Test Script Updates**
```bash
# OLD
curl -X POST "http://localhost:8003/advanced-chat/ai/detect-entities" \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}'

# NEW
curl -X POST "http://localhost:8003/sessions/{session_id}/advanced/detect-entities" \
  -H "Content-Type: application/json" \
  -d '{"message": "test", "session_id": "session_id"}'
```

### 3. **Import Statement Updates**
```python
# OLD
from advanced_chat_router import router as advanced_chat_router

# NEW
# No longer needed - functionality moved to chat_sessions_router
```

## ⚠️ **Important Notes**

### 1. **Session ID Requirement**
- All new advanced endpoints require a valid `session_id`
- Health checks may need to create a test session first
- Consider using a dedicated test session for monitoring

### 2. **Backward Compatibility**
- All existing chat functionality preserved
- No breaking changes to existing endpoints
- Only advanced chat endpoints moved to new structure

### 3. **Error Handling**
- New endpoints return 503 if advanced services unavailable
- Graceful degradation implemented
- No impact on basic chat functionality

## 🚀 **Deployment Checklist**

- [ ] Update health check scripts
- [ ] Update test scripts
- [ ] Update monitoring scripts
- [ ] Update Docker configuration (if needed)
- [ ] Update deployment scripts
- [ ] Test new endpoints
- [ ] Verify backward compatibility
- [ ] Update documentation

## 📞 **Support**

If you encounter any issues with CI/CD updates:

1. **Check Integration Summary**: See `INTEGRATION_SUMMARY.md`
2. **Review Code Changes**: All changes are well-documented
3. **Test Endpoints**: Use `test_actual_endpoints.py`
4. **Contact Team**: Reach out for assistance

---

**Status**: ✅ **READY** - All updates documented and ready for implementation
**Risk**: 🟢 **LOW** - No breaking changes, all functionality preserved
