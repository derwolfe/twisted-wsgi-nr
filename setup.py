from setuptools import setup, find_packages

version = '0.0.1'

setup(
    name='twisted_wsgi_nr',
    version=version,
    description="test of new relic with falcon wsgi and twisted server",
    long_description="new relic test with falcon wsgi and twisted server",
    author='Chris Wolfe',
    author_email='chriswwolfe@gmail.com',
    url='',
    entry_points={
        'console_scripts': [
            'pleasework = twisted_wsgi_nr.test:run'
        ],
    },
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'falcon',
        'twisted',
        'newrelic',
        'structlog'
    ],
)
