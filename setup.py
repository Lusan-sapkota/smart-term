"""Setup configuration for smart-term package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="smart-term",
    version="0.1.0",
    author="Lusan Sapkota",
    author_email="sapkotalusan@gmail.com",
    description="AI-powered terminal assistant CLI tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Lusan-sapkota/smart-term",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "ai=smart_term.main:main",
        ],
    },
)
