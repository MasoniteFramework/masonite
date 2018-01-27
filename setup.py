from distutils.core import setup
setup(
    name='masonite',
    packages=['masonite',
              'masonite.auth',
              'masonite.facades',
             ],
    version='0.2.10',
    install_requires=[
        'validator.py==1.2.5',
        'cryptography==2.1.4'
    ],
    description='The core for the Masonite ',
    author='Joseph Mancuso',
    author_email='idmann509@gmail.com',
    url='https://github.com/josephmancuso/masonite',  # use the URL to the github repo
    download_url='',
    keywords=['python web framework', 'python3'],  # arbitrary keywords
    classifiers=[],
)
