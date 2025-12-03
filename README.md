# Godot-Claude-Skills

A collection of Claude Code skills for Godot Engine game development.

## What are Skills?

Skills are folders of instructions, scripts, and resources that Claude loads dynamically to improve performance on specialized tasks. Each skill contains a `SKILL.md` file with YAML frontmatter and markdown instructions.

## Repository Structure

```
.
├── .claude-plugin/
│   ├── plugin.json            # Plugin metadata for marketplace
│   └── marketplace.json       # Marketplace registry info
├── .claude/
│   ├── settings.json          # Claude Code project settings
│   └── skills/                # Skills installed for local use
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI workflow
├── example-project/           # Tic-Tac-Toe game for testing
│   ├── project.godot
│   ├── test/                  # GdUnit4 test files
│   ├── scenes/
│   └── scripts/
├── skills/
│   ├── godot/                 # Main Godot development skill
│   │   ├── SKILL.md
│   │   ├── scripts/           # Python helper scripts
│   │   └── references/        # Documentation
│   └── example-test/          # Simple example skill
│       └── SKILL.md
├── LICENSE                    # MIT License
├── CHANGELOG.md               # Version history
└── README.md
```

## Available Skills

| Skill | Description |
|-------|-------------|
| `godot` | Develop, test, build, and deploy Godot 4.x games with GdUnit4, web exports, and CI/CD |
| `example-test` | Simple example skill for testing and learning the skill format |

## Godot Skill

The main skill for Godot game development. Includes:

- **GdUnit4 integration** - Unit tests, scene tests, input simulation
- **Web/Desktop exports** - Build and export games
- **CI/CD pipelines** - GitHub Actions workflows
- **Deployment** - Vercel, GitHub Pages, itch.io
- **Python helper scripts** - `run_tests.py`, `parse_results.py`, `export_build.py`

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
python skills/godot/scripts/run_tests.py --project ./my-game
```

### Building & Deploying

```bash
# Export web build
godot --headless --export-release "Web" ./build/index.html

# Deploy to Vercel
vercel deploy ./build --prod
```

## Example Project

The repository includes a **Tic-Tac-Toe** game (`example-project/`) with full test coverage:

- **2-player game** with X and O turns
- **Win detection** for rows, columns, and diagonals
- **Draw detection** when board is full
- **GdUnit4 tests** - 15+ unit and integration tests
- **Web export** - Deployable to Vercel

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

## Installing the Skills

### Option 1: Plugin Marketplace (Recommended)

Install via Claude Code's plugin system:

```bash
# Add the marketplace
/plugin marketplace add Randroids-Dojo/Godot-Claude-Skills

# Install the plugin
/plugin install godot-skills
```

The skills will be automatically available in all your Claude Code sessions.

### Option 2: Personal Installation

Install skills for all your projects:

```bash
# Clone this repo
git clone https://github.com/Randroids-Dojo/Godot-Claude-Skills.git

# Copy to personal skills directory
cp -r Godot-Claude-Skills/skills/godot ~/.claude/skills/
```

### Option 3: Project-Level Installation

Install skills for a specific project (shared with team via git):

```bash
# Clone this repo
git clone https://github.com/Randroids-Dojo/Godot-Claude-Skills.git

# Copy to project skills directory
mkdir -p your-project/.claude/skills
cp -r Godot-Claude-Skills/skills/godot your-project/.claude/skills/
```

### Verifying Installation

After installation, Claude will automatically discover the skill when you work on Godot projects. You can verify by asking Claude about GdUnit4 testing or Godot exports.

## CI/CD

This repository includes GitHub Actions CI that:

1. **Installs Claude CLI** - Sets up `@anthropic-ai/claude-code` via npm
2. **Installs Godot Engine** - Sets up Godot 4.3.0 with export templates
3. **Installs GdUnit4** - Clones testing framework into example project
4. **Runs Tests** - Executes all GdUnit4 unit and integration tests
5. **Builds Web Export** - Creates deployable web build
6. **Deploys to Vercel** - Automatic deployment on merge to main (optional)

The CI runs on:
- Push to `main`/`master` branches
- Pull requests to `main`/`master` branches
- Manual trigger via `workflow_dispatch`

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
