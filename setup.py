from setuptools import setup, find_packages

setup(
    name="ntwplot-cli",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.0.0",
        "plotext>=5.2.8",
        "icmplib>=3.0.3",
    ],
    entry_points={
        "console_scripts": [
            "ntwplot=src.cli:main",
        ],
    },
)