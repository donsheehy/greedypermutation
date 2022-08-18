import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="greedypermutation",
    version="0.5.2",
    author="Donald R. Sheehy",
    author_email="don.r.sheehy@gmail.com",
    description="A package for computing greedy permutations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/donsheehy/greedypermutation",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['ds2 >= 0.2.4',
                      'metricspaces',
                      'Click',
                     ],
    extras_require={
        'dev': [
                'sphinx',
                'sphinx-rtd-theme',
                'sphinxcontrib-bibtex',
                'sphinx-click',
                'pytest',
                'pycodestyle',
                'autopep8',
                'pytest-cov',
               ],
        'viz': [
                'ds2viz'
               ]
        },
    entry_points={
        'console_scripts': [
            'greedypermutation=greedypermutation.cli:cli',
        ],
    },
)
