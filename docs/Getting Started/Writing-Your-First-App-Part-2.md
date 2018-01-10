In part 2 we'll start our actual blog application. In this tutorial we'll do 3 things:

* Migrate our database
* Migrate our `Blog` model into the database
* Create a `Blog` model

## Setting up our migrations

To setup our migrations we will have to setup our database credentials. When we ran `craft install`, not only did we install our dependencies but we also created a new `.env` file which contains all of our sensitive application information

{danger} Do not commit your `.env` file into source control. Your `.env` file is in `.gitignore` by default

Lets change our database settings in our `.env` file. Open up this file and change all database credentials to the correct credentials. Again it is ok to put passwords in this file as it will not be commited into source control.

Once your credentials are correct we can migrate our database. 

Masonite comes with 1 migraton which creates a users table for you. **Keep in mind that migrations and models are completely separated in Masonite. You do not need to create a model before making a migration. All models take the form of the tables they are attached to.**

To migrate our migrations just run

```
$ craft migrate
```

## Creating our Blog model

Because Masonite uses a more manual approach to migrations that we will get to later on, there are several types of migrations we should be aware of. 

A `migration` in Masonite is a way to change your database tables at a lower level than Django's models. This is great because it removes all magic from model migrations which ironically speeds development by making it very hard to mess up migration trees. Many developers encounter major problems with Django as Django attempts to guess what the developer is doing by comparing past and present models.

In our example here we will create a blog migration.

Let's go ahead and use a `craft` command to create our model:

```
craft migration create_blog_table --create blogs
``` 

This will create a `blogs` migration which we can use to create our `blogs` table.

Lets create a simple title and body in our blogs table. In our `up()` function of our migration file. Our schema migrations should look like:

```python
table.increments('id')
table.string('title')
table.text('body')
table.timestamps()
```

Our whole `up()` function should look like:

```python
def up(self):
    """
    Run the migrations.
    """
    with self.schema.create('blogs') as table:
        table.increments('id')
        table.string('title')
        table.text('body')
        table.timestamps()
```

That's it! We can now migrate this into our database:

    $ craft migrate

## Creating our Model

Now that we have a `blogs` table in our database we can now make a model for it. To make a blog just run:

    $ craft model Blog

This will create a model inside `app/Blog.py`. We do not have to specify any columns. Our model is good to go.

Our model should look like this:

```python
''' A Blog Database Model '''
from orator import DatabaseManager, Model
from config.database import Model

class User(Model):
    pass
```

Keep in mind that our blog name will default to the plural form in our table. For example, the `Blog` model will point to the `blogs` table

Finally after scaffolding our project with the `craft` command can we finally start programming in Python.

Congratulations! You have successfully created your first model with Masonite.

In the next tutorial we'll talk about how we can start adding blogs to our table.