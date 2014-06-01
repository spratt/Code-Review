import sys
import bottle
from bottle import HTTPResponse, request
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.code import Code
import json

######################################################################
# Configuration
config_file = '../../etc/{}.ini'.format(sys.argv[1])
app = application = bottle.Bottle()
app.config.load_config(config_file)
logging.basicConfig(format='%(asctime)s %(message)s',
                    filename=app.config['code-review.logfile'],
                    level=logging.DEBUG)
engine = create_engine(app.config['db.con-string'], echo=True)
Session = sessionmaker(bind = engine)
logging.info('Loaded configuration from {}'.format(config_file))
logging.info('Logging to {}'.format(app.config['code-review.logfile']))
logging.info('Connecting to db {}'.format(app.config['db.con-string']))

######################################################################
# Create tables if not already present
from models.code import Base as CodeBase
CodeBase.metadata.create_all(engine)

######################################################################
# Request logging
@app.hook('before_request')
def log_request():
    logging.info('{} {}'.format(request.method, request.path))
    return True

######################################################################
# GET Routes
@app.get('/do/codeByID')
@app.get('/do/code/<id>')
def get_code_by_id(id = None):
    if id == None:
        id = request.query.get('id')
    if id == None:
        abort(400)
    try:
        session = Session()
        found = session.query(Code).filter(Code.id == int(id)).first()
        if found == None:
            abort(404)
    except:
        exctype, value = sys.exc_info()[:2]
        logging.info('Error adding new code')
        logging.info('exception type:  {}'.format(exctype))
        logging.info('exception value: {}'.format(value))
        abort(500, 'Error adding new code')
    return json.dumps({
        'id' : found.id,
        'text' : found.text,
        'lang' : found.lang
    })

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
    text = request.forms.get('text')
    lang = request.forms.get('lang')
    if text == None:
        abort(400, json.dumps({
            'error' : 'Attribute text not provided'
        }))
    if lang == None:
        abort(400, json.dumps({
            'error' : 'Attribute lang not provided'
        }))
    new_code = Code(text = text, lang = lang)
    try:
        session = Session()
        session.add(new_code)
        session.commit()
    except:
        exctype, value = sys.exc_info()[:2]
        logging.info('Error adding new code')
        logging.info('exception type:  {}'.format(exctype))
        logging.info('exception value: {}'.format(value))
        abort(500, 'Error adding new code')
    return json.dumps({'id' : new_code.id})

@app.post('/do/newcomment')
def add_comment():
    return HTTPResponse(status = 501) # not implemented

@app.post('/do/login')
def login():
    return HTTPResponse(status = 501) # not implemented

@app.post('/do/logout')
def logout():
    return HTTPResponse(status = 501) # not implemented

######################################################################
logging.info('Server started')



