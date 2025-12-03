# Godot-Claude-Skills

A collection of Claude Code skills for Godot Engine game development.

## What are Skills?

Skills are folders of instructions, scripts, and resources that Claude loads dynamically to improve performance on specialized tasks. Each skill contains a `SKILL.md` file with YAML frontmatter and markdown instructions.

## Repository Structure

```
skills/
├── example-test/
│   └── SKILL.md
└── [your-skill]/
    └── SKILL.md
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

## Resources

- [Claude Code Skills Documentation](https://www.claude.com/blog/skills)
- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [Godot Engine Documentation](https://docs.godotengine.org/)
