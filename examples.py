#!/usr/bin/env python3
"""
Example usage of the Solana MCP Server.

This script demonstrates how to interact with the MCP server
and use its various tools for Solana blockchain operations.
"""

import asyncio
import json
from typing import Dict, Any, List

from mcp.types import TextContent
from solana_mcp_server import SolanaMCPServer

class SolanaExample:
    """Example class demonstrating Solana MCP Server usage."""
    
    def __init__(self):
        self.server = SolanaMCPServer()
    
    async def example_wallet_operations(self):
        """Demonstrate wallet-related operations."""
        print("🔐 Wallet Operations Example")
        print("-" * 40)
        
        # Create a new wallet
        print("1. Creating a new wallet...")
        wallet_result = await self.server._create_wallet({})
        wallet_data = json.loads(wallet_result[0].text)
        
        print(f"   ✅ New wallet created:")
        print(f"   Public Key: {wallet_data['public_key']}")
        print(f"   Private Key: {wallet_data['private_key'][:20]}...")
        
        # Check balance of the new wallet
        print("\n2. Checking wallet balance...")
        balance_result = await self.server._get_balance({
            "address": wallet_data['public_key']
        })
        balance_data = json.loads(balance_result[0].text)
        
        print(f"   ✅ Balance: {balance_data['balance_sol']} SOL")
        
        return wallet_data
    
    async def example_account_info(self, address: str):
        """Demonstrate account information retrieval."""
        print(f"\n📊 Account Information Example")
        print("-" * 40)
        
        print(f"Getting account info for: {address[:20]}...")
        account_result = await self.server._get_account_info({"address": address})
        
        try:
            account_data = json.loads(account_result[0].text)
            print(f"   ✅ Account found:")
            print(f"   Lamports: {account_data.get('lamports', 0):,}")
            print(f"   Owner: {account_data.get('owner', 'Unknown')}")
            print(f"   Executable: {account_data.get('executable', False)}")
        except json.JSONDecodeError:
            print(f"   ℹ️  {account_result[0].text}")
    
    async def example_market_data(self):
        """Demonstrate market data retrieval."""
        print(f"\n💹 Market Data Example")
        print("-" * 40)
        
        tokens = ["sol", "usdc", "usdt"]
        
        for token in tokens:
            print(f"Getting price for {token.upper()}...")
            try:
                price_result = await self.server._get_token_price({
                    "token_symbol": token
                })
                price_data = json.loads(price_result[0].text)
                
                if "price_usd" in price_data:
                    price = price_data["price_usd"]
                    change = price_data.get("change_24h", 0)
                    change_symbol = "📈" if change > 0 else "📉" if change < 0 else "➡️"
                    
                    print(f"   ✅ {token.upper()}: ${price:.4f} {change_symbol} {change:.2f}%")
                else:
                    print(f"   ℹ️  {price_result[0].text}")
            except Exception as e:
                print(f"   ❌ Error getting {token} price: {e}")
    
    async def example_transaction_lookup(self):
        """Demonstrate transaction lookup."""
        print(f"\n🔍 Transaction Lookup Example")
        print("-" * 40)
        
        # Example transaction signature (this might not exist)
        example_sig = "5VERv8NMvzbJMEkV8xnrLkEaWRtSz9CosKDYjCJjBRnbJLgp8uirBgmQpjKhoR4tjF3ZpRzrFmBV6UjKdiSZkQUW"
        
        print(f"Looking up transaction: {example_sig[:20]}...")
        tx_result = await self.server._get_transaction({
            "signature": example_sig
        })
        
        print(f"   ℹ️  {tx_result[0].text}")
    
    async def example_token_operations(self):
        """Demonstrate token-related operations."""
        print(f"\n🪙 Token Operations Example")
        print("-" * 40)
        
        # Example addresses (these are real program addresses)
        usdc_mint = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
        example_address = "11111111111111111111111111111111"  # System program
        
        print(f"Checking USDC balance for system program...")
        token_balance_result = await self.server._get_token_balance({
            "address": example_address,
            "token_mint": usdc_mint
        })
        
        print(f"   ℹ️  {token_balance_result[0].text}")

    async def example_swap_tokens(self, user_public_key: str):
        """Demonstrate token swap operations."""
        print(f"\n🔄 Token Swap Example (Jupiter)")
        print("-" * 40)

        # Swap 0.01 SOL for USDC
        sol_mint = "So11111111111111111111111111111111111111112"
        usdc_mint = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
        amount_to_swap = 10_000_000  # 0.01 SOL in lamports

        print(f"Attempting to swap 0.01 SOL for USDC for wallet {user_public_key[:10]}...")

        try:
            swap_result = await self.server._swap_tokens({
                "input_mint": sol_mint,
                "output_mint": usdc_mint,
                "amount": amount_to_swap,
                "user_public_key": user_public_key,
                "slippage_bps": 50  # 0.5% slippage
            })

            swap_data = json.loads(swap_result[0].text)
            print(f"   ✅ {swap_data['message']}")
            print(f"   Transaction (base64): {swap_data['swapTransaction'][:50]}...")
            print(f"   To execute, this transaction must be signed and sent to the network.")

        except Exception as e:
            print(f"   ❌ Error during swap: {e}")
    
    async def run_examples(self):
        """Run all examples."""
        print("🚀 Solana MCP Server Examples")
        print("=" * 50)
        
        try:
            # Wallet operations
            wallet = await self.example_wallet_operations()
            
            # Account information
            await self.example_account_info(wallet['public_key'])
            await self.example_account_info("11111111111111111111111111111111")  # System program
            
            # Market data
            await self.example_market_data()
            
            # Transaction lookup
            await self.example_transaction_lookup()
            
            # Token operations
            await self.example_token_operations()

            # Token Swap
            await self.example_swap_tokens(wallet['public_key'])
            
            print("\n" + "=" * 50)
            print("✅ All examples completed!")
            
            # Show available tools
            await self.show_available_tools()
            
        except Exception as e:
            print(f"\n❌ Example error: {e}")
            import traceback
            traceback.print_exc()
    
    async def show_available_tools(self):
        """Show all available tools."""
        print(f"\n🛠️  Available MCP Tools")
        print("-" * 40)
        
        # Get tools list (this would normally be called by MCP client)
        tools = [
            "get_balance - Get SOL balance for an address",
            "get_token_balance - Get SPL token balance",
            "get_transaction - Get transaction details",
            "get_token_price - Get current token price",
            "create_wallet - Generate a new wallet",
            "get_account_info - Get detailed account information",
            "swap_tokens - Swap tokens using Jupiter Aggregator"
        ]
        
        for i, tool in enumerate(tools, 1):
            print(f"   {i}. {tool}")
        
        print(f"\n💡 Usage Tips:")
        print(f"   - Use devnet for testing (set DEFAULT_NETWORK=devnet)")
        print(f"   - Configure private key for transfer operations")
        print(f"   - Check rate limits for API calls")
        print(f"   - Always validate addresses before transactions")

async def main():
    """Main example function."""
    example = SolanaExample()
    await example.run_examples()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nExamples interrupted by user")
    except Exception as e:
        print(f"\n\nExample error: {e}")
        import traceback
        traceback.print_exc()