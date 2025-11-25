from setuptools import setup, find_packages

setup(
    name="pgx_toolkit",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "networkx",
        "matplotlib",
        "numpy",
        "scipy"
    ],
    extras_require={
        "docs": [
            "mkdocs",
            "mkdocs-material",
            "mkdocstrings[python]"
        ]
    },
    author="Antigravity",
    description="A toolkit for personalized pharmacogenomic network analysis.",
)
