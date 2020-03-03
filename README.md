
<p align="center">
<img src="https://i.imgur.com/rEXcoMn.png" width="160px"> 
</p>

<p align="center">
<img src="https://travis-ci.org/MasoniteFramework/masonite.svg?branch=master">
<img src="https://img.shields.io/badge/python-3.5+-blue.svg" alt="Python Version"> <img src="http://pepy.tech/badge/masonite?1" alt="License">  <img src="https://img.shields.io/github/license/MasoniteFramework/masonite.svg" alt="License"> 
<img src="https://coveralls.io/repos/github/MasoniteFramework/core/badge.svg?branch=master#" alt="License">
<img src="https://img.shields.io/badge/all_contributors-10-orange.svg?style=flat-square" alt="All Contributors">

</p>

**NOTE: Masonite 2.3 is no longer compatible with the `masonite-cli` tool. Please uninstall that by running `pip uninstall masonite-cli`. If you do not uninstall `masonite-cli` you will have command clashes**

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

Masonite strives to have extremely comprehensive documentation. All documentation can be [Found Here](https://docs.masoniteproject.com/) and would be wise to go through the tutorials there. If you find any discrepencies or anything that doesn't make sense, be sure to comment directly on the documentation to start a discussion!

If you are a visual learner you can find tutorials here: [MasoniteCasts](https://masonitecasts.com)

Also be sure to join the [Slack channel](http://slack.masoniteproject.com/)!

## Contributing

Contributing to Masonite is simple:
* Hop on [Slack Channel](http://slack.masoniteproject.com/)! to ask any questions you need.
* Read the [How To Contribute](https://masoniteframework.gitbook.io/docs/prologue/how-to-contribute) documentation to see ways to contribute to the project.
* Read the [Contributing Guide](https://masoniteframework.gitbook.io/docs/prologue/contributing-guide) to learn how to contribute to the core source code development of the project.
* Read the [Installation](https://docs.masoniteproject.com/#installation) documentation on how to get started creating a Masonite project.
* Check the [open issues and milestones](https://github.com/MasoniteFramework/core/issues).
* If you have any questions just [open up an issue](https://github.com/MasoniteFramework/core/issues/new/choose) to discuss with the core maintainers.
* [Follow Masonite Framework on Twitter](https://twitter.com/masoniteproject) to get updates about tips and tricks, announcement and releases.

## Requirements

In order to use Masonite, you’ll need:

* Python 3.5+
* Latest version of OpenSSL
* Pip3

> All commands of python and pip in this documentation is assuming they are pointing to the correct Python 3 versions. For example, anywhere you see the `python` command ran it is assuming that is a Python 3.5+ Python installation. If you are having issues with any installation steps just be sure the commands are for Python 3.5+ and not 2.7 or below.

## Linux

If you are running on a Linux flavor, you’ll need the Python dev package and the libssl package. You can download these packages by running:

### Debian and Ubuntu based Linux distributions

```text
$ sudo apt-get install python-dev libssl-dev python3-pip
```

Or you may need to specify your `python3.x-dev` version:

```text
$ sudo apt-get install python3.6-dev libssl-dev python3-pip
```

### Enterprise Linux based distributions \(Fedora, CentOS, RHEL, ...\)

```text
# dnf install python-devel openssl-devel
```

## Windows

With windows you MAY need to have the latest OpenSSL version. Install [OpenSSL 32-bit or 64-bit](https://slproweb.com/products/Win32OpenSSL.html).

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

### Python 3.7 and Windows

If you are using [Python 3.7](https://www.python.org/downloads/windows/), add it to your PATH Environment variable.

Open Windows PowerShell and run: `pip install masonite-cli`

Add `C:\Users\%USERNAME%\.AppData\Programs\Python\Python37\Scripts\` to PATH Environment variable.

Note: PATH variables depend on your installation folder

## Quick Install:

Here is the quick and dirty of what you need to run. More step by step instructions are found below.

```
    $ python3 -m venv venv
    $ source venv/bin/activate
    $ pip install masonite
    $ craft new
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

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore -->
<table>
  <tr>
     <td align="center"><a href="http://docs.masoniteproject.com"><img src="https://avatars1.githubusercontent.com/u/20172538?v=4" width="100px;" alt="Joseph Mancuso"/><br /><sub><b>Joseph Mancuso</b></sub></a><br /><a href="https://github.com/MasoniteFramework/masonite/commits?author=josephmancuso" title="Code">💻</a> <a href="https://github.com/MasoniteFramework/masonite/issues?q=author%3Ajosephmancuso" title="Bug reports">🐛</a> <a href="#question-josephmancuso" title="Answering Questions">💬</a> <a href="#ideas-josephmancuso" title="Ideas, Planning, & Feedback">🤔</a></td>
    <td align="center"><a href="http://vaibhavmule.com"><img src="https://avatars0.githubusercontent.com/u/6290791?v=4" width="100px;" alt="Vaibhav Mule"/><br /><sub><b>Vaibhav Mule</b></sub></a><br /><a href="https://github.com/MasoniteFramework/masonite/commits?author=vaibhavmule" title="Code">💻</a> <a href="https://github.com/MasoniteFramework/masonite/issues?q=author%3Avaibhavmule" title="Bug reports">🐛</a> <a href="#question-vaibhavmule" title="Answering Questions">💬</a> <a href="#ideas-vaibhavmule" title="Ideas, Planning, & Feedback">🤔</a></td>
    <td align="center"><a href="http://martinpeveri.wordpress.com"><img src="https://avatars3.githubusercontent.com/u/6276555?v=4" width="100px;" alt="Martín Peveri"/><br /><sub><b>Martín Peveri</b></sub></a><br /><a href="https://github.com/MasoniteFramework/masonite/commits?author=mapeveri" title="Code">💻</a> <a href="https://github.com/MasoniteFramework/masonite/issues?q=author%3Amapeveri" title="Bug reports">🐛</a> <a href="#question-mapeveri" title="Answering Questions">💬</a> <a href="#ideas-mapeveri" title="Ideas, Planning, & Feedback">🤔</a></td>
    <td align="center"><a href="http://tonyhammack.com"><img src="https://avatars0.githubusercontent.com/u/10157988?v=4" width="100px;" alt="Tony Hammack"/><br /><sub><b>Tony Hammack</b></sub></a><br /><a href="https://github.com/MasoniteFramework/masonite/commits?author=hammacktony" title="Code">💻</a> <a href="https://github.com/MasoniteFramework/masonite/issues?q=author%3Ahammacktony" title="Bug reports">🐛</a> <a href="#question-hammacktony" title="Answering Questions">💬</a> <a href="#ideas-hammacktony" title="Ideas, Planning, & Feedback">🤔</a></td>
    <td align="center"><a href="https://inkit.io"><img src="https://avatars0.githubusercontent.com/u/1970073?v=4" width="100px;" alt="Abram C. Isola"/><br /><sub><b>Abram C. Isola</b></sub></a><br /><a href="https://github.com/MasoniteFramework/masonite/commits?author=aisola" title="Code">💻</a> <a href="https://github.com/MasoniteFramework/masonite/issues?q=author%3Aaisola" title="Bug reports">🐛</a> <a href="#question-aisola" title="Answering Questions">💬</a> <a href="#ideas-aisola" title="Ideas, Planning, & Feedback">🤔</a></td>
    <td align="center"><a href="http://www.mitchdennett.com"><img src="https://avatars0.githubusercontent.com/u/16268619?v=4" width="100px;" alt="Mitch Dennett"/><br /><sub><b>Mitch Dennett</b></sub></a><br /><a href="https://github.com/MasoniteFramework/masonite/commits?author=mitchdennett" title="Code">💻</a> <a href="https://github.com/MasoniteFramework/masonite/issues?q=author%3Amitchdennett" title="Bug reports">🐛</a> <a href="#question-mitchdennett" title="Answering Questions">💬</a> <a href="#ideas-mitchdennett" title="Ideas, Planning, & Feedback">🤔</a></td>
    <td align="center"><a href="http://marlysson.github.io"><img src="https://avatars3.githubusercontent.com/u/4117999?v=4" width="100px;" alt="Marlysson Silva"/><br /><sub><b>Marlysson Silva</b></sub></a><br /><a href="https://github.com/MasoniteFramework/masonite/commits?author=Marlysson" title="Code">💻</a> <a href="https://github.com/MasoniteFramework/masonite/issues?q=author%3AMarlysson" title="Bug reports">🐛</a> <a href="#question-Marlysson" title="Answering Questions">💬</a> <a href="#ideas-Marlysson" title="Ideas, Planning, & Feedback">🤔</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://www.linkedin.com/in/christopher-byrd-49726691"><img src="https://avatars2.githubusercontent.com/u/7581926?v=4" width="100px;" alt="Christopher Byrd"/><br /><sub><b>Christopher Byrd</b></sub></a><br /><a href="https://github.com/MasoniteFramework/masonite/commits?author=ChrisByrd14" title="Code">💻</a> <a href="https://github.com/MasoniteFramework/masonite/issues?q=author%3AChrisByrd14" title="Bug reports">🐛</a> <a href="#question-ChrisByrd14" title="Answering Questions">💬</a> <a href="#ideas-ChrisByrd14" title="Ideas, Planning, & Feedback">🤔</a></td>
    <td align="center"><a href="https://github.com/bjorntheart"><img src="https://avatars1.githubusercontent.com/u/53244?v=4" width="100px;" alt="Björn Theart"/><br /><sub><b>Björn Theart</b></sub></a><br /><a href="https://github.com/MasoniteFramework/masonite/commits?author=bjorntheart" title="Code">💻</a> <a href="https://github.com/MasoniteFramework/masonite/issues?q=author%3Abjorntheart" title="Bug reports">🐛</a> <a href="#question-bjorntheart" title="Answering Questions">💬</a> <a href="#ideas-bjorntheart" title="Ideas, Planning, & Feedback">🤔</a></td>
    <td align="center"><a href="https://nioperas06.github.io"><img src="https://avatars1.githubusercontent.com/u/11293401?v=4" width="100px;" alt="Junior Gantin"/><br /><sub><b>Junior Gantin</b></sub></a><br /><a href="https://github.com/MasoniteFramework/masonite/commits?author=nioperas06" title="Code">💻</a> <a href="https://github.com/MasoniteFramework/masonite/issues?q=author%3Anioperas06" title="Bug reports">🐛</a> <a href="#question-nioperas06" title="Answering Questions">💬</a> <a href="#ideas-nioperas06" title="Ideas, Planning, & Feedback">🤔</a></td>
  </tr>
</table>

<!-- ALL-CONTRIBUTORS-LIST:END -->
Thank you for those who have contributed to Masonite!


## License

The Masonite framework is open-sourced software licensed under the MIT license. 

## Hello World

Getting started is very easy. Below is how you can get a simple Hello World application up and running.

## Installation

> Be sure to join the [Slack Channel](http://slack.masoniteproject.com) for help or guidance.

Masonite excels at being simple to install and get going. If you are coming from previous versions of Masonite, the order of some of the installation steps have changed a bit.

Firstly, open a terminal and head to a directory you want to create your application in. You might want to create it in a programming directory for example:

```
$ cd ~/programming
$ mkdir myapp
$ cd myapp
```

If you are on windows you can just create a directory and open the directory in the Powershell.

## Activating Our Virtual Environment \(optional\)

Although this step is technically optional, it is highly recommended. You can create a virtual environment if you don't want to install all of masonite's dependencies on your systems Python. If you use virtual environments then create your virtual environment by running:

```text
$ python -m venv venv
$ source venv/bin/activate
```

or if you are on Windows:

```text
$ python -m venv venv
$ ./venv/Scripts/activate
```

> The `python`command here is utilizing Python 3. Your machine may run Python 2 \(typically 2.7\) by default for UNIX machines. You may set an alias on your machine for Python 3 or simply run `python3`anytime you see the `python`command.

> For example, you would run `python3 -m venv venv` instead of `python -m venv venv`

## Installing Masonite

Now we can install Masonite. This will give us access to a craft command we can use to finish the install steps for us:

```
$ pip install masonite
```

Once Masonite installs you will now have access to the `craft` command line tool. Craft will become your best friend during your development. You will learn to love it very quickly :).

You can ensure Masonite and craft installed correctly by running:

```
$ craft
```

You should see a list of a few commands like `install` and `new`

## Creating Our Project

Great! We are now ready to create our first project. We should have the new `craft` command. We can check this by running:

```text
$ craft
```

We are currently only interested in the `craft new` command. To create a new project just run:

```text
$ craft new
```

This command will also run `craft install` which will install our dependencies.

This will get the latest Masonite project template and unzip it for you. We just need to go into our new project directory and install the dependencies in our `requirements.txt` file.


## Additional Commands

Now that Masonite installed fully we can check all the new commands we have available. There are many :).

```
$ craft
```

We should see many more commands now.

## Running The Server

After it’s done we can just run the server by using another `craft` command:

```text
$ craft serve
```

Congratulations! You’ve setup your first Masonite project! Keep going to learn more about how to use Masonite to build your applications.

{% hint style="success" %}
You can learn more about craft by reading [The Craft Command](https://github.com/MasoniteFramework/docs/tree/ba9d9f8ac3e41d58b9d92d951f92c898fb16a2a4/the-craft-command.md) documentation or continue on to learning about how to create web application by first reading the [Routing ](the-basics/routing.md)documentation
{% endhint %}

{% hint style="info" %}
Masonite uses romantic versioning instead of semantic versioning. Because of this, all minor releases \(2.0.x\) will contain bug fixes and fully backwards compatible feature releases. Be sure to always keep your application up to date with the latest minor release to get the full benefit of Masonite's romantic versioning.
{% endhint %}

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

You'll notice that we have a reference to the `HelloWorldController` class which we do not have yet. This framework uses controllers in order to separate the application logic. Controllers can be looked at as the views.py in a Django application. The architectural standard here is 1 controller per file.

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
