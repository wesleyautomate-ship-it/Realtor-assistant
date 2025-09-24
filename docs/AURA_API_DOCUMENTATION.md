# AURA API Documentation
## Complete PropertyPro AI AURA Integration Reference

**Version**: 1.0  
**Last Updated**: September 24, 2025  
**Base URL**: `http://localhost:8000`

---

## 🎯 **Overview**

PropertyPro AI's AURA integration provides a comprehensive API ecosystem with 95+ endpoints across 5 specialized routers. This implementation delivers enterprise-grade workflow automation specifically designed for Dubai real estate professionals.

### **Key Features**
- **95+ API Endpoints** across 5 comprehensive routers
- **Advanced AI Workflow Orchestration** with dependency management
- **Real-Time Progress Tracking** with pause/resume/cancel capabilities
- **Dubai Market Specialization** with RERA-compliant templates
- **Enterprise-Grade Error Handling** with proper HTTP status codes

---

## 🔐 **Authentication**

All AURA endpoints require JWT authentication. Include the access token in the Authorization header:

```http
Authorization: Bearer <your_access_token>
```

### **Getting Access Token**
```http
POST /auth/login
Content-Type: application/json

{
  "email": "agent@example.com",
  "password": "your_password"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

---

## 🈚 **Marketing Automation Router**
**Base Path**: `/api/v1/marketing`

### **1. Create Full Marketing Package**
Generate a complete marketing package with one API call.

```http
POST /api/v1/marketing/campaigns/full-package
Content-Type: application/json

{
  "property_id": "prop_123",
  "campaign_type": "new_listing",
  "target_channels": ["postcard", "email", "social"],
  "budget": 5000,
  "target_audience": "luxury_buyers",
  "customizations": {
    "headline": "Luxury Living in Dubai Marina",
    "call_to_action": "Schedule Private Viewing"
  }
}
```

**Response:**
```json
{
  "campaign_id": "camp_456",
  "status": "processing",
  "estimated_completion": "2025-09-24T16:30:00Z",
  "package_contents": {
    "postcard_design": "pending",
    "email_template": "pending",
    "social_posts": "pending",
    "landing_page": "pending"
  },
  "tracking_url": "/api/v1/marketing/campaigns/camp_456/status"
}
```

### **2. Get Marketing Templates**
Retrieve RERA-compliant templates for Dubai market.

```http
GET /api/v1/marketing/templates?category=postcard&market=dubai
```

**Response:**
```json
{
  "templates": [
    {
      "id": "tmpl_dubai_luxury",
      "name": "Dubai Luxury Listing",
      "category": "postcard",
      "compliance": "RERA_approved",
      "preview_url": "https://cdn.example.com/preview/tmpl_dubai_luxury.jpg",
      "customizable_fields": ["headline", "price", "property_features", "agent_info"]
    }
  ],
  "total": 15,
  "market_specific": true
}
```

### **3. Campaign Approval Workflow**
Submit campaign for approval through professional workflow.

```http
POST /api/v1/marketing/campaigns/camp_456/approval
Content-Type: application/json

{
  "action": "submit_for_review",
  "reviewer_id": "user_789",
  "notes": "Please review pricing and compliance",
  "priority": "standard"
}
```

**Response:**
```json
{
  "approval_id": "appr_321",
  "status": "pending_review",
  "assigned_reviewer": "user_789",
  "estimated_review_time": "2 hours",
  "workflow_stage": "review",
  "next_actions": ["approve", "request_changes", "reject"]
}
```

### **4. Generate Campaign Assets**
Trigger background generation of marketing assets.

```http
POST /api/v1/marketing/campaigns/camp_456/assets/generate
Content-Type: application/json

