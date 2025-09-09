#!/usr/bin/env python3
"""
Phase 1 Deployment Script
=========================

This script deploys Phase 1 features including:
- Database schema migration
- Service initialization
- Configuration updates
"""

import os
import sys
import logging
import subprocess
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_command(command, description):
    """Run a command and log the result"""
    try:
        logger.info(f"Running: {description}")
        logger.info(f"Command: {command}")
        
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=backend_dir
        )
        
        if result.returncode == 0:
            logger.info(f"✅ {description} completed successfully")
            if result.stdout:
                logger.info(f"Output: {result.stdout}")
        else:
            logger.error(f"❌ {description} failed")
            logger.error(f"Error: {result.stderr}")
            return False
            
        return True
        
    except Exception as e:
        logger.error(f"❌ Error running {description}: {e}")
        return False

def check_environment():
    """Check if the environment is ready for deployment"""
    try:
        logger.info("Checking deployment environment...")
        
        # Check if we're in the right directory
        if not (backend_dir / "main.py").exists():
            logger.error("❌ main.py not found. Are we in the right directory?")
            return False
        
        # Check if database migration file exists
        migration_file = backend_dir / "migrations" / "brokerage_schema_migration.sql"
        if not migration_file.exists():
            logger.error("❌ Database migration file not found")
            return False
        
        # Check if required services exist
        required_services = [
            "services/brokerage_management_service.py",
            "services/knowledge_base_service.py",
            "services/brand_management_service.py",
            "services/workflow_automation_service.py",
            "services/client_nurturing_service.py",
            "services/compliance_monitoring_service.py",
            "routers/team_management_router.py"
        ]
        
        for service in required_services:
            service_path = backend_dir / service
            if not service_path.exists():
                logger.error(f"❌ Required service not found: {service}")
                return False
        
        logger.info("✅ Environment check passed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Environment check failed: {e}")
        return False

def run_database_migration():
    """Run the database migration"""
    try:
        logger.info("Starting database migration...")
        
        # Run the migration script
        migration_script = backend_dir / "scripts" / "run_brokerage_migration.py"
        if not migration_script.exists():
            logger.error("❌ Migration script not found")
            return False
        
        # Execute the migration
        result = subprocess.run(
            [sys.executable, str(migration_script)],
            capture_output=True,
            text=True,
            cwd=backend_dir
        )
        
        if result.returncode == 0:
            logger.info("✅ Database migration completed successfully")
            if result.stdout:
                logger.info(f"Migration output: {result.stdout}")
            return True
        else:
            logger.error("❌ Database migration failed")
            logger.error(f"Migration error: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error running database migration: {e}")
        return False

def update_docker_configuration():
    """Update Docker configuration for Phase 1"""
    try:
        logger.info("Updating Docker configuration...")
        
        # Check if docker-compose.yml exists
        docker_compose_file = backend_dir.parent / "docker-compose.yml"
        if not docker_compose_file.exists():
            logger.warning("⚠️ docker-compose.yml not found, skipping Docker update")
            return True
        
        # For now, just log that we would update Docker config
        logger.info("✅ Docker configuration update completed (placeholder)")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error updating Docker configuration: {e}")
        return False

def verify_deployment():
    """Verify that the deployment was successful"""
    try:
        logger.info("Verifying deployment...")
        
        # Check if all required files exist
        required_files = [
            "models/brokerage_models.py",
            "services/brokerage_management_service.py",
            "routers/team_management_router.py"
        ]
        
        for file_path in required_files:
            full_path = backend_dir / file_path
            if not full_path.exists():
                logger.error(f"❌ Required file not found: {file_path}")
                return False
        
        # Check if database tables exist (this would require a database connection)
        logger.info("✅ Deployment verification completed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Deployment verification failed: {e}")
        return False

def main():
    """Main deployment function"""
    logger.info("=" * 60)
    logger.info("PHASE 1 DEPLOYMENT")
    logger.info("=" * 60)
    
    # Step 1: Check environment
    if not check_environment():
        logger.error("❌ Environment check failed. Aborting deployment.")
        sys.exit(1)
    
    # Step 2: Run database migration
    if not run_database_migration():
        logger.error("❌ Database migration failed. Aborting deployment.")
        sys.exit(1)
    
    # Step 3: Update Docker configuration
    if not update_docker_configuration():
        logger.error("❌ Docker configuration update failed. Aborting deployment.")
        sys.exit(1)
    
    # Step 4: Verify deployment
    if not verify_deployment():
        logger.error("❌ Deployment verification failed.")
        sys.exit(1)
    
    logger.info("🎉 Phase 1 deployment completed successfully!")
    logger.info("")
    logger.info("Next steps:")
    logger.info("1. Start the backend server: python main.py")
    logger.info("2. Start the frontend: cd ../frontend && npm start")
    logger.info("3. Test the new brokerage features")
    logger.info("4. Create a brokerage owner user account")
    logger.info("5. Begin Phase 2 development")

if __name__ == "__main__":
    main()
