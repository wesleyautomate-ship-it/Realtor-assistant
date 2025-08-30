# Content Generation Guide

## Overview

The `ai_manager.py` file now includes comprehensive content generation capabilities powered by specialized AI prompts. This system provides six distinct content types, each with its own AI persona and specialized prompt structure.

## 🎯 Content Types Available

### 1. Daily Agent Briefing
**AI Persona:** MarketPulse AI - Elite Real Estate Analyst  
**Purpose:** Generate personalized morning briefings for real estate agents

**Function:** `generate_daily_briefing(agent_name, market_summary, new_listings, new_leads)`

**Input Parameters:**
- `agent_name` (str): Name of the agent
- `market_summary` (dict): Market trend data
- `new_listings` (list): New property listings
- `new_leads` (list): New client leads

**Output Structure:**
- 📈 Market Snapshot
- 🔑 New Key Listings  
- 👤 New Client Opportunities
- ✅ Top 3 Priorities Today

### 2. Social Media Posts
**AI Persona:** RealtyScribe AI - Creative Social Media Marketer  
**Purpose:** Generate platform-specific social media content

**Function:** `generate_social_media_post(platform, topic, key_points, audience, call_to_action)`

**Input Parameters:**
- `platform` (str): Social media platform (Instagram, LinkedIn, etc.)
- `topic` (str): Content topic
- `key_points` (list): Key information points
- `audience` (str): Target audience
- `call_to_action` (str): Desired action

**Features:**
- Platform-specific tone adjustment
- Trending hashtag inclusion
- Emoji optimization
- Hook and CTA integration

### 3. Follow-up Emails
**AI Persona:** AgentAssist AI - Professional Email Assistant  
**Purpose:** Draft personalized client follow-up emails

**Function:** `draft_follow_up_email(client_name, client_context, email_goal, listings_to_mention)`

**Input Parameters:**
- `client_name` (str): Client's name
- `client_context` (str): Previous interaction context
- `email_goal` (str): Purpose of the email
- `listings_to_mention` (list): Relevant properties to mention

**Output Structure:**
- Subject line generation
- Personalized greeting
- Context-aware body content
- Clear next steps
- Professional signature

### 4. Market Reports
**AI Persona:** Dubai Data Insights - Chief Market Analyst  
**Purpose:** Generate formal market analysis reports

**Function:** `generate_market_report(neighborhood, property_type, time_period, market_data)`

**Input Parameters:**
- `neighborhood` (str): Target area
- `property_type` (str): Property category
- `time_period` (str): Analysis timeframe
- `market_data` (dict): Market statistics

**Report Structure:**
1. Executive Summary
2. Key Performance Metrics
3. Market Trends Analysis
4. Investment Outlook
5. Disclaimer

### 5. Property Brochures
**AI Persona:** LuxeNarratives - Luxury Real Estate Copywriter  
**Purpose:** Create compelling property marketing materials

**Function:** `build_property_brochure(property_details)`

**Input Parameters:**
- `property_details` (dict): Property information

**Content Structure:**
1. Captivating Headline
2. Evocative Opening Statement
3. Key Features (benefit-focused)
4. In-Depth Description
5. Call to Action

### 6. Comparative Market Analysis (CMA)
**AI Persona:** RERA-Certified Property Valuator  
**Purpose:** Generate professional property valuation reports

**Function:** `generate_cma_content(subject_property, comparable_properties)`

**Input Parameters:**
- `subject_property` (dict): Property being analyzed
- `comparable_properties` (list): Comparable sales data

**Analysis Structure:**
1. Introduction
2. Subject Property Overview
3. Comparable Sales Analysis
4. Valuation Rationale & Adjustments
5. Estimated Market Value Range

## 🚀 Usage Examples

### Basic Usage

