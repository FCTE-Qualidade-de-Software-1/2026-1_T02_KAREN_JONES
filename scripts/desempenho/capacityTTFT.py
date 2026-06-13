import requests
import json
import time
import csv
import statistics
from datetime import datetime
import os as os

URL = "http://127.0.0.1:11434/api/generate"
MODEL = "qwen2.5:3b"
N_RUNS = 7  # 7 execuções por tamanho de contexto, remove menor/maior TTFT -> 5 usados
KEEP_ALIVE = "5m"
NUM_CTX = 8192  # janela de contexto grande o suficiente pra caber o prompt de ~4096 tokens + resposta
NUM_PREDICT = 100  # limita a geração pra manter a fase de "eval" comparável entre tamanhos

TELEMETRIA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "telemetria")
os.makedirs(TELEMETRIA_DIR, exist_ok=True)
MONITOR_FILE = os.path.join(TELEMETRIA_DIR, "monitor_recursos.csv")

# Prompt base com ~253 tokens (medido via prompt_eval_count do Ollama)
BASE_PROMPT = (
    "Explique como a abordagem GQM pode ser aplicada para definir métricas de eficiência de desempenho de um sistema de software, segundo a norma ISO/IEC 25010. Considere um objetivo voltado para avaliar a eficiência de um modelo de linguagem executado localmente via Ollama, descrevendo: (1) como formular o objetivo no formato GQM (propósito, objeto, foco de qualidade, ponto de vista, contexto); (2) quais perguntas seriam derivadas desse objetivo para investigar comportamento temporal, utilização de recursos e capacidade; (3) quais métricas concretas poderiam responder a essas perguntas, como tempo até o primeiro token (TTFT), tokens por segundo (TPS), pico de uso de memória RAM, percentual médio de uso de CPU. Além disso, relacione essas métricas com as práticas recomendadas pelo PSM (Practical Software and Systems Measurement)."
)

# repeats aproximados pra atingir cada tamanho alvo (o valor real é medido via prompt_eval_count)
CONTEXT_SIZES = [
    ("~256", 1),
    ("~512", 2),
    ("~1024", 4),
    ("~2048", 8),
    ("~4096", 16),
]


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


def build_prompt(repeats):
    return " ".join([BASE_PROMPT] * repeats)


def warmup(prompt):
    """Descarta 1 run para estabilizar modelo e KV cache antes das medições."""
    try:
        run_once(prompt)
    except Exception as e:
        print(f"  [warm-up] erro (ignorado): {e}")


