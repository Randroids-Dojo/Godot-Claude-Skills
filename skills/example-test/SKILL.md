---
name: example-test
description: A simple example skill for testing Godot-related Claude Code workflows. Use this skill when learning how to create and structure skills for Godot game development assistance.
---

# Example Test Skill

This is a starter skill demonstrating the basic structure for Godot-Claude-Skills.

## Purpose

This skill serves as a template and test case for:
- Validating skill loading in Claude Code
- Demonstrating proper SKILL.md format
- Providing a foundation for Godot-specific skills

## Instructions

When this skill is activated:

1. **Acknowledge activation** - Confirm the skill has loaded successfully
2. **Explain capabilities** - Describe what this example skill demonstrates
3. **Guide next steps** - Help users understand how to create their own Godot skills

## Godot Context

This repository is designed for skills related to:
- Godot Engine game development (GDScript, C#)
- Scene and node management
- Game architecture patterns
- Asset pipeline workflows
- Debugging and testing Godot projects

## Example Usage

When a user wants to test skill functionality:

```
User: "Test the example skill"
Claude: "The example-test skill is active. This demonstrates proper skill structure for Godot-Claude-Skills."
```

## Creating New Skills

To add a new skill to this repository:

1. Create a new folder under `/skills/` with your skill name (lowercase, hyphens)
2. Add a `SKILL.md` file with YAML frontmatter (`name` and `description`)
3. Write clear instructions in markdown format
4. Include examples and context relevant to Godot development