{
  "asset_types": ["pdf_flyer", "social_graphics", "email_html"],
  "priority": "high",
  "format_options": {
    "pdf_flyer": {"size": "A4", "quality": "print_ready"},
    "social_graphics": {"platforms": ["instagram", "facebook"], "sizes": ["story", "post"]}
  }
}
```

**Response:**
```json
{
  "generation_job_id": "job_654",
  "status": "queued",
  "estimated_completion": "5 minutes",
  "assets_to_generate": 8,
  "progress_tracking": "/api/v1/marketing/assets/job_654/status"
}
```

### **5. Marketing Analytics Summary**
Get comprehensive marketing performance metrics.

```http
GET /api/v1/marketing/analytics/summary?period=30d&campaign_type=all
```

**Response:**
```json
{
  "summary": {
    "total_campaigns": 24,
    "active_campaigns": 8,
    "completed_campaigns": 16,
    "total_spend": 45000,
    "average_response_rate": 0.12,
    "roi": 3.4
  },
  "performance_by_channel": {
    "postcard": {"campaigns": 10, "response_rate": 0.08, "cost_per_lead": 125},
    "email": {"campaigns": 18, "response_rate": 0.15, "cost_per_lead": 45},
    "social": {"campaigns": 20, "response_rate": 0.18, "cost_per_lead": 65}
  },
  "top_performing_campaigns": [
    {
      "campaign_id": "camp_123",
      "name": "Palm Jumeirah Luxury Launch",
      "response_rate": 0.28,
      "leads_generated": 47,
      "roi": 5.8
    }
  ]
}
```

---

## 📊 **CMA & Analytics Router**
**Base Path**: `/api/v1/cma`

### **1. Generate CMA Report**
Create comprehensive comparative market analysis.

```http
POST /api/v1/cma/reports
Content-Type: application/json

{
  "subject_property": {
    "address": "Dubai Marina, Marina Heights Tower",
    "bedrooms": 2,
    "bathrooms": 2,
    "area_sqft": 1200,
    "property_type": "apartment"
  },
  "analysis_options": {
    "comparable_count": 6,
    "radius_km": 2.0,
    "time_frame_months": 12,
    "include_market_trends": true,
    "include_price_forecast": true
  },
  "report_format": "comprehensive"
}
```

**Response:**
```json
{
  "cma_report_id": "cma_789",
  "status": "processing",
  "estimated_completion": "3 minutes",
  "report_sections": {
    "comparables_analysis": "pending",
    "market_trends": "pending",
    "pricing_recommendation": "pending",
    "marketing_strategy": "pending"
  },
  "download_url": "will_be_available_on_completion"
}
```

### **2. Quick Property Valuation**
Get instant property pricing estimate.

```http
POST /api/v1/cma/valuation/quick
Content-Type: application/json

{
  "property": {
    "location": "Dubai Marina",
    "bedrooms": 2,
    "bathrooms": 2,
    "area_sqft": 1200,
    "property_type": "apartment",
    "amenities": ["swimming_pool", "gym", "parking"]
  }
}
```

**Response:**
```json
{
  "valuation": {
    "estimated_value": 2450000,
    "currency": "AED",
    "confidence_level": 0.87,
    "value_range": {
      "low": 2300000,
      "high": 2600000
    },
    "price_per_sqft": 2042,
    "market_status": "stable",
    "comparable_properties_used": 12
  },
  "market_context": {
    "neighborhood": "Dubai Marina",
    "recent_sales_trend": "stable",
    "average_days_on_market": 45,
    "inventory_level": "balanced"
  }
}
```

### **3. Analytics Dashboard Overview**
Comprehensive business intelligence dashboard.

```http
GET /api/v1/cma/analytics/dashboard/overview?user_id=user_123&period=30d
```

**Response:**
```json
{
  "performance_overview": {
    "total_listings": 18,
    "active_listings": 12,
    "closed_deals": 6,
    "total_volume": 15600000,
    "average_days_to_close": 38,
    "conversion_rate": 0.33
  },
  "market_insights": {
    "hot_neighborhoods": ["Dubai Marina", "JBR", "DIFC"],
    "price_trends": {
      "apartments": {"trend": "up", "change_percent": 0.08},
      "villas": {"trend": "stable", "change_percent": 0.02}
    },
    "inventory_status": "balanced"
  },
  "personal_metrics": {
    "listings_this_month": 8,
    "showings_scheduled": 24,
    "leads_generated": 47,
    "follow_ups_due": 12
  }
}
```

### **4. Agent Performance Metrics**
Individual agent performance analytics.

```http
GET /api/v1/cma/analytics/performance/user_123?period=90d&include_comparisons=true
```

**Response:**
```json
{
  "agent_performance": {
    "listings_taken": 24,
    "properties_sold": 8,
    "gross_commission": 485000,
    "average_list_price": 2850000,
    "average_sale_price": 2720000,
    "days_on_market_avg": 42,
    "conversion_rate": 0.33
  },
  "market_comparison": {
    "rank_in_brokerage": 3,
    "total_agents": 45,
    "performance_percentile": 0.85,
    "areas_of_strength": ["client_communication", "pricing_accuracy"],
    "improvement_opportunities": ["marketing_reach", "lead_conversion"]
  },
  "trending": {
    "listings": "up_18_percent",
    "sales": "up_12_percent",
    "commission": "up_22_percent"
  }
}
```

### **5. Custom Report Generation**
Generate tailored analytics reports.

```http
POST /api/v1/cma/analytics/reports/generate
Content-Type: application/json

