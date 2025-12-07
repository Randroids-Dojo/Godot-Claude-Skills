#!/usr/bin/env python3
"""
Test all PlayGodot native debugger features with the tic-tac-toe game.

This script demonstrates how to use PlayGodot to automate and test a Godot game
from Python. It requires a custom Godot build with automation support.

Configuration:
    Set the GODOT_PATH environment variable to your custom Godot binary:
        export GODOT_PATH=/path/to/godot/bin/godot.macos.editor.arm64

    Or pass it as a command-line argument:
        python run_game_demo.py --godot-path /path/to/godot

    If PlayGodot is not installed via pip, set PLAYGODOT_PATH:
        export PLAYGODOT_PATH=/path/to/PlayGodot/python
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path


def setup_playgodot_path():
    """Add PlayGodot to sys.path if not installed via pip."""
    # Check if playgodot is already importable
    try:
        import playgodot
        return
    except ImportError:
        pass

    # Require PLAYGODOT_PATH environment variable
    playgodot_path = os.environ.get("PLAYGODOT_PATH")
    if not playgodot_path:
        print("ERROR: PlayGodot not found.")
        print("")
        print("Either install it via pip:")
        print("  pip install playgodot")
        print("")
        print("Or set the PLAYGODOT_PATH environment variable:")
        print("  export PLAYGODOT_PATH=/path/to/PlayGodot/python")
        print("")
        print("See: https://github.com/Randroids-Dojo/PlayGodot")
        sys.exit(1)

    sys.path.insert(0, playgodot_path)


def get_godot_path(args_godot_path: str | None) -> str:
    """Get the path to the Godot binary."""
    # Command-line argument takes priority
    if args_godot_path:
        return args_godot_path

    # Require GODOT_PATH environment variable
    env_path = os.environ.get("GODOT_PATH")
    if not env_path:
        print("ERROR: GODOT_PATH environment variable not set.")
        print("")
        print("PlayGodot requires a custom Godot build with automation support.")
        print("")
        print("Set the environment variable to your custom Godot binary:")
        print("  export GODOT_PATH=/path/to/godot/bin/godot.macos.editor.arm64")
        print("")
        print("Or pass it as a command-line argument:")
        print("  python run_game_demo.py --godot-path /path/to/godot")
        print("")
        print("To build the custom Godot:")
        print("  git clone https://github.com/Randroids-Dojo/godot.git")
        print("  cd godot && git checkout automation")
        print("  scons platform=macos arch=arm64 target=editor -j8")
        sys.exit(1)

    return env_path


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Test PlayGodot native debugger features",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        "--godot-path",
        help="Path to the custom Godot binary with automation support"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run in headless mode (no window)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output from PlayGodot"
    )
    return parser.parse_args()


# Setup paths before importing playgodot
setup_playgodot_path()

from playgodot import Godot

GODOT_PROJECT = Path(__file__).parent / "example-project"
SCREENSHOT_DIR = Path(__file__).parent / "screenshots"


def header(title: str) -> None:
    """Print a section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


async def test_node_interaction(game: Godot) -> None:
    """Test node interaction features."""
    header("NODE INTERACTION")

    # get_node
    print("Testing get_node...")
    node = await game.get_node("/root/Game")
    print(f"  Got node: {node.name} (class: {node.class_name})")

    # node_exists
    print("\nTesting node_exists...")
    exists = await game.node_exists("/root/Game")
    print(f"  /root/Game exists: {exists}")
    not_exists = await game.node_exists("/root/NonExistent")
    print(f"  /root/NonExistent exists: {not_exists}")

    # get_property
    print("\nTesting get_property...")
    visible = await game.get_property("/root/Game", "visible")
    print(f"  /root/Game visible: {visible}")

    # call method
    print("\nTesting call method...")
    board_state = await game.call("/root/Game", "get_board_state")
    print(f"  Board state: {board_state}")

    current_player = await game.call("/root/Game", "get_current_player")
    print(f"  Current player: {current_player}")


async def test_query_nodes(game: Godot) -> None:
    """Test node query features."""
    header("NODE QUERIES")

    # query_nodes
    print("Testing query_nodes...")
    cells = await game.query_nodes("*Cell*")
    print(f"  Found {len(cells)} nodes matching '*Cell*':")
    for cell in cells[:5]:  # Show first 5
        print(f"    - {cell}")
    if len(cells) > 5:
        print(f"    ... and {len(cells) - 5} more")

    # count_nodes
    print("\nTesting count_nodes...")
    button_count = await game.count_nodes("*Button*")
    print(f"  Buttons matching '*Button*': {button_count}")

    label_count = await game.count_nodes("*Label*")
    print(f"  Labels matching '*Label*': {label_count}")


