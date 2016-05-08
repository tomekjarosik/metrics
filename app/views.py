from app import app
from flask import render_template
from flask import flash, redirect
from .forms import LoginForm
from flask import request, abort
from flask import jsonify, json

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Tomek'}  # fake user
    return render_template('index.html',
                           title='Home',
                           user=user)

@app.route('/charts')
def charts_demo():
    # fake chart
    #user = {'nickname': 'Tomek'}  # fake user
    return render_template('charts.html')

@app.route('/buildmetrics/api/v1.0/add', methods=['POST'])
def add_build_metrics():
    print("Received request: ", request.json)
    if not request.json or not 'scores' in request.json:
        abort(400)
    a_dict = request.json
    return jsonify({'params': a_dict}), 201

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
        return redirect('/index')
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])