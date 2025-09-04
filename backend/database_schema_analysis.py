#!/usr/bin/env python3
"""
Database Schema Analysis for Dubai Real Estate RAG System
Analyzes current database structure and identifies alignment with system functions
"""

import os
import sys
from sqlalchemy import create_engine, text, MetaData, inspect
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import json

# Add backend to path
sys.path.insert(0, str(os.path.dirname(__file__)))

from env_loader import load_env

load_env()

class DatabaseSchemaAnalyzer:
    def __init__(self):
        self.database_url = os.getenv('DATABASE_URL', 'postgresql://admin:password123@localhost:5432/real_estate_db')
        self.engine = create_engine(self.database_url)
        self.inspector = inspect(self.engine)
        
    def analyze_current_schema(self):
        """Analyze the current database schema"""
        print("🔍 Analyzing Current Database Schema...")
        print("=" * 60)
        
        try:
            # Get all table names
            tables = self.inspector.get_table_names()
            print(f"📊 Total tables found: {len(tables)}")
            
            # Analyze each table
            schema_analysis = {}
            for table_name in sorted(tables):
                print(f"\n📋 Table: {table_name}")
                table_info = self._analyze_table(table_name)
                schema_analysis[table_name] = table_info
                
            # Generate comprehensive report
            self._generate_schema_report(schema_analysis)
            
            # Check for missing tables
            self._check_missing_tables(schema_analysis)
            
            # Check for schema inconsistencies
            self._check_schema_inconsistencies(schema_analysis)
            
        except Exception as e:
            print(f"❌ Error analyzing schema: {e}")
            raise
    
    def _analyze_table(self, table_name):
        """Analyze a specific table"""
        try:
            # Get columns
            columns = self.inspector.get_columns(table_name)
            
            # Get indexes
            indexes = self.inspector.get_indexes(table_name)
            
            # Get foreign keys
            foreign_keys = self.inspector.get_foreign_keys(table_name)
            
            # Get primary keys
            primary_keys = self.inspector.get_pk_constraint(table_name)
            
            table_info = {
                'columns': columns,
                'indexes': indexes,
                'foreign_keys': foreign_keys,
                'primary_keys': primary_keys['constrained_columns'] if primary_keys else [],
                'column_count': len(columns),
                'index_count': len(indexes),
                'fk_count': len(foreign_keys)
            }
            
            # Print table details
            print(f"   Columns: {len(columns)}")
            print(f"   Indexes: {len(indexes)}")
            print(f"   Foreign Keys: {len(foreign_keys)}")
            
            # Show key columns
            key_columns = [col['name'] for col in columns if col.get('primary_key') or col.get('unique')]
            if key_columns:
                print(f"   Key Columns: {', '.join(key_columns)}")
            
            # Show foreign key relationships
            if foreign_keys:
                print("   Foreign Key Relationships:")
                for fk in foreign_keys:
                    print(f"     {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
            
            return table_info
            
        except Exception as e:
            print(f"   ❌ Error analyzing table {table_name}: {e}")
            return None
    
    def _check_missing_tables(self, schema_analysis):
        """Check for missing tables that our functions expect"""
        print("\n🔍 Checking for Missing Tables...")
        print("=" * 60)
        
        # Expected tables based on our system functions
        expected_tables = {
            # Core system tables
            'users': 'User authentication and management',
            'properties': 'Property listings and details',
            'conversations': 'Chat conversations and sessions',
            'messages': 'Individual chat messages',
            
            # Phase 3 tables
            'entity_detections': 'NLP entity extraction results',
            'context_cache': 'Conversation context storage',
            'leads': 'Lead management and tracking',
            'notifications': 'System notifications',
            'lead_history': 'Lead interaction history',
            'rich_content_metadata': 'Content analysis metadata',
            
            # Phase 4B ML tables
            'ml_automated_reports': 'AI-generated reports',
            'ml_smart_notifications': 'Smart notification system',
            'ml_performance_analytics': 'Performance metrics',
            'ml_market_intelligence': 'Market analysis data',
            'ml_model_performance': 'ML model metrics',
            'ml_websocket_connections': 'Real-time connections',
            'ml_notification_templates': 'Notification templates',
            'ml_insights_log': 'AI insights logging',
            
            # Additional expected tables
            'generated_documents': 'AI-generated content',
            'tasks': 'Task management',
            'user_sessions': 'User session tracking',
            'roles': 'Role-based access control',
            'permissions': 'Permission definitions'
        }
        
        missing_tables = []
        for table_name, description in expected_tables.items():
            if table_name not in schema_analysis:
                missing_tables.append((table_name, description))
                print(f"❌ Missing: {table_name} - {description}")
            else:
                print(f"✅ Found: {table_name}")
        
        if missing_tables:
            print(f"\n⚠️  Total missing tables: {len(missing_tables)}")
            print("These tables are required for full system functionality.")
        else:
            print("\n🎉 All expected tables are present!")
    
    def _check_schema_inconsistencies(self, schema_analysis):
        """Check for schema inconsistencies and optimization opportunities"""
        print("\n🔍 Checking Schema Inconsistencies...")
        print("=" * 60)
        
        issues_found = []
        
        for table_name, table_info in schema_analysis.items():
            if not table_info:
                continue
                
            # Check for missing primary keys
            if not table_info['primary_keys']:
                issues_found.append(f"Table '{table_name}' has no primary key")
                print(f"⚠️  {table_name}: No primary key defined")
            
            # Check for tables without indexes
            if table_info['index_count'] == 0:
                issues_found.append(f"Table '{table_name}' has no indexes")
                print(f"⚠️  {table_name}: No indexes defined")
            
            # Check for missing updated_at columns
            columns = [col['name'] for col in table_info['columns']]
            if 'updated_at' not in columns and 'created_at' in columns:
                issues_found.append(f"Table '{table_name}' missing updated_at column")
                print(f"⚠️  {table_name}: Missing updated_at column")
            
            # Check for missing created_at columns
            if 'created_at' not in columns:
                issues_found.append(f"Table '{table_name}' missing created_at column")
                print(f"⚠️  {table_name}: Missing created_at column")
        
        # Check for specific optimization opportunities
        self._check_optimization_opportunities(schema_analysis)
        
        if issues_found:
            print(f"\n⚠️  Total issues found: {len(issues_found)}")
        else:
            print("\n✅ No schema inconsistencies found!")
    
    def _check_optimization_opportunities(self, schema_analysis):
        """Check for database optimization opportunities"""
        print("\n🚀 Optimization Opportunities...")
        print("=" * 60)
        
        # Check for missing composite indexes
        tables_with_fk = {name: info for name, info in schema_analysis.items() 
                         if info and info['fk_count'] > 0}
        
        for table_name, table_info in tables_with_fk.items():
            if table_info['fk_count'] > 0 and table_info['index_count'] < table_info['fk_count']:
                print(f"💡 {table_name}: Consider adding indexes for foreign key columns")
        
        # Check for JSONB columns without GIN indexes
        for table_name, table_info in schema_analysis.items():
            if not table_info:
                continue
                
            jsonb_columns = [col['name'] for col in table_info['columns'] 
                           if col.get('type') and 'JSON' in str(col['type'])]
            
            if jsonb_columns:
                # Check if there are GIN indexes for JSONB columns
                gin_indexes = [idx for idx in table_info['indexes'] 
                             if any('gin' in str(idx.get('type', '')).lower() 
                                   for idx in table_info['indexes'])]
                
                if not gin_indexes:
                    print(f"💡 {table_name}: Consider adding GIN indexes for JSONB columns: {jsonb_columns}")
    
    def _generate_schema_report(self, schema_analysis):
        """Generate a comprehensive schema report"""
        print("\n📊 Schema Analysis Report...")
        print("=" * 60)
        
        report = {
            'analysis_date': datetime.now().isoformat(),
            'total_tables': len(schema_analysis),
            'tables': {},
            'summary': {
                'tables_with_pk': 0,
                'tables_without_pk': 0,
                'tables_with_indexes': 0,
                'tables_without_indexes': 0,
                'total_columns': 0,
                'total_indexes': 0,
                'total_foreign_keys': 0
            }
        }
        
        for table_name, table_info in schema_analysis.items():
            if not table_info:
                continue
                
            report['tables'][table_name] = {
                'column_count': table_info['column_count'],
                'index_count': table_info['index_count'],
                'fk_count': table_info['fk_count'],
                'has_primary_key': bool(table_info['primary_keys']),
                'columns': [col['name'] for col in table_info['columns']]
            }
            
            # Update summary
            report['summary']['total_columns'] += table_info['column_count']
            report['summary']['total_indexes'] += table_info['index_count']
            report['summary']['total_foreign_keys'] += table_info['fk_count']
            
            if table_info['primary_keys']:
                report['summary']['tables_with_pk'] += 1
            else:
                report['summary']['tables_without_pk'] += 1
                
            if table_info['index_count'] > 0:
                report['summary']['tables_with_indexes'] += 1
            else:
                report['summary']['tables_without_indexes'] += 1
        
        # Print summary
        print(f"📈 Schema Summary:")
        print(f"   Total Tables: {report['summary']['total_tables']}")
        print(f"   Total Columns: {report['summary']['total_columns']}")
        print(f"   Total Indexes: {report['summary']['total_indexes']}")
        print(f"   Total Foreign Keys: {report['summary']['total_foreign_keys']}")
        print(f"   Tables with Primary Keys: {report['summary']['tables_with_pk']}")
        print(f"   Tables without Primary Keys: {report['summary']['tables_without_pk']}")
        print(f"   Tables with Indexes: {report['summary']['tables_with_indexes']}")
        print(f"   Tables without Indexes: {report['summary']['tables_without_indexes']}")
        
        # Save report to file
        report_file = f"database_schema_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n💾 Detailed report saved to: {report_file}")
    
    def check_table_relationships(self):
        """Check table relationships and foreign key integrity"""
        print("\n🔗 Checking Table Relationships...")
        print("=" * 60)
        
        try:
            with self.engine.connect() as conn:
                # Check for orphaned foreign key references
                orphaned_fks = []
                
                for table_name in self.inspector.get_table_names():
                    foreign_keys = self.inspector.get_foreign_keys(table_name)
                    
                    for fk in foreign_keys:
                        referenced_table = fk['referred_table']
                        if referenced_table not in self.inspector.get_table_names():
                            orphaned_fks.append(f"Table '{table_name}' references non-existent table '{referenced_table}'")
                
                if orphaned_fks:
                    print("❌ Orphaned foreign key references found:")
                    for fk in orphaned_fks:
                        print(f"   {fk}")
                else:
                    print("✅ All foreign key references are valid")
                    
        except Exception as e:
            print(f"❌ Error checking relationships: {e}")
    
    def run_full_analysis(self):
        """Run the complete database schema analysis"""
        print("🚀 Starting Comprehensive Database Schema Analysis")
        print("=" * 80)
        
        try:
            # Analyze current schema
            self.analyze_current_schema()
            
            # Check relationships
            self.check_table_relationships()
            
            print("\n🎉 Database Schema Analysis Complete!")
            print("=" * 80)
            
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
            raise

def main():
    """Main function to run the database schema analysis"""
    try:
        analyzer = DatabaseSchemaAnalyzer()
        analyzer.run_full_analysis()
    except Exception as e:
        print(f"❌ Database schema analysis failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
