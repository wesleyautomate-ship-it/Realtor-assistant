#!/usr/bin/env python3
"""
Run Migrations from Docker Container
===================================

This script runs the database migrations from inside the Docker container.
"""

import subprocess
import sys
import os

def run_migration_from_docker():
    """Run migrations from inside the Docker container"""
    try:
        print("=" * 60)
        print("RUNNING MIGRATIONS FROM DOCKER CONTAINER")
        print("=" * 60)
        
        # List of migration files in order
        migration_files = [
            "base_schema_migration.sql",
            "brokerage_schema_migration.sql",
            "ai_assistant_schema_migration.sql",
            "phase3_advanced_schema_migration.sql"
        ]
        
        container_name = "real-estate-rag-chat-system-postgres-1"
        
        for migration_file in migration_files:
            migration_path = f"backend/migrations/{migration_file}"
            
            if not os.path.exists(migration_path):
                print(f"⚠️ Migration file not found: {migration_file}")
                continue
            
            print(f"Running migration: {migration_file}")
            
            # Copy file to container
            copy_cmd = f"docker cp {migration_path} {container_name}:/tmp/{migration_file}"
            result = subprocess.run(copy_cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ Failed to copy {migration_file}: {result.stderr}")
                continue
            
            # Run migration
            run_cmd = f"docker exec {container_name} psql -U admin -d real_estate_db -f /tmp/{migration_file}"
            result = subprocess.run(run_cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Migration {migration_file} completed successfully")
            else:
                print(f"❌ Migration {migration_file} failed: {result.stderr}")
                # Continue with other migrations even if one fails
        
        # Verify tables were created
        print("\nVerifying tables...")
        verify_cmd = f"docker exec {container_name} psql -U admin -d real_estate_db -c \"SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';\""
        result = subprocess.run(verify_cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            table_count = result.stdout.strip().split('\n')[-2]  # Get the count from output
            print(f"✅ Found {table_count} tables in the database")
        else:
            print(f"❌ Failed to verify tables: {result.stderr}")
        
        print("\n🎉 Migration process completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error running migrations: {e}")
        return False

if __name__ == "__main__":
    success = run_migration_from_docker()
    sys.exit(0 if success else 1)
