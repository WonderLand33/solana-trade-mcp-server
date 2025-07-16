"""
Solana MCP Server Package

A Model Context Protocol server for Solana blockchain interactions.
"""

__version__ = "1.0.0"
__description__ = "MCP server for Solana blockchain operations"

from .solana_mcp_server import SolanaMCPServer, main

__all__ = ["SolanaMCPServer", "main"]