{
  "report_type": "market_analysis",
  "parameters": {
    "location": "Dubai Marina",
    "property_types": ["apartment", "penthouse"],
    "price_range": {"min": 1000000, "max": 5000000},
    "time_period": "12_months"
  },
  "output_format": "pdf",
  "include_charts": true,
  "branding": "agent_branded"
}
```

**Response:**
```json
{
  "report_job_id": "rpt_456",
  "status": "processing",
  "estimated_completion": "8 minutes",
  "report_sections": [
    "executive_summary",
    "market_overview",
    "price_trends",
    "inventory_analysis",
    "recommendations"
  ],
  "download_url": "will_be_available_on_completion"
}
```

---

## 📲 **Social Media Router**
**Base Path**: `/api/v1/social`

### **1. Create Platform-Optimized Posts**
Generate social media content optimized for specific platforms.

```http
POST /api/v1/social/posts
Content-Type: application/json

{
  "property_id": "prop_123",
  "platforms": ["instagram", "facebook", "linkedin"],
  "post_type": "new_listing",
  "content_style": "luxury",
  "include_property_details": true,
  "call_to_action": "dm_for_viewing",
  "hashtags": "auto_generate"
}
```

**Response:**
```json
{
  "posts": [
    {
      "platform": "instagram",
      "content": "🏠✨ NEW LISTING ALERT! Stunning 2BR apartment in Dubai Marina with breathtaking views! Perfect for luxury living. DM for private viewing! #DubaiMarina #LuxuryRealEstate #NewListing #DubaiLife",
      "image_suggestions": ["hero_shot", "view_from_balcony", "interior_luxury"],
      "optimal_posting_time": "2025-09-24T18:00:00Z",
      "expected_reach": 2500
    }
  ],
  "campaign_id": "social_camp_789",
  "scheduling_options": "available"
}
```

### **2. Multi-Post Social Campaigns**
Create coordinated campaigns across platforms.

```http
POST /api/v1/social/campaigns
Content-Type: application/json

{
  "campaign_name": "Marina Heights Launch Campaign",
  "property_id": "prop_123",
  "campaign_duration_days": 14,
  "platforms": ["instagram", "facebook", "linkedin"],
  "content_calendar": {
    "frequency": "daily",
    "post_types": ["hero_image", "detail_shots", "lifestyle", "testimonial"]
  },
  "budget": 3000,
  "target_audience": "luxury_property_buyers"
}
```

**Response:**
```json
{
  "campaign_id": "social_camp_456",
  "status": "created",
  "total_posts_planned": 42,
  "content_calendar": [
    {
      "date": "2025-09-24",
      "platform": "instagram",
      "post_type": "hero_image",
      "status": "scheduled"
    }
  ],
  "estimated_reach": 15000,
  "budget_allocation": {
    "instagram": 1500,
    "facebook": 1000,
    "linkedin": 500
  }
}
```

### **3. Dubai Real Estate Hashtag Research**
Get optimized hashtags for Dubai real estate market.

```http
POST /api/v1/social/hashtags/research
Content-Type: application/json