def run_once(prompt):
    ts_inicio = datetime.now().isoformat(timespec="milliseconds")
    start_time = time.perf_counter()
    ttft = None
    created_at_first = None
    final_data = None

    with requests.post(
        URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "keep_alive": KEEP_ALIVE,
            "stream": True,
            "options": {
                "num_ctx": NUM_CTX,
                "num_predict": NUM_PREDICT,
            },
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

            if chunk.get("done", False):
                final_data = chunk

    ts_fim = datetime.now().isoformat(timespec="milliseconds")
    return ttft, created_at_first, final_data, ts_inicio, ts_fim


# ---------------------------------------------------------------------------

all_results = []
trimmed_results = []
summary_by_size = []

for label, repeats in CONTEXT_SIZES:
    prompt = build_prompt(repeats)
    print(f"\n=== Tamanho de contexto {label} (repeats={repeats}) ===")
    print(f"  [warm-up] estabilizando modelo e KV cache...")
    warmup(prompt)

    runs_for_size = []

    for i in range(N_RUNS):
        ttft, created_at_first, final_data, ts_inicio, ts_fim = run_once(prompt)

        peak_ram, avg_cpu, avg_ram = compute_monitor_metrics(MONITOR_FILE, ts_inicio, ts_fim)

        row = {
            "context_label": label,
            "repeats": repeats,
            "run": i + 1,
            "ts_inicio": ts_inicio,
            "ts_fim": ts_fim,
            "ts_first_chunk_ollama": created_at_first,
            "ttft_ms": round(ttft, 2),
            "prompt_eval_count": final_data["prompt_eval_count"],
            "prompt_eval_duration_ms": ns_to_ms(final_data["prompt_eval_duration"]),
            "load_duration_ms": ns_to_ms(final_data["load_duration"]),
            "eval_count": final_data["eval_count"],
            "eval_duration_ms": ns_to_ms(final_data["eval_duration"]),
            "total_duration_ms": ns_to_ms(final_data["total_duration"]),
            "peak_ollama_ram_used_mb": peak_ram,
            "avg_ollama_ram_used_mb": avg_ram,
            "avg_ollama_cpu_percent": avg_cpu,
        }

        all_results.append(row)
        runs_for_size.append(row)

        print(
            f"  Run {i+1}/{N_RUNS} -> TTFT: {row['ttft_ms']} ms | "
            f"prompt_eval_count: {row['prompt_eval_count']} | "
            f"prompt_eval_duration: {row['prompt_eval_duration_ms']} ms | "
            f"Pico RAM Ollama: {row['peak_ollama_ram_used_mb']} MB"
        )

    # remove menor e maior TTFT; guard para N_RUNS < 3
    sorted_runs = sorted(runs_for_size, key=lambda r: r["ttft_ms"])
    trimmed = sorted_runs[1:-1] if len(sorted_runs) >= 3 else sorted_runs
    trimmed_results.extend(trimmed)

    ttft_mean, ttft_median, ttft_desvio = summarize([r["ttft_ms"] for r in trimmed])
    prompt_eval_count_mean, _, _ = summarize([r["prompt_eval_count"] for r in trimmed])
    prompt_eval_duration_mean, prompt_eval_duration_median, prompt_eval_duration_desvio = summarize(
        [r["prompt_eval_duration_ms"] for r in trimmed]
    )
    peak_ram_mean, peak_ram_median, peak_ram_desvio = summarize(
        [r["peak_ollama_ram_used_mb"] for r in trimmed if r["peak_ollama_ram_used_mb"] is not None]
    )
    avg_ram_mean, _, _ = summarize(
        [r["avg_ollama_ram_used_mb"] for r in trimmed if r["avg_ollama_ram_used_mb"] is not None]
    )
    avg_cpu_mean, _, _ = summarize(
        [r["avg_ollama_cpu_percent"] for r in trimmed if r["avg_ollama_cpu_percent"] is not None]
    )

    summary_by_size.append(
        {
            "context_label": label,
            "prompt_eval_count_mean": prompt_eval_count_mean,
            "ttft_ms_mean": ttft_mean,
            "ttft_ms_median": ttft_median,
            "ttft_ms_desvio": ttft_desvio,
            "prompt_eval_duration_ms_mean": prompt_eval_duration_mean,
            "prompt_eval_duration_ms_median": prompt_eval_duration_median,
            "prompt_eval_duration_ms_desvio": prompt_eval_duration_desvio,
            "peak_ollama_ram_used_mb_mean": peak_ram_mean,
            "peak_ollama_ram_used_mb_median": peak_ram_median,
            "peak_ollama_ram_used_mb_desvio": peak_ram_desvio,
            "avg_ollama_ram_used_mb_mean": avg_ram_mean,
            "avg_ollama_cpu_percent_mean": avg_cpu_mean,
        }
    )

# ---------------------------------------------------------------------------
# ED-3.1 - Fator de Escalonamento de Contexto (CSF)
# CSF = TTFT(tamanho) / TTFT(~256)  -> quanto o TTFT cresce em relação ao baseline

baseline_ttft = summary_by_size[0]["ttft_ms_mean"]
for row in summary_by_size:
    if baseline_ttft:
        row["csf"] = round(row["ttft_ms_mean"] / baseline_ttft, 4)
    else:
        row["csf"] = None

# ---------------------------------------------------------------------------
# ED-3.2 - Taxa de Crescimento do KV Cache (KVCGR)
# KVCGR = (RAM_pico(n) - RAM_pico(256)) / (tokens(n) - tokens(256))
# Crescimento de RAM de pico em relação ao baseline ~256 tokens, por token adicionado.
# Referência: crescimento previsível ≤ 0,5 MB/token; excessivo > 1,0 MB/token.

baseline = summary_by_size[0]
baseline_ram    = baseline["peak_ollama_ram_used_mb_mean"]
baseline_tokens = baseline["prompt_eval_count_mean"] or 0

for idx, row in enumerate(summary_by_size):
    if idx == 0:
        row["kvcgr_mb_per_token"] = None
        continue

    curr_ram     = row["peak_ollama_ram_used_mb_mean"]
    delta_tokens = (row["prompt_eval_count_mean"] or 0) - baseline_tokens

    if curr_ram is not None and baseline_ram is not None and delta_tokens:
        delta_ram = curr_ram - baseline_ram
        row["kvcgr_mb_per_token"] = round(delta_ram / delta_tokens, 4)
    else:
        row["kvcgr_mb_per_token"] = None

# ---------------------------------------------------------------------------
# salva CSVs

with open(os.path.join(TELEMETRIA_DIR, "capacity_resultados_brutos.csv"), "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=all_results[0].keys())
    writer.writeheader()
    writer.writerows(all_results)

with open(os.path.join(TELEMETRIA_DIR, "capacity_resultados_tratados.csv"), "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=trimmed_results[0].keys())
    writer.writeheader()
    writer.writerows(trimmed_results)

with open(os.path.join(TELEMETRIA_DIR, "capacity_resumo.csv"), "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=summary_by_size[0].keys())
    writer.writeheader()
    writer.writerows(summary_by_size)

# ---------------------------------------------------------------------------
# print do resumo

print("\n=== RESUMO ED-3.1 (CSF) e ED-3.2 (KVCGR) ===")
print(f"Runs por tamanho: {N_RUNS} (5 usados após remover menor/maior TTFT)\n")

header = (
    f"{'contexto':<8} | {'tokens':>7} | {'TTFT médio (ms)':>16} | "
    f"{'desvio':>7} | {'CSF':>7} | {'RAM pico (MB)':>14} | {'KVCGR (MB/token)':>16}"
)
print(header)
print("-" * len(header))

for row in summary_by_size:
    kvcgr = row["kvcgr_mb_per_token"]
    print(
        f"{row['context_label']:<8} | {row['prompt_eval_count_mean']:>7} | "
        f"{row['ttft_ms_mean']:>16} | {row['ttft_ms_desvio']:>7} | {row['csf']:>7} | "
        f"{row['peak_ollama_ram_used_mb_mean']:>14} | "
        f"{(kvcgr if kvcgr is not None else '-'):>16}"
    )