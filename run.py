__author__ = 'Taylor'

import os.path
from eve import Eve
from flask.ext.bootstrap import Bootstrap
from eve_docs import eve_docs

DEPLOYED = True

if os.path.exists('deployed_settings.py') and DEPLOYED:
    app = Eve(settings = 'deployed_settings.py')
else:
    app = Eve(settings = 'settings.py')


Bootstrap(app)
app.register_blueprint(eve_docs, url_prefix='/docs')

if __name__ == '__main__':
    app.run()