{
  "property_type": "luxury_apartment",
  "location": "Dubai Marina",
  "target_audience": "investors",
  "platform": "instagram",
  "hashtag_count": 20
}
```

**Response:**
```json
{
  "recommended_hashtags": [
    "#DubaiMarina",
    "#LuxuryRealEstate",
    "#DubaiProperties",
    "#PropertyInvestment",
    "#DubaiLife",
    "#MarinaTower",
    "#LuxuryLiving",
    "#DubaiInvestment"
  ],
  "hashtag_analytics": {
    "#DubaiMarina": {"posts": 125000, "engagement_rate": 0.045},
    "#LuxuryRealEstate": {"posts": 89000, "engagement_rate": 0.038}
  },
  "trending_hashtags": ["#DubaiExpo2025", "#NewDubai"],
  "market_specific": true
}
```

### **4. Content Scheduling Management**
View and manage upcoming social media content.

```http
GET /api/v1/social/schedule/upcoming?days=7&platform=all
```

**Response:**
```json
{
  "upcoming_posts": [
    {
      "post_id": "post_123",
      "scheduled_time": "2025-09-24T18:00:00Z",
      "platform": "instagram",
      "content": "🏠✨ NEW LISTING ALERT! Stunning 2BR apartment...",
      "property_id": "prop_123",
      "status": "scheduled",
      "campaign_id": "social_camp_456"
    }
  ],
  "total_scheduled": 28,
  "platforms_summary": {
    "instagram": 12,
    "facebook": 10,
    "linkedin": 6
  }
}
```

### **5. Social Media Performance Analytics**
Track social media campaign performance.

```http
GET /api/v1/social/analytics/summary?period=30d&campaign_id=social_camp_456
```

**Response:**
```json
{
  "campaign_performance": {
    "total_posts": 42,
    "total_reach": 18500,
    "total_engagement": 2240,
    "engagement_rate": 0.121,
    "leads_generated": 28,
    "cost_per_lead": 107.14
  },
  "platform_breakdown": {
    "instagram": {
      "posts": 18,
      "reach": 8200,
      "engagement": 1100,
      "leads": 15
    },
    "facebook": {
      "posts": 15,
      "reach": 6800,
      "engagement": 820,
      "leads": 9
    },
    "linkedin": {
      "posts": 9,
      "reach": 3500,
      "engagement": 320,
      "leads": 4
    }
  },
  "top_performing_posts": [
    {
      "post_id": "post_789",
      "platform": "instagram",
      "reach": 1200,
      "engagement": 145,
      "engagement_rate": 0.121
    }
  ]
}
```

---

## 💼 **Workflow Orchestration Router**
**Base Path**: `/api/v1/workflows`

### **1. Execute Workflow Package**
Start execution of predefined workflow packages.

```http
POST /api/v1/workflows/packages/execute
Content-Type: application/json

{
  "package_name": "new_listing_package",
  "parameters": {
    "property_id": "prop_123",
    "listing_price": 2500000,
    "marketing_budget": 5000,
    "target_timeline": "2_weeks",
    "priority": "high"
  },
  "customizations": {
    "skip_social_media": false,
    "include_premium_photography": true,
    "rush_delivery": true
  }
}
```

**Response:**
```json
{
  "execution_id": "exec_789",
  "package_name": "new_listing_package",
  "status": "running",
  "started_at": "2025-09-24T15:30:00Z",
  "estimated_completion": "2025-09-24T17:15:00Z",
  "total_steps": 12,
  "completed_steps": 0,
  "current_step": {
    "step_name": "property_analysis",
    "status": "running",
    "estimated_duration": "5 minutes"
  },
  "progress_url": "/api/v1/workflows/packages/status/exec_789"
}
```

### **2. Real-Time Progress Tracking**
Monitor workflow execution progress in real-time.

```http
GET /api/v1/workflows/packages/status/exec_789
```

**Response:**
```json
{
  "execution_id": "exec_789",
  "package_name": "new_listing_package",
  "status": "running",
  "progress_percentage": 42,
  "current_step": {
    "step_id": 5,
    "step_name": "marketing_campaign_creation",
    "status": "running",
    "started_at": "2025-09-24T15:42:00Z",
    "estimated_completion": "2025-09-24T15:47:00Z"
  },
  "completed_steps": [
    {
      "step_id": 1,
      "step_name": "property_analysis",
      "status": "completed",
      "duration": "4 minutes",
      "output": {"cma_report_id": "cma_456", "market_score": 8.5}
    },
    {
      "step_id": 2,
      "step_name": "pricing_recommendation",
      "status": "completed",
      "duration": "2 minutes",
      "output": {"recommended_price": 2450000, "confidence": 0.89}
    }
  ],
  "remaining_steps": 7,
  "estimated_time_remaining": "33 minutes"
}
```

### **3. Workflow Control (Pause/Resume/Cancel)**
Control workflow execution with pause, resume, or cancel operations.

```http
POST /api/v1/workflows/packages/exec_789/control
Content-Type: application/json

