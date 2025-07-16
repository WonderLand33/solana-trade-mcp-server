#!/usr/bin/env python3
"""
Main entry point for the Solana MCP Server.
"""

import sys
import asyncio
from solana_mcp_server import main

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)