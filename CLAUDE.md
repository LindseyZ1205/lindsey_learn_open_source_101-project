# CLAUDE.md

## Project Overview

`lindsey_learn_open_source_101` is Lindsey Zhang's first open source Python library,
created as a learning project. The core function is `add_two(a, b)` which adds two integers.

## Project Structure

```
lindsey_learn_open_source_101-project/
├── lindsey_learn_open_source_101/   # Main Python package
│   ├── __init__.py
│   ├── api.py                       # Public API (exports add_two)
│   ├── math_utils.py                # Core logic (add_two function)
│   ├── paths.py                     # Centralized path management
│   ├── tests/                       # Package-level test helpers
│   │   ├── __init__.py
│   │   └── helper.py
│   └── vendor/                      # Vendored utilities
│       ├── __init__.py
│       └── pytest_cov_helper.py
├── tests/                           # Unit tests
│   ├── __init__.py
│   ├── test_api.py
│   └── all.py
├── docs/                            # Sphinx documentation
│   └── source/
│       ├── conf.py
│       └── index.rst
├── .github/workflows/main.yml       # GitHub Actions CI
├── .mise/tasks/                     # Automation scripts
├── pyproject.toml                   # Project metadata & dependencies
├── mise.toml                        # Task runner config
└── .coveragerc                      # Coverage config
```

## Common Commands

```bash
# Install dependencies
uv sync --all-extras

# Run tests
.venv/bin/pytest tests -v

# Run with coverage
.venv/bin/pytest tests --cov=lindsey_learn_open_source_101 --cov-report term-missing

# Build docs
.venv/bin/sphinx-build -b html docs/source docs/build/html
```

## Environment

- Python: 3.12 (managed by mise or system)
- Virtual environment: `.venv/`
- Package manager: `uv`
