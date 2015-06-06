__author__ = 'Taylor'

# The main start file for jenkitay.pythonanywhere.com
# Use this instead of run.py on hosted site. Use run.py for local development.

from flask import Flask
# from flask.ext.bcrypt import Bcrypt
# import os.path
from eve import Eve
from flask.ext.bootstrap import Bootstrap
from eve_docs import eve_docs
import bcrypt
from eve.auth import BasicAuth      # Implements basic authentication


# Reference: http://stackoverflow.com/questions/27029842/in-eve-how-can-you-store-the-users-password-securely
# Reference: http://python-eve.org/tutorials/account_management.html#basic-vs-token-final-considerations
# Reference: http://code.tutsplus.com/tutorials/building-rest-apis-using-eve--cms-22961
class BCryptAuth(BasicAuth):
     def check_auth(self, username, password, allowed_roles, resource, method):
         if resource == 'accounts' and method == 'POST':
             return True
         elif username == 'admin' and password == 'admin':
             return True
         else:
             # use Eve's own db driver; no additional connections/resources are used
             accounts = app.data.driver.db['accounts']
             account = accounts.find_one({'username': username})
             # set 'auth_field' value to the account's ObjectId
             # (instead of _id, you might want to use ID_FIELD)
             if account and '_id' in account:
                 self.set_request_auth_value(account['_id'])
             return account and bcrypt.hashpw(password.encode('utf-8'), account['salt']) == account['password']

def create_user(documents):
    for document in documents:
        document['salt'] = bcrypt.gensalt(4)
        password = document['password'].encode('utf-8')
        document['password'] = bcrypt.hashpw(password, document['salt'])


app = Flask(__name__)
app = Eve(auth=BCryptAuth, settings = '/home/jenkitay/mysite/deployed_settings.py')
app.on_insert_accounts += create_user
Bootstrap(app)
app.register_blueprint(eve_docs, url_prefix='/docs')

@app.route('/')
def index():
    # return 'Hello World'
    return app
