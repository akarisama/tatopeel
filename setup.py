from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='tatopeel',
    version='1.0',
    description='Converts Tatoeba base and sentences files into line delineated parallel corpora for use in deep learning machine translation applications.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/n-win/tatopeel',
    author='Noah Windsor',
    author_email='mail@nwin.me',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Pre-processors',
    ],
    keywords='tatoeba corpus conversion',
    py_modules=['tatopeel'],
    entry_points={
        'console_scripts': [
            'tatopeel=tatopeel:main',
        ],
    },
    test_suite='./tatopeel_test.TatoTest'
)
