"""
Performance and load tests for Dubai Real Estate RAG Chat System
"""
import pytest
import time
import threading
import asyncio
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any
import requests
from fastapi.testclient import TestClient
import json

# Import the modules to test
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))
from main import app
from auth.models import User
from auth.utils import hash_password
from tests.utils.test_helpers import PerformanceHelper, TestDataGenerator

class TestLoadPerformance:
    """Test system performance under load."""
    
    def test_single_user_response_time(self, client, db_session):
        """Test response time for single user requests."""
        # Create test user
        user = User(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            password_hash=hash_password("TestPassword123!"),
            is_active=True
        )
        db_session.add(user)
        db_session.commit()
        
        # Login to get token
        login_response = client.post("/auth/login", json={
            "email": "test@example.com",
            "password": "TestPassword123!"
        })
        token = login_response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test response times for different endpoints
        endpoints = [
            "/auth/me",
            "/properties/search",
            "/chat/send",
            "/properties/list"
        ]
        
        results = {}
        for endpoint in endpoints:
            response_times = []
            for _ in range(10):  # 10 requests per endpoint
                start_time = time.time()
                response = client.get(endpoint, headers=headers)
                end_time = time.time()
                
                assert response.status_code == 200
                response_times.append(end_time - start_time)
            
            results[endpoint] = {
                "avg_response_time": statistics.mean(response_times),
                "min_response_time": min(response_times),
                "max_response_time": max(response_times),
                "p95_response_time": statistics.quantiles(response_times, n=20)[18]  # 95th percentile
            }
        
        # Assert performance requirements
        for endpoint, metrics in results.items():
            assert metrics["avg_response_time"] < 2.0, f"Average response time for {endpoint} exceeds 2 seconds"
            assert metrics["p95_response_time"] < 5.0, f"95th percentile response time for {endpoint} exceeds 5 seconds"
            
    def test_concurrent_users_10(self, client, db_session):
        """Test system with 10 concurrent users."""
        self._test_concurrent_users(client, db_session, num_users=10)
        
    def test_concurrent_users_20(self, client, db_session):
        """Test system with 20 concurrent users."""
        self._test_concurrent_users(client, db_session, num_users=20)
        
    def test_concurrent_users_50(self, client, db_session):
        """Test system with 50 concurrent users."""
        self._test_concurrent_users(client, db_session, num_users=50)
        
    def test_concurrent_users_100(self, client, db_session):
        """Test system with 100 concurrent users."""
        self._test_concurrent_users(client, db_session, num_users=100)
        
    def _test_concurrent_users(self, client, db_session, num_users: int):
        """Helper method to test concurrent users."""
        # Create test users
        users = []
        for i in range(num_users):
            user = User(
                first_name=f"Test{i}",
                last_name="User",
                email=f"test{i}@example.com",
                password_hash=hash_password("TestPassword123!"),
                is_active=True
            )
            db_session.add(user)
        db_session.commit()
        
        # Login all users and get tokens
        tokens = []
        for i in range(num_users):
            login_response = client.post("/auth/login", json={
                "email": f"test{i}@example.com",
                "password": "TestPassword123!"
            })
            token = login_response.json().get("access_token")
            tokens.append(token)
        
        # Define workload for each user
        def user_workload(user_id: int, token: str):
            headers = {"Authorization": f"Bearer {token}"}
            results = []
            
            # Simulate user activity
            for _ in range(5):  # 5 requests per user
                start_time = time.time()
                
                # Randomly choose an endpoint
                import random
                endpoints = [
                    "/auth/me",
                    "/properties/search",
                    "/chat/send",
                    "/properties/list"
                ]
                endpoint = random.choice(endpoints)
                
                if endpoint == "/chat/send":
                    response = client.post(endpoint, json={
                        "message": "Test message",
                        "context": "property_search"
                    }, headers=headers)
                else:
                    response = client.get(endpoint, headers=headers)
                
                end_time = time.time()
                
                results.append({
                    "user_id": user_id,
                    "endpoint": endpoint,
                    "status_code": response.status_code,
                    "response_time": end_time - start_time,
                    "success": response.status_code < 400
                })
                
                # Small delay between requests
                time.sleep(0.1)
            
            return results
        
        # Execute concurrent requests
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=num_users) as executor:
            futures = [
                executor.submit(user_workload, i, tokens[i])
                for i in range(num_users)
            ]
            
            all_results = []
            for future in as_completed(futures):
                all_results.extend(future.result())
        
        end_time = time.time()
        total_duration = end_time - start_time
        
        # Calculate metrics
        successful_requests = sum(1 for r in all_results if r["success"])
        total_requests = len(all_results)
        success_rate = (successful_requests / total_requests) * 100
        
        response_times = [r["response_time"] for r in all_results]
        avg_response_time = statistics.mean(response_times)
        p95_response_time = statistics.quantiles(response_times, n=20)[18] if len(response_times) >= 20 else max(response_times)
        
        # Assert performance requirements
        assert success_rate >= 95.0, f"Success rate {success_rate}% is below 95% for {num_users} concurrent users"
        assert avg_response_time < 3.0, f"Average response time {avg_response_time}s exceeds 3 seconds for {num_users} concurrent users"
        assert p95_response_time < 8.0, f"95th percentile response time {p95_response_time}s exceeds 8 seconds for {num_users} concurrent users"
        
        # Log results
        print(f"\nConcurrent Users Test Results ({num_users} users):")
        print(f"Total Requests: {total_requests}")
        print(f"Successful Requests: {successful_requests}")
        print(f"Success Rate: {success_rate:.2f}%")
        print(f"Average Response Time: {avg_response_time:.3f}s")
        print(f"95th Percentile Response Time: {p95_response_time:.3f}s")
        print(f"Total Duration: {total_duration:.3f}s")
        print(f"Requests per Second: {total_requests / total_duration:.2f}")

