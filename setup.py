from setuptools import setup, find_packages

setup(
    name="anthropic-client",
    version="0.1.0",
    packages=find_packages(where="src/python"),
    package_dir={"": "src/python"},
    install_requires=[
        "sentence-transformers",
        "numpy",
        "networkx",
        "nltk",
        "scipy",
        "pandas"
    ],
    python_requires=">=3.7",
)