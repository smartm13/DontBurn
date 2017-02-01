import maps
from flask import Flask,request, render_template
app = Flask(__name__)
app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

#a=['wsfd','fdsf','fdffafaaa']
@app.route('/lai_lidho')
def res():
    a = maps.find_sun_pos(request.args['par1'],request.args['par2'])
    try:
    	return render_template('result.html', res_list = a)

    except:return "Locha"
	
@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return """
	<html>
	<title>Le maro</title>
	<body>
	<h1>greeting</h1>
	<!--form action=""-->
	<input id="str1" name="par1" type="text"/>
	<hr>
	<input id="str2" name="par2" type="text"/>
	<hr>
	<button id="clickme">BC</button>
	<a href="/help">help</a>

	<script>
	document.getElementById("clickme").addEventListener("click", clicked);
	function clicked()
	{
	var a=document.getElementById("str1").value;
	var b=document.getElementById("str2").value;
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
    if (xhttp.readyState == 4 && xhttp.status == 200) {
      document.getElementById("output").innerHTML = xhttp.responseText;
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
	return'hdkfjhkd'

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
    
    
if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5000, debug=True)