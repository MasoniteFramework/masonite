# Masonite 4 White Paper

This white paper is created to explain, in depth, how Masonite features, classes, and concepts should work.

**Concepts and code snippets in this white paper are subject to change at anytime. This is a living document and explains how Masonite 4 currently works in its current state.**

## Why This Paper Exists

This white paper is intended to be a full explanation of how major parts of the system work. We will use this white paper to bring on new contributors or people interested in learning how Masonite works.

We will use this document to stay on track and as a guide when creating new features for Masonite to stay consistent and efficient.

Masonite 4 is the successor to Masonite 3. Masonite 4 is a complete, from the ground up rewrite of Masonite. The reason for this rewrite is plentiful:

- Masonite was started in December of 2017 as a learning project for me to learn how frameworks work. It has since become a passion project for me and many others but there are still major parts of the framework that still have code from those beginning months. This code has obviously become legacy at this point and needs to be removed and rewritten.
- Masonite has gone through plenty of design changes over the course of 4 years and has relics in the codebase as such. We changed how routes work, added service providers, we changed how authentication works, we added web guards and many other changes. These were all sort of built around the same concepts and I think those decisions in the past have seriously stunted the growth of Masonite. Masonite at one point was one giant python file and only until version 2 did it even have service providers.
- When building a framework, one of the important concepts is making it expandable. This is done simply via new features but also done as packages and as a community. There really is no easy way to write a package for Masonite, theres no standard, theres some nice ways to plug it in but package development is not really there yet. This is why i think there are not many packages currently for Masonite. When first building Masonite I obviously didn't know what I know now. So now I am taking everything i learned over 4 years, plus everything i learned after a successful ORM project rewrite and building a Masonite framework i know will survive the test of time.
- Masonite ORM was developed recently and I am so proud of that library and how we built it that I want to apply those same principals to Masonite. Since Masonite codebase is so tightly coupled to everything it's hard to maintain it and build new features. Refactors are hard because it always leaves small remnants of technical debt left behind that eventually need to be cleaned up with a rewrite anyway. It's difficult sometimes to know which tests need to be fixed, which tests no longer apply and which tests need to be written. When you are dealing with nearly 1000 tests it gets time consuming to check them. They might be failing but how do we make them pass? Do we fix them? Do we fix the code? Do we delete the test? And even when all the tests pass again we are left with a mix of new code, refactored code and code thats there just to make the test pass. This type of time management and technical debt needed for new features is costly for open source projects.

## Table Of Contents

- Foundation
- Features

## Foundation

In M4, The foundation is completely redone.

These improvements allows the directory structure to be anything we need it to be. All features are fully encapsulated and modular and Masonite does not need to be in specific directory structure order anymore.

There is a new concept in M4 called the Application class. This class has is a mix between a new "Application" concept class and the container. So now everything is bound and made from the application class. It is also a callable so wsgi servers actually call this class to. Its very adaptable.

The application class is an IOC container. So we can bind anything to these classes from key value strings to lists and dicts, to classes. Later we can make these values back out, swap them out with other implementations and other cool things. This keeps the entire framework extremely modular and really revolves around this IOC container.

### Kernel Classes

Kernel classes is really just a service provider that only registers things to the application class that is crucial to making the framework work. For example, we need to know where the config directories are, the view directories, controller directories, bind middleware, etc. These are booted before the service providers are even imported. These classes should not need to be developed on but will come with new applications and will be located inside those new applications. These can be tweaked per application. For example if you want your views directory to be located in `app/views` then you can do just that.

## Providers

Providers are a concept in Masonite in which they are simply wrappers around binding things to the container as well as logic that runs during a request. Everything will be bound to the container through a provider from mail and sessions features to fetching controller responses and showing the exception handling page.

Providers will run 2 times. First when they are first added to the container. This runs a `register` method. The register method will bind things into the container. There is a second time it runs which is during the request which will run the `boot` method.

Let's take the example of the route provider which contains both a `register` and `boot` method:

