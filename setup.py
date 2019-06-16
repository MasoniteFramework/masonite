import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

meta = {}
with open(os.path.join(here, 'masonite', '__version__.py'), 'r') as f:
    exec(f.read(), meta)

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name=meta['__title__'],
    packages=[
        'masonite',
        'masonite.auth',
        'masonite.providers',
        'masonite.commands',
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
        'masonite.testsuite',
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
        'cryptography>=2.3,<2.4',
        'hupper>=1.0,<2.0',
        'Jinja2>=2,<3',
        'masonite-events>=1.0,<2',
        'masonite-scheduler>=1.0.0,<=1.0.99',
        'masonite-validation>=2.2.0,<=2.2.99',
        'orator>=0.9,<1',
        'passlib>=1.7,<1.8',
        'pendulum>=1.5,<1.6',
        'psutil>=5.4,<5.5',
        'python-dotenv>=0.8,<0.9',
        'requests>=2.0,<2.99',
        'tabulate>=0.8,<0.9',
        'tldextract>=2.2,<2.3',
        'whitenoise>=3.3',
    ],
    description=meta['__description__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    author=meta['__author__'],
    author_email=meta['__author_email__'],
    url=meta['__url__'],
    keywords=['masonite', 'python web framework', 'python3'],
    licence=meta['__licence__'],
    python_requires=">=3.4",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Masonite',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
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
