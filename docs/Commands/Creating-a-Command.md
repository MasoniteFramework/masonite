## Introduction

Creating a command is quite simple with Masonite and allows other developers to use your package in the command line similiar to a `craft` command by running `craft-vendor`. In this documentation we'll talk about how to create a package that can expand the `craft` tool by using `craft-vendor` which comes with the `masonite-cli` package.

**The `craft-vendor` command is added in the `masonite-cli >= v0.30.2`**

### Virtual Environments

It's important to note that `craft-vendor` does not have access to your virtual environment by default, only your system packages. What we can do is add our virtual environment's `site_packages` directory to our `config/packages.py` config file which should look something like:

```python
SITE_PACKAGES = [
    'venv/lib/python3.6/site-packages'
]
```

This will take that path and add it to the `sys.path` for the `craft-vendor` script.

### Getting Started

The `craft` command comes with a `package` helper and can be used to create the boilerplate for Masonite packages. We can use this boilerplate to quickly create a package that can be used on the masonite command line. Lets create our boiler plate now by navigating to a directory we would like to build our package in and run:

    $ craft package testpackage

This will create a file structure like:

```
testpackage/
    __init__.py
    integration.py
MANIFEST.in
setup.py
```

You can ignore the integration file for now as we won't be using it in this tutorial. This integration file is used to scaffold other Masonite projects (like adding configuration files and controllers)

#### Commands module

All Masonite packages that would like users to interact with their package via the command line will need a `commands` module. Let's create one now and make our package structure look like:

```
testpackage/
    __init__.py
    integration.py
    commands/
        __init__.py
        testpackage.py
MANIFEST.in
setup.py
```
 
### Craft Vendor Commands

The `craft-vendor` command is separate from our normal `craft` command but is primarily for running third party package commands. This is apart of the `masonite-cli` package. How the `craft-vendor` command works is there are three possibile commands that can be ran after someone installs your package:

    $ craft-vendor testpackage
    $ craft-vendor testpackage submodule
    $ craft-vendor testpackage submodule function_name

#### $ craft-vendor testpackage

This allows for some flexibility in how your commands can be ran. Lets start by explaining how the first command will interact with your package.

    $ craft-vendor testpackage

When the user runs this command, `craft-vendor` will look for a package called `testpackage`. Once it is found, it will look into the `command` module and look for a file called `testpackage`, and then a function in that file called `testpackage` and execute that function. In this instance, we might have a structure like:

```
testpackage/
    __init__.py
    integration.py
    commands/
        __init__.py
        testpackage.py
MANIFEST.in
setup.py
```

and then inside `testpackage/commands/testpackage` will look like:

```python
def testpackage():
    print('you have just ran the craft-vendor testpackage command')
```

#### $ craft-vendor testpackage payment

When the user runs this command, it will find the package called `testpackage`, look inside the `commands` module and for a file called `payments.py` and execute a function called `payments`. In this instance, we might have a structure like:

```
testpackage/
    __init__.py
    integration.py
    commands/
        __init__.py
        testpackage.py
        payments.py
MANIFEST.in
setup.py
```

and then inside `testpackage/commands/payments.py` will look like:

```python
def payments():
    print('you have just ran the craft-vendor testpackage payments command')
```

#### $ craft-vendor testpackage payment stripe

Lastly, When the user runs this command, it will find the package called `testpackage`, look inside the `commands` module and for a file called `payments.py` and execute a function called `stripe.py`. In this instance, we might have a structure like:

```
testpackage/
    __init__.py
    integration.py
    commands/
        __init__.py
        testpackage.py
        payments.py
MANIFEST.in
setup.py
```

and then inside `testpackage/commands/payments.py` will look like:

```python
def stripe():
    print('you have just ran the craft-vendor testpackage payments stripe command')
```

#### Uploading to PyPi

If you have never set up a package before then you'll need to [check how to make a `.pypirc` file](http://peterdowns.com/posts/first-time-with-pypi.html). This file will hold our PyPi credentials. 

To upload to PyPi we just have to change the name of our package in the `setup.py` file. Now that you have a super awesome name, we'll just need to run:

    $ python setup.py sdist upload

which should upload our package with our credentials in our `.pypirc` file. Make sure you click the link above and see how to make once.

#### Working With Our Package

We can either test our package locally or upload our package to PyPi.

To test our package locally, if you use virtual environments, just go to your Masonite project and activate your virtual environment. Navigate to the folder where you created your package and run:

    $ pip install .

If you want to be able to make changes without having to constantly reinstall your package then run 

    $ pip install --editable .

This will install your new package into your virtual environment. Go back to your project root so we can run our `craft-vendor` command. If we run `craft-vendor testpackage` we should see the respective print message. Try running all three commands and seeing the different print output. If you are getting an error of ModuleNotFound and you are inside a virtual environment, don't forget to add the site_packages directory to your `config/packages.py` by following the instructions at the top of this documentation.


