# PlayGodot Python Testing Guide

PlayGodot is an external testing framework for Godot games. It uses Godot's native RemoteDebugger protocol to automate game testing from Python.

## Requirements

- **Godot with automation support** - A custom Godot build with the RemoteDebugger automation protocol
- **Python 3.10+** - For running pytest tests
- **PlayGodot package** - The Python client library

## Installation

```bash
# Install from PyPI (when published)
pip install playgodot

# Or install from source
git clone https://github.com/Randroids-Dojo/PlayGodot.git
pip install -e PlayGodot/python
```

## Test Configuration

Create a `conftest.py` file in your tests directory:

```python
import pytest_asyncio
from pathlib import Path
from playgodot import Godot

GODOT_PROJECT = Path(__file__).parent.parent
GODOT_PATH = "/path/to/godot-fork"  # Path to Godot with automation support

@pytest_asyncio.fixture
async def game():
    """Fixture that launches the game and provides a connected client."""
    async with Godot.launch(
        str(GODOT_PROJECT),
        headless=True,
        timeout=15.0,
        godot_path=GODOT_PATH,
    ) as g:
        await g.wait_for_node("/root/Game")
        yield g
```

## Writing Tests

### Basic Test Structure

```python
import pytest

GAME = "/root/Game"

@pytest.mark.asyncio
async def test_example(game):
    # Your test code here
    result = await game.call(GAME, "some_method")
    assert result == expected_value
```

### Node Interaction

```python
@pytest.mark.asyncio
async def test_node_interaction(game):
    # Get a node
    node = await game.get_node("/root/Game/Player")

    # Get property
    health = await game.get_property("/root/Game/Player", "health")
    assert health == 100

    # Set property
    await game.set_property("/root/Game/Player", "health", 50)

    # Call method
    result = await game.call("/root/Game/Player", "take_damage", [25])

    # Check node exists
    exists = await game.node_exists("/root/Game/Enemy")
```

### Input Simulation

```python
@pytest.mark.asyncio
async def test_input(game):
    # Mouse clicks
    await game.click("/root/Game/StartButton")   # Click by node path
    await game.click(400, 300)                   # Click by coordinates
    await game.double_click("/root/Game/Item")
    await game.right_click(100, 100)

    # Drag and drop
    await game.drag("/root/Game/DragItem", "/root/Game/DropZone")

    # Keyboard
    await game.press_key("space")
    await game.press_key("ctrl+s")               # With modifiers
    await game.type_text("Hello World")

    # Input actions
    await game.press_action("jump")
    await game.hold_action("sprint", 2.0)        # Hold for 2 seconds

    # Touch gestures
    await game.tap(300, 200)
    await game.swipe(100, 100, 400, 100)
    await game.pinch((200, 200), 0.5)            # Pinch to zoom out
```

### Node Queries

```python
@pytest.mark.asyncio
async def test_queries(game):
    # Find all nodes matching a pattern
    buttons = await game.query_nodes("*Button*")
    print(f"Found {len(buttons)} buttons")

    # Count matching nodes
    count = await game.count_nodes("*Enemy*")
    assert count >= 0
```

### Screenshots

```python
@pytest.mark.asyncio
async def test_screenshots(game):
    # Capture entire viewport
    png_data = await game.screenshot()

    # Save to file
    await game.screenshot("/tmp/screenshot.png")

    # Capture specific node
    await game.screenshot(node="/root/Game/UI")
```

### Scene Management

```python
@pytest.mark.asyncio
async def test_scene_management(game):
    # Get current scene info
    scene = await game.get_current_scene()
    print(f"Current scene: {scene['name']} at {scene['path']}")

    # Change scene
    await game.change_scene("res://scenes/level2.tscn")
    await game.wait_for_node("/root/Level2")

    # Reload current scene
    await game.reload_scene()
    await game.wait_for_node("/root/Game")
```

### Game State Control

