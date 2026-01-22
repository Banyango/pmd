# Contributing to margarita

First off, thank you for considering contributing to margarita! It's people like you that make margarita such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* Use a clear and descriptive title
* Describe the exact steps which reproduce the problem
* Provide specific examples to demonstrate the steps
* Describe the behavior you observed after following the steps
* Explain which behavior you expected to see instead and why
* Include any error messages or stack traces

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* Use a clear and descriptive title
* Provide a step-by-step description of the suggested enhancement
* Provide specific examples to demonstrate the steps
* Describe the current behavior and explain which behavior you expected to see instead
* Explain why this enhancement would be useful

### Pull Requests

* Fill in the required template
* Do not include issue numbers in the PR title
* Follow the Python style guide (PEP 8)
* Include tests for new functionality
* Update documentation as needed
* End all files with a newline

## Development Process

1. Fork the repo and create your branch from `main`
2. Set up your development environment:
   ```bash
   uv sync --dev
   source .venv/bin/activate
   ```
3. Make your changes
4. Run tests:
   ```bash
   uv run pytest
   ```
5. Run linting and formatting:
   ```bash
   uv run ruff format .
   uv run ruff check .
   uv run mypy src/margarita
   ```
6. Commit your changes with a descriptive commit message
7. Push to your fork and submit a pull request

## Style Guide

### Python Style Guide

* Follow PEP 8
* Use type hints for function signatures
* Write docstrings for all public modules, functions, classes, and methods
* Keep functions small and focused
* Use meaningful variable names

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

## Testing

* Write tests for all new functionality
* Ensure all tests pass before submitting a PR
* Aim for high test coverage

## Documentation

* Update the README.md if needed
* Add docstrings to new functions/classes
* Update CHANGELOG.md with your changes

Thank you for contributing! 🎉

