from cx_Freeze import setup, Executable
import sys
import os

# Script to build a Windows executable for compressor.py using cx_Freeze.
# Features:
# - include_msvcr: copies MSVC runtime redistributable files into the build
# - optional icon: pass --icon path/to/icon.ico on the command line or set
#   the environment variable CXFREEZE_ICON to point to an .ico file

APP_NAME = "Compressor de Imagens"
MAIN_SCRIPT = "compressor.py"

# Determine icon: look for a local file named 'app.ico' in the project root
# (user requested the icon file to be simply a local file called app.ico).
# If not present, fall back to CXFREEZE_ICON env var.
DEFAULT_ICON_NAME = "app.ico"

def find_icon():
    # Prefer a local app.ico in the same folder as setup.py
    local_icon = os.path.join(os.path.dirname(__file__), DEFAULT_ICON_NAME)
    if os.path.isfile(local_icon):
        return local_icon
    # Fallback to environment variable if set
    env_icon = os.environ.get("CXFREEZE_ICON")
    if env_icon and os.path.isfile(env_icon):
        return env_icon
    return None

icon_path = find_icon()

# build_exe options: include_msvcr ensures required MSVC runtime files are
# copied into the build on Windows. include_files can be used to bundle the
# icon alongside the exe if desired.
build_exe_options = {
    "packages": [],
    "excludes": [],
    "include_msvcr": True,
    # Include the local icon if present so it is available in the build
    # (cx_Freeze will copy it into the build directory).
    # We'll append to include_files below if icon_path exists.
}

# Ensure include_files exists and add icon if found
if icon_path:
    include_files = build_exe_options.get("include_files") or []
    # Add the icon using its original name so it appears as 'app.ico' in the build
    include_files.append((icon_path, os.path.basename(icon_path)))
    build_exe_options["include_files"] = include_files

executables = [
    Executable(
        script=MAIN_SCRIPT,
        base="Win32GUI" if sys.platform == "win32" else None,
        target_name="compressor.exe" if sys.platform == "win32" else None,
        icon=icon_path,
    )
]

setup(
    name=APP_NAME,
    version="1.0",
    description="Aplicativo para compressão de imagens",
    options={"build_exe": build_exe_options},
    executables=executables,
)
