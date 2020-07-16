from setuptools import setup, find_packages


with open('README.md') as readme_file:
    README = readme_file.read()

with open("VERSION") as version_file:
    version = version_file.read()

setup(
    name='universal-parser-tool',
    version=version,
    description='Useful tool to speedup testing codes in cp-programming',
    license='GPL',
    author='Parsa Alizadeh',
    url='https://github.com/ParsaAlizadeh/universal-parser-tool',
    long_description_content_type="text/markdown",
    long_description=README + '\n',
    packages=find_packages(include=['upt', 'upt.*']),
    install_requires=[
        'selenium',
        'requests'
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['upt=upt:main']
    }
)
