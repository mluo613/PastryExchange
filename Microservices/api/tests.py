from django.test import TestCase
from api import views
from api.models import User, Item
from django.core import management
import json

# Create your tests here.

class UserTestCase(TestCase):
    '''New user creates an account on the market'''
    #fixtures = ['db.json']

    def setUp(self):
        management.call_command('loaddata', 'db.json', verbosity=0)
        #pass

#    def testGetValidUser(self):
        '''Test that request for valid user returns username'''
#        response = self.client.get('/api/v1/users/Neha')
#        self.assertContains(response, 'Neha')

    def testGetInvalidUser(self):
        '''Tests that invalid user returns error message'''
        response = self.client.get('/api/v1/users/NonexistentUser')
        self.assertContains(response, 'User does not exist.')

    def testCreateUser(self):
        '''Test creating new user and if get is able to access'''
        self.client.post('/api/v1/users/create', {'username':'TestNewUser',
                                                            'password':'TestPassword'})
        response = self.client.get('/api/v1/users/TestNewUser')
        self.assertContains(response, 'TestNewUser')

    def tearDown(self):
        pass

class UpdateUserAccountTest(TestCase):
    '''User would like to update user account'''
    def setUp(self):
        management.call_command('loaddata', 'db.json', verbosity=0)
        #pass

    def testUpdateUserPassword(self):
        '''Test if password is updated'''
        self.client.post('/api/v1/users/create', {'username': 'TestNewUser',
                                                  'password': 'TestPassword'})

        response = self.client.post('/api/v1/users/login', {'username': 'TestNewUser',
                                                            'password': 'TestPassword'})


        response = self.client.post('/api/v1/users/TestNewUser', {'username': 'TestNewUser',
                                                  'password': 'TestPassword', 'newPassword':'TestNewPassword'})
        self.assertContains(response, 'User exists. Password updated.')

    def testNonExistentUserUpdate(self):
        '''Test when trying to update nonexistent user, the update fails'''
        self.client.post('/api/v1/users/create', {'username': 'TestNewUser',
                                                  'password': 'TestPassword'})

        response = self.client.post('/api/v1/users/NonExistentUser', {'username': 'NonExistentUser',
                                                                  'password': 'TestNewPassword'})
        self.assertContains(response, 'User does not exist.')

    def tearDown(self):
        pass

class DeleteUserAccountTest(TestCase):
    '''User deletes account from the marketplace'''
    def setUp(self):
        management.call_command('loaddata', 'db.json', verbosity=0)
        #pass

    def testDeleteUserAccount(self):
        '''Tests that user is successfully deleted from database'''
        self.client.post('/api/v1/users/create', {'username': 'TestNewUser',
                                                  'password': 'TestPassword'})
        response = self.client.post('/api/v1/users/TestNewUser/delete')
        self.assertContains(response, 'User deleted')
        #print(response)
        response2 = self.client.get('/api/v1/users/TestNewUser')
        #print(response2)
        self.assertContains(response2, 'User does not exist.')

    def testDeleteNonexistentUser(self):
        '''Tests that unexistent user deletion returns error message'''
        response = self.client.post('/api/v1/users/Sam/delete')
        self.assertContains(response, 'Cannot delete user because user does not exist.')

    def tearDown(self):
        pass



class UploadItemTestCase(TestCase):
    '''User uploads an item for sale on the marketplace.'''

    def setUp(self):
        management.call_command('loaddata', 'db.json', verbosity=0)
        #pass

    def testUploadItem(self):
        '''Testing if Item is uploaded and can be retrived by get'''
        response = self.client.post('/api/v1/users/create', {'username': 'TestNewUser',
                                                  'password': 'TestPassword'})

        response = response.json()

        response = self.client.post('/api/v1/users/uploadItem', {'name':'cake',
                                                                  'price':'2.34', 'Auth_num':response['Auth_num']})

        self.assertContains(response, 'item_id')

    def testUploadUserNonExistentFailed(self):
        '''Tests if upload item fails accordingly when the user doesn't exist'''
        response = self.client.post('/api/v1/users/uploadItem')
        self.assertContains(response, 'User not logged in. Please login before uploading.')

    def tearDown(self):
        pass


class UpdateItemTestCase(TestCase):
    '''User updates the price of an item'''
    def setUp(self):
        management.call_command('loaddata', 'db.json', verbosity=0)
        #pass

    def testUpdatePrice(self):
        '''Test to update the price of an item '''
        response = self.client.post('/api/v1/users/create', {'username': 'TestNewUser',
                                                  'password': 'TestPassword'})

        response = response.json()

        id = self.client.post('/api/v1/users/uploadItem', {'name': 'cake',
                                                                  'price': '2.34', 'Auth_num':response['Auth_num']})
        id = id.json()


        response = self.client.post('/api/v1/users/TestNewUser/items/updateItem/' + str(id['item_id']), {'name': 'cake',
                                                                'price': '3.42'})

        self.assertContains(response, 'Item price updated')

    def testFailedUpdateItem(self):
        '''Tests that update price fails when item does not exist'''
        self.client.post('/api/v1/users/create', {'username': 'TestNewUser',
                                                  'password': 'TestPassword'})
        response = self.client.post('/api/v1/users/TestNewUser/items/updateItem/2', {'name': 'cake',
                                                                       'price': '3.42'})

        self.assertContains(response, 'Item not found')

    def tearDown(self):
        pass
