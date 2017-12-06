from app.http.providers.view import view

class AboutController():
	
	def show(self):
		return view('home')