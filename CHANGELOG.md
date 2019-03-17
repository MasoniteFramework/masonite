# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Sentimental Versioning](http://sentimentalversioning.org/).

## [2.1.21](https://github.com/MasoniteFramework/core/releases/tag/v2.1.21) - 2019-03-14
### Added
- [Added run_again_on_fail and run_times](https://docs.masoniteproject.com/useful-features/queues-and-jobs#specifying-failed-jobs)

## [2.1.20](https://github.com/MasoniteFramework/core/releases/tag/v2.1.20) - 2019-03-09
### Added
- [Added compact helper](https://docs.masoniteproject.com/the-basics/helper-functions#compact)

### Fixed
- Fixed issue with comments on resource controller being flipped.
- Fixed issue with misspelling of logger

## [2.1.19](https://github.com/MasoniteFramework/core/releases/tag/v2.1.19) - 2019-03-05
### Fixed
* Fixed issue with `.` template splices not working

## [2.1.18](https://github.com/MasoniteFramework/core/releases/tag/v2.1.18) - 2019-03-04
### Added
- Added a `--connection` option to the `model:doctring` command to use other connections

### Fixed
- Fixed issue with csrf not being able to correctly detect csrf wildcard routes.

## [2.1.17](https://github.com/MasoniteFramework/core/releases/tag/v2.1.17) - 2019-02-24
### Added
- [Added `-m` and `-s` to the model command to create a migration or a seed](https://docs.masoniteproject.com/the-craft-command/introduction#model-shortcuts)
- [Added ability to use dot notation to get a dictionary value](https://docs.masoniteproject.com/the-basics/requests#getting-dictionary-input)
- Added google and stack overflow links to the top of the exception page
- [Added optional helper](https://docs.masoniteproject.com/the-basics/helper-functions#optional)

### Changed
- [Changed where cleaning happens in the request class. Can now specify on if you want parameters cleaned.](https://docs.masoniteproject.com/the-basics/requests#input-cleaning)

### Fixed
- Fixed issue with not being able to set 404 status codes

## [2.1.16](https://github.com/MasoniteFramework/core/releases/tag/v2.1.16) - 2019-02-11
### Fixed
- Fixed issue with setting status codes on json responses
- Fixed issue with specifying exempt CSRF protection routes that contained route parameters

## [2.1.15](https://github.com/MasoniteFramework/core/releases/tag/v2.1.15) - 2019-02-10
### Added
- [Added ability to specify a list as the second parameter to routes instead of a dictionary](https://docs.masoniteproject.com/the-basics/requests#route-parsing)
- [Added ability to return a model which then returns a JSON response](https://docs.masoniteproject.com/the-basics/controllers#returning-json)
- [Added ability to show when you have unmigrated migrations](https://docs.masoniteproject.com/the-craft-command/introduction#running-the-wsgi-server)
- [Added improvements to the queue feature](https://docs.masoniteproject.com/useful-features/queues-and-jobs#queues-and-jobs)
- Added ability to pass in default as the driver method to get the default driver.

## [2.1.14](https://github.com/MasoniteFramework/core/releases/tag/v2.1.14) - 2019-02-01
### Fixed
- Fixed issue with login authentication

## [2.1.13](https://github.com/MasoniteFramework/core/releases/tag/v2.1.13) - 2019-01-26
### Fixed
- Fixed issue where a JSON null value could raise an exception 71d9016
- Fixed issue where a body type of 0 would throw an exception with the delete method type 9659363
- Fixed issue where status code could not be set in a controller 5ede5d8

### Added
- Added a better exception when passing in a set instead of a dictionary to the render method. This is a common mistake that would throw an ambiguous error
- [Added route redirection](https://docs.masoniteproject.com/the-basics/routing#redirect-route)

## [2.1.12](https://github.com/MasoniteFramework/core/releases/tag/v2.1.12) - 2019-01-19
### Fixed
- Fixed issue where incoming JSON response would only return the first value in a list.

## [2.1.11](https://github.com/MasoniteFramework/core/releases/tag/v2.1.11) - 2019-01-18
### Fixed
- Fixed issue when cleaning a multi dimensional dictionary

## [2.1.10](https://github.com/MasoniteFramework/core/releases/tag/v2.1.10) - 2019-01-11
### Removed
- Removed ability to set the password column using __password__

## [2.1.9](https://github.com/MasoniteFramework/core/releases/tag/v2.1.9) - 2019-01-11
### Fixed
- Fixed issue with auth requiring a __password__ attribute when it should not have been.

## [2.1.8](https://github.com/MasoniteFramework/core/releases/tag/v2.1.8) - 2019-01-10
### Fixed
- Fixed issue with whitenoise not auto refreshing static files

## [2.1.7](https://github.com/MasoniteFramework/core/releases/tag/v2.1.7) - 2019-01-10
### Fixed
- Fixed issue with storage folder not updating for static assets

## [2.1.6](https://github.com/MasoniteFramework/core/releases/tag/v2.1.6) - 2019-01-09
### Added
- [Added config helper](https://docs.masoniteproject.com/the-basics/helper-functions#config) [#517](https://github.com/MasoniteFramework/core/pull/517)
- [Added ability to use `in` keyword for the container](https://docs.masoniteproject.com/architectural-concepts/service-container#has) [#520](https://github.com/MasoniteFramework/core/pull/520) 
- [Added ability to use multiple columns to authenticate](https://docs.masoniteproject.com/security/authentication#multiple-authentication-columns) [#521](https://github.com/MasoniteFramework/core/pull/521)
- [Added ability to specify the user password column](https://docs.masoniteproject.com/security/authentication#changing-the-authentication-password) [#521](https://github.com/MasoniteFramework/core/pull/521)

## [2.1.5](https://github.com/MasoniteFramework/core/releases/tag/v2.1.5) - 2019-01-03
### Fixed
- Fixed issue with LoginController not working properly because of incorrectly specified input
- Fixed issue with view render method storing variables from previous renders
- Fixed issue with s3 not working properly when using both location and filename
- Fixed issue with Amazon S3 storing all files in root directory

### Changed
- Changed how S3 temporarily stores file uploads
- Changed where the exception is thrown in the s3 driver to prevent a temporary file being saved before uploading if the driver is not installed.

### Added
- Added the ability for disk driver to create directories if they do not exist

## [2.1.4](https://github.com/MasoniteFramework/core/releases/tag/v2.1.4) - 2018-12-30
### Fixed
- Fixed issue where uploading a file resulted in None being returned.

## [2.1.3](https://github.com/MasoniteFramework/core/releases/tag/v2.1.3) - 2018-12-22
### Security
- Fixed possibility of an XSS attack through query strings
- Fixed possibility of uploading arbitrary files by default

### Fixed
- Fixed issue where a 400 response was returning a 200 status code

## [2.1.2](https://github.com/MasoniteFramework/core/releases/tag/v2.1.2) - 2018-12-16
### Added
- [Added queue drivers so any objects can be queued](https://docs.masoniteproject.com/useful-features/queues-and-jobs#passing-functions-or-methods)
- Added ShouldQueue class
- [Added new redirection method options](https://docs.masoniteproject.com/the-basics/requests#redirection)

### Fixed
- Fixed issue with deeper module controllers
- Fixed issue when returning integer from a view
- Fixed container error warning

## [2.1.1](https://github.com/MasoniteFramework/core/releases/tag/v2.1.1) - 2018-12-04
### Fixed
- Fixed issue with header redirection

## [2.1.0](https://github.com/MasoniteFramework/core/releases/tag/v2.1.0) - 2018-12-01
### Added
- Added middleware classes instead of strings.
- Added migrate:status command
- Added a simple container binding
- Added Mail Helper
- Added status code mapping and `request.status(int)` features
- Added several methods to the service provider class to helper bind things into the container
- Added view Routes
- Added request.without() method
- Added port to database dictionary
- Added way to set an integer as a status code
- Added a way to set headers with a dictionary
- Added basic testing framework
- Added Match routes for multiple route methods
- Added Masonite events into core
- Added email verification
- Added request.without
- Added craft middleware command
- Added Headers can be added via a dictionary 
- Added views can now use dot notation
- Added swap to container
- Added masonite env function for cast conversions 
- Added ability to resolve with normal parameters like `.resolve(obj, var1, var2)`
- Added password reset to auth command
- Added Response Middleware and removed the StartResponse provider
- Added better pep 8 standards
- Added code of conduct
- Added test for file system helpers
- Added Masonite events to core
- Added Response object

### Removed
- Removed the arbitrary `payload` input when fetching a json response 308b3b1
- Removed container Resolving - #255 
- Removed the need for the |safe filters on Masonite template helpers
- Removed patch from serve command

### Fixed
- Fixed param method not working with custom route compilers
- Fixed issue when removing mailprovider from the optional providers section

### Changed
- Changed `Auth` class into the `auth` directory and removed the facades directory.
- Changed cache_exists to cache
- Changed Request redirections now set status codes
- Changed and refactored commands to inherit from scaffolding based classes
- Changed built in templates to bootstrap 4
- Changed all scaffolding commands to use view templates now
- Changed routes to work without adding a slash at the end
- Changed all dependencies to the most up to date versions

## [2.0.36](https://github.com/MasoniteFramework/core/releases/tag/v2.0.36) - 2018-11-16
### Added
- Added the `-b`, `-p` and `-i` options to the serve command for bind, port and interval.

### Fixed
- Fixed issue where the server would crash when there was a syntax error.

### Changed
- Changed the developer server completely and replaced waitress with a different pure python development server.

## [2.0.35](https://github.com/MasoniteFramework/core/releases/tag/v2.0.35) - 2018-11-10
### Added
- Added upload driver's abilities to accept an open file as a file item.

## [2.0.34](https://github.com/MasoniteFramework/core/releases/tag/v2.0.34) - 2018-11-09
### Fixed
- Fixed dependencies being fixed to a specific version number

## [2.0.33](https://github.com/MasoniteFramework/core/releases/tag/v2.0.33) - 2018-11-01
### Fixed
- Fixed issue with mail templates throwing `'function' object has no attribute 'render`

## [2.0.32](https://github.com/MasoniteFramework/core/releases/tag/v2.0.32) - 2018-10-31
### Added
- [Added Redis cache driver](https://docs.masoniteproject.com/useful-features/caching#redis)
- [Added `dd()`](https://docs.masoniteproject.com/the-basics/helper-functions#die-and-dump) and [custom exception handlers](https://docs.masoniteproject.com/useful-features/framework-hooks#exception-handlers)
- [Added ability to add jinja2 extensions](https://docs.masoniteproject.com/useful-features/framework-hooks#exception-handlers)

## [2.0.31](https://github.com/MasoniteFramework/core/releases/tag/v2.0.31) - 2018-10-31
### Security
- Security fix because of the `requests` package

## [2.0.30](https://github.com/MasoniteFramework/core/releases/tag/v2.0.30) - 2018-10-16
### Fixed
- Fixed issue where `amqp` driver was not reconnecting automatically if the connection was lost

## [2.0.29](https://github.com/MasoniteFramework/core/releases/tag/v2.0.29) - 2018-10-08
### Fixed
- Fixed `amqp` driver connection credentials when connecting to remote servers

## [2.0.28](https://github.com/MasoniteFramework/core/releases/tag/v2.0.28) - 2018-10-08
### Fixed
- Fixed `amqp` driver not requiring a port

## [2.0.27](https://github.com/MasoniteFramework/core/releases/tag/v2.0.27) - 2018-10-08
### Fixed
- Fixed `amqp` driver not accepting a vhost

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

    
