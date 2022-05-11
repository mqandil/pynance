from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ['pandas>=1.3.2', 'numpy>=1.21.2', 'yfinance>=0.1.70', 'scipy>=1.7.1', 'plotly>=5.7.0',]

setup(
    name="pynance",
    version="1.0.0",
    author="Matthew Qandil",
    description="A package to Optimize Stock Portfolios",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/mqandil/pynance/",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
    ],
)