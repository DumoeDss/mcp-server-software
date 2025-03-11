English | [中文](./README_ZH.md)

# Software MCP Server

A Model Context Protocol server that provides software management capabilities for your computer. This server enables LLMs to get a list of installed software, open applications, and close running programs, with support for multiple operating systems (Windows, macOS, Linux).

## Available Tools

- `get_software_list_tool` - Get a list of installed software on the computer.
  - Returns a list of software names.

- `open_software` - Open software by name.
  - Required arguments:
    - `name` (string): The name of the software to open.

- `close_software` - Close running software by name (currently Windows-only).
  - Required arguments:
    - `name` (string): The name of the software to close.

## Installation

### Using uv (recommended)

When using [`uv`](https://docs.astral.sh/uv/), no specific installation is needed. We can use [`uvx`](https://docs.astral.sh/uv/guides/tools/) to directly run *mcp-software-server*.

### Using PIP

Alternatively, you can install dependencies via pip:

```bash
pip install mcp_server_software
```

## Configuration

### Configure for Claude.app

Add to your Claude settings:

<details>
<summary>Using uvx</summary>

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
<summary>Using uv</summary>

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
<summary>Using manual Python command</summary>

```json
"mcpServers": {
  "software_manager": {
    "command": "python",
    "args": ["path/to/mcp_server_software.py"]
  }
}
```
</details>


## Platform Support

- **Windows**: Full functionality (software listing, opening, closing)
- **macOS**: Software listing and opening only
- **Linux**: Software listing and opening only

## Example Interactions

1. Get software list:
```json
{
  "name": "get_software_list_tool",
  "arguments": {}
}
```
Response:
```json
[
  "Chrome",
  "Firefox",
  "Visual Studio Code",
  "Notepad++",
  ...
]
```

2. Open software:
```json
{
  "name": "open_software",
  "arguments": {
    "name": "Chrome"
  }
}
```
Response:
```json
"Opened Chrome"
```

3. Close software (Windows only):
```json
{
  "name": "close_software",
  "arguments": {
    "name": "Chrome"
  }
}
```
Response:
```json
"Closed Chrome"
```

## Debugging

You can use the MCP inspector to debug the server:

```bash
npx @modelcontextprotocol/inspector python mcp_server_software.py
```

## Examples of Questions for Claude/AI

1. "What applications do I have installed on my computer?"
2. "Can you open Notepad for me?"
3. "Please close Chrome browser"
4. "Show me all available software on my system"

## How It Works

The server creates and maintains a JSON file (`software_list.json`) that maps software names to their executable paths. On Windows, it scans Start Menu shortcuts, on macOS it looks in the Applications folder, and on Linux it examines desktop entry files.

You can manually edit this JSON file to add custom software entries:

```json
{
  "CustomApp": "C:\\Path\\To\\Custom\\App.exe"
}
```

## Requirements

- Python 3.7+
- psutil
- mcp
- pywin32 (Windows only)

## Contributing

Contributions are welcome to help expand and improve mcp-software-server. Consider adding support for:

- Better closing support on macOS/Linux
- Enhanced software detection
- Software installation/uninstallation capabilities
- Additional software management features

## License

This project is licensed under the MIT License. See the LICENSE file for details.