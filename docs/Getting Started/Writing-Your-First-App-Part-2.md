In part 2 we'll start our actual blog application. In this tutorial we'll do 3 things:

* Migrate our database
* Create a `Blog` model
* Migrate our `Blog` model into the database

## Setting up our migrations

So to setup our migrations we will have to setup our database credentials. When we ran `python craft install`, not only did we install our dependencies but we also created a new `.env` file which contains all of our sensitive application information

{danger} Do not commit your `.env` file into source control. Your `.env` file is in `.gitignore` by default

Lets change our database settings in our `.env` file. Open up this file and change all database credentials to the correct credentials. Again it is ok to put passwords in this file as it will not be commited into source control.

Once your credentials are correct we can migrate our database. 

Masonite comes with 2 models which can be migrated over. The first is a `Migrations` model which masonite uses to keep track of which migrations need to be migrated and which haven't. The second model is a `Users` model which contains basic user information. These models can be expanded later on but for now the default values are good enough.

To migrate these two models in we can just run:

```
python craft migrate
```

{alert} This command will migrate these two models in. Running this command again will yield a "No Migrations Exists" message which means that all migrations are up to date and non exist to be migrated.

## Creating our Blog model

Because Masonite uses a more manual approach to migrations that we will get to later on, there are several types of migrations we should be aware of. 

`model migrations` are migrations based off of a model. Because of this, we need to make the model first before we create a model migration.

`make migrations` are more manual migrations which will create a migration file to be editing by the developer before the `migrate` command is ran. This manual approach has been far better in my experience and removes the finger crossing before migrations are ran because it removes a lot of the "magic" of database migrations.

In our example here we will create a `model migrations` and therefore need to make our Blog model first.

Let's go ahead and use a `craft` command to create our model:

```
python craft model Blog
``` 

This will create a `Blog` class inside `app/Blog.py` as well as import anything needed to get our model started.

{alert} Masonite uses a single class per file structure so everytime a model is created, it is put it in own respective file inside the `app/` directory.

Lets go into our `Blog` model and see what was creatied. We should see a structure similiar to:

```python
''' A Blog Database Module '''
from peewee import *
from config import database

db = database.ENGINES['default']

class Blog(Model):
    # column = CharField(default='')

    class Meta:
        database = db
```

Finally after scaffolding our project with the `craft` command can we finally start programming in Python.

Let's delete the column and put in two columns we'll need to get our blog started. Lets put a `title` and a `body` column.

Our model should now look something like:

```python
class Blog(Model):
    title = CharField(default='')
    body = CharField(default='')

    class Meta:
        database = db
```

Once our model is created we now need to create the migrations file for it. Like previously stated, since we already have a model to go off of, we can create a model migration. This migration will create a table based off of one of our models.

To do this we can just run:

```
python craft modelmigration Blog
```

Which will create a migration file based on our Blog model. And then run

```
python craft migrate
```

Which will migrate our model into our database.

Congratulations! You have successfully created your first model with Masonite.