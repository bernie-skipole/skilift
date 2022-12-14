

# from skipole import the WSGIApplication class which will be used to create a wsgi application

from skipole import WSGIApplication, FailPage, GoTo, ValidateError, ServerError, ServeFile, use_submit_list, skis, PageData, SectionData, set_debug

# FailPage, GoTo, ValidateError, ServerError, ServeFile are exception classes which you can raise in your own code

# use_submit_list is a decorator described below

# skis is another skipole project which serves javascript files and its use is shown below

# PageData and SectionData are dictionary-like objects with attributes. Your code sets contents into
# these which will be applied to the page finally returned to the user.

# set_debug(True) causes exception information to be displayed, a deployed site should normally
# have the default set_debug(False)

# the framework needs to know the location of the projectfiles directory holding the project data
# and static files.

PROJECTFILES = os.path.dirname(os.path.realpath(__file__))
PROJECT = "newproj"

# This file newproj.py is initially created under the projectfiles directory, however it does not
# need to be sited there, and can be moved and your code developed elsewhere. The above PROJECTFILES
# path is only needed to set the location of the support files used by the project, not code. 

# proj_data is an optional dictionary of values which you are free to use, it will be made
# available to your functions as the attribute 'skicall.proj_data'

PROJ_DATA={}


# Your code needs to provide your own version of the following three functions which will
# be used to set values into the widgets of returned pages. Minimal versions are provided below.

# When a call is received by the server, the framework converts the url called to a 'called_ident'
# which is a tuple (proj_ident, pagenumber), and then, if this is the project called, this
# start_call function is called. If the page called is not recognised, called_ident will be None.

# The skicall object has attributes and methods pertaining to the call. 


def start_call(called_ident, skicall):
    """When a call is initially received this function is called.
       Unless you want to divert to another page, this function should return the given called_ident
       which would typically be the ident of a Responder matching the url called.
       Each page ident is a tuple of the form (proj_ident, pagenumber) where proj_ident is
       usually the project name but can be set to a string when an instance of the WSGIApplication
       class is created.
       If a ServeFile exception is raised in this function, which contains a pathlib.Path object
       of a local server file then that server file will be sent to the client."""

    # To serve a directory of static files, you can map a url to a server directory with the
    # skicall.map_url_to_server method, which returns pathlib.Path objects, and then
    # raise a ServeFile exception, which causes the file to be served. For example:
    # servedfile = skicall.map_url_to_server("images", "/home/user/thisproject/imagefiles")
    # if servedfile:
    #    raise ServeFile(servedfile)

    # Of particular interest at this point are the attributes:
    # skicall.received_cookies is a dictionary of cookie name:values received from the client
    # skicall.call_data is a dictionary which you can set with your own data and, as skicall is
    # passed on to the submit_data and end_call functions defined below, can be used to pass
    # data to these functions.

    # Normally you would return called_ident, which is the page being called, or None to cause a
    # page not found error, or another ident (proj_ident, pagenumber) to divert the call to another page.

    return called_ident

# After start_call, if the call is passed to a Responder page which you have set up to call
# submit_data, then the function below will be called.
#
# You may wish to apply the decorator '@use_submit_list' to this submit_data function. This
# takes the package, module and function name which you have set in the Responder's 'submit list'
# and imports and calls that specified function instead. This is entirely optional. 

def submit_data(skicall):
    """This function is called when a Responder wishes to submit data for processing in some manner
       Typically you would create a PageData object containing widget,field values and call the
       skicall.update method, where the data will be applied to the page returned"""
    # For example, if you have a page with a widget 'displaydata' and with a field 'hide' which you want
    # to set to True, you would use:
    #   pd = PageData()
    #   pd['displaydata','hide'] = True
    #   pd['otherwidgets', 'otherfields'] = 'Other values'
    # You may also have a section in the page, with a section alias of "mysection"
    #   sd = SectionData("mysection")
    #   sd['anotherwidget', 'widgetfield'] = "Text displayed on widget"
    # And then update pd with this section data
    #   pd.update(sd)
    # and finally, you would set the pd into skicall using update
    #   skicall.update(pd)

    return