```python
from ai_manager import AIEnhancementManager

# Initialize with your AI model
ai_manager = AIEnhancementManager(db_url, model)

# Generate daily briefing
briefing = ai_manager.generate_daily_briefing(
    agent_name="Alex Smith",
    market_summary={
        'trend': 'Bullish',
        'price_change_pct': 2.5,
        'hotspot_area': 'Dubai Marina'
    },
    new_listings=[...],
    new_leads=[...]
)

# Generate social media post
social_post = ai_manager.generate_social_media_post(
    platform="Instagram",
    topic="New Luxury Villa",
    key_points=["5BR", "Private beach", "AED 12M"],
    audience="High-net-worth investors",
    call_to_action="Schedule viewing"
)
```

### Universal Content Generator

```python
# Use the universal function for any content type
content = ai_manager.generate_content_by_type(
    "daily_briefing",
    agent_name="Agent Name",
    market_summary=market_data,
    new_listings=listing_data,
    new_leads=lead_data
)

# Get available content types
available_types = ai_manager.get_available_content_types()
```

## 🎨 AI Personas & Specialization

Each content type uses a specialized AI persona with unique characteristics:

| Content Type | AI Persona | Specialization | Tone |
|--------------|------------|----------------|------|
| Daily Briefing | MarketPulse AI | Real Estate Analytics | Professional, Data-driven |
| Social Media | RealtyScribe AI | Social Media Marketing | Engaging, Platform-optimized |
| Follow-up Email | AgentAssist AI | Client Communication | Warm, Professional |
| Market Report | Dubai Data Insights | Market Analysis | Formal, Analytical |
| Property Brochure | LuxeNarratives | Luxury Copywriting | Aspirational, Sophisticated |
| CMA | RERA Valuator | Property Valuation | Objective, Data-driven |

## 📋 Input Data Requirements

### Market Summary (for Daily Briefing)
```python
market_summary = {
    'trend': 'Bullish/Bearish/Neutral',
    'price_change_pct': 2.5,  # Percentage change
    'hotspot_area': 'Dubai Marina'  # Trending area
}
```

### Property Details (for Brochures)
```python
property_details = {
    'type': 'Luxury Apartment',
    'address': 'Marina Gate 1, Dubai Marina',
    'price_aed': 3500000,
    'bedrooms': 3,
    'bathrooms': 3,
    'size_sqft': 2200,
    'features': 'Sea view, private balcony, gym access'
}
```

### Market Data (for Reports)
```python
market_data = {
    'avg_price_aed': 2500000,
    'price_change_percentage': 15.5,
    'sales_volume': 1250,
    'rental_yield': 6.8
}
```

## 🔧 Integration with Existing Systems

The content generation system integrates seamlessly with:

- **Database Systems:** Fetches real data for content generation
- **AI Models:** Uses Google Gemini or other AI models
- **Error Handling:** Comprehensive error handling and logging
- **Caching:** Conversation memory and response caching

## 🧪 Testing

Run the test script to verify functionality:

```bash
cd backend
python test_content_generation.py
```

This will test all content generation functions with sample data.

## 📈 Performance Considerations

- **Response Time:** AI model response time varies by content complexity
- **Token Usage:** Different content types use varying token amounts
- **Caching:** Implement caching for frequently generated content
- **Rate Limiting:** Consider API rate limits for AI model calls

## 🔮 Future Enhancements

Planned improvements include:

- **Template Customization:** Allow custom templates per agent
- **Brand Integration:** Automatic branding and logo insertion
- **Multi-language Support:** Arabic and other language support
- **Content Scheduling:** Automated content scheduling
- **Performance Analytics:** Track content effectiveness

## 🛠️ Troubleshooting

### Common Issues

1. **AI Model Errors:** Check model availability and API keys
2. **Data Format Issues:** Ensure input data matches expected format
3. **Memory Issues:** Clear conversation cache if needed
4. **Database Connection:** Verify database connectivity

### Error Handling

All functions include comprehensive error handling and return meaningful error messages when content generation fails.

## 📞 Support

For issues or questions about content generation:

1. Check the test script for usage examples
2. Review input data format requirements
3. Verify AI model configuration
4. Check logs for detailed error information
