#!/usr/bin/env python3
"""
PlayGodot interactive demo script.

Run all PlayGodot features against the tic-tac-toe game with verbose output.
Useful for manually testing or demonstrating the automation capabilities.

Usage:
    export GODOT_PATH=/path/to/godot-automation-fork
    python demo_playgodot.py [--headless] [--verbose]

Requires a custom Godot build with automation support.
"""

import asyncio
import os
import sys
from pathlib import Path

# Script is in example-project/tests/, project is parent directory
GODOT_PROJECT = Path(__file__).parent.parent
SCREENSHOT_DIR = Path(__file__).parent / "screenshots"


def header(title: str) -> None:
    """Print a section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


async def demo_node_interaction(game) -> None:
    """Demo node interaction features."""
    header("NODE INTERACTION")

    print("Testing get_node...")
    node = await game.get_node("/root/Game")
    print(f"  Got node: {node.name} (class: {node.class_name})")

    print("\nTesting node_exists...")
    exists = await game.node_exists("/root/Game")
    print(f"  /root/Game exists: {exists}")
    not_exists = await game.node_exists("/root/NonExistent")
    print(f"  /root/NonExistent exists: {not_exists}")

    print("\nTesting get_property...")
    visible = await game.get_property("/root/Game", "visible")
    print(f"  /root/Game visible: {visible}")

    print("\nTesting call method...")
    board_state = await game.call("/root/Game", "get_board_state")
    print(f"  Board state: {board_state}")
    current_player = await game.call("/root/Game", "get_current_player")
    print(f"  Current player: {current_player}")


async def demo_query_nodes(game) -> None:
    """Demo node query features."""
    header("NODE QUERIES")

    print("Testing query_nodes...")
    cells = await game.query_nodes("*Cell*")
    print(f"  Found {len(cells)} nodes matching '*Cell*':")
    for cell in cells[:5]:
        print(f"    - {cell}")
    if len(cells) > 5:
        print(f"    ... and {len(cells) - 5} more")

    print("\nTesting count_nodes...")
    label_count = await game.count_nodes("*Label*")
    print(f"  Labels matching '*Label*': {label_count}")


async def demo_input_simulation(game) -> None:
    """Demo input simulation features."""
    header("INPUT SIMULATION")

    print("Testing click (making a move on Cell0)...")
    await game.click("/root/Game/VBoxContainer/GameBoard/GridContainer/Cell0")
    await asyncio.sleep(0.2)
    board = await game.call("/root/Game", "get_board_state")
    print(f"  Board after click: {board}")

    print("\nTesting press_key (R to restart)...")
    await game.press_key("r")
    await asyncio.sleep(0.2)
    board = await game.call("/root/Game", "get_board_state")
    print(f"  Board after restart: {board}")


async def demo_screenshots(game) -> None:
    """Demo screenshot features."""
    header("SCREENSHOTS")

    SCREENSHOT_DIR.mkdir(exist_ok=True)

    print("Making some moves for visual variety...")
    await game.call("/root/Game", "make_move", [0])
    await game.call("/root/Game", "make_move", [4])
    await game.call("/root/Game", "make_move", [8])
    await asyncio.sleep(0.3)

    print("\nTesting screenshot (save to file)...")
    path1 = SCREENSHOT_DIR / "game_state.png"
    await game.screenshot(str(path1))
    print(f"  Saved to: {path1} ({path1.stat().st_size} bytes)")

    print("\nTesting screenshot (return bytes)...")
    png_data = await game.screenshot()
    print(f"  Got {len(png_data)} bytes of PNG data")
    print(f"  PNG header: {png_data[:8]}")


async def demo_scene_management(game) -> None:
    """Demo scene management features."""
    header("SCENE MANAGEMENT")

    print("Testing get_current_scene...")
    scene = await game.get_current_scene()
    print(f"  Current scene: {scene}")

    await game.call("/root/Game", "make_move", [4])

    print("\nTesting reload_scene...")
    await game.reload_scene()
    await asyncio.sleep(0.5)
    await game.wait_for_node("/root/Game")
    board = await game.call("/root/Game", "get_board_state")
    print(f"  Board after reload: {board}")


async def demo_game_state(game) -> None:
    """Demo game state control features."""
    header("GAME STATE CONTROL")

    print("Testing pause...")
    await game.pause()
    is_paused = await game.is_paused()
    print(f"  Is paused: {is_paused}")

    print("\nTesting unpause...")
    await game.unpause()
    is_paused = await game.is_paused()
    print(f"  Is paused: {is_paused}")

    print("\nTesting set_time_scale (0.5 = slow motion)...")
    await game.set_time_scale(0.5)
    scale = await game.get_time_scale()
    print(f"  Time scale: {scale}")

    print("\nTesting set_time_scale (2.0 = fast forward)...")
    await game.set_time_scale(2.0)
    scale = await game.get_time_scale()
    print(f"  Time scale: {scale}")

    print("\nResetting time scale to 1.0...")
    await game.set_time_scale(1.0)


async def demo_waiting(game) -> None:
    """Demo waiting features."""
    header("WAITING FEATURES")

    print("Testing wait_for_node (existing node)...")
    node = await game.wait_for_node("/root/Game", timeout=2.0)
    print(f"  Found node: {node.name}")

    print("\nTesting wait_for_visible...")
    await game.wait_for_visible("/root/Game/VBoxContainer/StatusLabel", timeout=2.0)
    print("  StatusLabel is visible")

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

    print("Reloading scene for fresh game...")
    await game.reload_scene()
    await asyncio.sleep(0.3)
    await game.wait_for_node("/root/Game")

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

    is_active = await game.call("/root/Game", "is_game_active")
    winner = await game.call("/root/Game", "get_winner")
    print(f"\n  Game active: {is_active}")
    print(f"  Winner: {winner}")

    SCREENSHOT_DIR.mkdir(exist_ok=True)
    final_path = SCREENSHOT_DIR / "game_won.png"
    await game.screenshot(str(final_path))
    print(f"\n  Final screenshot saved to: {final_path}")


async def main():
    """Run all demos."""
    # Import PlayGodot
    try:
        from playgodot import Godot
    except ImportError:
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
    asyncio.run(main())
