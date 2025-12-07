"""Pytest configuration for PlayGodot E2E tests."""

import os
import sys
from pathlib import Path

import pytest_asyncio

# Add PlayGodot to path if not installed via pip
playgodot_path = os.environ.get("PLAYGODOT_PATH")
if playgodot_path:
    sys.path.insert(0, playgodot_path)
else:
    # Try common relative location for development
    dev_path = Path(__file__).parent.parent.parent.parent / "PlayGodot" / "python"
    if dev_path.exists():
        sys.path.insert(0, str(dev_path))

try:
    from playgodot import Godot
except ImportError:
    raise ImportError(
        "PlayGodot not found.\n\n"
        "Install it via pip:\n"
        "  pip install playgodot\n\n"
        "Or set PLAYGODOT_PATH:\n"
        "  export PLAYGODOT_PATH=/path/to/PlayGodot/python\n\n"
        "See: https://github.com/Randroids-Dojo/PlayGodot"
    )

GODOT_PROJECT = Path(__file__).parent.parent

# Require GODOT_PATH environment variable
GODOT_PATH = os.environ.get("GODOT_PATH")
if not GODOT_PATH:
    raise RuntimeError(
        "GODOT_PATH environment variable not set.\n\n"
        "PlayGodot requires a custom Godot build with automation support.\n\n"
        "Set the environment variable:\n"
        "  export GODOT_PATH=/path/to/godot-automation-fork\n\n"
        "Build from source:\n"
        "  git clone https://github.com/Randroids-Dojo/godot.git\n"
        "  cd godot && git checkout automation\n"
        "  scons platform=macos arch=arm64 target=editor -j8\n\n"
        "Or download pre-built binary:\n"
        "  https://github.com/Randroids-Dojo/godot/releases/tag/automation-latest"
    )


@pytest_asyncio.fixture
async def game():
    """Fixture that launches the game and provides a connected PlayGodot client.

    Uses Godot's native RemoteDebugger protocol for automation.
    Requires the custom Godot fork with automation support.
    """
    async with Godot.launch(
        str(GODOT_PROJECT),
        headless=True,
        timeout=15.0,
        verbose=True,
        godot_path=GODOT_PATH,
    ) as g:
        await g.wait_for_node("/root/Game")
        yield g
