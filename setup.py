import setuptools

with open("README.md", "r") as fh:
	L_D = fh.read()

setuptools.setup(
    name="sptm",
    version="0.0.1",
    author="Rochan Avlur Venkat",
    author_email="rochan170543@mechyd.ac.in",
    description="Sentence Topic Prediction using Topic Modeling",
    long_description=L_D,
    long_description_content_type="text/markdown",
    url="https://github.com/Rochan-A/sptm",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
