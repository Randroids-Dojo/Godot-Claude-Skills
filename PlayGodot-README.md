# PlayGodot

**External automation and testing framework for Godot Engine games.**

PlayGodot enables you to control and test Godot games from external scripts, similar to how [Playwright](https://playwright.dev/) automates web browsers. Write tests in Python, run them headlessly in CI, and automate gameplay verification.

## Why PlayGodot?

Existing Godot testing tools (GdUnit4, GUT, GodotTestDriver) run *inside* the engine. PlayGodot runs *outside*, giving you:

- **Language freedom** - Write tests in Python, not just GDScript/C#
- **Process isolation** - Tests can't crash with the game
- **CI simplicity** - No need to understand Godot internals
- **Familiar patterns** - API inspired by Playwright

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         PlayGodot Architecture                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   External Process                           Godot Process              │
│  ┌─────────────────────┐                   ┌─────────────────────┐      │
│  │                     │    WebSocket      │                     │      │
│  │   Python Client     │◄────────────────►│   PlayGodot Addon   │      │
│  │                     │    JSON-RPC       │                     │      │
│  │  ┌───────────────┐  │                   │  ┌───────────────┐  │      │
│  │  │ playgodot     │  │   Commands:       │  │ Automate      │  │      │
│  │  │               │  │   ─────────────►  │  │ Server        │  │      │
│  │  │ .launch()     │  │   • click         │  │               │  │      │
│  │  │ .click()      │  │   • type          │  │ • Receives    │  │      │
│  │  │ .get_node()   │  │   • get_node      │  │   commands    │  │      │
│  │  │ .call()       │  │   • call_method   │  │ • Executes    │  │      │
│  │  │ .wait_for()   │  │   • screenshot    │  │   in game     │  │      │
│  │  │ .screenshot() │  │   • wait_signal   │  │ • Returns     │  │      │
│  │  │               │  │                   │  │   results     │  │      │
│  │  └───────────────┘  │   Responses:      │  └───────────────┘  │      │
│  │                     │   ◄─────────────  │                     │      │
│  │  async/await API    │   • node_data     │  Runs in _process() │      │
│  │                     │   • return_value  │                     │      │
│  └─────────────────────┘   • screenshots   └─────────────────────┘      │
│           │                • signals                  ▲                 │
│           │                                           │                 │
│           ▼                                           │                 │
│  ┌─────────────────────┐                   ┌─────────────────────┐      │
│  │   Test Framework    │                   │   Godot Engine      │      │
│  │   (pytest, etc.)    │                   │   (headless mode)   │      │
│  └─────────────────────┘                   └─────────────────────┘      │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Installation

### Python Client

```bash
pip install playgodot
```

### Godot Addon

1. Copy `addons/playgodot/` to your Godot project
2. Enable the plugin in Project Settings → Plugins
3. The automation server starts automatically in debug builds

Or install via Asset Library (coming soon).

## Quick Start

```python
import asyncio
from playgodot import Godot

async def test_game():
    # Launch Godot project
    async with Godot.launch("path/to/project") as game:
        # Wait for game to be ready
        await game.wait_for_node("/root/Main")

        # Click a button
        await game.click("/root/Main/UI/StartButton")

        # Wait for scene change
        await game.wait_for_signal("scene_changed")

        # Take a screenshot
        await game.screenshot("screenshots/game_started.png")

asyncio.run(test_game())
```

## API Reference

### Launching Games

```python
# Launch with default settings
game = await Godot.launch("path/to/project")

# Launch with options
game = await Godot.launch(
    "path/to/project",
    headless=True,           # Run without window (default: True)
    resolution=(1920, 1080), # Window size
    port=9999,               # WebSocket port (default: 9999)
    timeout=30000,           # Connection timeout in ms
    verbose=True,            # Enable debug logging
)

# Connect to already-running game
game = await Godot.connect("localhost:9999")
```

### Node Interaction

```python
# Get node by path
node = await game.get_node("/root/Main/Player")

# Get node properties
position = await game.get_property("/root/Main/Player", "position")
health = await game.get_property("/root/Main/Player", "health")

# Set node properties
await game.set_property("/root/Main/Player", "position", {"x": 100, "y": 200})

# Call node methods
result = await game.call("/root/Main/Game", "get_score")
await game.call("/root/Main/Game", "reset")

# Call with arguments
await game.call("/root/Main/Game", "make_move", [4])  # Single arg
await game.call("/root/Main/Game", "set_player", ["Alice", 100])  # Multiple args
```

### Input Simulation

```python
# Mouse input
await game.click("/root/Main/UI/Button")           # Click node center
await game.click_position(100, 200)                 # Click coordinates
await game.double_click("/root/Main/UI/Item")
await game.right_click("/root/Main/UI/ContextArea")
await game.drag("/root/Main/DragItem", "/root/Main/DropZone")
await game.move_mouse(500, 300)

# Keyboard input
await game.press_key("space")
await game.press_key("ctrl+s")                      # Key combinations
await game.type_text("Hello, World!")               # Type string
await game.press_action("jump")                     # Input actions
await game.hold_action("run", duration=2.0)

# Touch input (mobile)
await game.tap(100, 200)
await game.swipe(100, 200, 400, 200)
await game.pinch(center=(300, 300), scale=0.5)
```

### Waiting

```python
# Wait for node to exist
await game.wait_for_node("/root/Main/Enemy", timeout=5000)

# Wait for node to be visible
await game.wait_for_visible("/root/Main/UI/Popup")

# Wait for signal
await game.wait_for_signal("game_over")
await game.wait_for_signal("health_changed", source="/root/Main/Player")

# Wait for condition (polls until true)
await game.wait_for(
    lambda: game.get_property("/root/Main/Player", "health") < 50,
    timeout=10000
)

# Wait for frames/time
await game.wait_frames(60)      # Wait 60 frames
await game.wait_seconds(2.0)    # Wait 2 seconds
```

### Screenshots & Visual Testing

```python
# Take screenshot
await game.screenshot("output.png")

# Screenshot specific node
await game.screenshot("player.png", node="/root/Main/Player")

# Compare screenshots (returns similarity 0-1)
similarity = await game.compare_screenshot("expected.png", "actual.png")
assert similarity > 0.99, "Screenshots don't match"

# Visual regression testing
await game.assert_screenshot("reference/main_menu.png", threshold=0.01)
```

### Scene Management

```python
# Get current scene
scene = await game.get_current_scene()

# Change scene
await game.change_scene("res://levels/level2.tscn")

# Reload current scene
await game.reload_scene()

# Get scene tree structure
tree = await game.get_tree()
print(tree)  # Hierarchical node structure
```

### Game State

```python
# Get all nodes matching pattern
enemies = await game.query_nodes("/root/Main/Enemies/*")

# Check if node exists
exists = await game.node_exists("/root/Main/Boss")

# Get node count
count = await game.count_nodes("/root/Main/Coins/*")

# Pause/unpause game
await game.pause()
await game.unpause()
await game.set_time_scale(0.5)  # Slow motion
```

## Testing with pytest

```python
# test_game.py
import pytest
from playgodot import Godot

@pytest.fixture
async def game():
    async with Godot.launch("path/to/project") as g:
        yield g

@pytest.mark.asyncio
async def test_player_spawns(game):
    """Player should spawn at starting position."""
    await game.wait_for_node("/root/Main/Player")
    pos = await game.get_property("/root/Main/Player", "position")
    assert pos["x"] == 100
    assert pos["y"] == 200

@pytest.mark.asyncio
async def test_enemy_dies_when_shot(game):
    """Enemy should die when hit by bullet."""
    await game.wait_for_node("/root/Main/Enemy")

    # Simulate shooting
    await game.press_action("shoot")
    await game.wait_seconds(0.5)

    # Enemy should be gone
    exists = await game.node_exists("/root/Main/Enemy")
    assert not exists

@pytest.mark.asyncio
async def test_game_over_on_death(game):
    """Game over screen should appear when player dies."""
    # Kill the player
    await game.set_property("/root/Main/Player", "health", 0)

    # Wait for game over
    await game.wait_for_signal("game_over")
    await game.wait_for_visible("/root/Main/UI/GameOverScreen")

    # Verify screenshot
    await game.assert_screenshot("reference/game_over.png")
```

Run tests:

```bash
pytest test_game.py -v
```

## CI Integration

### GitHub Actions

```yaml
name: Game Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Godot
        uses: chickensoft-games/setup-godot@v2
        with:
          version: 4.3.0

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install PlayGodot
        run: pip install playgodot pytest pytest-asyncio

      - name: Run Tests
        run: pytest tests/ -v --tb=short
```

## JSON-RPC Protocol

PlayGodot uses JSON-RPC 2.0 over WebSocket. This enables building clients in any language.

### Request Format

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "get_node",
  "params": {
    "path": "/root/Main/Player"
  }
}
```

### Response Format

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "path": "/root/Main/Player",
    "class": "CharacterBody2D",
    "properties": {
      "position": {"x": 100, "y": 200},
      "health": 100
    }
  }
}
```

