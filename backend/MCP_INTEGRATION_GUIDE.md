# MCP (Model Context Protocol) Integration Guide

## Overview

This guide explains the MCP integration implemented in the Laura AI Real Estate Assistant backend. The MCP server exposes FastAPI endpoints as tools that AI models can directly call, enabling more dynamic and context-aware interactions.

## What is MCP?

Model Context Protocol (MCP) is a standard that allows AI models to interact with external tools and services. It provides a structured way for AI models to:

- Discover available tools
- Call tools with parameters
- Receive structured responses
- Maintain context across tool calls

## Implementation Details

### Files Added/Modified

1. **`mcp_config.py`** - MCP server configuration and setup
2. **`main.py`** - Modified to include MCP server initialization
3. **`requirements.txt`** - Added `fastapi-mcp>=0.3.0` dependency
4. **`test_mcp_integration.py`** - Test script for MCP functionality
5. **Router files** - Added `operation_id` to key endpoints

### MCP Server Configuration

The MCP server is configured with the following settings:

```python
# Server Configuration
MCP_SERVER_NAME = "Laura AI Real Estate MCP Server"
MCP_BASE_URL = "http://localhost:8003"
MCP_MOUNT_PATH = "/mcp"

# Included Tags (endpoints to expose as MCP tools)
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

# Excluded Tags (endpoints NOT to expose)
EXCLUDE_TAGS = [
    "admin",          # Admin-only endpoints
    "internal",       # Internal system endpoints
    "health",         # Health check endpoints
    "auth",           # Authentication endpoints
    "monitoring",     # System monitoring
    "debug"           # Debug endpoints
]
```

## Available MCP Tools

The following tools are exposed to AI models:

### 1. Chat Tools
- **`process_chat_message`** - Send messages to Laura AI for real estate assistance

### 2. Property Tools
- **`search_properties`** - Search for properties with specific criteria
- **`get_property_details`** - Get detailed property information

### 3. Market Analysis Tools
- **`get_market_analysis`** - Get comprehensive market analysis
- **`predict_market_trends`** - Get AI-powered market predictions

### 4. Client Management Tools
- **`create_lead`** - Create new lead/client records
- **`update_lead_status`** - Update lead status and information
- **`get_client_info`** - Retrieve client information

### 5. Document Processing Tools
- **`analyze_document`** - Analyze uploaded documents
- **`generate_report`** - Generate various types of reports

### 6. Investment Analysis Tools
- **`calculate_investment_roi`** - Calculate ROI for property investments

### 7. Task Management Tools
- **`schedule_follow_up`** - Schedule follow-up tasks
- **`get_agent_agenda`** - Get agent's daily agenda

## Installation and Setup

### 1. Install Dependencies

```bash
# Install fastapi-mcp
pip install fastapi-mcp>=0.3.0

# Or add to requirements.txt and install
pip install -r requirements.txt
```

### 2. Start the Backend Server

```bash
# Start the FastAPI server
python main.py

# Or using uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8003
```

### 3. Verify MCP Integration

```bash
# Run the test script
python test_mcp_integration.py

# Or test manually
curl http://localhost:8003/mcp/health
curl http://localhost:8003/mcp/info
```

## MCP Endpoints

### Health Check
- **GET** `/mcp/health` - Check MCP server health

### Information
- **GET** `/mcp/info` - Get MCP server information and available tools

### MCP Server
- **GET** `/mcp` - Main MCP server endpoint (for AI model interaction)

## Usage Examples

### 1. Testing MCP Server Health

```bash
curl http://localhost:8003/mcp/health
```

Response:
```json
{
  "status": "healthy",
  "mcp_available": true,
  "server_name": "Laura AI Real Estate MCP Server",
  "endpoint": "http://localhost:8003/mcp",
  "timestamp": "2024-12-01T10:00:00Z"
}
```

### 2. Getting MCP Server Information

```bash
curl http://localhost:8003/mcp/info
```

Response:
```json
{
  "status": "available",
  "server_name": "Laura AI Real Estate MCP Server",
  "base_url": "http://localhost:8003",
  "mount_path": "/mcp",
  "mcp_endpoint": "http://localhost:8003/mcp",
  "included_tags": ["properties", "chat", "ml-insights", ...],
  "total_tools": 14,
  "description": "Laura AI Real Estate Assistant MCP Server"
}
```

### 3. AI Model Integration

AI models can now call your backend functions directly:

```python
# Example: AI model calling property search
result = mcp_client.call_tool(
    tool_name="search_properties",
    parameters={
        "location": "Dubai Marina",
        "price_min": 1000000,
        "price_max": 3000000,
        "bedrooms": 2
    }
)

# Example: AI model calling market analysis
analysis = mcp_client.call_tool(
    tool_name="get_market_analysis",
    parameters={
        "area": "Downtown Dubai",
        "property_type": "apartment",
        "timeframe": "6_months"
    }
)
```

## Benefits of MCP Integration

### 1. Enhanced AI Capabilities
- AI models can directly call backend functions
- Structured tool calling with proper parameters
- Better context management across interactions

### 2. Improved User Experience
- More accurate and contextual responses
- Ability to perform complex multi-step operations
- Real-time data access for AI responses

### 3. Scalable Architecture
- Easy to add new tools as the system grows
- Maintains existing API structure
- No need to rewrite existing services

### 4. Better Integration
- AI models get better context about available operations
- Structured responses improve AI understanding
- Enables more sophisticated AI workflows

## Troubleshooting

### Common Issues

1. **MCP Server Not Starting**
   - Check if `fastapi-mcp` is installed
   - Verify Python version compatibility
   - Check for import errors in logs

2. **Endpoints Not Exposed**
   - Verify `operation_id` is set on endpoints
   - Check if endpoints have correct tags
   - Ensure endpoints are not in excluded tags

3. **Authentication Issues**
   - MCP inherits FastAPI authentication
   - Ensure proper authentication headers
   - Check user permissions for endpoints

### Debug Commands

```bash
# Check MCP server status
curl http://localhost:8003/mcp/health

# Get detailed MCP information
curl http://localhost:8003/mcp/info

# Test specific endpoint
curl -X POST http://localhost:8003/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "session_id": "test"}'

# Run integration tests
python test_mcp_integration.py
```

## Future Enhancements

### Planned Features

1. **Advanced Tool Descriptions**
   - Enhanced tool descriptions for AI models
   - Parameter validation and examples
   - Response schema documentation

2. **Tool Composition**
   - Ability to chain multiple tool calls
   - Workflow automation
   - Complex multi-step operations

3. **Performance Optimization**
   - Tool call caching
   - Batch operations
   - Async tool execution

4. **Monitoring and Analytics**
   - Tool usage analytics
   - Performance metrics
   - Error tracking and reporting

## Security Considerations

### Authentication
- MCP inherits FastAPI authentication mechanisms
- All tool calls require proper authentication
- User permissions are enforced per endpoint

### Authorization
- Role-based access control applies to MCP tools
- Admin-only tools are excluded from MCP exposure
- Sensitive operations require appropriate permissions

### Rate Limiting
- Existing rate limiting applies to MCP tool calls
- Prevents abuse of AI-triggered operations
- Maintains system stability

## Conclusion

The MCP integration transforms your FastAPI backend into an AI-native service, enabling sophisticated interactions between AI models and your real estate system. This provides a foundation for building more intelligent and context-aware AI applications.

For questions or issues, refer to the test script (`test_mcp_integration.py`) or check the server logs for detailed error information.