{
  "action": "pause",
  "reason": "Client requested changes to marketing approach",
  "notify_stakeholders": true
}
```

**Response:**
```json
{
  "execution_id": "exec_789",
  "action": "pause",
  "status": "paused",
  "paused_at": "2025-09-24T15:45:00Z",
  "current_step_preserved": "marketing_campaign_creation",
  "resume_capability": true,
  "stakeholders_notified": ["user_123", "user_456"],
  "next_actions": ["resume", "cancel", "modify_parameters"]
}
```

### **4. Workflow Execution History**
View historical workflow executions and outcomes.

```http
GET /api/v1/workflows/packages/history?user_id=user_123&limit=20&status=all
```

**Response:**
```json
{
  "executions": [
    {
      "execution_id": "exec_789",
      "package_name": "new_listing_package",
      "property_id": "prop_123",
      "status": "completed",
      "started_at": "2025-09-24T15:30:00Z",
      "completed_at": "2025-09-24T17:12:00Z",
      "total_duration": "1h 42m",
      "success_rate": 1.0,
      "deliverables_created": 8
    },
    {
      "execution_id": "exec_654",
      "package_name": "lead_nurturing_package",
      "lead_id": "lead_456",
      "status": "completed",
      "started_at": "2025-09-23T14:00:00Z",
      "completed_at": "2025-09-23T14:28:00Z",
      "total_duration": "28m",
      "success_rate": 1.0,
      "leads_contacted": 15
    }
  ],
  "summary": {
    "total_executions": 47,
    "success_rate": 0.94,
    "average_duration": "45 minutes",
    "most_used_package": "new_listing_package"
  }
}
```

### **5. Available Workflow Templates**
Get list of available workflow packages and their configurations.

```http
GET /api/v1/workflows/packages/templates
```

**Response:**
```json
{
  "workflow_packages": [
    {
      "package_name": "new_listing_package",
      "display_name": "New Listing Package",
      "description": "Complete property listing workflow including CMA, marketing, and social media",
      "estimated_duration": "45 minutes",
      "steps_count": 12,
      "required_parameters": ["property_id", "listing_price"],
      "optional_parameters": ["marketing_budget", "target_timeline"],
      "deliverables": [
        "CMA Report",
        "Marketing Campaign",
        "Social Media Content",
        "Property Listing",
        "Photography Schedule"
      ]
    },
    {
      "package_name": "lead_nurturing_package",
      "display_name": "Lead Nurturing Package",
      "description": "Automated lead nurturing sequence with personalized content",
      "estimated_duration": "30 minutes",
      "steps_count": 8,
      "required_parameters": ["lead_id"],
      "deliverables": [
        "Personalized Email Sequence",
        "Follow-up Schedule",
        "Property Recommendations",
        "Market Insights Report"
      ]
    },
    {
      "package_name": "client_onboarding_package",
      "display_name": "Client Onboarding Package",
      "description": "Complete new client onboarding with welcome materials and setup",
      "estimated_duration": "20 minutes",
      "steps_count": 6,
      "required_parameters": ["client_id"],
      "deliverables": [
        "Welcome Package",
        "Service Overview",
        "Market Briefing",
        "Communication Preferences Setup"
      ]
    }
  ]
}
```

---

## 📈 **Advanced Analytics Router**
**Base Path**: `/api/v1/analytics`

### **1. Performance Overview Dashboard**
Comprehensive performance overview with KPIs.

```http
GET /api/v1/analytics/dashboard/overview?user_id=user_123&period=30d
```

**Response:**
```json
{
  "performance_overview": {
    "listings_active": 12,
    "listings_sold": 6,
    "total_volume": 15600000,
    "gross_commission": 468000,
    "conversion_rate": 0.33,
    "average_days_on_market": 42
  },
  "kpi_trends": {
    "listings": {"current": 12, "previous": 10, "change": 0.2},
    "sales": {"current": 6, "previous": 4, "change": 0.5},
    "volume": {"current": 15600000, "previous": 12400000, "change": 0.26}
  },
  "goal_progress": {
    "monthly_sales_target": {"target": 8, "current": 6, "progress": 0.75},
    "volume_target": {"target": 20000000, "current": 15600000, "progress": 0.78}
  },
  "recent_activities": [
    {"type": "listing_created", "property": "Marina Heights 2BR", "timestamp": "2025-09-24T14:30:00Z"},
    {"type": "offer_received", "property": "JBR Penthouse", "amount": 4200000, "timestamp": "2025-09-24T13:45:00Z"}
  ]
}
```

### **2. Market Insights and Forecasting**
Advanced market intelligence and trend forecasting.

```http
GET /api/v1/analytics/insights/market?location=dubai_marina&property_type=apartment&forecast_months=6
```

**Response:**
```json
{
  "market_insights": {
    "location": "Dubai Marina",
    "property_type": "apartment",
    "current_market_status": "stable_growth",
    "inventory_level": "balanced",
    "price_trend": "upward",
    "demand_level": "high"
  },
  "price_forecasting": {
    "current_avg_price": 2450000,
    "6_month_forecast": 2580000,
    "confidence_level": 0.78,
    "factors": ["infrastructure_development", "tourism_recovery", "expo_impact"]
  },
  "market_dynamics": {
    "supply": {
      "new_developments": 8,
      "expected_completions": 1200,
      "timeline": "next_18_months"
    },
    "demand": {
      "buyer_interest": "high",
      "international_buyers": 0.35,
      "investor_activity": "strong"
    }
  },
  "comparable_neighborhoods": [
    {"name": "JBR", "price_differential": 0.15, "trend": "similar"},
    {"name": "Downtown Dubai", "price_differential": 0.25, "trend": "stronger"}
  ]
}
```

### **3. System Health Monitoring**
Monitor AURA system health and performance.

```http
GET /api/v1/analytics/health/system
```

**Response:**
```json
{
  "system_status": "healthy",
  "last_updated": "2025-09-24T15:30:00Z",
  "services": {
    "api_gateway": {"status": "healthy", "response_time": "45ms", "uptime": "99.9%"},
    "database": {"status": "healthy", "connections": 15, "query_avg": "12ms"},
    "ai_services": {"status": "healthy", "queue_length": 3, "avg_processing": "2.3s"},
    "workflow_engine": {"status": "healthy", "active_workflows": 8, "success_rate": "94%"},
    "file_storage": {"status": "healthy", "usage": "67%", "availability": "100%"}
  },
  "performance_metrics": {
    "api_requests_per_minute": 245,
    "workflow_completions_today": 23,
    "error_rate": 0.002,
    "user_sessions_active": 12
  },
  "alerts": [],
  "maintenance_scheduled": null
}
```

### **4. Custom Analytics Reports**
Generate custom analytics reports for specific metrics.

```http
POST /api/v1/analytics/reports/custom
Content-Type: application/json

