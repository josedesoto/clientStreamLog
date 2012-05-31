# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

if not request.env.web2py_runtime_gae:     
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite') 
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore') 
    ## store sessions and tickets there
    session.connect(request, response, db = db) 
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
response.generic_patterns = ['*.json']

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db, hmac_key=Auth.get_or_create_key()) 
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables() 

## configure email
mail=auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth,filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

import datetime
now=datetime.datetime.now()
if auth.is_logged_in():
   me=auth.user.id
else:
   me=None

db.define_table('t_project',
    Field('name', notnull=True, default=None),
    Field('description','text', default=None))


db.define_table('t_server',
    Field('project', db.t_project),
    Field('name', notnull=True, default=None),
    Field('IP', notnull=True, default=None),
    Field('port', notnull=True, default=8888),
    Field('description','text', default=None))

db.define_table('t_type_log',
    Field('name'),
    Field('regex_code','text'),
    Field('html_table','text'),
    Field('description', 'text'),
    Field('datecreated','datetime',default=now,readable=False),
    Field('datemodified','datetime',default=now, readable=False))

db.define_table('t_log',
    Field('server', db.t_server),
    Field('type_log', db.t_type_log),
    Field('name'),
    Field('description', 'text'),
    Field('datecreated','datetime',default=now,readable=False),
    Field('datemodified','datetime',default=now, readable=False))



db.t_log.type_log.requires=IS_IN_DB(db,'t_type_log.id', 't_type_log.name')
db.t_server.project.requires=IS_IN_DB(db,'t_project.id', 't_project.name')
db.t_log.server.requires=IS_IN_DB(db,'t_server.id', 't_server.name')
db.t_log.name.requires = IS_NOT_EMPTY()

    

