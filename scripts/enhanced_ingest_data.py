import os
import json
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import chromadb
from chromadb.config import Settings
from pathlib import Path
import uuid
from datetime import datetime

# Load environment variables
load_dotenv()

class EnhancedDataIngester:
    def __init__(self):
        # Database connection
        self.database_url = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/real_estate')
        self.engine = create_engine(self.database_url)
        
        # ChromaDB connection
        self.chroma_client = chromadb.HttpClient(
            host=os.getenv('CHROMA_HOST', 'localhost'),
            port=int(os.getenv('CHROMA_PORT', '8000'))
        )
        
        # Data directories
        self.data_root = Path("../data")
        self.dubai_market_dir = self.data_root / "dubai-market"
        self.agent_resources_dir = self.data_root / "agent-resources"
        self.company_data_dir = self.data_root / "company-data"
        
    def create_enhanced_tables(self):
        """Create additional tables for enhanced knowledge base"""
        with self.engine.connect() as conn:
            # Create neighborhoods table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS neighborhoods (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    description TEXT,
                    location_data JSONB,
                    amenities JSONB,
                    price_ranges JSONB,
                    rental_yields JSONB,
                    service_charges JSONB,
                    market_trends JSONB,
                    target_audience TEXT[],
                    pros TEXT[],
                    cons TEXT[],
                    investment_advice TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # Create market_updates table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS market_updates (
                    id SERIAL PRIMARY KEY,
                    period VARCHAR(100) NOT NULL,
                    report_type VARCHAR(100),
                    summary TEXT,
                    key_highlights TEXT[],
                    market_performance JSONB,
                    area_performance JSONB,
                    investment_insights JSONB,
                    legislative_updates JSONB,
                    forecast JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # Create agent_resources table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS agent_resources (
                    id SERIAL PRIMARY KEY,
                    category VARCHAR(100) NOT NULL,
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    content TEXT,
                    key_strategies JSONB,
                    common_scenarios JSONB,
                    templates JSONB,
                    related_topics TEXT[],
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # Create employees table
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS employees (
                    id SERIAL PRIMARY KEY,
                    employee_id VARCHAR(50) UNIQUE NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    role VARCHAR(100),
                    department VARCHAR(100),
                    specializations TEXT[],
                    contact_info JSONB,
                    experience VARCHAR(50),
                    languages TEXT[],
                    achievements TEXT[],
                    availability TEXT,
                    team VARCHAR(100),
                    manager VARCHAR(100),
                    performance_metrics JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # Create Dubai-specific tables (Phase 2 additions)
            self.create_dubai_specific_tables(conn)
            
            conn.commit()
            print("✅ Enhanced tables created successfully")
    
    def create_dubai_specific_tables(self, conn):
        """Create Dubai-specific tables for Phase 2"""
        print("🏗️ Creating Dubai-specific tables...")
        
        # Create market_data table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS market_data (
                id SERIAL PRIMARY KEY,
                date DATE NOT NULL,
                neighborhood VARCHAR(100),
                property_type VARCHAR(50),
                avg_price_per_sqft DECIMAL(10,2),
                transaction_volume INTEGER,
                price_change_percent DECIMAL(5,2),
                rental_yield DECIMAL(5,2),
                market_trend VARCHAR(50),
                off_plan_percentage DECIMAL(5,2),
                foreign_investment_percentage DECIMAL(5,2),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        
        # Create regulatory_updates table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS regulatory_updates (
                id SERIAL PRIMARY KEY,
                law_name VARCHAR(200),
                enactment_date DATE,
                description TEXT,
                impact_areas TEXT[],
                relevant_stakeholders TEXT[],
                status VARCHAR(50),
                key_provisions TEXT[],
                compliance_requirements TEXT[],
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        
        # Create developers table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS developers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                type VARCHAR(50),
                market_share DECIMAL(5,2),
                total_projects INTEGER,
                avg_project_value DECIMAL(15,2),
                reputation_score DECIMAL(3,1),
                specialties TEXT[],
                key_projects TEXT[],
                financial_strength VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        
        # Create investment_insights table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS investment_insights (
                id SERIAL PRIMARY KEY,
                category VARCHAR(100),
                title VARCHAR(200),
                description TEXT,
                key_benefits TEXT[],
                requirements TEXT[],
                investment_amount_min DECIMAL(15,2),
                investment_amount_max DECIMAL(15,2),
                roi_projection DECIMAL(5,2),
                risk_level VARCHAR(50),
                target_audience TEXT[],
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        
        # Create neighborhood_profiles table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS neighborhood_profiles (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                description TEXT,
                location_data JSONB,
                amenities JSONB,
                price_ranges JSONB,
                rental_yields JSONB,
                market_trends JSONB,
                target_audience TEXT[],
                pros TEXT[],
                cons TEXT[],
                investment_advice TEXT,
                transportation_links TEXT[],
                schools_hospitals JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        
        print("✅ Dubai-specific tables created successfully")
    
    def ingest_neighborhoods(self):
        """Ingest neighborhood data from JSON files"""
        neighborhoods_dir = self.dubai_market_dir / "neighborhoods"
        if not neighborhoods_dir.exists():
            print("⚠️ Neighborhoods directory not found")
            return
        
        with self.engine.connect() as conn:
            for json_file in neighborhoods_dir.glob("*.json"):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Insert into database
                    conn.execute(text("""
                        INSERT INTO neighborhoods (
                            name, description, location_data, amenities, 
                            price_ranges, rental_yields, service_charges,
                            market_trends, target_audience, pros, cons, 
                            investment_advice
                        ) VALUES (
                            :name, :description, :location_data, :amenities,
                            :price_ranges, :rental_yields, :service_charges,
                            :market_trends, :target_audience, :pros, :cons,
                            :investment_advice
                        )
                    """), {
                        "name": data.get("name"),
                        "description": data.get("description"),
                        "location_data": json.dumps(data.get("location", {})),
                        "amenities": json.dumps(data.get("amenities", {})),
                        "price_ranges": json.dumps(data.get("price_ranges", {})),
                        "rental_yields": json.dumps(data.get("rental_yields", {})),
                        "service_charges": json.dumps(data.get("service_charges", {})),
                        "market_trends": json.dumps(data.get("market_trends", {})),
                        "target_audience": data.get("target_audience", []),
                        "pros": data.get("pros", []),
                        "cons": data.get("cons", []),
                        "investment_advice": data.get("investment_advice")
                    })
                    
                    # Add to ChromaDB for semantic search
                    self.add_to_chromadb("neighborhoods", data)
                    
                    print(f"✅ Ingested neighborhood: {data.get('name')}")
                    
                except Exception as e:
                    print(f"❌ Error ingesting {json_file}: {e}")
            
            conn.commit()
    
    def ingest_market_updates(self):
        """Ingest market update data"""
        updates_dir = self.dubai_market_dir / "market-updates"
        if not updates_dir.exists():
            print("⚠️ Market updates directory not found")
            return
        
        with self.engine.connect() as conn:
            for json_file in updates_dir.glob("*.json"):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Insert into database
                    conn.execute(text("""
                        INSERT INTO market_updates (
                            period, report_type, summary, key_highlights,
                            market_performance, area_performance, 
                            investment_insights, legislative_updates, forecast
                        ) VALUES (
                            :period, :report_type, :summary, :key_highlights,
                            :market_performance, :area_performance,
                            :investment_insights, :legislative_updates, :forecast
                        )
                    """), {
                        "period": data.get("period"),
                        "report_type": data.get("report_type"),
                        "summary": data.get("summary"),
                        "key_highlights": data.get("key_highlights", []),
                        "market_performance": json.dumps(data.get("market_performance", {})),
                        "area_performance": json.dumps(data.get("area_performance", {})),
                        "investment_insights": json.dumps(data.get("investment_insights", {})),
                        "legislative_updates": json.dumps(data.get("legislative_updates", [])),
                        "forecast": json.dumps(data.get("forecast", {}))
                    })
                    
                    # Add to ChromaDB
                    self.add_to_chromadb("market_updates", data)
                    
                    print(f"✅ Ingested market update: {data.get('period')}")
                    
                except Exception as e:
                    print(f"❌ Error ingesting {json_file}: {e}")
            
            conn.commit()
    
    def ingest_agent_resources(self):
        """Ingest agent success resources"""
        resources_dir = self.agent_resources_dir
        if not resources_dir.exists():
            print("⚠️ Agent resources directory not found")
            return
        
        with self.engine.connect() as conn:
            for category_dir in resources_dir.iterdir():
                if category_dir.is_dir():
                    for json_file in category_dir.glob("*.json"):
                        try:
                            with open(json_file, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                            
                            # Insert into database
                            conn.execute(text("""
                                INSERT INTO agent_resources (
                                    category, title, description, content,
                                    key_strategies, common_scenarios, templates,
                                    related_topics
                                ) VALUES (
                                    :category, :title, :description, :content,
                                    :key_strategies, :common_scenarios, :templates,
                                    :related_topics
                                )
                            """), {
                                "category": data.get("category"),
                                "title": data.get("title"),
                                "description": data.get("description"),
                                "content": data.get("content"),
                                "key_strategies": json.dumps(data.get("key_strategies", [])),
                                "common_scenarios": json.dumps(data.get("common_scenarios", [])),
                                "templates": json.dumps(data.get("templates", [])),
                                "related_topics": data.get("related_topics", [])
                            })
                            
                            # Add to ChromaDB
                            self.add_to_chromadb("agent_resources", data)
                            
                            print(f"✅ Ingested agent resource: {data.get('title')}")
                            
                        except Exception as e:
                            print(f"❌ Error ingesting {json_file}: {e}")
            
            conn.commit()
    
    def ingest_employees(self):
        """Ingest employee data"""
        employees_file = self.company_data_dir / "employees" / "agent-profiles.json"
        if not employees_file.exists():
            print("⚠️ Employee profiles file not found")
            return
        
        try:
            with open(employees_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            with self.engine.connect() as conn:
                # Clear existing data
                conn.execute(text("DELETE FROM employees"))
                
                # Insert employee data
                for employee in data.get('employees', []):
                    conn.execute(text("""
                        INSERT INTO employees (
                            employee_id, name, role, department, specializations,
                            contact_info, experience, languages, achievements,
                            availability, team, manager, performance_metrics
                        ) VALUES (
                            :employee_id, :name, :role, :department, :specializations,
                            :contact_info, :experience, :languages, :achievements,
                            :availability, :team, :manager, :performance_metrics
                        )
                    """), {
                        "employee_id": employee.get("employee_id"),
                        "name": employee.get("name"),
                        "role": employee.get("role"),
                        "department": employee.get("department"),
                        "specializations": employee.get("specializations", []),
                        "contact_info": json.dumps(employee.get("contact_info", {})),
                        "experience": employee.get("experience"),
                        "languages": employee.get("languages", []),
                        "achievements": employee.get("achievements", []),
                        "availability": employee.get("availability"),
                        "team": employee.get("team"),
                        "manager": employee.get("manager"),
                        "performance_metrics": json.dumps(employee.get("performance_metrics", {}))
                    })
                
                self.add_to_chromadb("employees", data)
                
                conn.commit()
                print(f"✅ Ingested {len(data.get('employees', []))} employees")
                
        except Exception as e:
            print(f"❌ Error ingesting employees: {e}")
    
    def ingest_dubai_market_data(self):
        """Ingest Dubai market data into new tables"""
        print("📊 Ingesting Dubai market data...")
        
        # Sample market data for Dubai
        market_data = [
            {
                "date": "2025-01-01",
                "neighborhood": "Dubai Marina",
                "property_type": "apartment",
                "avg_price_per_sqft": 1800.00,
                "transaction_volume": 245,
                "price_change_percent": 8.5,
                "rental_yield": 6.2,
                "market_trend": "rising",
                "off_plan_percentage": 35.0,
                "foreign_investment_percentage": 65.0
            },
            {
                "date": "2025-01-01",
                "neighborhood": "Downtown Dubai",
                "property_type": "apartment",
                "avg_price_per_sqft": 2500.00,
                "transaction_volume": 189,
                "price_change_percent": 12.3,
                "rental_yield": 4.8,
                "market_trend": "rising",
                "off_plan_percentage": 28.0,
                "foreign_investment_percentage": 72.0
            }
        ]
        
        try:
            with self.engine.connect() as conn:
                for data in market_data:
                    conn.execute(text("""
                        INSERT INTO market_data (date, neighborhood, property_type, avg_price_per_sqft, 
                                               transaction_volume, price_change_percent, rental_yield, 
                                               market_trend, off_plan_percentage, foreign_investment_percentage)
                        VALUES (:date, :neighborhood, :property_type, :avg_price_per_sqft, 
                               :transaction_volume, :price_change_percent, :rental_yield, 
                               :market_trend, :off_plan_percentage, :foreign_investment_percentage)
                    """), data)
                conn.commit()
                print(f"✅ Ingested {len(market_data)} market data records")
        except Exception as e:
            print(f"❌ Error ingesting market data: {e}")
    
    def ingest_dubai_regulatory_data(self):
        """Ingest Dubai regulatory data"""
        print("📋 Ingesting Dubai regulatory data...")
        
        regulatory_data = [
            {
                "law_name": "Golden Visa Property Investment",
                "enactment_date": "2019-05-20",
                "description": "Property investment of AED 2 million grants 10-year residency visa",
                "impact_areas": ["foreign_investment", "residency", "property_market"],
                "relevant_stakeholders": ["foreign_investors", "developers", "real_estate_agents"],
                "status": "active",
                "key_provisions": ["AED 2M investment", "10-year visa", "renewable"],
                "compliance_requirements": ["property_registration", "minimum_investment", "annual_renewal"]
            }
        ]
        
        try:
            with self.engine.connect() as conn:
                for data in regulatory_data:
                    conn.execute(text("""
                        INSERT INTO regulatory_updates (law_name, enactment_date, description, impact_areas,
                                                      relevant_stakeholders, status, key_provisions, compliance_requirements)
                        VALUES (:law_name, :enactment_date, :description, :impact_areas,
                               :relevant_stakeholders, :status, :key_provisions, :compliance_requirements)
                    """), data)
                conn.commit()
                print(f"✅ Ingested {len(regulatory_data)} regulatory records")
        except Exception as e:
            print(f"❌ Error ingesting regulatory data: {e}")
    
    def ingest_dubai_developers(self):
        """Ingest Dubai developers data"""
        print("🏢 Ingesting Dubai developers data...")
        
        developers_data = [
            {
                "name": "Emaar Properties",
                "type": "government",
                "market_share": 25.5,
                "total_projects": 150,
                "avg_project_value": 2500000000.00,
                "reputation_score": 9.2,
                "specialties": ["master_planned_communities", "luxury_developments", "mixed_use"],
                "key_projects": ["Burj Khalifa", "Dubai Mall", "Dubai Marina", "Dubai Hills Estate"],
                "financial_strength": "excellent"
            },
            {
                "name": "DAMAC Properties",
                "type": "private",
                "market_share": 8.3,
                "total_projects": 85,
                "avg_project_value": 1800000000.00,
                "reputation_score": 8.7,
                "specialties": ["luxury_residences", "branded_properties", "high_end"],
                "key_projects": ["DAMAC Hills", "AKOYA Oxygen", "DAMAC Towers"],
                "financial_strength": "strong"
            }
        ]
        
        try:
            with self.engine.connect() as conn:
                for data in developers_data:
                    conn.execute(text("""
                        INSERT INTO developers (name, type, market_share, total_projects, avg_project_value,
                                              reputation_score, specialties, key_projects, financial_strength)
                        VALUES (:name, :type, :market_share, :total_projects, :avg_project_value,
                               :reputation_score, :specialties, :key_projects, :financial_strength)
                    """), data)
                conn.commit()
                print(f"✅ Ingested {len(developers_data)} developer records")
        except Exception as e:
            print(f"❌ Error ingesting developers data: {e}")
    
    def ingest_dubai_investment_insights(self):
        """Ingest Dubai investment insights"""
        print("💰 Ingesting Dubai investment insights...")
        
        investment_data = [
            {
                "category": "golden_visa",
                "title": "Golden Visa Property Investment",
                "description": "Property investment pathway to UAE residency",
                "key_benefits": ["10_year_residency", "tax_advantages", "family_inclusion"],
                "requirements": ["AED 2M investment", "freehold_property", "valid_passport"],
                "investment_amount_min": 2000000.00,
                "investment_amount_max": 50000000.00,
                "roi_projection": 8.5,
                "risk_level": "low",
                "target_audience": ["foreign_investors", "expats", "high_net_worth"]
            }
        ]
        
        try:
            with self.engine.connect() as conn:
                for data in investment_data:
                    conn.execute(text("""
                        INSERT INTO investment_insights (category, title, description, key_benefits,
                                                       requirements, investment_amount_min, investment_amount_max,
                                                       roi_projection, risk_level, target_audience)
                        VALUES (:category, :title, :description, :key_benefits,
                               :requirements, :investment_amount_min, :investment_amount_max,
                               :roi_projection, :risk_level, :target_audience)
                    """), data)
                conn.commit()
                print(f"✅ Ingested {len(investment_data)} investment insight records")
        except Exception as e:
            print(f"❌ Error ingesting investment data: {e}")
    
    def add_to_chromadb(self, collection_name, data):
        """Add structured data to ChromaDB for semantic search"""
        try:
            # Get or create collection
            try:
                collection = self.chroma_client.get_collection(collection_name)
            except:
                collection = self.chroma_client.create_collection(collection_name)
            
            # Create document content for embedding
            if collection_name == "neighborhoods":
                content = f"""
                {data.get('name', '')} - {data.get('description', '')}
                Lifestyle: {', '.join(data.get('lifestyle', []))}
                Amenities: {json.dumps(data.get('amenities', {}))}
                Price ranges: {json.dumps(data.get('price_ranges', {}))}
                Investment advice: {data.get('investment_advice', '')}
                """
            elif collection_name == "market_updates":
                content = f"""
                {data.get('period', '')} Market Update
                Summary: {data.get('summary', '')}
                Key highlights: {', '.join(data.get('key_highlights', []))}
                Market performance: {json.dumps(data.get('market_performance', {}))}
                """
            elif collection_name == "agent_resources":
                content = f"""
                {data.get('title', '')} - {data.get('description', '')}
                Content: {data.get('content', '')}
                Key strategies: {json.dumps(data.get('key_strategies', []))}
                """
            elif collection_name == "employees":
                # Handle employee data specifically
                if isinstance(data, dict) and "employees" in data:
                    # This is the full employee list
                    content = f"""
                    Employee Directory:
                    {', '.join([emp.get('name', '') + ' (' + emp.get('role', '') + ')' for emp in data.get('employees', [])])}
                    Departments: {json.dumps(data.get('departments', {}))}
                    """
                else:
                    # This is a single employee
                    content = f"""
                    {data.get('name', '')} - {data.get('role', '')}
                    Department: {data.get('department', '')}
                    Specializations: {', '.join(data.get('specializations', []))}
                    Experience: {data.get('experience', '')}
                    Languages: {', '.join(data.get('languages', []))}
                    Achievements: {', '.join(data.get('achievements', []))}
                    Performance: {data.get('success_rate', '')} success rate, {data.get('average_deal_size', '')} average deal
                    """
            else:
                content = json.dumps(data)
            
            # Add to collection
            collection.add(
                documents=[content],
                metadatas=[{
                    "type": collection_name,
                    "title": data.get("name") or data.get("title") or data.get("period", ""),
                    "source": str(uuid.uuid4())
                }],
                ids=[str(uuid.uuid4())]
            )
            
        except Exception as e:
            print(f"❌ Error adding to ChromaDB: {e}")
    
    def run_full_ingestion(self):
        """Run complete enhanced data ingestion"""
        print("🚀 Starting Enhanced Data Ingestion...")
        
        # Create tables
        self.create_enhanced_tables()
        
        # Ingest all data types
        print("\n📊 Ingesting Dubai Market Intelligence...")
        self.ingest_neighborhoods()
        self.ingest_market_updates()
        
        print("\n👥 Ingesting Agent Resources...")
        self.ingest_agent_resources()
        
        print("\n🏢 Ingesting Company Data...")
        self.ingest_employees()

        print("\n📊 Ingesting Dubai market data...")
        self.ingest_dubai_market_data()

        print("\n📋 Ingesting Dubai regulatory data...")
        self.ingest_dubai_regulatory_data()

        print("\n🏢 Ingesting Dubai developers data...")
        self.ingest_dubai_developers()

        print("\n💰 Ingesting Dubai investment insights...")
        self.ingest_dubai_investment_insights()
        
        print("\n✅ Enhanced Data Ingestion Complete!")

if __name__ == "__main__":
    ingester = EnhancedDataIngester()
    ingester.run_full_ingestion()
