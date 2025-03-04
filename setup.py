from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="anthropic-client",
    version="0.1.0",
    author="Ryan Oates",
    author_email="ryanoatsie@outlook.com",
    description="A Python client for the Anthropic Claude API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ryanoates/anthropic_project",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "anthropic>=0.49.0,<0.50",
        "python-dotenv>=1.0.1,<2",
    ],
    entry_points={
        "console_scripts": [
            "claude=cli:main",
        ],
    },
) 