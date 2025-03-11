import sys
import json
import subprocess
import psutil
from pathlib import Path
import getpass
import glob
from typing import List
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("software_manager")

SOFTWARE_JSON_PATH = "software_list.json"


def get_software_list_windows() -> dict[str, str]:
    software_dict = {}
    start_menu_paths = [
        Path("C:\\ProgramData\\Microsoft\\Windows\\Start Menu"),
        Path(f"C:\\Users\\{getpass.getuser()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu")
    ]
    for start_menu in start_menu_paths:
        for file in start_menu.rglob("*.lnk"):
            try:
                import win32com.client
                shell = win32com.client.Dispatch("WScript.Shell")
                shortcut = shell.CreateShortCut(str(file))
                target_path = shortcut.TargetPath
                if Path(target_path).exists() and Path(target_path).is_file():
                    software_name = file.stem
                    software_dict[software_name] = target_path
            except Exception as e:
                print(f"Error processing {file}: {e}")
    return software_dict


def get_software_list_linux() -> dict[str, str]:
    software_dict = {}
    for file in glob.glob("/usr/share/applications/*.desktop"):
        try:
            with open(file, 'r') as f:
                content = f.read()
                name = None
                exec_cmd = None
                for line in content.splitlines():
                    if line.startswith("Name="):
                        name = line[5:].strip()
                    elif line.startswith("Exec="):
                        exec_cmd = line[5:].strip()
                if name and exec_cmd:
                    software_dict[name] = exec_cmd
        except Exception as e:
            print(f"Error processing {file}: {e}")
    return software_dict


def get_software_list_mac() -> dict[str, str]:
    software_dict = {}
    applications_dir = Path("/Applications")
    for app in applications_dir.glob("*.app"):
        software_name = app.stem
        software_dict[software_name] = str(app)
    return software_dict


def get_software_list() -> dict[str, str]:
    if sys.platform == 'win32':
        try:
            return get_software_list_windows()
        except ImportError:
            print("pywin32 library not installed. Cannot retrieve software list on Windows.")
            return {}
    elif sys.platform == 'linux':
        return get_software_list_linux()
    elif sys.platform == 'darwin':
        return get_software_list_mac()
    else:
        print("Unsupported platform")
        return {}


def save_software_list(software_dict: dict[str, str]):
    with open(SOFTWARE_JSON_PATH, 'w') as f:
        json.dump(software_dict, f, ensure_ascii=False)


def load_software_list() -> dict[str, str]:
    try:
        with open(SOFTWARE_JSON_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


@mcp.tool()
async def get_software_list_tool() -> List[str]:
    """Get a list of installed software on the computer

    Returns:
        A list of software names
    """
    software_dict = get_software_list()
    save_software_list(software_dict)
    return list(software_dict.keys())


@mcp.tool()
async def open_software(name: str) -> str:
    """Open software by name

    Args:
        name: The name of the software to open
    """
    software_dict = load_software_list()
    if name not in software_dict:
        return f"Software '{name}' not found."

    path_or_cmd = software_dict[name]

    if sys.platform == 'win32':
        try:
            subprocess.Popen(path_or_cmd)
            return f"Opened {name}"
        except Exception as e:
            return f"Failed to open {name}: {e}"
    elif sys.platform == 'linux':
        try:
            subprocess.Popen(path_or_cmd, shell=True)
            return f"Opened {name}"
        except Exception as e:
            return f"Failed to open {name}: {e}"
    elif sys.platform == 'darwin':
        try:
            subprocess.Popen(["open", path_or_cmd])
            return f"Opened {name}"
        except Exception as e:
            return f"Failed to open {name}: {e}"
    else:
        return "Unsupported platform"


@mcp.tool()
async def close_software(name: str) -> str:
    """Close software by name

    Args:
        name: The name of the software to close
    """
    if sys.platform != 'win32':
        return "Closing operation not supported on this platform"

    software_dict = load_software_list()
    if name not in software_dict:
        return f"Software '{name}' not found."

    path = software_dict[name]

    for proc in psutil.process_iter(['pid', 'exe']):
        if proc.info['exe'] == path:
            try:
                proc.terminate()
                return f"Closed {name}"
            except Exception as e:
                return f"Failed to close {name}: {e}"
    return f"{name} is not running"


if __name__ == "__main__":
    get_software_list_tool()
    mcp.run(transport='stdio')