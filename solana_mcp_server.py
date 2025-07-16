#!/usr/bin/env python3
"""
Solana MCP Server

A Model Context Protocol server that provides onchain tools for LLMs
to interact with the Solana blockchain network.
"""

import asyncio
import json
import logging
import os
from typing import Any, Dict, List, Optional, Sequence
from urllib.parse import urlparse

import httpx
from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    TextContent,
    Tool,
)
from pydantic import BaseModel
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment
from solana.rpc.types import TxOpts
from solders.keypair import Keypair
from solders.pubkey import Pubkey

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SolanaConfig:
    """Configuration for Solana connection and operations."""
    
    def __init__(self):
        self.rpc_url = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
        self.devnet_rpc_url = os.getenv("SOLANA_DEVNET_RPC_URL", "https://api.devnet.solana.com")
        self.private_key = os.getenv("SOLANA_PRIVATE_KEY")
        self.commitment = Commitment(os.getenv("DEFAULT_COMMITMENT", "confirmed"))
        self.network = os.getenv("DEFAULT_NETWORK", "mainnet")
        self.max_transaction_amount = float(os.getenv("MAX_TRANSACTION_AMOUNT", "1.0"))
        self.require_confirmation = os.getenv("REQUIRE_CONFIRMATION", "true").lower() == "true"

