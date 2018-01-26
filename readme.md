
<p align="center">
<img src="https://lh3.googleusercontent.com/EIteMlqzzc0ydpLMsBPshbGkud80_HrOpnFGv6Y1VhIHV2icIdu3NjFvBl5cBKHDRsfEfhHNpDaiLPI0Jf6tREdGkIZXXUX7cvAkLvY0BMUWxp1sOKS63i-hAW8z05-86EhyYbL_p-ri7WLj9iZhAbasAwojF1AZMFi31g8meHJy0zujBACQ6buKxGr-yeYftrkC6Qdno6S_kv-5_5kJL5LHkZquJpvRPHp54NnXtHaYfz1TgnmDxHNdVNjRqtQWXFIUcN4mcrNtOcSHOwy4dCLj6x_EEdXrUBGCnNRSUo0PgU-bNBD-eK60nfuJBz_B_voEFHQaKJWTP_1Qobx-RpmMNZl6ZfrIfz9XD9BDes23F1LymCKbjcRKkVAnifyeWSYYb-cEV1RUQ1-S5oM7lgLTabbpeVM-539lXL6uEV4ewlZoQVsSG0qULqLlkekth1sZbK7OhUiFDBVRB7UGq6DsrFlqwmGuJss-nSgwfT9nrzZNFEktAuOoc83cMzADEufDQ4qtl8fTCk6_klYiqOXCy1TUyLrEe0jF1B9EK-NifSgrkYrowIUDFYcJ-3uN9FDSdxqL1scFpi7CijEAi8wiQfUq4j3iok_a6ZA=w631-h648-no" width="160px"> 
</p>

<p align="center">

<img src="https://travis-ci.org/josephmancuso/masonite.svg?branch=master">
<img src="https://img.shields.io/badge/python-3.3+-blue.svg" alt="Python Version"> <img src="https://img.shields.io/github/license/josephmancuso/masonite.svg" alt="License"> 

</p>

## About Masonite

Masonite is a Python web application framework that strives for elegant and beautiful syntax. We make building web applications fun and enjoyable. Masonite takes all the pain out of developing and deploying web applications from simple payment systems to single command line deployments. Masonite removes much of the mundane tasks of building web applications by:

* Having a simple routing engine
* An extremely powerful command line helper called `craft` commands
* A simple migration system, removing the "magic" and finger crossing of migrations
* A great Active Record style ORM called Orator
* A great filesystem architecture for navigating and expanding your projec.

## Learning Masonite

Masonite strives to have extremely comprehensive documentation. All documentation can be [Found Here](https://josephmancuso.gitbooks.io/masonite/content/) and would be wise to go through the tutorials there.

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
