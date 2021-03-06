import os, sys
from setuptools import find_packages, setup


with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()



def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def read_requirements(fname):
    f = open(os.path.join(os.path.dirname(__file__), fname))
    return filter(lambda f: f != '', map(lambda f: f.strip(), f.readlines()))

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-csdt-forums',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',  # example license
    description='A simple Django forums.',
    long_description=read('README.md'),
    install_requires = read_requirements('requirements.txt'),
    url='https://csdt.rpi.edu/',
    author='Ryan Holm',
    author_email='holmr@rpi.edu',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.10',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
