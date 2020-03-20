import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sclblpy",
    version="0.0.2",
    author="Maurits Kaptein",
    author_email="maurits.kaptein@scailable.net",
    description="Python package for uploading models to Scailable toolchain.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/scailable/sclblpy/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
