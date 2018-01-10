Welcome to Masonite. This tutorial will introduce you into how the Masonite frameworks works architecturally by walking you through creating a simple blog. 

This tutorial will consist of three parts:

* An authentication system to include login and logout features
* A series of blog posts you can add, update and delete
* an api system you can use that is built into Masonite

## Installation

Currently the best way to create a Masonite project is through pip

```
$ pip install masonite-cli
$ craft new project_name
```

This command will download a zip of the `josephmancuso/masonite-starter` repository and name the newly created folder the same name as the project name you specified.

{alert} You can optionally create a virtual environment here by running `python3 -m venv venv` which will create a virtual environment into the project. You can then run `source venv/bin/activate` on a Mac or `./venv/bin/activate` on Windows

## Dependencies

You now need to install all the project dependencies. Masonite comes with a helper command tool called the `craft` command tool which we used to setup the project. The `craft` command tool is to speed development and make remembering multiple commands under multiple modules easier.

To install all needed requirements just `cd` into your project and simply run:

```
$ craft install
```

This will install all dependencies specified in the requirements.txt file. This may take a minute to complete.

## Running The Server

Another great `craft` command is the `serve` command. This will serve Masonite under the `8000` port by default. To serve your project just run:

```
$ craft serve
```

Your application will now run and give you the supplied URL in the terminal. Default for this is `127.0.0.1:8000`

You will see a welcome message that says Masonite.

Congratulations, you've successfully installed and served Masonite.

In part 2 we'll talk about how to start creating our blog application