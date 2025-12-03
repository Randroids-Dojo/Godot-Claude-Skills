# PlayGodot (Future)

> **Status**: Planned - Not yet implemented

PlayGodot is a planned external automation framework for Godot, inspired by Playwright.

## Vision

Control Godot games from Python without modifying game code:

```python
from playgodot import Godot

async with Godot.launch("path/to/project") as game:
    await game.wait_for_node("/root/Main")
    await game.click("/root/Main/UI/StartButton")
    await game.wait_for_signal("game_started")

    state = await game.call("/root/Main/Game", "get_board_state")
    assert state[4] == "X"
```

## Architecture

```
┌─────────────────┐         WebSocket         ┌─────────────────┐
│  Python Client  │◄─────────────────────────►│  Godot Addon    │
│                 │         JSON-RPC           │                 │
│  playgodot      │                            │  Automate       │
│  .click()       │  Commands:                 │  Server         │
│  .call()        │  → click, type, get_node   │                 │
│  .wait_for()    │  ← results, screenshots    │                 │
└─────────────────┘                            └─────────────────┘
```

## Planned Features

### Node Interaction

```python
# Get/set properties
pos = await game.get_property("/root/Player", "position")
await game.set_property("/root/Player", "health", 100)

# Call methods
await game.call("/root/Game", "make_move", [4])
result = await game.call("/root/Game", "get_score")
```

### Input Simulation

```python
# Mouse
await game.click("/root/UI/Button")
await game.click_position(100, 200)
await game.drag("/root/Item", "/root/DropZone")

# Keyboard
await game.press_key("space")
await game.type_text("player1")
await game.press_action("jump")
```

### Waiting

```python
await game.wait_for_node("/root/Enemy")
await game.wait_for_signal("game_over")
await game.wait_for_visible("/root/UI/Popup")
```

### Screenshots

```python
await game.screenshot("output.png")
await game.assert_screenshot("reference.png", threshold=0.01)
```

## Comparison

| Feature | GdUnit4 | PlayGodot |
|---------|---------|-----------|
| Language | GDScript/C# | Python |
| Runs in | Godot process | External |
| Requires addon | Yes | Yes |
| Requires game changes | Test code in project | None |

## When to Use What

**Use GdUnit4 when:**
- Writing unit tests for GDScript
- Testing game logic in isolation
- Running tests from Godot editor
- Team uses GDScript primarily

**Use PlayGodot when:**
- End-to-end testing
- Testing from CI without Godot knowledge
- Visual regression testing
- Cross-project test automation

## Roadmap

1. **v0.1** - Basic WebSocket protocol, node queries
2. **v0.2** - Input simulation, waiting
3. **v0.3** - Screenshots, visual testing
4. **v1.0** - Production ready

## Contributing

PlayGodot is open source and welcomes contributions.

See: [PlayGodot README](../../../../PlayGodot-README.md) for full architecture and contribution guidelines.

## Resources

- [Playwright](https://playwright.dev/) - Inspiration
- [GodotTestDriver](https://github.com/chickensoft-games/GodotTestDriver) - C# test driver
- [GdUnit4](https://github.com/MikeSchulze/gdUnit4) - GDScript testing
