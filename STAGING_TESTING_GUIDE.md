# 🚀 Staging & Testing Guide

## 📋 **Testing Checklist**

### **Phase 1: Environment Setup**

#### **✅ 1. Start Docker Services**
```bash
# Start all services
docker-compose up -d

# Or start individually
docker-compose up postgres -d
docker-compose up redis -d
docker-compose up chromadb -d

# Verify services are running
docker ps
```

#### **✅ 2. Verify Database Connection**
```bash
# Test database connection
docker exec real-estate-rag-chat-system-postgres-1 psql -U admin -d real_estate_db -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';"

# Expected output: 32 tables
```

#### **✅ 3. Check Database Tables**
```bash
# List all tables
docker exec real-estate-rag-chat-system-postgres-1 psql -U admin -d real_estate_db -c "\dt"

# Expected tables:
# - users, properties, conversations (base)
# - brokerages, team_performance, knowledge_base (Phase 1)
# - ai_requests, human_experts, content_deliverables (Phase 2)
# - predictive_performance_models, dubai_market_data (Phase 3)
```

### **Phase 2: Backend Testing**

#### **✅ 4. Start Backend Server**
```bash
cd backend
python main.py
```

**Expected Output:**
```
✅ Database connection successful
✅ All routers loaded successfully
✅ AI Assistant router loaded successfully
✅ Phase 3 Advanced router loaded successfully
🚀 Server running on http://0.0.0.0:8003
```

#### **✅ 5. Test API Endpoints**

**Health Check:**
```bash
curl http://localhost:8003/health
```

**Phase 3 Advanced Endpoints:**
```bash
# System Health
curl http://localhost:8003/api/phase3/developer/health

# Market Data
curl "http://localhost:8003/api/phase3/dubai/market-data?area_name=Dubai%20Marina&property_type=apartment"

# Performance Analytics
curl http://localhost:8003/api/phase3/developer/performance-analytics
```

**AI Assistant Endpoints:**
```bash
# AI Requests
curl http://localhost:8003/api/ai-assistant/requests

# Human Experts
curl http://localhost:8003/api/ai-assistant/experts
```

**Brokerage Management:**
```bash
# Brokerages
curl http://localhost:8003/api/team/brokerages

# Team Performance
curl http://localhost:8003/api/team/performance
```

### **Phase 3: Frontend Testing**

#### **✅ 6. Start Frontend**
```bash
cd frontend
npm install
npm start
```

**Expected Output:**
```
✅ Compiled successfully!
✅ Local: http://localhost:3000
✅ Network: http://192.168.x.x:3000
```

#### **✅ 7. Test Frontend Interfaces**

**Navigation Test:**
1. Open http://localhost:3000
2. Verify sidebar navigation includes:
   - AI Copilot
   - AI Assistant
   - Developer Dashboard (admin/developer only)
   - Brokerage Dashboard (brokerage_owner only)
   - Properties
   - Team Management

**User Role Testing:**
1. **Admin/Developer**: Should see Developer Dashboard
2. **Brokerage Owner**: Should see Brokerage Dashboard
3. **Agent/Employee**: Should see AI Assistant and Properties

**Interface Testing:**
1. **AI Assistant Page**: Test request submission
2. **Developer Dashboard**: Test system health monitoring
3. **Brokerage Dashboard**: Test team performance metrics
4. **Properties Page**: Test property management

### **Phase 4: Integration Testing**

#### **✅ 8. End-to-End User Flows**

**AI Request Flow:**
1. Navigate to AI Assistant
2. Submit a text request: "Create a CMA for a 3-bedroom apartment in Dubai Marina"
3. Verify request is processed
4. Check if human expert assignment works

**Developer Panel Flow:**
1. Login as admin/developer
2. Navigate to Developer Dashboard
3. Check system health metrics
4. View performance analytics
5. Test system alerts creation

**Brokerage Management Flow:**
1. Login as brokerage owner
2. Navigate to Brokerage Dashboard
3. View team performance
4. Check knowledge base management
5. Test brand management

#### **✅ 9. Database Integration Test**
```bash
# Test data insertion
docker exec real-estate-rag-chat-system-postgres-1 psql -U admin -d real_estate_db -c "
INSERT INTO ai_requests (agent_id, brokerage_id, request_type, request_content, status) 
VALUES (1, 1, 'CMA', 'Test request', 'pending');
"

# Verify data
docker exec real-estate-rag-chat-system-postgres-1 psql -U admin -d real_estate_db -c "
SELECT * FROM ai_requests;
"
```

### **Phase 5: Performance Testing**

#### **✅ 10. Load Testing**
```bash
# Test multiple concurrent requests
for i in {1..10}; do
  curl http://localhost:8003/api/phase3/developer/health &
done
wait
```

#### **✅ 11. Database Performance**
```bash
# Test query performance
docker exec real-estate-rag-chat-system-postgres-1 psql -U admin -d real_estate_db -c "
EXPLAIN ANALYZE SELECT * FROM ai_requests WHERE status = 'pending';
"
```

### **Phase 6: Error Handling Testing**

#### **✅ 12. Error Scenarios**
1. **Invalid API requests**: Test with malformed data
2. **Database connection loss**: Stop PostgreSQL and test
3. **Frontend error boundaries**: Test with invalid data
4. **Authentication failures**: Test with invalid credentials

### **Phase 7: Security Testing**

#### **✅ 13. Security Checks**
1. **Role-based access**: Verify users can only access allowed features
2. **API authentication**: Test protected endpoints
3. **Data validation**: Test input sanitization
4. **CORS configuration**: Test cross-origin requests

## 🐛 **Troubleshooting Guide**

### **Common Issues & Solutions**

#### **Database Connection Issues**
```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Check PostgreSQL logs
docker logs real-estate-rag-chat-system-postgres-1

# Restart PostgreSQL
docker-compose restart postgres
```

#### **Backend Startup Issues**
```bash
# Check Python dependencies
cd backend
pip install -r requirements.txt

# Check for port conflicts
netstat -an | grep 8003

# Check backend logs
python main.py
```

#### **Frontend Issues**
```bash
# Clear npm cache
cd frontend
npm cache clean --force

# Reinstall dependencies
rm -rf node_modules
npm install

# Check for port conflicts
netstat -an | grep 3000
```

#### **API Endpoint Issues**
```bash
# Test individual endpoints
curl -v http://localhost:8003/health
curl -v http://localhost:8003/api/phase3/developer/health

# Check backend logs for errors
```

## 📊 **Success Criteria**

### **✅ All Tests Must Pass**
- [ ] All Docker services running
- [ ] Database connection successful
- [ ] All 32 tables present
- [ ] Backend server starts without errors
- [ ] All API endpoints responding
- [ ] Frontend loads successfully
- [ ] All user interfaces functional
- [ ] Role-based access working
- [ ] End-to-end user flows working
- [ ] Performance within acceptable limits

### **✅ Performance Benchmarks**
- [ ] API response time < 2 seconds
- [ ] Frontend load time < 3 seconds
- [ ] Database query time < 1 second
- [ ] System health check < 500ms

## 🎯 **Next Steps After Testing**

1. **Fix any issues** found during testing
2. **Optimize performance** based on test results
3. **Document any limitations** or known issues
4. **Prepare for production deployment**
5. **Set up monitoring and alerting**

---

**Ready to begin testing!** 🚀
