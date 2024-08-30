from setuptools import setup, find_packages

setup(
    name="pyiBook",
    version="0.4",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'rich',
        'pandas',
        'requests',
        'openpyxl'
        # Add any other dependencies here
    ],
    entry_points={
        'console_scripts': [
            'pyiBook = pyiBook.__init__:cli',
        ],
    },
    author="Tess",
    description="A CLI tool for interacting with iBooks library.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/higher-bottle/pyiBook",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
