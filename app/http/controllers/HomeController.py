from app.http.providers.view import view

class HomeController:

    def show(self):
        return view('index', {"name": "joseph", "lastname": "Mancuso"})