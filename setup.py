import setuptools
import ConfigFramework

with open('README.md') as f:
    text = f.read()

setuptools.setup(
    name="ConfigFramework",
    version=ConfigFramework.__version__,
    author="Rud356",
    author_email="rud356github@gmail.com",
    description="A small framework to build your flexible project configurations",
    long_description=text,
    long_description_content_type="text/markdown",
    license="GPLv3",
    url="https://github.com/Rud356/ConfigFramework",
    packages=setuptools.find_packages(exclude=["tests"]),
    install_requires=["pyyaml>=5.4.1"],
    extras_require={
        'mypy': ["mypy", "types-PyYAML"],
        'docs': [
            "sphinx~=3.5.2",
            "sphinx-rtd-theme~=0.5.1",
            "Pygments~=2.8.1"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Natural Language :: English",
    ],
    python_requires=">=3.7"
)
