#!/usr/bin/env python3
"""
Phase 5.1.2: Performance Testing
Optimize context retrieval to consistently meet <2.0s benchmark
"""

import os
import sys
import time
import json
import statistics
import requests
from datetime import datetime
from typing import Dict, List, Any

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.enhanced_rag_service import EnhancedRAGService

class PerformanceTestSuite:
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
        
        # Performance targets
        self.targets = {
            "context_retrieval": 2.0,  # seconds
            "total_response": 3.0,     # seconds
            "database_query": 0.5,     # seconds
            "chromadb_query": 1.0      # seconds
        }
    
    def log_performance(self, test_name: str, duration: float, target: float, details: str = ""):
        """Log performance test results"""
        status = "PASS" if duration <= target else "FAIL"
        result = {
            "test_name": test_name,
            "duration": duration,
            "target": target,
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        emoji = "✅" if status == "PASS" else "❌"
        print(f"{emoji} {test_name}: {duration:.3f}s (target: {target:.1f}s) - {status}")
        if details:
            print(f"   Details: {details}")
    
    def test_context_retrieval_performance(self) -> List[float]:
        """Test context retrieval performance with various queries"""
        print("\n⚡ Testing Context Retrieval Performance:")
        print("=" * 50)
        
        test_queries = [
            "What are the best investment opportunities in Dubai Marina?",
            "Tell me about Emaar's latest projects and track record",
            "What are the Golden Visa requirements for real estate investors?",
            "Compare rental yields in Downtown Dubai vs Dubai Marina",
            "What are the latest RERA regulations for property transactions?"
        ]
        
        durations = []
        
        for i, query in enumerate(test_queries, 1):
            start_time = time.time()
            try:
                # Test context retrieval
                analysis = self.rag_service.analyze_query(query)
                context = self.rag_service.get_relevant_context(query, analysis)
                duration = time.time() - start_time
                durations.append(duration)
                
                context_count = len(context) if context else 0
                self.log_performance(
                    f"Context Retrieval {i}", 
                    duration, 
                    self.targets["context_retrieval"],
                    f"Retrieved {context_count} context items"
                )
                
            except Exception as e:
                duration = time.time() - start_time
                self.log_performance(
                    f"Context Retrieval {i}", 
                    duration, 
                    self.targets["context_retrieval"],
                    f"Error: {str(e)}"
                )
        
        return durations
    
    def test_api_response_performance(self) -> List[float]:
        """Test complete API response performance"""
        print("\n🌐 Testing API Response Performance:")
        print("=" * 50)
        
        test_payloads = [
            {
                "message": "What are the best investment opportunities in Dubai Marina?",
                "role": "client",
                "session_id": "perf_test_001"
            },
            {
                "message": "Tell me about Emaar's latest projects and track record",
                "role": "agent", 
                "session_id": "perf_test_002"
            },
            {
                "message": "What are the Golden Visa requirements for real estate investors?",
                "role": "client",
                "session_id": "perf_test_003"
            }
        ]
        
        durations = []
        
        for i, payload in enumerate(test_payloads, 1):
            start_time = time.time()
            try:
                response = requests.post(f"{self.api_base_url}/chat", json=payload, timeout=30)
                duration = time.time() - start_time
                durations.append(duration)
                
                if response.status_code == 200:
                    data = response.json()
                    response_length = len(data.get("response", ""))
                    self.log_performance(
                        f"API Response {i}", 
                        duration, 
                        self.targets["total_response"],
                        f"Response: {response_length} chars"
                    )
                else:
                    self.log_performance(
                        f"API Response {i}", 
                        duration, 
                        self.targets["total_response"],
                        f"HTTP {response.status_code}"
                    )
                
            except Exception as e:
                duration = time.time() - start_time
                self.log_performance(
                    f"API Response {i}", 
                    duration, 
                    self.targets["total_response"],
                    f"Error: {str(e)}"
                )
        
        return durations
    
    def analyze_performance(self, durations: List[float], test_name: str) -> Dict[str, float]:
        """Analyze performance metrics"""
        if not durations:
            return {}
        
        return {
            "count": len(durations),
            "mean": statistics.mean(durations),
            "median": statistics.median(durations),
            "min": min(durations),
            "max": max(durations),
            "std_dev": statistics.stdev(durations) if len(durations) > 1 else 0
        }
    
    def generate_optimization_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Generate optimization recommendations based on test results"""
        recommendations = []
        
        # Context retrieval optimization
        context_avg = results.get("context_retrieval", {}).get("mean", 0)
        if context_avg > self.targets["context_retrieval"]:
            recommendations.append(
                f"Context retrieval average ({context_avg:.3f}s) exceeds target ({self.targets['context_retrieval']}s). "
                "Consider: limiting ChromaDB collection queries, implementing caching, optimizing embeddings."
            )
        
        # API response optimization
        api_avg = results.get("api_response", {}).get("mean", 0)
        if api_avg > self.targets["total_response"]:
            recommendations.append(
                f"API response average ({api_avg:.3f}s) exceeds target ({self.targets['total_response']}s). "
                "Consider: optimizing context retrieval, implementing response caching, parallel processing."
            )
        
        return recommendations
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all performance tests"""
        print("⚡ Phase 5.1.2: Performance Testing Suite")
        print("=" * 60)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Target Context Retrieval: <{self.targets['context_retrieval']}s")
        print(f"Target Total Response: <{self.targets['total_response']}s")
        print()
        
        # Run performance tests
        context_durations = self.test_context_retrieval_performance()
        api_durations = self.test_api_response_performance()
        
        # Analyze results
        results = {
            "context_retrieval": self.analyze_performance(context_durations, "Context Retrieval"),
            "api_response": self.analyze_performance(api_durations, "API Response")
        }
        
        # Calculate summary
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        failed_tests = len([r for r in self.test_results if r["status"] == "FAIL"])
        
        total_duration = time.time() - self.start_time
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 PERFORMANCE TESTING SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {passed_tests / total_tests * 100:.1f}%")
        print(f"Total Duration: {total_duration:.2f}s")
        
        # Print detailed results
        print("\n📈 PERFORMANCE METRICS:")
        print("-" * 40)
        for test_type, metrics in results.items():
            if metrics and "mean" in metrics:
                print(f"{test_type.replace('_', ' ').title()}:")
                print(f"  Mean: {metrics['mean']:.3f}s")
                print(f"  Median: {metrics['median']:.3f}s")
                print(f"  Min: {metrics['min']:.3f}s")
                print(f"  Max: {metrics['max']:.3f}s")
                print()
        
        # Generate recommendations
        recommendations = self.generate_optimization_recommendations(results)
        if recommendations:
            print("🔧 OPTIMIZATION RECOMMENDATIONS:")
            print("-" * 40)
            for i, rec in enumerate(recommendations, 1):
                print(f"{i}. {rec}")
            print()
        
        # Save detailed results
        summary = {
            "test_suite": "Phase 5.1.2 Performance Testing",
            "timestamp": datetime.now().isoformat(),
            "targets": self.targets,
            "total_tests": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "success_rate": passed_tests / total_tests * 100,
            "total_duration": total_duration,
            "performance_results": results,
            "recommendations": recommendations,
            "detailed_results": self.test_results
        }
        
        # Save to file
        with open("test_results_performance.json", "w") as f:
            json.dump(summary, f, indent=2)
        
        print(f"📄 Detailed results saved to: test_results_performance.json")
        
        return summary

def main():
    """Main function to run performance tests"""
    test_suite = PerformanceTestSuite()
    results = test_suite.run_all_tests()
    
    # Exit with appropriate code
    if results["failed"] == 0:
        print("\n🎉 All performance targets met!")
        sys.exit(0)
    else:
        print(f"\n⚠️  {results['failed']} performance targets not met. Review recommendations.")
        sys.exit(1)

if __name__ == "__main__":
    main()
