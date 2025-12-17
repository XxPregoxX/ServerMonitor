async function cpuMonitoring() {
    const res = await fetch('/cpu');
    const novaLista = await res.json();

    const res2 = await fetch('/cpu_info');
    const cpu_info = await res2.json();

    document.getElementById("tota_usage").textContent =
        "Uso total: " + cpu_info[0] + "%";
    document.getElementById("load_avrg").textContent =
        "Load Average: " + cpu_info[3];
    document.getElementById("temp").textContent =
        "Temperatura: " + cpu_info[1] + "Cº";
    document.getElementById("frequency").textContent =
        "Frequência: " + cpu_info[2].toFixed(2) + "MHz";

    if (novaLista.length > 6){
        document.querySelector('.cpu-cores-grid').style.gridTemplateRows = 'repeat(6, 100px)';
    } else {
        document.querySelector('.cpu-cores-grid').style.gridTemplateRows = `repeat(${novaLista.length}, 100px)`;
    }

    const delay = 15;
    const tarefas = [];

    let cpu_counter = 0;
    for (const novoValor of novaLista) {
        tarefas.push(animarCPU(cpu_counter, novoValor, delay));
        cpu_counter++;
    }

    await Promise.all(tarefas); 
}

async function animarCPU(index, novoValor, delay) {
    const box = document.getElementById('cpu-bar' + index);
    const valorAtual = box.childElementCount;
    const color = corProporcional(novoValor);

    document.getElementById('cpu-counter' + index).textContent =
        novoValor + "% | cpu" + index;

    const current_columns = document.querySelectorAll('#barra' + index);
    current_columns.forEach(item => item.style.backgroundColor = color);

    if (novoValor < valorAtual) {
        let diff = valorAtual - novoValor;
        for (let i = 0; i < diff; i++) {
            box.removeChild(box.lastChild);
            await sleep(delay);
        }
    } else if (novoValor > valorAtual) {
        let diff = novoValor - valorAtual;
        for (let i = 0; i < diff; i++) {
            const span = document.createElement('span');
            span.id = 'barra' + index;
            span.style.backgroundColor = color;
            box.appendChild(span);
            await sleep(delay);
        }
    }
}

function corProporcional(qtd) {
  if (qtd < 1) qtd = 1;
  if (qtd > 100) qtd = 100;

  const t = qtd / 100; // 0 a 1

  const r = Math.round(0 + (255 - 0) * t);
  const g = Math.round(255 - (255 * t));
  const b = 0;
  return `rgb(${r}, ${g}, ${b})`;
}

async function memMonitoring() {
    const res = await fetch('/mem');
    const valores = await res.json();
    
    delay = 15;
    var used_bytes = valores[0];
    var cache_bytes = valores[1];
    var buffers_bytes = valores[2];
    var total_bytes = valores[3];
    var total_used = used_bytes + cache_bytes + buffers_bytes;
    var free_bytes = total_bytes - total_used

    let usedPercent = (used_bytes / total_bytes) * 100;
    let freePercent = (free_bytes / total_bytes) * 100;
    let cachePercent = (cache_bytes / total_bytes) * 100;
    let buffersPercent = (buffers_bytes / total_bytes) * 100;
    let total_used_percent = (total_used / total_bytes) * 100
    document.getElementById('RAM').textContent =
        total_used_percent.toFixed(1) + "% | " + kbToGb(total_bytes);
    
    document.getElementById("usage-percent").textContent = usedPercent.toFixed(1) + "%";
    document.getElementById("cache-percent").textContent = cachePercent.toFixed(1) + "%";
    document.getElementById("buffer-percent").textContent = buffersPercent.toFixed(1) + "%";
    document.getElementById("free-percent").textContent = freePercent.toFixed(1) + "%"
    document.getElementById("usage-bytes").textContent = kbToGb(used_bytes);
    document.getElementById("cache-bytes").textContent = kbToGb(cache_bytes);
    document.getElementById("buffer-bytes").textContent = kbToGb(buffers_bytes);
    document.getElementById("free-bytes").textContent = kbToGb(free_bytes)
    for (let i = 0; i < 100; i++) {
        if (i <= usedPercent){
            document.getElementById('mem-line' + i).style.backgroundColor = '#7d33ff';
            await sleep(delay);  
            } else if (i <= usedPercent + cachePercent){
            document.getElementById('mem-line' + i).style.backgroundColor = '#ff751f';
            await sleep(delay); 
            } else if (i <= usedPercent + cachePercent + buffersPercent){
            document.getElementById('mem-line' + i).style.backgroundColor = '#ff66c4';
            await sleep(delay);  
            } else {
            document.getElementById('mem-line' + i).style.backgroundColor = '#9e9e9e';
            await sleep(delay);  
            };
    } 
}