{
  "report_name": "Q3 Performance Analysis",
  "date_range": {
    "start": "2025-07-01",
    "end": "2025-09-30"
  },
  "metrics": [
    "listings_taken",
    "properties_sold",
    "gross_commission",
    "conversion_rate",
    "market_share"
  ],
  "segments": ["property_type", "price_range", "location"],
  "comparisons": ["previous_quarter", "year_over_year"],
  "visualization": "charts_and_tables",
  "format": "pdf"
}
```

**Response:**
```json
{
  "report_id": "rpt_analytics_789",
  "status": "processing",
  "estimated_completion": "5 minutes",
  "report_sections": [
    "executive_summary",
    "performance_metrics",
    "market_analysis",
    "trend_analysis",
    "recommendations"
  ],
  "download_url": "will_be_available_on_completion",
  "scheduled_delivery": null
}
```

### **5. Agent Performance Comparison**
Compare individual agent performance against team and market.

```http
GET /api/v1/analytics/performance/agent/user_123?include_team_comparison=true&include_market_benchmarks=true
```

**Response:**
```json
{
  "agent_metrics": {
    "listings_this_quarter": 18,
    "sales_this_quarter": 7,
    "commission_this_quarter": 385000,
    "conversion_rate": 0.39,
    "avg_days_on_market": 35,
    "client_satisfaction": 4.8
  },
  "team_comparison": {
    "rank": 3,
    "total_team_members": 12,
    "percentile": 0.75,
    "above_team_average": ["conversion_rate", "client_satisfaction"],
    "below_team_average": ["listing_volume"]
  },
  "market_benchmarks": {
    "market_avg_conversion": 0.28,
    "market_avg_days_on_market": 48,
    "performance_vs_market": {
      "conversion_rate": "significantly_above",
      "days_on_market": "significantly_below",
      "overall_performance": "top_quartile"
    }
  },
  "improvement_recommendations": [
    "Increase listing acquisition activities",
    "Focus on higher-value properties",
    "Leverage strong conversion rate for team leadership"
  ]
}
```

---

## 🔄 **Common Response Patterns**

### **Success Response**
```json
{
  "status": "success",
  "data": { /* endpoint-specific data */ },
  "message": "Operation completed successfully",
  "timestamp": "2025-09-24T15:30:00Z"
}
```

### **Error Response**
```json
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid property ID provided",
    "details": {
      "field": "property_id",
      "value": "invalid_prop_123",
      "expected": "Valid property ID format"
    }
  },
  "timestamp": "2025-09-24T15:30:00Z"
}
```

### **Async Operation Response**
```json
{
  "status": "accepted",
  "job_id": "job_12345",
  "estimated_completion": "2025-09-24T15:35:00Z",
  "progress_url": "/api/v1/status/job_12345",
  "webhook_url": "optional_callback_url"
}
```

---

## 📋 **Status Codes**

| Code | Description | Usage |
|------|-------------|--------|
| 200 | OK | Successful GET requests |
| 201 | Created | Successful POST requests creating resources |
| 202 | Accepted | Async operations started successfully |
| 400 | Bad Request | Invalid request parameters |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 422 | Unprocessable Entity | Validation errors |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server-side error |
| 503 | Service Unavailable | Temporary service outage |

---

## 🔧 **Rate Limits**

### **Standard Limits**
- **General API**: 1000 requests/hour per user
- **Workflow Execution**: 10 concurrent workflows per user
- **Asset Generation**: 50 assets/hour per user
- **Analytics Reports**: 20 reports/day per user

### **Premium Limits**
- **General API**: 5000 requests/hour per user
- **Workflow Execution**: 25 concurrent workflows per user
- **Asset Generation**: 200 assets/hour per user
- **Analytics Reports**: 100 reports/day per user

---

## 🔍 **Error Codes**

### **Authentication Errors**
- `AUTH_001`: Invalid credentials
- `AUTH_002`: Token expired
- `AUTH_003`: Insufficient permissions

### **Validation Errors**
- `VAL_001`: Missing required field
- `VAL_002`: Invalid field format
- `VAL_003`: Value out of range

### **Workflow Errors**
- `WF_001`: Workflow package not found
- `WF_002`: Invalid workflow parameters
- `WF_003`: Workflow execution failed

### **System Errors**
- `SYS_001`: Service temporarily unavailable
- `SYS_002`: Database connection error
- `SYS_003`: External service timeout

---

## 🚀 **Getting Started**

1. **Authenticate**: Get your JWT token using `/auth/login`
2. **Explore Templates**: Check available workflow packages with `/api/v1/workflows/packages/templates`
3. **Execute Workflow**: Start with a simple workflow using `/api/v1/workflows/packages/execute`
4. **Monitor Progress**: Track execution with `/api/v1/workflows/packages/status/{execution_id}`
5. **Analyze Results**: Review performance with `/api/v1/analytics/dashboard/overview`

---

## 📞 **Support**

For API support and questions:
- **Documentation**: http://localhost:8000/docs
- **Status Page**: http://localhost:8000/health
- **Interactive API Explorer**: http://localhost:8000/docs#/

---

**PropertyPro AI AURA Integration** - Your Complete Workflow Automation Platform for Dubai Real Estate
