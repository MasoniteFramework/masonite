
<p align="center">
<img src="https://i.imgur.com/rEXcoMn.png" width="160px"> 
</p>

<p align="center">

<img src="https://travis-ci.org/MasoniteFramework/masonite.svg?branch=master">
<img src="https://img.shields.io/badge/python-3.4+-blue.svg" alt="Python Version"> <img src="https://img.shields.io/github/license/MasoniteFramework/masonite.svg" alt="License"> 

</p>

## About Masonite

Masonite is the rapid application Python development framework that strives for elegant, readable, and beautiful syntax. Masonite makes building web applications fun, enjoyable and scalable. Masonite takes much of the pain out of developing web applications from simple payment systems to removing mundane development tasks with a command line companion tool called craft commands. Masonite removes much of the mundane tasks of building web applications by:

* Having a simple and expressive routing engine
* Extremely powerful command line helpers called `craft` commands
* A simple migration system, removing the "magic" and finger crossing of migrations
* A great Active Record style ORM called Orator
* A great filesystem architecture for navigating and expanding your project
* An extremely powerful Service Container (IOC Container)
* Service Providers which makes Masonite extremely extendable

## Learning Masonite

Masonite strives to have extremely comprehensive documentation. All documentation can be [Found Here](https://masoniteframework.gitbooks.io/docs/content/) and would be wise to go through the tutorials there. If you find any discrepencies or anything that doesn't make sense, be sure to comment directly on the documentation to start a discussion!

## Installation:

```
    $ pip install masonite-cli
    $ craft new project
    $ cd project
    $ craft install
    $ craft serve
```

Go to `http://localhost:8000/`

## Contributing

Please read the [Contributing Documentation](https://masoniteframework.gitbooks.io/docs/content/todo-contributing.html) here. Development will be on the current releasing branch (typically the `develop` branch) so check open issues, the current Milestone as well as the contributing file. Ask any questions you like in the issues so we can have an open discussion about the framework, design decisions and future of the project.

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

This will install all the required dependencies to run this framework. Now we can run the `craft` command:

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
