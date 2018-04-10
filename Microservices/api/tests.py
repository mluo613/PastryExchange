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
        response = self.client.post('/api/v1/users/create', {'username': 'TestNewUser',
                                                  'password': 'TestPassword'})


        response = response.json()

        response = self.client.post('/api/v1/users/update', {'username': 'TestNewUser',
                                                  'password': 'TestPassword', 'newPassword':'TestNewPassword', 'Auth_num':response['Auth_num']})

        self.assertContains(response, 'User exists. Password updated.')

    def testNonExistentUserUpdate(self):
        '''Test when trying to update nonexistent user, the update fails'''
        response = self.client.post('/api/v1/users/create', {'username': 'TestNewUser',
                                                  'password': 'TestPassword'})

        response = response.json()

        response = self.client.post('/api/v1/users/update', {'username': 'NonExistentUser',
                                                                  'password': 'TestNewPassword','Auth_num':'12345'})
        self.assertContains(response, 'Update failed')

    def tearDown(self):
        pass

class DeleteUserAccountTest(TestCase):
    '''User deletes account from the marketplace'''
    def setUp(self):
        management.call_command('loaddata', 'db.json', verbosity=0)
        #pass

    def testDeleteUserAccount(self):
        '''Tests that user is successfully deleted from database'''
        response = self.client.post('/api/v1/users/create', {'username': 'TestNewUser',
                                                  'password': 'TestPassword'})

        response = response.json()

        response = self.client.post('/api/v1/users/delete', {'username':'TestNewUser', 'Auth_num': response['Auth_num']})
        self.assertContains(response, 'User deleted')
        #print(response)
        response2 = self.client.get('/api/v1/users/TestNewUser')
        #print(response2)
        self.assertContains(response2, 'User does not exist.')

    def testDeleteNonexistentUser(self):
        '''Tests that unexistent user deletion returns error message'''
        response = self.client.post('/api/v1/users/delete', {'username': 'Sam', 'Auth_num': '123456'})
        self.assertContains(response, 'Cannot delete user')

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


        response = self.client.post('/api/v1/items/updateItem/' + str(id['item_id']), {'name': 'cake',
                                                                'price': '3.42', 'Auth_num':response['Auth_num']})

        self.assertContains(response, "Item's name and price are updated")

    def testFailedUpdateItem(self):
        '''Tests that update price fails when item does not exist'''
        response = self.client.post('/api/v1/users/create', {'username': 'TestNewUser',
                                                  'password': 'TestPassword'})

        response = response.json()

        response = self.client.post('/api/v1/items/updateItem/2', {'name': 'cake',
                                                                       'price': '3.42','Auth_num': response['Auth_num']})

        self.assertContains(response, 'Item not found')

    def tearDown(self):
        pass
