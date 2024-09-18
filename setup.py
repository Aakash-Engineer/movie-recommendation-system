from setuptools import setup, find_packages

# Read the requirements from the requirements.txt file
with open('requirements.txt') as f:
    install_requires = f.read().splitlines()
    install_requires.remove('-e .')

setup(
    name='movie_recommendation_system',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=install_requires,
)