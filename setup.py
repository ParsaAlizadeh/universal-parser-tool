from setuptools import setup, find_packages
from upt import __name__, __version__

with open('README.md') as readme_file:
    README = readme_file.read()

setup(
    name=__name__,
    version=__version__,
    description='Useful tool to speedup testing codes in cp-programming',
    license='GPL',
    author='Parsa Alizadeh',
    author_email="parsa.alizadeh1+upt@gmail.com",
    url='https://github.com/ParsaAlizadeh/universal-parser-tool',
    long_description_content_type="text/markdown",
    long_description=README + '\n',
    packages=find_packages(include=['upt', 'upt.*']),
    install_requires=[
        'selenium',
        'requests',
        'bs4',
        'markdown',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['upt=upt:main']
    }
)
