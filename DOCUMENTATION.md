# Solana MCP Server - Technical Documentation

## Overview

The Solana MCP (Model Context Protocol) Server is a comprehensive tool that enables Large Language Models (LLMs) to interact with the Solana blockchain. It provides a standardized interface for blockchain operations through the MCP protocol.

## Architecture

### Core Components

1. **solana_mcp_server.py** - Main MCP server implementation
2. **config.py** - Configuration management system
3. **utils.py** - Utility functions for Solana operations
4. **examples.py** - Usage examples and demonstrations
5. **test_server.py** - Test suite for validation

### Key Features

- **Account Management**: Create wallets, check balances, get account information
- **Token Operations**: Transfer SOL and SPL tokens, check token balances
- **Transaction Monitoring**: Track transaction status and retrieve transaction details
- **Market Data Integration**: Real-time token prices via CoinGecko API
- **Security Features**: Rate limiting, transaction amount limits, confirmation requirements
- **Multi-Network Support**: Mainnet, Devnet, and Testnet compatibility

## MCP Tools Available

### Account Tools

#### `get_balance`
Get SOL balance for a Solana address.

**Parameters:**
- `address` (string): Solana public key address

**Returns:**
```json
{
  "address": "11111111111111111111111111111111",
  "balance_sol": 0.0,
  "balance_lamports": 0
}
```

#### `get_account_info`
Get detailed account information.

**Parameters:**
- `address` (string): Solana public key address

**Returns:**
```json
{
  "address": "11111111111111111111111111111111",
  "lamports": 1000000000,
  "owner": "11111111111111111111111111111111",
  "executable": false,
  "rent_epoch": 361,
  "data_length": 0
}
```

#### `create_wallet`
Generate a new Solana wallet.

**Parameters:** None

**Returns:**
```json
{
  "public_key": "8sLbNZoA1cfnvMJLPfp98ZLAnFSYCFApfJKMbiXNLwxj",
  "private_key": "base58_encoded_private_key",
  "warning": "Store the private key securely. Never share it with anyone."
}
```

### Token Tools

#### `get_token_balance`
Get SPL token balance for an address.

**Parameters:**
- `address` (string): Solana public key address
- `token_mint` (string): Token mint address

**Returns:**
```json
{
  "address": "8sLbNZoA1cfnvMJLPfp98ZLAnFSYCFApfJKMbiXNLwxj",
  "token_mint": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
  "balance": 1000000,
  "token_account": "token_account_address"
}
```

#### `transfer_sol`
Transfer SOL from the configured wallet to another address.

**Parameters:**
- `to_address` (string): Recipient's Solana address
- `amount` (number): Amount of SOL to transfer

**Returns:**
```json
{
  "signature": "transaction_signature",
  "from_address": "sender_address",
  "to_address": "recipient_address",
  "amount_sol": 0.1,
  "amount_lamports": 100000000
}
```

### Transaction Tools

#### `get_transaction`
Get details of a Solana transaction.

**Parameters:**
- `signature` (string): Transaction signature

**Returns:**
```json
{
  "signature": "transaction_signature",
  "slot": 123456789,
  "block_time": 1640995200,
  "meta": {
    "fee": 5000,
    "status": "success"
  }
}
```

### Market Data Tools

#### `get_token_price`
Get current price of a token from CoinGecko.

**Parameters:**
- `token_symbol` (string): Token symbol (e.g., SOL, USDC)

**Returns:**
```json
{
  "token": "SOL",
  "price_usd": 100.50,
  "change_24h": 5.25
}
```

## Configuration

### Environment Variables

Create a `.env` file with the following configuration:

```env
# Solana Configuration
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
SOLANA_DEVNET_RPC_URL=https://api.devnet.solana.com
SOLANA_PRIVATE_KEY=your_base58_private_key_here

# Network Settings
DEFAULT_COMMITMENT=confirmed
DEFAULT_NETWORK=mainnet

# Security
MAX_TRANSACTION_AMOUNT=1.0
REQUIRE_CONFIRMATION=true

# API Keys (optional)
COINGECKO_API_KEY=your_coingecko_api_key

# Features
ENABLE_DEFI_TOOLS=true
ENABLE_NFT_TOOLS=true
ENABLE_MARKET_DATA=true
```

### Network Configuration

The server supports multiple Solana networks:

- **Mainnet**: Production network with real SOL
- **Devnet**: Development network with test SOL
- **Testnet**: Testing network for validators

### Security Settings

- **MAX_TRANSACTION_AMOUNT**: Maximum SOL amount per transaction
- **REQUIRE_CONFIRMATION**: Whether to require transaction confirmation
- **Rate Limiting**: Built-in rate limiting for API calls

## Installation and Setup

### Quick Start

1. **Clone or download the project**
2. **Run setup (Windows):**
   ```bash
   setup.bat
   ```
   
3. **Run setup (Linux/Mac):**
   ```bash
   python setup.py
   ```

4. **Configure environment:**
   - Edit `.env` file with your settings
   - Add your Solana private key for transaction capabilities

5. **Start the server:**
   ```bash
   python solana_mcp_server.py
   ```

### Manual Installation

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate.bat  # Windows
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

## Usage Examples

### Basic Usage

```python
from solana_mcp_server import SolanaMCPServer

# Create server instance
server = SolanaMCPServer()

# Get balance
result = await server._get_balance({
    "address": "11111111111111111111111111111111"
})

# Create wallet
wallet = await server._create_wallet({})

# Get token price
price = await server._get_token_price({
    "token_symbol": "sol"
})
```

### Running Examples

```bash
# Run comprehensive examples
python examples.py

# Run tests
python test_server.py
```

## Error Handling

The server includes comprehensive error handling:

- **Invalid addresses**: Validates Solana address format
- **Network errors**: Handles RPC connection issues
- **Transaction failures**: Reports detailed error messages
- **Rate limiting**: Prevents API abuse
- **Security checks**: Validates transaction amounts and permissions

## Common Token Addresses

The server includes common Solana token mint addresses:

- **USDC**: `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`
- **USDT**: `Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB`
- **Wrapped SOL**: `So11111111111111111111111111111111111111112`
- **RAY**: `4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R`

## Security Best Practices

1. **Private Key Management**:
   - Never commit private keys to version control
   - Use environment variables for sensitive data
   - Consider using hardware wallets for production

2. **Network Security**:
   - Test on devnet before mainnet operations
   - Use HTTPS RPC endpoints
   - Implement proper rate limiting

3. **Transaction Security**:
   - Set reasonable transaction limits
   - Require confirmation for large amounts
   - Validate all addresses before transactions

4. **API Security**:
   - Use API keys where available
   - Implement request throttling
   - Monitor for unusual activity

## Troubleshooting

### Common Issues

1. **Python not found**:
   - Install Python 3.8+ from python.org
   - Add Python to system PATH

2. **Dependencies fail to install**:
   - Upgrade pip: `python -m pip install --upgrade pip`
   - Use virtual environment
   - Check internet connection

3. **RPC connection errors**:
   - Verify RPC URL in .env file
   - Check network connectivity
   - Try different RPC endpoints

4. **Private key errors**:
   - Ensure private key is in base58 format
   - Verify key length (64 bytes when decoded)
   - Check key permissions

### Debug Mode

Enable debug logging by setting:
```env
LOG_LEVEL=DEBUG
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the examples and tests
3. Create an issue on the repository
4. Join the community discussions

## Roadmap

Future enhancements planned:
- NFT operations support
- DeFi protocol integrations
- Advanced transaction building
- WebSocket real-time updates
- Multi-signature wallet support
- Staking operations
- Governance participation tools