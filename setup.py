"""
setup.py - Package configuration
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="automonitor",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Automated news scraping and Telegram messaging bot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/AutoMonitor",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "requests>=2.28.0",
        "beautifulsoup4>=4.11.0",
        "lxml>=4.9.0",
        "selenium>=4.10.0",
        "feedparser>=6.0.0",
        "schedule>=1.2.0",
        "python-dotenv>=1.0.0",
        "twilio>=8.10.0",
        "aiohttp>=3.8.0",
        "pydantic>=2.0.0",
        "pyyaml>=6.0",
        "sqlalchemy>=2.0.0",
        "psycopg2-binary>=2.9.0",
        "flask>=3.0.0",
        "gunicorn>=21.0.0",
    ],
)
