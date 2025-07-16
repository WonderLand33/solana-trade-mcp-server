# Solana Trade MCP 服务器

一个模型上下文协议（MCP）服务器，为大型语言模型（LLM）提供与 Solana 网络交互的链上工具。

[English](./README.en.md)

## 功能

- **账户管理**：创建钱包、查询 SOL 和 SPL 代币余额、获取账户信息。
- **交易监控**：查询单笔交易详情。
- **市场数据**：获取代币的实时价格。
- **DeFi 集成**：使用 Jupiter 聚合器进行代币交换。

## 安装

1.  **克隆仓库**
    ```bash
    git clone <repository_url>
    ```

2.  **设置环境**
    ```bash
    chmod +x setup.sh
    ./setup.sh
    ```
    该命令将创建一个虚拟环境，安装依赖项，并设置您的 `.env` 文件。

3.  **配置环境变量**

    您的 `.env` 文件将根据 `.env.example` 创建。您可以添加您的 Solana RPC URL 和私钥（如果需要执行签名操作，当前未实现）。

    ```env
    SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
    SOLANA_PRIVATE_KEY=
    DEFAULT_COMMITMENT=confirmed
    DEFAULT_NETWORK=mainnet
    ```

## 使用方法

使用运行脚本启动 MCP 服务器：

```bash
chmod +x run.sh
./run.sh
```

要查看工具使用示例，请运行：

```bash
./run.sh examples
```

## 可用工具

- `get_balance`：获取指定地址的 SOL 余额。
- `get_token_balance`：获取指定地址的特定 SPL 代币余额。
- `create_wallet`：生成一个新的 Solana 钱包（密钥对）。
- `get_transaction`：通过交易签名获取特定交易的详细信息。
- `get_token_price`：从外部 API 获取代币（例如 SOL、USDC）的当前价格。
- `get_account_info`：获取有关 Solana 账户的详细底层信息。
- `swap_tokens`：从 Jupiter 聚合器获取交换交易，以将一种代币兑换为另一种代币。

## 在 IDE 中使用（例如 Cursor）

要将此 MCP 服务器与像 Cursor 这样的人工智能驱动的 IDE 一起使用，您可以将其配置为自定义工具提供程序。

1.  **启动服务器**：首先，确保 MCP 服务器正在运行：
    ```bash
    ./run.sh
    ```

2.  **在 Cursor 中配置**：
    - 前往 `文件 > 首选项 > 设置`。
    - 搜索 `mcp` 或 `模型上下文协议`。
    - 在 `自定义 MCP 服务器` 部分，添加一个新条目：
      - **名称**：`Solana Tools`（或任何您喜欢的名称）
      - **地址**：`stdio`（因为此服务器通过标准输入/输出进行通信）
      - **命令**：`[项目路径]/run.sh`（使用 `run.sh` 的绝对路径）

3.  **使用工具**：配置完成后，您可以在与 AI 的聊天中调用这些工具。例如：
    ```
    @Solana Tools get_balance --address <some_solana_address>
    ```

    AI 将使用该服务器执行命令，并直接在聊天中返回结果。

## 安全性

- 切勿将私钥提交到版本控制中
- 使用环境变量配置敏感信息
- 在主网操作前先在开发网进行测试
- 实现适当的错误处理和验证

## 许可证

MIT 许可证