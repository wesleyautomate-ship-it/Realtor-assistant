"""
Content Management Service for Laura AI Real Estate Assistant

This service manages AI-generated content, templates, approvals, and publishing
as a separate system from the main application.
"""

import json
import logging
import uuid
from typing import Dict, Any, Optional, List
from datetime import datetime
import google.generativeai as genai
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

class ContentManagementService:
    """Content management service for AI-generated real estate content"""
    
    def __init__(self, database_url: str, google_api_key: str):
        # Use SQLite for testing if PostgreSQL is not available
        if 'postgresql' in database_url and 'localhost' in database_url:
            # Check if we can connect to PostgreSQL, fallback to SQLite
            try:
                test_engine = create_engine(database_url)
                with test_engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                self.database_url = database_url
            except:
                print("⚠️ PostgreSQL not available, using SQLite for testing")
                self.database_url = 'sqlite:///voice_ai_test.db'
        else:
            self.database_url = database_url
            
        self.google_api_key = google_api_key
        
        # Initialize Google Gemini for content generation
        genai.configure(api_key=google_api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
        # Database connection
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        # Content templates configuration
        self.templates = {
            'cma': self._generate_cma_content,
            'just_listed': self._generate_just_listed_content,
            'just_sold': self._generate_just_sold_content,
            'open_house': self._generate_open_house_content,
            'newsletter': self._generate_newsletter_content,
            'investor_deck': self._generate_investor_deck_content,
            'brochure': self._generate_brochure_content,
            'social_banner': self._generate_social_banner_content,
            'story_content': self._generate_story_content
        }
    
    async def generate_content(self, template_type: str, property_data: Dict[str, Any], 
                             user_preferences: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """
        Generate content using specified template
        
        Args:
            template_type: Type of content to generate
            property_data: Property information
            user_preferences: User's preferences and settings
            user_id: User ID for tracking
            
        Returns:
            Generated content data
        """
        try:
            if template_type not in self.templates:
                raise ValueError(f"Unknown template type: {template_type}")
            
            # Get template configuration
            template_config = await self._get_template_config(template_type)
            
            # Generate content using AI
            generator = self.templates[template_type]
            content_data = await generator(property_data, user_preferences, template_config)
            
            # Store generated content
            content_id = await self._store_generated_content(
                template_type, content_data, property_data, user_preferences, user_id
            )
            
            return {
                'content_id': content_id,
                'template_type': template_type,
                'content_data': content_data,
                'status': 'generated',
                'approval_status': 'pending',
                'created_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating content: {e}")
            raise
    
    async def _get_template_config(self, template_type: str) -> Dict[str, Any]:
        """
        Get template configuration from database
        """
        try:
            with self.SessionLocal() as session:
                sql = """
                SELECT template_prompt, template_config
                FROM content_templates
                WHERE template_type = :template_type AND is_active = true
                """
                
                result = session.execute(text(sql), {'template_type': template_type}).fetchone()
                
                if result:
                    return {
                        'prompt': result.template_prompt,
                        'config': json.loads(result.template_config) if result.template_config else {}
                    }
                else:
                    # Return default configuration
                    return {
                        'prompt': f"Generate {template_type} content for the given property",
                        'config': {}
                    }
                    
        except Exception as e:
            logger.error(f"Error getting template config: {e}")
            return {'prompt': '', 'config': {}}
    
    async def _generate_cma_content(self, property_data: Dict[str, Any], 
                                  user_preferences: Dict[str, Any], 
                                  template_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate Comparative Market Analysis content
        """
        prompt = f"""
        Generate a comprehensive Comparative Market Analysis (CMA) for the following property:
        
        Property Details:
        - Address: {property_data.get('address', 'N/A')}
        - Price: {property_data.get('price', 'N/A')}
        - Bedrooms: {property_data.get('beds', 'N/A')}
        - Bathrooms: {property_data.get('baths', 'N/A')}
        - Square Feet: {property_data.get('sqft', 'N/A')}
        - Features: {', '.join(property_data.get('features', []))}
        
        User Preferences:
        - Specialty: {user_preferences.get('specialty', 'residential')}
        - Methodology: {user_preferences.get('methodology', 'standard')}
        
        Please provide:
        1. Executive Summary
        2. Market Overview for the area
        3. Comparable Properties Analysis (3-5 properties)
        4. Two Pricing Strategies:
           - Aggressive Pricing Strategy
           - Standard Pricing Strategy
        5. Market Trends and Insights
        6. Investment Potential Analysis
        7. Recommendations
        
        Format as a professional CMA report suitable for client presentation.
        Include specific data points, market statistics, and actionable insights.
        """
        
        response = await self.model.generate_content_async(prompt)
        
        return {
            'title': f'CMA Analysis - {property_data.get("address", "Property")}',
            'content': response.text,
            'sections': {
                'executive_summary': 'Market analysis summary',
                'market_overview': 'Area market conditions',
                'comparable_analysis': 'Similar properties analysis',
                'pricing_strategies': 'Aggressive and standard pricing',
                'market_trends': 'Current market trends',
                'investment_analysis': 'ROI and investment potential',
                'recommendations': 'Strategic recommendations'
            },
            'metadata': {
                'property_data': property_data,
                'user_preferences': user_preferences,
                'generated_at': datetime.now().isoformat(),
                'template_type': 'cma'
            }
        }
    
    async def _generate_just_listed_content(self, property_data: Dict[str, Any], 
                                          user_preferences: Dict[str, Any], 
                                          template_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate Just Listed marketing content
        """
        prompt = f"""
        Create compelling "Just Listed" marketing content for:
        
        Property: {property_data.get('address', 'N/A')}
        Price: {property_data.get('price', 'N/A')}
        Details: {property_data.get('beds', 'N/A')} bed, {property_data.get('baths', 'N/A')} bath, {property_data.get('sqft', 'N/A')} sqft
        Features: {', '.join(property_data.get('features', []))}
        
        Generate:
        1. Property Description (150-200 words) - compelling and engaging
        2. Social Media Post (Instagram/Facebook) - with hashtags
        3. Email Announcement - professional and informative
        4. Key Selling Points - bullet points highlighting unique features
        5. Call-to-Action - clear next steps for potential buyers
        
        Style: Professional, engaging, highlight unique features
        Target: Potential buyers in the area
        Tone: Exciting but professional, emphasizing value and opportunity
        """
        
        response = await self.model.generate_content_async(prompt)
        
        return {
            'title': f'Just Listed - {property_data.get("address", "Property")}',
            'content': response.text,
            'sections': {
                'property_description': 'Main property description',
                'social_media_post': 'Instagram/Facebook post with hashtags',
                'email_announcement': 'Professional email content',
                'selling_points': 'Key features and benefits',
                'call_to_action': 'Clear next steps for buyers'
            },
            'metadata': {
                'property_data': property_data,
                'user_preferences': user_preferences,
                'generated_at': datetime.now().isoformat(),
                'template_type': 'just_listed'
            }
        }
    
    async def _generate_just_sold_content(self, property_data: Dict[str, Any], 
                                        user_preferences: Dict[str, Any], 
                                        template_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate Just Sold celebration content
        """
        prompt = f"""
        Create "Just Sold" celebration content for:
        
        Property: {property_data.get('address', 'N/A')}
        Sale Price: {property_data.get('price', 'N/A')}
        Details: {property_data.get('beds', 'N/A')} bed, {property_data.get('baths', 'N/A')} bath, {property_data.get('sqft', 'N/A')} sqft
        
        Generate:
        1. Success Announcement - celebrate the sale
        2. Social Media Post - with celebration hashtags
        3. Thank You Message - to the client
        4. Market Impact - how this sale affects the market
        5. Call-to-Action - for future clients
        
        Style: Celebratory, professional, confident
        Tone: Proud, successful, encouraging for future clients
        """
        
        response = await self.model.generate_content_async(prompt)
        
        return {
            'title': f'Just Sold - {property_data.get("address", "Property")}',
            'content': response.text,
            'sections': {
                'success_announcement': 'Sale celebration message',
                'social_media_post': 'Celebration post with hashtags',
                'thank_you_message': 'Client appreciation message',
                'market_impact': 'Market significance of the sale',
                'call_to_action': 'Encouragement for future clients'
            },
            'metadata': {
                'property_data': property_data,
                'user_preferences': user_preferences,
                'generated_at': datetime.now().isoformat(),
                'template_type': 'just_sold'
            }
        }
    
    async def _generate_open_house_content(self, property_data: Dict[str, Any], 
                                         user_preferences: Dict[str, Any], 
                                         template_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate Open House invitation content
        """
        prompt = f"""
        Create Open House invitation and promotional content for:
        
        Property: {property_data.get('address', 'N/A')}
        Price: {property_data.get('price', 'N/A')}
        Details: {property_data.get('beds', 'N/A')} bed, {property_data.get('baths', 'N/A')} bath, {property_data.get('sqft', 'N/A')} sqft
        Date: {property_data.get('open_house_date', 'TBD')}
        Time: {property_data.get('open_house_time', 'TBD')}
        
        Generate:
        1. Open House Invitation - formal invitation
        2. Social Media Announcement - with event details
        3. Email Invitation - to your network
        4. Property Highlights - key features to showcase
        5. Directions and Parking Info - practical details
        
        Style: Inviting, professional, creates excitement
        Tone: Welcoming, informative, creates urgency
        """
        
        response = await self.model.generate_content_async(prompt)
        
        return {
            'title': f'Open House - {property_data.get("address", "Property")}',
            'content': response.text,
            'sections': {
                'invitation': 'Formal open house invitation',
                'social_media_announcement': 'Event announcement post',
                'email_invitation': 'Network invitation email',
                'property_highlights': 'Key features to showcase',
                'logistics': 'Directions and parking information'
            },
            'metadata': {
                'property_data': property_data,
                'user_preferences': user_preferences,
                'generated_at': datetime.now().isoformat(),
                'template_type': 'open_house'
            }
        }
    
    async def _generate_newsletter_content(self, property_data: Dict[str, Any], 
                                         user_preferences: Dict[str, Any], 
                                         template_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate market newsletter content
        """
        prompt = f"""
        Create a market newsletter for real estate clients:
        
        Market Focus: {user_preferences.get('market_focus', 'General Market')}
        Specialty: {user_preferences.get('specialty', 'residential')}
        
        Generate:
        1. Market Overview - current market conditions
        2. Featured Properties - highlight new listings
        3. Market Statistics - key metrics and trends
        4. Investment Opportunities - market insights
        5. Client Success Stories - recent sales and achievements
        6. Upcoming Events - open houses, market updates
        
        Style: Professional, informative, engaging
        Tone: Expert, helpful, builds trust
        """
        
        response = await self.model.generate_content_async(prompt)
        
        return {
            'title': f'Market Newsletter - {datetime.now().strftime("%B %Y")}',
            'content': response.text,
            'sections': {
                'market_overview': 'Current market conditions',
                'featured_properties': 'New listings highlights',
                'market_statistics': 'Key metrics and trends',
                'investment_opportunities': 'Market insights',
                'success_stories': 'Recent achievements',
                'upcoming_events': 'Events and updates'
            },
            'metadata': {
                'property_data': property_data,
                'user_preferences': user_preferences,
                'generated_at': datetime.now().isoformat(),
                'template_type': 'newsletter'
            }
        }
    
    async def _generate_investor_deck_content(self, property_data: Dict[str, Any], 
                                           user_preferences: Dict[str, Any], 
                                           template_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate investment presentation deck content
        """
        prompt = f"""
        Create an investment presentation deck for:
        
        Property: {property_data.get('address', 'N/A')}
        Price: {property_data.get('price', 'N/A')}
        Details: {property_data.get('beds', 'N/A')} bed, {property_data.get('baths', 'N/A')} bath, {property_data.get('sqft', 'N/A')} sqft
        
        Generate:
        1. Executive Summary - investment overview
        2. Property Analysis - detailed property assessment
        3. Market Analysis - investment market conditions
        4. Financial Projections - ROI, cash flow, appreciation
        5. Risk Assessment - potential risks and mitigation
        6. Investment Recommendation - clear recommendation
        
        Style: Professional, data-driven, investor-focused
        Tone: Analytical, confident, persuasive
        """
        
        response = await self.model.generate_content_async(prompt)
        
        return {
            'title': f'Investment Analysis - {property_data.get("address", "Property")}',
            'content': response.text,
            'sections': {
                'executive_summary': 'Investment overview',
                'property_analysis': 'Detailed property assessment',
                'market_analysis': 'Investment market conditions',
                'financial_projections': 'ROI and cash flow analysis',
                'risk_assessment': 'Risks and mitigation strategies',
                'recommendation': 'Investment recommendation'
            },
            'metadata': {
                'property_data': property_data,
                'user_preferences': user_preferences,
                'generated_at': datetime.now().isoformat(),
                'template_type': 'investor_deck'
            }
        }
    
    async def _generate_brochure_content(self, property_data: Dict[str, Any], 
                                       user_preferences: Dict[str, Any], 
                                       template_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate property brochure content
        """
        prompt = f"""
        Create a property brochure for:
        
        Property: {property_data.get('address', 'N/A')}
        Price: {property_data.get('price', 'N/A')}
        Details: {property_data.get('beds', 'N/A')} bed, {property_data.get('baths', 'N/A')} bath, {property_data.get('sqft', 'N/A')} sqft
        Features: {', '.join(property_data.get('features', []))}
        
        Generate:
        1. Property Overview - compelling introduction
        2. Key Features - highlight unique selling points
        3. Room Descriptions - detailed room-by-room descriptions
        4. Neighborhood Highlights - area benefits and amenities
        5. Investment Potential - value proposition
        6. Contact Information - clear call-to-action
        
        Style: Elegant, detailed, visually appealing
        Tone: Luxurious, informative, creates desire
        """
        
        response = await self.model.generate_content_async(prompt)
        
        return {
            'title': f'Property Brochure - {property_data.get("address", "Property")}',
            'content': response.text,
            'sections': {
                'property_overview': 'Compelling introduction',
                'key_features': 'Unique selling points',
                'room_descriptions': 'Detailed room descriptions',
                'neighborhood_highlights': 'Area benefits and amenities',
                'investment_potential': 'Value proposition',
                'contact_information': 'Clear call-to-action'
            },
            'metadata': {
                'property_data': property_data,
                'user_preferences': user_preferences,
                'generated_at': datetime.now().isoformat(),
                'template_type': 'brochure'
            }
        }
    
    async def _generate_social_banner_content(self, property_data: Dict[str, Any], 
                                            user_preferences: Dict[str, Any], 
                                            template_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate social media banner content
        """
        prompt = f"""
        Create social media banner content for:
        
        Property: {property_data.get('address', 'N/A')}
        Price: {property_data.get('price', 'N/A')}
        Details: {property_data.get('beds', 'N/A')} bed, {property_data.get('baths', 'N/A')} bath, {property_data.get('sqft', 'N/A')} sqft
        
        Generate:
        1. Banner Headline - eye-catching title
        2. Key Selling Points - 3-4 bullet points
        3. Call-to-Action - clear next step
        4. Hashtags - relevant hashtags for social media
        5. Visual Suggestions - what images to use
        
        Style: Bold, attention-grabbing, social media optimized
        Tone: Exciting, urgent, creates FOMO
        """
        
        response = await self.model.generate_content_async(prompt)
        
        return {
            'title': f'Social Media Banner - {property_data.get("address", "Property")}',
            'content': response.text,
            'sections': {
                'banner_headline': 'Eye-catching title',
                'selling_points': 'Key property highlights',
                'call_to_action': 'Clear next step',
                'hashtags': 'Relevant social media hashtags',
                'visual_suggestions': 'Image recommendations'
            },
            'metadata': {
                'property_data': property_data,
                'user_preferences': user_preferences,
                'generated_at': datetime.now().isoformat(),
                'template_type': 'social_banner'
            }
        }
    
    async def _generate_story_content(self, property_data: Dict[str, Any], 
                                    user_preferences: Dict[str, Any], 
                                    template_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate social media story content
        """
        prompt = f"""
        Create social media story content for:
        
        Property: {property_data.get('address', 'N/A')}
        Price: {property_data.get('price', 'N/A')}
        Details: {property_data.get('beds', 'N/A')} bed, {property_data.get('baths', 'N/A')} bath, {property_data.get('sqft', 'N/A')} sqft
        
        Generate:
        1. Story Sequence - 5-7 story slides
        2. Slide 1: Property Introduction
        3. Slide 2: Key Features
        4. Slide 3: Price and Details
        5. Slide 4: Neighborhood Highlights
        6. Slide 5: Call-to-Action
        7. Visual Suggestions - what to show in each slide
        
        Style: Engaging, story-driven, mobile-optimized
        Tone: Personal, authentic, creates connection
        """
        
        response = await self.model.generate_content_async(prompt)
        
        return {
            'title': f'Social Media Stories - {property_data.get("address", "Property")}',
            'content': response.text,
            'sections': {
                'story_sequence': '5-7 story slides',
                'slide_1': 'Property introduction',
                'slide_2': 'Key features',
                'slide_3': 'Price and details',
                'slide_4': 'Neighborhood highlights',
                'slide_5': 'Call-to-action',
                'visual_suggestions': 'What to show in each slide'
            },
            'metadata': {
                'property_data': property_data,
                'user_preferences': user_preferences,
                'generated_at': datetime.now().isoformat(),
                'template_type': 'story_content'
            }
        }
    
    async def _store_generated_content(self, template_type: str, content_data: Dict[str, Any], 
                                     property_data: Dict[str, Any], user_preferences: Dict[str, Any], 
                                     user_id: str) -> str:
        """
        Store generated content in database
        """
        try:
            content_id = str(uuid.uuid4())
            
            with self.SessionLocal() as session:
                sql = """
                INSERT INTO generated_content (
                    id, user_id, template_type, content_data, 
                    property_data, user_preferences, approval_status, created_at
                ) VALUES (
                    :id, :user_id, :template_type, :content_data,
                    :property_data, :user_preferences, 'pending', NOW()
                )
                """
                
                session.execute(text(sql), {
                    'id': content_id,
                    'user_id': user_id,
                    'template_type': template_type,
                    'content_data': json.dumps(content_data),
                    'property_data': json.dumps(property_data),
                    'user_preferences': json.dumps(user_preferences)
                })
                
                session.commit()
                
            return content_id
            
        except Exception as e:
            logger.error(f"Error storing generated content: {e}")
            raise
    
    async def approve_content(self, content_id: str, user_id: str) -> Dict[str, Any]:
        """
        Approve generated content for publishing
        """
        try:
            with self.SessionLocal() as session:
                sql = """
                UPDATE generated_content 
                SET approval_status = 'approved', 
                    approved_by = :user_id,
                    approved_at = NOW(),
                    updated_at = NOW()
                WHERE id = :content_id
                """
                
                session.execute(text(sql), {
                    'content_id': content_id,
                    'user_id': user_id
                })
                
                session.commit()
                
            return {
                'content_id': content_id,
                'status': 'approved',
                'approved_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error approving content: {e}")
            raise
    
    async def get_pending_approvals(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Get pending content approvals for user
        """
        try:
            with self.SessionLocal() as session:
                sql = """
                SELECT gc.*, ct.template_name, ct.template_description
                FROM generated_content gc
                JOIN content_templates ct ON gc.template_type = ct.template_type
                WHERE gc.user_id = :user_id AND gc.approval_status = 'pending'
                ORDER BY gc.created_at DESC
                """
                
                results = session.execute(text(sql), {'user_id': user_id}).fetchall()
                
                return [
                    {
                        'content_id': row.id,
                        'template_type': row.template_type,
                        'template_name': row.template_name,
                        'content_data': json.loads(row.content_data),
                        'property_data': json.loads(row.property_data),
                        'created_at': row.created_at.isoformat()
                    }
                    for row in results
                ]
                
        except Exception as e:
            logger.error(f"Error getting pending approvals: {e}")
            return []
