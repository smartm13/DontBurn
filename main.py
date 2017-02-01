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
    return """
	<html>
	<title>SunPosition</title>
	<body>
	<h1>SunPosition</h1>
	<!--form action=""-->
	<label for="str1">source</label>
	<input id="str1" name="par1" type="text"/>
	<hr>
	<label for="str2">destination</label>
	<input id="str2" name="par2" type="text" onkeydown="if (event.keyCode == 13) document.getElementById('clickme').click()"/>
	<hr>
	<button id="clickme">Calculate</button>
	<a href="/help">help</a>
	<a href="https://docs.google.com/forms/d/1E3Ey4U1_ev1cnD5p29y8r5zLyITA9G2_F2vxUWVMbU4/viewform">feedback</a>


	<script>
	document.getElementById("clickme").addEventListener("click", clicked);
	function clicked()
	{
    document.getElementById("output").innerHTML = "Please Wait.";
	var a=document.getElementById("str1").value;
	var b=document.getElementById("str2").value;
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
    if (xhttp.readyState == 4 && xhttp.status == 200) {
      document.getElementById("output").innerHTML = xhttp.responseText;
    }
    if (xhttp.readyState == 4 && xhttp.status != 200) {
          document.getElementById("output").innerHTML = "Failed";

    }
  };
  xhttp.open("GET", "lai_lidho?par1=".concat(a).concat("&par2=").concat(b), true);
  xhttp.send();
}

	</script>

	<hr><hr>
	<p id="output">	</p>
	</body>
	</html>
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
