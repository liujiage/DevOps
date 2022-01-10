from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit
import logging
from view.DeployView import DeployView as dv
from view.HistoryView import HistoryView as hv
from view.AuthenticationView import AuthenticationView as auth

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, logger=True, engineio_logger=True)


'''
@Function login system
@Author Jiage
@Date 2021-09-03
'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('userid'):
        session.pop('userid')
    return render_template('login.html')

'''
@Function the first page
@Author Jiage
@Date 2021-08-07
'''
@app.route("/")
def index():
    return render_template('index.html', user = session['userid'])

'''
@Function deploy first page
@Author Jiage
@Date 2021-08-07
'''
@app.route("/deploy")
def deploy():
    return render_template('deploy.html', services=dv.loadView())

'''
@Function deploy service selected
@Author Jiage
@Date 2021-08-07
'''
@app.route("/deploy/service/<service>", methods=['GET','POST'])
def deployService(service=None):
    # app.logger.info('===========deploy/service')
    dv.deployService(service)
    return "got it, deploy services info is " + service

'''
@Function display deploys history detail by id
@Author Jiage
@Date 2021-09-10
'''
@app.route("/history/detail/<id>", methods=['GET','POST'])
def historyService(id):
    return hv.loadDetail(id)

'''
@Function trace the log real-time by id
@Author Jiage
@Date 2021-09-13
'''
@app.route("/history/web/<id>", methods=['GET','POST'])
def historyWebService(id):
    return hv.loadDetail(id)

'''
@Function search history deploys records
@Author Jiage
@Date 2021-09-09
'''
@app.route("/history")
def history():
    return render_template('history.html', records=hv.loadView())

'''
@Function watch currently hosts memory usage. 
@Author Jiage
@Date 2021-08-23
'''
@app.route("/memory")
def memory():
    return render_template('memory.html')

'''
@Function received requests from the client 
@Author Jiage
@Date 2021-08-18
@Data
   Json {event:{connect|start_deploy},data: {type of string}}
@Param event 
   connect, the client connect to service at the first time.
   start_deploy, the user submit deploy service. 
@Param data
   connect, string
   start_deploy, string
'''
@socketio.on('request')
def socketRequest(msg):
    dv.socketRequest(app, msg)

@socketio.on('connect')
def socketConnect(msg):
    emit('response', {'event': 'connect', 'data': 'Connected'})

'''
@Function Intercept request, authentication. 
@Author Jiage
@Date 2021-09-03
'''
@app.before_request
def authentication():
    return auth.auth(app)

if __name__ == "__main__":
    socketio.run(app)