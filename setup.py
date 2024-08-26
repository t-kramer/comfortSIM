from setuptools import setup, find_packages

setup(
    name="comfortSIM",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        # Add other dependencies here
    ],
    python_requires=">=3.6",
    author="Tobias Kramer",
    author_email="t.kramer@berkeley.com",
    description="A Python library for thermal comfort simulation and analysis.",
    url="https://github.com/t-kramer/comfort-sim",
    license="MIT",
)
