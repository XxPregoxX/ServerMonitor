import json
import re
import psutil
import subprocess
import os
import socket

# uso total
#print(psutil.cpu_percent(interval=1))

# uso por núcleo
#print(psutil.cpu_percent(interval=1, percpu=True))

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
# 
# 
# cached_total = cached + sreclaim
# used = total - free - buffers - cached_total
# 
# print(used)
# print(cached_total)


# def get_lscpu_clean():
#     res = subprocess.run(
#         ["bash", "-c", "LC_ALL=C lscpu --json"],
#         capture_output=True,
#         text=True
#     )
#     data = json.loads(res.stdout)
#     return {item["field"].strip(":"): item["data"] for item in data["lscpu"]}
# 
# for chave, item in get_lscpu_clean().items():
#     print(f'{chave}: {item}')

# import glob
# 
# temps = []
# for path in glob.glob("/sys/class/hwmon/hwmon*"):
#     try:
#         with open(f"{path}/name") as f:
#             name = f.read().strip().lower()
#     except:
#         continue
# 
#     if any(x in name for x in ["k10temp", "coretemp", "zenpower"]):
#         temp_files = glob.glob(f"{path}/temp*_input")
#         for tf in temp_files:
#             with open(tf) as f:
#                 temps.append(int(f.read().strip()) / 1000)
# 
# # pegar a primeira, geralmente temp1_input
# cpu_temp = temps[0] if temps else None
# 
# print(f"CPU Temperature: {cpu_temp} °C")

# def get_load_avg():
#     load1, load5, load15 = os.getloadavg()
#     load = f"{load1:.2f}" + f" {load5:.2f}" + f" {load15:.2f}"
#     return load
# 
# print(get_load_avg())
# 
# swap_total = 0
# swap_free = 0
# with open("/proc/meminfo") as f:
#     for line in f:
#         if line.startswith("SwapTotal:"):
#             swap_total = int(line.split()[1])  # em KB
#         elif line.startswith("SwapFree:"):
#             swap_free = int(line.split()[1])  # em KB
# swap_used = swap_total - swap_free
# print(swap_total, swap_free, swap_used)



def get_disks():
    output = subprocess.check_output(["lsblk", "-J"])  # -b = bytes
    data = json.loads(output)
    disk_return = {}
    disk_counter = 0
    for device in data['blockdevices']:
        name = device['name']
        if device['type'] == 'disk':
            disk_counter += 1
            size = device['size']
            disk_return.update({f"disk{disk_counter}": [name, size]})
            if device['children']:
                for part in device['children']:
                    if part["mountpoints"][0]:
                        part_name = part['name']
                        part_size = part['size']
                        mountpoint = part['mountpoints']
                        used = psutil.disk_usage(mountpoint[0])
                        disk_return.update({part_name: {"size": part_size, "mountpoint": mountpoint, "used": used}})
    return disk_return

def smartctl(device):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect("/var/run/servermonitor.sock")
    s.sendall(f"smart {device}".encode())
    output = s.recv(500000).decode()
    s.close()
    return output

def get_disks_info():
    discs = get_disks()
    for key, value in discs.items():
        if "disk" in key:
            device = f"/dev/{value[0]}"
            jsoned = smartctl(device)
            smart_info = json.loads(jsoned)
            if "nvme" in value[0]:
                print(smart_info['temperature'])

# def ping(host):
#     result = subprocess.run(
#         ["ping", "-c", "1", host],  # manda 1 pacote
#         capture_output=True,
#         text=True
#     )
#     if result.returncode != 0:
#         return jsonify([False, 0])  # host não respondeu
# 
#     # Procura o tempo no output (latência)
#     match = re.search(r'time=([\d.]+) ms', result.stdout)
#     if match:
#         return jsonify([True, float(match.group(1))])  # converte pra float
# 
# 
# print(ping("8.8.8.8"))
