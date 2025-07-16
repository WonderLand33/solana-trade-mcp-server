"""
Utility functions for Solana operations.
"""

import base58
import json
from typing import Dict, List, Optional, Union
from solders.pubkey import Pubkey
from solders.keypair import Keypair

# Common Solana token mint addresses
COMMON_TOKENS = {
    "USDC": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
    "USDT": "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB",
    "SOL": "So11111111111111111111111111111111111111112",  # Wrapped SOL
    "RAY": "4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R",
    "SRM": "SRMuApVNdxXokk5GT7XD5cUUgXMBCoAz2LHeuAoKWRt",
    "ORCA": "orcaEKTdK7LKz57vaAYr9QeNsVEPfiu6QeMU1kektZE",
    "MNGO": "MangoCzJ36AjZyKwVj3VnYU4GTonjfVEnJmvvWaxLac"
}

# Common Solana program addresses
PROGRAM_ADDRESSES = {
    "SYSTEM_PROGRAM": "11111111111111111111111111111111",
    "TOKEN_PROGRAM": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
    "ASSOCIATED_TOKEN_PROGRAM": "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL",
    "RENT_PROGRAM": "SysvarRent111111111111111111111111111111111",
    "CLOCK_PROGRAM": "SysvarC1ock11111111111111111111111111111111"
}

def validate_solana_address(address: str) -> bool:
    """
    Validate if a string is a valid Solana address.
    
    Args:
        address: The address string to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        pubkey = Pubkey.from_string(address)
        return True
    except Exception:
        return False

def lamports_to_sol(lamports: int) -> float:
    """
    Convert lamports to SOL.
    
    Args:
        lamports: Amount in lamports
        
    Returns:
        float: Amount in SOL
    """
    return lamports / 1_000_000_000

def sol_to_lamports(sol: float) -> int:
    """
    Convert SOL to lamports.
    
    Args:
        sol: Amount in SOL
        
    Returns:
        int: Amount in lamports
    """
    return int(sol * 1_000_000_000)

def format_token_amount(amount: int, decimals: int) -> float:
    """
    Format token amount based on decimals.
    
    Args:
        amount: Raw token amount
        decimals: Number of decimal places
        
    Returns:
        float: Formatted amount
    """
    return amount / (10 ** decimals)

def get_token_mint_address(symbol: str) -> Optional[str]:
    """
    Get token mint address by symbol.
    
    Args:
        symbol: Token symbol (e.g., 'USDC')
        
    Returns:
        Optional[str]: Mint address if found, None otherwise
    """
    return COMMON_TOKENS.get(symbol.upper())

def is_valid_private_key(private_key: str) -> bool:
    """
    Validate if a string is a valid Solana private key.
    
    Args:
        private_key: The private key string to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        # Try to decode as base58
        decoded = base58.b58decode(private_key)
        # Solana private keys should be 64 bytes
        if len(decoded) == 64:
            # Try to create a keypair
            Keypair.from_bytes(decoded)
            return True
        return False
    except Exception:
        return False

def create_keypair_from_private_key(private_key: str) -> Optional[Keypair]:
    """
    Create a Keypair from a private key string.
    
    Args:
        private_key: Base58 encoded private key
        
    Returns:
        Optional[Keypair]: Keypair if successful, None otherwise
    """
    try:
        decoded = base58.b58decode(private_key)
        return Keypair.from_bytes(decoded)
    except Exception:
        return None

def format_transaction_result(signature: str, success: bool, error: Optional[str] = None) -> Dict:
    """
    Format transaction result for consistent output.
    
    Args:
        signature: Transaction signature
        success: Whether transaction was successful
        error: Error message if failed
        
    Returns:
        Dict: Formatted result
    """
    result = {
        "signature": signature,
        "success": success,
        "timestamp": None  # Could add current timestamp
    }
    
    if error:
        result["error"] = error
        
    return result

def truncate_address(address: str, start_chars: int = 4, end_chars: int = 4) -> str:
    """
    Truncate a Solana address for display purposes.
    
    Args:
        address: Full address
        start_chars: Number of characters to show at start
        end_chars: Number of characters to show at end
        
    Returns:
        str: Truncated address
    """
    if len(address) <= start_chars + end_chars + 3:
        return address
    
    return f"{address[:start_chars]}...{address[-end_chars:]}"

def calculate_rent_exempt_balance(data_length: int) -> int:
    """
    Calculate minimum balance for rent exemption.
    
    Args:
        data_length: Length of account data in bytes
        
    Returns:
        int: Minimum balance in lamports
    """
    # Solana rent calculation: (128 + data_length) * rent_per_byte_year * years_exempt
    # Simplified calculation for 2 years exemption
    return (128 + data_length) * 19055406 * 2

class SolanaAddressBook:
    """Helper class to manage commonly used addresses."""
    
    def __init__(self):
        self.addresses = {}
    
    def add_address(self, name: str, address: str, description: str = ""):
        """Add an address to the address book."""
        if validate_solana_address(address):
            self.addresses[name] = {
                "address": address,
                "description": description
            }
            return True
        return False
    
    def get_address(self, name: str) -> Optional[str]:
        """Get an address by name."""
        entry = self.addresses.get(name)
        return entry["address"] if entry else None
    
    def list_addresses(self) -> Dict[str, Dict[str, str]]:
        """List all addresses in the address book."""
        return self.addresses.copy()
    
    def remove_address(self, name: str) -> bool:
        """Remove an address from the address book."""
        if name in self.addresses:
            del self.addresses[name]
            return True
        return False

def parse_transaction_logs(logs: List[str]) -> Dict[str, Union[str, List[str]]]:
    """
    Parse transaction logs for useful information.
    
    Args:
        logs: List of log strings from transaction
        
    Returns:
        Dict: Parsed log information
    """
    parsed = {
        "program_calls": [],
        "errors": [],
        "success": True
    }
    
    for log in logs:
        if "Program" in log and "invoke" in log:
            parsed["program_calls"].append(log)
        elif "Error" in log or "failed" in log.lower():
            parsed["errors"].append(log)
            parsed["success"] = False
    
    return parsed