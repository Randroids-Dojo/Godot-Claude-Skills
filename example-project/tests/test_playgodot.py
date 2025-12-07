"""
PlayGodot E2E tests for the tic-tac-toe game.

Tests PlayGodot automation features against a real Godot game.
Requires a custom Godot build with automation support.

Run with:
    export GODOT_PATH=/path/to/godot-automation-fork
    pytest tests/test_playgodot.py -v
"""

import asyncio

import pytest


GAME = "/root/Game"


@pytest.mark.asyncio
async def test_get_node(game):
    """Test getting a node."""
    node = await game.get_node(GAME)
    assert node.name == "Game"


@pytest.mark.asyncio
async def test_node_exists(game):
    """Test checking node existence."""
    assert await game.node_exists(GAME) is True
    assert await game.node_exists("/root/NonExistent") is False


@pytest.mark.asyncio
async def test_get_property(game):
    """Test getting a node property."""
    assert await game.get_property(GAME, "visible") is True


@pytest.mark.asyncio
async def test_call_method(game):
    """Test calling a method on a node."""
    board = await game.call(GAME, "get_board_state")
    assert board == ["", "", "", "", "", "", "", "", ""]


@pytest.mark.asyncio
async def test_query_nodes(game):
    """Test querying nodes by pattern."""
    cells = await game.query_nodes("*Cell*")
    assert len(cells) == 9


@pytest.mark.asyncio
async def test_click(game):
    """Test clicking on a node."""
    await game.click(f"{GAME}/VBoxContainer/GameBoard/GridContainer/Cell0")
    await asyncio.sleep(0.1)
    board = await game.call(GAME, "get_board_state")
    assert board[0] == "X"


@pytest.mark.asyncio
async def test_screenshot(game):
    """Test screenshot returns bytes."""
    png_data = await game.screenshot()
    assert isinstance(png_data, bytes)


@pytest.mark.asyncio
async def test_get_current_scene(game):
    """Test getting current scene."""
    scene = await game.get_current_scene()
    assert scene["path"] == "res://scenes/main.tscn"
    assert scene["name"] == "Game"


@pytest.mark.asyncio
async def test_reload_scene(game):
    """Test reloading the scene resets state."""
    await game.call(GAME, "make_move", [4])
    assert (await game.call(GAME, "get_board_state"))[4] == "X"

    await game.reload_scene()
    await asyncio.sleep(0.3)
    await game.wait_for_node(GAME)

    board = await game.call(GAME, "get_board_state")
    assert board == ["", "", "", "", "", "", "", "", ""]


@pytest.mark.asyncio
async def test_pause(game):
    """Test pausing and unpausing."""
    await game.pause()
    assert await game.is_paused() is True

    await game.unpause()
    assert await game.is_paused() is False


@pytest.mark.asyncio
async def test_time_scale(game):
    """Test setting time scale."""
    await game.set_time_scale(2.0)
    assert await game.get_time_scale() == 2.0

    await game.set_time_scale(1.0)


@pytest.mark.asyncio
async def test_wait_for_node(game):
    """Test waiting for a node with timeout."""
    node = await game.wait_for_node(GAME, timeout=1.0)
    assert node.name == "Game"


@pytest.mark.asyncio
async def test_game_win(game):
    """Test playing a game to completion."""
    # X wins with top row: 0, 1, 2
    for pos in [0, 3, 1, 4, 2]:
        await game.call(GAME, "make_move", [pos])

    assert await game.call(GAME, "is_game_active") is False
    assert await game.call(GAME, "get_winner") == "X"
