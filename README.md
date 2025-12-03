# Godot-Claude-Skills

A collection of Claude Code skills for Godot Engine game development and testing.

## What are Skills?

Skills are folders of instructions, scripts, and resources that Claude loads dynamically to improve performance on specialized tasks. Each skill contains a `SKILL.md` file with YAML frontmatter and markdown instructions.

## Repository Structure

```
.
├── .claude/
│   ├── settings.json          # Claude Code project settings
│   └── skills/                # Skills installed for local use
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI workflow
├── example-project/           # Tic-Tac-Toe game for testing
│   ├── project.godot
│   ├── test/                  # GdUnit4 test files
│   │   ├── game_test.gd
│   │   └── game_scene_test.gd
│   ├── scenes/
│   │   └── main.tscn
│   └── scripts/
│       └── game.gd
├── skills/
│   ├── godot-testing/         # Main testing skill
│   │   ├── SKILL.md
│   │   ├── scripts/           # Python helper scripts
│   │   └── references/        # Documentation
│   └── example-test/          # Simple example skill
│       └── SKILL.md
└── README.md
```

## Available Skills

| Skill | Description |
|-------|-------------|
| `godot-testing` | Test Godot projects using GdUnit4 framework with input simulation, scene testing, and CI integration |
| `example-test` | Simple example skill for testing and learning the skill format |

## godot-testing Skill

The main skill for testing Godot projects. Includes:

- **GdUnit4 integration** - Unit tests, scene tests, input simulation
- **Python helper scripts** - `run_tests.py`, `parse_results.py`, `validate_project.py`
- **Reference documentation** - Quickstart, scene runner API, assertions, CI setup

### Quick Example

```gdscript
# test/game_test.gd
extends GdUnitTestSuite

func test_player_health() -> void:
    var player = auto_free(Player.new())
    assert_that(player.health).is_equal(100)

    player.take_damage(30)
    assert_that(player.health).is_equal(70)
```

### Running Tests

```bash
# Run all tests
godot --headless --path . -s res://addons/gdUnit4/bin/GdUnitCmdTool.gd --run-tests

# Using helper script
python skills/godot-testing/scripts/run_tests.py --project ./my-game
```

## Example Project

The repository includes a **Tic-Tac-Toe** game (`example-project/`) with full test coverage:

- **2-player game** with X and O turns
- **Win detection** for rows, columns, and diagonals
- **Draw detection** when board is full
- **GdUnit4 tests** - 15+ unit and integration tests

### Running Locally

```bash
# Open in Godot Editor
godot --path example-project --editor

# Run headless (for testing)
godot --headless --path example-project --quit

# Run GdUnit4 tests (after installing GdUnit4)
cd example-project
godot --headless -s res://addons/gdUnit4/bin/GdUnitCmdTool.gd --run-tests
```

### Automation API

The game exposes methods for automated testing:

```gdscript
game.make_move(4)           # Place at cell index (0-8)
game.get_board_state()      # Get current board as array
game.is_game_active()       # Check if game is running
game.get_current_player()   # Get "X" or "O"
```

## Creating New Skills

1. Create a new folder under `/skills/` with your skill name (lowercase, use hyphens)
2. Add a `SKILL.md` file with the following format:

```yaml
---
name: your-skill-name
description: Brief description of what the skill does and when to use it.
---

# Your Skill Title

Your instructions and guidelines here...
```

3. Optionally add:
   - `scripts/` - Helper scripts (Python, GDScript)
   - `references/` - Additional documentation
   - `assets/` - Templates, boilerplate files

## CI/CD

This repository includes GitHub Actions CI that:

1. **Installs Claude CLI** - Sets up `@anthropic-ai/claude-code` via npm
2. **Installs Godot Engine** - Sets up Godot 4.3.0 for headless use
3. **Installs GdUnit4** - Clones testing framework into example project
4. **Installs Skills** - Copies skills to `.claude/skills/` directory
5. **Validates Skills** - Checks that all skills have proper YAML frontmatter
6. **Imports Godot Project** - Generates `.godot` cache
7. **Runs Smoke Test** - Validates game initialization
8. **Runs GdUnit4 Tests** - Executes all unit and integration tests
9. **Uploads Reports** - Saves JUnit XML test results as artifacts

The CI runs on:
- Push to `main`/`master` branches
- Pull requests to `main`/`master` branches
- Manual trigger via `workflow_dispatch`

### Local Development

```bash
# Install Claude CLI
npm install -g @anthropic-ai/claude-code

# Copy skills to .claude directory
cp -r skills/* .claude/skills/

# Install GdUnit4 in your project
cd your-project
git clone https://github.com/MikeSchulze/gdUnit4.git addons/gdUnit4

# Run tests
python skills/godot-testing/scripts/run_tests.py --project ./your-project
```

## Future: PlayGodot

We're planning **PlayGodot** - an external automation framework for Godot (like Playwright for web apps). See `PlayGodot-README.md` for architecture and roadmap.

```python
# Future API
async with Godot.launch("path/to/project") as game:
    await game.click("/root/UI/StartButton")
    await game.wait_for_signal("game_started")
```

## Resources

- [Claude Code Skills Documentation](https://www.claude.com/blog/skills)
- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [GdUnit4 Documentation](https://mikeschulze.github.io/gdUnit4/)
- [Godot Engine Documentation](https://docs.godotengine.org/)
