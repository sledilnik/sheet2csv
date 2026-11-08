#!/usr/bin/env python

from setuptools import setup

setup(
    name="sheet2csv",
    version="1.0.7",
    author="sledilnik.org",
    author_email="info@sledilnik.org",
    description="A package to export Google Sheet to CSV via API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sledilnik/sheet2csv",
    project_urls={
        "Bug Tracker": "https://github.com/sledilnik/sheet2csv/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["sheet2csv"],
    python_requires=">=3.6",
    install_requires=[
        "google-api-python-client~=1.12.2",
        "google-auth-httplib2~=0.0.4",
        "google-auth-oauthlib~=0.4.1",
        "python-dateutil~=2.8.1",
        "certifi>=2020.12.5",
    ],
)
