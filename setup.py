from setuptools import setup

from runner import Runner


setup(
    name='Emerald',
    version='0.1',
    packages=['pyemerald'],
    url='github.com/okielife/Emerald',
    license='',
    author='Edwin Lee',
    author_email='',
    description='',
    cmdclass={
        'run': Runner,
    },
)
