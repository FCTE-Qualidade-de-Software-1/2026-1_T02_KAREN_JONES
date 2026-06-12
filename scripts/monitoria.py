import psutil
import time
import csv
from datetime import datetime

SAMPLE_INTERVAL = 0.5  # 500ms
OUTPUT_FILE = "monitor_recursos.csv"
CPU_COUNT = psutil.cpu_count() or 1


fieldnames = [
    "timestamp",
    "elapsed_s",
    "cpu_percent",
    "ram_used_mb",
    "ram_percent",
    "peak_ram_used_mb",
    "ollama_cpu_percent",
    "ollama_cpu_percent_norm",
    "ollama_ram_used_mb",
    "peak_ollama_ram_used_mb",
]


def get_ollama_processes():
    """Retorna os processos do Ollama (server + runner do modelo)."""
    procs = []
    for p in psutil.process_iter(["pid", "name"]):
        try:
            name = (p.info["name"] or "").lower()
            if "ollama" in name:
                procs.append(psutil.Process(p.info["pid"]))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return procs


print(f"Monitorando recursos a cada {SAMPLE_INTERVAL*1000:.0f}ms... (Ctrl+C para parar)")
print(f"Salvando em {OUTPUT_FILE}")

start = time.perf_counter()
peak_ram_used_mb = 0.0
peak_ollama_ram_used_mb = 0.0

# primeira chamada do cpu_percent é "lixo", descarta
psutil.cpu_percent(interval=None)

# inicializa lista de processos do ollama e "prime" o cpu_percent de cada um
ollama_procs = {}
for p in get_ollama_processes():
    try:
        p.cpu_percent(interval=None)
        ollama_procs[p.pid] = p
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        continue

with open(OUTPUT_FILE, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    try:
        while True:
            # atualiza lista de processos do ollama (podem subir/morrer durante o teste)
            current_procs = get_ollama_processes()
            for p in current_procs:
                if p.pid not in ollama_procs:
                    try:
                        p.cpu_percent(interval=None)  # prime
                        ollama_procs[p.pid] = p
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue

            ollama_cpu_percent = 0.0
            ollama_ram_mb = 0.0
            dead_pids = []
            for pid, p in ollama_procs.items():
                try:
                    ollama_cpu_percent += p.cpu_percent(interval=None)
                    ollama_ram_mb += p.memory_info().rss / (1024 * 1024)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    dead_pids.append(pid)

            for pid in dead_pids:
                ollama_procs.pop(pid, None)

            # psutil.Process().cpu_percent() é relativo a 1 núcleo (pode passar de 100%
            # se o processo usa várias threads em paralelo). Normaliza para 0-100% do
            # sistema total, igual ao psutil.cpu_percent() global.
            ollama_cpu_percent_norm = ollama_cpu_percent / CPU_COUNT

            current_ram_mb = round(psutil.virtual_memory().used / (1024 * 1024), 2)
            peak_ram_used_mb = max(peak_ram_used_mb, current_ram_mb)
            peak_ollama_ram_used_mb = max(peak_ollama_ram_used_mb, ollama_ram_mb)

            row = {
                "timestamp": datetime.now().isoformat(timespec="milliseconds"),
                "elapsed_s": round(time.perf_counter() - start, 2),
                "cpu_percent": psutil.cpu_percent(interval=None),
                "ram_used_mb": current_ram_mb,
                "ram_percent": psutil.virtual_memory().percent,
                "peak_ram_used_mb": round(peak_ram_used_mb, 2),
                "ollama_cpu_percent": round(ollama_cpu_percent, 2),
                "ollama_cpu_percent_norm": round(ollama_cpu_percent_norm, 2),
                "ollama_ram_used_mb": round(ollama_ram_mb, 2),
                "peak_ollama_ram_used_mb": round(peak_ollama_ram_used_mb, 2),
            }

            writer.writerow(row)
            f.flush()  # garante que grava em disco mesmo se interromper com Ctrl+C
            print(
                f"{row['timestamp']} | CPU total: {row['cpu_percent']}% | "
                f"RAM total: {row['ram_used_mb']} MB | "
                f"Ollama CPU: {row['ollama_cpu_percent']}% (norm: {row['ollama_cpu_percent_norm']}%) | "
                f"Ollama RAM: {row['ollama_ram_used_mb']} MB (pico: {row['peak_ollama_ram_used_mb']} MB)"
            )

            time.sleep(SAMPLE_INTERVAL)
    except KeyboardInterrupt:
        print("\nMonitoramento finalizado.")