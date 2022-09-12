from flask import Flask, jsonify, redirect
from database import Database
from flask_cors import CORS

app = Flask('__app__')
CORS(app)
instance = Database()
URL_RUN, PORT_RUN = [
    'localhost', 
    5555
]

@app.route('/c/<path:URL>')
def consult(URL):
    query = instance.return_hashURL_from_link(URL)
    return jsonify({
        'url': f'{URL_RUN}:{PORT_RUN}/{query}'
    })

@app.route('/<string:URL>')
def goto(URL):
    return redirect(instance.return_link_from_hashURL(URL))
    

app.run(host=URL_RUN, port=PORT_RUN, debug=True)