async function swapMonitoring() {
    const res = await fetch('/swap');
    const valores = await res.json();
    delay = 15;
    var used_bytes = valores[0];
    var free_bytes = valores[1];
    var total_bytes = valores[2];

    let usedPercent = (used_bytes / total_bytes) * 100;
    let freePercent = (free_bytes / total_bytes) * 100;
    let total_used_percent = (used_bytes / total_bytes) * 100

    document.getElementById('swap').textContent =
        usedPercent.toFixed(1) + "% | " + kbToGb(total_bytes);
    
    
    for (let i = 0; i < 100; i++) {
        if (i < usedPercent){
            document.getElementById('swap-line' + i).style.backgroundColor = '#cc5a26';
            await sleep(delay);  
            } else {
            document.getElementById('swap-line' + i).style.backgroundColor = '#9e9e9e';
            await sleep(delay);  
            }
        }
}

async function DiskCheck() {
    const res = await fetch('/disks');
    const valores = await res.json();

Object.entries(valores).forEach(([device, disk], index) => {
    const em_uso = bytesToGB(disk['used']);
    const em_uso_percent = disk['used_percent'];
    const livre_disco = bytesToGB(disk['free']);
    const temperatura = disk['temperature'];
    document.getElementById(`disk${index}-em-uso`).textContent =
        "Em uso: " + em_uso + "G";

    document.getElementById(`disk${index}-em-uso%`).textContent =
        "Em uso %: " + em_uso_percent + "%";

    document.getElementById(`disk${index}-livre-disco`).textContent =
        "Livre: " + livre_disco + "G";

    document.getElementById(`disk${index}-temperatura`).textContent =
        "Temperatura: " + temperatura + "°C";
});

};

async function DiskInitInfo(){
    const res = await fetch('/disks');
    const valores = await res.json();

    Object.entries(valores).forEach(([device, disk], index) => {
    const nome_disco = disk['name'];
    const capacidade_total = disk['size'];

    document.getElementById(`disk${index}-title`).textContent =
        nome_disco;

    document.getElementById(`disk${index}-capacidade-total`).textContent =
        "Tamanho: " + capacidade_total;
});
};

async function PingCheck() {
    const res = await fetch('/ping');
    const valores = await res.json();
    const status = valores[0];
    const latencia = valores[1];

    if (status === false) {
        document.getElementById('ping-bar').style.backgroundColor = 'red';
        document.getElementById('latency').textContent = "- ms";
    } else {
        document.getElementById('ping-bar').style.backgroundColor = 'green';
        document.getElementById('latency').textContent = latencia + " ms";
    }
}

async function UpdateUptime() {
    const res = await fetch('/uptime');
    const valores = await res.json();
    const uptime = valores;

    document.getElementById('uptime').textContent =
        "Uptime: " + uptime;
}

function bytesToGB(bytes) {
    if (!bytes || isNaN(bytes)) return 0;
    return (bytes / (1024 ** 3)).toFixed(2);
}

function kbToGb(kb) {
    return (kb / (1024 * 1024)).toFixed(1) + "GB";
}

function sleep(ms) {
    return new Promise(r => setTimeout(r, ms));
}

window.onload = function() {
    cpuMonitoring();
    memMonitoring();
    swapMonitoring();
    DiskCheck();
    DiskInitInfo()
};

// Atualiza as infromações de CPU a cada 2 segundos
setInterval(cpuMonitoring, 2000);
cpuMonitoring();

// Verifica a RAM a cada 5 segundos
setInterval(memMonitoring, 5000);
memMonitoring();

// Verifica a swap a cada 10 segundos
setInterval(swapMonitoring, 10000);
swapMonitoring();

// Verifica o disco a cada 30 segundos
setInterval(DiskCheck, 30000);
DiskCheck();

// Pinga a cada 1 segundo
setInterval(PingCheck, 1000);
PingCheck();

// Atualiza o uptime a cada 1 segundo
setInterval(UpdateUptime, 1000);
UpdateUptime();

