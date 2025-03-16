from setuptools import setup, find_packages

setup(
    name="anthropic-client",
    version="0.1.0",
    packages=find_packages(where="src/python"),
    package_dir={"": "src/python"},
    install_requires=[
        # Core dependencies
        "anthropic>=0.49.0,<0.50",
        "openai>=1.65.5,<2",
        "python-dotenv>=1.0.1,<2",
        
        # HTTP and SSL
        "requests>=2.32.3,<3",
        "httpx>=0.28.1,<0.29",
        "certifi>=2025.1.31,<2026",
        
        # ML and data processing
        "sentence-transformers",
        "numpy",
        "networkx",
        "nltk",
        "scipy",
        "pandas",
        
        # Development dependencies
        "pytest>=8.3.5,<9",
        "pytest-cov>=6.0.0,<7",
        "black>=25.1.0,<26",
        "flake8>=7.1.2,<8",
        "mypy>=1.15.0,<2",
        "mkdocs>=1.6.1,<2"
    ],
    python_requires=">=3.12",  # Updated to match your Python version
    
    # Additional metadata
    description="Anthropic client with Mojo integration",
    author="Surfer12",
    author_email="ryanoatsie@outlook.com",
    url="https://github.com/surfer12/anthropic_project",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.12",
    ],
)