class SolanaMCPServer:
    """Main MCP server class for Solana blockchain interactions."""
    
    def __init__(self):
        self.config = SolanaConfig()
        self.client: Optional[AsyncClient] = None
        self.keypair: Optional[Keypair] = None
        self.server = Server("solana-mcp-server")
        
        # Register tool handlers
        self._register_tools()
    
    def _register_tools(self):
        """Register all available tools with the MCP server."""
        
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """List all available Solana tools."""
            return [
                Tool(
                    name="get_balance",
                    description="Get SOL balance for a Solana address",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "address": {
                                "type": "string",
                                "description": "Solana public key address"
                            }
                        },
                        "required": ["address"]
                    }
                ),
                Tool(
                    name="get_token_balance",
                    description="Get SPL token balance for an address",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "address": {
                                "type": "string",
                                "description": "Solana public key address"
                            },
                            "token_mint": {
                                "type": "string",
                                "description": "Token mint address"
                            }
                        },
                        "required": ["address", "token_mint"]
                    }
                ),
                Tool(
                    name="get_transaction",
                    description="Get details of a Solana transaction",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "signature": {
                                "type": "string",
                                "description": "Transaction signature"
                            }
                        },
                        "required": ["signature"]
                    }
                ),
                Tool(
                    name="get_token_price",
                    description="Get current price of a token",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "token_symbol": {
                                "type": "string",
                                "description": "Token symbol (e.g., SOL, USDC)"
                            }
                        },
                        "required": ["token_symbol"]
                    }
                ),
                Tool(
                    name="create_wallet",
                    description="Generate a new Solana wallet",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                Tool(
                    name="get_account_info",
                    description="Get detailed account information",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "address": {
                                "type": "string",
                                "description": "Solana public key address"
                            }
                        },
                        "required": ["address"]
                    }
                ),
                Tool(
                    name="swap_tokens",
                    description="Swap one SPL token for another using Jupiter Aggregator.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "input_mint": {
                                "type": "string",
                                "description": "The mint address of the token to swap from."
                            },
                            "output_mint": {
                                "type": "string",
                                "description": "The mint address of the token to swap to."
                            },
                            "amount": {
                                "type": "integer",
                                "description": "The amount of the input token to swap, in the smallest unit (e.g., lamports)."
                            },
                            "user_public_key": {
                                "type": "string",
                                "description": "The public key of the user's wallet performing the swap."
                            },
                            "slippage_bps": {
                                "type": "integer",
                                "description": "The slippage tolerance in basis points (e.g., 50 for 0.5%).",
                                "default": 50
                            }
                        },
                        "required": ["input_mint", "output_mint", "amount", "user_public_key"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """Handle tool calls."""
            try:
                if name == "get_balance":
                    return await self._get_balance(arguments)
                elif name == "get_token_balance":
                    return await self._get_token_balance(arguments)
                elif name == "get_transaction":
                    return await self._get_transaction(arguments)
                elif name == "get_token_price":
                    return await self._get_token_price(arguments)
                elif name == "create_wallet":
                    return await self._create_wallet(arguments)
                elif name == "get_account_info":
                    return await self._get_account_info(arguments)
                elif name == "swap_tokens":
                    return await self._swap_tokens(arguments)
                else:
                    return [TextContent(type="text", text=f"Unknown tool: {name}")]
            except Exception as e:
                logger.error(f"Error in tool {name}: {str(e)}")
                return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    async def _ensure_client(self):
        """Ensure Solana client is initialized."""
        if self.client is None:
            rpc_url = self.config.devnet_rpc_url if self.config.network == "devnet" else self.config.rpc_url
            self.client = AsyncClient(rpc_url, commitment=self.config.commitment)
    
    async def _ensure_keypair(self):
        """Ensure keypair is loaded from private key."""
        if self.keypair is None and self.config.private_key:
            try:
                # Assume private key is in base58 format
                import base58
                private_key_bytes = base58.b58decode(self.config.private_key)
                self.keypair = Keypair.from_bytes(private_key_bytes)
            except Exception as e:
                logger.error(f"Failed to load keypair: {e}")
                raise ValueError("Invalid private key format")
    
    async def _get_balance(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Get SOL balance for an address."""
        await self._ensure_client()
        
        try:
            address = Pubkey.from_string(arguments["address"])
            response = await self.client.get_balance(address)
            
            if response.value is not None:
                balance_sol = response.value / 1_000_000_000  # Convert lamports to SOL
                result = {
                    "address": arguments["address"],
                    "balance_sol": balance_sol,
                    "balance_lamports": response.value
                }
                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            else:
                return [TextContent(type="text", text="Failed to get balance")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error getting balance: {str(e)}")]
    
    async def _get_token_balance(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Get SPL token balance for an address."""
        await self._ensure_client()
        
        try:
            address = Pubkey.from_string(arguments["address"])
            token_mint = Pubkey.from_string(arguments["token_mint"])
            
            # Get token accounts by owner
            response = await self.client.get_token_accounts_by_owner(
                address, 
                {"mint": token_mint}
            )
            
            if response.value:
                # Get the first token account
                token_account = response.value[0]
                account_info = token_account.account
                
                # Parse token account data
                import struct
                data = account_info.data
                if len(data) >= 64:
                    amount = struct.unpack('<Q', data[0:8])[0]
                    
                    result = {
                        "address": arguments["address"],
                        "token_mint": arguments["token_mint"],
                        "balance": amount,
                        "token_account": str(token_account.pubkey)
                    }
                    return [TextContent(type="text", text=json.dumps(result, indent=2))]
            
            return [TextContent(type="text", text="No token account found")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error getting token balance: {str(e)}")]
    
    async def _get_transaction(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Get transaction details."""
        await self._ensure_client()
        
        try:
            signature = arguments["signature"]
            response = await self.client.get_transaction(signature)
            
            if response.value:
                tx = response.value
                result = {
                    "signature": signature,
                    "slot": tx.slot,
                    "block_time": tx.block_time,
                    "meta": {
                        "fee": tx.transaction.meta.fee if tx.transaction.meta else None,
                        "status": "success" if tx.transaction.meta and tx.transaction.meta.err is None else "failed"
                    }
                }
                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            else:
                return [TextContent(type="text", text="Transaction not found")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error getting transaction: {str(e)}")]
    
    async def _get_token_price(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Get current token price from CoinGecko."""
        try:
            token_symbol = arguments["token_symbol"].lower()
            
            # Map common Solana tokens to CoinGecko IDs
            token_map = {
                "sol": "solana",
                "usdc": "usd-coin",
                "usdt": "tether",
                "ray": "raydium",
                "srm": "serum"
            }
            
            token_id = token_map.get(token_symbol, token_symbol)
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"https://api.coingecko.com/api/v3/simple/price",
                    params={
                        "ids": token_id,
                        "vs_currencies": "usd",
                        "include_24hr_change": "true"
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if token_id in data:
                        price_data = data[token_id]
                        result = {
                            "token": token_symbol.upper(),
                            "price_usd": price_data.get("usd"),
                            "change_24h": price_data.get("usd_24h_change")
                        }
                        return [TextContent(type="text", text=json.dumps(result, indent=2))]
                
                return [TextContent(type="text", text=f"Price data not found for {token_symbol}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error getting token price: {str(e)}")]
    
    async def _create_wallet(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Generate a new Solana wallet."""
        try:
            # Generate new keypair
            new_keypair = Keypair()
            
            # Get the public key and private key
            public_key = str(new_keypair.pubkey())
            
            import base58
            private_key = base58.b58encode(bytes(new_keypair)).decode('utf-8')
            
            result = {
                "public_key": public_key,
                "private_key": private_key,
                "warning": "Store the private key securely. Never share it with anyone."
            }
            
            return [TextContent(type="text", text=json.dumps(result, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error creating wallet: {str(e)}")]
    
    async def _get_account_info(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Get detailed account information."""
        await self._ensure_client()
        
        try:
            address = Pubkey.from_string(arguments["address"])
            response = await self.client.get_account_info(address)
            
            if response.value:
                account = response.value
                result = {
                    "address": arguments["address"],
                    "lamports": account.lamports,
                    "owner": str(account.owner),
                    "executable": account.executable,
                    "rent_epoch": account.rent_epoch,
                    "data_length": len(account.data) if account.data else 0
                }
                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            else:
                return [TextContent(type="text", text="Account not found")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error getting account info: {str(e)}")]

    async def _swap_tokens(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """Swap tokens using Jupiter Aggregator."""
        await self._ensure_client()
        
        input_mint = arguments["input_mint"]
        output_mint = arguments["output_mint"]
        amount = arguments["amount"]
        user_public_key = arguments["user_public_key"]
        slippage_bps = arguments.get("slippage_bps", 50) # Default 0.5%

        jup_api_base = "https://quote-api.jup.ag/v6"

        async with httpx.AsyncClient() as client:
            # 1. Get quote
            quote_url = f"{jup_api_base}/quote"
            quote_params = {
                "inputMint": input_mint,
                "outputMint": output_mint,
                "amount": amount,
                "slippageBps": slippage_bps
            }
            
            try:
                quote_response = await client.get(quote_url, params=quote_params)
                quote_response.raise_for_status()
                quote_data = quote_response.json()
            except httpx.HTTPStatusError as e:
                logger.error(f"Jupiter quote API error: {e.response.text}")
                return [TextContent(type="text", text=f"Error getting swap quote: {e.response.text}")]
            except Exception as e:
                logger.error(f"Error getting swap quote: {e}")
                return [TextContent(type="text", text=f"Error getting swap quote: {str(e)}")]

            # 2. Get swap transaction
            swap_url = f"{jup_api_base}/swap"
            swap_payload = {
                "userPublicKey": user_public_key,
                "quoteResponse": quote_data,
                "wrapAndUnwrapSol": True, # Automatically wrap/unwrap SOL if needed
            }

            try:
                swap_response = await client.post(swap_url, json=swap_payload)
                swap_response.raise_for_status()
                swap_data = swap_response.json()
                
                swap_transaction = swap_data.get("swapTransaction")
                if not swap_transaction:
                    return [TextContent(type="text", text="Failed to get swap transaction from Jupiter.")]

                result = {
                    "message": "Swap transaction created successfully. Please sign and send this transaction.",
                    "swapTransaction": swap_transaction # This is a base64 encoded transaction
                }
                return [TextContent(type="text", text=json.dumps(result, indent=2))]

            except httpx.HTTPStatusError as e:
                logger.error(f"Jupiter swap API error: {e.response.text}")
                return [TextContent(type="text", text=f"Error creating swap transaction: {e.response.text}")]
            except Exception as e:
                logger.error(f"Error creating swap transaction: {e}")
                return [TextContent(type="text", text=f"Error creating swap transaction: {str(e)}")]

async def main():
    """Main entry point for the MCP server."""
    server_instance = SolanaMCPServer()
    
    # Run the server
    async with stdio_server() as (read_stream, write_stream):
        await server_instance.server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="solana-mcp-server",
                server_version="1.0.0",
                capabilities=server_instance.server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None,
                ),
            ),
        )

if __name__ == "__main__":
    import base58
    asyncio.run(main())