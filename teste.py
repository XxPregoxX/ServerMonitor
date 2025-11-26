from flask import Flask, jsonify, render_template
import os
import psutil
import random
app = Flask(__name__)

contador = 0

@app.route("/")
def index():
    lines = range(100)
    nucleos = range(os.cpu_count())
    return render_template("index.html", lines=lines, nucleos=nucleos)

@app.route("/cpu")
def get_spams():
    global contador
    nucleos = psutil.cpu_percent(interval=1, percpu=True)
    nucleos_int = [int(u) for u in nucleos]
    return jsonify(nucleos_int)

@app.route("/mem")
def get_meminfo():
    # info = {}
    # with open("/proc/meminfo") as f:
    #     for line in f:
    #         key, value = line.split(":")
    #         info[key] = value.strip()
    # total = int(info["MemTotal"].split()[0])
    # free = int(info["MemFree"].split()[0])
    # buffers = int(info["Buffers"].split()[0])
    # cached = int(info["Cached"].split()[0])
    # sreclaim = int(info["SReclaimable"].split()[0])
    # cached_total = cached + sreclaim
    # used = total - free - buffers - cached_total

    # rando generator for testing
    used = random.randrange(1, 5368709120)
    cached_total = random.randrange(1, 3221225472)
    buffers = random.randrange(1, 2147483648)
    total = 17179869184
    return jsonify([used, cached_total, buffers, total])

if __name__ == "__main__":
    app.run(debug=True)