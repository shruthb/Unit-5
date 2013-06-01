import json
import bottle
from bottle import route, run, request, abort, static_file
import keyclassifier


@route('/restapi/', method='POST')
def getthis():
    keys = []
    for each in request.forms :
        keys.append(request.forms[each].lower())
    #print type(keys)
    dom,urls = keyclassifier.querydomain(keys)
    res = {'domain':dom, 'urls':urls}
    return res

@route('/index.html')
def start():
    return static_file("interface.html", root=".")

run(host='localhost', port=8080)
