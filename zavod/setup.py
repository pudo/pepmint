from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()


setup(
    name="zavod",
    version="0.8.0",
    description="Data factory for followthemoney data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="data mapping identity followthemoney etl parsing",
    author="OpenSanctions",
    author_email="friedrich@opensanctions.org",
    url="https://github.com/opensanctions/opensanctions",
    license="MIT",
    packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
    namespace_packages=[],
    include_package_data=True,
    package_data={"": ["zavod/data/*", "zavod/py.typed"]},
    zip_safe=False,
    install_requires=[
        "followthemoney == 3.6.*",
        "nomenklatura[leveldb] == 3.11.*",
        "plyvel == 1.5.1",
        "redis == 5.0.4",
        "fakeredis == 2.23.2",
        "rigour == 0.5.2",
        "datapatch >= 1.1,< 1.3",
        "fingerprints == 1.2.*",
        "addressformatting == 1.3.*",
        "certifi",
        "colorama",
        "google-cloud-storage",
        "jinja2",
        "types-jinja2",
        "lxml == 5.2.2",
        "openpyxl == 3.1.2",
        "orjson == 3.10.3",
        "ijson > 3.2, < 4.0",
        "pantomime == 0.6.1",
        "prefixdate",
        "psycopg2-binary",
        "pyicu == 2.13.1",
        "pywikibot==9.1.2",
        "requests[security]",
        "requests_oauthlib",
        "sqlalchemy[mypy]",
        "structlog",
        "xlrd == 2.0.1",
        "cryptography",
    ],
    tests_require=[],
    entry_points={
        "console_scripts": [
            "zavod = zavod.cli:cli",
        ],
    },
    extras_require={
        "dev": [
            "black==24.4.2",
            "wheel>=0.29.0",
            "twine",
            "mypy",
            "flake8>=2.6.0",
            "pytest",
            "ruff==0.4.4",
            "pytest-cov",
            "lxml-stubs == 0.5.1",
            "coverage>=4.1",
            "requests-mock",
            "types-setuptools",
            "types-requests",
            "types-openpyxl",
            "types-google-cloud-ndb",
        ],
        "docs": [
            "pillow",
            "cairosvg",
            "mkdocs",
            "mkdocstrings[python]",
            "mkdocs-material",
        ],
    },
)
