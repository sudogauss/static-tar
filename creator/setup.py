from setuptools import setup, find_packages

setup(
    name='creator',
    version='0.0.1',
    description='A cli used to create cross-compilers and use them to build standalone binaries',
    author='sudogauss',
    author_email='t.liashkevich1772@gmial.com',
    packages=find_packages(),
    install_requires=[
        'blessed',
        'typer',
        'rich',
        'shellingham',
    ],
    entry_points={
        'console_scripts': [
            'creator = creator.creator:run',
        ],
    },
)