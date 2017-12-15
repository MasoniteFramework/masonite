''' Storage Asset Definitions '''

'''
|--------------------------------------------------------------------------
| Static Files
|--------------------------------------------------------------------------
|
| Put anywhere you keep your static assets in a key, value dictionary here
| The key will be the folder you put your assets in relative to the root
| and the value will be the alias you wish to have in your templates.
| You may have multiple aliases of the same name
|
| Example will be the static assets folder at /storage/static
| and an alias of <img src="/static/image.png"
|
'''

STATICFILES = {
    # folder          # template alias
    'storage/static': 'static/',
    'storage/uploads': 'static/',
}
