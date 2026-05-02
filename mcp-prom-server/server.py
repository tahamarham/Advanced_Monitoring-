import httpx
from mcp.server.fastmcp import FastMCP

# 1. Initialize the MCP Server
mcp = FastMCP("Prometheus-SRE-Gateway")

# The internal Docker URL for Prometheus
# 'prometheus' is the service name defined in your docker-compose.yml
PROMETHEUS_URL = "http://prometheus:9090/api/v1/query"

# 2. Define the Tool for the AI
@mcp.tool()
async def query_prometheus(query: str) -> str:
    """
    Executes a PromQL query against the local Prometheus instance.
    Use this tool to check container metrics like CPU, Memory, or uptime status.
    """
    # 3. Execute the HTTP request to Prometheus
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(PROMETHEUS_URL, params={"query": query})
            response.raise_for_status()
            
            # Return the raw JSON data back to the AI
            return response.text
            
        except Exception as e:
            return f"Error querying Prometheus: {str(e)}"

if __name__ == "__main__":
    # We removed 'transport="sse"' and 'port=8000'
    # Running it empty defaults to 'stdio', which is what 'docker exec' requires.
    mcp.run()