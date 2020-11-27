from setuptools import find_packages, setup


def load(filename):
    return open(filename, "rb").read().decode("utf-8")


version_info = {}
exec(load("gumby/package_version.py"), version_info)

setup(
    name="gumby",
    version=version_info["__version__"],
    description="Stretch polygonal meshes in segments along an axis",
    long_description=load("README.md"),
    long_description_content_type="text/markdown",
    author="Metabolize",
    author_email="github@paulmelnikow.com",
    url="https://github.com/lace/gumby",
    packages=find_packages(),
    install_requires=load("requirements.txt"),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Other Audience",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Artistic Software",
        "Topic :: Multimedia :: Graphics :: 3D Modeling",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
)
