from setuptools import setup, find_packages
from upt import __version__

with open('README.md') as readme_file:
    README = readme_file.read()

with open('requirements.txt') as req_file:
    requirements = req_file.readlines()

setup(
    name='universal-parser-tool',
    version=__version__,
    description='Useful tool to speedup testing in cp-programming',
    license='GPL-3.0',
    author='Parsa Alizadeh',
    author_email='parsa.alizadeh1@gmail.com',
    url='https://github.com/ParsaAlizadeh/universal-parser-tool',
    long_description_content_type="text/markdown",
    long_description=README + '\n',
    packages=find_packages(include=['upt', 'upt.*']),
    install_requires=requirements,
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['upt=upt.__main__:main']
    }
)
