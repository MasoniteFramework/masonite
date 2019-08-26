
<p align="center">
<img src="https://i.imgur.com/rEXcoMn.png" width="160px"> 
</p>

<p align="center">

<img src="https://travis-ci.org/MasoniteFramework/masonite.svg?branch=master">
<img src="https://img.shields.io/badge/python-3.4+-blue.svg" alt="Python Version"> <img src="http://pepy.tech/badge/masonite?1" alt="License">  <img src="https://img.shields.io/github/license/MasoniteFramework/masonite.svg" alt="License"> 
<img src="https://coveralls.io/repos/github/MasoniteFramework/core/badge.svg?branch=master#" alt="License">

</p>

## About Masonite

The modern and developer centric Python web framework that strives for an actual batteries included developer tool with a lot of out of the box functionality with an extremely extendable architecture. Masonite is perfect for beginner developers getting into their first web applications as well as experienced devs that need to utilize the full potential of Masonite to get their applications done.

Masonite works hard to be fast and easy from install to deployment so developers can go from concept to creation in as quick and efficiently as possible. Use it for your next SaaS! Try it once and you’ll fall in love.

* Having a simple and expressive routing engine
* Extremely powerful command line helpers called `craft` commands
* A simple migration system, removing the "magic" and finger crossing of migrations
* A great Active Record style ORM called Orator
* A great filesystem architecture for navigating and expanding your project
* An extremely powerful Service Container (IOC Container)
* Service Providers which makes Masonite extremely extendable

## Learning Masonite

