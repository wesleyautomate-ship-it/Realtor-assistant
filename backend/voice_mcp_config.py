"""
Voice-First MCP Configuration for Laura AI Real Estate Assistant

This module configures a separate MCP server specifically for voice processing
and content generation, complementing the existing MCP infrastructure.
"""

from fastapi_mcp import FastApiMCP
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class VoiceMCPConfig:
    """Configuration class for Voice MCP server setup"""
    
    # Voice MCP Server Configuration
    VOICE_MCP_SERVER_NAME = "Laura AI Voice-First MCP Server"
    VOICE_MCP_BASE_URL = "http://localhost:8004"
    VOICE_MCP_MOUNT_PATH = "/voice-mcp"
    
    # Voice-specific endpoints to include as MCP tools
    VOICE_INCLUDE_TAGS = [
        "voice-processing",    # Voice transcription and processing
        "content-generation",  # AI content generation
        "template-management", # Template system
        "real-time-ai",       # Real-time AI responses
        "batch-processing"    # Batch AI processing
    ]
    
    # Endpoints to exclude from Voice MCP tools
    VOICE_EXCLUDE_TAGS = [
        "admin",              # Admin-only endpoints
        "internal",           # Internal system endpoints
        "health",             # Health check endpoints
        "auth",               # Authentication endpoints
        "monitoring",         # System monitoring
        "debug"               # Debug endpoints
    ]
    
    # Voice-specific operations to include
    VOICE_INCLUDE_OPERATIONS = [
        "process_voice_request",
        "transcribe_audio",
        "extract_voice_intent",
        "generate_content_template",
        "create_marketing_campaign",
        "generate_cma_analysis",
        "create_social_media_content",
        "generate_newsletter",
        "create_investor_deck",
        "generate_brochure",
        "create_open_house_content",
        "generate_just_listed_content",
        "generate_just_sold_content",
        "get_voice_request_status",
        "approve_generated_content",
        "publish_content"
    ]
    
    # Operations to exclude from Voice MCP
    VOICE_EXCLUDE_OPERATIONS = [
        "delete_user",
        "admin_reset_system",
        "internal_debug",
        "health_check"
    ]

def create_voice_mcp_server(app) -> FastApiMCP:
    """
    Create and configure the Voice MCP server for the FastAPI application
    
    Args:
        app: FastAPI application instance
        
    Returns:
        Configured FastApiMCP instance for voice processing
    """
    try:
        logger.info("🎤 Initializing Voice MCP server for Laura AI Real Estate Assistant...")
        
        # Create Voice MCP server with configuration
        voice_mcp = FastApiMCP(
            app=app,
            name=VoiceMCPConfig.VOICE_MCP_SERVER_NAME,
            base_url=VoiceMCPConfig.VOICE_MCP_BASE_URL,
            describe_all_responses=True,           # Include all response schemas
            describe_full_response_schema=True,    # Include full JSON schemas
            include_tags=VoiceMCPConfig.VOICE_INCLUDE_TAGS,   # Include voice-specific tags
            exclude_tags=VoiceMCPConfig.VOICE_EXCLUDE_TAGS,   # Exclude specific tags
            include_operations=VoiceMCPConfig.VOICE_INCLUDE_OPERATIONS,  # Include voice operations
            exclude_operations=VoiceMCPConfig.VOICE_EXCLUDE_OPERATIONS   # Exclude operations
        )
        
        logger.info("✅ Voice MCP server configured successfully")
        logger.info(f"🎤 Voice included tags: {VoiceMCPConfig.VOICE_INCLUDE_TAGS}")
        logger.info(f"🚫 Voice excluded tags: {VoiceMCPConfig.VOICE_EXCLUDE_TAGS}")
        logger.info(f"🎤 Voice included operations: {len(VoiceMCPConfig.VOICE_INCLUDE_OPERATIONS)} operations")
        
        return voice_mcp
        
    except Exception as e:
        logger.error(f"❌ Failed to create Voice MCP server: {e}")
        raise

