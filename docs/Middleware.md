## Introduction

Middleware is an extremely important aspect of web applications as it allows you to run important code either before or after every request or even before or after certain routes. In this documentation we'll talk about how middleware works, how to consume middleware and how to create your own middleware. Middleware is only ran when the route is found and a status code of 200 will be returned.

### Getting Started

Middleware in placed inside the `app/http/middleware` but can be placed anywhere you like. All middleware are just classes that take in a request and contain a `before` method and an `after` method.

There are four types of middleware in total:

* Middleware ran before every request
* Middleware ran after every request
* Middleware ran before certain routes
* Middleware ran after certain routes

#### Creating Middleware

Again, middleware should live inside the `app/http/middleware` folder and should look something like:

```python
class AuthenticationMiddleware(object):
    ''' Middleware class which loads the current user into the request '''

    def __init__(self, request):
        self.request = request

    def before(self):
        pass

    def after(self):
        pass
```

This is a boilerplate for middleware. It's simply a class with a before and after method. Creating a middleware is that simple. Let's create a middleware that checks if the user is authenticated and redirect to the login page if they are not. Because we have access to the request object, we can do something like:

```python
class AuthenticationMiddleware(object):
    ''' Middleware class which loads the current user into the request '''

    def __init__(self, request):
        self.request = request

    def before(self):
        if not self.request.user():
            self.request.redirectTo('login')

    def after(self):
        pass
```

That's it! Now we just have to make sure our route picks this up. If we wanted this to execute after a request, we could use the exact same logic in the `after` method instead.

#### Configuration

We have one of two lists we need to work with. These lists both reside in our `config/middleware.py` file and are `HTTP_MIDDLEWARE` and `ROUTE_MIDDLEWARE`.

`HTTP_MIDDLEWARE` is a simple list which should contain your middleware classes. This constant is a list because all middleware will simply run in succession one after another, similiar to Django middleware

In our `config/middleware.py` file this type of middleware may look something like:

```python
from app.http.middleware.AuthenticationMiddleware import AuthenticationMiddleware

HTTP_MIDDLEWARE = [
    AuthenticationMiddleware
]
```

`ROUTE_MIDDLEWARE` is also simple but instead is a dictionary with a custom name as the key and the middleware class as the value. This is so we can specify the middleware based on the key in our routes file.

In our `config/middleware.py` file this might look something like:

```python
from app.http.middleware.RouteMiddleware import RouteMiddleware

ROUTE_MIDDLEWARE = {
    'auth': RouteMiddleware
}
```

#### Consuming Middleware

Using middleware is also simple. If we put our middleware in the `HTTP_MIDDLEWARE` constant then we don't have to worry about it anymore. It will run on every successful request.

If we are using a route middleware, we'll need to specify which route should execute the middleware. To specify which route we can just append a `.middleware()` method onto our routes. This will look something like:

```python
Get().route('/dashboard', 'DashboardController@show').name('dashboard').middleware('auth')
Get().route('/login', 'LoginController@show').name('login')
```

This will execute the auth middleware only when the user visits the `/dashboard` url and as per our middleware will be redirected to the named route of `login`

That's it! That's how middleware works. It's a very simple solution to the middleware problem.