### Available Methods

| Method | Params | Description |
|--------|--------|-------------|
| `get_node` | `path` | Get node info |
| `get_property` | `path`, `property` | Get property value |
| `set_property` | `path`, `property`, `value` | Set property value |
| `call_method` | `path`, `method`, `args?` | Call node method |
| `click` | `path` or `x`, `y` | Simulate click |
| `press_key` | `key`, `modifiers?` | Press keyboard key |
| `press_action` | `action` | Press input action |
| `screenshot` | `path?` | Capture screenshot |
| `wait_signal` | `signal`, `source?`, `timeout?` | Wait for signal |
| `get_tree` | - | Get scene tree structure |
| `change_scene` | `path` | Load new scene |

## Comparison with Other Tools

| Feature | PlayGodot | GdUnit4 | GodotTestDriver | GUT |
|---------|-----------|---------|-----------------|-----|
| **Language** | Python (any) | GDScript, C# | C# only | GDScript |
| **Runs externally** | ✅ | ❌ | ❌ | ❌ |
| **Input simulation** | ✅ | ✅ | ✅ | ❌ |
| **Screenshot testing** | ✅ | ❌ | ❌ | ❌ |
| **Node drivers** | ✅ | ✅ | ✅ | ❌ |
| **Signal waiting** | ✅ | ✅ | ✅ | ✅ |
| **CI-friendly** | ✅ | ✅ | ✅ | ✅ |
| **No game modification** | ❌* | ❌ | ❌ | ❌ |