```python
class RouteProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        # Register the routes
        Route.set_controller_locations(
            self.application.make("controllers.location")
        )

    def boot(self):
        router = self.application.make("router")
        request = self.application.make("request")
        response = self.application.make("response")

        route = router.find(request.get_path(), request.get_request_method())

        # Run before middleware

        if route:
            Pipeline(request, response).through(
                self.application.make("middleware").get_http_middleware(),
                handler="before",
            )
            Pipeline(request, response).through(
                self.application.make("middleware").get_route_middleware(["web"]),
                handler="before",
            )

            response.view(route.get_response(self.application))

            Pipeline(request, response).through(
                self.application.make("middleware").get_route_middleware(["web"]),
                handler="after",
            )
            Pipeline(request, response).through(
                self.application.make("middleware").get_http_middleware(),
                handler="after",
            )
        else:
            raise Exception(f"NO route found for {request.get_path()}")

```

Notice that this provider is a `RouteProvider` so it registers routes as well as handles getting the response from the controller and attaching it to the response.

So a provider can do many different things and its really not limited by anything.

### Pipeline

Pipeline classes run logic that needs to happen in a specific order and then cancel out if anything fails. This is perfect for request and response in the form of middleware.

The concept is simple: we pass in 2 things into the pipe and if you want to continue, you return the first object, if you want to stop you return the second object.

Here is an example of middleware doing this:

```python
class VerifyCsrfToken(Middleware):

    exempt = []

    def before(self, request, response):

        if not self.verify_token(request, self.get_token(request)):
          return response.status(403)

        token = self.create_token(request)

        request.app.make("view").share(
            {
                "csrf_field": Markup(
                    f"<input type='hidden' name='__token' value='{token}' />"
                ),
                "csrf_token": token,
            }
        )

        return request
```

So if the token doesn't pass we return the response which stops and exists the pipeline. Else we will continue down through to the controller.

## Features

Features of Masonite should be written in a very specific way. This way features are written in Masonite allow features to be:

- expanded
- fixed
- tweaked
- provides the maximum effeciency for maintenance
- standardized features so anybody can improve features with a common understanding.

This is a guide on how Masonite features are developed but also apply to packages as well. Packaging will be in another white paper which will be linked here: Link TBD.

There are several moving peices to each feature. I'll explain them briefly here and then will go into detail.

- A manager style class. This is a class that will likely be the front facing class that people use in controllers. This class will have all the drivers registered to it and be responsible for handling switching drivers, wrapping some logic, the front facing API. This is also the class that will be type hinting and "made" from the container.
  - (see src/masonite/mail/Mail.py)
- driver class(es). Could be 1 or more
  - (see src/masonite/drivers/mail/MailgunDriver.py)
- A service provider to register to the framework
  - (see src/masonite/providers/MailProvider.py).
- Components classes when applicable. These are helper classes that wrap logic. In the ORM, think of those expression classes that wrap some logic like if a query is Raw. These classes are small encapsulated peices of functionality designed to write cleaner code in other parts of the system. Because then i would just need to do something like. So component classes help to write clean code somewhere else. very Handy.
  - (see src/masonite/mail/MessageAttachment.py & src/masonite/drivers/mail/Recipient.py)
