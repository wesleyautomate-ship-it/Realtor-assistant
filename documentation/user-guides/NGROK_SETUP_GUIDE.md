# 📱 Mobile Access Setup with ngrok

## 🎯 **Overview**
This guide will help you access your RAG web app on your phone using ngrok, which creates secure tunnels to your local development environment.

## 🚀 **Step 1: Start Your Application**

### Option A: Using Docker (Recommended)
```bash
# Start all services
docker-compose up -d --build

# Verify services are running
docker-compose ps
```

### Option B: Using Local Development
```bash
# Terminal 1: Start Backend
cd backend
uvicorn main:app --host 0.0.0.0 --port 8001 --reload

# Terminal 2: Start Frontend
cd frontend
npm start
```

## 🔧 **Step 2: Configure ngrok**

### 2.1 Download and Setup ngrok
```bash
# If you don't have ngrok installed
# Download from: https://ngrok.com/download

# Extract ngrok.exe to your project root (if not already there)
# You already have ngrok.exe in your project root
```

### 2.2 Sign up for ngrok (Free Account)
1. Go to https://ngrok.com/signup
2. Create a free account
3. Get your authtoken from the dashboard
4. Authenticate ngrok:
```bash
./ngrok authtoken YOUR_AUTH_TOKEN_HERE
```

## 🌐 **Step 3: Create ngrok Tunnels**

### 3.1 For Frontend (Port 3000)
```bash
# Open a new terminal window
./ngrok http 3000
```

### 3.2 For Backend (Port 8003)
```bash
# Open another terminal window
./ngrok http 8003
```

## 📱 **Step 4: Access on Your Phone**

### 4.1 Frontend Access
1. Look for the ngrok URL in the frontend terminal (e.g., `https://abc123.ngrok.io`)
2. Open this URL on your phone's browser
3. The app should load and be fully functional

### 4.2 Backend API Access
1. Note the backend ngrok URL (e.g., `https://xyz789.ngrok.io`)
2. Update your frontend configuration to use this URL

## ⚙️ **Step 5: Update Frontend Configuration**

### 5.1 Update API URL
You need to update the frontend to use the ngrok backend URL:

```bash
# Edit frontend environment
cd frontend
```

Create or update `.env` file:
```env
REACT_APP_API_URL=https://YOUR_BACKEND_NGROK_URL
```

### 5.2 Alternative: Update Docker Environment
If using Docker, update the docker-compose.yml:

```yaml
frontend:
  build: ./frontend
  ports:
    - "3000:3000"
  environment:
    - REACT_APP_API_URL=https://YOUR_BACKEND_NGROK_URL
  # ... rest of config
```

## 🔄 **Step 6: Restart Services (if needed)**

```bash
# If you updated environment variables
docker-compose down
docker-compose up -d --build
```

## 🛠️ **Step 7: Troubleshooting**

### Common Issues:

1. **CORS Errors**
   - Backend needs to allow ngrok domains
   - Update CORS settings in backend

2. **Mixed Content Errors**
   - Ensure both frontend and backend use HTTPS
   - Use ngrok's HTTPS URLs

3. **Connection Issues**
   - Check if ngrok tunnels are active
   - Verify ports are correct
   - Ensure no firewall blocking

### Debug Commands:
```bash
# Check if services are running
docker-compose ps

# Check ngrok status
./ngrok status

# Test backend directly
curl https://YOUR_BACKEND_NGROK_URL/health

# Check frontend
curl https://YOUR_FRONTEND_NGROK_URL
```

## 📋 **Quick Setup Script**

Create a batch file `start_mobile.bat`:
```batch
@echo off
echo Starting RAG Web App for Mobile Access...

REM Start Docker services
docker-compose up -d --build

REM Wait for services to start
timeout /t 10

REM Start ngrok tunnels
start "Frontend Tunnel" ngrok http 3000
timeout /t 3
start "Backend Tunnel" ngrok http 8003

echo.
echo Services started! Check ngrok URLs in the new windows.
echo.
echo Frontend: Look for ngrok URL in "Frontend Tunnel" window
echo Backend: Look for ngrok URL in "Backend Tunnel" window
echo.
pause
```

## 🔒 **Security Notes**

1. **ngrok URLs are public** - anyone with the URL can access your app
2. **Use ngrok authentication** to restrict access
3. **Consider using ngrok's paid plans** for better security
4. **Don't use this for production** - only for development/testing

## 🎯 **Final Checklist**

- [ ] Docker services running (`docker-compose ps`)
- [ ] Frontend accessible at `http://localhost:3000`
- [ ] Backend accessible at `http://localhost:8003`
- [ ] ngrok tunnels created for both services
- [ ] Frontend environment updated with backend ngrok URL
- [ ] App loads on phone browser
- [ ] All features working on mobile

## 📞 **Support**

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all services are running
3. Check ngrok tunnel status
4. Review browser console for errors
5. Test with different browsers on your phone

**🎉 You're all set! Your RAG web app should now be accessible on your phone!**
