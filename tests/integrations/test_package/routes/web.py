from src.masonite.routes import Route

ROUTES = [
    Route.get("/package/test/", "PackageController@index"),
]
