import subprocess
from threading import Thread
from threading import Lock
from threading import Thread
from threading import active_count
from time import sleep, time
import signal
import sys
from flask import Flask, request
import datetime
import os
import shutil


app = Flask(__name__)

DEBUG = False

sleep_time = 1
create_new = False

count = 0
lock = Lock()
latency_lock = Lock()
latencies_time = {}

def get_and_increment():
    global count
    with lock:
        count +=1
        return count - 1

def gnbsim_thread():
    count = get_and_increment()
    if DEBUG:
        print(f"run {count} started")
    subprocess.call(["./run.sh", f"{count}"])
    latency_file = open(f"./logs/{count}/latencies.txt")
    latencies_string = latency_file.read()
    latencies = [int(i.strip()) for i in latencies_string.split("\n") if not i == ""]
    with latency_lock:
        curr_time = time()
        if not curr_time in latencies_time:
            latencies_time[curr_time] = []
        latencies_time[curr_time] += latencies 
    shutil.rmtree(f"./logs/{count}")
    

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
    print(f"rps is now {rps}")
    if rps <= 0:
        create_new = False
        return 'Disabling new'

    sleep_time = 10 / rps
    create_new = True
    return "Adjusted"

@app.route("/latency")
def get_latency():
    with latency_lock:
        global latencies_time
        curr_time = time()

        running_latencies = []

        times = latencies_time.keys()
        to_delete = []
        for get_time in times:
            if get_time >= curr_time - 15:
                running_latencies += latencies_time[get_time]
            else:
                to_delete.append(get_time)
        
        for get_time in to_delete:
            del latencies_time[get_time]

        if len(running_latencies) == 0:
            return {"latency": 0, "size": 0, "max": 0}

        return {"latency": sum(running_latencies) / len(running_latencies), "size": len(running_latencies), "max": max(running_latencies)}

if __name__ == "__main__":
    for folder in os.listdir("./logs/"):
        shutil.rmtree(f"./logs/{folder}")
    Thread(target = creator).start()
    app.run(port=3001, host='0.0.0.0')
