#!/bin/bash
# Run the Godot game using Claude Code with the godot skill
#
# Usage:
#   ./scripts/run-with-claude.sh [prompt]
#
# Example:
#   ./scripts/run-with-claude.sh "Run the tic-tac-toe game and take a screenshot"
#
# Requirements:
#   - Claude Code CLI installed: npm install -g @anthropic-ai/claude-code
#   - ANTHROPIC_API_KEY environment variable set
#   - Godot installed and in PATH

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Default prompt if none provided
PROMPT="${1:-Run the example-project game headlessly and verify it starts correctly}"

# Ensure the skill is available in .claude/skills/ for project-level discovery
SKILL_SOURCE="$PROJECT_DIR/skills/godot"
SKILL_DEST="$PROJECT_DIR/.claude/skills/godot"

if [ -d "$SKILL_SOURCE" ] && [ ! -e "$SKILL_DEST" ]; then
    echo "Linking godot skill to .claude/skills/..."
    mkdir -p "$PROJECT_DIR/.claude/skills"
    ln -s "$SKILL_SOURCE" "$SKILL_DEST"
fi

cd "$PROJECT_DIR"

echo "Running Claude Code with prompt: $PROMPT"
echo "---"

# Run Claude Code in print mode (non-interactive)
# --print outputs only the final response
# --dangerously-skip-permissions skips permission prompts for CI
claude --print --dangerously-skip-permissions "$PROMPT"
