import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="acceptlang",
    version="0.0.4",
    description="A package for parsing Accept-Language tag received from (untrusted) client context.",  # Optional
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/piotrszyma/acceptlang",
    author="Piotr Szyma",
    author_email="contact@piotrszyma.pl",
    classifiers=[
        "Development Status :: 3 - Alpha",
    ],
    packages=find_packages(include=["acceptlang", "acceptlang/*"]),  # Required
    package_data={"acceptlang": ["py.typed"]},
    python_requires=">=3.7, <4",
    project_urls={
        "Bug Reports": "https://github.com/piotrszyma/acceptlang/issues",
        "Source": "https://github.com/piotrszyma/acceptlang",
    },
)
