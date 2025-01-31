from setuptools import setup, find_packages

with open("README.md") as f:
    long_description = f.read()

setup(
    name="lookml-tools",
    version="2.0.5",
    description="Set of tools for handling LookML files: a linter, updater, and grapher",
    url="https://github.com/ww-tech/lookml-tools",
    author="Carl Anderson",
    author_email="carl.anderson@weightwatchers.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache 2.0",
    packages=find_packages(),
    install_requires=["lkml"],
    entry_points={  # Optional
        'console_scripts': [
            'lookml-tools=lkmltools.cli:main',
        ],
    },
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Documentation": "https://ww-tech.github.io/lookml-tools/",
        "Source": "https://github.com/ww-tech/lookml-tools",
    },
)
