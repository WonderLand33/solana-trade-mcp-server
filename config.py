"""
Configuration management for Solana MCP Server.
"""

import os
from typing import Optional
from dataclasses import dataclass
from dotenv import load_dotenv

@dataclass
class NetworkConfig:
    """Network-specific configuration."""
    name: str
    rpc_url: str
    ws_url: Optional[str] = None
    explorer_url: Optional[str] = None

@dataclass
class SecurityConfig:
    """Security-related configuration."""
    max_transaction_amount: float = 1.0
    require_confirmation: bool = True
    allowed_programs: Optional[list] = None
    rate_limit_per_minute: int = 60

class Config:
    """Main configuration class for the Solana MCP Server."""
    
    def __init__(self, env_file: Optional[str] = None):
        """
        Initialize configuration.
        
        Args:
            env_file: Path to environment file (optional)
        """
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()
        
        self._load_config()
    
    def _load_config(self):
        """Load configuration from environment variables."""
        
        # Network configuration
        self.networks = {
            "mainnet": NetworkConfig(
                name="mainnet",
                rpc_url=os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com"),
                ws_url=os.getenv("SOLANA_WS_URL", "wss://api.mainnet-beta.solana.com"),
                explorer_url="https://explorer.solana.com"
            ),
            "devnet": NetworkConfig(
                name="devnet",
                rpc_url=os.getenv("SOLANA_DEVNET_RPC_URL", "https://api.devnet.solana.com"),
                ws_url=os.getenv("SOLANA_DEVNET_WS_URL", "wss://api.devnet.solana.com"),
                explorer_url="https://explorer.solana.com?cluster=devnet"
            ),
            "testnet": NetworkConfig(
                name="testnet",
                rpc_url=os.getenv("SOLANA_TESTNET_RPC_URL", "https://api.testnet.solana.com"),
                ws_url=os.getenv("SOLANA_TESTNET_WS_URL", "wss://api.testnet.solana.com"),
                explorer_url="https://explorer.solana.com?cluster=testnet"
            )
        }
        
        # Current network
        self.current_network = os.getenv("DEFAULT_NETWORK", "mainnet")
        
        # Wallet configuration
        self.private_key = os.getenv("SOLANA_PRIVATE_KEY")
        self.wallet_path = os.getenv("SOLANA_WALLET_PATH")
        
        # Commitment level
        self.commitment = os.getenv("DEFAULT_COMMITMENT", "confirmed")
        
        # Security configuration
        self.security = SecurityConfig(
            max_transaction_amount=float(os.getenv("MAX_TRANSACTION_AMOUNT", "1.0")),
            require_confirmation=os.getenv("REQUIRE_CONFIRMATION", "true").lower() == "true",
            rate_limit_per_minute=int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
        )
        
        # API Keys
        self.jupiter_api_key = os.getenv("JUPITER_API_KEY")
        self.coingecko_api_key = os.getenv("COINGECKO_API_KEY")
        
        # Logging
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.log_file = os.getenv("LOG_FILE")
        
        # Server configuration
        self.server_host = os.getenv("SERVER_HOST", "localhost")
        self.server_port = int(os.getenv("SERVER_PORT", "8000"))
        
        # Feature flags
        self.enable_defi_tools = os.getenv("ENABLE_DEFI_TOOLS", "true").lower() == "true"
        self.enable_nft_tools = os.getenv("ENABLE_NFT_TOOLS", "true").lower() == "true"
        self.enable_market_data = os.getenv("ENABLE_MARKET_DATA", "true").lower() == "true"
    
    def get_network_config(self, network: Optional[str] = None) -> NetworkConfig:
        """
        Get network configuration.
        
        Args:
            network: Network name (defaults to current network)
            
        Returns:
            NetworkConfig: Network configuration
        """
        network_name = network or self.current_network
        return self.networks.get(network_name, self.networks["mainnet"])
    
    def get_rpc_url(self, network: Optional[str] = None) -> str:
        """
        Get RPC URL for specified network.
        
        Args:
            network: Network name (defaults to current network)
            
        Returns:
            str: RPC URL
        """
        return self.get_network_config(network).rpc_url
    
    def is_mainnet(self) -> bool:
        """Check if current network is mainnet."""
        return self.current_network == "mainnet"
    
    def is_devnet(self) -> bool:
        """Check if current network is devnet."""
        return self.current_network == "devnet"
    
    def validate_config(self) -> list:
        """
        Validate configuration and return list of issues.
        
        Returns:
            list: List of configuration issues
        """
        issues = []
        
        # Check if network exists
        if self.current_network not in self.networks:
            issues.append(f"Unknown network: {self.current_network}")
        
        # Check private key format if provided
        if self.private_key:
            try:
                import base58
                decoded = base58.b58decode(self.private_key)
                if len(decoded) != 64:
                    issues.append("Invalid private key length")
            except Exception:
                issues.append("Invalid private key format")
        
        # Check security settings
        if self.security.max_transaction_amount <= 0:
            issues.append("Max transaction amount must be positive")
        
        if self.security.rate_limit_per_minute <= 0:
            issues.append("Rate limit must be positive")
        
        return issues
    
    def to_dict(self) -> dict:
        """Convert configuration to dictionary."""
        return {
            "current_network": self.current_network,
            "commitment": self.commitment,
            "security": {
                "max_transaction_amount": self.security.max_transaction_amount,
                "require_confirmation": self.security.require_confirmation,
                "rate_limit_per_minute": self.security.rate_limit_per_minute
            },
            "features": {
                "defi_tools": self.enable_defi_tools,
                "nft_tools": self.enable_nft_tools,
                "market_data": self.enable_market_data
            },
            "server": {
                "host": self.server_host,
                "port": self.server_port
            }
        }

# Global configuration instance
config = Config()