async def test_input_simulation(game: Godot) -> None:
    """Test input simulation features."""
    header("INPUT SIMULATION")

    # click on cell
    print("Testing click (making a move on Cell0)...")
    await game.click("/root/Game/VBoxContainer/GameBoard/GridContainer/Cell0")
    await asyncio.sleep(0.2)

    board = await game.call("/root/Game", "get_board_state")
    print(f"  Board after click: {board}")

    # click by coordinates
    print("\nTesting click by coordinates (Cell8 at ~370,525)...")
    await game.click(370, 525)
    await asyncio.sleep(0.2)

    board = await game.call("/root/Game", "get_board_state")
    print(f"  Board after coordinate click: {board}")

    # press_key (R to restart)
    print("\nTesting press_key (R to restart)...")
    await game.press_key("r")
    await asyncio.sleep(0.2)

    board = await game.call("/root/Game", "get_board_state")
    print(f"  Board after restart: {board}")


async def test_screenshots(game: Godot) -> None:
    """Test screenshot features."""
    header("SCREENSHOTS")

    SCREENSHOT_DIR.mkdir(exist_ok=True)

    # Make some moves first
    print("Making some moves for visual variety...")
    await game.call("/root/Game", "make_move", [0])  # X
    await game.call("/root/Game", "make_move", [4])  # O
    await game.call("/root/Game", "make_move", [8])  # X
    await asyncio.sleep(0.3)

    # screenshot to file
    print("\nTesting screenshot (save to file)...")
    path1 = SCREENSHOT_DIR / "game_state.png"
    await game.screenshot(str(path1))
    print(f"  Saved to: {path1} ({path1.stat().st_size} bytes)")

    # screenshot returns bytes
    print("\nTesting screenshot (return bytes)...")
    png_data = await game.screenshot()
    print(f"  Got {len(png_data)} bytes of PNG data")
    print(f"  PNG header: {png_data[:8]}")

    # Save the bytes manually
    path2 = SCREENSHOT_DIR / "game_state_bytes.png"
    path2.write_bytes(png_data)
    print(f"  Manually saved to: {path2}")


async def test_scene_management(game: Godot) -> None:
    """Test scene management features."""
    header("SCENE MANAGEMENT")

    # get_current_scene
    print("Testing get_current_scene...")
    scene = await game.get_current_scene()
    print(f"  Current scene: {scene}")

    # reload_scene
    print("\nTesting reload_scene...")
    await game.reload_scene()
    await asyncio.sleep(0.5)
    await game.wait_for_node("/root/Game")

    board = await game.call("/root/Game", "get_board_state")
    print(f"  Board after reload: {board}")

    scene = await game.get_current_scene()
    print(f"  Scene after reload: {scene}")


async def test_game_state(game: Godot) -> None:
    """Test game state control features."""
    header("GAME STATE CONTROL")

    # pause/unpause
    print("Testing pause...")
    await game.pause()
    is_paused = await game.is_paused()
    print(f"  Is paused: {is_paused}")

    print("\nTesting unpause...")
    await game.unpause()
    is_paused = await game.is_paused()
    print(f"  Is paused: {is_paused}")

    # time_scale
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
    scale = await game.get_time_scale()
    print(f"  Time scale: {scale}")


async def test_waiting(game: Godot) -> None:
    """Test waiting features."""
    header("WAITING FEATURES")

    # wait_for_node (already exists)
    print("Testing wait_for_node (existing node)...")
    node = await game.wait_for_node("/root/Game", timeout=2.0)
    print(f"  Found node: {node.name}")

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


async def test_game_play(game: Godot) -> None:
    """Test a complete game play sequence."""
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

    # Take final screenshot
    final_path = SCREENSHOT_DIR / "game_won.png"
    await game.screenshot(str(final_path))
    print(f"\n  Final screenshot saved to: {final_path}")


async def main():
    args = parse_args()
    godot_path = get_godot_path(args.godot_path)

    print("\n" + "="*60)
    print("  PlayGodot Native Debugger Feature Test")
    print("="*60)
    print(f"\nUsing Godot: {godot_path}")
    print(f"Project: {GODOT_PROJECT}")

    async with Godot.launch(
        str(GODOT_PROJECT),
        headless=args.headless,
        timeout=15.0,
        verbose=args.verbose,
        godot_path=godot_path,
    ) as game:
        print("\nGame launched, waiting for main scene...")
        await game.wait_for_node("/root/Game")
        print("Game ready!")
        await asyncio.sleep(0.5)

        try:
            await test_node_interaction(game)
            await test_query_nodes(game)
            await test_input_simulation(game)
            await test_screenshots(game)
            await test_scene_management(game)
            await test_game_state(game)
            await test_waiting(game)
            await test_game_play(game)

            header("ALL TESTS COMPLETE")
            print("All PlayGodot native debugger features tested successfully!")
            print(f"\nScreenshots saved to: {SCREENSHOT_DIR}/")

        except Exception as e:
            print(f"\n ERROR: {e}")
            import traceback
            traceback.print_exc()
            raise

        # Keep game open briefly
        await asyncio.sleep(2)


if __name__ == "__main__":
    asyncio.run(main())
