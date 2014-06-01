import bottle
from bottle import HTTPResponse

app = application = bottle.Bottle()

@app.get('/do/codeByID')
@app.get('/do/code/<id>')
def get_code_by_id(id = None):
    return HTTPResponse(status = 501) # not implemented

@app.get('/do/commentsOnLine')
@app.get('/do/code/<id>/comments/<line>')
def get_comments(id = None, line = None):
    return HTTPResponse(status = 501) # not implemented

@app.get('/do/commentCount')
@app.get('/do/code/<id>/comments/count')
def count_comments(id = None):
    return HTTPResponse(status = 501) # not implemented

@app.get('/do/anticsrf')
def get_anticsrf():
    return HTTPResponse(status = 501) # not implemented

@app.post('/do/newcode')
def add_code():
    return HTTPResponse(status = 501) # not implemented

@app.post('/do/newcomment')
def add_code():
    return HTTPResponse(status = 501) # not implemented

@app.post('/do/login')
def add_code():
    return HTTPResponse(status = 501) # not implemented

@app.post('/do/logout')
def add_code():
    return HTTPResponse(status = 501) # not implemented

if __name__ == '__main__':
    bottle.run(app, port=8080)
