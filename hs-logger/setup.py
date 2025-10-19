from setuptools import (
    setup,
    find_packages,
)


def read(filename):
    with open(filename) as fp:
        return fp.read()


setup(
    name='hs-logger',
    version='0.1.0',
    author='MSL NZ',
    author_email='humidity@measurement.govt.nz',
    url='https://github.com/MSLNZ/hs-logger',
    description='Logging software for Humidity Standards calibrations.',
    long_description=read('README.md'),
    platforms='windows',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: GUI',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Windows',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
        'Topic :: Scientific/Engineering',
    ],
    setup_requires=[],
    tests_require=[],
    install_requires=['numpy', 'matplotlib', 'wxpython==4.0.1', 'serial', 'GitPython', 'pyvisa-py', 'pymodbus', 'thorlabs_apt'],
    extras_require={},
    cmdclass={},
    entry_points={
        'console_scripts': [
            'hs-logger = hs-logger.main_controller:main',
        ],
    },
    packages=find_packages(include=('folder1*',)),
    include_package_data=True,
    zip_safe=False,
)
