#!/usr/bin/env python3
"""
Data Quality Verification Script
Verifies the generated Dubai real estate simulation data
"""

import pandas as pd
import json
import os
from datetime import datetime

def verify_data_quality():
    """Verify the quality and statistics of generated data"""
    print("🔍 Dubai Real Estate Data Quality Verification")
    print("=" * 60)
    
    data_dir = "upload_data"
    
    # Verify CSV files
    csv_files = [
        "property_listings.csv",
        "transactions.csv", 
        "clients.csv",
        "leads.csv",
        "agent_performance.csv",
        "market_trends.csv",
        "property_analytics.csv",
        "commissions.csv"
    ]
    
    total_records = 0
    csv_stats = {}
    
    print("\n📊 CSV Data Verification:")
    print("-" * 40)
    
    for csv_file in csv_files:
        file_path = os.path.join(data_dir, csv_file)
        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                records = len(df)
                total_records += records
                file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
                
                csv_stats[csv_file] = {
                    'records': records,
                    'size_mb': round(file_size, 2),
                    'columns': len(df.columns)
                }
                
                print(f"✅ {csv_file}: {records:,} records, {file_size:.2f}MB, {len(df.columns)} columns")
                
                # Show sample data for key files
                if csv_file == "property_listings.csv":
                    print(f"   📍 Areas: {df['location'].nunique()} unique areas")
                    print(f"   🏠 Property Types: {df['property_type'].nunique()} types")
                    print(f"   👥 Agents: {df['agent_id'].nunique()} agents")
                    print(f"   💰 Price Range: AED {df['price_aed'].min():,} - {df['price_aed'].max():,}")
                
                elif csv_file == "transactions.csv":
                    print(f"   💵 Transaction Range: AED {df['transaction_amount'].min():,} - {df['transaction_amount'].max():,}")
                    print(f"   📅 Date Range: {df['transaction_date'].min()} to {df['transaction_date'].max()}")
                    print(f"   💰 Commission Range: {df['commission_rate'].min():.1f}% - {df['commission_rate'].max():.1f}%")
                
                elif csv_file == "clients.csv":
                    print(f"   🌍 Nationalities: {df['nationality'].nunique()} countries")
                    print(f"   🎯 Client Types: {df['client_type'].nunique()} types")
                    print(f"   📊 Lead Scores: {df['lead_score'].min()} - {df['lead_score'].max()}")
                
            except Exception as e:
                print(f"❌ Error reading {csv_file}: {e}")
        else:
            print(f"❌ Missing file: {csv_file}")
    
    # Verify PDF files
    print(f"\n📚 PDF Documents Verification:")
    print("-" * 40)
    
    pdf_files = [
        "company_policies.pdf",
        "agent_guide.pdf", 
        "service_charges_guide.pdf",
        "market_report_1.pdf",
        "market_report_2.pdf",
        "market_report_3.pdf",
        "legal_guide_1.pdf",
        "legal_guide_2.pdf",
        "training_material_1.pdf",
        "training_material_2.pdf"
    ]
    
    # Add neighborhood profiles
    areas = ['Dubai_Marina', 'Downtown_Dubai', 'Palm_Jumeirah', 'Business_Bay', 
             'JBR', 'Jumeirah', 'DIFC', 'Emirates_Hills', 'Arabian_Ranches']
    
    for area in areas:
        pdf_files.append(f"{area}_profile.pdf")
    
    pdf_count = 0
    total_pdf_size = 0
    
    for pdf_file in pdf_files:
        file_path = os.path.join(data_dir, pdf_file)
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path) / 1024  # KB
            total_pdf_size += file_size
            pdf_count += 1
            print(f"✅ {pdf_file}: {file_size:.1f}KB")
        else:
            print(f"❌ Missing file: {pdf_file}")
    
    # Summary statistics
    print(f"\n📈 Data Summary:")
    print("-" * 40)
    print(f"📊 Total CSV Records: {total_records:,}")
    print(f"📚 Total PDF Documents: {pdf_count}")
    print(f"💾 Total Data Size: ~{sum([stats['size_mb'] for stats in csv_stats.values()]) + (total_pdf_size/1024):.1f}MB")
    
    # Data quality indicators
    print(f"\n🎯 Data Quality Indicators:")
    print("-" * 40)
    
    if total_records >= 85000:
        print("✅ Comprehensive data volume achieved")
    else:
        print("⚠️ Data volume below target")
    
    if pdf_count >= 18:
        print("✅ Complete knowledge base created")
    else:
        print("⚠️ Some knowledge base documents missing")
    
    # Check for realistic data ranges
    property_file = os.path.join(data_dir, "property_listings.csv")
    if os.path.exists(property_file):
        df = pd.read_csv(property_file)
        price_range = df['price_aed'].max() - df['price_aed'].min()
        if price_range > 10000000:  # 10M AED range
            print("✅ Realistic property price ranges")
        else:
            print("⚠️ Property price ranges may be limited")
    
    # Check transaction data
    transaction_file = os.path.join(data_dir, "transactions.csv")
    if os.path.exists(transaction_file):
        df = pd.read_csv(transaction_file)
        if len(df) >= 50000:
            print("✅ Comprehensive transaction history")
        else:
            print("⚠️ Transaction data may be incomplete")
    
    print(f"\n🎉 Data verification completed!")
    print(f"📁 Data ready for upload to application")
    print(f"🚀 Next step: Follow UPLOAD_GUIDE.md for ingestion")

if __name__ == "__main__":
    verify_data_quality()
