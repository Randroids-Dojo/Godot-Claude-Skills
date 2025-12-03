---
name: example-test
description: Test and validate Godot projects by building, running, and analyzing logs. Use this skill when building Godot projects, checking for errors, reading game logs, or validating game functionality.
---

# Godot Project Testing Skill

This skill enables Claude to build, run, and test Godot Engine projects through CLI commands and log analysis.

## Capabilities

1. **Build Projects** - Validate and import Godot projects
2. **Read Logs** - Parse and analyze Godot output logs
3. **Validate Scripts** - Check GDScript for syntax errors
4. **Run Headless** - Execute games in headless mode for testing

## Building a Godot Project

To validate and import a Godot project:

```bash
# Import project resources (required before building)
godot --headless --import --path /path/to/project

# Validate the project configuration
godot --headless --validate-extension-api --path /path/to/project

# Check for script errors
godot --headless --check-only --script res://scripts/game.gd --path /path/to/project
```

## Running Tests

To run the project in headless mode:

```bash
# Run project headlessly (exits after initialization)
godot --headless --path /path/to/project --quit

# Run with verbose output for debugging
godot --headless --verbose --path /path/to/project --quit
```

## Log Analysis

Godot logs use prefixes to indicate message types. When analyzing logs, look for:

| Prefix | Meaning |
|--------|---------|
| `[TicTacToe]` | Game-specific log messages |
| `ERROR` | Critical errors that need fixing |
| `WARNING` | Non-critical issues to review |
| `SCRIPT ERROR` | GDScript syntax or runtime errors |

### Example Log Output

```
[TicTacToe] Game initialized
[TicTacToe] Board initialized with 9 empty cells
[TicTacToe] Player X placed at cell 4
[TicTacToe] Player O placed at cell 0
[TicTacToe] Winning combination found: [0, 1, 2]
[TicTacToe] Game ended - O wins!
```

## Project Structure

The example project follows this structure:

```
example-project/
├── project.godot          # Project configuration
├── icon.svg               # Project icon
├── scenes/
│   └── main.tscn         # Main game scene
└── scripts/
    └── game.gd           # Game logic script
```

## Validation Checklist

When testing a Godot project, verify:

1. **Project imports successfully** - No missing resources
2. **Scripts compile** - No GDScript syntax errors
3. **Scene loads** - Main scene initializes correctly
4. **Logs show expected output** - Game logic executes properly
5. **No errors or warnings** - Clean build output

## CI Integration

This skill is designed to work with CI pipelines. The workflow should:

1. Set up Godot Engine (headless mode)
2. Import the project to generate .godot cache
3. Validate scripts and resources
4. Run headless tests if available
5. Parse output for errors

## Automation API

The example tic-tac-toe game exposes methods for automation:

```gdscript
# Get current board state
var state: Array[String] = game.get_board_state()

# Make a move programmatically
var success: bool = game.make_move(4)  # Place in center

# Check if game is still active
var active: bool = game.is_game_active()

# Get current player
var player: String = game.get_current_player()  # "X" or "O"
```

## Future Capabilities

This skill will be extended to support:

- **Visual testing** - Screenshot comparison
- **Gameplay automation** - Simulate player input
- **Performance profiling** - Frame time analysis
- **Memory leak detection** - Resource monitoring
