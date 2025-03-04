from setuptools import setup, find_packages

# Read version from __init__.py
with open("anthropic_client/anthropic_client/__init__.py", "r") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"').strip("'")
            break

# Read README for long description
with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="anthropic-client",
    version=version,
    description="A Python client for interacting with Anthropic's Claude models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Ryan Oates",
    packages=find_packages(),
    install_requires=[
        "anthropic>=0.18.1",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "claude=anthropic_client.cli:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
) 