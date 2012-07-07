# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.title = request.application
response.subtitle = T('Stream Log Client!')

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Jose de Soto <josedesoto@gmail.com>'
response.meta.description = 'a cool new app'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'
response.meta.copyright = 'Copyright 2012'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Index'), False, URL('default','index'), [])

    ]


response.menu+=[
        (T('Manage'),False, None, [
		(T('Logs'), False, URL('default','log_manage'), []),
        	(T('Servers'), False, URL('default','server_manage'), []),
   		(T('Projects'), False, URL('default','project_manage'), []),
		(T('Type Logs'), False, URL('default','type_log_manage'), [])
	])]

#########################################################################
## provide shortcuts for development. remove in production
#########################################################################

