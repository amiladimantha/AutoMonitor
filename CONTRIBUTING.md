# Contributing Guide

Thank you for your interest in contributing to AutoMonitor!

## How to Contribute

### 1. Fork the Repository
- Click "Fork" on GitHub
- Clone your fork locally

### 2. Create a Branch
```bash
git checkout -b feature/your-feature-name
```

### 3. Make Changes
- Follow PEP 8 style guide
- Add docstrings to functions
- Update tests for new functionality

### 4. Test Your Changes
```bash
# Run tests
python -m pytest tests/

# Check code style
pylint src/
```

### 5. Submit Pull Request
- Push your branch to your fork
- Create Pull Request with clear description
- Link any related issues

## Development Setup

```bash
# Clone the repo
git clone https://github.com/yourusername/AutoMonitor.git
cd AutoMonitor

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dev dependencies
pip install -r requirements.txt
pip install pytest pylint black

# Copy env template
cp .env.example .env

# Run application
python src/main.py
```

## Code Style

- Use 4 spaces for indentation
- Follow PEP 8
- Use type hints
- Write docstrings for all functions

## Areas for Contribution

### New Scrapers
Add scrapers for new news categories:
- Sports news
- Finance updates
- Entertainment news
- Health and medical breakthroughs

### Improvements
- Better error handling
- Performance optimization
- Caching mechanisms
- Database persistence

### Documentation
- Add API documentation
- Create usage examples
- Improve README
- Add inline code comments

### Bug Reports
Found a bug? Create an issue with:
- Description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details

## Testing

New features should include tests:

```python
# tests/test_scrapers.py
def test_tech_scraper():
    scraper = TechScraper()
    articles = scraper.scrape()
    assert isinstance(articles, list)
    assert len(articles) > 0
```

## Questions?

- Check existing issues/discussions
- Create a new discussion for questions
- Open an issue for bugs

---

All contributors are expected to follow the Code of Conduct.
