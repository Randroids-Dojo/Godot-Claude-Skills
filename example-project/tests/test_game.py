"""Tests for the Tic Tac Toe game using PlayGodot."""

import pytest


# Node paths for this game's structure
GAME = "/root/Game"
CELL = "/root/Game/VBoxContainer/GameBoard/GridContainer/Cell{}"
STATUS = "/root/Game/VBoxContainer/StatusLabel"
RESTART = "/root/Game/VBoxContainer/RestartButton"


@pytest.mark.asyncio
async def test_game_starts_with_empty_board(game):
    """Game should start with an empty board."""
    board = await game.call(GAME, "get_board_state")
    assert board == ["", "", "", "", "", "", "", "", ""]


@pytest.mark.asyncio
async def test_game_starts_with_x_turn(game):
    """X should go first."""
    player = await game.call(GAME, "get_current_player")
    assert player == "X"


@pytest.mark.asyncio
async def test_game_is_active_on_start(game):
    """Game should be active when starting."""
    active = await game.call(GAME, "is_game_active")
    assert active is True


@pytest.mark.asyncio
async def test_clicking_cell_makes_move(game):
    """Clicking a cell should place the current player's mark."""
    # Click the center cell (Cell4)
    await game.click(CELL.format(4))

    # Check the board
    board = await game.call(GAME, "get_board_state")
    assert board[4] == "X"


@pytest.mark.asyncio
async def test_players_alternate(game):
    """Players should alternate turns."""
    # X plays
    await game.click(CELL.format(0))
    player = await game.call(GAME, "get_current_player")
    assert player == "O"

    # O plays
    await game.click(CELL.format(1))
    player = await game.call(GAME, "get_current_player")
    assert player == "X"


@pytest.mark.asyncio
async def test_cannot_click_occupied_cell(game):
    """Clicking an occupied cell should not change it."""
    # X plays center
    await game.click(CELL.format(4))

    # O tries to play center (should fail)
    await game.click(CELL.format(4))

    # Cell should still be X
    board = await game.call(GAME, "get_board_state")
    assert board[4] == "X"

    # Should still be O's turn
    player = await game.call(GAME, "get_current_player")
    assert player == "O"


@pytest.mark.asyncio
async def test_x_wins_top_row(game):
    """X should win with top row."""
    # X: 0, O: 3, X: 1, O: 4, X: 2 (wins)
    await game.click(CELL.format(0))  # X
    await game.click(CELL.format(3))  # O
    await game.click(CELL.format(1))  # X
    await game.click(CELL.format(4))  # O
    await game.click(CELL.format(2))  # X wins

    active = await game.call(GAME, "is_game_active")
    assert active is False

    status = await game.get_property(STATUS, "text")
    assert "X" in status and "Wins" in status


@pytest.mark.asyncio
async def test_o_wins_diagonal(game):
    """O should win with diagonal."""
    # X: 1, O: 0, X: 5, O: 4, X: 6, O: 8 (wins)
    await game.click(CELL.format(1))  # X
    await game.click(CELL.format(0))  # O
    await game.click(CELL.format(5))  # X
    await game.click(CELL.format(4))  # O
    await game.click(CELL.format(6))  # X
    await game.click(CELL.format(8))  # O wins

    active = await game.call(GAME, "is_game_active")
    assert active is False

    status = await game.get_property(STATUS, "text")
    assert "O" in status and "Wins" in status


@pytest.mark.asyncio
async def test_draw_game(game):
    """Game should end in draw when board is full with no winner."""
    # Play a draw game:
    # X O X
    # X X O
    # O X O
    moves = [0, 1, 3, 4, 2, 6, 7, 8, 5]  # Results in draw
    for move in moves:
        await game.click(CELL.format(move))

    active = await game.call(GAME, "is_game_active")
    assert active is False

    status = await game.get_property(STATUS, "text")
    assert "Draw" in status


@pytest.mark.asyncio
async def test_restart_button_resets_game(game):
    """Restart button should reset the game."""
    # Make some moves
    await game.click(CELL.format(0))
    await game.click(CELL.format(1))

    # Click restart
    await game.click(RESTART)

    # Board should be empty
    board = await game.call(GAME, "get_board_state")
    assert board == ["", "", "", "", "", "", "", "", ""]

    # Should be X's turn
    player = await game.call(GAME, "get_current_player")
    assert player == "X"

    # Game should be active
    active = await game.call(GAME, "is_game_active")
    assert active is True


@pytest.mark.asyncio
async def test_make_move_api(game):
    """make_move API should work correctly."""
    result = await game.call(GAME, "make_move", [4])
    assert result is True

    board = await game.call(GAME, "get_board_state")
    assert board[4] == "X"


@pytest.mark.asyncio
async def test_make_move_fails_on_occupied(game):
    """make_move should return false for occupied cell."""
    await game.call(GAME, "make_move", [4])
    result = await game.call(GAME, "make_move", [4])
    assert result is False


@pytest.mark.asyncio
async def test_status_label_shows_turn(game):
    """Status label should show current player's turn."""
    status = await game.get_property(STATUS, "text")
    assert "X" in status and "Turn" in status