- Bindings should also be extremely simple. for mail it should be `application.make('mail')`. For sessions it should be `application.make('session')`, etc etc.
- Registers drivers to the manager in the same exact way.
  (see https://github.com/MasoniteFramework/masonite4/pull/28/files#diff-221cd9f78ee5571e49f930cfd66a2229a784701de1076f132c379c81794e0ff1R18-R20)

**I'll be using the example of building a mail feature to demonstrate how each part works together.**

### Managers

There are 3 parts to a manager class:

- The manager class itself
- Drivers.
- Optional component classes.

Managers are wrappers around your feature. Its a single entry point for your app. This is typically the class you will be type hinting. If your API looks like this:

```python
def show(self, mail: Mail):
  mail.mailable(Welcome()).send(driver="smtp")
```

Then this manager will have both the `mailable` and `send` methods. This is the front facing class.

The manager is called a manager class because it manages smaller classes. These smaller classes are called drivers.

An example manager looks something like this:

```python
class Mail:
    def __init__(self, application, driver_config=None):
        self.application = application
        self.drivers = {}
        self.driver_config = driver_config or {}
        self.options = {}

    def add_driver(self, name, driver):
        self.drivers.update({name: driver})

    def set_configuration(self, config):
        self.driver_config = config
        return self

    def get_driver(self, name=None):
        if name is None:
            return self.drivers[self.driver_config.get("default")]
        return self.drivers[name]

    def get_config_options(self, driver=None):
        if driver is None:
            return self.driver_config[self.driver_config.get("default")]

        return self.driver_config.get(driver, {})

    def mailable(self, mailable):
        self.options = mailable.set_application(self.application).build().get_options()
        return self

    def send(self, driver=None):
        self.options.update(self.get_config_options(driver))
        return self.get_driver(driver).set_options(self.options).send()
```

The first 4 methods are really the manager boiler plates and the last 2 are the front facing methods needed to make this specific mail feature work.

### Drivers

Driver classes are small classes that do 1 thing and 1 thing only: do the driver logic. If this is an SMTP mail driver then the driver will be responsible for sending an email using SMTP. These driver classes **should not be responsible for anything else**. It should not be responsible for building an actual email, calling a view class to render a template, switching drivers to another driver, nothing. It should do nothing but send an email using SMTP from some kind of data structure like a dictionary of options.

Here is an example of a driver class:

```python
import requests
from .Recipient import Recipient


class MailgunDriver:
    def __init__(self, application):
        self.application = application
        self.options = {}

    def set_options(self, options):
        self.options = options
        return self

    def get_mime_message(self):
        data = {
            "from": self.options.get("from"),
            "to": Recipient(self.options.get("to")).header(),
            "subject": self.options.get("subject"),
            "h:Reply-To": self.options.get("reply_to"),
            "html": self.options.get("html_content"),
            "text": self.options.get("text_content"),
        }

        if self.options.get("cc"):
            data.update({"cc", self.options.get("cc")})
        if self.options.get("bcc"):
            data.update({"bcc", self.options.get("bcc")})

        return data

    def get_attachments(self):
        files = []
        for attachment in self.options.get("attachments", []):
            files.append(("attachment", open(attachment.path, "rb")))

        return files

    def send(self):
        domain = self.options["domain"]
        secret = self.options["secret"]
        attachments = self.get_attachments()

        return requests.post(
            f"https://api.mailgun.net/v3/{domain}/messages",
            auth=("api", secret),
            data=self.get_mime_message(),
            files=attachments,
        )

```

Notice that theres nothing in the class above that isn't related to sending an email with mailgun.

### Component Classes

Component classes are another part of this relationship. A component is also a class that does 1 thing and 1 thing only. This class should have a small peice of logic **that is designed to clean up other parts of the code later down the line**. For example, if we want to compile an email from `joe@masoniteproject.com, idmann509@gmail.com` to `<joe@masoniteproject.com>, <idmann509@gmail.com>` we could loop through the emails and append them inside the SMTP driver, right?

This would look kind of messy and with some psuedo code would look like this:

```python
# Inside the SMTP mail driver
to_emails = []
for email in emails.split(','):
  to_emails.append(f"<{email.trim()}>")
```

This is a problem for a few reasons.

**Problem number 1** is that we now can no longer add cool features to this part of the feature. For example maybe now we want to support something like `Joseph Mancuso idmann509@gmail.com` and compile it down to `Joseph Mancuso <idmann509@gmail.com>`. We can't really do this and if we do we have to add the logic in each mail driver to support this. It also needs to be tested in each mail driver.

**Problem Number 2** is we need to do this for each email address. In a normal email we have things like to, from, cc and bcc. so you can see can _can_ make it work but it will get quite messy. Especially if we have to support more features down the road.

```python
# Inside the SMTP mail driver
to_emails = []
for email in emails.split(','):
  to_emails.append(f"<{email.trim()}>")

cc_emails = []
for email in cc_emails.split(','):
  cc_emails.append(f"<{email.trim()}>")
```

You can see how this can get messy.

**Solution**: better way to do this is to create a component class to do this for us. Final usage of this component class looks something like:

```python
# Inside the SMTP mail driver
to_emails = Recipient(emails).header()
cc_emails = Recipient(cc_emails).header()
```

The same rules apply to an email attachment.

So these component classes should be used where applicable so we can add features at a central location and it be propogated throughout other drivers. They should also do 1 thing and 1 thing only to not break anything with side effects

### Registering Drivers

Registering drivers are simple too. All drivers need to be registered and can be done in the providers. It should simply pass into an `add_driver()` method and look like this:

```python
    def register(self):
        mail = Mail(self.application).set_configuration(config("mail.drivers"))
        mail.add_driver("smtp", SMTPDriver(self.application))
        mail.add_driver("mailgun", MailgunDriver(self.application))
        mail.add_driver("terminal", TerminalDriver(self.application))
        self.application.bind("mail", mail)
```

Notice we just create the manager, bind the drivers to the manager and then bind the manager to the container.
