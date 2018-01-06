Commands are a huge part of masonite and help you scaffold and maintain your project. Masonite uses `craft` commands 
which is a file inside the root of the project and can be run by typing:

```
$ python craft command_here
```

## Where commands live

Commands like `craft auth` and `craft migrate` are inside the `PROVIDERS` list inside `config/application.py`. This list contains a list of modules which are imported in order and searches for a function with the command specified.

For example the command `python craft auth` searches through the modules inside the `PROVIDERS` list and looks for a function called `auth`. Once found it will execute that command and break the loop.

## Additional commands

If no commands are found, Masonite will search all modules in the package, both internally and in site_packages for a module that has a submodule of `commands` and searches for commands inside that submodule.

For example, executing a command like `python craft masonite` will look inside the `masonite.commands` module for additional commands. This behavior is great for simply installing python packages and having a list of commands readily available after you pip install a package.

### Architecture of commands

Commands are really not complex at all but there are four levels masonite looks for commands that you should know.

The first level is the `PROVIDERS` list explained above.

The other three levels are for commands like below:

```
$ python craft masonite submodule function
$ python craft masonite submodule
$ python craft masonite
```

All three of these commands will search the module specified but in different places.

The first commands will simply search the `masonite.commands` module and look inside `submodule.py` and then execute a function called `function`

The second command will search the `masonite.commands` module and look inside `submodule.py` and execute a function called `submodule`

The third command will search the `masonite.commands` module and look inside `masonite.py` and execute a function called `masonite`

Those are the four levels of commands so if you would like to make a PyPi package for Masonite then be weary of this architecture so you can tap into the commands of Masonite