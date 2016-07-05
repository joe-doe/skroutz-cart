try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='skroutz cart',
    version='0.1',
    packages=['.'],
    url='http://localhost:5000',
    license='',
    author='Joe Doe',
    author_email='joe,doe@engineer.com',
    description='skroutz.gr cart',
    install_requires=[
        'flask-restplus',
        'Flask',
        'pymongo',
        'gunicorn',
        'bs4',
        'schedule'
    ]
)