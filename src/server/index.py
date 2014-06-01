import sys
import bottle
from bottle import HTTPResponse, request
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.code import Code
from models.comment import Comment
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
from models.comment import Base as CommentBase
CommentBase.metadata.create_all(engine)

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
    try:
        id = int(id)
    except:
        abort(400)
    try:
        session = Session()
        found = session.query(Code).filter(Code.id == id).first()
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
    code_id = request.forms.get('code_id')
    text = request.forms.get('text')
    line_start = request.forms.get('line_start')
    line_end = request.forms.get('line_end')
    diffs = request.forms.get('diffs')
    if code_id == None:
        abort(400, json.dumps({
            'error' : 'Attribute code_id not provided'
        }))
    if text == None:
        abort(400, json.dumps({
            'error' : 'Attribute text not provided'
        }))
    if diffs == None:
        abort(400, json.dumps({
            'error' : 'Attribute diffs not provided'
        }))
    try:
        line_start = int(line_start)
    except:
        abort(400, json.dumps({
            'error' : 'Attribute line_start not a valid integer'
        }))
    try:
        line_end = int(line_end)
    except:
        abort(400, json.dumps({
            'error' : 'Attribute line_start not a valid integer'
        }))
    try:
        session = Session()
        found = session.query(Code).filter(Code.id == code_id).first()
        if found == None:
            abort(404)
        new_comment = Comment(
            code_id = code_id,
            text = text,
            line_start = line_start,
            line_end = line_end,
            diffs = diffs
        )
        session.add(new_comment)
        session.commit()
    except:
        exctype, value = sys.exc_info()[:2]
        logging.info('Error adding new comment')
        logging.info('exception type:  {}'.format(exctype))
        logging.info('exception value: {}'.format(value))
        abort(500, 'Error adding new comment')
    return json.dumps({'id' : new_comment.id})

@app.post('/do/login')
def login():
    return HTTPResponse(status = 501) # not implemented

@app.post('/do/logout')
def logout():
    return HTTPResponse(status = 501) # not implemented

######################################################################
logging.info('Server started')
