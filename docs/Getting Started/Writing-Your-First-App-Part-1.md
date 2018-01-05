Welcome to Masonite. This tutorial will introduce you into how the Masonite frameworks works architecturally by walking you through creating a simple blog. 

This tutorial will consist of three parts:

* An authentication system to include login and logout features
* A series of blog posts you can add, update and delete
* an api system you can use that is built into Masonite

## Installation

Currently the best way to install masonite is by cloning the repository onto your machine. This will require `git`.

```
$ git clone http://github.com/josephmancuso/masonite.git
```

After the repository has been cloned to your machine you can open it in any text editor you choose. 

{alert} You can optionally create a virtual environment here by running `python3 -m venv venv` which will create a virtual environment into the project. You can then run `source venv/bin/activate` on a Mac or `./venv/bin/activate` on Windows

## Dependencies

You now need to install all the project dependencies. Masonite comes with a helper command tool called the `craft` command tool. The `craft` command tool is to speed development and make remembering multiple commands under multiple modules easier.

To install all needed requirements you can simply run:

```
python craft install
```

This will install all dependencies specified in the requirements.txt file. This may take a minute to complete.

## Running The Server

Another great `craft` command is the `serve` command. This will serve Masonite under the `8000` port by default. To serve your project just run:

```
python craft serve
```

Your application will now run and give you the supplied URL in the terminal. Default for this is `127.0.0.1:8000`

You will see a welcome message that says Masonite.

Congratulations, you've successfully installed and served Masonite.

In part 2 we'll talk about how to start creating our blog application