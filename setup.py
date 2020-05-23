import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

meta = {}
with open(os.path.join(here, 'src/masonite', '__version__.py'), 'r') as f:
    exec(f.read(), meta)

try:
    with open('README.md', 'r', encoding='utf-8') as f:
        readme = f.read()
except FileNotFoundError:
    readme = ""
    
setup(
    name=meta['__title__'],
    packages=[
        'masonite',
        'masonite.auth',
        'masonite.auth.guards',
        'masonite.providers',
        'masonite.listeners',
        'masonite.commands',
        'masonite.commands.presets',
        'masonite.controllers',
        'masonite.drivers',
        'masonite.drivers.authentication',
        'masonite.drivers.mail',
        'masonite.drivers.broadcast',
        'masonite.drivers.cache',
        'masonite.drivers.queue',
        'masonite.drivers.session',
        'masonite.drivers.storage',
        'masonite.drivers.upload',
        'masonite.managers',
        'masonite.queues',
        'masonite.contracts',
        'masonite.contracts.managers',
        'masonite.helpers',
        'masonite.middleware',
        'masonite.testing',
    ],
    version=meta['__version__'],
    install_requires=[
        'bcrypt>=3.1,<3.2',
        'cleo>=0.6,<0.7',
        'cryptography>=2.3,<=2.9',
        'hupper<1.10',
        'Jinja2>=2,<3',
        'orator>=0.9,<1',
        'passlib>=1.7,<1.8',
        'pendulum>=1.5,<1.6',
        'psutil>=5.4,<5.7',
        'python-dotenv>=0.8,<0.11',
        'requests>=2.0,<2.99',
        'tabulate>=0.8,<0.9',
        'tldextract>=2.2,<2.3',
        'whitenoise>=3.3,<5',
        'exceptionite>=1.0,<2',
    ],
    description=meta['__description__'],
    long_description_content_type='text/markdown',
    long_description=readme,
    author=meta['__author__'],
    author_email=meta['__author_email__'],
    package_dir={'': 'src'},
    url=meta['__url__'],
    keywords=['masonite', 'python web framework', 'python3'],
    license=meta['__licence__'],
    python_requires=">=3.5",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Masonite',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'craft = masonite.cli:application.run',
        ],
    },
)
