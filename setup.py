from setuptools import setup, find_packages

setup(
    name="textils",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[line.strip() for line in open("requirements.txt").readlines()],
    author="puigde",
    description="Some custom TeX utils",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/puigde/TeXtils",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
