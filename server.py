from flask import Flask, redirect, url_for, render_template, request
from flask_socketio import SocketIO
from threading import Lock
from datetime import datetime 
from sheets.saintquote import pick_quote
from alarm.alarm import play_alarm, init_alarm, stop_alarm


"""
Background Thread
"""
thread = None
thread_lock = Lock()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gilead'
socketio = SocketIO(app, cors_allowed_origins='*')

#app.register_blueprint(second, url_prefix="")

"""
In Background Thread loop whatever code you want to run continously. Then at the end have it emit the data you want
to send to the javascript.
"""
def background_thread():
    alarm_active = False
    quote_picked = pick_quote()
    alarm = init_alarm('Good_MorningV2.mp3')
    global stop
    stop = False
    while True:
        now = datetime.now()
        if now.second % 20 == 0:
            quote_picked = pick_quote()
            #print(quote_picked)


        play_alarm(alarm, 7, 52, 0)
        stop_alarm(alarm, stop)

        if now.second == 30:
            stop = True
        else: 
            stop = False

        print(stop)
        socketio.emit('updateData', {'quote': quote_picked})
        socketio.sleep(1)
    
    


"""
===============================================================================================================================
Runs the site and renders the screen, all code goes above this portion
================================================================================================================================
"""
@app.route('/')

def index():
    return render_template("index.html")


"""
Decorator for connect
"""
@socketio.on('connect')
def connect():
    global thread
    print('Client connected')

    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)

"""
Decorator for disconnect
"""
@socketio.on('disconnect')
def disconnect():
    print('Client disconnected',  request.sid)

if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0', port=8000)