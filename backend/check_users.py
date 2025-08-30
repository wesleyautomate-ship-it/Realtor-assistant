#!/usr/bin/env python3
"""
Check users in the database
"""

import sys
import os
sys.path.append('/app')

from auth.database import get_db_context
from auth.models import User

try:
    with get_db_context() as db:
        users = db.query(User).all()
        print(f"Found {len(users)} users:")
        for user in users:
            print(f"- {user.email} ({user.role}) - Active: {user.is_active}")
        
        if not users:
            print("No users found. You need to register a user first.")
            print("Default admin credentials:")
            print("Email: admin@dubai-estate.com")
            print("Password: Admin123!")
            
except Exception as e:
    print(f"Error: {e}")
