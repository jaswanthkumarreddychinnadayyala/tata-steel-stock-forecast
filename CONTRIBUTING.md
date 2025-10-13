# Contributing to Tata Steel Stock Forecasting

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect differing viewpoints and experiences

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear title and description
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version)
- Relevant code snippets or error messages

### Suggesting Enhancements

For feature requests:
- Explain the use case clearly
- Describe the proposed solution
- Consider backwards compatibility
- Note any potential drawbacks

### Pull Requests

1. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/tata-steel-forecast.git
   cd tata-steel-forecast
   ```

2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Set Up Development Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   pip install pytest flake8 black
   ```

4. **Make Your Changes**
   - Follow existing code style
   - Add tests for new features
   - Update documentation as needed
   - Ensure all tests pass

5. **Run Tests and Linting**
   ```bash
   pytest tests/ -v
   flake8 src/ tests/
   black src/ tests/
   ```

6. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Add feature: brief description"
   ```

7. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a Pull Request on GitHub.

## Development Guidelines

### Code Style

- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions focused and modular
- Maximum line length: 127 characters

### Testing

- Write tests for new features
- Ensure tests are reproducible
- Use descriptive test names
- Test edge cases and error conditions
- Maintain test coverage

### Documentation

- Update README.md for user-facing changes
- Add docstrings with parameter descriptions
- Include usage examples
- Update PROJECT_OVERVIEW.md for technical details

### Commit Messages

- Use present tense ("Add feature" not "Added feature")
- Be concise but descriptive
- Reference issues when applicable
- Example: "Fix #123: Handle missing data in feature engineering"

## Areas for Contribution

### High Priority
- [ ] Add more comprehensive unit tests
- [ ] Implement hyperparameter tuning
- [ ] Add model comparison framework
- [ ] Improve error handling and logging

### Medium Priority
- [ ] Add more feature engineering options
- [ ] Implement ensemble methods
- [ ] Add visualization scripts
- [ ] Create Jupyter notebook tutorials

### Advanced Features
- [ ] LSTM/Transformer models
- [ ] Probabilistic forecasting
- [ ] Real-time data integration
- [ ] MLOps pipeline (MLflow, DVC)

## Questions?

Feel free to:
- Open an issue for questions
- Start a discussion on GitHub
- Reach out to maintainers

Thank you for contributing! 🎉
