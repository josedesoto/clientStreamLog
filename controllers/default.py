# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


#@auth.requires_login()
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    """
    db.t_log.id.readable=False
    db.t_log.server.readable=False
    
    db.t_log.type_log.readable=False
    links = [lambda row:  INPUT(_type='button',_value='Load Table', _onclick='loadTable('+str(row.id)+')')]
    links += [lambda row:  INPUT(_type='button',_value='START STREAM', _onclick='createStream('+str(row.id)+')')]
    form=SQLFORM.grid(db.t_log, selectable=False, csv=False,create=False, deletable=False, editable=False, links=links, user_signature=False)
    return dict(message=T('Hello World2'), form=form)

'''
@auth.requires_login()
def getConnectionData():
    
    id_log=request.args[0]
    ip=''
    port=''
    name_log=''
    
    data_connection=db((db.t_log.id==id_log)&(db.t_log.server==db.t_server.id)).select(db.t_log.name,db.t_server.IP,db.t_server.port)
  
    for row in data_connection:
        ip=row.t_server.IP
        port=row.t_server.port
        name_log=row.t_log.name
        
    
    regex=db((db.t_log.id==id_log)&(db.t_log.type_log==db.t_type_log.id)).select()
    
    regex_code=''
    for row in regex:
        regex_code=row.t_type_log.regex_code
    
    #return response.json([{'name_log': name_log,'IP': ip,'port': port,'regex': regex_code}])
    return dict(name_log=name_log, ip=ip, port=port,regex=regex_code)

'''




#@auth.requires_login()
def getConnectionData():
    
    id_log=request.args[0]
    ip=''
    port=''
    name_log=''
    server=''
    
    row_log=db(db.t_log.id==id_log).select(db.t_log.server,db.t_log.name,db.t_log.type_log)[0]
    server=row_log.server
    name_log=row_log.name
    type_log=row_log.type_log	
                       
    data_connection=db(db.t_server.id==server).select(db.t_server.IP,db.t_server.port)[0]
    ip=data_connection.IP
    port=data_connection.port 
    
        
    regex=db(db.t_type_log.id==type_log).select(db.t_type_log.regex_code)[0]
    regex_code=regex.regex_code
  
    
    #return response.json([{'name_log': name_log,'IP': ip,'port': port,'regex': regex_code}])
    return dict(name_log=name_log, ip=ip, port=port,regex=regex_code)


#@auth.requires_login()
def getTypeTable():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    """
    table=''
    id_log=request.args[0]
    row_log=db(db.t_log.id==id_log).select(db.t_log.type_log)[0]
        
    type_table=db(db.t_type_log.id==row_log.type_log).select(db.t_type_log.html_table)[0]
       
    return type_table.html_table

'''
@auth.requires_login()
def getTypeTable():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    """
    table=''
    id_log=request.args[0]
    type_table=db((db.t_log.id==id_log)&(db.t_log.type_log==db.t_type_log.id)).select(db.t_type_log.html_table)
    for row in type_table:
        table=row.html_table
        
    
    return table
'''

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    auth.settings.actions_disabled.append('register')
    auth.settings.actions_disabled.append('request_reset_password')
    auth.settings.actions_disabled.append('login')
    return dict(form=auth())

def error():
    return dict()


#@auth.requires_login()
def project_manage():
    
    form = SQLFORM.smartgrid(db.t_project,csv=False,user_signature = False)
    return locals()

#@auth.requires_login()
def server_manage():

    form=SQLFORM.grid(db.t_server,csv=False, user_signature = False)
    return locals()

#@auth.requires_login()
def log_manage():
 
    #form = SQLFORM.smartgrid(db.t_log,constraints=dict(t_log=query), selectable=True,searchable=False, csv=False,showbuttontext=True,onupdate=auth.archive)
    #form = SQLFORM.smartgrid(db.t_log)
    form=SQLFORM.grid(db.t_log,csv=False,user_signature = False)
    return locals()

#@auth.requires_login()
def type_log_manage():

    form=SQLFORM.grid(db.t_type_log,csv=False,user_signature = False)
    return locals()

def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


#@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs bust be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
