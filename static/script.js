async function cpuMonitoring() {
    const res = await fetch('/cpu');
    const novaLista = await res.json();

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
            var free_bytes = total_bytes - total_used;

            const usedPercent = (used_bytes / total_bytes) * 100;
            const freePercent = (free_bytes / total_bytes) * 100;
            const cachePercent = (cache_bytes / total_bytes) * 100;
            const buffersPercent = (buffers_bytes / total_bytes) * 100;
            const total_used_percent = (total_used / total_bytes) * 100;

            document.querySelector('.mem-total-title').textContent =
                total_used_percent.toFixed(1) + "% | " + bytesToGB(total_bytes);
            
            document.getElementById("usage-percent").textContent = usedPercent.toFixed(1) + "%";
            document.getElementById("cache-percent").textContent = cachePercent.toFixed(1) + "%";
            document.getElementById("buffer-percent").textContent = buffersPercent.toFixed(1) + "%";
            document.getElementById("free-percent").textContent = freePercent.toFixed(1) + "%";

            document.getElementById("usage-bytes").textContent = bytesToGB(used_bytes);
            document.getElementById("cache-bytes").textContent = bytesToGB(cache_bytes);
            document.getElementById("buffer-bytes").textContent = bytesToGB(buffers_bytes);
            document.getElementById("free-bytes").textContent = bytesToGB(free_bytes);

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

function bytesToGB(bytes) {
    const gb = bytes / (1024 ** 3); // divide por 1024³ pra converter pra GB
    return gb.toFixed(1) + "GB"; // 1 decimal, retorna string
}

function sleep(ms) {
    return new Promise(r => setTimeout(r, ms));
}

window.onload = function() {
    cpuMonitoring();
    memMonitoring();
};

// Atualiza a lista a cada 3 segundos
setInterval(cpuMonitoring, 2000);
cpuMonitoring();

setInterval(memMonitoring, 5000);
memMonitoring();