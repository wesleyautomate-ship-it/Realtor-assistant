"""
MCP (Model Context Protocol) Configuration for Laura AI Real Estate Assistant

This module configures the MCP server integration with FastAPI,
exposing key endpoints as MCP tools for AI model interaction.
"""

from fastapi_mcp import FastApiMCP
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class MCPConfig:
    """Configuration class for MCP server setup"""
    
    # MCP Server Configuration
    MCP_SERVER_NAME = "Laura AI Real Estate MCP Server"
    MCP_BASE_URL = "http://localhost:8003"
    MCP_MOUNT_PATH = "/mcp"
    
    # Endpoints to include as MCP tools
    INCLUDE_TAGS = [
        "properties",      # Property search and management
        "chat",           # Chat and conversation endpoints
        "ml-insights",    # ML insights and market analysis
        "contacts",       # Contact and lead management
        "documents",      # Document processing
        "reports",        # Report generation
        "market-data",    # Market data endpoints
        "analytics",      # Analytics and performance
        "nurturing",      # Lead nurturing
        "detection"       # Property detection
    ]
    
    # Endpoints to exclude from MCP tools
    EXCLUDE_TAGS = [
        "admin",          # Admin-only endpoints
        "internal",       # Internal system endpoints
        "health",         # Health check endpoints
        "auth",           # Authentication endpoints (handled separately)
        "monitoring",     # System monitoring
        "debug"           # Debug endpoints
    ]
    
    # Specific operations to include (by operation_id)
    INCLUDE_OPERATIONS = [
        "process_chat_message",
        "search_properties", 
        "get_market_analysis",
        "get_property_details",
        "create_lead",
        "update_lead_status",
        "generate_report",
        "analyze_document",
        "get_client_info",
        "predict_market_trends",
        "calculate_investment_roi",
        "detect_property_features",
        "schedule_follow_up",
        "get_agent_agenda"
    ]
    
    # Specific operations to exclude
    EXCLUDE_OPERATIONS = [
        "delete_user",
        "admin_reset_system",
        "internal_debug",
        "health_check"
    ]

def create_mcp_server(app) -> FastApiMCP:
    """
    Create and configure the MCP server for the FastAPI application
    
    Args:
        app: FastAPI application instance
        
    Returns:
        Configured FastApiMCP instance
    """
    try:
        logger.info("🔧 Initializing MCP server for Laura AI Real Estate Assistant...")
        
        # Create MCP server with configuration
        mcp = FastApiMCP(
            app=app,
            name=MCPConfig.MCP_SERVER_NAME,
            base_url=MCPConfig.MCP_BASE_URL,
            describe_all_responses=True,           # Include all response schemas
            describe_full_response_schema=True,    # Include full JSON schemas
            include_tags=MCPConfig.INCLUDE_TAGS,   # Include specific tags
            exclude_tags=MCPConfig.EXCLUDE_TAGS,   # Exclude specific tags
            include_operations=MCPConfig.INCLUDE_OPERATIONS,  # Include specific operations
            exclude_operations=MCPConfig.EXCLUDE_OPERATIONS   # Exclude specific operations
        )
        
        logger.info("✅ MCP server configured successfully")
        logger.info(f"📋 Included tags: {MCPConfig.INCLUDE_TAGS}")
        logger.info(f"🚫 Excluded tags: {MCPConfig.EXCLUDE_TAGS}")
        logger.info(f"📋 Included operations: {len(MCPConfig.INCLUDE_OPERATIONS)} operations")
        
        return mcp
        
    except Exception as e:
        logger.error(f"❌ Failed to create MCP server: {e}")
        raise

def mount_mcp_server(mcp: FastApiMCP) -> None:
    """
    Mount the MCP server to the FastAPI application
    
    Args:
        mcp: Configured FastApiMCP instance
    """
    try:
        logger.info(f"🔗 Mounting MCP server at {MCPConfig.MCP_MOUNT_PATH}")
        mcp.mount()
        logger.info("✅ MCP server mounted successfully")
        logger.info(f"🌐 MCP server available at: {MCPConfig.MCP_BASE_URL}{MCPConfig.MCP_MOUNT_PATH}")
        
    except Exception as e:
        logger.error(f"❌ Failed to mount MCP server: {e}")
        raise

def get_mcp_tools_info() -> dict:
    """
    Get information about available MCP tools
    
    Returns:
        Dictionary with MCP tools information
    """
    return {
        "server_name": MCPConfig.MCP_SERVER_NAME,
        "base_url": MCPConfig.MCP_BASE_URL,
        "mount_path": MCPConfig.MCP_MOUNT_PATH,
        "included_tags": MCPConfig.INCLUDE_TAGS,
        "excluded_tags": MCPConfig.EXCLUDE_TAGS,
        "included_operations": MCPConfig.INCLUDE_OPERATIONS,
        "excluded_operations": MCPConfig.EXCLUDE_OPERATIONS,
        "total_included_operations": len(MCPConfig.INCLUDE_OPERATIONS)
    }

# MCP Tool Descriptions for AI Models
MCP_TOOL_DESCRIPTIONS = {
    "process_chat_message": {
        "name": "Chat with Laura AI",
        "description": "Send a message to Laura AI for real estate assistance, property queries, market analysis, or general real estate advice",
        "category": "conversation"
    },
    "search_properties": {
        "name": "Search Properties",
        "description": "Search for properties in Dubai with specific criteria like location, price range, bedrooms, property type",
        "category": "property_search"
    },
    "get_market_analysis": {
        "name": "Get Market Analysis",
        "description": "Get comprehensive market analysis for specific areas, property types, or time periods in Dubai",
        "category": "market_analysis"
    },
    "get_property_details": {
        "name": "Get Property Details",
        "description": "Get detailed information about a specific property including features, pricing, and market data",
        "category": "property_info"
    },
    "create_lead": {
        "name": "Create New Lead",
        "description": "Create a new lead or client record with contact information and property preferences",
        "category": "lead_management"
    },
    "update_lead_status": {
        "name": "Update Lead Status",
        "description": "Update the status of an existing lead or client (e.g., from prospect to qualified)",
        "category": "lead_management"
    },
    "generate_report": {
        "name": "Generate Report",
        "description": "Generate various types of reports including market reports, client reports, or performance analytics",
        "category": "reporting"
    },
    "analyze_document": {
        "name": "Analyze Document",
        "description": "Analyze uploaded documents like property listings, contracts, or market data",
        "category": "document_processing"
    },
    "get_client_info": {
        "name": "Get Client Information",
        "description": "Retrieve comprehensive information about a client including history, preferences, and interactions",
        "category": "client_management"
    },
    "predict_market_trends": {
        "name": "Predict Market Trends",
        "description": "Get AI-powered predictions about market trends, property values, and investment opportunities",
        "category": "ml_insights"
    },
    "calculate_investment_roi": {
        "name": "Calculate Investment ROI",
        "description": "Calculate return on investment for property purchases including rental yields and appreciation",
        "category": "investment_analysis"
    },
    "detect_property_features": {
        "name": "Detect Property Features",
        "description": "Analyze property images or descriptions to detect and extract property features",
        "category": "property_analysis"
    },
    "schedule_follow_up": {
        "name": "Schedule Follow-up",
        "description": "Schedule follow-up tasks or appointments with clients or leads",
        "category": "task_management"
    },
    "get_agent_agenda": {
        "name": "Get Agent Agenda",
        "description": "Get the agent's daily agenda including tasks, appointments, and follow-ups",
        "category": "task_management"
    }
}



