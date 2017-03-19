from setuptools import setup

with open("README.md") as f:
    README = f.read()


setup(
    name="permadict",
    version="1.0.0",
    author="Michael V. DePalatis",
    author_email="mike@depalatis.net",
    url="https://github.com/mivade/permadict",
    description="A trivial, persistent, dictionary-like object, backed by SQLite.",
    long_description=README,
    license="Unlicense",
    py_modules=["permadict"],
    tests_require=["pytest"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: Public Domain",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Database"
    ]
)
