import logging
from logging.handlers import RotatingFileHandler
import maps
from flask import Flask,request, render_template
app = Flask(__name__)
app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

#a=['wsfd','fdsf','fdffafaaa']
@app.route('/lai_lidho')
def res():
    import maps
    a = maps.find_sun_pos(request.args['par1'],request.args['par2'])
    try:
    	return render_template('result.html', res_list = a)

    except:return "Locha"

@app.route('/')
@app.route('/sun')
def sunhello():
    """Return a friendly HTTP greeting."""
    return render_template('index.html')
    return """
	"""

@app.route('/help')
def help():
	return render_template('help.html')


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
    
    
if __name__ == '__main__':
	formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
        handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
        handler.setLevel(logging.DEBUG)
        app.logger.addHandler(handler)
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.DEBUG)
        handler.setFormatter(formatter)
        log.addHandler(handler)
        app.run(host='0.0.0.0', port=5000, debug=True)