def end_call(page_ident, page_type, skicall):
    """This function is called prior to returning a page,
       it can also be used to return an optional session cookie string."""

    # page_ident is the ident of the page being returned. A tuple (proj_ident, pagenumber),
    # this is usually the ident of the template, css etc., page but can also be the ident
    # of one of the responders which create a dynamic page.

    # page_type is a string giving the type of the page returned, typically 'TemplatePage',
    # 'CSS', 'SVG', 'FilePage' or 'JSON'. Certain responders create their own pages and for
    # these the page_type will be the responder type, one of 'SubmitJSON', 'SubmitPlainText',
    # 'SubmitCSS', 'SubmitIterator'.

    # This function should return either None, or optionally a session cookie string. This
    # string will be returned with the next call to this web site in the skicall.received_cookies
    # dictionary with key being the proj_ident.

    return


# The above functions are required as arguments to the skipole.WSGIApplication object
# and will be called as required.

# create the wsgi application
application = WSGIApplication(project=PROJECT,
                              projectfiles=PROJECTFILES,
                              proj_data=PROJ_DATA,
                              start_call=start_call,
                              submit_data=submit_data,
                              end_call=end_call,
                              url="/")

# As well as the above arguments, a further argument proj_ident can be included in the above
# (for skipole version 5.5.2 and later), if this is left at its default None value, then it
# will be automatically set to the project name. However it can be set to a different string
# here which may be useful if multiple instances of this project are to be added to a parent
# 'root' project. Each unique proj_ident will then define each of the sub applications.

# This proj_ident value is then used as part of the page ident tuples (proj_ident, pagenumber)


# Add the 'skis' application which serves javascript and css files required by
# the framework widgets.

# The skipole.skis package, contains the function makeapp() - which returns a
# WSGIApplication object which is then appended to your own project

skis_application = skis.makeapp()
application.add_project(skis_application, url='/lib')

# The add_project method of WSGIApplication enables the added sub application
# to be served at a URL which should extend the URL of the main 'root' application.
# The above shows the main application served at "/" and the skis library
# project served at "/lib"

# You can add further sub applications using the add_project method which has signature
# application.add_project(subapplication, url=None, check_cookies=None)
# The optional check_cookies argument can be set to a function which you would create, with signature:
# def my_check_cookies_function(received_cookies, proj_data):
# Before the call is routed to the subapplication, your my_check_cookies_function is called, with the
# received_cookies dictionary, and with your application's proj_data dictionary. If your function
# returns None, the call proceeds unhindered to the subapplication. If however your function returns
# an ident tuple, of the form (proj_ident, pagenumber), then the call is routed to that page instead.


#############################################################################
#
# You should remove everything below here when deploying and serving your
# finished application. The following lines are used to serve the project
# locally and add the skiadmin project for development.

# Normally, when deploying on a web server, you would follow the servers
# own documentation which should describe how to load a wsgi application.
# for example, using gunicorn3 by command line

# gunicorn3 -w 4 newproj:application

# Where gunicorn3 is the python3 version of gunicorn

############### THESE LINES IMPORT SKILIFT AND ADD THE SKIADMIN SUB-PROJECT #
############### AND SHOULD BE REMOVED WHEN YOU DEPLOY YOUR APPLICATION #

## The skilift package is only needed for development, it is not needed
## for your finished application


if __name__ == "__main__":

    set_debug(True)

    from skilift import make_skiadmin, development_server

    skiadmin_application = make_skiadmin(editedprojname=PROJECT, examples="http://www.webparametrics.co.uk/skiwidgets/")
    application.add_project(skiadmin_application, url='/skiadmin')

    # the skiadmin sub project can now be used to edit your application
    # please note: when being used to edit a project in this way, skilift requires the
    # application to be the root application, and (for skipole versions >= 5.5.2) to have
    # proj_ident to be set to the project name ( default set to None automatically does this )

    # serve the application with the development server from skilift

    host = "127.0.0.1"
    port = 8000
    print(f"Serving {PROJECT} on port {port}. Call http://localhost:{port}/skiadmin to edit.")
    development_server(host, port, application)
 


