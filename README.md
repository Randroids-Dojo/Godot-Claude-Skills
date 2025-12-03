# Godot-Claude-Skills

A collection of Claude Code skills for Godot Engine game development.

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
│   ├── scenes/
│   │   └── main.tscn
│   └── scripts/
│       └── game.gd
├── skills/
│   ├── example-test/
│   │   └── SKILL.md
│   └── [your-skill]/
│       └── SKILL.md
└── README.md
```

## Available Skills

| Skill | Description |
|-------|-------------|
| `example-test` | Test and validate Godot projects by building, running, and analyzing logs |

## Example Project

The repository includes a **Tic-Tac-Toe** game (`example-project/`) for testing skills:

- **2-player game** with X and O turns
- **Win detection** for rows, columns, and diagonals
- **Draw detection** when board is full
- **Restart functionality**
- **Logging** with `[TicTacToe]` prefix for CI validation

### Running Locally

```bash
# Open in Godot Editor
godot --path example-project --editor

# Run headless (for testing)
godot --headless --path example-project --quit
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

3. Include clear instructions, examples, and context relevant to Godot development

## Usage

To use these skills with Claude Code, reference them in your project or add them to your Claude Code configuration.

## CI/CD

This repository includes GitHub Actions CI that:

1. **Installs Claude CLI** - Sets up `@anthropic-ai/claude-code` via npm
2. **Installs Godot Engine** - Sets up Godot 4.3.0 for headless use
3. **Installs Skills** - Copies skills to `.claude/skills/` directory
4. **Validates Skills** - Checks that all skills have proper YAML frontmatter
5. **Imports Godot Project** - Generates `.godot` cache for the example project
6. **Validates GDScript** - Checks scripts for syntax errors
7. **Runs Headless Test** - Executes game and validates log output

The CI runs on:
- Push to `main`/`master` branches
- Pull requests to `main`/`master` branches
- Manual trigger via `workflow_dispatch`

### Local Development

To set up the environment locally:

```bash
# Install Claude CLI
npm install -g @anthropic-ai/claude-code

# Copy skills to .claude directory
cp -r skills/* .claude/skills/

# Verify skills
find .claude/skills -name "SKILL.md" -type f
```

## Resources

- [Claude Code Skills Documentation](https://www.claude.com/blog/skills)
- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [Godot Engine Documentation](https://docs.godotengine.org/)