Masonite strives to have extremely comprehensive documentation. All documentation can be [Found Here](https://docs.masoniteproject.com/v/v2.1/) and would be wise to go through the tutorials there. If you find any discrepencies or anything that doesn't make sense, be sure to comment directly on the documentation to start a discussion!

If you are a visual learner you can find tutorials here: [MasoniteCasts](https://casts.masonite.dev)

Also be sure to join the [Slack channel](http://slack.masoniteproject.com/)!


## Requirements

- Python 3.4 +
- OpenSSL (latest version)
- Pip

## Linux

If you are running on a Linux flavor, you’ll need a few extra packages before you start. You can download these packages by running:

```
$ sudo apt-get install python-dev libssl-dev
```

Instead of `python-dev` you may need to specify your Python version

```
$ sudo apt-get install python3.6-dev libssl-dev
```

## Windows

With windows you will need to have the latest OpenSSL version. Install [OpenSSL 32-bit or 64-bit](https://slproweb.com/products/Win32OpenSSL.html).

## Mac

If you do not have the latest version of OpenSSL you will encounter some installation issues with creating new applications since we need to download a zip of the application via GitHub.

With Mac you can install OpenSSL through `brew`.

```
brew install openssl
```

Python 3.6 does not come preinstalled with certificates so you may need to install certificates with this command:

```
/Applications/Python\ 3.6/Install\ Certificates.command
```

You should now be good to install new Masonite application of Mac :)

### Python 3.7

If you are using [Python 3.7](https://www.python.org/downloads/windows/), add it to your PATH Environment variable.

Open Windows PowerShell and run: `pip install masonite-cli`

Add `C:\Users\%USERNAME%\.AppData\Programs\Python\Python37\Scripts\` to PATH Environment variable.

Note: PATH variables depend on your installation folder

## Installation:

```
    $ pip3 install masonite-cli :: (may need sudo if using UNIX) ::
    $ craft new project
    $ cd project
    $ craft install
    $ craft serve
```

Go to `http://localhost:8000/`
****

<p align="center">
* * * *
</p>

Not all computers are made the same so you may have some trouble installing Masonite depending on your machine. If you have any issues be sure to read the [Known Installation Issues](https://docs.masoniteproject.com/prologue/known-installation-issues) Documentation.

<p align="center">
* * * *
</p>

****

## Contributing

Please read the [Contributing Documentation](https://masoniteframework.gitbook.io/docs/prologue/contributing-guide) here. Development will be on the current releasing branch of the [Core Repository](https://github.com/MasoniteFramework/core) (typically the `develop` branch) so check open issues, the current Milestone and the releases in that repository. Ask any questions you like in the issues so we can have an open discussion about the framework, design decisions and future of the project.

## Contributors

Thank you for those who have contributed to Masonite!

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore -->
| | | | | | |
| :-------------: | :-------------: | :-------------: | :-------------: | :-------------: | :-------------: |
| [<img src="https://avatars1.githubusercontent.com/u/6290791?s=460&v=4" width="100px;"/><br /><sub><b>Vaibhav Mule</b></sub>](https://github.com/vaibhavmule) | [<img src="https://avatars.githubusercontent.com/u/6276555?v=3" width="100px;"/><br /><sub><b>Martín Peveri</b></sub>](https://github.com/mapeveri) | [<img src="https://avatars.githubusercontent.com/u/25895176?v=3" width="100px;"/><br /><sub><b>Adorifski</b></sub>](https://github.com/afdolriski) | [<img src="https://avatars.githubusercontent.com/u/1970073?v=3" width="100px;"/><br /><sub><b>Abram C. Isola</b></sub>](https://github.com/aisola) | [<img src="https://avatars.githubusercontent.com/u/41387624?v=3" width="100px;"/><br /><sub><b>Raphael Schubert</b></sub>](https://github.com/rfschubert) | [<img src="https://avatars.githubusercontent.com/u/16268619?v=3" width="100px;"/><br /><sub><b>Mitch Dennett</b></sub>](https://github.com/mitchdennett) |

## License

The Masonite framework is open-sourced software licensed under the MIT license. 

## Hello World

Getting started is very easy. Below is how you can get a simple Hello World application up and running.

## Installation

The best way to install Masonite is by starting in a virtual environment first. This will avoid any issues with filesystem permissions.

```
python3 -m venv venv
```

Then activate the virtual environment:

```
WINDOWS: $ ./venv/Scripts/activate
MAC: $ source venv/bin/activate
```


You can easily create new applications with `craft`. To create a new application run:

```
$ pip install masonite-cli
$ craft new .
```

The `.` will tell craft to create the project in the current directory instead of a new directory.

```
$ craft install
```

This will install all of Masonites dependencies as well as create a new `.env` file consisting of all of your environment variables.

****

<p align="center">
* * * *
</p>

NOTE: Python craft commands are essentially wrappers around common mundane tasks. Read the docs about the craft command tool to learn more

<p align="center">
* * * *
</p>

****


Now we can run the `craft` command:

    $ craft serve

This will run the server at `localhost:8000` and be in an auto-reloading state. When you change files, your server will restart. Navigating to that URL should show the Masonite welcome message. 

If that port is blocked you can specify a port by running:

    $ craft serve --port 8080

Or specify a host by running:

    $ craft serve --host 192.168.1.283

## Hello World

All web routes are in `routes/web.py`. In this file is already the route to the welcome controller. To start your hello world example just add something like:

```python
Get('/hello/world', 'HelloWorldController@show'),
```

our routes constant file should now look something like:

```python
ROUTES = [
    Get('/', 'WelcomeController@show'),
    Get('/hello/world', 'HelloWorldController@show'),
]
```

****

<p align="center">
* * * *
</p>

NOTE: Notice this new interesting string syntax in our route. This will grant our route access to a controller (which we will create below)

<p align="center">
* * * *
</p>

****

Since we used a string controller we don't have to import our controller into this file. All imports are done through Masonite on the backend.

You'll notice that we have a reference to the HelloWorldController class which we do not have yet. This framework uses controllers in order to separate the application logic. Controllers can be looked at as the views.py in a Django application. The architectural standard here is 1 controller per file.

In order to make the `HelloWorldController` we can use a `craft` command:

    $ craft controller HelloWorld

This will scaffold the controller for you and put it in `app/http/controllers/HelloWorldController.py`. This new file will have all the imports for us.

Inside the `HelloWorldController` we can make our `show` method like this:

```python
def show(self, view: View):
    """ Show Hello World Template """
    return view.render('helloworld')
```

As you see above, we are returning a `helloworld` template but we do not have that yet. All templates are in `resources/templates`. We can simply make a file called `helloworld.html` or run the `craft` command:

    $ craft view helloworld

Which will create the `resources/templates/helloworld.html` template for us.

Lastly all templates run through the Jinja2 rendering engine so we can use any Jinja2 code inside our template like:

inside the `resources/views/helloworld.html`

```
{{ 'Hello World' }}
```

Now just run the server:

    $ craft serve

And navigate to `localhost:8000/hello/world` and you will see `Hello World` in your browser.

Happy Crafting!
