import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "Moka",
    version = "0.0.1",
    author = "phzbOx",
    author_email = "phzbox@gmail.com",
    description = ("minimalist functional library"),
    license = "WTFPL",
    keywords = "functional",
    url = "https://github.com/phzbox/moka",
    packages=['moka'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities"])