class TestStressPerformance:
    """Test system performance under stress conditions."""
    
    def test_rapid_requests(self, client, db_session):
        """Test system with rapid successive requests."""
        # Create test user
        user = User(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            password_hash=hash_password("TestPassword123!"),
            is_active=True
        )
        db_session.add(user)
        db_session.commit()
        
        # Login to get token
        login_response = client.post("/auth/login", json={
            "email": "test@example.com",
            "password": "TestPassword123!"
        })
        token = login_response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        
        # Make rapid requests
        start_time = time.time()
        successful_requests = 0
        total_requests = 100
        
        for i in range(total_requests):
            response = client.get("/auth/me", headers=headers)
            if response.status_code == 200:
                successful_requests += 1
        
        end_time = time.time()
        duration = end_time - start_time
        
        success_rate = (successful_requests / total_requests) * 100
        requests_per_second = total_requests / duration
        
        assert success_rate >= 95.0, f"Success rate {success_rate}% is below 95% for rapid requests"
        assert requests_per_second >= 50, f"Request rate {requests_per_second} req/s is below 50 req/s"
        
    def test_large_payload_handling(self, client, db_session):
        """Test system with large payloads."""
        # Create test user
        user = User(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            password_hash=hash_password("TestPassword123!"),
            is_active=True
        )
        db_session.add(user)
        db_session.commit()
        
        # Login to get token
        login_response = client.post("/auth/login", json={
            "email": "test@example.com",
            "password": "TestPassword123!"
        })
        token = login_response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test with large chat message
        large_message = "A" * 10000  # 10KB message
        chat_data = {
            "message": large_message,
            "context": "property_search",
            "user_preferences": {
                "location": "Dubai Marina",
                "max_price": 3000000,
                "property_type": "apartment"
            }
        }
        
        start_time = time.time()
        response = client.post("/chat/send", json=chat_data, headers=headers)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200, f"Large payload request failed with status {response.status_code}"
        assert response_time < 10.0, f"Large payload response time {response_time}s exceeds 10 seconds"
        
    def test_memory_usage_under_load(self, client, db_session):
        """Test memory usage under load."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Create multiple users and perform operations
        users = []
        for i in range(50):
            user = User(
                first_name=f"Test{i}",
                last_name="User",
                email=f"test{i}@example.com",
                password_hash=hash_password("TestPassword123!"),
                is_active=True
            )
            db_session.add(user)
        db_session.commit()
        
        # Perform operations
        for i in range(50):
            login_response = client.post("/auth/login", json={
                "email": f"test{i}@example.com",
                "password": "TestPassword123!"
            })
            token = login_response.json().get("access_token")
            headers = {"Authorization": f"Bearer {token}"}
            
            # Make several requests
            for _ in range(5):
                client.get("/auth/me", headers=headers)
                client.get("/properties/search", headers=headers)
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (less than 100MB)
        assert memory_increase < 100, f"Memory increase {memory_increase}MB exceeds 100MB"

class TestDatabasePerformance:
    """Test database performance under load."""
    
    def test_database_connection_pool(self, client, db_session):
        """Test database connection pool performance."""
        # Create multiple users
        users = []
        for i in range(100):
            user = User(
                first_name=f"Test{i}",
                last_name="User",
                email=f"test{i}@example.com",
                password_hash=hash_password("TestPassword123!"),
                is_active=True
            )
            db_session.add(user)
        db_session.commit()
        
        # Test concurrent database operations
        def db_operation(user_id: int):
            # Simulate database operations
            user = db_session.query(User).filter_by(email=f"test{user_id}@example.com").first()
            return user is not None
        
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(db_operation, i) for i in range(100)]
            results = [future.result() for future in as_completed(futures)]
        
        end_time = time.time()
        duration = end_time - start_time
        
        successful_operations = sum(results)
        success_rate = (successful_operations / len(results)) * 100
        
        assert success_rate == 100.0, f"Database operation success rate {success_rate}% is not 100%"
        assert duration < 5.0, f"Database operations took {duration}s, exceeding 5 seconds"
        
    def test_database_query_performance(self, client, db_session):
        """Test database query performance."""
        # Create test data
        users = []
        for i in range(1000):
            user = User(
                first_name=f"Test{i}",
                last_name="User",
                email=f"test{i}@example.com",
                password_hash=hash_password("TestPassword123!"),
                is_active=True
            )
            db_session.add(user)
        db_session.commit()
        
        # Test query performance
        start_time = time.time()
        
        # Complex query
        active_users = db_session.query(User).filter_by(is_active=True).all()
        
        end_time = time.time()
        query_time = end_time - start_time
        
        assert len(active_users) == 1000, f"Expected 1000 users, got {len(active_users)}"
        assert query_time < 1.0, f"Database query took {query_time}s, exceeding 1 second"

class TestCachePerformance:
    """Test cache performance under load."""
    
    def test_cache_hit_performance(self, client, db_session):
        """Test cache hit performance."""
        # Create test user
        user = User(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            password_hash=hash_password("TestPassword123!"),
            is_active=True
        )
        db_session.add(user)
        db_session.commit()
        
        # Login to get token
        login_response = client.post("/auth/login", json={
            "email": "test@example.com",
            "password": "TestPassword123!"
        })
        token = login_response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        
        # First request (cache miss)
        start_time = time.time()
        response1 = client.get("/auth/me", headers=headers)
        first_request_time = time.time() - start_time
        
        # Second request (cache hit)
        start_time = time.time()
        response2 = client.get("/auth/me", headers=headers)
        second_request_time = time.time() - start_time
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert second_request_time < first_request_time, "Cache hit should be faster than cache miss"
        
    def test_cache_concurrent_access(self, client, db_session):
        """Test cache performance under concurrent access."""
        # Create test users
        users = []
        for i in range(20):
            user = User(
                first_name=f"Test{i}",
                last_name="User",
                email=f"test{i}@example.com",
                password_hash=hash_password("TestPassword123!"),
                is_active=True
            )
            db_session.add(user)
        db_session.commit()
        
        # Login all users
        tokens = []
        for i in range(20):
            login_response = client.post("/auth/login", json={
                "email": f"test{i}@example.com",
                "password": "TestPassword123!"
            })
            token = login_response.json().get("access_token")
            tokens.append(token)
        
        # Concurrent cache access
        def cache_access(user_id: int, token: str):
            headers = {"Authorization": f"Bearer {token}"}
            response_times = []
            
            for _ in range(10):
                start_time = time.time()
                response = client.get("/auth/me", headers=headers)
                end_time = time.time()
                
                assert response.status_code == 200
                response_times.append(end_time - start_time)
            
            return response_times
        
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [
                executor.submit(cache_access, i, tokens[i])
                for i in range(20)
            ]
            
            all_response_times = []
            for future in as_completed(futures):
                all_response_times.extend(future.result())
        
        end_time = time.time()
        total_duration = end_time - start_time
        
        avg_response_time = statistics.mean(all_response_times)
        p95_response_time = statistics.quantiles(all_response_times, n=20)[18] if len(all_response_times) >= 20 else max(all_response_times)
        
        assert avg_response_time < 0.5, f"Average cache response time {avg_response_time}s exceeds 0.5 seconds"
        assert p95_response_time < 1.0, f"95th percentile cache response time {p95_response_time}s exceeds 1 second"

class TestAIResponsePerformance:
    """Test AI response performance under load."""
    
    def test_ai_response_time(self, client, db_session, mock_google_ai):
        """Test AI response time."""
        # Create test user
        user = User(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            password_hash=hash_password("TestPassword123!"),
            is_active=True
        )
        db_session.add(user)
        db_session.commit()
        
        # Login to get token
        login_response = client.post("/auth/login", json={
            "email": "test@example.com",
            "password": "TestPassword123!"
        })
        token = login_response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test AI response time
        chat_data = {
            "message": "I'm looking for properties in Dubai Marina under 3 million AED",
            "context": "property_search"
        }
        
        response_times = []
        for _ in range(10):
            start_time = time.time()
            response = client.post("/chat/send", json=chat_data, headers=headers)
            end_time = time.time()
            
            assert response.status_code == 200
            response_times.append(end_time - start_time)
        
        avg_response_time = statistics.mean(response_times)
        p95_response_time = statistics.quantiles(response_times, n=10)[9] if len(response_times) >= 10 else max(response_times)
        
        assert avg_response_time < 5.0, f"Average AI response time {avg_response_time}s exceeds 5 seconds"
        assert p95_response_time < 10.0, f"95th percentile AI response time {p95_response_time}s exceeds 10 seconds"
        
    def test_concurrent_ai_requests(self, client, db_session, mock_google_ai):
        """Test concurrent AI requests."""
        # Create test users
        users = []
        for i in range(10):
            user = User(
                first_name=f"Test{i}",
                last_name="User",
                email=f"test{i}@example.com",
                password_hash=hash_password("TestPassword123!"),
                is_active=True
            )
            db_session.add(user)
        db_session.commit()
        
        # Login all users
        tokens = []
        for i in range(10):
            login_response = client.post("/auth/login", json={
                "email": f"test{i}@example.com",
                "password": "TestPassword123!"
            })
            token = login_response.json().get("access_token")
            tokens.append(token)
        
        # Concurrent AI requests
        def ai_request(user_id: int, token: str):
            headers = {"Authorization": f"Bearer {token}"}
            chat_data = {
                "message": f"User {user_id} looking for properties",
                "context": "property_search"
            }
            
            start_time = time.time()
            response = client.post("/chat/send", json=chat_data, headers=headers)
            end_time = time.time()
            
            return {
                "user_id": user_id,
                "status_code": response.status_code,
                "response_time": end_time - start_time,
                "success": response.status_code == 200
            }
        
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(ai_request, i, tokens[i])
                for i in range(10)
            ]
            
            results = [future.result() for future in as_completed(futures)]
        
        end_time = time.time()
        total_duration = end_time - start_time
        
        successful_requests = sum(1 for r in results if r["success"])
        success_rate = (successful_requests / len(results)) * 100
        
        response_times = [r["response_time"] for r in results]
        avg_response_time = statistics.mean(response_times)
        max_response_time = max(response_times)
        
        assert success_rate == 100.0, f"AI request success rate {success_rate}% is not 100%"
        assert avg_response_time < 8.0, f"Average AI response time {avg_response_time}s exceeds 8 seconds"
        assert max_response_time < 15.0, f"Maximum AI response time {max_response_time}s exceeds 15 seconds"

class TestEndToEndPerformance:
    """Test end-to-end performance scenarios."""
    
    def test_full_user_journey_performance(self, client, db_session):
        """Test performance of full user journey."""
        # Register user
        user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "TestPassword123!",
            "role": "client"
        }
        
        start_time = time.time()
        
        # Step 1: Register
        register_response = client.post("/auth/register", json=user_data)
        assert register_response.status_code == 201
        
        # Step 2: Login
        login_response = client.post("/auth/login", json={
            "email": user_data["email"],
            "password": user_data["password"]
        })
        assert login_response.status_code == 200
        token = login_response.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        
        # Step 3: Get user profile
        profile_response = client.get("/auth/me", headers=headers)
        assert profile_response.status_code == 200
        
        # Step 4: Search properties
        search_response = client.get("/properties/search", headers=headers)
        assert search_response.status_code == 200
        
        # Step 5: Send chat message
        chat_response = client.post("/chat/send", json={
            "message": "I'm looking for properties in Dubai Marina",
            "context": "property_search"
        }, headers=headers)
        assert chat_response.status_code == 200
        
        # Step 6: Logout
        logout_response = client.post("/auth/logout", headers=headers)
        assert logout_response.status_code == 200
        
        end_time = time.time()
        total_duration = end_time - start_time
        
        assert total_duration < 10.0, f"Full user journey took {total_duration}s, exceeding 10 seconds"
        
    def test_concurrent_user_journeys(self, client, db_session):
        """Test concurrent full user journeys."""
        def user_journey(user_id: int):
            # Register user
            user_data = {
                "first_name": f"User{user_id}",
                "last_name": "Doe",
                "email": f"user{user_id}@example.com",
                "password": "TestPassword123!",
                "role": "client"
            }
            
            start_time = time.time()
            
            # Register
            register_response = client.post("/auth/register", json=user_data)
            if register_response.status_code != 201:
                return {"user_id": user_id, "success": False, "error": "Registration failed"}
            
            # Login
            login_response = client.post("/auth/login", json={
                "email": user_data["email"],
                "password": user_data["password"]
            })
            if login_response.status_code != 200:
                return {"user_id": user_id, "success": False, "error": "Login failed"}
            
            token = login_response.json().get("access_token")
            headers = {"Authorization": f"Bearer {token}"}
            
            # Get profile
            profile_response = client.get("/auth/me", headers=headers)
            if profile_response.status_code != 200:
                return {"user_id": user_id, "success": False, "error": "Profile fetch failed"}
            
            # Search properties
            search_response = client.get("/properties/search", headers=headers)
            if search_response.status_code != 200:
                return {"user_id": user_id, "success": False, "error": "Property search failed"}
            
            # Send chat message
            chat_response = client.post("/chat/send", json={
                "message": f"User {user_id} looking for properties",
                "context": "property_search"
            }, headers=headers)
            if chat_response.status_code != 200:
                return {"user_id": user_id, "success": False, "error": "Chat failed"}
            
            # Logout
            logout_response = client.post("/auth/logout", headers=headers)
            if logout_response.status_code != 200:
                return {"user_id": user_id, "success": False, "error": "Logout failed"}
            
            end_time = time.time()
            duration = end_time - start_time
            
            return {
                "user_id": user_id,
                "success": True,
                "duration": duration
            }
        
        # Execute concurrent user journeys
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(user_journey, i) for i in range(20)]
            results = [future.result() for future in as_completed(futures)]
        
        end_time = time.time()
        total_duration = end_time - start_time
        
        successful_journeys = sum(1 for r in results if r["success"])
        success_rate = (successful_journeys / len(results)) * 100
        
        journey_durations = [r["duration"] for r in results if r["success"]]
        avg_journey_duration = statistics.mean(journey_durations) if journey_durations else 0
        max_journey_duration = max(journey_durations) if journey_durations else 0
        
        assert success_rate >= 90.0, f"User journey success rate {success_rate}% is below 90%"
        assert avg_journey_duration < 15.0, f"Average user journey duration {avg_journey_duration}s exceeds 15 seconds"
        assert max_journey_duration < 30.0, f"Maximum user journey duration {max_journey_duration}s exceeds 30 seconds"
        
        print(f"\nConcurrent User Journeys Test Results:")
        print(f"Total Journeys: {len(results)}")
        print(f"Successful Journeys: {successful_journeys}")
        print(f"Success Rate: {success_rate:.2f}%")
        print(f"Average Journey Duration: {avg_journey_duration:.3f}s")
        print(f"Maximum Journey Duration: {max_journey_duration:.3f}s")
        print(f"Total Test Duration: {total_duration:.3f}s")
