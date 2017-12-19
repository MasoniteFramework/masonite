import shutil

def auth():
    f = open('routes/web.py', 'a')

    # add all the routes
    f.write('\nfrom app.http.controllers.LoginController import LoginController\n')
    f.write('from app.http.controllers.RegisterController import RegisterController\n')
    f.write('from app.http.controllers.HomeController import HomeController\n')
    f.write('\nROUTES = ROUTES + [\n    ')
    f.write("Get().route('/login', LoginController().show),\n    ")
    f.write("Get().route('/logout', LoginController().logout),\n    ")
    f.write("Post().route('/login', LoginController().store),\n    ")
    f.write("Get().route('/register', RegisterController().show),\n    ")
    f.write("Post().route('/register', RegisterController().store),\n    ")
    f.write("Get().route('/home', HomeController().show),\n")
    f.write(']\n')

    # move controllers
    shutil.copyfile("kernal/auth/controllers/LoginController.py",
                    "app/http/controllers/LoginController.py")
    shutil.copyfile("kernal/auth/controllers/RegisterController.py",
                    "app/http/controllers/RegisterController.py")
    shutil.copyfile("kernal/auth/controllers/HomeController.py",
                    "app/http/controllers/HomeController.py")

    # move templates
    shutil.copytree("kernal/auth/templates/auth",
                    "resources/templates/auth")
