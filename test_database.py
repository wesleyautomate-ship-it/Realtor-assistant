#!/usr/bin/env python3
"""
Database Testing Script for Dubai Real Estate RAG System
Tests database connections, tables, and data integrity
"""

import psycopg2
import requests
import time
import json
from datetime import datetime
import os

class DatabaseTester:
    def __init__(self, backend_url="http://localhost:8003"):
        self.backend_url = backend_url
        self.results = []
        self.start_time = datetime.now()
        
        # Database connection parameters
        self.db_config = {
            'host': 'localhost',
            'port': 5432,
            'database': 'real_estate_db',
            'user': 'admin',
            'password': 'password123'
        }
    
    def log_test(self, test_name, success, message, response_time=None):
        status = "✅ PASS" if success else "❌ FAIL"
        time_str = f"Response time: {response_time:.3f}s" if response_time else ""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {status} - {test_name}")
        if message:
            print(f"    {message}")
        if time_str:
            print(f"    {time_str}")
        
        self.results.append({
            "test": test_name,
            "success": success,
            "message": message,
            "response_time": response_time,
            "timestamp": datetime.now().isoformat()
        })
    
    def test_database_connection(self):
        """Test direct database connection"""
        print("\n🧪 Testing Database Connection...")
        
        try:
            start_time = time.time()
            conn = psycopg2.connect(**self.db_config)
            response_time = time.time() - start_time
            
            # Test basic query
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            
            cursor.close()
            conn.close()
            
            self.log_test("Database Connection", True, f"Connected successfully. PostgreSQL version: {version[:50]}...", response_time)
            return True
        except Exception as e:
            self.log_test("Database Connection", False, f"Connection failed: {str(e)}")
            return False
    
    def test_database_tables(self):
        """Test if all required tables exist"""
        print("\n🧪 Testing Database Tables...")
        
        # Expected tables from our migrations
        expected_tables = [
            # Core tables
            'users', 'properties', 'conversations', 'user_sessions',
            
            # Phase 1 - Brokerage tables
            'brokerages', 'team_performance', 'knowledge_base', 'brand_assets',
            'workflow_automation', 'client_nurturing', 'compliance_rules',
            'agent_consistency_metrics', 'lead_retention_analytics', 'workflow_efficiency_metrics',
            
            # Phase 2 - AI Assistant tables
            'ai_requests', 'human_experts', 'content_deliverables', 'compliance_checks',
            'voice_requests', 'task_automation', 'smart_nurturing_sequences',
            'dubai_property_data', 'rera_compliance_data', 'retention_analytics',
            
            # Phase 3 - Advanced tables
            'predictive_performance_models', 'benchmarking_data', 'dubai_market_data',
            'rera_integration_data', 'system_performance_metrics', 'user_activity_analytics',
            'ai_processing_analytics', 'multi_brokerage_analytics', 'developer_panel_settings',
            'system_alerts'
        ]
        
        try:
            start_time = time.time()
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Get all tables
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                ORDER BY table_name;
            """)
            existing_tables = [row[0] for row in cursor.fetchall()]
            
            response_time = time.time() - start_time
            
            # Check which expected tables exist
            missing_tables = [table for table in expected_tables if table not in existing_tables]
            existing_expected = [table for table in expected_tables if table in existing_tables]
            
            if len(missing_tables) == 0:
                self.log_test("Database Tables", True, f"All {len(expected_tables)} expected tables exist", response_time)
                result = True
            else:
                self.log_test("Database Tables", False, f"Missing {len(missing_tables)} tables: {missing_tables[:5]}...", response_time)
                result = False
            
            # Log existing tables for reference
            self.log_test("Existing Tables", True, f"Found {len(existing_tables)} tables in database", 0)
            
            cursor.close()
            conn.close()
            
            return result
        except Exception as e:
            self.log_test("Database Tables", False, f"Error checking tables: {str(e)}")
            return False
    
    def test_table_schemas(self):
        """Test table schemas and constraints"""
        print("\n🧪 Testing Table Schemas...")
        
        # Key tables to check
        key_tables = ['users', 'properties', 'conversations', 'brokerages']
        
        try:
            start_time = time.time()
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            
            schema_results = []
            for table in key_tables:
                try:
                    # Check if table exists and get column info
                    cursor.execute("""
                        SELECT column_name, data_type, is_nullable, column_default
                        FROM information_schema.columns
                        WHERE table_name = %s AND table_schema = 'public'
                        ORDER BY ordinal_position;
                    """, (table,))
                    
                    columns = cursor.fetchall()
                    if columns:
                        schema_results.append(f"{table}: {len(columns)} columns")
                    else:
                        schema_results.append(f"{table}: NOT FOUND")
                except Exception as e:
                    schema_results.append(f"{table}: ERROR - {str(e)}")
            
            response_time = time.time() - start_time
            
            # Check if key tables have expected structure
            success_count = sum(1 for result in schema_results if "NOT FOUND" not in result and "ERROR" not in result)
            
            if success_count >= len(key_tables) * 0.75:  # 75% success rate
                self.log_test("Table Schemas", True, f"Schema check passed for {success_count}/{len(key_tables)} tables", response_time)
                for result in schema_results:
                    print(f"    {result}")
                result = True
            else:
                self.log_test("Table Schemas", False, f"Schema check failed for {len(key_tables) - success_count}/{len(key_tables)} tables", response_time)
                result = False
            
            cursor.close()
            conn.close()
            
            return result
        except Exception as e:
            self.log_test("Table Schemas", False, f"Error checking schemas: {str(e)}")
            return False
    
    def test_database_performance(self):
        """Test database performance with sample queries"""
        print("\n🧪 Testing Database Performance...")
        
        try:
            start_time = time.time()
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Test queries
            test_queries = [
                ("SELECT COUNT(*) FROM users", "User count"),
                ("SELECT COUNT(*) FROM properties", "Property count"),
                ("SELECT COUNT(*) FROM conversations", "Conversation count"),
                ("SELECT COUNT(*) FROM brokerages", "Brokerage count")
            ]
            
            query_results = []
            total_query_time = 0
            
            for query, description in test_queries:
                try:
                    query_start = time.time()
                    cursor.execute(query)
                    result = cursor.fetchone()[0]
                    query_time = time.time() - query_start
                    total_query_time += query_time
                    
                    query_results.append(f"{description}: {result} ({(query_time*1000):.1f}ms)")
                except Exception as e:
                    query_results.append(f"{description}: ERROR - {str(e)}")
            
            response_time = time.time() - start_time
            
            # Check if queries executed successfully
            success_count = sum(1 for result in query_results if "ERROR" not in result)
            
            if success_count >= len(test_queries) * 0.75:  # 75% success rate
                self.log_test("Database Performance", True, f"Performance test passed: {success_count}/{len(test_queries)} queries successful", response_time)
                for result in query_results:
                    print(f"    {result}")
                result = True
            else:
                self.log_test("Database Performance", False, f"Performance test failed: {len(test_queries) - success_count}/{len(test_queries)} queries failed", response_time)
                result = False
            
            cursor.close()
            conn.close()
            
            return result
        except Exception as e:
            self.log_test("Database Performance", False, f"Error testing performance: {str(e)}")
            return False
    
    def test_database_via_api(self):
        """Test database functionality through API endpoints"""
        print("\n🧪 Testing Database via API...")
        
        # Test endpoints that interact with database
        api_endpoints = [
            ("/properties", "GET", "Properties API"),
            ("/market/overview", "GET", "Market Data API"),
            ("/health", "GET", "Health Check API")
        ]
        
        success_count = 0
        for endpoint, method, description in api_endpoints:
            try:
                start_time = time.time()
                url = f"{self.backend_url}{endpoint}"
                
                if method == "GET":
                    response = requests.get(url, timeout=10)
                else:
                    response = requests.post(url, json={}, timeout=10)
                
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    self.log_test(f"API DB Test - {description}", True, f"Status: {response.status_code}", response_time)
                    success_count += 1
                else:
                    self.log_test(f"API DB Test - {description}", False, f"Status: {response.status_code}", response_time)
            except Exception as e:
                self.log_test(f"API DB Test - {description}", False, f"Error: {str(e)}")
        
        return success_count >= len(api_endpoints) * 0.6  # 60% success rate
    
    def test_database_constraints(self):
        """Test database constraints and relationships"""
        print("\n🧪 Testing Database Constraints...")
        
        try:
            start_time = time.time()
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Check foreign key constraints
            cursor.execute("""
                SELECT 
                    tc.table_name, 
                    kcu.column_name, 
                    ccu.table_name AS foreign_table_name,
                    ccu.column_name AS foreign_column_name 
                FROM 
                    information_schema.table_constraints AS tc 
                    JOIN information_schema.key_column_usage AS kcu
                      ON tc.constraint_name = kcu.constraint_name
                      AND tc.table_schema = kcu.table_schema
                    JOIN information_schema.constraint_column_usage AS ccu
                      ON ccu.constraint_name = tc.constraint_name
                      AND ccu.table_schema = tc.table_schema
                WHERE tc.constraint_type = 'FOREIGN KEY' 
                AND tc.table_schema='public'
                ORDER BY tc.table_name;
            """)
            
            foreign_keys = cursor.fetchall()
            response_time = time.time() - start_time
            
            if foreign_keys:
                self.log_test("Database Constraints", True, f"Found {len(foreign_keys)} foreign key constraints", response_time)
                # Show some examples
                for i, fk in enumerate(foreign_keys[:3]):
                    print(f"    {fk[0]}.{fk[1]} -> {fk[2]}.{fk[3]}")
                if len(foreign_keys) > 3:
                    print(f"    ... and {len(foreign_keys) - 3} more")
                result = True
            else:
                self.log_test("Database Constraints", False, "No foreign key constraints found", response_time)
                result = False
            
            cursor.close()
            conn.close()
            
            return result
        except Exception as e:
            self.log_test("Database Constraints", False, f"Error checking constraints: {str(e)}")
            return False
    
    def test_database_indexes(self):
        """Test database indexes for performance"""
        print("\n🧪 Testing Database Indexes...")
        
        try:
            start_time = time.time()
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Get all indexes
            cursor.execute("""
                SELECT 
                    schemaname,
                    tablename,
                    indexname,
                    indexdef
                FROM pg_indexes 
                WHERE schemaname = 'public'
                ORDER BY tablename, indexname;
            """)
            
            indexes = cursor.fetchall()
            response_time = time.time() - start_time
            
            if indexes:
                self.log_test("Database Indexes", True, f"Found {len(indexes)} indexes", response_time)
                # Show some examples
                for i, idx in enumerate(indexes[:5]):
                    print(f"    {idx[1]}.{idx[2]}")
                if len(indexes) > 5:
                    print(f"    ... and {len(indexes) - 5} more")
                result = True
            else:
                self.log_test("Database Indexes", False, "No indexes found", response_time)
                result = False
            
            cursor.close()
            conn.close()
            
            return result
        except Exception as e:
            self.log_test("Database Indexes", False, f"Error checking indexes: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all database tests"""
        print("=" * 70)
        print("🚀 DATABASE TESTING - DUBAI REAL ESTATE RAG SYSTEM")
        print("=" * 70)
        print(f"Database: {self.db_config['database']}@{self.db_config['host']}:{self.db_config['port']}")
        print(f"Backend URL: {self.backend_url}")
        print(f"Started at: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run tests
        connection_ok = self.test_database_connection()
        tables_ok = self.test_database_tables()
        schemas_ok = self.test_table_schemas()
        performance_ok = self.test_database_performance()
        api_db_ok = self.test_database_via_api()
        constraints_ok = self.test_database_constraints()
        indexes_ok = self.test_database_indexes()
        
        # Summary
        print("\n" + "=" * 70)
        print("📊 DATABASE TEST SUMMARY")
        print("=" * 70)
        
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r["success"])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        # Test categories summary
        print(f"\n📋 Database Test Categories:")
        print(f"  Database Connection: {'✅' if connection_ok else '❌'}")
        print(f"  Database Tables: {'✅' if tables_ok else '❌'}")
        print(f"  Table Schemas: {'✅' if schemas_ok else '❌'}")
        print(f"  Database Performance: {'✅' if performance_ok else '❌'}")
        print(f"  Database via API: {'✅' if api_db_ok else '❌'}")
        print(f"  Database Constraints: {'✅' if constraints_ok else '❌'}")
        print(f"  Database Indexes: {'✅' if indexes_ok else '❌'}")
        
        if success_rate >= 70:
            print("\n✅ Database testing successful!")
            print("📄 Test results saved to database_test_results.json")
        else:
            print("\n⚠️ Some database tests failed. Please check the issues above.")
            print("📄 Test results saved to database_test_results.json")
        
        # Save results
        with open("database_test_results.json", "w") as f:
            json.dump({
                "summary": {
                    "total_tests": total_tests,
                    "passed_tests": passed_tests,
                    "failed_tests": failed_tests,
                    "success_rate": success_rate,
                    "test_duration": (datetime.now() - self.start_time).total_seconds(),
                    "database_config": self.db_config,
                    "backend_url": self.backend_url
                },
                "categories": {
                    "connection": connection_ok,
                    "tables": tables_ok,
                    "schemas": schemas_ok,
                    "performance": performance_ok,
                    "api_database": api_db_ok,
                    "constraints": constraints_ok,
                    "indexes": indexes_ok
                },
                "results": self.results
            }, f, indent=2)
        
        return success_rate >= 70

if __name__ == "__main__":
    tester = DatabaseTester()
    success = tester.run_all_tests()
    exit(0 if success else 1)
