from app.http.providers.view import view

class WelcomeController():
	
	def show(self):
		return view('welcome')