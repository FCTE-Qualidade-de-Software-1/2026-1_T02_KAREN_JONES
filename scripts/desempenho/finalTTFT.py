import os
import requests
import json
import time
import csv
import statistics
from datetime import datetime  # Pra juntar com os dados de monitor.py

URL = "http://127.0.0.1:11434/api/generate"  # se trocar pra localhost tava aumentando 2000ms no TTFT
N_RUNS = 5
KEEP_ALIVE = "5m"  # já é o padrão mas so pra garantir

TELEMETRIA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "telemetria")
os.makedirs(TELEMETRIA_DIR, exist_ok=True)

results = []
metrics_per_run = []


def ns_to_ms(ns):
    return round(ns / 1_000_000, 2)


def parse_iso(ts):
    return datetime.fromisoformat(ts)


def compute_monitor_metrics(monitor_file, start_ts, end_ts):
    peak_ram = 0.0
    cpu_samples = []
    ram_samples = []
    start_dt = parse_iso(start_ts)
    end_dt = parse_iso(end_ts)

    try:
        with open(monitor_file, "r", newline="") as mf:
            reader = csv.DictReader(mf)
            for row in reader:
                try:
                    row_ts = parse_iso(row["timestamp"])
                except ValueError:
                    continue

                if row_ts < start_dt or row_ts > end_dt:
                    continue

                try:
                    cpu_samples.append(float(row["ollama_cpu_percent_norm"]))
                    current_ram = float(row["ollama_ram_used_mb"])
                    ram_samples.append(current_ram)
                    peak_ram = max(peak_ram, current_ram)
                except (KeyError, ValueError):
                    continue
    except FileNotFoundError:
        return None, None, None

    if not cpu_samples or not ram_samples:
        return None, None, None

    avg_cpu = sum(cpu_samples) / len(cpu_samples)
    avg_ram = sum(ram_samples) / len(ram_samples)
    return round(peak_ram, 2), round(avg_cpu, 2), round(avg_ram, 2)


def summarize(values):
    if not values:
        return None, None, None
    mean = round(statistics.mean(values), 2)
    median = round(statistics.median(values), 2)
    desvio = round(statistics.pstdev(values), 2) if len(values) > 1 else 0.0
    return mean, median, desvio


