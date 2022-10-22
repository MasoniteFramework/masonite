def app(binding=None, *arguments):
    from wsgi import application

    if binding:
        return application.make(binding, *arguments)
    else:
        return application
