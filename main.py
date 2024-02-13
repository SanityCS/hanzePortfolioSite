from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')


@app.route('/notes')
def notes():
    return render_template('notes.html')


@app.route('/network_notes')
def network_notes():
    return render_template('network_notes.html')

@app.route('/infastructure_notes')
def infrastructure_notes():
    return render_template('infrastructure_notes.html')

app.run(debug=True)