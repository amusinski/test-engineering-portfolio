my-feature-tests/
├── conftest.py               # Fixtures (copy from playwright/conftest.py)
├── pyproject.toml            # Project config (copy from playwright/pyproject.toml)
├── .env.example              # Environment variable template
├── pages/
│   ├── __init__.py
│   ├── base_page.py          # Inherit all page objects from this
│   └── home_page.py          # Add one page object per page/feature
├── utils/
│   ├── __init__.py
│   ├── api_client.py         # HTTP client for test setup/teardown
│   └── helpers.py            # Shared utilities
└── tests/
    ├── __init__.py
    └── test_home.py          # Start with smoke tests
