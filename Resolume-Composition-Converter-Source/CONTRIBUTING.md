# Contributing to Resolume Composition Converter

Thank you for considering contributing to Resolume Composition Converter! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to see if the problem has already been reported. When you are creating a bug report, please include as many details as possible:

- **Use a clear and descriptive title** for the issue
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** to demonstrate the steps
- **Describe the behavior you observed** after following the steps
- **Explain which behavior you expected to see instead**
- **Include screenshots or animated GIFs** if possible
- **Include details about your configuration and environment**:
  - Which version of the application are you using?
  - What's the name and version of your OS?
  - What's the version of Resolume Arena you're working with?

### Suggesting Enhancements

Enhancement suggestions are welcome! When suggesting an enhancement, please:

- **Use a clear and descriptive title** for the issue
- **Provide a step-by-step description of the suggested enhancement**
- **Provide specific examples** to demonstrate the steps
- **Describe the current behavior** and **explain which behavior you expected to see instead**
- **Explain why this enhancement would be useful** to most users

### Pull Requests

- Fill in the required template
- Follow the Python style guide
- Document new code
- Include tests when applicable
- End all files with a newline

## Development Environment Setup

1. Fork and clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Development Workflow

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
   or
   ```bash
   git checkout -b fix/your-bugfix-name
   ```

2. Make your changes

3. Test your changes:
   - Run the application locally
   - Ensure it works as expected
   - Check for any errors or warnings

4. Commit your changes:
   ```bash
   git commit -m "Description of your changes"
   ```

5. Push your branch to GitHub:
   ```bash
   git push origin feature/your-feature-name
   ```

6. Create a Pull Request

## Style Guide

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code
- Use 4 spaces for indentation
- Use docstrings for functions and classes
- Keep line length to a maximum of 100 characters

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

## Additional Notes

### Issue and Pull Request Labels

This project uses labels to categorize issues and pull requests:

- `bug`: Indicates a bug or issue
- `enhancement`: Indicates a new feature or enhancement
- `documentation`: Indicates documentation improvements
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed

## Thank You!

Thank you for contributing to Resolume Composition Converter!