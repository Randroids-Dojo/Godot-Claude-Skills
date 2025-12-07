---
name: godot
version: 1.0.0
description: Develop, test, build, and deploy Godot 4.x games. Includes GdUnit4 testing with input simulation, web/desktop exports, CI/CD pipelines, and deployment to Vercel/GitHub Pages/itch.io. Use when working with Godot Engine projects, writing GDScript, running tests, or deploying games.
---

# Godot Skill

Develop, test, build, and deploy Godot 4.x games. This skill provides comprehensive support for Godot game development workflows.

## Quick Reference

```bash
# Run all tests headlessly
godot --headless --path . -s res://addons/gdUnit4/bin/GdUnitCmdTool.gd --run-tests

# Run specific test
godot --headless --path . -s res://addons/gdUnit4/bin/GdUnitCmdTool.gd --run-tests --add res://test/my_test.gd

# Generate JUnit XML for CI
godot --headless --path . -s res://addons/gdUnit4/bin/GdUnitCmdTool.gd --run-tests --report-directory ./reports
```

## Test Structure

Place tests in `res://test/` directory with `_test.gd` suffix:

```
project/
├── addons/gdUnit4/          # GdUnit4 addon
├── test/                    # Test directory
│   ├── game_test.gd         # Test file
│   └── player_test.gd
└── scripts/
    └── game.gd              # Code under test
```

## Writing Tests

### Basic Test

```gdscript
# test/game_test.gd
extends GdUnitTestSuite

var game: Node

func before_test() -> void:
    game = auto_free(load("res://scripts/game.gd").new())

func test_initial_state() -> void:
    assert_that(game.is_game_active()).is_true()
    assert_that(game.get_current_player()).is_equal("X")

func test_make_move() -> void:
    var success := game.make_move(4)
    assert_that(success).is_true()
    assert_that(game.get_board_state()[4]).is_equal("X")
```

### Scene Testing with Input Simulation

```gdscript
# test/game_scene_test.gd
extends GdUnitTestSuite

var runner: GdUnitSceneRunner

func before_test() -> void:
    runner = scene_runner("res://scenes/main.tscn")

func after_test() -> void:
    runner.free()

func test_click_cell() -> void:
    # Wait for scene to be ready
    await runner.await_idle_frame()

    # Get cell position and click it
    var cell = runner.find_child("Cell4")
    runner.set_mouse_position(cell.global_position + cell.size / 2)
    runner.simulate_mouse_button_pressed(MOUSE_BUTTON_LEFT)
    await runner.await_input_processed()

    # Verify move was made
    var game = runner.scene()
    assert_that(game.get_board_state()[4]).is_equal("X")

func test_keyboard_restart() -> void:
    # Simulate pressing R to restart
    runner.simulate_key_pressed(KEY_R)
    await runner.await_input_processed()

    var game = runner.scene()
    assert_that(game.is_game_active()).is_true()
```

## Scene Runner API

### Mouse Input

```gdscript
# Position
runner.set_mouse_position(Vector2(100, 100))

# Clicks
runner.simulate_mouse_button_pressed(MOUSE_BUTTON_LEFT)
runner.simulate_mouse_button_released(MOUSE_BUTTON_LEFT)

# Convenience
runner.simulate_mouse_button_press(MOUSE_BUTTON_LEFT)  # Press and release

# Always wait after input
await runner.await_input_processed()
```

### Keyboard Input

```gdscript
# Single key
runner.simulate_key_pressed(KEY_SPACE)
runner.simulate_key_released(KEY_SPACE)

# With modifiers
runner.simulate_key_pressed(KEY_S, false, true)  # Ctrl+S

# Input actions
runner.simulate_action_pressed("jump")
runner.simulate_action_released("jump")
```

### Waiting

```gdscript
# Wait for input processing
await runner.await_input_processed()

# Wait for frames
await runner.await_idle_frame()

# Wait for signal
await runner.await_signal("game_over", [], 5000)  # 5s timeout

# Wait for condition
await runner.await_func(game, "is_game_over").is_true()
```

## Assertions

```gdscript
# Basic
assert_that(value).is_equal(expected)
assert_that(value).is_not_equal(other)
assert_that(value).is_null()
assert_that(value).is_not_null()

# Boolean
assert_that(condition).is_true()
assert_that(condition).is_false()

# Numbers
assert_that(number).is_greater(5)
assert_that(number).is_less(10)
assert_that(number).is_between(1, 100)

# Strings
assert_that(text).contains("expected")
assert_that(text).starts_with("prefix")
assert_that(text).ends_with("suffix")

# Arrays
assert_that(array).contains(element)
assert_that(array).has_size(5)
assert_that(array).is_empty()

# Signals
await assert_signal(node).is_emitted("signal_name")
await assert_signal(node).wait_until(1000).is_emitted("signal_name")
```

## CI Integration