```python
@pytest.mark.asyncio
async def test_game_state(game):
    # Pause and unpause
    await game.pause()
    assert await game.is_paused() == True

    await game.unpause()
    assert await game.is_paused() == False

    # Time scale (slow motion / speed up)
    await game.set_time_scale(0.5)              # Half speed
    scale = await game.get_time_scale()
    assert scale == 0.5

    await game.set_time_scale(2.0)              # Double speed
    await game.set_time_scale(1.0)              # Normal speed
```

### Waiting for Conditions

```python
@pytest.mark.asyncio
async def test_waiting(game):
    # Wait for a node to exist
    node = await game.wait_for_node("/root/Game/SpawnedEnemy", timeout=5.0)

    # Wait for a node to be visible
    await game.wait_for_visible("/root/Game/UI/GameOverPanel", timeout=10.0)

    # Wait for a custom condition
    async def check_score():
        score = await game.call("/root/Game", "get_score")
        return score >= 100

    await game.wait_for(check_score, timeout=30.0)
```

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_game.py -v

# Run specific test
pytest tests/test_game.py::test_clicking_makes_move -v

# With timeout
pytest tests/ -v --timeout=60

# Stop on first failure
pytest tests/ -v -x
```

## Complete Example

Here's a complete example test file for a tic-tac-toe game:

```python
"""PlayGodot tests for Tic-Tac-Toe game."""

import pytest

GAME = "/root/Game"

@pytest.mark.asyncio
async def test_game_starts_with_empty_board(game):
    """Test that the game initializes with an empty board."""
    board = await game.call(GAME, "get_board_state")
    assert board == ["", "", "", "", "", "", "", "", ""]

@pytest.mark.asyncio
async def test_game_starts_with_x_turn(game):
    """Test that X goes first."""
    player = await game.call(GAME, "get_current_player")
    assert player == "X"

@pytest.mark.asyncio
async def test_clicking_cell_makes_move(game):
    """Test that clicking a cell places the current player's mark."""
    await game.click("/root/Game/Board/Cell4")

    board = await game.call(GAME, "get_board_state")
    assert board[4] == "X"

@pytest.mark.asyncio
async def test_x_wins(game):
    """Test that X can win with a top row."""
    # X takes top row, O takes middle row
    for i, pos in enumerate([0, 3, 1, 4, 2]):  # X: 0,1,2 / O: 3,4
        await game.call(GAME, "make_move", [pos])

    is_active = await game.call(GAME, "is_game_active")
    assert is_active == False

    winner = await game.call(GAME, "get_winner")
    assert winner == "X"

@pytest.mark.asyncio
async def test_restart_button(game):
    """Test that the restart button resets the game."""
    # Make some moves
    await game.call(GAME, "make_move", [0])
    await game.call(GAME, "make_move", [1])

    # Click restart
    await game.click("/root/Game/RestartButton")

    # Verify board is empty
    board = await game.call(GAME, "get_board_state")
    assert board == ["", "", "", "", "", "", "", "", ""]
```

## Debugging Tests

### Verbose Logging

Enable verbose output when launching Godot:

```python
async with Godot.launch(
    str(GODOT_PROJECT),
    headless=True,
    verbose=True,  # Enable Godot verbose output
) as g:
    ...
```

### Non-Headless Testing

Run tests with a visible window for debugging:

```python
async with Godot.launch(
    str(GODOT_PROJECT),
    headless=False,  # Show window
    resolution=(1280, 720),
) as g:
    ...
```

### Custom Port

Use a different debugger port to avoid conflicts:

```python
async with Godot.launch(
    str(GODOT_PROJECT),
    port=6008,  # Custom port (default is 6007)
) as g:
    ...
```

## Architecture

PlayGodot uses Godot's RemoteDebugger protocol:

1. PlayGodot starts a TCP server on port 6007
2. Godot is launched with `--remote-debug tcp://127.0.0.1:6007`
3. Godot connects to PlayGodot as a debugging client
4. PlayGodot sends automation commands and receives responses
5. Commands are serialized using Godot's binary Variant format

This approach requires no addons or modifications to your game - it works with any Godot project using the automation-enabled Godot fork.
