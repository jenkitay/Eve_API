__author__ = 'Taylor'

import os.path
from eve import Eve
# import my_auth
from flask.ext.bootstrap import Bootstrap
from eve_docs import eve_docs
import bcrypt
from eve.auth import BasicAuth      # Implements basic authentication

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
        # document['username'] = document['username'].encode('utf-8')
        document['salt'] = bcrypt.gensalt(4)
        password = document['password'].encode('utf-8')
        document['password'] = bcrypt.hashpw(password, document['salt'])

DEPLOYED = True

if os.path.exists('deployed_settings.py') and DEPLOYED:
    app = Eve(auth=BCryptAuth, settings = 'deployed_settings.py')
    # app = Eve(settings = 'deployed_settings.py')
else:
    app = Eve(settings = 'settings.py')

app.on_insert_accounts += create_user
Bootstrap(app)
app.register_blueprint(eve_docs, url_prefix='/docs')

if __name__ == '__main__':
    app.run()
