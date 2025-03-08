from setuptools import setup, find_packages

setup(
    name="anthropic_client_mojo",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "anthropic>=0.49.0,<0.50",
        "python-dotenv>=1.0.1,<2",
    ],
) 