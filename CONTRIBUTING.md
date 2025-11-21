# Contributing to Content Quality Audit Tool

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Getting Started

1. **Fork the Repository**
   - Click the "Fork" button at the top right of the repository page

2. **Clone Your Fork**
   ```bash
   git clone https://github.com/your-username/Content_Audit_Tool.git
   cd Content_Audit_Tool
   ```

3. **Set Up Development Environment**
   ```bash
   # Backend
   cd backend
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt

   # Frontend
   cd ../frontend
   npm install
   ```

4. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Guidelines

### Code Style

**Python (Backend)**
- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and modular

**JavaScript/React (Frontend)**
- Use functional components with hooks
- Follow React best practices
- Use Tailwind CSS for styling
- Keep components small and reusable

### Commit Messages

Use clear and descriptive commit messages:

```
feat: Add sentiment analysis module
fix: Resolve SERP scraping timeout issue
docs: Update API documentation
style: Format code according to PEP 8
refactor: Restructure analyzer modules
test: Add unit tests for SEO analyzer
```

### Adding New Features

1. **Create an Issue**
   - Describe the feature
   - Explain the use case
   - Wait for maintainer feedback

2. **Write Code**
   - Follow existing code patterns
   - Add comments for complex logic
   - Ensure backward compatibility

3. **Add Tests** (when applicable)
   - Write unit tests for new functions
   - Ensure existing tests pass

4. **Update Documentation**
   - Update README.md if needed
   - Add docstrings and comments
   - Update API documentation

### Bug Reports

When reporting bugs, include:

- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, Node version)
- Error messages and logs
- Screenshots (if applicable)

## Pull Request Process

1. **Update Your Fork**
   ```bash
   git fetch upstream
   git merge upstream/main
   ```

2. **Test Your Changes**
   - Run the application locally
   - Test all affected features
   - Check for console errors

3. **Create Pull Request**
   - Use a clear title
   - Describe your changes
   - Reference related issues
   - Add screenshots for UI changes

4. **Code Review**
   - Address reviewer feedback
   - Make requested changes
   - Keep discussions professional

5. **Merge**
   - Maintainers will merge after approval
   - Delete your branch after merge

## Project Structure

```
Content_Audit_Tool/
├── backend/
│   ├── analyzers/      # Analysis modules (add new analyzers here)
│   ├── utils/          # Utility functions
│   └── app.py          # Main Flask app
└── frontend/
    └── src/
        └── components/ # React components (add new UI here)
```

## Checklist Before Submitting PR

- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] No sensitive data (API keys, credentials) in code
- [ ] Changes are tested locally
- [ ] PR description is complete

## Found a Security Issue?

Please **do not** create a public issue. Instead:

1. Email the maintainers directly
2. Include detailed information
3. Allow time for a fix before public disclosure

## Questions?

- Open a Discussion for general questions
- Create an Issue for bug reports or feature requests
- Check existing Issues and Discussions first

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to make this project better!
