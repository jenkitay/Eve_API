__author__ = 'Taylor'

# Library to Authenticate API Users
# Reference: http://stackoverflow.com/questions/27029842/in-eve-how-can-you-store-the-users-password-securely
# Reference: http://python-eve.org/tutorials/account_management.html#basic-vs-token-final-considerations
# Reference: http://code.tutsplus.com/tutorials/building-rest-apis-using-eve--cms-22961

import bcrypt
from eve import Eve
from eve.auth import BasicAuth      # Implements basic authentication

class BCryptAuth(BasicAuth):
     def check_auth(self, username, password, allowed_roles, resource, method):
         if resource == 'accounts' and method == 'POST':
             return True
         else:
             # use Eve's own db driver; no additional connections/resources are used
             accounts = Eve.app.data.driver.db['accounts']
             account = accounts.find_one({'username': username})
             # set 'auth_field' value to the account's ObjectId
             # (instead of _id, you might want to use ID_FIELD)
             if account and '_id' in account:
                 self.set_request_auth_value(account['_id'])
             return account and bcrypt.hashpw(password.encode('utf-8'), account['salt']) == account['password']

def create_user(documents):
    for document in documents:
        # document['username'] = document['username'].encode('utf-8')
        document['salt'] = bcrypt.gensalt(4)
        password = document['password'].encode('utf-8')
        document['password'] = bcrypt.hashpw(password, document['salt'])



class MyBasicAuth(BasicAuth):
    def check_auth(self, username, password, allowed_roles, resource, method):
        return username == "admin" and password == "secret"

class Authenticate(BasicAuth):
    def check_auth(self, username, password, allowed_roles, resource, method):
        if resource == 'user' and method == 'GET':
            user = Eve.app.data.driver.db['user']
            user = user.find_one({'username': username,'password':password})
            if user:
                return True
            else:
                return False
        elif resource == 'user' and method == 'POST':
            return username == 'admin' and password == 'admin'
        else:
            return True