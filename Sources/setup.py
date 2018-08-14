from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="osol.extremum",
    version="0.0.2",

    description="OSOL.Extermum",

    url="https://github.com/wol4aravio/OSOL.Extremum",

    author="Panovskiy Valentin",
    author_email="panovskiy.v@yandex.ru",

    license="MIT License",

    classifiers=[
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
    ],

    keywords="",

    packages=find_packages(),

    install_requires=required

)
