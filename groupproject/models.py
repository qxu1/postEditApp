"""
This file defines the database models
"""

import datetime
from .common import db, Field, auth
from pydal.validators import *


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()


### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later

db.define_table('contact',
                Field('first_name'),
                Field('last_name'),
                Field('thumbnail', 'text'),
                )
db.define_table(
    'post',
    Field('user_name', requires=IS_NOT_EMPTY()),
    Field('like', 'integer', default=0, requires=IS_INT_IN_RANGE(0, 1e6)),
    Field('user_email', default=get_user_email),
)

db.commit()
