"""
Setup script for FCM Receiver library
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fcm-receiver",
    version="0.1.0",
    author="Agus Ibrahim",
    author_email="hello@agusibrahim.com",
    description="A Python library for receiving Firebase Cloud Messages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/agusibrahim/pyfcm-receiver",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "cryptography>=3.0.0",
        "http-ece>=1.0.5",
        "requests>=2.25.0",
        "pycryptodome>=3.9.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.900",
        ],
    },
    entry_points={
        "console_scripts": [
            "fcm-receiver=fcm_receiver.cli:main",
        ],
    },
)
