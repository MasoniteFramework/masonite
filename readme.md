# Masonite

## The Framework For Web Crafters
<img src="https://img.shields.io/badge/python-3.2+-blue.svg" alt="Python Version"> [![Join the chat at https://gitter.im/LaraPyFramework/Lobby](https://badges.gitter.im/LaraPyFramework/Lobby.svg)](https://gitter.im/LaraPyFramework/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) <img src="https://img.shields.io/github/license/josephmancuso/masonite.svg" alt="License"> <img src="https://img.shields.io/github/issues/josephmancuso/masonite.svg" alt="Issues"> [![Build Status](https://travis-ci.org/josephmancuso/masonite.svg?branch=master)](https://travis-ci.org/josephmancuso/masonite)

Documentation: [Found Here](http://masonite.docsforcode.com)

## About Masonite

Masonite is a Python web application framework that strives for elegant and beautiful syntax. We make building web applications fun and enjoyable. Masonite takes all the pain out of developing and deploying web applications from simple payment systems to single command line deployments. Masonite removes much of the mundane tasks of building web applications by:

* Having a simple routing engine
* An extremely powerful command line helper called `craft` commands
* A single `craft deploy` command to deploy your web applications
* A simple migration system, removing the "magic" and finger crossing of migrations
* A great filesystem architecture for navigating and expanding your projec.

## Learning Masonite

Masonite strives to have extremely comprehensive documentation. All documentation can be [Found Here](http://masonite.docsforcode.com) and would be wise to go through the tutorials there.

## Installation:

```
    $ pip install masonite-cli
    $ craft new project
    $ cd project
    $ craft install
    $ craft serve
```

Go to `http://127.0.0.1:8000/`

## Contributing

Please read the CONTRIBUTING file in this repo and then please post or view open issues

## License

The Masonite framework is open-sourced software licensed under the MIT license. 


## Hello World

Getting started is very easy. Below is how you can get a simple Hello World application up and running.

## Installation

You can easily create new applications with `craft`. To create a new application run:

    $ craft new project_name

**NOTE: If you do not have the craft command, you can run `pip install masonite-cli` which will install `craft` and `craft-vendor` command line tools.**

This command will create a new directory called `project_name` with our new Masonite project.

You can now cd into this directory by doing:

    $ cd project_name

Once that is cloned we need to add the pip dependencies. You can run `pip3 install -r "requirements.txt"` or you can run the `craft` command:

    $ craft install

**NOTE: Python craft commands are essentially wrappers around common mundane tasks. Read the docs about the craft command tool to learn more**

This will install all the required dependencies to run this framework. Now we can run the gunicorn server by simply running `gunicorn -w 2 wsgi:application` or the `craft` command:

    $ craft serve

This will run the server at `localhost:8000`. Navigating to that URL should show the Masonite welcome message.

## Hello World

All web routes are in `routes/web.py`. In this file is already the route to the welcome controller. To start your hello world example just add something like:

```python
Get().route('/hello/world', 'HelloWorldController@show'),
```

our routes constant file should now look something like:

```python
ROUTES = [
    Get().route('/', 'WelcomeController@show'),
    Get().route('/hello/world', 'HelloWorldController@show'),
]
```

**NOTE: Notice this new interesting string syntax in our route. This will grant our route access to a controller (which we will create below)**

Since we used a string controller we don't have to import our controller into this file. All imports are does through Masonite on the backend.

You'll notice that we have a reference to the HelloWorldController class which we do not have yet. This framework uses controllers in order to separate the application logic. Controller can be looked at as the views.py in a Django application. The architecture here is 1 controller per file.

In order to make the `HelloWorldController` we can use a `craft` command:

    $ craft controller HelloWorldController

This will scaffold the controller for you and put it in `app/http/controllers/HelloWorldController.py` with the needed imports already scaffolded for you.

We can make a method called `show()` in order to handle the logic for our template.

Inside the `HelloWorldController` we can make a method that looks like this:

```python
def show(self, request):
    ''' Show Hello World Template '''
    return view('helloworld')
```

**NOTE: All views (controller methods) MUST take `self` and `request` as an argument. If you would like to render a template then you return a `view()` function which is imported for you at the top.**

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
