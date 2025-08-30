#!/usr/bin/env python3
"""
Script to update CORS settings for ngrok access
This script adds ngrok domains to the allowed origins
"""

import re
import os
from pathlib import Path

def update_cors_settings():
    """Update CORS settings to allow ngrok domains"""
    
    settings_file = Path("backend/config/settings.py")
    
    if not settings_file.exists():
        print("❌ Settings file not found!")
        return False
    
    # Read current settings
    with open(settings_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if ngrok domains are already allowed
    if "ngrok.io" in content:
        print("✅ ngrok domains already allowed in CORS settings")
        return True
    
    # Find the ALLOWED_ORIGINS list
    pattern = r'ALLOWED_ORIGINS\s*=\s*\[(.*?)\]'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        print("❌ Could not find ALLOWED_ORIGINS in settings file")
        return False
    
    # Add ngrok domains to the list
    current_origins = match.group(1)
    
    # Add ngrok domains
    ngrok_origins = [
        '    "https://*.ngrok.io",',
        '    "https://*.ngrok-free.app",',
        '    "http://*.ngrok.io",',
        '    "http://*.ngrok-free.app",'
    ]
    
    # Insert ngrok origins before the closing bracket
    new_origins = current_origins.rstrip() + '\n' + '\n'.join(ngrok_origins) + '\n'
    
    # Replace in content
    new_content = re.sub(pattern, f'ALLOWED_ORIGINS = [{new_origins}]', content, flags=re.DOTALL)
    
    # Write back to file
    with open(settings_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ Updated CORS settings to allow ngrok domains")
    print("📝 Added the following origins:")
    for origin in ngrok_origins:
        print(f"   {origin.strip()}")
    
    return True

def create_ngrok_config():
    """Create ngrok configuration file"""
    
    config_content = """# ngrok configuration for RAG Web App
version: "2"
authtoken: YOUR_AUTH_TOKEN_HERE

tunnels:
  frontend:
    addr: 3000
    proto: http
    inspect: true
    
  backend:
    addr: 8003
    proto: http
    inspect: true
"""
    
    config_file = Path("ngrok.yml")
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print("✅ Created ngrok.yml configuration file")
    print("📝 Remember to:")
    print("   1. Replace YOUR_AUTH_TOKEN_HERE with your actual ngrok token")
    print("   2. Run: ngrok start --config ngrok.yml frontend backend")

if __name__ == "__main__":
    print("🔧 Updating CORS settings for ngrok access...")
    
    success = update_cors_settings()
    
    if success:
        print("\n📋 Next steps:")
        print("1. Restart your backend service")
        print("2. Run the start_mobile.bat script")
        print("3. Or manually start ngrok tunnels")
        
        # Offer to create ngrok config
        response = input("\nWould you like to create an ngrok configuration file? (y/n): ")
        if response.lower() in ['y', 'yes']:
            create_ngrok_config()
    else:
        print("\n❌ Failed to update CORS settings")
        print("Please manually add ngrok domains to backend/config/settings.py")
