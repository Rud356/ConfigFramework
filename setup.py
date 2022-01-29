import setuptools
import config_framework

with open('README.md') as f:
    text = f.read()

with open("requirements.txt") as requirement_f:
    requirements = [line.strip() for line in requirement_f.readlines()]

with open("dev-requirements.txt") as dev_requirement_f:
    dev_requirements = [line.strip() for line in dev_requirement_f.readlines()]

setuptools.setup(
    name="ConfigFramework",
    version=config_framework.__version__,
    author="Rud356",
    author_email="rud356github@gmail.com",
    description="A small framework to build your flexible project configurations",
    long_description=text,
    long_description_content_type="text/markdown",
    license="GPLv3",
    url="https://github.com/Rud356/ConfigFramework",
    packages=setuptools.find_packages(exclude=["tests", "examples"]),
    install_requires=requirements,
    extras_require={
        'mypy': ["mypy", "types-PyYAML"],
        'dev': dev_requirements
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