Run tests in GitHub Actions:

```yaml
- name: Run GdUnit4 Tests
  run: |
    godot --headless --path . \
      -s res://addons/gdUnit4/bin/GdUnitCmdTool.gd \
      --run-tests \
      --report-directory ./reports

- name: Upload Test Results
  uses: actions/upload-artifact@v4
  if: always()
  with:
    name: test-results
    path: reports/
```

Use bundled helper script for simpler CI:

```bash
python skills/godot/scripts/run_tests.py --project ./example-project
```

## Setup GdUnit4

1. Download from Asset Library or clone:
   ```bash
   git clone https://github.com/MikeSchulze/gdUnit4.git addons/gdUnit4
   ```

2. Enable plugin in Project Settings → Plugins

3. Create `test/` directory and add test files

## Exporting & Deployment

### Web Export

```bash
# Export to web (requires export_presets.cfg)
godot --headless --export-release "Web" ./build/index.html

# Using helper script
python scripts/export_build.py --project . --preset Web --output ./build/index.html
```

### Deploy to Vercel

```bash
npm i -g vercel
vercel deploy ./build --prod
```

### Export Preset (export_presets.cfg)

```ini
[preset.0]
name="Web"
platform="Web"
runnable=true
export_path="build/index.html"
```

See `references/deployment.md` for full Vercel, GitHub Pages, and itch.io setup.

## External Testing with PlayGodot

PlayGodot enables testing Godot games from Python using pytest, supporting both WebSocket addon and native RemoteDebugger protocols.

### Setup

```bash
# Install PlayGodot
pip install playgodot

# Or from source
git clone https://github.com/Randroids-Dojo/PlayGodot.git
pip install -e PlayGodot/python
```

### Test Configuration (conftest.py)

```python
import pytest_asyncio
from pathlib import Path
from playgodot import Godot

GODOT_PROJECT = Path(__file__).parent.parent
GODOT_PATH = "/path/to/godot"  # or use system godot

@pytest_asyncio.fixture
async def game():
    async with Godot.launch(
        str(GODOT_PROJECT),
        headless=True,
        timeout=15.0,
        godot_path=GODOT_PATH,
        native=True,  # Use native RemoteDebugger protocol
    ) as g:
        await g.wait_for_node("/root/Game")
        yield g
```

### Writing PlayGodot Tests

```python
import pytest

GAME = "/root/Game"

@pytest.mark.asyncio
async def test_game_starts_with_empty_board(game):
    board = await game.call(GAME, "get_board_state")
    assert board == ["", "", "", "", "", "", "", "", ""]

@pytest.mark.asyncio
async def test_clicking_cell_makes_move(game):
    # Click on center cell (Cell4)
    await game.click("/root/Game/VBoxContainer/GameBoard/GridContainer/Cell4")

    # Verify move was made
    board = await game.call(GAME, "get_board_state")
    assert board[4] == "X"

@pytest.mark.asyncio
async def test_game_win(game):
    # Make winning moves
    await game.call(GAME, "make_move", [0])  # X
    await game.call(GAME, "make_move", [3])  # O
    await game.call(GAME, "make_move", [1])  # X
    await game.call(GAME, "make_move", [4])  # O
    await game.call(GAME, "make_move", [2])  # X wins!

    is_active = await game.call(GAME, "is_game_active")
    assert is_active is False
```

### PlayGodot API

```python
# Wait for nodes
await game.wait_for_node("/root/Game", timeout=10.0)

# Call methods
result = await game.call("/root/Node", "method_name", [arg1, arg2])

# Get/set properties
value = await game.get("/root/Node", "property_name")
await game.set("/root/Node", "property_name", new_value)

# Input simulation
await game.click("/root/Button")           # Click node
await game.click(300, 200)                 # Click coordinates
await game.press_key("space")              # Press key
await game.press_action("jump")            # Press input action
await game.type_text("hello")              # Type text

# Get node info
node = await game.get_node("/root/Game")
tree = await game.get_tree()
```

### Native vs Addon Protocol

```python
# Native protocol (requires Godot fork with automation)
# Uses --remote-debug tcp://127.0.0.1:6007
async with Godot.launch(project, native=True) as g:
    pass

# WebSocket addon protocol (requires playgodot addon)
# Uses WebSocket on port 9999
async with Godot.launch(project, native=False) as g:
    pass
```

### Running PlayGodot Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_game.py::test_clicking_cell_makes_move -v

# Use addon protocol instead of native
PLAYGODOT_ADDON=1 pytest tests/ -v
```

## References

- `references/gdunit4-quickstart.md` - Installation and setup
- `references/scene-runner.md` - Full input simulation API
- `references/assertions.md` - All assertion methods
- `references/ci-integration.md` - CI/CD configuration
- `references/deployment.md` - Web export and deployment guide
- `references/playgodot.md` - PlayGodot Python testing guide
