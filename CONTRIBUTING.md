# Contributing Guide

## Introduction

When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the owners or contributors of this repository before making a change.

Please note we have a code of conduct, please follow it in all your interactions with the project.

## Getting Started

The framework has three main parts.

This `MasoniteFramework/masonite` repository is the main repository that will install when creating new projects using the `craft new` command. Not much development will be done in this repository and won't be changed unless new releases of Masonite require changes in the default installation project.

The `MasoniteFramework/core` repository where the main `masonite` pip package lives. This is where the `from masonite ...` module lives.

The `MasoniteFramework/craft` repository where the `craft` command lives

### Getting the Masonite repository up and running to be edited

[You can read about how the framework flows, works and architectural concepts here](https://masoniteframework.gitbooks.io/docs/content/request-lifecycle.html)

This repo is simple and will be able to be installed following the installation instruction in the README.

* Fork the `MasoniteFramework/masonite` repo.
* Clone that repo into your computer:
  * `git clone http://github.com/your-username/masonite.git`
* Checkout the current release branch \(example: `develop`\)
* You should now be on a `develop` local branch.
* Run `git pull origin develop` to get the current release version.
* From there simply create your feature branches \(`change-default-orm`\) and make your desired changes.
* Push to your origin repository:
  * `git push origin change-default-orm`
* Open a pull request and follow the PR process below

### Editing the Masonite core repository

The trick to this is that we need it to be pip installed and then quickly editable until we like it, and then pushed back to the repo for a PR. Do this only if you want to make changes to the core Masonite package

To do this just:

* Fork the `MasoniteFramework/core` repo,
* Clone that repo into your computer:
  * `git clone http://github.com/your-username/core.git`
* Activate your masonite virtual environment \(optional\)
  * Go to where you installed masonite and activate the environment
* While inside the virtual environment, cd into the directory you installed core.
* Run `pip install .` from inside the masonite-core directory. This will install masonite as a pip package.
* Any changes you make to this package just push it to your feature branch on your fork and follow the PR process below.

{% hint style="warning" %}
This repository has a barebones skeleton of a sample project in order to aid in testing all the features of Masonite against a real project. If you install this as editable by passing the `--editable` flag then this may break your project because it will override the modules in this package with your application modules.
{% endhint %}

### Editing the craft repository \(`craft` commands\)

Craft commands make up a large part of the workflow for Masonite. Follow these instructions to get the masonite-cli package on your computer and editable.

* Fork the `MasoniteFramework/craft` repo,
* Clone that repo into your computer:
  * `git clone http://github.com/your-username/craft.git`
* Activate your masonite virtual environment \(optional\)
  * Go to where you installed masonite and activate the environment
* While inside the virtual environment, cd into the directory you installed cli
* Run `pip install --editable .` from inside the masonite-cli directory. This will install craft \(which contains the craft commands\) as a pip package but also keep a reference to the folder so you can make changes freely to craft commands while not having to worry about continuously reinstalling it.
* Any changes you make to this package just push it to your feature branch on your fork and follow the PR process below.

### Comments

Comments are a vital part of any repository and should be used where needed. It is important not to overcomment something. If you find you need to constantly add comments, you're code may be too complex. Code should be self documenting \(with clearly defined variable and method names\)

#### Types of comments to use

There are 3 main type of comments you should use when developing for Masonite:

**Module Docstrings**

All modules should have a docstring at the top of every module file and should look something like:

```python
""" This is a module to add support for Billing users """
from masonite.request import Request
...
```

**Method and Function Docstrings**

All methods and functions should also contain a docstring with a brief description of what the module does

For example:

```python
def some_function(self):
    """
    This is a function that does x action. 
    Then give an exmaple of when to use it 
    """
    ... code ...
```

**Code Comments**

If you're code MUST be complex enough that future developers will not understand it, add a `#` comment above it

For normal code this will look something like:

```python
# This code performs a complex task that may not be understood later on
# You can add a second line like this
complex_code = 'value'

perform_some_complex_task()
```

**Flagpole Comments**

Flag pole comments are a fantastic way to give developers an inside to what is really happening and for now should only be reserved for configuration files. A flag pole comment gets its name from how the comment looks

```text
'''
|--------------------------------------------------------------------------
| A Heading of The Setting Being Set
|--------------------------------------------------------------------------
|
| A quick description
|
'''

SETTING = 'some value'
```

It's important to note that there should have exactly 75 `-` above and below the header and have a trailing `|` at the bottom of the comment.

### Pull Request Process

1. You should open an issue before making any pull requests. Not all features will be added to the framework and some may be better off as a third party package. It wouldn't be good if you worked on a feature for several days and the pull request gets rejected for reasons that could have been discussed in an issue for several minutes.
2. Ensure any changes are well commented and any configuration files that are added have a flagpole comment on the variables it's setting.
3. Update the README.md and `MasoniteFramework/docs` repo with details of changes to the interface, this includes new environment variables, new file locations, container parameters etc.
4. You must add unit testing for any changes made. Of the three repositories listed above, only the `craft` and `core` repos require unit testing.
5. Increase the version numbers in any example files and the README.md to the new version that this Pull Request would represent. The versioning scheme we use is [SemVer](http://semver.org/) for both `core` and `craft` or [RomVer](http://blog.legacyteam.info/2015/12/romver-romantic-versioning/) for the main Masonite repo.
6. The PR must pass the Travis CI build. The Pull Request can be merged in once you have a successful review from two other collaborators, or the feature maintainer for your specific feature improvement or the repo owner. 
