import setuptools

# get long description
with open("README.md", "r") as fh:
    long_description = fh.read()

exec(open('sclblpy/version.py').read())

setuptools.setup(
    name="sclblpy",
    version=__version__,
    author="Maurits Kaptein",
    author_email="maurits.kaptein@scailable.net",
    description="Python package for interacting with our API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
	package_data={'': ['glob.json']},
    url="https://github.com/scailable/sclblpy/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests',
        'pyjwt',
      ],
    python_requires='>=3.7',
)