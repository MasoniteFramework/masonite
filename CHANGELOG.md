# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Sentimental Versioning](http://sentimentalversioning.org/).

## [2.0.26](https://github.com/MasoniteFramework/core/releases/tag/v2.0.26) - 2018-10-08
### Fixed
- [Fixed passing variables into jobs](https://docs.masoniteproject.com/useful-features/queues-and-jobs#passing-variables-into-jobs)

## [2.0.25](https://github.com/MasoniteFramework/core/releases/tag/v2.0.25) - 2018-10-07
### Added
- [Added 2 new mail drivers: `terminal` and `log`](https://docs.masoniteproject.com/useful-features/mail#terminal-driver)
- [Added `amqp` queue driver and `queue:work` command](https://docs.masoniteproject.com/useful-features/queues-and-jobs#amqp-driver)
- [Added `model:docstring` command](https://docs.masoniteproject.com/useful-features/queues-and-jobs#amqp-driver)

## [2.0.24](https://github.com/MasoniteFramework/core/releases/tag/v2.0.24) - 2018-09-30
### Added
- Added ability to "make" a class from the container
- Added a way to make a full route

## [2.0.23](https://github.com/MasoniteFramework/core/releases/tag/v2.0.23) - 2018-09-16
### Fixed
- Fixed Issue where url parameters were not resetting at the end of each request and being carried over when the second route does not have any URL parameters.

## [2.0.22](https://github.com/MasoniteFramework/core/releases/tag/v2.0.22) - 2018-09-13
### Fixed
- Fixed Issue where multiple select inputs were not fetching all values and also made it so it will fetch via dot notation

## [2.0.21](https://github.com/MasoniteFramework/core/releases/tag/v2.0.21) - 2018-09-13
### Fixed
- Fixed Issue where Masonite was not overriding environment variables that were already set

## [2.0.20](https://github.com/MasoniteFramework/core/releases/tag/v2.0.20) - 2018-09-09
### Added
- Contracts to managers

- Better exception handling for invalid secret keys

- Python 3.7 to travis.yml file

- SSL option in config

- View tests

## Changed
- Made the view class more modular

## [2.0.19](https://github.com/MasoniteFramework/core/releases/tag/v2.0.19) - 2018-09-01
### Fixed
- Fixed Issue where the reset migration command was not throwing `QueryExceptions`.

## [2.0.18](https://github.com/MasoniteFramework/core/releases/tag/v2.0.18) - 2018-08-30
### Fixed
- Fixed Issue where route groups were overriding middleware

## [2.0.17](https://github.com/MasoniteFramework/core/releases/tag/v2.0.17) - 2018-08-27
### Fixed
- Fixed Issue where the autoloader was loading more directories than it was suppose to

## [2.0.16](https://github.com/MasoniteFramework/core/releases/tag/v2.0.16) - 2018-08-22
### Added
- Added docstrings to nearly all classes
- Added container hooks
- Added strict and override options to the container
- Added a validator command
- Added middleware groups
- Added change log
- Added route compilers

## [2.0.15](https://github.com/MasoniteFramework/core/releases/tag/v2.0.15) - 2018-08-12

### Fixed
- Fixed an issue where the craft info command was calling the masonite-cli command prematurely.

## [2.0.14](https://github.com/MasoniteFramework/core/releases/tag/v2.0.14) - 2018-08-08

### Added
- Added casting for validations and added a validation helper
- Added ability to set a dictionary in the session and be able to automatically JSON encode and decode.

### Fixed
- Fixed cryptography dependency
- Fixed issue where URL endpoints could not have - or . in them.

## [2.0.13](https://github.com/MasoniteFramework/core/releases/tag/v2.0.13) - 2018-07-28

### Fixed
- Fixed seed files not being able to import user models
- Fixed models not being able to be created in deeper directories

## [2.0.12](https://github.com/MasoniteFramework/core/releases/tag/v2.0.12) - 2018-07-19

### Fixed
- Fixed exception thrown when a route inside a group route did not have a name but the route did

## [2.0.11](https://github.com/MasoniteFramework/core/releases/tag/v2.0.11) - 2018-07-14

### Fixed
- Made a hot fix for the .env file not being found on some systems

## [2.0.10](https://github.com/MasoniteFramework/core/releases/tag/v2.0.10) - 2018-07-10

### Added

- Added back method to request class
- Added ability to add custom filters
- Added better route groups

## [2.0.9](https://github.com/MasoniteFramework/core/releases/tag/v2.0.9) - 2018-07-06

### Added

- Added a possible default value to the request input
- Added a way to do multiple values in the request.has() method
- Added request route #203
- Added a pop method to request to remove inputs
- Added a url_from_controller method to request
- Added a contain method to request to request
- Added a is named route method to request

## [2.0.8](https://github.com/MasoniteFramework/core/releases/tag/v2.0.8) - 2018-06-26

### Added
- Added craft info command
- Added the ability to add environments to the container and View Class

### Changed
- Moved the route middleware to the top of the container so it can be appended onto by packages.

### Fixed
- Fixed what errors the status code provider is executed on (500 and 404)

## [2.0.7](https://github.com/MasoniteFramework/core/releases/tag/v2.0.7) - 2018-06-24

### Added
- Added warning message to craft serve command if applications are not correctly patched for 2.0

## [2.0.6](https://github.com/MasoniteFramework/core/releases/tag/v2.0.6) - 2018-06-22

### Fixed
- Fixed windows throwing bad exceptions in the exception view

## [2.0.5](https://github.com/MasoniteFramework/core/releases/tag/v2.0.5) - 2018-06-22

### Added
- Added better exception handling for Masonite encrypted key signing

## [2.0.4](https://github.com/MasoniteFramework/core/releases/tag/v2.0.4) - 2018-06-16

### Fixed
- Fixed circular cleo version.

## [2.0.3](https://github.com/MasoniteFramework/core/releases/tag/v2.0.3) - 2018-06-16

### Fixed
- Fixed controller constructors not being resolved by the container

## [2.0.2](https://github.com/MasoniteFramework/core/releases/tag/v2.0.2) - 2018-06-15

### Changed
- Bumped requests version

## [2.0.1](https://github.com/MasoniteFramework/core/releases/tag/v2.0.1) - 2018-06-14

### Added
- Added Tinker Command #116
- Added Show Routes Command #117
- Added Automatic Code Reloading to Serve Command #119
- Added autoloading support #146
- Adds a new get_request_method method to request class
- Adds a new parameter to the all() method to get all the inputs without the framework internals
- Added Masontite Scheduler
- Added Database Seeding Support #168
- Added static file helper #167
- Added Password helper
- Added dot notation to upload drivers
- Added Status Code provider and support #165
- Added support for making location dictionaries to upload drivers
- Adds better .env environment support #172
- Added activate subdomain #173
- Added class based drivers
- Added collect method the he autoload class and changes the return type of instance and collect as well as added an instantiate to the load method #178

### Changed

- Controller constructors are resolved by the container
- Updated all dependencies to latest version.
- Providers now need to be imported into a provider.py file and removed from the application.py file. #177
- Renamed Request.redirectTo to Request.redirect_to #152
- Changed the csrf middleware accordingly.

### Removed
- Removed all duplicated import class names
- Removed need for providers list to also have duplicated class names
- Removed redirection provider completely
- Removed database specific dependencies
    
### Notes
- Need documentation for the new Request.only() method.

## [Older Releases](https://github.com/MasoniteFramework/core/releases?after=v2.0.1)   

    