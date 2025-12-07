"""Pytest configuration for tic-tac-toe PlayGodot tests."""

import sys
from pathlib import Path

import pytest
import pytest_asyncio

# Add the PlayGodot Python client to the path
playgodot_python = Path(__file__).parent.parent.parent.parent / "PlayGodot" / "python"
sys.path.insert(0, str(playgodot_python))

from playgodot import Godot

GODOT_PROJECT = Path(__file__).parent.parent
GODOT_FORK = Path(__file__).parent.parent.parent.parent / "godot" / "bin" / "godot.macos.editor.arm64"


@pytest_asyncio.fixture
async def game():
    """Fixture that launches the tic-tac-toe game and provides a connected client."""
    async with Godot.launch(
        str(GODOT_PROJECT),
        headless=True,
        timeout=15.0,
        verbose=True,
        godot_path=str(GODOT_FORK),
    ) as g:
        # Wait for the main scene to be ready
        await g.wait_for_node("/root/Game")
        yield g