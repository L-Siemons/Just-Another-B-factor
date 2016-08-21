from distutils.core import setup

setup(
    name='just_another_Bfactor',
    version='0.1.0',
    author='L. Siemons',
    author_email='zcbtla0@ucl.ac.uk',
    packages=['just_another_Bfactor',],
    package_data={'just_another_Bfactor': ['resources/*dat']},
    #scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
    url='http://pypi.python.org/pypi/TowelStuff/',
    license='LICENSE.txt',
    description='Colour structures in pymol!',
    long_description=open('README.txt').read(),
    install_requires=[
        "sys",
        "pymol",
        "math",
        "numpy"
    ],
)