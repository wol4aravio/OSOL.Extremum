from setuptools import setup, find_packages

setup(
    name="OSOL_Extremum",
    version="0.0.5",

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
        "License :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],

    keywords="",

    packages=find_packages(),

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=["ast2json==0.2.1",
                      "numpy==1.13.1"]
)
