import subprocess
from threading import Thread
from threading import Lock
from threading import Thread
from threading import active_count
from time import sleep
import signal
import sys
from flask import Flask, request

app = Flask(__name__)

sleep_time = 1
create_new = False

count = 0
lock = Lock()
def get_and_increment():
    global count
    with lock:
        count +=1
        return count

def gnbsim_thread():
    count = get_and_increment()
    print(f"run {count} started")
    subprocess.call("./run.sh")
    print(f"run {count} finished")

def creator():
    global sleep_time
    global create_new
    while (True):
        if create_new:
            Thread(target = gnbsim_thread).start()
            sleep(sleep_time)

@app.route("/", methods=['POST'])
def set_rate():
    global sleep_time
    global create_new
    rps = int(request.form['rps'])
    if rps <= 0:
        create_new = False
        return 'Disabling new'

    sleep_time = 10 / rps
    create_new = True
    return "Adjusted"

if __name__ == "__main__":
    Thread(target = creator).start()
    app.run(port=3001)
