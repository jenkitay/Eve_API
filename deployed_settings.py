__author__ = 'Taylor'
import os

# Reference: http://python-eve.org/config.html
# Reference: http://python-eve.org/quickstart.html

# We want to run our API seamlessly, both locally and on the cloud, so:
LOCAL = True
if os.environ.get('PORT'):
    # We're hosted on Heroku! Using the mongolab.com sandbox as our backend.
    MONGO_HOST = 'ds061228.mongolab.com'
    MONGO_PORT = 61228
    MONGO_USERNAME = 'DB_USER'
    MONGO_PASSWORD = 'DB_PASSWORD'
    MONGO_DBNAME = 'practice'
elif LOCAL:
    # We are running on a local machine, so just use the local mongod instance.
    # print("Running local DB")
    # Note that MONGO_HOST and MONGO_PORT could very well be left
    # out as they already default to a bare bones local 'mongod' instance.
    MONGO_HOST = 'localhost'
    MONGO_PORT = 27017
    MONGO_USERNAME = ''
    MONGO_PASSWORD = ''
    MONGO_DBNAME = 'practice'
else:
    # We're hosted on a cloud server! Using the mongolab.com sandbox as our backend.
    # print("running on mongolab")
    MONGO_HOST = 'ds061228.mongolab.com'
    MONGO_PORT = 61228
    MONGO_USERNAME = 'DB_USER'
    MONGO_PASSWORD = 'DB_PASSWORD'
    MONGO_DBNAME = 'practice'
    # MONGO_URI "mongodb://DB_USER:DB_PASSWORD@ds061228.mongolab.com:61228/practice"

# Name of the field used to store the owner of each document
AUTH_FIELD = 'user_id'

# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# Enable reads (GET), edits (PATCH), replacements (PUT) and deletes of
# individual items  (defaults to read-only item access).
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']
IF_MATCH = False  # When set to false, older versions may potentially replace newer versions

XML = False  # disable xml output

# Schemas for data objects are defined here:
classes = {
    'item_title': 'class',  # 'title' tag used in item links.
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'subject',
    },
    # most global settings can be overridden at resource level
    'resource_methods': ['GET', 'POST'],
    # Schema definition, based on Cerberus grammar. Check the Cerberus project
    # (https://github.com/nicolaiarocci/cerberus) for details.
    'schema': {
        'subject': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 32,
            'required': True,
            'unique': True,  # name is an API entry-point so it must be unique.
        },
        'teachers': {
            'type': 'list',
            'schema': {
                # 'teacher': {
                'type': 'objectid',
                # 'required': True,
                # referential integrity constraint: value must exist in the
                # 'people' collection. Since we aren't declaring a 'field' key,
                # will default to `people._id` (or, more precisely, to whatever
                # ID_FIELD value is).
                'data_relation': {
                    'resource': 'people',
                    'field': '_id',
                    # make the teacher embeddable with ?embedded={"teacher":1}
                    'embeddable': True
                },
                # },
            },
        },
        'students': {
            'type': 'list',
            'schema': {
                # 'student': {
                'type': 'objectid',
                # 'required': True,
                # referential integrity constraint: value must exist in the
                # 'people' collection. Since we aren't declaring a 'field' key,
                # will default to `people._id` (or, more precisely, to whatever
                # ID_FIELD value is).
                'data_relation': {
                    'resource': 'people',
                    'field': '_id',
                    # make the student embeddable with ?embedded={"student":1}
                    'embeddable': True
                },
                # },
            },
        },
    }
}

people = {
    # 'title' tag used in item links. Defaults to the resource title minus
    # the final, plural 's' (works fine in most cases but not for 'people')
    'item_title': 'person',

    # by default the standard item entry point is defined as
    # '/people/<ObjectId>'. We leave it untouched, and we also enable an
    # additional read-only entry point. This way consumers can also perform
    # GET requests at '/people/<id_number>'.
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'id_number',
    },

    # We choose to override global cache-control directives for this resource.
    # 'cache_control': 'max-age=10,must-revalidate',
    # 'cache_expires': 10,

    # most global settings can be overridden at resource level
    'resource_methods': ['GET', 'POST'],

    'schema': {
        # Schema definition, based on Cerberus grammar. Check the Cerberus project
        # (https://github.com/nicolaiarocci/cerberus) for details.
        'id_number': {
            'type': 'string',
            'regex': '^\d{7}$',
            'required': True,
            'unique': True,
        },
        'firstname': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 10,
        },
        'lastname': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 15,
            'required': True,
        },
        # An embedded 'strongly-typed' dictionary.
        'contact': {
            'type': 'dict',
            'schema': {
                'address': {'type': 'string'},
                'city': {'type': 'string'},
                'state': {'type': 'string'},
                'zip': {'type': 'string', 'regex': '^\d{5}$'},
                'phone': {'type': 'string', 'regex': '^\d\d\d-\d\d\d-\d\d\d\d$'},
                'email': {'type': 'string', 'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'},
            },
        },
        'about': {
            'type': 'string',
            'maxlength': 1024,
        },
    },
}

logs = {
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'due_date',
    },
    # most global settings can be overridden at resource level
    'resource_methods': ['GET', 'POST'],
    'schema': {
        'student_id': {
            'type': 'string',
            'required': True,
            'data_relation': {
                'resource': 'people',
                'field': 'id_number',
                # make the student embeddable with ?embedded={"student":1}
                'embeddable': True,
            },
        },
        'assignment': {
            'type': 'string',
            'maxlength': 1024,
        },
        'due_date': {
            'type': 'datetime',
            'required': True,
        },
        'goal': {
            'type': 'string',
            'maxlength': 1024,
        },
        'reflection': {
            'type': 'string',
            'maxlength': 1024,
        },
        'sessions': {
            'type': 'list',
            'schema': {
                # 'session': {
                'type': 'objectid',
                # 'required': True,
                'data_relation': {
                    'resource': 'sessions',
                    # make the student embeddable with ?embedded={"student":1}
                    'embeddable': True
                },
                # },
            },
        },
    },
}

sessions = {
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'date',
    },
    # most global settings can be overridden at resource level
    'resource_methods': ['GET', 'POST'],
    'schema': {
        'date': {
            'type': 'datetime',
        },
        'duration': {'type': 'string',
                     'regex': '^\d\d:\d\d:\d\d$'
                     },
        'comment': {
            'type': 'string',
            'maxlength': 1024,
        },
    },
}

accounts = {
    # the standard account entry point is defined as '/accounts/<ObjectId>'.
    # an additional read-only entry point is accessible at '/accounts/<username>'.
    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'username',
    },
    # most global settings can be overridden at resource level
    'resource_methods': ['GET', 'POST'],

    # disable endpoint caching to prevent apps from caching account data
    'cache_control': '',
    'cache_expires': 0,

    # schema for the accounts endpoint
    'schema': {
        'username': {
            'type': 'string',
            'required': True,
            'unique': True,
        },
        'password': {
            'type': 'string',
            'required': True,
        },
        'salt': {
            'type': 'string',
        },
    },
}

# The DOMAIN dict explains which resources will be available and how they will
# be accessible to the API consumer.
DOMAIN = {
    'classes': classes,
    'people': people,
    'logs': logs,
    'sessions': sessions,
    'accounts': accounts,
}
