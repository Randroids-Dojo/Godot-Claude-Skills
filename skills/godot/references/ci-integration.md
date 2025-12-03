# CI Integration for GdUnit4

## GitHub Actions

### Basic Workflow

```yaml
name: Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Godot
        uses: chickensoft-games/setup-godot@v2
        with:
          version: 4.3.0
          use-dotnet: false

      - name: Import Project
        run: godot --headless --import --path . --quit || true

      - name: Run Tests
        run: |
          godot --headless --path . \
            -s res://addons/gdUnit4/bin/GdUnitCmdTool.gd \
            --run-tests \
            --report-directory ./reports

      - name: Upload Results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: test-results
          path: reports/
```

### With Test Results Reporting

```yaml
      - name: Run Tests
        run: |
          godot --headless --path . \
            -s res://addons/gdUnit4/bin/GdUnitCmdTool.gd \
            --run-tests \
            --report-directory ./reports

      - name: Publish Test Results
        uses: EnricoMi/publish-unit-test-result-action@v2
        if: always()
        with:
          files: reports/**/*.xml
```

### Using Helper Script

```yaml
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Run Tests
        run: |
          python skills/godot/scripts/run_tests.py \
            --project . \
            --report ./reports \
            --verbose

      - name: Parse Results
        if: always()
        run: |
          python skills/godot/scripts/parse_results.py \
            ./reports \
            --format markdown >> $GITHUB_STEP_SUMMARY
```

## GitLab CI

```yaml
test:
  image: barichello/godot-ci:4.3
  stage: test
  script:
    - godot --headless --import --path . --quit || true
    - godot --headless --path .
        -s res://addons/gdUnit4/bin/GdUnitCmdTool.gd
        --run-tests
        --report-directory ./reports
  artifacts:
    when: always
    reports:
      junit: reports/**/*.xml
```

## Command Line Options

```bash
godot --headless --path PROJECT_PATH \
    -s res://addons/gdUnit4/bin/GdUnitCmdTool.gd \
    OPTIONS
```

### Available Options

| Option | Description |
|--------|-------------|
| `--run-tests` | Run all tests |
| `--add PATH` | Add specific test file or directory |
| `--ignore PATH` | Ignore test file or directory |
| `--report-directory DIR` | Output JUnit XML to directory |
| `--continue-on-failure` | Don't stop on first failure |
| `--verbose` | Verbose output |

### Examples

```bash
# Run all tests
--run-tests

# Run specific test file
--run-tests --add res://test/game_test.gd

# Run tests in directory
--run-tests --add res://test/unit/

# Ignore slow tests
--run-tests --ignore res://test/integration/

# Multiple filters
--run-tests --add res://test/unit/ --ignore res://test/unit/slow_test.gd
```

## JUnit XML Output

GdUnit4 generates JUnit XML format compatible with most CI systems:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<testsuites>
  <testsuite name="game_test" tests="3" failures="1" errors="0" time="0.5">
    <testcase name="test_initial_state" classname="game_test" time="0.1"/>
    <testcase name="test_make_move" classname="game_test" time="0.2"/>
    <testcase name="test_win_detection" classname="game_test" time="0.2">
      <failure message="Expected 'X' but was 'O'">
        Assertion failed at line 45
      </failure>
    </testcase>
  </testsuite>
</testsuites>
```

## Handling Failures

### Exit Codes

- `0` - All tests passed
- `1` - One or more tests failed

### Fail Fast vs Continue

```bash
# Stop on first failure (default)
--run-tests

# Continue running all tests
--run-tests --continue-on-failure
```

## Timeouts

Set workflow timeout to prevent hanging:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 10  # Fail if tests take > 10 minutes
```

## Caching

Speed up CI by caching Godot:

```yaml
      - name: Cache Godot
        uses: actions/cache@v4
        with:
          path: ~/.local/share/godot
          key: godot-4.3.0-${{ runner.os }}
```

## Matrix Testing

Test on multiple Godot versions:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        godot-version: ['4.2.0', '4.3.0']

    steps:
      - uses: chickensoft-games/setup-godot@v2
        with:
          version: ${{ matrix.godot-version }}
```

## Debugging CI Failures

### Enable Verbose Output

```bash
godot --headless --verbose --path . \
    -s res://addons/gdUnit4/bin/GdUnitCmdTool.gd \
    --run-tests
```

### Capture Screenshots

```gdscript
func test_visual_state() -> void:
    await runner.await_idle_frame()

    # Capture for debugging
    var image = runner.get_viewport().get_texture().get_image()
    image.save_png("test_screenshot.png")
```

Then upload as artifact:

```yaml
      - name: Upload Screenshots
        uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: screenshots
          path: "*.png"
```

## Common CI Issues

### Issue: Tests Hang

Add timeout and use `--headless`:

```yaml
      - name: Run Tests
        timeout-minutes: 5
        run: godot --headless --path . ...
```

### Issue: Import Errors

Run import step before tests:

```yaml
      - name: Import Project
        run: godot --headless --import --path . --quit || true
```

### Issue: Display Errors

Ensure headless mode or use xvfb:

```yaml
      - name: Run Tests
        run: xvfb-run godot --path . ...
```

### Issue: Missing Addons

Ensure GdUnit4 is committed or installed:

```yaml
      - name: Install GdUnit4
        run: |
          git clone --depth 1 https://github.com/MikeSchulze/gdUnit4.git addons/gdUnit4
```
