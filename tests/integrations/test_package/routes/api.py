from src.masonite.routes import Route

ROUTES = [
    Route.get("/api/package/test/", "PackageController@api"),
]
