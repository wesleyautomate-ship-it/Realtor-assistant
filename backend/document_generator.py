#!/usr/bin/env python3
"""
Document Generator for Blueprint 2.0: Proactive AI Copilot
Handles HTML generation for web-based content delivery
"""

import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional
from sqlalchemy import create_engine, text
import uuid

logger = logging.getLogger(__name__)

class DocumentGenerator:
    """Handles generation of HTML documents for web-based content delivery"""
    
    def __init__(self, db_url: str, ai_model):
        self.db_url = db_url
        self.engine = create_engine(db_url)
        self.ai_model = ai_model
    
    def generate_cma_html(self, subject_property: dict, comparable_properties: list, agent_id: int) -> Dict[str, Any]:
        """Generate HTML CMA document with preview summary"""
        try:
            # Generate HTML content using AI
            html_content = self._generate_cma_html_content(subject_property, comparable_properties)
            
            # Generate preview summary
            preview_summary = self._generate_preview_summary(subject_property, comparable_properties)
            
            # Create document record
            document_id = self._save_document(
                document_type="cma",
                title=f"CMA Report: {subject_property.get('address', 'Property')}",
                content_html=html_content,
                preview_summary=preview_summary,
                agent_id=agent_id,
                metadata={
                    "subject_property": subject_property,
                    "comparable_count": len(comparable_properties),
                    "generated_at": datetime.now().isoformat()
                }
            )
            
            # Generate result URL
            result_url = f"/documents/view/{document_id}"
            
            # Update document with result URL
            self._update_document_url(document_id, result_url)
            
            return {
                "document_id": document_id,
                "result_url": result_url,
                "preview_summary": preview_summary,
                "title": f"CMA Report: {subject_property.get('address', 'Property')}"
            }
            
        except Exception as e:
            logger.error(f"Error generating CMA HTML: {e}")
            raise
    
    def generate_brochure_html(self, property_details: dict, agent_id: int) -> Dict[str, Any]:
        """Generate HTML property brochure with preview summary"""
        try:
            # Generate HTML content using AI
            html_content = self._generate_brochure_html_content(property_details)
            
            # Generate preview summary
            preview_summary = self._generate_brochure_preview_summary(property_details)
            
            # Create document record
            document_id = self._save_document(
                document_type="brochure",
                title=f"Property Brochure: {property_details.get('address', 'Property')}",
                content_html=html_content,
                preview_summary=preview_summary,
                agent_id=agent_id,
                metadata={
                    "property_details": property_details,
                    "generated_at": datetime.now().isoformat()
                }
            )
            
            # Generate result URL
            result_url = f"/documents/view/{document_id}"
            
            # Update document with result URL
            self._update_document_url(document_id, result_url)
            
            return {
                "document_id": document_id,
                "result_url": result_url,
                "preview_summary": preview_summary,
                "title": f"Property Brochure: {property_details.get('address', 'Property')}"
            }
            
        except Exception as e:
            logger.error(f"Error generating brochure HTML: {e}")
            raise
    
    def _generate_cma_html_content(self, subject_property: dict, comparable_properties: list) -> str:
        """Generate HTML content for CMA report"""
        try:
            # Create AI prompt for HTML generation
            prompt = f"""
You are a professional real estate analyst. Create a comprehensive HTML CMA report.

**Subject Property:**
{json.dumps(subject_property, indent=2)}

**Comparable Properties:**
{json.dumps(comparable_properties, indent=2)}

**Requirements:**
1. Generate complete HTML document with proper structure
2. Include CSS styling for professional appearance
3. Use a clean, modern design
4. Include sections: Executive Summary, Property Analysis, Market Comparison, Valuation, Recommendations
5. Make it mobile-responsive
6. Use professional fonts and colors
7. Include data tables for comparable properties
8. Add charts/graphs placeholders for visual data

**HTML Structure:**
- Use semantic HTML5 elements
- Include proper meta tags
- Add responsive CSS
- Use professional color scheme (blues, grays, whites)
- Include company branding elements
- Make it print-friendly

Generate the complete HTML document:
"""
            
            # Generate content using AI model
            response = self.ai_model.generate_content(prompt)
            html_content = response.text
            
            # Ensure it's valid HTML
            if not html_content.strip().startswith('<'):
                html_content = self._wrap_in_html_template(html_content, "CMA Report")
            
            return html_content
            
        except Exception as e:
            logger.error(f"Error generating CMA HTML content: {e}")
            return self._get_default_cma_html(subject_property, comparable_properties)
    
    def _generate_brochure_html_content(self, property_details: dict) -> str:
        """Generate HTML content for property brochure"""
        try:
            # Create AI prompt for HTML generation
            prompt = f"""
You are a luxury real estate copywriter. Create a stunning HTML property brochure.

**Property Details:**
{json.dumps(property_details, indent=2)}

**Requirements:**
1. Generate complete HTML document with luxury design
2. Include modern CSS styling with animations
3. Use high-end, aspirational language
4. Include sections: Hero, Features, Location, Investment Highlights, Contact
5. Make it visually appealing with placeholder images
6. Use luxury color scheme (gold, black, white, deep blues)
7. Include call-to-action elements
8. Make it mobile-responsive

**HTML Structure:**
- Use modern HTML5 with CSS Grid/Flexbox
- Include smooth animations and transitions
- Use professional typography
- Add interactive elements
- Include social sharing buttons
- Make it print-friendly

Generate the complete HTML document:
"""
            
            # Generate content using AI model
            response = self.ai_model.generate_content(prompt)
            html_content = response.text
            
            # Ensure it's valid HTML
            if not html_content.strip().startswith('<'):
                html_content = self._wrap_in_html_template(html_content, "Property Brochure")
            
            return html_content
            
        except Exception as e:
            logger.error(f"Error generating brochure HTML content: {e}")
            return self._get_default_brochure_html(property_details)
    
    def _generate_preview_summary(self, subject_property: dict, comparable_properties: list) -> str:
        """Generate 1-2 sentence preview summary for CMA"""
        try:
            prompt = f"""
Generate a concise 1-2 sentence summary for a CMA report preview.

**Subject Property:** {subject_property.get('address', 'Property')}
**Property Type:** {subject_property.get('property_type', 'Unknown')}
**Bedrooms:** {subject_property.get('bedrooms', 'N/A')}
**Comparable Properties:** {len(comparable_properties)} found

Create a brief, professional summary that highlights:
- Property location and type
- Key valuation insights
- Market positioning

Summary (1-2 sentences):
"""
            
            response = self.ai_model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            logger.error(f"Error generating preview summary: {e}")
            return f"CMA Report for {subject_property.get('address', 'Property')} with {len(comparable_properties)} comparable properties analyzed."
    
    def _generate_brochure_preview_summary(self, property_details: dict) -> str:
        """Generate 1-2 sentence preview summary for brochure"""
        try:
            prompt = f"""
Generate a concise 1-2 sentence summary for a property brochure preview.

**Property:** {property_details.get('address', 'Property')}
**Type:** {property_details.get('property_type', 'Unknown')}
**Bedrooms:** {property_details.get('bedrooms', 'N/A')}
**Price:** {property_details.get('price', 'N/A')}

Create a brief, attractive summary that highlights:
- Property highlights
- Key selling points
- Location benefits

Summary (1-2 sentences):
"""
            
            response = self.ai_model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            logger.error(f"Error generating brochure preview summary: {e}")
            return f"Luxury {property_details.get('property_type', 'property')} in {property_details.get('address', 'prime location')}."
    
    def _save_document(self, document_type: str, title: str, content_html: str, 
                      preview_summary: str, agent_id: int, metadata: dict) -> int:
        """Save document to database"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                    INSERT INTO generated_documents 
                    (document_type, title, content_html, preview_summary, agent_id, metadata, created_at, updated_at)
                    VALUES (:document_type, :title, :content_html, :preview_summary, :agent_id, :metadata, NOW(), NOW())
                    RETURNING id
                """), {
                    'document_type': document_type,
                    'title': title,
                    'content_html': content_html,
                    'preview_summary': preview_summary,
                    'agent_id': agent_id,
                    'metadata': json.dumps(metadata)
                })
                
                document_id = result.fetchone()[0]
                conn.commit()
                
                logger.info(f"Saved document {document_id} of type {document_type}")
                return document_id
                
        except Exception as e:
            logger.error(f"Error saving document: {e}")
            raise
    
    def _update_document_url(self, document_id: int, result_url: str):
        """Update document with result URL"""
        try:
            with self.engine.connect() as conn:
                conn.execute(text("""
                    UPDATE generated_documents 
                    SET result_url = :result_url, updated_at = NOW()
                    WHERE id = :document_id
                """), {
                    'result_url': result_url,
                    'document_id': document_id
                })
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error updating document URL: {e}")
    
    def get_document(self, document_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve document by ID"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT id, document_type, title, content_html, preview_summary, 
                           result_url, agent_id, metadata, created_at
                    FROM generated_documents 
                    WHERE id = :document_id
                """), {'document_id': document_id})
                
                row = result.fetchone()
                if row:
                    return {
                        'id': row.id,
                        'document_type': row.document_type,
                        'title': row.title,
                        'content_html': row.content_html,
                        'preview_summary': row.preview_summary,
                        'result_url': row.result_url,
                        'agent_id': row.agent_id,
                        'metadata': json.loads(row.metadata) if row.metadata else {},
                        'created_at': row.created_at.isoformat() if row.created_at else None
                    }
                return None
                
        except Exception as e:
            logger.error(f"Error retrieving document: {e}")
            return None
    
    def _wrap_in_html_template(self, content: str, title: str) -> str:
        """Wrap content in basic HTML template"""
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; line-height: 1.6; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ background: #2c3e50; color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; }}
        .footer {{ background: #34495e; color: white; padding: 20px; text-align: center; margin-top: 40px; }}
        @media print {{ .header, .footer {{ display: none; }} }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title}</h1>
            <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        </div>
        <div class="content">
            {content}
        </div>
        <div class="footer">
            <p>© 2024 Dubai Real Estate RAG System</p>
        </div>
    </div>
</body>
</html>
"""
    
    def _get_default_cma_html(self, subject_property: dict, comparable_properties: list) -> str:
        """Get default CMA HTML template"""
        return self._wrap_in_html_template(f"""
            <h2>Comparative Market Analysis</h2>
            <h3>Subject Property</h3>
            <p><strong>Address:</strong> {subject_property.get('address', 'N/A')}</p>
            <p><strong>Property Type:</strong> {subject_property.get('property_type', 'N/A')}</p>
            <p><strong>Bedrooms:</strong> {subject_property.get('bedrooms', 'N/A')}</p>
            <p><strong>Bathrooms:</strong> {subject_property.get('bathrooms', 'N/A')}</p>
            
            <h3>Comparable Properties ({len(comparable_properties)} found)</h3>
            <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                <thead>
                    <tr style="background: #f8f9fa;">
                        <th style="border: 1px solid #ddd; padding: 12px;">Address</th>
                        <th style="border: 1px solid #ddd; padding: 12px;">Price</th>
                        <th style="border: 1px solid #ddd; padding: 12px;">Bedrooms</th>
                        <th style="border: 1px solid #ddd; padding: 12px;">Price/Sqft</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join([f'''
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 12px;">{comp.get('address', 'N/A')}</td>
                        <td style="border: 1px solid #ddd; padding: 12px;">AED {comp.get('price', 0):,.0f}</td>
                        <td style="border: 1px solid #ddd; padding: 12px;">{comp.get('bedrooms', 'N/A')}</td>
                        <td style="border: 1px solid #ddd; padding: 12px;">AED {comp.get('price_per_sqft', 0):,.0f}</td>
                    </tr>
                    ''' for comp in comparable_properties])}
                </tbody>
            </table>
            
            <h3>Market Analysis</h3>
            <p>This CMA report provides a comprehensive analysis of the subject property compared to recent market transactions in the area.</p>
            
            <h3>Recommendations</h3>
            <p>Based on the comparable properties analysis, we recommend a price range that reflects current market conditions and property characteristics.</p>
        """, "CMA Report")
    
    def _get_default_brochure_html(self, property_details: dict) -> str:
        """Get default brochure HTML template"""
        return self._wrap_in_html_template(f"""
            <h2>Property Brochure</h2>
            <h3>{property_details.get('address', 'Property')}</h3>
            
            <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h4>Property Highlights</h4>
                <ul>
                    <li><strong>Type:</strong> {property_details.get('property_type', 'N/A')}</li>
                    <li><strong>Bedrooms:</strong> {property_details.get('bedrooms', 'N/A')}</li>
                    <li><strong>Bathrooms:</strong> {property_details.get('bathrooms', 'N/A')}</li>
                    <li><strong>Size:</strong> {property_details.get('size_sqft', 'N/A')} sq ft</li>
                    <li><strong>Price:</strong> AED {property_details.get('price', 0):,.0f}</li>
                </ul>
            </div>
            
            <h3>Description</h3>
            <p>{property_details.get('description', 'This exceptional property offers luxury living in a prime location.')}</p>
            
            <h3>Location</h3>
            <p>Located in the prestigious {property_details.get('address', 'area')}, this property offers easy access to major amenities and transportation.</p>
            
            <h3>Investment Potential</h3>
            <p>This property represents an excellent investment opportunity with strong rental yield potential and capital appreciation prospects.</p>
            
            <div style="background: #e8f5e8; padding: 20px; border-radius: 8px; margin: 20px 0; text-align: center;">
                <h3>Contact Us</h3>
                <p>For more information or to schedule a viewing, please contact our team.</p>
                <p><strong>Phone:</strong> +971 4 XXX XXXX</p>
                <p><strong>Email:</strong> info@dubai-estate.com</p>
            </div>
        """, "Property Brochure")
