''' Maintainance Mode Middleware '''
import os
from config import application

class MaintainceModeMiddleware:
    ''' Middleware To Check Maintaince Mode'''

    def __init__(self, Request:
        ''' Inject Any Dependencies From The Service Container '''
        self.request = Request


    def before(self):
        ''' Run This Middleware Before The Route Executes '''
        down = os.path.exists(os.path.join(application.BASE_DIRECTORY, 'bootstrap/down'))
        if down is True:
            self.request.status('503 Service Unavailable')
            return # todo return response request lifecycle should stop 
    def after(self):
        ''' Run This Middleware After The Route Executes '''
        pass
