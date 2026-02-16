# API Automation Framework for ReqRes & JSONPlaceholder (REST API)

## Project Overview
A production-grade, maintainable API automation framework built with Python, Requests, and Pytest, designed to test core REST API functionalities across two mock platforms (ReqRes for auth validation, JSONPlaceholder for business parameter association). This framework follows industry best practices for API test automation, integrates structured logging for debugging, and leverages GitHub Actions for CI/CD to ensure test reliability, traceability, and seamless collaboration—aligned with enterprise QA standards for remote teams.

The framework focuses on two critical API testing scenarios: authentication token association and business parameter correlation, with a focus on reusability, environment compatibility (local/CI), and clear reporting for enterprise-level QA workflows.

## Tech Stack & Dependencies

### Core Technologies
- Programming Language: Python 3.9
- HTTP Client: Requests 2.31.0
- Testing Framework: Pytest 7.4.3
- Logging: Python Standard Library logging
- Reporting Tool: Pytest-HTML 4.0.2
- CI/CD Integration: GitHub Actions
- Design Pattern: Modular Request Wrapper

### Key Dependencies
pytest==7.4.3
requests==2.31.0
pytest-html==4.0.2
pytest-metadata==3.0.0
ghp-import==2.1.0

## Project Structure (Modular Architecture)
The framework follows a modular, maintainable structure that separates configuration, request logic, and test cases for scalability and ease of maintenance:

api-automation-rest/
├── .github/
│   └── workflows/
│       └── api-test.yml
├── common/
│   └── request.py
├── config/
│   ├── config.py
│   └── log_config.py
├── tests/
│   ├── test_reqres_auth.py
│   └── test_jsonplaceholder_business.py
├── public/
│   ├── test-report.html
│   └── logs/
├── requirements.txt
└── README.md

### Key Module Explanations
- common/request.py: Encapsulates all HTTP request logic (GET/POST), auth token handling, and scenario switching to reduce code duplication and ensure consistent request formatting.
- config/config.py: Centralized configuration for base URLs, test credentials, request timeouts, and report paths—eliminates hardcoding and enables easy environment switching.
- config/log_config.py: Structured logging setup with dual handlers (console for debugging, file for persistence) and standardized log formatting.
- tests/test_reqres_auth.py: Test cases for authentication token association with local/CI environment compatibility and mock token fallback.
- tests/test_jsonplaceholder_business.py: Test cases for business parameter correlation with stable, rate-limit-free execution.
- .github/workflows/api-test.yml: GitHub Actions workflow to run tests automatically, generate reports and logs, and deploy to GitHub Pages.

## Core Test Scenarios Covered

### ReqRes Authentication Association
- Token Generation: Automated login with configurable credentials, with fallback to mock token for CI environments.
- Protected Endpoint Validation: Positive and negative test cases to verify authorization mechanism.
- Token Isolation: Fixture-based token management for test independence and reusability.

### JSONPlaceholder Business Parameter Association
- Single-Layer Correlation: Create post, extract postId, query related comments.
- Multi-Layer Correlation: Get post, extract userId, query associated user.
- Response Validation: Assert status codes, parameter consistency, and response structure.

## How to Run the Tests

### Prerequisites
1. Install Python 3.9 or above.
2. Clone the repository.
3. Install dependencies: pip install -r requirements.txt.
4. Configuration is ready to use with default mock values.

### Run Tests Locally
- Run all tests: pytest tests/ -v
- Run tests with HTML report: pytest tests/ -v --html=public/test-report.html --self-contained-html
- View execution logs in public/logs/api_test_latest.log

### CI/CD with GitHub Actions
Tests are triggered automatically on:
- Push to the main branch
- Pull Request to the main branch

### CI/CD Workflow Steps
1. Checkout repository code
2. Set up Python environment and install dependencies
3. Create output directory for reports and logs
4. Execute all API test cases
5. Upload test artifacts as backup
6. Deploy report and logs to GitHub Pages
7. Output online access links for quick verification

## Framework Highlights (Best Practices)
- Modular Request Wrapper: Separates HTTP logic from test cases for cleaner code and easier maintenance.
- Environment Compatibility: Supports both local and CI execution with automatic mock token fallback.
- Structured Logging: Dual-handler logging system for real-time debugging and persistent records.
- CI/CD Optimization: Cached dependencies, self-contained reports, and Pages deployment for team collaboration.
- Test Isolation: Fixture-based setup and teardown to ensure independent, stable test execution.
- Minimal Dependencies: No redundant packages for fast installation and consistent behavior.
- Enterprise-Grade Configuration: Centralized config file for easy scaling and environment management.

## Test Reporting & Logging
### HTML Test Report
- Self-contained HTML report with full test results and execution details.
- Accessible online via GitHub Pages at https://<username>.github.io/<repository-name>/test-report.html.

### Structured Logs
- Console output for real-time debugging.
- File logs with timestamps, modules, and levels for traceability.
- Latest log file available online at https://<username>.github.io/<repository-name>/logs/api_test_latest.log.

## Troubleshooting
- Test Failures: Review log files in public/logs for detailed request/response information.
- CI Permission Issues: Ensure workflow permissions are set to Read and write in GitHub repository settings.
- Mock Token Behavior: Mock tokens return 401 in CI (expected behavior), real tokens return 200 locally.
- GitHub Pages Access: Confirm the gh-pages branch exists and is set as the source in repository Settings → Pages.
- Dependency Conflicts: Use the provided requirements.txt to install exact versions and avoid conflicts.

## Future Enhancements
- Add support for PUT, DELETE, PATCH methods to cover full CRUD operation validation.
- Implement parallel test execution (pytest-xdist) to reduce overall test runtime.
- Integrate JSON schema validation to ensure API responses match expected structures.
- Add Slack/email notifications for real-time test result alerts.
- Extend test coverage to additional public mock APIs (e.g., Restful Booker).
- Implement parameterized testing with CSV/JSON test data for edge case validation.
