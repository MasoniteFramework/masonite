from distutils.core import setup
setup(
    name='masonite',
    packages=['masonite',
              'masonite.auth',
              'masonite.cashier',
              'masonite.extensions',
              'masonite.facades',
             ],  # this must be the same as the name above
    version='0.2.8',
    description='The core for the python framework',
    author='Joseph Mancuso',
    author_email='idmann509@gmail.com',
    url='https://github.com/josephmancuso/masonite',  # use the URL to the github repo
    download_url='',
    keywords=['python web framework', 'python3'],  # arbitrary keywords
    classifiers=[],
)
