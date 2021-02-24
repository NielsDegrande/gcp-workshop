# -*- coding: utf-8 -*-

"""Setup script for the GCP workshop."""

from setuptools import find_packages, setup


def read_file(file_name: str) -> str:
    """Read file and return its content.
    :param file_name: Name of file to be read (at root level).
    :return: Content of file, unprocessed.
    """
    with open(file_name, "r") as file_:
        return file_.read()


setup(
    name="gcp-workshop",
    version="1.0.0",
    description="Minimal API for GCP workshop.",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    url="",
    # Overview: https://pypi.python.org/pypi?:action=list_classifiers.
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.8",
    ],
    keywords=["gcp", "workshop"],
    packages=find_packages(exclude=("tests",)),
    platforms=["Any"],
    python_requires=">=3.8",
    install_requires=read_file("requirements.txt").splitlines(),
    extras_require={"dev": read_file("requirements-dev.txt").splitlines()},
    include_package_data=True,
    entry_points={"console_scripts": ["server = server.__main__:main"]},
    project_urls={"Source": ""},
    license="Other/Proprietary",
)
