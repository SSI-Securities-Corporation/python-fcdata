import re
from setuptools import setup

# python setup.py sdist bdist_wheel
# twine upload dist/*
def _read_long_description():
    try:
        with open("README.md") as fd:
            return fd.read()
    except Exception:
        return None
    


with open("ssi_fc_data/__init__.py", "r") as fd:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE
    ).group(1)


setup(
    name="ssi_fc_data",
    version=version,
    description='FastConnect Data client by Python',
    author="ducdv",
    author_email="ducdv@ssi.com.vn",
    license='MIT',
    platforms=['POSIX', 'Windows'],
    long_description=_read_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/SSI-Securities-Corporation/python-fcdata",
    python_requires='>=3.5',
    install_requires=['requests>=2.18.4', 'websocket-client>=1.5.2'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)