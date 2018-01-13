# Contributing

When contributing to this repository, please first discuss the change you wish to make via issue,
email, or any other method with the owners of this repository before making a change. 

Please note we have a code of conduct, please follow it in all your interactions with the project.

## Getting Started

The framework has four main parts.

* This official repository where most work will be done primarily in release branches
* The josephmancuso/masonite-core repository where all masonite packages live.
    * This is where the `from masonite ...` module lives. 
* The josephmancuso/masonite-cli repository where the `craft` command lives
* The josephmancuso/masonite-starter repository where the project is built when `craft new` is ran
    * This repository will be updated based on this repository. It's basically just this repo stripped down
    
### Geting this repository up and running to be edited

[You can read about how the framework flows, works and architectural concepts here](http://masonite.docsforcode.com/docs/2.-Architecture-Concepts)

This repo is simple and will be able to be installed following the installation instruction in the README.

* Fork the josephmancuso/masonite repo.
* Clone that repo into your computer:
    * `git clone your-username/masonite`
* Checkout the current release branch (example: `v030`)
* You should now be on a `v030` local branch.
* run `git pull origin v030` to get the current release version.
* From there simply create your feature branches (`change-default-orm`), make your desired changes.
* Push to your origin repository:
    * `git push origin change-default-orm`
* Open a pull request and follow the PR process below

### Editing the masonite-core repository 

The trick to this is that we need it to be pip installed and then quickly editable until we like it, and then pushed back to the repo for a PR. Do this only if you want to make changes to the core masonite package

To do this just:

* Fork the josephmancuso/masonite-core repo,
* Clone that repo into your computer:
    * `git clone your-username/masonite-core`
* Activate your masonite virtual environment (optional)
    * Go to where you installed masonite and activate the environment
* While inside the virtual environment, cd into the directory you installed masonite-core
* Run `pip install --editable .` from inside the masonite-core directory. This will install masonite as a pip package but also keep a reference to the folder so you can make changes freely to masonite-core while not having to worry about continuously reinstalling it.
* Any changes you make to this package just push it to your feature branch on your fork and follow the PR process below.

### Editing the masonite-cli repository (`craft` commands)

Craft commands make up a large part of the workflow for Masonite. Follow these instructions to get the masonite-cli package on your computer and editable.

* Fork the josephmancuso/masonite-cli repo,
* Clone that repo into your computer:
    * `git clone your-username/masonite-cli`
* Activate your masonite virtual environment (optional)
    * Go to where you installed masonite and activate the environment
* While inside the virtual environment, cd into the directory you installed masonite-cli
* Run `pip install --editable .` from inside the masonite-cli directory. This will install masonite-cli (which contains the craft commands) as a pip package but also keep a reference to the folder so you can make changes freely to craft commands while not having to worry about continuously reinstalling it.
* Any changes you make to this package just push it to your feature branch on your fork and follow the PR process below.

## Editing the josephmancuso/masonite-starter repository

This repository is the repository where `craft new project_name` will install from. It takes the zip of the repository, unzips it and renames the folder to the project name. This repository is not directly editable by contributors as it's a pretty static repo that is only updated on josephmancuso/masonite releases. We will take the contents of this repo, strip it down (remove .travis and docs/ stuff) data and leave only the core project.

## Comments

Comments are a vital part of any repository and should be used where needed. It is important not to overcomment something. If you find you need to constantly add comments, you're code may be too complex. Code should be self documenting (with clearly defined variable and method names)

### Types of comments to use

There are 4 main type of comments you should use when developing for Masonite:

#### Module Docstrings

All modules should have a docstring at the top of every module file and should look something like:

```python
''' This is a module to add support for Billing users '''
from masonite.request import Request
...
```

#### Method and Function Docstrings

All methods and functions should also contain a docstring with a brief description of what the module does

For example:

```python
def some_function(self):
    ''' This is a function that does x action. 
        Then give an exmaple of when to use it 
    '''
    ... code ...
```

#### Code Comments

If you're code MUST be complex enough that future developers will not understand it, add a `#` comment above it

For normal code this will look something like:

```python
# This code performs a complex task that may not be understood later on
# You can add a second line like this
complex_code = 'value'

perform_some_complex_task()
```

If you are using if statements it should look something like:

```python
if x in y:
    # This comment should be inside the if statement
    ... code ...
else:
    # this comment should be inside the else statement
    ... code ...
```

#### Flagpole Comments

Flag pole comments are a fantastic way to give developers an inside to what is really happening and for now should only be reserved for configuration files. A flag pole comment gets its name from how the comment looks

```
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


## Pull Request Process

1. Ensure any changes are well commented and any configuration files that are added have a flagpole comment on the
   variables it is setting.
2. Update the README.md and docs/ with details of changes to the interface, this includes new environment 
   variables, exposed ports, useful file locations and container parameters.
3. Must add unit testing for any changes made.
4. Increase the version numbers in any examples files and the README.md to the new version that this
   Pull Request would represent. The versioning scheme we use is [SemVer](http://semver.org/).
5. The PR must pass the Travis build. The Pull Request can be merged in once you have the sign-off of two other developers, or    the repo owner, so that we can merge it in. 

## Code of Conduct

### Our Pledge

In the interest of fostering an open and welcoming environment, we as
contributors and maintainers pledge to making participation in our project and
our community a harassment-free experience for everyone, regardless of age, body
size, disability, ethnicity, gender identity and expression, level of experience,
nationality, personal appearance, race, religion, or sexual identity and
orientation.

### Our Standards

Examples of behavior that contributes to creating a positive environment
include:

* Using welcoming and inclusive language
* Being respectful of differing viewpoints and experiences
* Gracefully accepting constructive criticism
* Focusing on what is best for the community
* Showing empathy towards other community members

Examples of unacceptable behavior by participants include:

* The use of sexualized language or imagery and unwelcome sexual attention or
advances
* Trolling, insulting/derogatory comments, and personal or political attacks
* Public or private harassment
* Publishing others' private information, such as a physical or electronic
  address, without explicit permission
* Other conduct which could reasonably be considered inappropriate in a
  professional setting

### Our Responsibilities

Project maintainers are responsible for clarifying the standards of acceptable
behavior and are expected to take appropriate and fair corrective action in
response to any instances of unacceptable behavior.

Project maintainers have the right and responsibility to remove, edit, or
reject comments, commits, code, wiki edits, issues, and other contributions
that are not aligned to this Code of Conduct, or to ban temporarily or
permanently any contributor for other behaviors that they deem inappropriate,
threatening, offensive, or harmful.

### Scope

This Code of Conduct applies both within project spaces and in public spaces
when an individual is representing the project or its community. Examples of
representing a project or community include using an official project e-mail
address, posting via an official social media account, or acting as an appointed
representative at an online or offline event. Representation of a project may be
further defined and clarified by project maintainers.

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be
reported by contacting the project team at idmann509@gmail.com. All
complaints will be reviewed and investigated and will result in a response that
is deemed necessary and appropriate to the circumstances. The project team is
obligated to maintain confidentiality with regard to the reporter of an incident.
Further details of specific enforcement policies may be posted separately.

Project maintainers who do not follow or enforce the Code of Conduct in good
faith may face temporary or permanent repercussions as determined by other
members of the project's leadership.

### Attribution

This Code of Conduct is adapted from the [Contributor Covenant][homepage], version 1.4,
available at [http://contributor-covenant.org/version/1/4][version]

[homepage]: http://contributor-covenant.org
[version]: http://contributor-covenant.org/version/1/4/
