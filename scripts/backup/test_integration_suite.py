#!/usr/bin/env python3
"""
Phase 5.1.1: Integration Testing Suite
Tests the full pipeline from data ingestion to response generation
"""

import os
import sys
import time
import json
import requests
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Tuple
from sqlalchemy import text

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.enhanced_rag_service import EnhancedRAGService

class IntegrationTestSuite:
    def __init__(self):
        self.api_base_url = "http://localhost:8001"
        self.test_results = []
        self.start_time = time.time()
        
        # Initialize RAG service for direct testing
        self.rag_service = EnhancedRAGService(
            db_url=os.getenv("DATABASE_URL", "postgresql://admin:password123@localhost:5432/real_estate_db"),
            chroma_host=os.getenv("CHROMA_HOST", "localhost"),
            chroma_port=os.getenv("CHROMA_PORT", 8000)
        )
        
    def log_test(self, test_name: str, status: str, details: str = "", duration: float = 0):
        """Log test results"""
        result = {
            "test_name": test_name,
            "status": status,
            "details": details,
            "duration": duration,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        print(f"{'✅' if status == 'PASS' else '❌'} {test_name}: {status} ({duration:.3f}s)")
        if details:
            print(f"   Details: {details}")
    
    def test_api_health(self) -> bool:
        """Test API health endpoint"""
        start_time = time.time()
        try:
            response = requests.get(f"{self.api_base_url}/health", timeout=10)
            duration = time.time() - start_time
            
            if response.status_code == 200:
                self.log_test("API Health Check", "PASS", "API is healthy", duration)
                return True
            else:
                self.log_test("API Health Check", "FAIL", f"Status code: {response.status_code}", duration)
                return False
        except Exception as e:
            duration = time.time() - start_time
            self.log_test("API Health Check", "FAIL", f"Connection error: {str(e)}", duration)
            return False
    
    def test_chat_endpoint(self) -> bool:
        """Test basic chat endpoint functionality"""
        start_time = time.time()
        try:
            payload = {
                "message": "Hello, can you help me with Dubai real estate?",
                "role": "client",
                "session_id": "test_session_001"
            }
            
            response = requests.post(f"{self.api_base_url}/chat", json=payload, timeout=30)
            duration = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if "response" in data:
                    self.log_test("Chat Endpoint", "PASS", f"Response received: {len(data['response'])} chars", duration)
                    return True
                else:
                    self.log_test("Chat Endpoint", "FAIL", "No response in data", duration)
                    return False
            else:
                self.log_test("Chat Endpoint", "FAIL", f"Status code: {response.status_code}", duration)
                return False
        except Exception as e:
            duration = time.time() - start_time
            self.log_test("Chat Endpoint", "FAIL", f"Request error: {str(e)}", duration)
            return False
    
    def test_all_intent_types(self) -> Dict[str, bool]:
        """Test all 12 intent types with sample queries"""
        intent_tests = {
            "PROPERTY_SEARCH": "I'm looking for a 2-bedroom apartment in Dubai Marina under 2 million AED",
            "MARKET_INFO": "What are the current market trends in Dubai real estate?",
            "POLICY_QUESTION": "What are the requirements for buying property in Dubai as a foreigner?",
            "AGENT_SUPPORT": "How can I improve my real estate sales techniques?",
            "GENERAL": "Tell me about Dubai's real estate market",
            "INVESTMENT_QUESTION": "What's the ROI for investing in Dubai Marina properties?",
            "REGULATORY_QUESTION": "What are the latest RERA regulations for property transactions?",
            "NEIGHBORHOOD_QUESTION": "Tell me about the amenities and lifestyle in Downtown Dubai",
            "DEVELOPER_QUESTION": "What are Emaar's latest projects and track record?",
            "TRANSACTION_GUIDANCE": "What's the process for buying an off-plan property in Dubai?",
            "FINANCIAL_INSIGHTS": "What financing options are available for Dubai real estate?",
            "URBAN_PLANNING": "What are the key features of Dubai 2040 master plan?"
        }
        
        results = {}
        print("\n🧪 Testing All Intent Types:")
        print("=" * 50)
        
        for intent, query in intent_tests.items():
            start_time = time.time()
            try:
                # Test direct RAG service
                analysis = self.rag_service.analyze_query(query)
                duration = time.time() - start_time
                
                if analysis.intent.name == intent:
                    self.log_test(f"Intent: {intent}", "PASS", f"Correctly classified as {intent}", duration)
                    results[intent] = True
                else:
                    self.log_test(f"Intent: {intent}", "FAIL", f"Expected {intent}, got {analysis.intent.name}", duration)
                    results[intent] = False
                    
            except Exception as e:
                duration = time.time() - start_time
                self.log_test(f"Intent: {intent}", "FAIL", f"Error: {str(e)}", duration)
                results[intent] = False
        
        return results
    
    def test_data_ingestion_pipeline(self) -> bool:
        """Test data ingestion pipeline with sample data"""
        print("\n📥 Testing Data Ingestion Pipeline:")
        print("=" * 50)
        
        # Test CSV processor
        start_time = time.time()
        try:
            from scripts.processors.csv_processor import CSVProcessor
            from scripts.storage.postgres_storage import PostgresStorage
            
            csv_processor = CSVProcessor()
            postgres_storage = PostgresStorage(db_url=os.getenv("DATABASE_URL", "postgresql://admin:password123@localhost:5432/real_estate_db"))
            
            # Create sample CSV data
            sample_csv_data = """property_id,address,price,bedrooms,bathrooms,neighborhood,developer
1,Dubai Marina Tower 1,2500000,2,2,Dubai Marina,Emaar
2,Downtown Dubai Apartment,3500000,3,3,Downtown Dubai,Emaar
3,Palm Jumeirah Villa,8500000,4,5,Palm Jumeirah,Nakheel"""
            
            # Test processing
            processed_data = csv_processor.process(sample_csv_data)
            duration = time.time() - start_time
            
            if processed_data and len(processed_data) > 0:
                self.log_test("CSV Processor", "PASS", f"Processed {len(processed_data)} records", duration)
                return True
            else:
                self.log_test("CSV Processor", "FAIL", "No data processed", duration)
                return False
                
        except Exception as e:
            duration = time.time() - start_time
            self.log_test("CSV Processor", "FAIL", f"Error: {str(e)}", duration)
            return False
    
    def test_multi_source_retrieval(self) -> bool:
        """Test hybrid data retrieval (ChromaDB + PostgreSQL)"""
        print("\n🔄 Testing Multi-Source Data Retrieval:")
        print("=" * 50)
        
        test_queries = [
            "What are the best investment opportunities in Dubai Marina with high ROI?",
            "Compare Emaar and DAMAC developers for luxury properties",
            "What are the Golden Visa requirements and benefits for real estate investors?"
        ]
        
        all_passed = True
        
        for i, query in enumerate(test_queries, 1):
            start_time = time.time()
            try:
                # Test context retrieval
                analysis = self.rag_service.analyze_query(query)
                context = self.rag_service.get_relevant_context(query, analysis)
                duration = time.time() - start_time
                
                if context and len(context) > 0:
                    # Check if we got both ChromaDB and PostgreSQL data
                    chroma_items = [item for item in context if item.data_type == "document"]
                    postgres_items = [item for item in context if item.data_type == "structured"]
                    
                    if chroma_items and postgres_items:
                        self.log_test(f"Multi-Source Query {i}", "PASS", 
                                    f"Got {len(chroma_items)} docs + {len(postgres_items)} structured items", duration)
                    else:
                        self.log_test(f"Multi-Source Query {i}", "PARTIAL", 
                                    f"Got {len(chroma_items)} docs + {len(postgres_items)} structured items", duration)
                else:
                    self.log_test(f"Multi-Source Query {i}", "FAIL", "No context retrieved", duration)
                    all_passed = False
                    
            except Exception as e:
                duration = time.time() - start_time
                self.log_test(f"Multi-Source Query {i}", "FAIL", f"Error: {str(e)}", duration)
                all_passed = False
        
        return all_passed
    
    def test_end_to_end_workflow(self) -> bool:
        """Test complete end-to-end workflow"""
        print("\n🔄 Testing End-to-End Workflow:")
        print("=" * 50)
        
        test_scenarios = [
            {
                "name": "Property Search Workflow",
                "query": "I need a 3-bedroom apartment in Downtown Dubai under 4 million AED",
                "role": "client"
            },
            {
                "name": "Investment Analysis Workflow", 
                "query": "What's the best area for rental investment with high ROI in Dubai?",
                "role": "agent"
            },
            {
                "name": "Regulatory Guidance Workflow",
                "query": "What are the latest RERA regulations for off-plan property sales?",
                "role": "employee"
            }
        ]
        
        all_passed = True
        
        for scenario in test_scenarios:
            start_time = time.time()
            try:
                # Test complete workflow
                payload = {
                    "message": scenario["query"],
                    "role": scenario["role"],
                    "session_id": f"e2e_test_{int(time.time())}"
                }
                
                response = requests.post(f"{self.api_base_url}/chat", json=payload, timeout=30)
                duration = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    if "response" in data and len(data["response"]) > 50:
                        self.log_test(scenario["name"], "PASS", 
                                    f"Complete response generated ({len(data['response'])} chars)", duration)
                    else:
                        self.log_test(scenario["name"], "FAIL", "Incomplete response", duration)
                        all_passed = False
                else:
                    self.log_test(scenario["name"], "FAIL", f"HTTP {response.status_code}", duration)
                    all_passed = False
                    
            except Exception as e:
                duration = time.time() - start_time
                self.log_test(scenario["name"], "FAIL", f"Error: {str(e)}", duration)
                all_passed = False
        
        return all_passed
    
    def test_data_consistency(self) -> bool:
        """Test data consistency across systems"""
        print("\n🔍 Testing Data Consistency:")
        print("=" * 50)
        
        # Test that Dubai-specific data is available in both systems
        start_time = time.time()
        try:
            # Test ChromaDB collections
            chroma_collections = [
                "market_analysis", "regulatory_framework", "neighborhood_profiles",
                "investment_insights", "developer_profiles", "transaction_guidance",
                "market_forecasts", "agent_resources", "urban_planning", "financial_insights"
            ]
            
            missing_collections = []
            for collection_name in chroma_collections:
                try:
                    collection = self.rag_service.chroma_client.get_collection(collection_name)
                    count = collection.count()
                    if count == 0:
                        missing_collections.append(f"{collection_name} (empty)")
                except:
                    missing_collections.append(f"{collection_name} (missing)")
            
            # Test PostgreSQL tables
            postgres_tables = [
                "market_data", "neighborhood_profiles", "developers", 
                "investment_insights", "regulatory_updates"
            ]
            
            missing_tables = []
            for table_name in postgres_tables:
                try:
                    with self.rag_service.engine.connect() as conn:
                        result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                        count = result.fetchone()[0]
                        if count == 0:
                            missing_tables.append(f"{table_name} (empty)")
                except Exception as e:
                    missing_tables.append(f"{table_name} (missing: {str(e)})")
            
            duration = time.time() - start_time
            
            if not missing_collections and not missing_tables:
                self.log_test("Data Consistency", "PASS", "All data sources populated", duration)
                return True
            else:
                issues = []
                if missing_collections:
                    issues.append(f"ChromaDB: {', '.join(missing_collections)}")
                if missing_tables:
                    issues.append(f"PostgreSQL: {', '.join(missing_tables)}")
                
                self.log_test("Data Consistency", "FAIL", f"Issues: {'; '.join(issues)}", duration)
                return False
                
        except Exception as e:
            duration = time.time() - start_time
            self.log_test("Data Consistency", "FAIL", f"Error: {str(e)}", duration)
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all integration tests"""
        print("🧪 Phase 5.1.1: Integration Testing Suite")
        print("=" * 60)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Run all tests
        tests = [
            ("API Health", self.test_api_health),
            ("Chat Endpoint", self.test_chat_endpoint),
            ("Intent Types", self.test_all_intent_types),
            ("Data Ingestion", self.test_data_ingestion_pipeline),
            ("Multi-Source Retrieval", self.test_multi_source_retrieval),
            ("End-to-End Workflow", self.test_end_to_end_workflow),
            ("Data Consistency", self.test_data_consistency)
        ]
        
        results = {}
        
        for test_name, test_func in tests:
            try:
                if test_name == "Intent Types":
                    results[test_name] = test_func()
                else:
                    results[test_name] = test_func()
            except Exception as e:
                print(f"❌ {test_name}: ERROR - {str(e)}")
                results[test_name] = False
        
        # Calculate summary
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        failed_tests = len([r for r in self.test_results if r["status"] == "FAIL"])
        partial_tests = len([r for r in self.test_results if r["status"] == "PARTIAL"])
        
        total_duration = time.time() - self.start_time
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 INTEGRATION TESTING SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"⚠️  Partial: {partial_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests + partial_tests * 0.5) / total_tests * 100:.1f}%")
        print(f"Total Duration: {total_duration:.2f}s")
        
        # Save detailed results
        summary = {
            "test_suite": "Phase 5.1.1 Integration Testing",
            "timestamp": datetime.now().isoformat(),
            "total_tests": total_tests,
            "passed": passed_tests,
            "partial": partial_tests,
            "failed": failed_tests,
            "success_rate": (passed_tests + partial_tests * 0.5) / total_tests * 100,
            "total_duration": total_duration,
            "detailed_results": self.test_results
        }
        
        # Save to file
        with open("test_results_integration.json", "w") as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n📄 Detailed results saved to: test_results_integration.json")
        
        return summary

def main():
    """Main function to run integration tests"""
    test_suite = IntegrationTestSuite()
    results = test_suite.run_all_tests()
    
    # Exit with appropriate code
    if results["failed"] == 0:
        print("\n🎉 All integration tests passed!")
        sys.exit(0)
    else:
        print(f"\n⚠️  {results['failed']} tests failed. Please review the results.")
        sys.exit(1)

if __name__ == "__main__":
    main()
