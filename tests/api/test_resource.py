from masonite.api.Resource import Resource
from masonite.api.JsonSerialize import JsonSerialize
from masonite.testsuite.TestSuite import TestSuite


# from config.database import Model

# ''' User Model '''
# class User(Model):
#     ''' User Model '''

#     __fillable__ = ['name', 'email', 'password']

#     __auth__ = 'email'


# class UserResource(Resource, JsonSerialize):
#     pass

# class RandomClass:
#     def __init__(self):
#         self.x = 1
#         self._y = 2
    
#     def random_func(self): pass

# def test_user_resource_can_serialize():
#     container = TestSuite().create_container().container
#     request = container.make('Request')

#     request.path = '/api/user'

#     user_resource = UserResource(User()).load_request(container.make('Request'))

#     assert len(user_resource.handle()) > 1

#     request.path = '/api/user/5'

#     user_resource = UserResource(User()).load_request(
#         container.make('Request'))

#     assert len(user_resource.handle()) == 332


