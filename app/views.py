from app import app, r_server
from flask import render_template
from flask import flash, redirect
from .forms import LoginForm
from flask import request, abort
from flask import jsonify, json
from utils import CustomSorter
import utils
import zlib

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
    if not request.json:
        abort(400)

    request_data = None
    try:
        request_data = request.json
        username = request_data["username"]
    except:
        try:
            request_data = json.loads(request.json)
            username = request_data["username"]
        except:
            abort(501)

    metric_id = r_server.incr("metric.id")
    r_server.set("metric.id."+str(metric_id), json.dumps(request_data))
    r_server.rpush("username." + username + ".metric_ids", metric_id)
    return jsonify({'params': request_data}), 201

def sort_filelist_by_ext_relevance(filelist):
    res = []
    exts = [".java", ".cpp", ".gradle"]
    for ext in exts:
        res += filter(lambda x: x.strip().endswith(ext), filelist)
    res += utils.listdiff(filelist, res)
    return res

def show_metric_id(metric_id):
    metric_data = json.loads(r_server.get("metric.id."+str(metric_id)))
    metric_data = transform_metric_data(metric_data, -1)
    metric_data["diff_sorted"] = sort_filelist_by_ext_relevance(metric_data["diff"])
    return render_template('metrics_details.html', metric = metric_data)

def transform_metric_data(metric_data, task_cnt=3):
    if metric_data["scores"]:
        metric_data["top_tasks"] = CustomSorter.sort_scores(metric_data["scores"])[:task_cnt]
    if "timestamp" in metric_data:
        metric_data["timestamp_formatted"] = utils.format_timestamp(metric_data["timestamp"])
        if "previous_timestamp" in metric_data:
            metric_data["time_diff"] = utils.timediff(metric_data["timestamp"], metric_data["previous_timestamp"])
    return metric_data

@app.route('/metrics', methods=['GET'])
def show_metrics():
    # get username from query string
    # username = request.args.get('username')
    if (request.args.get("mid")):
        return show_metric_id(request.args.get("mid"))

    metrics_ids = []
    if (request.args.get('username')):
        username = request.args.get('username')
        fieldname = "username." + username + ".metric_ids"
        metrics_ids = r_server.lrange(fieldname, 0, -1)
    else:
        max_metric_id = int(r_server.get("metric.id"))
        metrics_ids = range(1, max_metric_id)

    metrics = []
    for id in metrics_ids:
        metric_data = json.loads(r_server.get("metric.id."+str(id)))
        metric_data = transform_metric_data(metric_data)
        metric_data["mid"] = id
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