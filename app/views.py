from app import app, r_server
from flask import render_template
from flask import flash, redirect
from .forms import LoginForm
from flask import request, abort
from flask import jsonify, json

from redis import Redis

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
    request_data = request.json
    username = request_data["username"]
    metric_id = r_server.incr("metric.id")
    r_server.set("metric.id."+str(metric_id), json.dumps(request_data))
    r_server.rpush(username, metric_id)
    return jsonify({'params': request_data}), 201

@app.route('/metrics', methods=['GET'])
def show_builds():
    # get username from query string
    # username = request.args.get('username')

    max_metric_id = int(r_server.get("metric.id"))
    metrics = []
    for id in range(1, max_metric_id):
        metric_data = json.loads(r_server.get("metric.id."+str(id)))
        metrics.append(metric_data)

    return render_template('metrics_list.html', metrics = metrics)

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