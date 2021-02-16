from flask import Flask, request, jsonify, abort
from steam import game_servers as gs
from flask_cors import CORS, cross_origin
import os
import psutil
import subprocess

app = Flask(__name__)
cors = CORS(app)

# FUCK CORS 142.93.124.24


@app.route("/")
def init():
    if request.remote_addr != '142.93.124.24':
        abort(403)  # Forbidden
    return jsonify({"status": "true"})


@app.route("/dashboard")
def dashboard():
    if request.remote_addr != '142.93.124.24':
        abort(403)  # Forbidden
    players = 0
    try:
        for server_addr in gs.query_master(r'\app_id\107410\gameaddr\51.89.155.186'):
            players += gs.a2s_info(server_addr)["players"]
    except:
        print("No servers online")
    return jsonify(cpu=psutil.cpu_percent(), players=players, ram=psutil.virtual_memory().percent)


@app.route("/server/<int:port>")
def serverInfo(port):
    if request.remote_addr != '142.93.124.24':
        abort(403)  # Forbidden
    x = ""
    try:
        x = subprocess.check_output(['screen', '-list'])
    except:
        print("Wrong")
    if "arma_"+str(port) in str(x):
        for server_addr in gs.query_master(r'\app_id\107410\gameaddr\51.89.155.186:'+str(port)):
            serverinfo = gs.a2s_info(server_addr)
            return jsonify(running=2, maxplayers=serverinfo["max_players"], players=serverinfo["players"], version=serverinfo["version"], map=serverinfo["map"], mission=serverinfo["game"], hostname=serverinfo["name"])
        return jsonify(running=1)
    return jsonify(running=0)


@app.route("/start")
def start():
    if request.remote_addr != '142.93.124.24':
        abort(403)  # Forbidden
    foldername = request.args['foldername']
    startfile = request.args['startfile']
    port = request.args['port']
    x = ""
    try:
        x = subprocess.check_output(['screen', '-list'])
    except:
        print("Wrong")
    if "arma_"+port not in str(x):
        os.chdir("/home/steam/"+foldername+"/")
        os.system("screen -AdmSL arma_"+startfile +
                  " ./"+port+"_start.sh")
    return "false"


@app.route("/stop")
def stop():
    port = request.args['port']
    if request.remote_addr != '142.93.124.24':
        abort(403)  # Forbidden
    x = ""
    try:
        x = subprocess.check_output(['screen', '-list'])
    except:
        print("Wrong")
    if "arma_"+port in str(x):
        os.system("screen -X -S arma_"+port +
                  " quit")
    return "false"
