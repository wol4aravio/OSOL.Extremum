"""Setup script."""


from setuptools import find_packages, setup

with open("requirements.txt") as f:
    REQUIRED = f.read().splitlines()

setup(
    name="osol.extremum",
    version="0.1.0",
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
    packages=find_packages(exclude=["tests"]),
    install_requires=REQUIRED,
)
