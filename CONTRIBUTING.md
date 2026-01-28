# Contributing to VisionGuard

Thank you for your interest in contributing to VisionGuard! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/VisionGuard.git`
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit your changes: `git commit -m "Add your feature"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

### Backend Development
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run backend
python main.py
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

## Code Style

### Python (Backend)
- Follow PEP 8 style guide
- Use type hints where appropriate
- Document functions with docstrings
- Keep functions focused and small

### JavaScript/React (Frontend)
- Use functional components with hooks
- Follow React best practices
- Use meaningful variable names
- Keep components small and reusable

## Testing

Before submitting a PR:
1. Test all API endpoints
2. Verify frontend functionality
3. Check responsive design
4. Test authentication flow
5. Verify motion detection works

## Pull Request Guidelines

- Provide a clear description of changes
- Reference related issues
- Include screenshots for UI changes
- Update documentation if needed
- Ensure code passes all tests

## Reporting Issues

When reporting issues, include:
- Clear description of the problem
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Python version, etc.)
- Screenshots if applicable

## Feature Requests

We welcome feature requests! Please:
- Check if feature already exists
- Provide clear use case
- Explain expected behavior
- Consider implementation complexity

## Questions?

Feel free to open an issue for questions or discussions.

Thank you for contributing to VisionGuard! 🛡️
