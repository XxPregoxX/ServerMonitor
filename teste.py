import json
import re
import socket
import subprocess
from flask import Flask, jsonify, render_template
from pythonping import ping
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
    dis_count = get_disk_count()
    return render_template("index.html",
                            lines=lines,
                            nucleos=nucleos,
                            cpu_model=cpu_model,
                            cpu_real_cores=cpu_real_cores,
                            cpu_cores=cpu_cores,
                            cpu_max_ghz=cpu_max_ghz,
                            dis_count=dis_count
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

@app.route("/ping")
def ping():
    result = subprocess.run(
        ["ping", "-c", "1", '8.8.8.8'],  # manda 1 pacote
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        return jsonify([False, 0])  # host não respondeu

    # Procura o tempo no output (latência)
    match = re.search(r'time=([\d.]+) ms', result.stdout)
    if match:
        return jsonify([True, float(match.group(1))])  # converte pra float

@app.route("/disks")
def get_disks_info():
    discs = get_disks()
    info = {}
    for device, value in discs.items():
        jsoned = smartctl(f"/dev/{device}")
        smart_info = json.loads(jsoned)
        if "nvme" in device:
            temp = smart_info['temperature'] - 273
        else:
            temp = smart_info['temperature']['current']
        usage = value["used"]
        info[device] = {
            'name': device,
            'size': value['size'],
            'temperature': temp,
            'used': usage.used,
            'used_percent': usage.percent,
            'free': usage.free,}
    return jsonify(info)

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

def get_disks():
    output = subprocess.check_output(["lsblk", "-J"])  # -b = bytes
    data = json.loads(output)
    disk_return = {}
    for device in data['blockdevices']:
        name = device['name']
        if device['type'] == 'disk':
            size = device['size']
            if device['children']:
                for part in device['children']:
                    if part.get("mountpoints") and part["mountpoints"][0]:
                        mountpoint = part['mountpoints']
                        used = psutil.disk_usage(mountpoint[0])
                        disk_return[name] = {"size": size, "used": used}
    return disk_return

def smartctl(device):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect("/var/run/servermonitor.sock")
    s.sendall(f"smart {device}".encode())
    output = s.recv(500000).decode()
    s.close()
    return output

def get_disk_count():
    return len(get_disks())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)