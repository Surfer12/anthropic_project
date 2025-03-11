from setuptools import setup, find_packages
import os

setup(
    name="anthropic-client",
    version="0.1.0",
    package_dir={"": "src/python"},
    packages=find_packages(where="src/python"),
    install_requires=[
        "anthropic>=0.49.0,<0.50",
        "python-dotenv>=1.0.1,<2",
    ],
    entry_points={
        'console_scripts': [
            'anthropic=anthropic_client.cli:main',
            'claudethink=anthropic_client.cli:main',
        ],
    },
) 