for i in range(N_RUNS):
    ts_inicio = datetime.now().isoformat(timespec="milliseconds")
    created_at_first = None
    start_time = time.perf_counter()
    ttft = None
    full_response = []
    final_data = None

    with requests.post(
        URL,
        json={
            "model": "qwen2.5:3b",
            "prompt": "Explique como a abordagem GQM pode ser aplicada para definir métricas de eficiência de desempenho de um sistema de software, segundo a norma ISO/IEC 25010. Considere um objetivo voltado para avaliar a eficiência de um modelo de linguagem executado localmente via Ollama, descrevendo: (1) como formular o objetivo no formato GQM (propósito, objeto, foco de qualidade, ponto de vista, contexto); (2) quais perguntas seriam derivadas desse objetivo para investigar comportamento temporal, utilização de recursos e capacidade; (3) quais métricas concretas poderiam responder a essas perguntas, como tempo até o primeiro token (TTFT), tokens por segundo (TPS), pico de uso de memória RAM, percentual médio de uso de CPU. Além disso, relacione essas métricas com as práticas recomendadas pelo PSM (Practical Software and Systems Measurement).",
            "keep_alive": KEEP_ALIVE,
            "stream": True,  # com o true ele vai enviando pacotes de token, com false ele espera tudo e devolve de uma x
        },
        stream=True,
    ) as r:
        for line in r.iter_lines():
            if not line:
                continue

            chunk = json.loads(line)
            if ttft is None:
                ttft = (time.perf_counter() - start_time) * 1000
                created_at_first = chunk.get("created_at")

            if "response" in chunk:
                full_response.append(chunk["response"])

            if chunk.get("done", False):
                final_data = chunk

    ts_fim = datetime.now().isoformat(timespec="milliseconds")
    tps = final_data["eval_count"] / (final_data["eval_duration"] / 1_000_000_000)

    monitor_file = os.path.join(TELEMETRIA_DIR, "monitor_recursos.csv")
    peak_ram_used_mb, avg_cpu_percent, avg_ram_used_mb = compute_monitor_metrics(
        monitor_file, ts_inicio, ts_fim
    )

    rei = None
    if peak_ram_used_mb and avg_cpu_percent:
        peak_ram_used_gb = peak_ram_used_mb / 1024
        rei = round(tps / (peak_ram_used_gb * avg_cpu_percent), 6)

    row = {
        "run": i + 1,
        "ts_inicio": ts_inicio,
        "ts_fim": ts_fim,
        "ts_first_chunk_ollama": created_at_first,
        "ttft_ms": round(ttft, 2),
        "tps": round(tps, 2),
        "peak_ollama_ram_used_mb": peak_ram_used_mb,
        "avg_ollama_ram_used_mb": avg_ram_used_mb,
        "avg_ollama_cpu_percent": avg_cpu_percent,
        "rei": rei,
        "load_duration:": ns_to_ms(final_data["load_duration"]),
        "prompt_eval_count:": final_data["prompt_eval_count"],
        "prompt_eval_duration:": ns_to_ms(final_data["prompt_eval_duration"]),
        "eval_count:": final_data["eval_count"],
        "eval_duration:": ns_to_ms(final_data["eval_duration"]),
        "total_duration:": ns_to_ms(final_data["total_duration"]),
    }

    results.append(row)
    metrics_per_run.append(
        {
            "ttft_ms": row["ttft_ms"],
            "tps": row["tps"],
            "load_duration_ms": row["load_duration:"],
            "peak_ollama_ram_used_mb": peak_ram_used_mb,
            "avg_ollama_ram_used_mb": avg_ram_used_mb,
            "avg_ollama_cpu_percent": avg_cpu_percent,
            "rei": rei,
        }
    )

    print(
        f"Run {i+1}/{N_RUNS} -> TTFT: {row['ttft_ms']} ms | TPS: {row['tps']} | "
        f"Pico RAM Ollama: {row['peak_ollama_ram_used_mb']} MB | "
        f"CPU Ollama: {row['avg_ollama_cpu_percent']}% | REI: {row['rei']}"
    )

# salva os dados de todos os testes (bruto)
with open(os.path.join(TELEMETRIA_DIR, "resultados_brutos.csv"), "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

# remove os dados gerados relacionados ao menor e maior TTFT
combined = sorted(zip(results, metrics_per_run), key=lambda item: item[0]["ttft_ms"])
trimmed = combined[1:-1]  # remove o menor e o maior
trimmed_rows = [item[0] for item in trimmed]
trimmed_metrics = [item[1] for item in trimmed]

# salva os dados tratados
with open(os.path.join(TELEMETRIA_DIR, "resultados_tratados.csv"), "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=trimmed_rows[0].keys())
    writer.writeheader()
    writer.writerows(trimmed_rows)

summary_values = {
    "ttft_ms": [m["ttft_ms"] for m in trimmed_metrics if m["ttft_ms"] is not None],
    "tps": [m["tps"] for m in trimmed_metrics if m["tps"] is not None],
    "load_duration_ms": [m["load_duration_ms"] for m in trimmed_metrics if m["load_duration_ms"] is not None],
    "peak_ollama_ram_used_mb": [m["peak_ollama_ram_used_mb"] for m in trimmed_metrics if m["peak_ollama_ram_used_mb"] is not None],
    "avg_ollama_ram_used_mb": [m["avg_ollama_ram_used_mb"] for m in trimmed_metrics if m["avg_ollama_ram_used_mb"] is not None],
    "avg_ollama_cpu_percent": [m["avg_ollama_cpu_percent"] for m in trimmed_metrics if m["avg_ollama_cpu_percent"] is not None],
    "rei": [m["rei"] for m in trimmed_metrics if m["rei"] is not None],
}

print("\n=== RESUMO (sem menor/maior TTFT) ===")
print(f"Runs usados: {len(trimmed_rows)}")

with open(os.path.join(TELEMETRIA_DIR, "resultados_estatisticas.csv"), "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["metric", "mean", "median", "desvio"])
    writer.writeheader()

    for metric, values in summary_values.items():
        mean, median, desvio = summarize(values)
        if mean is None:
            continue
        writer.writerow({"metric": metric, "mean": mean, "median": median, "desvio": desvio})