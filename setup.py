from setuptools import setup, find_packages

setup(
    name="json2sql",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "jsonschema",
    ],
    extras_require={
        "dev": [
            "unittest",
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
