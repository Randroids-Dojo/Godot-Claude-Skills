#!/usr/bin/env python3
"""
PlayGodot E2E tests and demo script for the tic-tac-toe game.

This file serves dual purposes:
1. Pytest tests: Run with `pytest tests/test_playgodot_demo.py -v`
2. Standalone demo: Run with `python tests/test_playgodot_demo.py`

Requires a custom Godot build with automation support.

Configuration:
    export GODOT_PATH=/path/to/godot-automation-fork
"""

import asyncio
import os
import sys
from pathlib import Path

import pytest

# Script is in example-project/tests/, project is parent directory
GODOT_PROJECT = Path(__file__).parent.parent
SCREENSHOT_DIR = Path(__file__).parent / "screenshots"


def header(title: str) -> None:
    """Print a section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


# =============================================================================
# Demo Functions (used by both pytest tests and standalone script)
# =============================================================================

async def demo_node_interaction(game) -> None:
    """Demo node interaction features."""
    header("NODE INTERACTION")

    # get_node
    print("Testing get_node...")
    node = await game.get_node("/root/Game")
    print(f"  Got node: {node.name} (class: {node.class_name})")
    assert node is not None
    assert node.name == "Game"

    # node_exists
    print("\nTesting node_exists...")
    exists = await game.node_exists("/root/Game")
    print(f"  /root/Game exists: {exists}")
    assert exists is True

    not_exists = await game.node_exists("/root/NonExistent")
    print(f"  /root/NonExistent exists: {not_exists}")
    assert not_exists is False

    # get_property
    print("\nTesting get_property...")
    visible = await game.get_property("/root/Game", "visible")
    print(f"  /root/Game visible: {visible}")
    assert visible is True

    # call method
    print("\nTesting call method...")
    board_state = await game.call("/root/Game", "get_board_state")
    print(f"  Board state: {board_state}")
    assert board_state == ["", "", "", "", "", "", "", "", ""]

    current_player = await game.call("/root/Game", "get_current_player")
    print(f"  Current player: {current_player}")
    assert current_player == "X"


async def demo_query_nodes(game) -> None:
    """Demo node query features."""
    header("NODE QUERIES")

    # query_nodes
    print("Testing query_nodes...")
    cells = await game.query_nodes("*Cell*")
    print(f"  Found {len(cells)} nodes matching '*Cell*':")
    for cell in cells[:5]:
        print(f"    - {cell}")
    if len(cells) > 5:
        print(f"    ... and {len(cells) - 5} more")
    assert len(cells) >= 9

    # count_nodes
    print("\nTesting count_nodes...")
    label_count = await game.count_nodes("*Label*")
    print(f"  Labels matching '*Label*': {label_count}")
    assert label_count >= 1


async def demo_input_simulation(game) -> None:
    """Demo input simulation features."""
    header("INPUT SIMULATION")

    # click on cell
    print("Testing click (making a move on Cell0)...")
    await game.click("/root/Game/VBoxContainer/GameBoard/GridContainer/Cell0")
    await asyncio.sleep(0.2)

    board = await game.call("/root/Game", "get_board_state")
    print(f"  Board after click: {board}")
    assert board[0] == "X"

    # press_key (R to restart)
    print("\nTesting press_key (R to restart)...")
    await game.press_key("r")
    await asyncio.sleep(0.2)

    board = await game.call("/root/Game", "get_board_state")
    print(f"  Board after restart: {board}")
    assert board == ["", "", "", "", "", "", "", "", ""]


async def demo_screenshots(game) -> None:
    """Demo screenshot features."""
    header("SCREENSHOTS")

    SCREENSHOT_DIR.mkdir(exist_ok=True)

    # Make some moves first
    print("Making some moves for visual variety...")
    await game.call("/root/Game", "make_move", [0])
    await game.call("/root/Game", "make_move", [4])
    await game.call("/root/Game", "make_move", [8])
    await asyncio.sleep(0.3)

    # screenshot to file
    print("\nTesting screenshot (save to file)...")
    path1 = SCREENSHOT_DIR / "game_state.png"
    await game.screenshot(str(path1))
    print(f"  Saved to: {path1} ({path1.stat().st_size} bytes)")
    assert path1.exists()
    assert path1.stat().st_size > 0

    # screenshot returns bytes
    print("\nTesting screenshot (return bytes)...")
    png_data = await game.screenshot()
    print(f"  Got {len(png_data)} bytes of PNG data")
    print(f"  PNG header: {png_data[:8]}")
    assert isinstance(png_data, bytes)
    assert png_data[:8] == b'\x89PNG\r\n\x1a\n'


async def demo_scene_management(game) -> None:
    """Demo scene management features."""
    header("SCENE MANAGEMENT")

    # get_current_scene
    print("Testing get_current_scene...")
    scene = await game.get_current_scene()
    print(f"  Current scene: {scene}")
    assert "game" in scene.lower() or "main" in scene.lower()

    # Make a move to verify reload works
    await game.call("/root/Game", "make_move", [4])

    # reload_scene
    print("\nTesting reload_scene...")
    await game.reload_scene()
    await asyncio.sleep(0.5)
    await game.wait_for_node("/root/Game")

    board = await game.call("/root/Game", "get_board_state")
    print(f"  Board after reload: {board}")
    assert board == ["", "", "", "", "", "", "", "", ""]


async def demo_game_state(game) -> None:
    """Demo game state control features."""
    header("GAME STATE CONTROL")

    # pause/unpause
    print("Testing pause...")
    await game.pause()
    is_paused = await game.is_paused()
    print(f"  Is paused: {is_paused}")
    assert is_paused is True

    print("\nTesting unpause...")
    await game.unpause()
    is_paused = await game.is_paused()
    print(f"  Is paused: {is_paused}")
    assert is_paused is False

    # time_scale
    print("\nTesting set_time_scale (0.5 = slow motion)...")
    await game.set_time_scale(0.5)
    scale = await game.get_time_scale()
    print(f"  Time scale: {scale}")
    assert scale == 0.5

    print("\nTesting set_time_scale (2.0 = fast forward)...")
    await game.set_time_scale(2.0)
    scale = await game.get_time_scale()
    print(f"  Time scale: {scale}")
    assert scale == 2.0

    print("\nResetting time scale to 1.0...")
    await game.set_time_scale(1.0)
    scale = await game.get_time_scale()
    print(f"  Time scale: {scale}")
    assert scale == 1.0


async def demo_waiting(game) -> None:
    """Demo waiting features."""
    header("WAITING FEATURES")

    # wait_for_node
    print("Testing wait_for_node (existing node)...")
    node = await game.wait_for_node("/root/Game", timeout=2.0)
    print(f"  Found node: {node.name}")
    assert node.name == "Game"

    # wait_for_visible
    print("\nTesting wait_for_visible...")
    await game.wait_for_visible("/root/Game/VBoxContainer/StatusLabel", timeout=2.0)
    print("  StatusLabel is visible")

    # wait_for with custom condition
    print("\nTesting wait_for (custom condition: board is empty)...")
    await game.reload_scene()
    await asyncio.sleep(0.3)

    async def board_is_empty():
        board = await game.call("/root/Game", "get_board_state")
        return board == ["", "", "", "", "", "", "", "", ""]

    await game.wait_for(board_is_empty, timeout=5.0)
    print("  Board is empty!")


async def demo_game_play(game) -> None:
    """Demo a complete game play sequence."""
    header("COMPLETE GAME PLAY")

    # Reset the game
    print("Reloading scene for fresh game...")
    await game.reload_scene()
    await asyncio.sleep(0.3)
    await game.wait_for_node("/root/Game")

    # Play a winning game for X
    print("\nPlaying a winning game (X wins with top row)...")
    moves = [
        (0, "X"),  # X top-left
        (3, "O"),  # O middle-left
        (1, "X"),  # X top-center
        (4, "O"),  # O center
        (2, "X"),  # X top-right - WIN!
    ]

    for pos, player in moves:
        await game.call("/root/Game", "make_move", [pos])
        board = await game.call("/root/Game", "get_board_state")
        print(f"  {player} plays at {pos}: {board}")
        await asyncio.sleep(0.2)

    # Check game state
    is_active = await game.call("/root/Game", "is_game_active")
    winner = await game.call("/root/Game", "get_winner")
    print(f"\n  Game active: {is_active}")
    print(f"  Winner: {winner}")
    assert is_active is False
    assert winner == "X"

    # Take final screenshot
    SCREENSHOT_DIR.mkdir(exist_ok=True)
    final_path = SCREENSHOT_DIR / "game_won.png"
    await game.screenshot(str(final_path))
    print(f"\n  Final screenshot saved to: {final_path}")


# =============================================================================
# Pytest Tests (wrap the demo functions)
# =============================================================================

@pytest.mark.asyncio
async def test_node_interaction(game):
    """Test node interaction features."""
    await demo_node_interaction(game)


@pytest.mark.asyncio
async def test_query_nodes(game):
    """Test node query features."""
    await demo_query_nodes(game)


@pytest.mark.asyncio
async def test_input_simulation(game):
    """Test input simulation features."""
    await demo_input_simulation(game)


@pytest.mark.asyncio
async def test_screenshots(game):
    """Test screenshot features."""
    await demo_screenshots(game)


@pytest.mark.asyncio
async def test_scene_management(game):
    """Test scene management features."""
    await demo_scene_management(game)


@pytest.mark.asyncio
async def test_game_state(game):
    """Test game state control features."""
    await demo_game_state(game)


@pytest.mark.asyncio
async def test_waiting(game):
    """Test waiting features."""
    await demo_waiting(game)


@pytest.mark.asyncio
async def test_game_play(game):
    """Test a complete game play sequence with win detection."""
    await demo_game_play(game)


# =============================================================================
# Standalone Script Mode
# =============================================================================

async def run_all_demos():
    """Run all demos as a standalone script."""
    # Import here to avoid issues when running as pytest
    try:
        from playgodot import Godot
    except ImportError:
        # Try adding PlayGodot to path
        playgodot_path = os.environ.get("PLAYGODOT_PATH")
        if playgodot_path:
            sys.path.insert(0, playgodot_path)
            from playgodot import Godot
        else:
            print("ERROR: PlayGodot not found.")
            print("Install via pip or set PLAYGODOT_PATH")
            sys.exit(1)

    godot_path = os.environ.get("GODOT_PATH")
    if not godot_path:
        print("ERROR: GODOT_PATH environment variable not set.")
        print("Set it to your custom Godot binary with automation support.")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("  PlayGodot Demo Script")
    print("=" * 60)
    print(f"\nUsing Godot: {godot_path}")
    print(f"Project: {GODOT_PROJECT}")

    async with Godot.launch(
        str(GODOT_PROJECT),
        headless="--headless" in sys.argv,
        timeout=15.0,
        verbose="--verbose" in sys.argv,
        godot_path=godot_path,
    ) as game:
        print("\nGame launched, waiting for main scene...")
        await game.wait_for_node("/root/Game")
        print("Game ready!")
        await asyncio.sleep(0.5)

        await demo_node_interaction(game)
        await demo_query_nodes(game)
        await demo_input_simulation(game)
        await demo_screenshots(game)
        await demo_scene_management(game)
        await demo_game_state(game)
        await demo_waiting(game)
        await demo_game_play(game)

        header("ALL DEMOS COMPLETE")
        print("All PlayGodot features demonstrated successfully!")
        print(f"\nScreenshots saved to: {SCREENSHOT_DIR}/")

        await asyncio.sleep(2)


if __name__ == "__main__":
    asyncio.run(run_all_demos())
