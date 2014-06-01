import sys
import bottle
from bottle import HTTPResponse
import logging
from sqlalchemy import create_engine

######################################################################
# Configuration
conf = sys.argv[1]
app = application = bottle.Bottle()
app.config.load_config('../../etc/{}.ini'.format(conf))
logging.basicConfig(filename=app.config['code-review.logfile'],
                    level=logging.DEBUG)
engine = create_engine(app.config['db.con-string'], echo=True)

######################################################################
# GET Routes
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

######################################################################
# POST Routes
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

######################################################################
if __name__ == '__main__':
    bottle.run(app, port=8080)