def mount_voice_mcp_server(voice_mcp: FastApiMCP) -> None:
    """
    Mount the Voice MCP server to the FastAPI application
    
    Args:
        voice_mcp: Configured Voice FastApiMCP instance
    """
    try:
        logger.info(f"🔗 Mounting Voice MCP server at {VoiceMCPConfig.VOICE_MCP_MOUNT_PATH}")
        voice_mcp.mount()
        logger.info("✅ Voice MCP server mounted successfully")
        logger.info(f"🌐 Voice MCP server available at: {VoiceMCPConfig.VOICE_MCP_BASE_URL}{VoiceMCPConfig.VOICE_MCP_MOUNT_PATH}")
        
    except Exception as e:
        logger.error(f"❌ Failed to mount Voice MCP server: {e}")
        raise

def get_voice_mcp_tools_info() -> dict:
    """
    Get information about available Voice MCP tools
    
    Returns:
        Dictionary with Voice MCP tools information
    """
    return {
        "server_name": VoiceMCPConfig.VOICE_MCP_SERVER_NAME,
        "base_url": VoiceMCPConfig.VOICE_MCP_BASE_URL,
        "mount_path": VoiceMCPConfig.VOICE_MCP_MOUNT_PATH,
        "included_tags": VoiceMCPConfig.VOICE_INCLUDE_TAGS,
        "excluded_tags": VoiceMCPConfig.VOICE_EXCLUDE_TAGS,
        "included_operations": VoiceMCPConfig.VOICE_INCLUDE_OPERATIONS,
        "excluded_operations": VoiceMCPConfig.VOICE_EXCLUDE_OPERATIONS,
        "total_voice_operations": len(VoiceMCPConfig.VOICE_INCLUDE_OPERATIONS)
    }

# Voice MCP Tool Descriptions for AI Models
VOICE_MCP_TOOL_DESCRIPTIONS = {
    "process_voice_request": {
        "name": "Process Voice Request",
        "description": "Process voice input from real estate agents, extract intent, and route to appropriate AI handlers",
        "category": "voice_processing"
    },
    "transcribe_audio": {
        "name": "Transcribe Audio",
        "description": "Convert speech to text using advanced speech recognition for real estate terminology",
        "category": "voice_processing"
    },
    "extract_voice_intent": {
        "name": "Extract Voice Intent",
        "description": "Analyze voice transcript to understand agent's intent (content generation, task management, etc.)",
        "category": "voice_processing"
    },
    "generate_content_template": {
        "name": "Generate Content Template",
        "description": "Generate marketing content using predefined templates (CMA, listings, newsletters, etc.)",
        "category": "content_generation"
    },
    "create_marketing_campaign": {
        "name": "Create Marketing Campaign",
        "description": "Create comprehensive marketing campaigns for properties including social media, email, and print materials",
        "category": "content_generation"
    },
    "generate_cma_analysis": {
        "name": "Generate CMA Analysis",
        "description": "Generate Comparative Market Analysis with pricing strategies and market insights",
        "category": "content_generation"
    },
    "create_social_media_content": {
        "name": "Create Social Media Content",
        "description": "Generate social media posts, stories, and banners for property marketing",
        "category": "content_generation"
    },
    "generate_newsletter": {
        "name": "Generate Newsletter",
        "description": "Create market newsletters and client communications",
        "category": "content_generation"
    },
    "create_investor_deck": {
        "name": "Create Investor Deck",
        "description": "Generate investment presentations and property analysis decks",
        "category": "content_generation"
    },
    "generate_brochure": {
        "name": "Generate Brochure",
        "description": "Create property brochures and marketing materials",
        "category": "content_generation"
    },
    "create_open_house_content": {
        "name": "Create Open House Content",
        "description": "Generate open house invitations and promotional materials",
        "category": "content_generation"
    },
    "generate_just_listed_content": {
        "name": "Generate Just Listed Content",
        "description": "Create 'Just Listed' marketing content and announcements",
        "category": "content_generation"
    },
    "generate_just_sold_content": {
        "name": "Generate Just Sold Content",
        "description": "Create 'Just Sold' celebration content and success stories",
        "category": "content_generation"
    },
    "get_voice_request_status": {
        "name": "Get Voice Request Status",
        "description": "Check the status of voice processing requests and content generation",
        "category": "real_time_ai"
    },
    "approve_generated_content": {
        "name": "Approve Generated Content",
        "description": "Approve AI-generated content for publishing and distribution",
        "category": "content_management"
    },
    "publish_content": {
        "name": "Publish Content",
        "description": "Publish approved content to various channels (social media, email, etc.)",
        "category": "content_management"
    }
}
