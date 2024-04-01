from setuptools import setup, find_packages

from codecs import open
from os import path

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="poof-util",
    version="0.1.1",
    description="Demo library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Zayd Alzein",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3"    ],
    packages=["poof_util"],
    include_package_data=True,
    install_requires=["requests", "PySocks"],
    test_requires=["requests", "PySocks", "unittest", "pytest"],
    python_requires=">=3.6",
    test_suite="tests"
)