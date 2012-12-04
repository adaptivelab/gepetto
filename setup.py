from setuptools import setup

setup(
    name='Gepetto',
    version='0.1',
    packages=['gepetto'],
    install_requires=['boto'],
    include_package_data=True,
    zip_safe=False,
)
