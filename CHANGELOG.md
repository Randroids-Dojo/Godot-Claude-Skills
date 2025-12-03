# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-03

### Added

- **Godot Skill** (`skills/godot/`)
  - GdUnit4 testing integration with scene runner and input simulation
  - Web/desktop export support via helper scripts
  - CI/CD pipeline configuration for GitHub Actions and GitLab CI
  - Deployment guides for Vercel, GitHub Pages, and itch.io
  - Python helper scripts: `run_tests.py`, `parse_results.py`, `export_build.py`, `validate_project.py`
  - Reference documentation for GdUnit4 quickstart, assertions, scene runner API

- **Example Test Skill** (`skills/example-test/`)
  - Simple example skill demonstrating skill structure and format
  - Basic Godot project validation and log analysis

- **Example Project** (`example-project/`)
  - Tic-Tac-Toe game for testing skills in CI
  - Full GdUnit4 test suite with unit and integration tests
  - Web export preset configuration
  - Vercel deployment configuration with CORS headers

- **CI/CD Workflow** (`.github/workflows/ci.yml`)
  - Automated testing with GdUnit4
  - Web build generation
  - Optional Vercel deployment (production and PR previews)

- **Plugin Structure**
  - `.claude-plugin/plugin.json` for marketplace metadata
  - `.claude-plugin/marketplace.json` for registry discovery
  - MIT License

### Documentation

- Comprehensive README with installation instructions
- PlayGodot architecture document for future external automation framework