*Requires addon installed, but no test code in game.

## Project Structure

```
playgodot/
├── python/                     # Python client library
│   ├── playgodot/
│   │   ├── __init__.py
│   │   ├── client.py          # WebSocket client
│   │   ├── godot.py           # Main Godot class
│   │   ├── node.py            # Node wrapper
│   │   ├── input.py           # Input simulation
│   │   ├── screenshot.py      # Screenshot utilities
│   │   └── exceptions.py      # Custom exceptions
│   ├── tests/
│   └── pyproject.toml
│
├── addons/                     # Godot addon
│   └── playgodot/
│       ├── plugin.cfg
│       ├── playgodot.gd       # Main plugin script
│       ├── server.gd          # WebSocket server
│       ├── commands.gd        # Command handlers
│       ├── input_simulator.gd # Input simulation
│       └── screenshot.gd      # Screenshot capture
│
├── protocol/                   # Protocol specification
│   └── PROTOCOL.md
│
├── examples/                   # Example projects
│   ├── tic-tac-toe/
│   └── platformer/
│
└── docs/                       # Documentation
    ├── getting-started.md
    ├── api-reference.md
    └── ci-integration.md
```

## Roadmap

### v0.1.0 - Foundation
- [ ] WebSocket server addon for Godot 4.x
- [ ] Python client with async/await API
- [ ] Basic node interaction (get/set/call)
- [ ] Mouse and keyboard input simulation
- [ ] Screenshot capture

### v0.2.0 - Testing Features
- [ ] Signal waiting
- [ ] Node existence/visibility waiting
- [ ] Screenshot comparison
- [ ] pytest plugin

### v0.3.0 - Advanced Features
- [ ] Touch/gesture simulation
- [ ] Visual regression testing
- [ ] Record & playback
- [ ] Performance metrics

### v1.0.0 - Production Ready
- [ ] Godot 4.x full support
- [ ] Comprehensive documentation
- [ ] Asset Library publication
- [ ] PyPI publication

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Clone the repo
git clone https://github.com/your-org/playgodot.git
cd playgodot

# Python client development
cd python
pip install -e ".[dev]"
pytest

# Godot addon development
# Open addons/playgodot/ in Godot editor
```

### Areas for Contribution

- **Protocol design** - Help refine the JSON-RPC protocol
- **Python client** - Implement client features
- **Godot addon** - Implement server-side handlers
- **Documentation** - Improve docs and examples
- **Testing** - Add tests for the framework itself
- **Other clients** - TypeScript, Rust, Go clients

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- Inspired by [Playwright](https://playwright.dev/)
- Thanks to [GodotTestDriver](https://github.com/chickensoft-games/GodotTestDriver) for input simulation patterns
- Thanks to [GdUnit4](https://github.com/MikeSchulze/gdUnit4) for scene runner concepts

---

**PlayGodot** is not affiliated with Godot Engine or the Godot Foundation.
