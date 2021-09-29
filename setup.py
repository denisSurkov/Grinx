# https://docs.pytest.org/en/6.2.x/goodpractices.html
from setuptools import setup

with open('./requirements.txt', 'r') as f:
    lines = f.readlines()

requirements = list(filter(lambda line: '#' not in line, lines))

setup(
    name='grinx',
    version='0.0.2',
    description='Python async http server',
    author='Denis Surkov',
    packages=[
        'grinx',
    ],
    install_requires=requirements,
)
