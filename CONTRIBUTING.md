# Contributing to Wagtail Image From URL

Thank you for your interest in contributing to Wagtail Image From URL! We welcome contributions from the community.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue on GitHub with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Your environment (Python version, Django version, Wagtail version)
- Any relevant logs or screenshots

### Suggesting Features

We love new ideas! Please open an issue with:
- A clear description of the feature
- Why this feature would be useful
- Any implementation ideas you have

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes**
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed
3. **Test your changes**
   ```bash
   pytest
   ```
4. **Ensure code quality**
   ```bash
   # Format code
   black image_url_upload tests
   
   # Check for issues
   flake8 image_url_upload tests
   ```
5. **Commit your changes**
   - Use clear, descriptive commit messages
   - Reference any related issues
6. **Push to your fork** and submit a pull request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/wagtail-image-from-url.git
cd wagtail-image-from-url

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest
```

## Code Style

- Follow PEP 8 guidelines
- Use Black for code formatting (line length: 120)
- Write docstrings for public functions and classes
- Add type hints where appropriate
- Keep functions focused and single-purpose

## Testing

- Write tests for new features
- Ensure existing tests pass
- Aim for high test coverage
- Test edge cases and error conditions

## Documentation

- Update README.md if adding features
- Add docstrings to new functions/classes
- Include code examples where helpful
- Update CHANGELOG.md

## Code Review Process

All pull requests will be reviewed by maintainers. We may suggest changes or improvements. Please be patient and responsive to feedback.

## Questions?

Feel free to open an issue or reach out on the Wagtail Slack #packages channel.

Thank you for contributing! 🎉

