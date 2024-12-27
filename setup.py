# setup.py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="podbro",
    version="0.1.0",
    author="Adetunji Samuel",
    author_email="samadetunji01@gmail.com",
    description="A tool for podcast generation from various content sources",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/detunjisamuel/podbro",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[req for req in open("requirements.txt").read().splitlines() if not req.startswith("#")],
    entry_points={
        "console_scripts": [
            "podbro=podbro.main:app",
        ],
    },
)