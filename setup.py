from setuptools import setup, find_packages

setup(
    name="finscraper",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "yfinance",
        "pandas",
        "requests"
    ],
) 