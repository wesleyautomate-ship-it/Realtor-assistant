# Database Setup Guide

## 🎯 **Quick Setup (Recommended)**

### **Step 1: Start PostgreSQL**
```bash
# Start PostgreSQL using Docker
docker-compose up postgres -d

# Or if you have PostgreSQL installed locally, make sure it's running
```

### **Step 2: Create the Database**
```bash
# Run the simple database creation script
python create_database.py
```

### **Step 3: Run All Migrations**
```bash
# Run the complete setup script (recommended)
python backend/scripts/setup_database.py

# OR run migrations individually:
python backend/scripts/run_brokerage_migration.py
python backend/scripts/run_ai_assistant_migration.py
python backend/scripts/run_phase3_migration.py
```

## 🔧 **Manual Setup (Alternative)**

### **Step 1: Connect to PostgreSQL**
```bash
# Using psql command line
psql -h localhost -p 5432 -U admin -d postgres

# Or using Docker
docker exec -it <postgres_container_id> psql -U admin -d postgres
```

### **Step 2: Create Database**
```sql
-- Create the database
CREATE DATABASE real_estate_db;

-- Verify it was created
\l

-- Exit psql
\q
```

### **Step 3: Run Migrations**
```bash
# Run each migration script
python backend/scripts/run_brokerage_migration.py
python backend/scripts/run_ai_assistant_migration.py
python backend/scripts/run_phase3_migration.py
```

## 🐳 **Docker Setup (Full Stack)**

### **Step 1: Start All Services**
```bash
# Start the entire stack
docker-compose up -d

# Check if services are running
docker-compose ps
```

### **Step 2: Verify Database**
```bash
# Check if database was created
docker exec -it <postgres_container_id> psql -U admin -d real_estate_db -c "\dt"
```

### **Step 3: Run Migrations (if needed)**
```bash
# If migrations weren't run automatically
docker exec -it <backend_container_id> python scripts/setup_database.py
```

## 🔍 **Troubleshooting**

### **Database Connection Issues**
```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Check PostgreSQL logs
docker-compose logs postgres

# Test connection
docker exec -it <postgres_container_id> pg_isready -U admin -d real_estate_db
```

### **Migration Issues**
```bash
# Check if database exists
docker exec -it <postgres_container_id> psql -U admin -d postgres -c "\l"

# Check if tables exist
docker exec -it <postgres_container_id> psql -U admin -d real_estate_db -c "\dt"

# Check migration logs
docker-compose logs backend
```

### **Permission Issues**
```bash
# Make sure scripts are executable
chmod +x backend/scripts/*.py
chmod +x create_database.py

# Check file permissions
ls -la backend/scripts/
ls -la create_database.py
```

## 📋 **Verification Checklist**

### **✅ Database Created**
- [ ] Database `real_estate_db` exists
- [ ] User `admin` has access
- [ ] Connection string is correct

### **✅ Phase 1 Tables**
- [ ] `brokerages` table exists
- [ ] `users` table exists with brokerage relationships
- [ ] `team_performance` table exists
- [ ] `knowledge_base` table exists

### **✅ Phase 2 Tables**
- [ ] `ai_requests` table exists
- [ ] `human_experts` table exists
- [ ] `content_deliverables` table exists
- [ ] `voice_requests` table exists
- [ ] `task_automation` table exists

### **✅ Phase 3 Tables**
- [ ] `predictive_performance_models` table exists
- [ ] `benchmarking_data` table exists
- [ ] `dubai_market_data` table exists
- [ ] `rera_integration_data` table exists
- [ ] `system_performance_metrics` table exists
- [ ] `user_activity_analytics` table exists
- [ ] `ai_processing_analytics` table exists
- [ ] `multi_brokerage_analytics` table exists
- [ ] `developer_panel_settings` table exists
- [ ] `system_alerts` table exists

## 🚀 **Next Steps After Setup**

### **1. Start Backend**
```bash
cd backend
python main.py
```

### **2. Start Frontend**
```bash
cd frontend
npm start
```

### **3. Test the System**
- Navigate to `http://localhost:3000`
- Test login functionality
- Check if all features are working
- Verify database connections

## 📞 **Support**

If you encounter issues:

1. **Check the logs**: `docker-compose logs`
2. **Verify database connection**: Test with `psql`
3. **Check file permissions**: Ensure scripts are executable
4. **Review configuration**: Verify `DATABASE_URL` in settings

## 🎉 **Success Indicators**

You'll know the setup is successful when:

- ✅ Database `real_estate_db` exists
- ✅ All migration scripts run without errors
- ✅ Backend starts without database connection errors
- ✅ Frontend can connect to backend APIs
- ✅ You can log in and access all features

---

**Ready to proceed with Phase 3 testing!** 🚀
