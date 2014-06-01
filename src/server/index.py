import sys
import bottle
from bottle import HTTPResponse, request
import logging
from sqlalchemy import create_engine, func
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
# Helper functions
def getIntOrDie(request, name):
    try:
        val = int(request.params.get(name))
    except:
        abort(400)
    return val

def getStrOrDie(request, name):
    val = request.params.get(name)
    if val == None:
        abort(400)
    return val

def logThenDie(message, exctype, value):
    logging.info('exception type:  {}'.format(exctype))
    logging.info('exception value: {}'.format(value))
    logging.info(message)
    abort(500, message)
    

######################################################################
# GET Routes
@app.get('/do/codeByID')
@app.get('/do/code/<id>')
def get_code_by_id(id = None):
    id = id or getIntOrDie(request, 'id')
    try:
        session = Session()
        found = session.query(Code).filter(Code.id == id).first()
        if found == None:
            abort(404)
    except:
        logThenDie('Error while getting code by id', *sys.exc_info()[:2])
    return json.dumps({
        'id' : found.id,
        'text' : found.text,
        'lang' : found.lang
    })

@app.get('/do/commentsOnLine')
@app.get('/do/code/<code_id>/comments/<line>')
def get_comments(code_id = None, line = None):
    code_id = code_id or getIntOrDie(request, 'code_id')
    line = line or getIntOrDie(request, 'line')
    try:
        session = Session()
        comments = session.query(Comment).filter(
            Comment.code_id == code_id,
            Comment.line_start == line
        ).all()
        returnarr = [c.getDict() for c in comments]
    except:
        logThenDie('Error getting comments on line', *sys.exc_info()[:2])
    return json.dumps(returnarr)


@app.get('/do/commentCount')
@app.get('/do/code/<code_id>/comments/count')
def count_comments(code_id = None):
    code_id = code_id or getIntOrDie(request, 'code_id')
    try:
        session = Session()
        counts = session.query(
            Comment.line_start, func.count(Comment.id)).filter(
                Comment.code_id == code_id).group_by(Comment.line_start).all()
        returnob = {}
        for line, count in counts:
            returnob[line] = count
    except:
        logThenDie('Error getting comment counts', *sys.exc_info()[:2])
    return json.dumps(returnob)

@app.get('/do/anticsrf')
def get_anticsrf():
    return HTTPResponse(status = 501) # not implemented

######################################################################
# POST Routes
@app.post('/do/newcode')
def add_code():
    text = getStrOrDie(request, 'text')
    lang = getStrOrDie(request, 'lang')
    new_code = Code(text = text, lang = lang)
    try:
        session = Session()
        session.add(new_code)
        session.commit()
    except:
        logThenDie('Error adding new code', *sys.exc_info()[:2])
    return json.dumps({'id' : new_code.id})

@app.post('/do/newcomment')
def add_comment():
    code_id = getStrOrDie(request, 'code_id')
    text = getStrOrDie(request, 'text')
    line_start = getIntOrDie(request, 'line_start')
    line_end = getIntOrDie(request, 'line_end')
    diffs = getStrOrDie(request, 'diffs')
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
        logThenDie('Error adding new comment', *sys.exc_info()[:2])
    return json.dumps({'id' : new_comment.id})

@app.post('/do/login')
def login():
    return HTTPResponse(status = 501) # not implemented

@app.post('/do/logout')
def logout():
    return HTTPResponse(status = 501) # not implemented

######################################################################
logging.info('Server started')
