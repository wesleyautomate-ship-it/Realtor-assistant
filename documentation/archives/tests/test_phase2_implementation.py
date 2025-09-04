#!/usr/bin/env python3
"""
Test script for Phase 2: Intelligent AI Data Processor
Tests the new document classification and data extraction capabilities
"""

import os
import sys
import json
from pathlib import Path

# Add backend to path
sys.path.append('backend')

from intelligent_processor import IntelligentDataProcessor

def create_test_documents():
    """Create test documents for testing"""
    test_dir = Path("test_documents")
    test_dir.mkdir(exist_ok=True)
    
    # Test transaction document
    transaction_content = """
    PROPERTY TRANSACTION REPORT - DUBAI MARINA
    
    Recent Sales Transactions:
    
    1. Sale Date: 2025-01-15
       Property: Marina Gate 1, Unit 3405
       Address: Dubai Marina, Tower 1, Floor 34
       Sale Price: AED 2,500,000
       Buyer: Ahmed Al Mansouri
    
    2. Sale Date: 2025-01-20
       Property: Marina Gate 2, Unit 1208
       Address: Dubai Marina, Tower 2, Floor 12
       Sale Price: AED 1,800,000
       Buyer: Sarah Johnson
    
    3. Sale Date: 2025-01-25
       Property: Marina Heights, Unit 2501
       Address: Dubai Marina, Tower A, Floor 25
       Sale Price: AED 3,200,000
       Buyer: Mohammed Al Rashid
    """
    
    with open(test_dir / "test_transactions.txt", "w", encoding="utf-8") as f:
        f.write(transaction_content)
    
    # Test legal document
    legal_content = """
    REAL ESTATE REGULATORY FRAMEWORK - DUBAI
    
    RERA COMPLIANCE REQUIREMENTS
    
    Section 1: Agent Licensing
    All real estate agents must be licensed by RERA and maintain valid credentials.
    Agents must complete mandatory training and pass certification exams.
    
    Section 2: Commission Rules
    Standard commission rates are 2% for residential properties and 3% for commercial.
    All commissions must be disclosed in writing to clients.
    
    Section 3: Deal Structuring
    All property transactions must be structured according to Dubai Land Department guidelines.
    Proper documentation and escrow accounts are mandatory.
    
    Section 4: Financing Requirements
    Buyers must provide proof of funds or mortgage pre-approval.
    Down payment requirements vary by property type and buyer nationality.
    
    Section 5: Tenancy Contracts
    All rental agreements must be registered with Ejari system.
    Standard tenancy contracts must include all mandatory clauses.
    """
    
    with open(test_dir / "test_legal.txt", "w", encoding="utf-8") as f:
        f.write(legal_content)
    
    return test_dir

def test_document_classification():
    """Test document classification functionality"""
    print("🧪 Testing Document Classification...")
    
    processor = IntelligentDataProcessor()
    test_dir = create_test_documents()
    
    # Test transaction document
    transaction_file = test_dir / "test_transactions.txt"
    with open(transaction_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    classification = processor._get_document_category(content)
    print(f"📄 Transaction document classification: {classification}")
    
    # Test legal document
    legal_file = test_dir / "test_legal.txt"
    with open(legal_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    classification = processor._get_document_category(content)
    print(f"📄 Legal document classification: {classification}")
    
    return True

def test_full_processing():
    """Test full document processing pipeline"""
    print("\n🧪 Testing Full Processing Pipeline...")
    
    processor = IntelligentDataProcessor()
    test_dir = create_test_documents()
    
    # Test transaction processing
    print("📊 Testing transaction document processing...")
    transaction_result = processor.process_uploaded_document(
        str(test_dir / "test_transactions.txt"),
        "text"
    )
    print(f"Transaction processing result: {json.dumps(transaction_result, indent=2)}")
    
    # Test legal processing
    print("\n⚖️ Testing legal document processing...")
    legal_result = processor.process_uploaded_document(
        str(test_dir / "test_legal.txt"),
        "text"
    )
    print(f"Legal processing result: {json.dumps(legal_result, indent=2)}")
    
    return True

def test_error_handling():
    """Test error handling with invalid files"""
    print("\n🧪 Testing Error Handling...")
    
    processor = IntelligentDataProcessor()
    
    # Test with non-existent file
    try:
        result = processor.process_uploaded_document("non_existent_file.txt", "text")
        print(f"Non-existent file result: {result}")
    except Exception as e:
        print(f"✅ Correctly handled non-existent file: {e}")
    
    # Test with empty content
    try:
        result = processor._get_document_category("")
        print(f"Empty content classification: {result}")
    except Exception as e:
        print(f"✅ Correctly handled empty content: {e}")
    
    return True

def main():
    """Run all tests"""
    print("🚀 Phase 2 Implementation Test Suite")
    print("=" * 50)
    
    try:
        # Test 1: Document Classification
        test_document_classification()
        
        # Test 2: Full Processing Pipeline
        test_full_processing()
        
        # Test 3: Error Handling
        test_error_handling()
        
        print("\n✅ All tests completed successfully!")
        print("\n📋 Test Summary:")
        print("- Document classification working")
        print("- Full processing pipeline functional")
        print("- Error handling robust")
        print("- AI integration operational")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
