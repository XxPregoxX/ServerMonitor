import json
import subprocess
from flask import Flask, jsonify, render_template
import psutil
import os
import glob
app = Flask(__name__)

@app.route("/")
def index():
    cpu_info = get_lscpu()
    cpu_model = cpu_info['Model name']
    cpu_real_cores = cpu_info['Core(s) per socket']
    cpu_cores = cpu_info['CPU(s)']
    cpu_max_ghz = int(float(cpu_info['CPU max MHz'])) / 1000
    lines = range(100)
    nucleos = range(os.cpu_count())
    return render_template("index.html",
                            lines=lines,
                            nucleos=nucleos,
                            cpu_model=cpu_model,
                            cpu_real_cores=cpu_real_cores,
                            cpu_cores=cpu_cores,
                            cpu_max_ghz=cpu_max_ghz
                           )

@app.route("/cpu")
def get_spams():
    global contador
    nucleos = psutil.cpu_percent(interval=1, percpu=True)
    nucleos_int = [int(u) for u in nucleos]
    return jsonify(nucleos_int)

@app.route("/cpu_info")
def get_cpu_info():
    clock = get_cpu_clock()
    temp = get_cpu_temp()
    usage_total = psutil.cpu_percent(interval=1)
    load = get_load_avg()

    return jsonify(usage_total, temp, clock, load)

@app.route("/mem")
def get_meminfo():
    info = {}
    with open("/proc/meminfo") as f:
        for line in f:
            key, value = line.split(":")
            info[key] = value.strip()
    total = int(info["MemTotal"].split()[0])
    free = int(info["MemFree"].split()[0])
    buffers = int(info["Buffers"].split()[0])
    cached = int(info["Cached"].split()[0])
    sreclaim = int(info["SReclaimable"].split()[0])
    cached_total = cached + sreclaim
    used = total - free - buffers - cached_total
    return jsonify([used, cached_total, buffers, total])

@app.route("/swap")
def get_swap():
    swap_total = 0
    swap_free = 0

    with open("/proc/meminfo") as f:
        for line in f:
            if line.startswith("SwapTotal:"):
                swap_total = int(line.split()[1])  # em KB
            elif line.startswith("SwapFree:"):
                swap_free = int(line.split()[1])  # em KB

    swap_used = swap_total - swap_free
    
    return jsonify([swap_used, swap_free, swap_total])

def get_lscpu():
    res = subprocess.run(
        ["bash", "-c", "LC_ALL=C lscpu --json"],
        capture_output=True,
        text=True
    )
    data = json.loads(res.stdout)
    return {item["field"].strip(":"): item["data"] for item in data["lscpu"]}

def get_cpu_temp():
    temps = []
    for path in glob.glob("/sys/class/hwmon/hwmon*"):
        try:
            with open(f"{path}/name") as f:
                name = f.read().strip().lower()
        except:
            continue

        if any(x in name for x in ["k10temp", "coretemp", "zenpower"]):
            temp_files = glob.glob(f"{path}/temp*_input")
            for tf in temp_files:
                with open(tf) as f:
                    temps.append(int(f.read().strip()) / 1000)

    # pegar a primeira, geralmente temp1_input
    cpu_temp = temps[0] if temps else None
    return cpu_temp

def get_cpu_clock():
    clock_atual = None
    with open("/proc/cpuinfo") as f:
        for line in f:
            if "cpu MHz" in line:
                clock_atual = float(line.split(":")[1])
                break
    return clock_atual

def get_load_avg():
    load1, load5, load15 = os.getloadavg()
    load = f"{load1:.2f}" + f" {load5:.2f}" + f" {load15:.2f}"
    return load

if __name__ == "__main__":
    app.run(debug=True)