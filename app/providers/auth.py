import shutil

def auth():
    f = open('routes/web.py', 'a')

    # add all the routes
    f.write('\nfrom app.http.controllers.LoginController import LoginController\n')
    f.write('from app.http.controllers.RegisterController import RegisterController\n')
    f.write('\nroutes = routes + [\n    ')
    f.write("Get().route('/login', LoginController().show()),\n    ")
    f.write("Get().route('/register', RegisterController().show())\n")
    f.write(']')

    # move controllers
    shutil.copyfile("kernal/auth/controllers/LoginController.py",
                    "app/http/controllers/LoginController.py")
    shutil.copyfile("kernal/auth/controllers/RegisterController.py",
                    "app/http/controllers/RegisterController.py")

    # move templates
    shutil.copyfile("kernal/auth/templates/login.blade.html",
                    "resources/templates/login.blade.html")
    shutil.copyfile("kernal/auth/templates/register.blade.html",
                    "resources/templates/register.blade.html")
