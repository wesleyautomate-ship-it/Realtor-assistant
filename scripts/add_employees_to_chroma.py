import json
import uuid
from pathlib import Path
import chromadb
from chromadb.config import Settings

def add_employees_to_chroma():
    """Add employee data to ChromaDB collection"""
    
    # Initialize ChromaDB client
    chroma_client = chromadb.HttpClient(
        host="localhost",
        port=8000,
        settings=Settings(allow_reset=True)
    )
    
    # Load employee data
    employees_file = Path("../data/company-data/employees/agent-profiles.json")
    if not employees_file.exists():
        print("❌ Employee profiles file not found")
        return
    
    try:
        with open(employees_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Get or create employees collection
        try:
            collection = chroma_client.get_collection("employees")
            print("📋 Found existing employees collection")
        except:
            collection = chroma_client.create_collection("employees")
            print("📋 Created new employees collection")
        
        # Create content for each employee
        documents = []
        metadatas = []
        ids = []
        
        for employee in data.get("employees", []):
            content = f"""
            {employee.get('name', '')} - {employee.get('role', '')}
            Department: {employee.get('department', '')}
            Specializations: {', '.join(employee.get('specializations', []))}
            Experience: {employee.get('experience', '')}
            Languages: {', '.join(employee.get('languages', []))}
            Achievements: {', '.join(employee.get('achievements', []))}
            Performance: {employee.get('success_rate', '')} success rate, {employee.get('average_deal_size', '')} average deal
            Contact: {employee.get('contact', {}).get('email', '')} | {employee.get('contact', {}).get('phone', '')}
            """
            
            documents.append(content)
            metadatas.append({
                "type": "employee",
                "name": employee.get("name", ""),
                "role": employee.get("role", ""),
                "department": employee.get("department", ""),
                "specializations": ", ".join(employee.get("specializations", [])),
                "source": "agent-profiles.json"
            })
            ids.append(str(uuid.uuid4()))
        
        # Add to collection
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"✅ Added {len(documents)} employees to ChromaDB")
        
        # Test query
        results = collection.query(
            query_texts=["luxury properties"],
            n_results=2
        )
        print(f"🔍 Test query results: {len(results['documents'][0])} documents found")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    add_employees_to_chroma()
