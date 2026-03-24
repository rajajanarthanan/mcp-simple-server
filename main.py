#!/usr/bin/env python3
"""Minimal MCP Server with FastMCP - Simple Working Solution"""

import os

import uvicorn

from app.mcp_app import mcp
import tools  # noqa: F401 — registers all @mcp.tool() decorators

def main():
    """Run the server"""
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))

    print("Starting MCP server...")
    print(f"HOST: {host}")
    print(f"PORT: {port}")
    print("MCP endpoint will be available at the server URL + /mcp")

    # For production (Railway), use direct uvicorn control
    if host == "0.0.0.0" or os.getenv("RAILWAY_ENVIRONMENT"):
        print("🚀 PRODUCTION MODE: Using FastMCP's streamable_http_app directly")

        try:
            # Get the streamable HTTP app from FastMCP (it's a method, so call it)
            app = mcp.streamable_http_app()

            if app is None:
                raise AttributeError("streamable_http_app() returned None")

            print(f"✅ SUCCESS: Got streamable_http_app from FastMCP!")
            print(f"App type: {type(app)}")
            print(f"Running uvicorn on {host}:{port}")

            # Run with uvicorn directly - this WILL bind to 0.0.0.0
            uvicorn.run(app, host=host, port=port, log_level="info", access_log=True)

        except Exception as e:
            print(f"❌ Could not get streamable_http_app: {e}")
            print("🔄 Falling back to FastMCP default...")

            # Fallback to FastMCP (will still bind to 127.0.0.1 but at least it runs)
            mcp.run(transport="streamable-http")
    else:
        print("🏠 LOCAL DEVELOPMENT: Using FastMCP default")
        mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
