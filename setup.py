# ONLY TO RUN TESTS!!
# https://docs.pytest.org/en/6.2.x/goodpractices.html
from setuptools import setup

with open('./requirements.txt', 'r') as f:
    lines = f.readlines()

requirements = list(filter(lambda line: '#' not in line, lines))

setup(
        name='grinx',
        author='Denis Surkov',
        packages=[
            'grinx',
        ],
        install_requires=requirements,
)
