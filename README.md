# Solana Trade MCP Server

A Model Context Protocol (MCP) server that provides onchain tools for LLMs, allowing them to interact with the Solana network.

## Features

- **Account Management**: Create wallets, check SOL and SPL token balances, and get account info.
- **Transaction Monitoring**: Look up individual transaction details.
- **Market Data**: Get real-time token prices.
- **DeFi Integration**: Swap tokens using the Jupiter aggregator.

## Installation

1.  **Clone the repository**
    ```bash
    git clone <repository_url>
    ```

2.  **Set up the environment**
    ```bash
    chmod +x setup.sh
    ./setup.sh
    ```
    This will create a virtual environment, install dependencies, and set up your `.env` file.

3.  **Configure environment variables**

    Your `.env` file will be created from `.env.example`. You can add your Solana RPC URL and a private key if you intend to perform actions that require signing (not currently implemented).

    ```env
    SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
    SOLANA_PRIVATE_KEY=
    DEFAULT_COMMITMENT=confirmed
    DEFAULT_NETWORK=mainnet
    ```

## Usage

Start the MCP server using the run script:

```bash
chmod +x run.sh
./run.sh
```

To see examples of how to use the tools, run:

```bash
./run.sh examples
```

## Available Tools

- `get_balance`: Get SOL balance for a given address.
- `get_token_balance`: Get the balance of a specific SPL token for a given address.
- `create_wallet`: Generate a new Solana wallet (keypair).
- `get_transaction`: Get the details of a specific transaction by its signature.
- `get_token_price`: Get the current price of a token (e.g., SOL, USDC) from an external API.
- `get_account_info`: Get detailed, low-level information about a Solana account.
- `swap_tokens`: Get a swap transaction from Jupiter Aggregator to exchange one token for another.

## Using in an IDE (e.g., Cursor)

To use this MCP server with an AI-powered IDE like Cursor, you can configure it as a custom tool provider.

1.  **Start the Server**: First, ensure the MCP server is running:
    ```bash
    ./run.sh
    ```

2.  **Configure in Cursor**:
    - Go to `File > Preferences > Settings`.
    - Search for `mcp` or `Model Context Protocol`.
    - In the `Custom MCP Servers` section, add a new entry:
      - **Name**: `Solana Tools` (or any name you prefer)
      - **Address**: `stdio` (since this server communicates over stdin/stdout)
      - **Command**: `[path-to-your-project]/run.sh` (use the absolute path to `run.sh`)

3.  **Use the Tools**: Once configured, you can invoke the tools in your chat with the AI. For example:
    ```
    @Solana Tools get_balance --address <some_solana_address>
    ```

    The AI will use the server to execute the command and return the result directly in the chat.

## Security

- Never commit private keys to version control
- Use environment variables for sensitive configuration
- Test on devnet before mainnet operations
- Implement proper error handling and validation

## License

MIT License