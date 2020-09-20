#!/usr/bin/env python
import io
import os
import re


from setuptools import setup, find_packages

module_path = os.path.dirname(__file__)

with io.open(os.path.join(module_path, "invoice_gui/__init__.py"), "rt", encoding="utf8") as f:
    version = re.search(r"__version__ = \"(.*?)\"", f.read()).group(1)

with io.open(os.path.join(module_path, "./README.rst"), "rt", encoding="utf8") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="Invoice GUI",
    version=version,
    project_urls={
        "Source Code": "https://github.com/molitoris/invoice_gui"
    },
    author="Rafael S. Müller",
    author_email="rafa.molitoris@gmail.com",
    description="GUI to generate invoice and QR payment slip",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/x-rst",
    packages=find_packages(),
    install_requires=[
        "setuptools~=49.2.0",
        "pyyaml~=5.3.1",
        "invoice~=0.1.0"
    ],
    keywords="Invoice QR Payment Slip bill swiss payment GUI",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
    ],
    test_suite="tests"
)
