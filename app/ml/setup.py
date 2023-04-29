from setuptools import setup, find_packages

setup(
    name='my_microservice',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'flask',
        'requests',
    ],
)
