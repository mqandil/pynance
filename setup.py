from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ['pandas>=1.3.2', 'numpy>=1.21.2', 'yfinance>=0.1.70', 'seaborn>=0.11.2', 'matplotlib>=3.4.3', 'scipy>=1.7.1', 'plotly>=5.7.0',]

setup(
    name="PortfolioOptimizer",
    version="0.0.2",
    author="Matthew Qandil",
    description="A package to Optimize Stock Portfolios",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/mqandil/PortfolioOptimizer/",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)