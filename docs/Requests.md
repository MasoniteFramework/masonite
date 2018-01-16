## Introduction

The `request` object is used primarily inside your controllers and allows you to interact with various things related to the requests handled by the framework. Below we'll explain how the `request` object works as well as some coding examples on how to use it.

### Getting Started

The `request` object you see inside the controller is actually an object instance of the `Request` class. This `Request` class is initialized inside the `bootstrap/start.py` file and is passed down through the request. The `Request` class is the parameter you see as `request` inside your controllers like so:

```python
def show(self, request):
    # request is the instance of Request
    pass
```

### Usage

The `Request` has several helper methods attached to it in order to interact with various aspects of the request.

In order to get the current request input variables such as the form data during a `POST` request or the query string during a `GET` request looks like:

```python
def show(self, request):
    request.input('username')
```

**NOTE: There is no difference between `GET` and `POST` when it comes to getting query strings or form parameters. They are both retrieved through this `input` method so there is no need to make a distinction if the request if `GET` or `POST`**

In order to get all the request input variables such as form data or from a query string. This will return all the available request input variables for that request.

```python
def show(self, request):
    return request.all()
```

To check if a request input variable exists:


```python
def show(self, request):
    return request.has('variable')
```

To get the request parameter retrieved from the url. This is used to get variables inside: `/url/@firstname` for example.

```python
def show(self, request):
    return request.param('firstname')
```

You may also set a cookie in the browser. The below code will set a cookie named `key` to the value of `value`

```python
def show(self, request):
    return request.cookie('key', 'value')
```

You can get all the cookies set from the browser

```python
def show(self, request):
    return request.get_cookies()
```

You can get a specific cookie set from the browser

```python
def show(self, request):
    return request.get_cookie('key')
```

Get the current user from the request. This requires the `LoadUserMiddleware` middleware which is in Masonite by default

```python
def show(self, request):
    return request.user()
```

You can specify a url to redirect to

```python
def show(self, request):
    return request.redirect('/home')
```

You can redirect to a named route

```python
def show(self, request):
    return request.redirectTo('name_of_route')
```

You can also go back to a named route specified from the form parameter `back`. This will get the request input named `back` and redirect to that named route. This is great if you want to redirect the user to a login page and then back to where they came from. Just remember during your form submission that you need to supply a `back` input.

```python
def show(self, request):
    return request.back()
```

This is equivalent to:

```python
def show(self, request):
    return request.redirectTo(request.input('back'))
```

You can also specify the input parameter that contains the named route

```python
def show(self, request):
    return request.back('redirect')
```

Sometimes your routes may require parameters passed to it such as redirecting to a route that has a url like: `/url/@firstname:string/@lastname:string`. For this you can use the `send` method. Currently this only works with named routes.

```python
def show(self, request):
    return request.back().send({'firstname': 'Joseph', 'lastname': 'Mancuso'})

    return request.redirectTo('dashboard').send({'firstname': 'Joseph', 'lastname': 'Mancuso'})

```
