from masoniteorm.models import Model
from src.masonite.authentication import Authenticates
from src.masonite.authorization import Authorizes
from src.masonite.notification import Notifiable


class User(Model, Authenticates, Authorizes, Notifiable):
    __fillable__ = ["name", "password", "email", "phone"]
