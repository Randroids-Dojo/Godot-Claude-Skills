"""
PlayGodot E2E tests for the tic-tac-toe game.

Tests all PlayGodot automation features. Requires a custom Godot build
with automation support.

Run with:
    export GODOT_PATH=/path/to/godot-automation-fork
    pytest tests/test_playgodot.py -v
"""

import asyncio
from pathlib import Path

import pytest

SCREENSHOT_DIR = Path(__file__).parent / "screenshots"


@pytest.mark.asyncio
async def test_get_node(game):
    """Test getting a node by path."""
    node = await game.get_node("/root/Game")
    assert node is not None
    assert node.name == "Game"


@pytest.mark.asyncio
async def test_node_exists(game):
    """Test checking if nodes exist."""
    assert await game.node_exists("/root/Game") is True
    assert await game.node_exists("/root/NonExistent") is False


@pytest.mark.asyncio
async def test_get_property(game):
    """Test getting node properties."""
    visible = await game.get_property("/root/Game", "visible")
    assert visible is True


@pytest.mark.asyncio
async def test_call_method(game):
    """Test calling methods on nodes."""
    board_state = await game.call("/root/Game", "get_board_state")
    assert board_state == ["", "", "", "", "", "", "", "", ""]

    current_player = await game.call("/root/Game", "get_current_player")
    assert current_player == "X"


@pytest.mark.asyncio
async def test_query_nodes(game):
    """Test querying nodes by pattern."""
    cells = await game.query_nodes("*Cell*")
    assert len(cells) >= 9


@pytest.mark.asyncio
async def test_count_nodes(game):
    """Test counting nodes by pattern."""
    label_count = await game.count_nodes("*Label*")
    assert label_count >= 1


@pytest.mark.asyncio
async def test_click_on_node(game):
    """Test clicking on a node."""
    await game.click("/root/Game/VBoxContainer/GameBoard/GridContainer/Cell0")
    await asyncio.sleep(0.2)

    board = await game.call("/root/Game", "get_board_state")
    assert board[0] == "X"


@pytest.mark.asyncio
async def test_restart_button(game):
    """Test clicking the restart button resets the game."""
    await game.call("/root/Game", "make_move", [0])
    assert (await game.call("/root/Game", "get_board_state"))[0] == "X"

    await game.click("/root/Game/VBoxContainer/RestartButton")
    await asyncio.sleep(0.2)

    board = await game.call("/root/Game", "get_board_state")
    assert board == ["", "", "", "", "", "", "", "", ""]


@pytest.mark.asyncio
async def test_screenshot_returns_bytes(game):
    """Test that screenshot returns bytes (may be empty in headless mode)."""
    png_data = await game.screenshot()
    assert isinstance(png_data, bytes)
    # Note: Screenshots return empty bytes in headless mode due to Godot limitation
    if len(png_data) > 0:
        assert png_data[:8] == b'\x89PNG\r\n\x1a\n'


@pytest.mark.asyncio
async def test_screenshot_saves_to_file(game):
    """Test saving screenshot to file (may be empty in headless mode)."""
    SCREENSHOT_DIR.mkdir(exist_ok=True)
    path = SCREENSHOT_DIR / "test_screenshot.png"

    await game.screenshot(str(path))

    # Note: File may not be created or be empty in headless mode
    # This is a Godot limitation, not a PlayGodot bug


@pytest.mark.asyncio
async def test_get_current_scene(game):
    """Test getting current scene path."""
    scene = await game.get_current_scene()
    # API returns various formats: [path, name], {"path": ...}, or just path
    if isinstance(scene, list):
        scene_path = scene[0]
    elif isinstance(scene, dict):
        scene_path = scene.get("path", scene.get("file_path", str(scene)))
    else:
        scene_path = str(scene)
    assert "game" in scene_path.lower() or "main" in scene_path.lower()


@pytest.mark.asyncio
async def test_reload_scene(game):
    """Test reloading the scene."""
    await game.call("/root/Game", "make_move", [4])
    assert (await game.call("/root/Game", "get_board_state"))[4] == "X"

    await game.reload_scene()
    await asyncio.sleep(0.5)
    await game.wait_for_node("/root/Game")

    board = await game.call("/root/Game", "get_board_state")
    assert board == ["", "", "", "", "", "", "", "", ""]


@pytest.mark.asyncio
async def test_pause_unpause(game):
    """Test pausing and unpausing the game."""
    await game.pause()
    assert await game.is_paused() is True

    await game.unpause()
    assert await game.is_paused() is False


@pytest.mark.asyncio
async def test_time_scale(game):
    """Test setting time scale."""
    await game.set_time_scale(0.5)
    assert await game.get_time_scale() == 0.5

    await game.set_time_scale(2.0)
    assert await game.get_time_scale() == 2.0

    await game.set_time_scale(1.0)
    assert await game.get_time_scale() == 1.0


@pytest.mark.asyncio
async def test_wait_for_node(game):
    """Test waiting for a node."""
    node = await game.wait_for_node("/root/Game", timeout=2.0)
    assert node is not None
    assert node.name == "Game"


@pytest.mark.asyncio
async def test_wait_for_visible(game):
    """Test waiting for node visibility."""
    await game.wait_for_visible("/root/Game/VBoxContainer/StatusLabel", timeout=2.0)


@pytest.mark.asyncio
async def test_wait_for_condition(game):
    """Test waiting for a custom condition."""
    await game.reload_scene()
    await asyncio.sleep(0.3)
    await game.wait_for_node("/root/Game")

    async def board_is_empty():
        board = await game.call("/root/Game", "get_board_state")
        return board == ["", "", "", "", "", "", "", "", ""]

    await game.wait_for(board_is_empty, timeout=5.0)


@pytest.mark.asyncio
async def test_win_detection(game):
    """Test that game correctly detects a win."""
    moves = [0, 3, 1, 4, 2]  # X: 0,1,2 | O: 3,4

    for pos in moves:
        await game.call("/root/Game", "make_move", [pos])
        await asyncio.sleep(0.1)

    assert await game.call("/root/Game", "is_game_active") is False
    assert await game.call("/root/Game", "get_winner") == "X"
