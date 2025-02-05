from setuptools import setup, find_packages

setup(
    name="nurdsem",
    version="0.1.0",
    description="A NurdRage-themed placeholder text generator with GUI file pickers and robust error handling.",
    author="NurdRage",
    author_email="NurdRageDevelopment@gmail.com",
    packages=find_packages(),
    install_requires=[
        "regex",
    ],
    entry_points={
        "console_scripts": [
            "nurdsem = nurdsem.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
