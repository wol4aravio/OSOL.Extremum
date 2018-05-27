from setuptools import setup, find_packages

setup(
    name="OSOL_Extremum",
    version="0.1.0",

    description="Computational Center for OSOL.Extremum Project",

    url="https://github.com/wol4aravio/OSOL.Extremum",

    author="Valentin Panovskiy",
    author_email="wol4aravio@yandex.ru",

    license="MIT License",

    classifiers=[
        "Environment :: Console"
        "Development Status :: Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Optimization :: Optimal Control",
        "License :: MIT License"
    ],

    keywords="",

    packages=find_packages(exclude=["tests"]),

    install_requires=["ast2json>=0.2.1",
                      "numpy>=1.13.1",
                      "sympy>=1.1.1",
                      "scipy>=0.19.1",
                      "pandas>=0.20.3",
                      "flask>=0.12.2"],

    entry_points={
        'console_scripts': ['run_core=OSOL_Extremum.computational_core.__main__:main']
    }
)
