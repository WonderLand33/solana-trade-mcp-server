#!/usr/bin/env python3
"""
Test script for Solana MCP Server functionality.
"""

import asyncio
import json
import os
from typing import Dict, Any

from solana_mcp_server import SolanaMCPServer
from utils import validate_solana_address, lamports_to_sol, get_token_mint_address
from config import config

class MCPServerTester:
    """Test class for MCP server functionality."""
    
    def __init__(self):
        self.server = SolanaMCPServer()
    
    async def test_get_balance(self, address: str = "11111111111111111111111111111111"):
        """Test getting SOL balance."""
        print(f"\n🔍 Testing get_balance for address: {address}")
        
        try:
            result = await self.server._get_balance({"address": address})
            print(f"✅ Result: {result[0].text}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    async def test_create_wallet(self):
        """Test wallet creation."""
        print(f"\n🔍 Testing create_wallet")
        
        try:
            result = await self.server._create_wallet({})
            wallet_data = json.loads(result[0].text)
            print(f"✅ Created wallet:")
            print(f"   Public Key: {wallet_data['public_key']}")
            print(f"   Private Key: {wallet_data['private_key'][:20]}...")
            return wallet_data
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    async def test_get_token_price(self, token: str = "sol"):
        """Test getting token price."""
        print(f"\n🔍 Testing get_token_price for {token}")
        
        try:
            result = await self.server._get_token_price({"token_symbol": token})
            print(f"✅ Result: {result[0].text}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    async def test_get_account_info(self, address: str):
        """Test getting account information."""
        print(f"\n🔍 Testing get_account_info for address: {address}")
        
        try:
            result = await self.server._get_account_info({"address": address})
            print(f"✅ Result: {result[0].text}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    async def test_address_validation(self):
        """Test address validation utilities."""
        print(f"\n🔍 Testing address validation")
        
        test_addresses = [
            "11111111111111111111111111111111",  # System program
            "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",  # Token program
            "invalid_address",  # Invalid
            "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"  # USDC mint
        ]
        
        for addr in test_addresses:
            is_valid = validate_solana_address(addr)
            status = "✅ Valid" if is_valid else "❌ Invalid"
            print(f"   {addr[:20]}... - {status}")
    
    async def test_token_utilities(self):
        """Test token utility functions."""
        print(f"\n🔍 Testing token utilities")
        
        # Test token mint lookup
        tokens = ["USDC", "SOL", "USDT", "INVALID"]
        for token in tokens:
            mint = get_token_mint_address(token)
            if mint:
                print(f"   {token}: {mint}")
            else:
                print(f"   {token}: Not found")
        
        # Test lamports conversion
        lamports = 1000000000
        sol = lamports_to_sol(lamports)
        print(f"   {lamports} lamports = {sol} SOL")
    
    async def run_all_tests(self):
        """Run all tests."""
        print("🚀 Starting Solana MCP Server Tests")
        print("=" * 50)
        
        # Test configuration
        print(f"\n📋 Configuration:")
        print(f"   Network: {config.current_network}")
        print(f"   RPC URL: {config.get_rpc_url()}")
        print(f"   Commitment: {config.commitment}")
        
        # Validate configuration
        issues = config.validate_config()
        if issues:
            print(f"   ⚠️  Configuration issues: {issues}")
        else:
            print(f"   ✅ Configuration valid")
        
        # Test utilities
        await self.test_address_validation()
        await self.test_token_utilities()
        
        # Test wallet creation
        wallet = await self.test_create_wallet()
        
        # Test balance checking (using system program address as example)
        await self.test_get_balance("11111111111111111111111111111111")
        
        # Test account info
        if wallet:
            await self.test_get_account_info(wallet["public_key"])
        
        # Test token price (if market data is enabled)
        if config.enable_market_data:
            await self.test_get_token_price("sol")
            await self.test_get_token_price("usdc")
        
        print("\n" + "=" * 50)
        print("🎉 Tests completed!")

async def main():
    """Main test function."""
    tester = MCPServerTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    # Set up test environment
    os.environ.setdefault("DEFAULT_NETWORK", "devnet")
    os.environ.setdefault("ENABLE_MARKET_DATA", "true")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
    except Exception as e:
        print(f"\n\nTest error: {e}")
        import traceback
        traceback.print_exc()