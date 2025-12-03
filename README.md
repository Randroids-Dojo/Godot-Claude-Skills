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
| `example-test` | A simple example skill for testing and learning the skill format |

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
