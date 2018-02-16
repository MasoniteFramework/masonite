DRIVER = 'disk'

DRIVERS = {
    'disk': {
        'location': 'uploads/'
    }
}

SASSFILES = {
    'importFrom': [
        'storage/static'
    ],
    'includePaths': [
        'storage/static/sass'
    ],
    'compileTo': 'storage/compiled'
}

STATICFILES = {
    'storage/static': 'static/',
}
