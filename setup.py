from setuptools import setup


setup(
    name='requestify',
    version='0.0.1',
    url='https://github.com/ggabarrin/requestify',
    license='MIT License',
    author='Guillermo Gabarrin',
    install_requires=[
        'Jinja2>=2.10',
    ],
    author_email='g.gabarrin@gmail.com',
    description='Generate request code from raw HTTP request',
    packages=['requestify'],
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Programming Language :: Python',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'License :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
)
