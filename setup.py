from setuptools import setup
from masonite.info import VERSION

setup(
    name='masonite',
    packages=[
        'masonite',
        'masonite.auth',
        'masonite.providers',
        'masonite.commands',
        'masonite.drivers',
        'masonite.managers',
        'masonite.testsuite',
        'masonite.queues',
        'masonite.contracts',
        'masonite.contracts.managers',
        'masonite.helpers',
        'masonite.middleware',
        'masonite.testing',
    ],
    version=VERSION,
    install_requires=[
        'masonite-events>=1.0,<2',
        'validator.py>=1.2,<1.3',
        'cryptography>=2.3,<2.4',
        'bcrypt>=3.1,<3.2',
        'requests>=2.0,<2.99',
        'tldextract>=2.2,<2.3',
        'Jinja2>=2,<3',
        'python-dotenv>=0.8,<0.9',
        'passlib>=1.7,<1.8',
        'whitenoise>=3.3',
        'pytest>=3.6,<4',
        'masonite-entry>=0.0.0,<=0.9.99',
        'masonite-scheduler>=1.0.0,<=1.0.99',
        'pendulum>=1.5,<1.6',
        'cleo>=0.6,<0.7',
        'tabulate>=0.8,<0.9',
        'psutil>=5.4,<5.5',
        'orator>=0.9,<1',
        'hupper>=1.0,<2.0'
    ],
    description='The core for the Masonite framework',
    author='Joseph Mancuso',
    author_email='idmann509@gmail.com',
    url='https://github.com/MasoniteFramework/masonite',
    keywords=['masonite', 'python web framework', 'python3'],
    licence='MIT',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'Operating System :: OS Independent',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',


        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    include_package_data=True,
)
