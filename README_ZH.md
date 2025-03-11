[English](./README.md) | 中文

# 软件管理 MCP 服务器

一个基于模型上下文协议(Model Context Protocol)的服务器，为您的计算机提供软件管理功能。该服务器使大型语言模型(LLM)能够获取已安装软件列表、打开应用程序和关闭运行中的程序，并支持多种操作系统(Windows、macOS、Linux)。

## 可用工具

- `get_software_list_tool` - 获取计算机上已安装的软件列表。
  - 返回软件名称列表。

- `open_software` - 通过名称打开软件。
  - 必需参数：
    - `name` (字符串)：要打开的软件名称。

- `close_software` - 通过名称关闭正在运行的软件(目前仅支持Windows)。
  - 必需参数：
    - `name` (字符串)：要关闭的软件名称。

## 安装

### 使用 uv (推荐)

当使用 [`uv`](https://docs.astral.sh/uv/) 时，无需特定安装。我们可以使用 [`uvx`](https://docs.astral.sh/uv/guides/tools/) 直接运行 *mcp-software-server*。

### 使用 PIP

或者，您可以通过pip安装依赖：

```bash
pip install mcp_server_software
```

## 配置

### 为 Claude.app 配置

在Claude设置中添加：

<details>
<summary>使用 uvx</summary>

```json
"mcpServers": {
  "software_manager": {
    "command": "uvx",
    "args": ["mcp-server-software"]
  }
}
```
</details>

<details>
<summary>使用 uv</summary>

```json
"mcpServers": {
  "software_manager": {
        "command": "uv",
        "args": [
          "--directory",
          "{path/to/mcp_server_software.py}",
          "run",
          "mcp_server_software.py"
        ],
        "env": {},
        "disabled": false,
        "alwaysAllow": []
    }
}
```
</details>

<details>
<summary>使用手动Python命令</summary>

```json
"mcpServers": {
  "software_manager": {
    "command": "python",
    "args": ["path/to/mcp_server_software.py"]
  }
}
```
</details>


## 平台支持

- **Windows**: 完整功能支持(软件列表、打开、关闭)
- **macOS**: 仅支持软件列表和打开功能
- **Linux**: 仅支持软件列表和打开功能

## 交互示例

1. 获取软件列表:
```json
{
  "name": "get_software_list_tool",
  "arguments": {}
}
```
响应:
```json
[
  "Chrome",
  "Firefox",
  "Visual Studio Code",
  "Notepad++",
  ...
]
```

2. 打开软件:
```json
{
  "name": "open_software",
  "arguments": {
    "name": "Chrome"
  }
}
```
响应:
```json
"Opened Chrome"
```

3. 关闭软件(仅Windows):
```json
{
  "name": "close_software",
  "arguments": {
    "name": "Chrome"
  }
}
```
响应:
```json
"Closed Chrome"
```

## 调试

您可以使用MCP检查器来调试服务器:

```bash
npx @modelcontextprotocol/inspector python mcp_server_software.py
```

## 示例问题(向Claude/AI提问)

1. "我的计算机上安装了哪些应用程序?"
2. "你能帮我打开记事本吗?"
3. "请关闭Chrome浏览器"
4. "显示我系统上所有可用的软件"

## 工作原理

服务器创建并维护一个JSON文件(`software_list.json`)，该文件将软件名称映射到其可执行文件路径。在Windows上，它扫描开始菜单快捷方式；在macOS上，它查看应用程序文件夹；在Linux上，它检查桌面条目文件。

您可以手动编辑此JSON文件以添加自定义软件条目:

```json
{
  "CustomApp": "C:\\Path\\To\\Custom\\App.exe"
}
```

## 系统要求

- Python 3.7+
- psutil
- mcp
- pywin32 (仅Windows)

## 参与贡献

欢迎贡献，帮助扩展和改进mcp-software-server。可以考虑添加以下支持:

- 改进macOS/Linux上的关闭软件功能
- 增强软件检测能力
- 软件安装/卸载功能
- 其他软件管理功能

## 许可证

本项目采用MIT许可证。详情请参阅LICENSE文件。