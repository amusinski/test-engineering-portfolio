# test-engineering-portfolio
A curated QE/SDET toolkit: test agents, Playwright (Python) automation patterns, scaffolding, and case-study artifacts focused on reliability, observability, and testability.

## What's inside

- **Agents**: structured QA workflows for requirement extraction, risk analysis, and observability gaps
- **Playwright (Python)**: reusable fixtures, page objects, utilities, and CI-friendly patterns
- **Scaffolding**: project templates, conventions, and test data strategies
- **Case Studies**: redacted examples demonstrating testability-first thinking and defect prevention

## Structure

```
├── agents/                  # QA workflow agents (YAML + Markdown)
│   ├── requirement_extraction.md
│   ├── risk_analysis.md
│   └── observability_gaps.md
├── playwright/              # Python Playwright automation framework
│   ├── conftest.py          # Reusable pytest fixtures
│   ├── pyproject.toml       # Project config and dependencies
│   ├── pages/               # Page Object Model classes
│   ├── utils/               # Shared helpers and utilities
│   └── tests/               # Example test suites
├── scaffolding/             # Project bootstrapping resources
│   ├── project_template/    # Opinionated starter template
│   ├── conventions.md       # Naming, structure, and style guide
│   └── test_data_strategies.md
└── case_studies/            # Redacted real-world QA examples
    ├── testability_first.md
    └── defect_prevention.md
```

## Quick Start

```bash
# Install Playwright + dependencies
cd playwright
pip install -e ".[dev]"
playwright install chromium

# Run the example test suite
pytest tests/ -v
```
