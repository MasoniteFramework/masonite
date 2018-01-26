<div style="text-align:center">
<img src="https://lh3.googleusercontent.com/M78mPGyhJxVspj6aP_rlF4VlFcMmI8tzsgCxO7S-UqtimlF5Ldr1cHn7SLvkMcknDVFMYqu-wbCPRuECGn7zOUKnbieM4wQqnQyPvU2C48vYH26gtuU1gf363DnVHl2ceZGejt9XI4ZmitOFO1NW80-t56IcIzEWSkX_BoyMCc-3JitQKjcharHGKhaoOJDrayLd1RSmlKGTNNWGX-ESNbPnBrKyX5VW8rExFXVRF5oPim19-1WutRqXwevFz-ia8SgHUEyJqGMx-OmRoVIOwNnckAxLzPPwL6llujfjnnekAvJrgKLM4B__8O0Dc8Tz508skvsWz0o-AZtyZMowrBcV4k7Kri1TSEeN_T9UxmJC2fg819mjtWe0ZDqyg3e9sZC9xUP1JmFCHzllUmbiaa6hJmWoVyNj8Wk3p_ZOX4QlqzB1ys_jzOGfMbw8zNFyY2Ea3nAVS57fkRh79wNkqYM5uU9Z0T77QR6m5wsx6GjR5IuUolPsWBvBkjg9i87uZe6gX3Ru0H0DrhFzs9mxZ6wIs13312X-wbzl8pzm1dvT9zPnnmZ6fW1EKUxxWNBORBSmH_1NLCSEtNT6Qxy8n36QCVYYe4qUZdq25kxUxNhdNEl5q8DR2DGi9cwkb1qBn9J_iFsaaggRXVDTEGJ8mI5BGpGgBlfp=s648-no" width="64px">

# Masonite

[![Build Status](https://travis-ci.org/josephmancuso/masonite.svg?branch=master)](https://travis-ci.org/josephmancuso/masonite)
<img src="https://img.shields.io/badge/python-3.3+-blue.svg" alt="Python Version"> [![Join the chat at https://gitter.im/masonite-framework/Lobby](https://badges.gitter.im/masonite-framework/Lobby.svg)](https://gitter.im/masonite-framework/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) <img src="https://img.shields.io/github/license/josephmancuso/masonite.svg" alt="License">

## Documentation: [Found Here](https://josephmancuso.gitbooks.io/masonite/content/)
</div>

## About Masonite

Masonite is a Python web application framework that strives for elegant and beautiful syntax. We make building web applications fun and enjoyable. Masonite takes all the pain out of developing and deploying web applications from simple payment systems to single command line deployments. Masonite removes much of the mundane tasks of building web applications by:

* Having a simple routing engine
* An extremely powerful command line helper called `craft` commands
* A simple migration system, removing the "magic" and finger crossing of migrations
* A great Active Record style ORM called Orator
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

Please read the CONTRIBUTING file in this repo and then please post or view open issues. Development will be on the current releasing branch so check open issues, the current Milestone as well as the contributing file. Ask any questions you like in the issues so we can have an open discussion about the framework, design decisions and future of the project.

## Official Packages

Masonite also has optional packages that extend the functionality of the framework. It's very easy to make packages that integrate solely and perfectly with Masonite. Documentation on how to create packages can be [Found Here](https://github.com/josephmancuso/masonite/blob/master/docs/Creating-Packages.md). Official packages include:

* [Masonite Clerk](https://github.com/josephmancuso/masonite/blob/master/docs/Masonite-Clerk.md) - Adds stripe charging, customer creation and subscriptions to your models.
* [Masonite Triggers](https://github.com/josephmancuso/masonite-triggers) - Adds a way to register classes in a configuration file and then call it in anywhere with a `trigger` function. This is great for registering a class for sending a welcome email and then triggering it in your controllers
* [Masonite AuthHub](https://github.com/josephmancuso/masonite/blob/master/docs/Masonite-AuthHub.md) - Add OAuth support for authenticating users with third party providers like GitHub.

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
