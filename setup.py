from setuptools import setup, find_packages


with open('README.md') as readme_file:
    README = readme_file.read()

setup(
    name='universal-parser-tool',
    version='0.1.5',
    description='Useful tool to speedup testing codes in cp-programming',
    author='Parsa Alizadeh',
    author_email='parsa.alizadeh1@gmail.com',
    url='https://github.com/ParsaAlizadeh/universial-parser-tool',
    long_description_content_type="text/markdown",
    long_description=README + '\n',
    packages=find_packages(include=['upt', 'upt.*']),
    install_requires=[
        'selenium'
    ],
    entry_points={
        'console_scripts': ['upt=upt.__init__:main']
    }
)
