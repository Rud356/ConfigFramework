import setuptools
import ConfigFramework

with open('README.md') as f:
    text = f.read()

setuptools.setup(
    name="ConfigFramework",
    version=ConfigFramework.__version__,
    author="Rud356",
    author_email="devastator12a@mail.ru",
    description="A small framework to build your flexible project configurations",
    long_description=text,
    long_description_content_type="text/markdown",
    license="GPLv3",
    url="https://github.com/Rud356/ConfigFramework",
    packages=setuptools.find_packages(exclude=["tests"]),
    install_requires=["pyyaml>=5.3.1"],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Natural Language :: English",
    ],
    python_requires=">=3.7"
)
