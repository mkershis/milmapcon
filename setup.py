from setuptools import find_packages, setup

with open("README.md","r") as file:
    long_description = file.read()

setup(
    name="milmapcon",
    version="1.0.0",
    description="A coordinate converter built on pyproj to convert WWII-era map grid coordinates to latitude & longitude",
    #package_dir={"":"/"},
    packages=find_packages(),
    package_data={'milmapcon':['gs_data.db']},
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mkershis/milmapcon",
    author="Matt Kershis",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    install_requires=["pyproj>=3.6.1","certifi>=2024.12.14","pathlib>=1.0.1"],
    python_requires=">=3.11.7"
)